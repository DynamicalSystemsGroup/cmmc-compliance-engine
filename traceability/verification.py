"""Closure-rule verification — SHACL suite + evidence re-hashing.

Ported from ADCS-lifecycle-demo/traceability/verification.py, retargeted to the
compliance engine. Runs the `ontology/cmmc_shapes.ttl` closure suite (including
`ControlShape`, `PoamLegalityShape`, and `ContradictionShape` R13) against the
assembled Dataset via pyshacl, PLUS the runtime re-verification closure: re-hash
every `ce:Evidence` node and flag any content-hash mismatch.

Naming discipline: SHACL conformance and hash-matching are **verification**
(automated, fully specified). Human attestation (traceability.attestation) is
separate — this module never asserts a control MET.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pyshacl
from rdflib import Dataset, Graph, URIRef
from rdflib.namespace import RDF

from ontology.prefixes import CE
from evidence.hashing import hash_evidence

ROOT = Path(__file__).resolve().parent.parent
SHAPES_PATH = ROOT / "ontology" / "cmmc_shapes.ttl"


@dataclass
class ShapeViolation:
    shape: str          # SHACL source-shape IRI (or "?")
    focus: str          # focus node IRI
    path: str | None    # violating property path
    message: str        # human-readable failure message
    severity: str       # sh:Violation / sh:Warning / sh:Info


@dataclass
class ReverificationMismatch:
    evidence: str       # evidence IRI
    expected: str       # stored ce:contentHash
    actual: str         # recomputed content hash (hash_evidence(model_hash))


@dataclass
class VerificationReport:
    conforms: bool
    shape_violations: list[ShapeViolation] = field(default_factory=list)
    reverification_mismatches: list[ReverificationMismatch] = field(default_factory=list)
    shape_results_text: str = ""

    def shapes_named(self) -> set[str]:
        """Local names of every shape that produced a violation."""
        return {v.shape.rsplit("#", 1)[-1].rsplit("/", 1)[-1] for v in self.shape_violations}

    def summary_lines(self) -> list[str]:
        lines = []
        status = "PASS" if self.conforms else "FAIL"
        lines.append(f"Closure-rule verification: {status}")
        lines.append(f"  SHACL violations:     {len(self.shape_violations)}")
        lines.append(f"  Re-verification:      {len(self.reverification_mismatches)} mismatches")
        for v in self.shape_violations[:10]:
            lines.append(f"    - {v.shape.rsplit('#', 1)[-1]}: {v.message[:80]}")
        for m in self.reverification_mismatches:
            lines.append(f"    - hash mismatch {m.evidence}: "
                         f"expected {m.expected[:12]}, got {m.actual[:12]}")
        return lines


def _flatten(ds: Graph | Dataset) -> Graph:
    """Flatten a Dataset's union (all named graphs) into one Graph for pyshacl.

    Works regardless of default_union by walking quads."""
    g = Graph()
    if isinstance(ds, Dataset):
        for s, p, o, _ctx in ds.quads((None, None, None, None)):
            g.add((s, p, o))
    else:
        for triple in ds:
            g.add(triple)
    return g


_SH = "http://www.w3.org/ns/shacl#"


def _parse_shape_violations(report_graph: Graph) -> list[ShapeViolation]:
    """Extract structured violation records from pyshacl's report graph."""
    sh_result = URIRef(f"{_SH}ValidationResult")
    sh_focus = URIRef(f"{_SH}focusNode")
    sh_path = URIRef(f"{_SH}resultPath")
    sh_msg = URIRef(f"{_SH}resultMessage")
    sh_sev = URIRef(f"{_SH}resultSeverity")
    sh_shape = URIRef(f"{_SH}sourceShape")

    out: list[ShapeViolation] = []
    for result in report_graph.subjects(RDF.type, sh_result):
        focus = next(iter(report_graph.objects(result, sh_focus)), None)
        path = next(iter(report_graph.objects(result, sh_path)), None)
        msg = next(iter(report_graph.objects(result, sh_msg)), None)
        sev = next(iter(report_graph.objects(result, sh_sev)), None)
        shape = next(iter(report_graph.objects(result, sh_shape)), None)
        out.append(ShapeViolation(
            shape=str(shape) if shape else "?",
            focus=str(focus) if focus else "?",
            path=str(path) if path else None,
            message=str(msg) if msg else "",
            severity=str(sev) if sev else "?",
        ))
    return out


def verify_shacl(
    ds: Graph | Dataset, shapes_path: Path = SHAPES_PATH
) -> tuple[bool, list[ShapeViolation], str]:
    """Run pyshacl against `ds` with the cmmc_shapes closure suite."""
    shapes = Graph()
    shapes.parse(shapes_path, format="turtle")
    data = _flatten(ds)
    conforms, report_graph, results_text = pyshacl.validate(
        data, shacl_graph=shapes,
        inference="none", allow_warnings=True, advanced=True,
    )
    return conforms, _parse_shape_violations(report_graph), results_text


def verify_reverification(ds: Graph | Dataset) -> list[ReverificationMismatch]:
    """Re-verification closure — re-hash every ce:Evidence node.

    An evidence node's content hash MUST equal hash_evidence(model_hash) (the
    same chain evidence/binding.py builds). Any node whose stored ce:contentHash
    no longer matches its ce:modelHash-derived recomputation is flagged as a
    tamper/mismatch. Self-contained: needs only the node's own recorded fields.
    """
    flat = _flatten(ds)
    mismatches: list[ReverificationMismatch] = []
    for ev in flat.subjects(RDF.type, CE.Evidence, unique=True):
        stored = flat.value(ev, CE.contentHash)
        model = flat.value(ev, CE.modelHash)
        if stored is None or model is None:
            continue
        recomputed = hash_evidence(str(model))
        if recomputed != str(stored):
            mismatches.append(ReverificationMismatch(
                evidence=str(ev), expected=str(stored), actual=recomputed,
            ))
    return mismatches


def verify(
    ds: Graph | Dataset, *,
    shapes_path: Path = SHAPES_PATH,
    skip_reverification: bool = False,
) -> VerificationReport:
    """Run the full closure suite (SHACL + re-verification); structured verdict.

    `conforms` is True iff SHACL conforms AND no re-verification mismatch.
    """
    conforms, violations, text = verify_shacl(ds, shapes_path)
    mismatches: list[ReverificationMismatch] = []
    if not skip_reverification:
        mismatches = verify_reverification(ds)
    return VerificationReport(
        conforms=conforms and not mismatches,
        shape_violations=violations,
        reverification_mismatches=mismatches,
        shape_results_text=text,
    )
