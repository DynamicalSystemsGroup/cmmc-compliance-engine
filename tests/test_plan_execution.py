"""U1 — P-PLAN step model + per-stage activity emission.

Adapted from the ADCS test_plan_execution.py. The ADCS version drove a
full `run_pipeline()`; here (substrate spine only) we emit activities
directly and assert the step model:

  - STEP_NAMES enumerates the ten Factory stages.
  - plan.ttl parses, declares the root Plan, and contains a p-plan:Step
    for every STEP_NAMES entry (STEP_NAMES ↔ plan.ttl lockstep).
  - isPrecededBy relations form a DAG.
  - step_iri() resolves known names and raises KeyError on unknown ones.
  - start_step/end_step/plan_step/emit_stage_activity write activities
    into the <ce:plan-execution> named graph with correspondsToStep +
    prov:startedAtTime (and endedAtTime on completion).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from rdflib import Graph, URIRef
from rdflib.namespace import RDF

from ontology.prefixes import CE, G_PLAN_EXECUTION, P_PLAN, PROV
from pipeline.dataset import create_dataset
from pipeline.plan_execution import (
    STEP_NAMES,
    emit_stage_activity,
    end_step,
    plan_step,
    start_step,
    step_iri,
)

ROOT = Path(__file__).resolve().parent.parent
PLAN_TTL = ROOT / "pipeline" / "plan.ttl"
PLAN_IRI = URIRef(f"{CE}SOP-CMMC-TIER1-PROVISION")

EXPECTED_STEPS = {
    "LoadOrder", "FetchByHash", "Plan", "PolicyCheck", "Apply",
    "CollectEvidence", "Oracles", "Attestation", "Audit", "SignAndStore",
}


@pytest.fixture(scope="module")
def plan_graph() -> Graph:
    g = Graph()
    g.parse(PLAN_TTL, format="turtle")
    return g


# ---------------------------------------------------------------------------
# STEP_NAMES + step_iri
# ---------------------------------------------------------------------------

def test_step_names_are_the_ten_factory_stages():
    assert STEP_NAMES == EXPECTED_STEPS


def test_step_iri_resolves_known_step():
    assert step_iri("PolicyCheck") == URIRef(f"{CE}step-PolicyCheck")


def test_step_iri_raises_on_unknown_step():
    with pytest.raises(KeyError, match="Unknown plan step"):
        step_iri("NotAStage")


# ---------------------------------------------------------------------------
# plan.ttl structure (STEP_NAMES ↔ plan.ttl lockstep)
# ---------------------------------------------------------------------------

def test_plan_ttl_parses_and_is_nonempty(plan_graph):
    assert len(plan_graph) > 20


def test_plan_has_root_plan_individual(plan_graph):
    assert (PLAN_IRI, RDF.type, P_PLAN.Plan) in plan_graph


def test_every_step_name_appears_in_plan_ttl(plan_graph):
    declared = {
        str(s) for s in plan_graph.subjects(P_PLAN.isStepOfPlan, PLAN_IRI)
    }
    missing = [n for n in STEP_NAMES if str(step_iri(n)) not in declared]
    assert not missing, f"plan.ttl missing steps referenced by code: {missing}"


def test_plan_ttl_declares_no_extra_steps(plan_graph):
    """Every p-plan:Step in the plan corresponds to a known STEP_NAMES entry."""
    declared = {
        str(s) for s in plan_graph.subjects(P_PLAN.isStepOfPlan, PLAN_IRI)
    }
    known = {str(step_iri(n)) for n in STEP_NAMES}
    extra = declared - known
    assert not extra, f"plan.ttl declares steps not in STEP_NAMES: {extra}"


def test_predecessor_relations_form_dag(plan_graph):
    edges: dict[URIRef, set[URIRef]] = {}
    for s, _, o in plan_graph.triples((None, P_PLAN.isPrecededBy, None)):
        edges.setdefault(s, set()).add(o)

    visiting: set[URIRef] = set()
    visited: set[URIRef] = set()

    def dfs(node: URIRef) -> None:
        if node in visiting:
            raise AssertionError(f"Predecessor cycle through {node}")
        if node in visited:
            return
        visiting.add(node)
        for nxt in edges.get(node, ()):
            dfs(nxt)
        visiting.remove(node)
        visited.add(node)

    for n in list(edges):
        dfs(n)
    # sanity: the chain actually wired predecessors up
    assert edges, "no isPrecededBy edges declared in plan.ttl"


# ---------------------------------------------------------------------------
# Runtime activity emission
# ---------------------------------------------------------------------------

def test_start_step_emits_activity_into_plan_execution_graph():
    ds = create_dataset()
    activity = start_step(ds, "Apply")
    pe = URIRef(G_PLAN_EXECUTION)

    quads = list(ds.quads((activity, None, None, pe)))
    preds = {p for _, p, _, _ in quads}
    assert P_PLAN.correspondsToStep in preds
    assert PROV.startedAtTime in preds
    assert (activity, P_PLAN.correspondsToStep, step_iri("Apply"), pe) in ds
    assert (activity, RDF.type, P_PLAN.Activity, pe) in ds


def test_start_step_rejects_unknown_step():
    ds = create_dataset()
    with pytest.raises(KeyError, match="Unknown plan step"):
        start_step(ds, "Nope")


def test_end_step_sets_ended_at_time():
    ds = create_dataset()
    activity = start_step(ds, "Audit")
    end_step(ds, activity)
    pe = URIRef(G_PLAN_EXECUTION)
    assert list(ds.quads((activity, PROV.endedAtTime, None, pe)))


def test_plan_step_context_manager_records_start_and_end():
    ds = create_dataset()
    pe = URIRef(G_PLAN_EXECUTION)
    with plan_step(ds, "SignAndStore") as activity:
        assert list(ds.quads((activity, PROV.startedAtTime, None, pe)))
    assert list(ds.quads((activity, PROV.endedAtTime, None, pe)))


def test_plan_step_records_end_even_on_exception():
    ds = create_dataset()
    pe = URIRef(G_PLAN_EXECUTION)
    captured = {}
    with pytest.raises(RuntimeError):
        with plan_step(ds, "Oracles") as activity:
            captured["a"] = activity
            raise RuntimeError("stage blew up")
    assert list(ds.quads((captured["a"], PROV.endedAtTime, None, pe)))


def test_emit_stage_activity_declares_pipeline_agent():
    ds = create_dataset()
    emit_stage_activity(ds, "LoadOrder")
    pe = URIRef(G_PLAN_EXECUTION)
    agent = CE["agent/pipeline-runner"]
    assert (agent, RDF.type, PROV.SoftwareAgent, pe) in ds
