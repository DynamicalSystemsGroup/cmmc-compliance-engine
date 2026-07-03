"""COP build + human attestation (per-deliverable affirmation + spillover)."""

import sys
from pathlib import Path

import pytest
from rdflib import URIRef

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "order-compiler"))

import cop  # noqa: E402
import rule_library as rl  # noqa: E402
from ontology.prefixes import CE, EARL, PROV  # noqa: E402
from rdflib.namespace import RDF  # noqa: E402
from pipeline.dataset import create_dataset, graph_for, load_into  # noqa: E402

CATALOG = _ROOT / "ontology" / "cmmc-edit.ttl"
TIER1 = _ROOT / "structural" / "tier1.ttl"
COP_DRAFT = _ROOT / "fixtures" / "nv012" / "cop_draft.ttl"
OBLIGATIONS = _ROOT / "order-compiler" / "obligations.ttl"
NOW = "2026-07-02T00:00:00+00:00"


def _base_ds():
    d = create_dataset()
    load_into(d, "ontology", CATALOG)
    load_into(d, "structural", TIER1)
    load_into(d, "order", COP_DRAFT)
    return d


def test_attest_cop_records_manual_assertion_in_order_graph():
    ds = _base_ds()
    obl = rl.load_obligations(COP_DRAFT)
    att = cop.attest_cop(ds, obl, auto=False, now=NOW)
    assert att.is_attested
    assert att.mode == "manual"

    order_g = graph_for(ds, "order")
    a = att.attestation_iri
    assert (a, RDF.type, PROV.Activity) in order_g
    assert (a, RDF.type, EARL.Assertion) in order_g
    assert (a, CE.attestsCOP, att.cop_iri) in order_g
    assert (a, CE.outcome, EARL.passed) in order_g
    assert (a, CE.attestationMode, EARL.manual) in order_g


def test_auto_flag_downgrades_to_semiauto():
    ds = _base_ds()
    obl = rl.load_obligations(COP_DRAFT)
    att = cop.attest_cop(ds, obl, auto=True, now=NOW)
    assert att.mode == "semiAuto"
    order_g = graph_for(ds, "order")
    assert (att.attestation_iri, CE.attestationMode, EARL.semiAuto) in order_g


def test_plain_deliverable_forces_no_env_control_affirmation():
    ds = _base_ds()
    obl = rl.load_obligations(COP_DRAFT)
    att = cop.attest_cop(ds, obl, auto=True, now=NOW)
    # The plain deliverable resolves to {} (rule_library) ...
    deliv = obl["OBL-NV012-DELIV-TOOL"]
    assert rl.resolve(deliv) == set()
    # ... and gets an explicit affirmation recorded.
    assert att.affirmations.get("OBL-NV012-DELIV-TOOL") is True
    order_g = graph_for(ds, "order")
    aff = CE["affirmation/OBL-NV012-DELIV-TOOL"]
    assert (aff, RDF.type, CE.DeliverableAffirmation) in order_g
    assert (att.attestation_iri, CE.hasAffirmation, aff) in order_g


def test_cui_marked_deliverable_surfaces_spillover_before_gate1():
    """The canonical COP's OBL-VENDOR-PORTAL (CUI deliverable) must NOT be
    silently affirmed — attest_cop re-raises SpilloverReviewRequired."""
    ds = _base_ds()
    canon = rl.load_obligations(OBLIGATIONS)
    with pytest.raises(rl.SpilloverReviewRequired) as exc:
        cop.attest_cop(ds, canon, auto=True, now=NOW)
    assert exc.value.obligation.name == "OBL-VENDOR-PORTAL"


def test_acknowledged_spillover_is_not_auto_affirmed():
    """When the officer acknowledges the spillover, attestation proceeds but the
    CUI deliverable does NOT receive a 'no environment control' affirmation."""
    ds = _base_ds()
    canon = rl.load_obligations(OBLIGATIONS)
    att = cop.attest_cop(
        ds, canon, auto=True, now=NOW,
        acknowledge_spillovers={"OBL-VENDOR-PORTAL"},
    )
    assert att.is_attested
    # The plain deliverable (OBL-AUDIT-EVIDENCE) IS affirmed ...
    assert att.affirmations.get("OBL-AUDIT-EVIDENCE") is True
    # ... the CUI deliverable is NOT.
    assert "OBL-VENDOR-PORTAL" not in att.affirmations


def test_officer_agent_declared():
    ds = _base_ds()
    obl = rl.load_obligations(COP_DRAFT)
    att = cop.attest_cop(ds, obl, auto=True, now=NOW)
    order_g = graph_for(ds, "order")
    assert (att.officer, RDF.type, PROV.Agent) in order_g
    assert isinstance(att.officer, URIRef)
