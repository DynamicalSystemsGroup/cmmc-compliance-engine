"""Deterministic SHA-256 hashing for evidence identity.

SCAFFOLD. Port ADCS-lifecycle-demo/evidence/hashing.py **verbatim** — the
functions there are domain-agnostic:

    hash_structural_model(graph)      -> canonical hash of an RDF model
    hash_docker_image(dockerfile, ctx)-> (dockerfile_hash, build_context_hash)
    hash_* / hash_evidence(...)       -> combined evidence hash

Then add the two compliance-specific helpers below. Content-addressing is
SHA-256 keyed into the tiered registry (GCS/Azure Blob) — NOT IPFS.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _serialize_for_hash(data: dict) -> str:
    """Deterministic JSON for hashing (sorted keys)."""
    return json.dumps(data, sort_keys=True, default=str)


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
