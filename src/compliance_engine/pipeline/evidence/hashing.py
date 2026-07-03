"""Deterministic SHA-256 hashing for evidence identity.

Pure functions — no state. Content-addressing is SHA-256 keyed into the
tiered registry (GCS/Azure Blob) — NOT IPFS.

Ported from ``ADCS-lifecycle-demo/evidence/hashing.py``. The RDF/model and
evidence-combining helpers are domain-agnostic and reused as-is:

    hash_structural_model(graph)  -> canonical hash of an RDF model
    hash_evidence(...)            -> combined evidence hash
    _serialize_for_hash(...)      -> deterministic JSON for hashing

The two compliance-specific helpers (``hash_check_result``,
``hash_config_export``) pin the exact bytes of a policy-as-code check result
or a live-config export so the BOM is tamper-evident.

Deliberately NOT ported: ``hash_proof`` / ``hash_simulation`` (they import
``sympy``, which this project dropped) and ``hash_docker_image`` (no Docker
evidence in scope).
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from rdflib import Graph


def _serialize_for_hash(data: dict) -> str:
    """JSON-serialize a dict deterministically for hashing (sorted keys)."""
    return json.dumps(data, sort_keys=True, default=str)


def hash_structural_model(graph: Graph) -> str:
    """Deterministic SHA-256 hash of the structural RDF model.

    Produces a canonical hash by:
    1. Extracting all triples as (s, p, o) N-Triples strings
    2. Replacing blank node identifiers with a content-based hash of
       all non-blank triples reachable from that blank node
    3. Sorting and hashing the result

    For simplicity, we flatten blank-node subgraphs: triples involving
    blank nodes are replaced by their grounded content (the non-blank
    subjects/objects they ultimately connect).
    """
    from rdflib import BNode, URIRef, Literal

    # Collect grounded triples (no blank nodes) directly
    grounded_lines: list[str] = []

    # For blank-node triples, collect the chain of properties
    # and serialize as: subject -> predicate chain -> leaf values
    def _nt_term(term):
        if isinstance(term, URIRef):
            return f"<{term}>"
        if isinstance(term, Literal):
            if term.datatype:
                return f'"{term}"^^<{term.datatype}>'
            return f'"{term}"'
        return f"_:blank"  # placeholder, will be skipped

    def _collect_bnode_properties(bnode, visited=None):
        """Recursively collect all property-value pairs from a blank node."""
        if visited is None:
            visited = set()
        if bnode in visited:
            return []
        visited.add(bnode)
        pairs = []
        for p, o in graph.predicate_objects(bnode):
            if isinstance(o, BNode):
                sub_pairs = _collect_bnode_properties(o, visited)
                for sp_, so_ in sub_pairs:
                    pairs.append((f"{_nt_term(p)}/{sp_}", so_))
            else:
                pairs.append((_nt_term(p), _nt_term(o)))
        return sorted(pairs)

    for s, p, o in graph:
        if isinstance(s, BNode) and isinstance(o, BNode):
            continue  # skip pure blank-to-blank (will be captured via parent)
        if isinstance(s, BNode):
            continue  # blank subjects are captured when their parent references them
        if isinstance(o, BNode):
            # Inline the blank node's content
            props = _collect_bnode_properties(o)
            for prop_path, value in props:
                grounded_lines.append(f"{_nt_term(s)} {_nt_term(p)}/{prop_path} {value} .")
        else:
            grounded_lines.append(f"{_nt_term(s)} {_nt_term(p)} {_nt_term(o)} .")

    canonical = "\n".join(sorted(grounded_lines))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def hash_evidence(
    model_hash: str,
    proof_hash: str | None = None,
    sim_hash: str | None = None,
) -> str:
    """Combined evidence hash from model, proof, and simulation hashes."""
    data: dict[str, str | None] = {
        "model_hash": model_hash,
        "proof_hash": proof_hash,
        "sim_hash": sim_hash,
    }
    serialized = _serialize_for_hash(data)
    return hashlib.sha256(serialized.encode()).hexdigest()


def hash_check_result(tool: str, control_id: str, result: dict[str, Any]) -> str:
    """SHA-256 of a policy-as-code check result (OPA/Checkov/Trivy/Azure Policy).

    `result` should carry at least {"status": "PASS|FAIL", "detail": ...} plus
    the raw tool output. The hash pins the exact result bytes so the BOM is
    tamper-evident.
    """
    payload = {"tool": tool, "control": control_id, "result": result}
    return hashlib.sha256(_serialize_for_hash(payload).encode()).hexdigest()


def hash_config_export(source: str, control_id: str, config: dict[str, Any]) -> str:
    """SHA-256 of a live-config export (MFA policy, Org Policy, IAM binding, ...).

    `source` names the export origin (e.g. "workspace.2sv", "gcp.org_policy").
    """
    payload = {"source": source, "control": control_id, "config": config}
    return hashlib.sha256(_serialize_for_hash(payload).encode()).hexdigest()
