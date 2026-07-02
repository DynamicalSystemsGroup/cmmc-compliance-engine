"""U5 — Gate 1 planning-coverage audit (forward / backward / no-paper-claim)."""

import sys
from pathlib import Path

import pytest
from rdflib import BNode
from rdflib.namespace import RDF

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "order-compiler"))

import gate1  # noqa: E402
from ontology.prefixes import CE, CMMC, SYSML  # noqa: E402
from pipeline.dataset import create_dataset, graph_for, load_into  # noqa: E402

CATALOG = _ROOT / "ontology" / "cmmc-edit.ttl"
TIER1 = _ROOT / "structural" / "tier1.ttl"

# The full Tier-1-covered required set (== the 22 controls tier1 claims).
FULL_REQUIRED = {
    "IA.L2-3.5.3", "IA.L2-3.5.2", "IA.L2-3.5.4",
    "SC.L2-3.13.11", "SC.L2-3.13.10", "SC.L2-3.13.16",
    "AC.L2-3.1.1", "AC.L2-3.1.2", "AC.L2-3.1.5", "AC.L2-3.1.3",
    "SC.L2-3.13.1",
    "AU.L2-3.3.1", "AU.L2-3.3.2", "AU.L2-3.3.5",
    "CM.L2-3.4.6", "CM.L2-3.4.7", "CM.L2-3.4.1", "CM.L2-3.4.2",
    "SI.L2-3.14.3", "SI.L2-3.14.6",
    "PE.L2-3.10.1", "PE.L2-3.10.2",
}


@pytest.fixture()
def ds():
    d = create_dataset()
    load_into(d, "ontology", CATALOG)
    load_into(d, "structural", TIER1)
    return d


def test_full_coverage_passes(ds):
    report = gate1.run_gate1(FULL_REQUIRED, ds)
    assert report.passed
    assert report.forward.passed and report.backward.passed and report.untestable.passed
    # every required control maps to ≥1 module; all 10 modules included.
    assert len(report.included_modules) == 10
    assert all(report.forward_map[c] for c in FULL_REQUIRED)


def test_forward_gap_names_control_and_weight(ds):
    """A required 5-point control with no claiming module ⇒ forward FAIL."""
    required = set(FULL_REQUIRED) | {"AC.L2-3.1.12"}  # weight 5, no module
    report = gate1.run_gate1(required, ds)
    assert not report.passed
    assert not report.forward.passed
    assert report.gap_controls() == ["AC.L2-3.1.12"]
    (failure,) = report.forward.failures
    assert failure.details["weight"] == 5


def test_backward_orphan_flagged(ds):
    """An included module claiming no required control ⇒ orphan (backward FAIL)."""
    required = {"IA.L2-3.5.3", "IA.L2-3.5.2", "IA.L2-3.5.4"}   # only MFA
    report = gate1.run_gate1(
        required, ds,
        included_modules={"Workspace2SV_CUI_OU", "CMEK_KeyRing"},  # CMEK is orphan
    )
    assert not report.passed
    assert not report.backward.passed
    assert report.orphan_modules() == ["CMEK_KeyRing"]
    assert report.forward.passed  # the MFA controls are still covered


def test_paper_claim_without_verification_method_rejected(ds):
    """A module claiming a required control but with no cmmc:verificationMethod
    ⇒ rejected as a paper claim."""
    struct = graph_for(ds, "structural")
    paper = CE["PaperClaim"]
    rel = BNode()
    struct.add((paper, RDF.type, SYSML.PartUsage))
    struct.add((paper, SYSML.ownedRelationship, rel))
    struct.add((rel, RDF.type, SYSML.SatisfyRequirementUsage))
    struct.add((rel, SYSML.satisfiedRequirement, CMMC["AC.L2-3.1.1"]))
    struct.add((paper, CMMC.controlsSatisfied, CMMC["AC.L2-3.1.1"]))
    # deliberately NO cmmc:verificationMethod

    report = gate1.run_gate1({"AC.L2-3.1.1"}, ds)
    assert not report.passed
    assert not report.untestable.passed
    assert "PaperClaim" in report.paper_claim_modules()


def test_render_reports_status(ds):
    ok = gate1.run_gate1(FULL_REQUIRED, ds).render()
    assert "PASS" in ok
    bad = gate1.run_gate1(FULL_REQUIRED | {"AC.L2-3.1.12"}, ds).render()
    assert "FAIL" in bad
    assert "AC.L2-3.1.12" in bad


def test_empty_required_is_vacuously_covered(ds):
    report = gate1.run_gate1(set(), ds)
    assert report.passed
    assert report.included_modules == {}
