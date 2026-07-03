"""Order compiler tests: refuse-first (Gate 1 / unattested) then happy path.

Per the plan's execution note, gap-detection is proven BEFORE the happy path.
"""

import sys
from pathlib import Path

import pytest
from rdflib.namespace import RDF

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "order-compiler"))

import compiler  # noqa: E402
import cop  # noqa: E402
import rule_library as rl  # noqa: E402
from ontology.prefixes import CE, CMMC, PROV  # noqa: E402
from pipeline.dataset import graph_for  # noqa: E402

COP_DRAFT = _ROOT / "fixtures" / "nv012" / "cop_draft.ttl"
OBLIGATIONS = _ROOT / "order-compiler" / "obligations.ttl"
NOW = "2026-07-02T00:00:00+00:00"


def _attested(ds, obligations, **kw):
    return cop.attest_cop(ds, obligations, auto=True, now=NOW, **kw)


# ---------------------------------------------------------------------------
# REFUSE FIRST — Gate 1 gap detection before any happy path
# ---------------------------------------------------------------------------

def test_gate1_gap_refuses_order_and_names_control():
    """Omit a module for a 5-point control ⇒ Order refused; gap names it.

    Track A + B now claim all 110 catalog controls, so to exercise the gap
    path we STRIP one module's claim from the loaded graph before Gate 1
    runs. AC.L2-3.1.12 (5-pt) is claimed by VPNAccess_BeyondCorp — remove
    that claim and Gate 1 must refuse.
    """
    ds, obl = compiler.load_pipeline_dataset(cop_ttl=COP_DRAFT)

    # Strip VPNAccess_BeyondCorp's claim on AC.L2-3.1.12 to synthesize a gap.
    # Gate 1 reads via the sysml:SatisfyRequirementUsage edge; drop BOTH the
    # cmmc:controlsSatisfied triple AND the satisfy-edge blank node's
    # satisfiedRequirement triple.
    from ontology.prefixes import SYSML
    struct = graph_for(ds, "structural")
    struct.remove((CE.VPNAccess_BeyondCorp, CMMC.controlsSatisfied,
                   CMMC["AC.L2-3.1.12"]))
    for rel in list(struct.objects(CE.VPNAccess_BeyondCorp, SYSML.ownedRelationship)):
        struct.remove((rel, SYSML.satisfiedRequirement, CMMC["AC.L2-3.1.12"]))

    # Require the now-unclaimed 5-point control.
    obl = dict(obl)
    obl["OBL-EXTRA-MFA-REMOTE"] = rl.Obligation(
        "OBL-EXTRA-MFA-REMOTE", rl.DATA, derives=frozenset({"AC.L2-3.1.12"})
    )
    att = _attested(ds, obl)
    with pytest.raises(compiler.Gate1Failed) as exc:
        compiler.compile_order(ds, obl, att, now=NOW)

    report = exc.value.report
    assert not report.passed
    assert report.gap_controls() == ["AC.L2-3.1.12"]
    assert report.forward.failures[0].details["weight"] == 5
    # The Order was NOT emitted.
    order_g = graph_for(ds, "order")
    assert (CE["Order-NV012"], RDF.type, CE.Order) not in order_g


def test_unattested_cop_is_refused():
    ds, obl = compiler.load_pipeline_dataset(cop_ttl=COP_DRAFT)
    with pytest.raises(compiler.UnattestedCOP):
        compiler.compile_order(ds, obl, None, now=NOW)


def test_backward_orphan_refuses_order():
    """Force-include an orphan module (claims nothing required) ⇒ refused."""
    ds, obl = compiler.load_pipeline_dataset(cop_ttl=COP_DRAFT)
    att = _attested(ds, obl)
    with pytest.raises(compiler.Gate1Failed) as exc:
        compiler.compile_order(
            ds, obl, att, now=NOW,
            included_modules={"Workspace2SV_CUI_OU", "CMEK_KeyRing",
                              "CUI_Users_Group", "Drive_DLP_Rules",
                              "OrgPolicy_USRegion", "AuditLog_Export",
                              "Disable_NonFedRAMP_Services", "Terraform_Baseline",
                              "Monitoring_Alerting", "CSP_Physical_Inheritance",
                              "Tier1Enclave"},  # PartDefinition, not a claiming module
        )
    # Tier1Enclave is included but claims no required control -> orphan.
    assert "Tier1Enclave" in exc.value.report.orphan_modules()


# ---------------------------------------------------------------------------
# HAPPY PATH — full-coverage NV012 COP emits a hash-referenced Order
# ---------------------------------------------------------------------------

def test_full_coverage_emits_hash_referenced_order():
    ds, obl = compiler.load_pipeline_dataset(cop_ttl=COP_DRAFT)
    att = _attested(ds, obl)
    order = compiler.compile_order(ds, obl, att, now=NOW)

    assert len(order.required_controls) == 22
    assert len(order.included_modules) == 10
    assert order.contract == "NV012"
    assert order.tier == "Tier1" and order.impact_level == "IL4"
    assert order.standard == "NIST SP 800-171 Rev 2"

    # Carries all four content-addressing hashes (64-hex SHA-256).
    for h in (order.order_hash, order.cop_hash,
              order.control_set_hash, order.coverage_proof_hash):
        assert isinstance(h, str) and len(h) == 64

    # Each included module has a content hash.
    assert all(len(h) == 64 for h in order.included_modules.values())


def test_order_rdf_emitted_into_ce_order_graph():
    ds, obl = compiler.load_pipeline_dataset(cop_ttl=COP_DRAFT)
    att = _attested(ds, obl)
    order = compiler.compile_order(ds, obl, att, now=NOW)

    g = graph_for(ds, "order")
    o = order.iri
    assert (o, RDF.type, CE.Order) in g
    assert (o, RDF.type, PROV.Entity) in g
    assert str(list(g.objects(o, CE.orderHash))[0]) == order.order_hash
    assert str(list(g.objects(o, CE.copHash))[0]) == order.cop_hash
    assert str(list(g.objects(o, CE.controlSetHash))[0]) == order.control_set_hash
    assert str(list(g.objects(o, CE.coverageProofHash))[0]) == order.coverage_proof_hash
    # 22 required controls + 10 included modules as RDF.
    assert len(list(g.objects(o, CE.requiresControl))) == 22
    assert len(list(g.objects(o, CE.includesModule))) == 10
    # A specific control + module are present.
    assert (o, CE.requiresControl, CMMC["IA.L2-3.5.3"]) in g
    assert (o, CE.includesModule, CE["Workspace2SV_CUI_OU"]) in g
    # Per-module content-hash records resolve module -> hash.
    mh = list(g.objects(o, CE.hasModuleHash))
    assert len(mh) == 10
    assert (o, CE.derivedFromCOP, order.cop_iri) in g


def test_order_hash_is_deterministic():
    ds1, o1 = compiler.load_pipeline_dataset(cop_ttl=COP_DRAFT)
    r1 = compiler.compile_order(ds1, o1, _attested(ds1, o1), now=NOW)
    ds2, o2 = compiler.load_pipeline_dataset(cop_ttl=COP_DRAFT)
    r2 = compiler.compile_order(ds2, o2, _attested(ds2, o2), now=NOW)
    assert r1.order_hash == r2.order_hash
    assert r1.cop_hash == r2.cop_hash
    assert r1.control_set_hash == r2.control_set_hash
    assert r1.coverage_proof_hash == r2.coverage_proof_hash
    assert r1.included_modules == r2.included_modules


# ---------------------------------------------------------------------------
# Deliverable / spillover semantics at the resolution layer
# ---------------------------------------------------------------------------

def test_deliverable_adds_no_required_control():
    _ds, obl = compiler.load_pipeline_dataset(cop_ttl=COP_DRAFT)
    required, _ = compiler.resolve_required_controls(obl)
    # 22 controls come only from the environment/data/personnel obligations.
    assert len(required) == 22
    # The deliverable obligation itself resolves to nothing.
    assert rl.resolve(obl["OBL-NV012-DELIV-TOOL"]) == set()


def test_cui_deliverable_triggers_spillover_before_gate1():
    """resolve() raises for the canonical CUI deliverable — surfaced before
    any Gate 1 evaluation."""
    canon = rl.load_obligations(OBLIGATIONS)
    with pytest.raises(rl.SpilloverReviewRequired):
        compiler.resolve_required_controls(canon)
    # With acknowledgement it resolves (deliverable contributes no controls).
    required, _ = compiler.resolve_required_controls(
        canon, acknowledge_spillovers={"OBL-VENDOR-PORTAL"}
    )
    assert "OBL-VENDOR-PORTAL" not in required  # sanity: it's a name, not a control
    assert len(required) == 110  # OBL-CMMC-L2 expands to the full baseline
