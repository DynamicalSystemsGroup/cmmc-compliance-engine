"""SHACL negative-shape tests for the two guardrails (contradiction / POA&M).

Constructs tiny in-memory data graphs and validates them against
ontology/cmmc_shapes.ttl with pyshacl (advanced=True for the SPARQL-based
constraints). Offline — no build artifact needed.
"""
from __future__ import annotations

from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF

CMMC = Namespace("http://dynamicalsystems.group/ontology/cmmc#")
CE = Namespace("http://dynamicalsystems.group/compliance-engine/")
EARL = Namespace("http://www.w3.org/ns/earl#")

_SHAPES = Path(__file__).resolve().parent.parent / "ontology" / "cmmc_shapes.ttl"


def _shapes() -> Graph:
    g = Graph()
    g.parse(_SHAPES, format="turtle")
    return g


def _validate(data: Graph):
    conforms, _results_graph, results_text = validate(
        data, shacl_graph=_shapes(), advanced=True
    )
    return conforms, results_text


def _control(g: Graph, cid: str, weight: int, poam_eligible: bool) -> URIRef:
    node = CMMC[cid]
    g.add((node, RDF.type, CMMC.Control))
    g.add((node, CMMC.controlId, Literal(cid)))
    g.add((node, CMMC.text, Literal("statement")))
    g.add((node, CMMC.weight, Literal(weight)))
    g.add((node, CMMC.poamEligible, Literal(poam_eligible)))
    return node


# ---------------------------------------------------------------------------
# PoamLegalityShape: weight > 1 must NOT carry a cmmc:poamItem.
# ---------------------------------------------------------------------------

def test_weight3_with_poamitem_fails_poam_legality():
    data = Graph()
    node = _control(data, "AC.L2-3.1.5", 3, False)
    data.add((node, CMMC.poamItem, URIRef("urn:ce:poam:1")))
    conforms, text = _validate(data)
    assert not conforms
    assert "POA&M legality" in text


def test_weight1_with_poamitem_is_legal():
    # 1-point control MAY sit on a POA&M -> PoamLegalityShape must not fire.
    data = Graph()
    node = _control(data, "AC.L2-3.1.3", 1, True)
    data.add((node, CMMC.poamItem, URIRef("urn:ce:poam:2")))
    _conforms, text = _validate(data)
    assert "POA&M legality" not in text


def test_weight5_without_poamitem_is_legal_for_that_shape():
    data = Graph()
    _control(data, "IA.L2-3.5.1", 5, False)
    _conforms, text = _validate(data)
    assert "POA&M legality" not in text


# ---------------------------------------------------------------------------
# ContradictionShape (R13): MET attestation over a FAILED oracle w/o override.
# ---------------------------------------------------------------------------

def _met_attestation(g: Graph, oracle_failed: bool, override: bool) -> URIRef:
    att = CE["att-1"]
    g.add((att, RDF.type, CE.Attestation))
    g.add((att, CE.attests, CMMC["AC.L2-3.1.1"]))
    g.add((att, CE.hasOutcome, EARL.passed))          # MET
    if oracle_failed:
        g.add((att, CE.oracleOutcome, EARL.failed))   # backing oracle failed
    if override:
        g.add((att, CMMC.overrideJustification, Literal("risk accepted; documented")))
    return att


def test_met_over_failed_oracle_without_override_fails_contradiction():
    data = Graph()
    _met_attestation(data, oracle_failed=True, override=False)
    conforms, text = _validate(data)
    assert not conforms
    assert "Contradiction (R13)" in text


def test_met_over_failed_oracle_with_override_clears_contradiction():
    data = Graph()
    _met_attestation(data, oracle_failed=True, override=True)
    _conforms, text = _validate(data)
    assert "Contradiction (R13)" not in text


def test_met_over_passing_oracle_no_contradiction():
    data = Graph()
    att = CE["att-2"]
    data.add((att, RDF.type, CE.Attestation))
    data.add((att, CE.attests, CMMC["AC.L2-3.1.1"]))
    data.add((att, CE.hasOutcome, EARL.passed))
    data.add((att, CE.oracleOutcome, EARL.passed))     # oracle agrees
    _conforms, text = _validate(data)
    assert "Contradiction (R13)" not in text


def test_backedby_assertion_path_also_trips_contradiction():
    # Alternate modelling: backing oracle is a linked earl:Assertion node.
    data = Graph()
    att = CE["att-3"]
    assertion = CE["oracle-assertion-3"]
    data.add((att, RDF.type, CE.Attestation))
    data.add((att, CE.attests, CMMC["SC.L2-3.13.11"]))
    data.add((att, CE.hasOutcome, EARL.passed))
    data.add((att, CE.backedBy, assertion))
    data.add((assertion, EARL.outcome, EARL.failed))
    conforms, text = _validate(data)
    assert not conforms
    assert "Contradiction (R13)" in text
