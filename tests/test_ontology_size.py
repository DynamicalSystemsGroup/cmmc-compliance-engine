"""Data-integrity / size invariants over the built cmmc.ttl."""
from __future__ import annotations

from pathlib import Path

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF

from scripts.build_ontology import build

CMMC = Namespace("http://dynamicalsystems.group/ontology/cmmc#")

EXPECTED_HISTOGRAM = {5: 42, 3: 14, 1: 52, "variable": 2}
EXCLUDED_NONDEFERRABLE = {
    "AC.L2-3.1.20", "AC.L2-3.1.22", "CA.L2-3.12.4",
    "PE.L2-3.10.3", "PE.L2-3.10.4", "PE.L2-3.10.5",
}


def _built_graph(tmp_path) -> Graph:
    out = tmp_path / "cmmc.ttl"
    build(out_file=out, manifest_file=tmp_path / "m.json", verbose=False)
    g = Graph()
    g.parse(out, format="turtle")
    return g


def test_weight_histogram(tmp_path):
    g = _built_graph(tmp_path)
    hist = {5: 0, 3: 0, 1: 0, "variable": 0}
    for c in g.subjects(RDF.type, CMMC.Control):
        if (c, CMMC.variableWeight, Literal(True)) in g:
            hist["variable"] += 1
        else:
            hist[int(g.value(c, CMMC.weight))] += 1
    assert hist == EXPECTED_HISTOGRAM


def test_every_control_has_required_fields(tmp_path):
    g = _built_graph(tmp_path)
    controls = list(g.subjects(RDF.type, CMMC.Control))
    assert len(controls) == 110
    for c in controls:
        assert g.value(c, CMMC.controlId) is not None, f"{c} missing controlId"
        assert g.value(c, CMMC.text) is not None, f"{c} missing text"
        assert g.value(c, CMMC.weight) is not None, f"{c} missing weight"
        assert g.value(c, CMMC.poamEligible) is not None, f"{c} missing poamEligible"


def test_six_excluded_controls_are_nondeferrable(tmp_path):
    g = _built_graph(tmp_path)
    by_id = {str(g.value(c, CMMC.controlId)): c for c in g.subjects(RDF.type, CMMC.Control)}
    for cid in EXCLUDED_NONDEFERRABLE:
        node = by_id[cid]
        assert (node, CMMC.nonDeferrable, Literal(True)) in g, f"{cid} not nonDeferrable"
        assert int(g.value(node, CMMC.weight)) == 1
        assert (node, CMMC.poamEligible, Literal(False)) in g


def test_total_triples_within_budget(tmp_path):
    from scripts.build_ontology import TRIPLE_BUDGET
    g = _built_graph(tmp_path)
    assert len(g) <= TRIPLE_BUDGET
