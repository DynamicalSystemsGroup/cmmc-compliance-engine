"""Per-stage P-PLAN activity emission.

Every Factory stage records its execution as a p-plan:Activity in
<ce:plan-execution> with correspondsToStep pointing at the matching
p-plan:Step from pipeline/plan.ttl. This makes the build process
queryable: SPARQL can confirm every required step executed and that
ordering was preserved — proof the SOP was followed.

The closure-rule shape enforces well-formedness:
  - every p-plan:Activity correspondsToStep exactly one p-plan:Step
  - prov:startedAtTime is set
  - (predecessor-ordering check is a runtime SPARQL ASK, not SHACL)

Usage:
    with plan_step(ds, "PolicyCheck"):
        ...stage body...

    # Or imperatively, for stages that span multiple phases:
    activity = start_step(ds, "Apply")
    ...
    end_step(ds, activity)
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator

from rdflib import Dataset, Literal, URIRef
from rdflib.namespace import RDF, XSD

from compliance_engine.ontology.prefixes import CE, P_PLAN, PROV
from compliance_engine.pipeline.dataset import graph_for

# Default agent for Factory-stage executions. Concrete identity (a
# specific engineer, or a CI runner) belongs to the attestation; this
# agent represents the pipeline orchestrator itself, which is what
# actually runs each stage.
PIPELINE_AGENT = CE["agent/pipeline-runner"]


# The Factory stages, as short-names. Each maps to a p-plan:Step IRI in
# pipeline/plan.ttl (ce:step-<name>). Keep this in sync with plan.ttl.
STEP_NAMES = {
    "LoadOrder",
    "FetchByHash",
    "Plan",
    "PolicyCheck",
    "Apply",
    "CollectEvidence",
    "Oracles",
    "Attestation",
    "Audit",
    "SignAndStore",
}


def step_iri(step_name: str) -> URIRef:
    """Resolve a stage short-name to its plan.ttl step IRI."""
    if step_name not in STEP_NAMES:
        raise KeyError(
            f"Unknown plan step {step_name!r}. "
            f"Valid steps: {sorted(STEP_NAMES)}"
        )
    return URIRef(f"{CE}step-{step_name}")


def start_step(ds: Dataset, step_name: str) -> URIRef:
    """Begin recording an activity for `step_name`. Returns its IRI."""
    started = datetime.now(timezone.utc)
    activity_id = f"exec/{step_name}-{started.strftime('%Y%m%dT%H%M%S%fZ')}"
    activity = CE[activity_id]

    plan_g = graph_for(ds, "plan_execution")
    plan_g.add((activity, RDF.type, P_PLAN.Activity))
    plan_g.add((activity, RDF.type, PROV.Activity))
    plan_g.add((activity, P_PLAN.correspondsToStep, step_iri(step_name)))
    plan_g.add((activity, PROV.startedAtTime,
                Literal(started.isoformat(), datatype=XSD.dateTime)))
    plan_g.add((activity, PROV.wasAssociatedWith, PIPELINE_AGENT))
    # Declare the pipeline agent once; idempotent if already present.
    plan_g.add((PIPELINE_AGENT, RDF.type, PROV.SoftwareAgent))
    return activity


def end_step(ds: Dataset, activity: URIRef) -> None:
    """Record completion of `activity` (sets prov:endedAtTime)."""
    plan_g = graph_for(ds, "plan_execution")
    plan_g.add((activity, PROV.endedAtTime,
                Literal(datetime.now(timezone.utc).isoformat(),
                        datatype=XSD.dateTime)))


@contextmanager
def plan_step(ds: Dataset, step_name: str) -> Iterator[URIRef]:
    """Context manager wrapping start_step / end_step.

    Always records endedAtTime on exit, even if the body raises — so the
    plan-execution record stays consistent for diagnostics.
    """
    activity = start_step(ds, step_name)
    try:
        yield activity
    finally:
        end_step(ds, activity)


def emit_stage_activity(ds: Dataset, step_name: str) -> URIRef:
    """One-shot activity emission for callers that don't want a context
    manager. Used by pipeline/runner.py to mark each stage's execution
    without re-indenting the existing stage bodies.

    Sets startedAtTime only; the runtime ordering of these activities is
    what the predecessor check validates.
    """
    return start_step(ds, step_name)
