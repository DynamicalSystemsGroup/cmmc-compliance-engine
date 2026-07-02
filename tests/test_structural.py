"""U3 — Tier 1 structural model (module ↔ control allocation).

Loads the control catalog (`ontology/cmmc-edit.ttl`, <ce:ontology>) and the
structural model (`structural/tier1.ttl`, <ce:structural>) into one named-graph
Dataset (the U1 substrate) and asserts:

  - tier1.ttl parses.
  - Referential integrity: every `cmmc:controlsSatisfied` / satisfy-edge
    `sysml:satisfiedRequirement` object is a `cmmc:Control` that EXISTS in the
    catalog (no dangling claims).
  - Every module that claims a control also carries a `cmmc:verificationMethod`
    (Gate 1's "no untestable claim" precondition).
  - The two claim representations agree (satisfy-edge ⇔ controlsSatisfied).
  - Coverage query over <ce:structural>+<ce:ontology>: per-control claiming
    modules, and the count of controls with NO machine (oracle-IRI)
    verificationMethod — the proven-vs-attested denominator.

`cmmc:verificationMethod` convention (see tier1.ttl header): an IRI names a
machine oracle/live-test (proven); a literal ("inherited:…") is manual /
CSP-inherited (attested, not machine-proven).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from rdflib import Literal, URIRef
from rdflib.namespace import RDF

from ontology.prefixes import CMMC, CE, SYSML
from pipeline.dataset import create_dataset, graph_for, load_into

ROOT = Path(__file__).resolve().parent.parent
CMMC_EDIT = ROOT / "ontology" / "cmmc-edit.ttl"
TIER1 = ROOT / "structural" / "tier1.ttl"

CONTROL = CMMC.Control
CONTROLS_SATISFIED = CMMC.controlsSatisfied
VERIFICATION_METHOD = CMMC.verificationMethod
SATISFY_USAGE = SYSML.SatisfyRequirementUsage
SATISFYING_ELEMENT = SYSML.satisfyingElement
SATISFIED_REQUIREMENT = SYSML.satisfiedRequirement

# The authoritative Tier 1 mapping — this test IS the spec for the allocation.
# Machine-verifiable modules: verificationMethod is an oracle IRI.
EXPECTED_MACHINE = {
    "Workspace2SV_CUI_OU": {"IA.L2-3.5.3", "IA.L2-3.5.2", "IA.L2-3.5.4"},
    "CMEK_KeyRing": {"SC.L2-3.13.11", "SC.L2-3.13.10", "SC.L2-3.13.16"},
    "CUI_Users_Group": {"AC.L2-3.1.1", "AC.L2-3.1.2", "AC.L2-3.1.5"},
    "Drive_DLP_Rules": {"AC.L2-3.1.3"},
    "OrgPolicy_USRegion": {"SC.L2-3.13.1"},
    "AuditLog_Export": {"AU.L2-3.3.1", "AU.L2-3.3.2", "AU.L2-3.3.5"},
    "Disable_NonFedRAMP_Services": {"CM.L2-3.4.6", "CM.L2-3.4.7"},
    "Terraform_Baseline": {"CM.L2-3.4.1", "CM.L2-3.4.2"},
    "Monitoring_Alerting": {"SI.L2-3.14.3", "SI.L2-3.14.6"},
}
# Inherited module: verificationMethod is a literal (attested, not machine).
EXPECTED_INHERITED = {
    "CSP_Physical_Inheritance": {"PE.L2-3.10.1", "PE.L2-3.10.2"},
}

TOTAL_CONTROLS = 110


@pytest.fixture(scope="module")
def ds():
    d = create_dataset()
    load_into(d, "ontology", CMMC_EDIT)
    load_into(d, "structural", TIER1)
    return d


@pytest.fixture(scope="module")
def catalog_controls(ds) -> set[URIRef]:
    onto = graph_for(ds, "ontology")
    return set(onto.subjects(RDF.type, CONTROL))


def _ctrl(local: str) -> URIRef:
    return CMMC[local]


def _modules_with_claims(ds):
    """{module_iri: set(control_iris)} from cmmc:controlsSatisfied."""
    struct = graph_for(ds, "structural")
    out: dict[URIRef, set[URIRef]] = {}
    for m, _, c in struct.triples((None, CONTROLS_SATISFIED, None)):
        out.setdefault(m, set()).add(c)
    return out


# ---------------------------------------------------------------------------
# Parsing + catalog sanity
# ---------------------------------------------------------------------------

def test_tier1_parses_standalone():
    from rdflib import Graph
    g = Graph()
    g.parse(TIER1, format="turtle")
    assert len(g) > 30


def test_catalog_has_110_controls(catalog_controls):
    assert len(catalog_controls) == TOTAL_CONTROLS


# ---------------------------------------------------------------------------
# Referential integrity — no dangling claims
# ---------------------------------------------------------------------------

def test_every_controls_satisfied_exists_in_catalog(ds, catalog_controls):
    """Happy path: every cmmc:controlsSatisfied object is a catalog control."""
    claims = _modules_with_claims(ds)
    assert claims, "tier1.ttl declares no cmmc:controlsSatisfied claims"
    dangling = {
        (str(m), str(c))
        for m, cs in claims.items()
        for c in cs
        if c not in catalog_controls
    }
    assert not dangling, f"controlsSatisfied point at non-existent controls: {dangling}"


def test_no_module_claims_control_absent_from_catalog(ds, catalog_controls):
    """Edge case: the satisfy-edge object set has no control absent from the catalog."""
    struct = graph_for(ds, "structural")
    edge_targets = set(struct.objects(None, SATISFIED_REQUIREMENT))
    assert edge_targets, "no sysml:satisfiedRequirement edges found"
    dangling = {str(c) for c in edge_targets if c not in catalog_controls}
    assert not dangling, f"satisfy-edges reference non-existent controls: {dangling}"


def test_satisfy_edge_and_controls_satisfied_agree(ds):
    """The two claim representations (SysML satisfy-edge and the
    cmmc:controlsSatisfied shortcut) must express the same allocation."""
    struct = graph_for(ds, "structural")
    claims = _modules_with_claims(ds)
    for m, controls in claims.items():
        edge_controls: set[URIRef] = set()
        for usage in struct.objects(m, SYSML.ownedRelationship):
            if (usage, RDF.type, SATISFY_USAGE) in struct:
                # the satisfying element must be the module itself
                assert (usage, SATISFYING_ELEMENT, m) in struct, (
                    f"{m} satisfy-edge satisfyingElement is not the module"
                )
                edge_controls |= set(struct.objects(usage, SATISFIED_REQUIREMENT))
        assert edge_controls == controls, (
            f"{m}: satisfy-edge {edge_controls} != controlsSatisfied {controls}"
        )


# ---------------------------------------------------------------------------
# Verification method — Gate 1 "no untestable claim"
# ---------------------------------------------------------------------------

def test_every_claiming_module_has_verification_method(ds):
    struct = graph_for(ds, "structural")
    claims = _modules_with_claims(ds)
    missing = [
        str(m) for m in claims
        if not list(struct.objects(m, VERIFICATION_METHOD))
    ]
    assert not missing, f"claiming modules with no cmmc:verificationMethod: {missing}"


def test_machine_modules_use_iri_method_inherited_uses_literal(ds):
    struct = graph_for(ds, "structural")
    for name in EXPECTED_MACHINE:
        methods = list(struct.objects(CE[name], VERIFICATION_METHOD))
        assert methods and all(isinstance(x, URIRef) for x in methods), (
            f"{name} should carry an oracle-IRI verificationMethod, got {methods}"
        )
    for name in EXPECTED_INHERITED:
        methods = list(struct.objects(CE[name], VERIFICATION_METHOD))
        assert methods and all(isinstance(x, Literal) for x in methods), (
            f"{name} should carry a literal (inherited) verificationMethod, got {methods}"
        )


# ---------------------------------------------------------------------------
# Exact mapping (this test locks the allocation)
# ---------------------------------------------------------------------------

def test_mapping_matches_spec_exactly(ds):
    claims = _modules_with_claims(ds)
    got = {str(m).replace(str(CE), ""): {str(c).replace(str(CMMC), "") for c in cs}
           for m, cs in claims.items()}
    expected = {**EXPECTED_MACHINE, **EXPECTED_INHERITED}
    assert got == expected, f"tier1 mapping drifted from spec:\n{got}"


def test_inherited_controls_are_marked_inherited_in_catalog(ds, catalog_controls):
    """PE 5-pointers claimed by inheritance are cmmc:inherited in the catalog."""
    onto = graph_for(ds, "ontology")
    for local in EXPECTED_INHERITED["CSP_Physical_Inheritance"]:
        ctrl = _ctrl(local)
        assert ctrl in catalog_controls
        assert (ctrl, CMMC.inherited, Literal(True)) in onto, (
            f"{local} should be cmmc:inherited true in the catalog"
        )


# ---------------------------------------------------------------------------
# Coverage query — proven-vs-attested denominator (integration)
# ---------------------------------------------------------------------------

def test_coverage_query_reports_proven_vs_attested(ds, catalog_controls):
    """Per-control claiming modules + count of controls with NO machine
    verificationMethod. Runs over <ce:structural> + <ce:ontology> via the
    default-union view."""
    struct = graph_for(ds, "structural")
    claims = _modules_with_claims(ds)

    # control -> set(modules claiming it)
    per_control: dict[URIRef, set[URIRef]] = {}
    for m, controls in claims.items():
        for c in controls:
            per_control.setdefault(c, set()).add(m)

    # A control is machine-verified iff some claiming module has an IRI method.
    machine_verified: set[URIRef] = set()
    for c, mods in per_control.items():
        for m in mods:
            methods = list(struct.objects(m, VERIFICATION_METHOD))
            if any(isinstance(x, URIRef) for x in methods):
                machine_verified.add(c)
                break

    claimed = set(per_control)
    no_machine = catalog_controls - machine_verified  # proven-vs-attested denominator

    # Every claimed control is a real catalog control.
    assert claimed <= catalog_controls

    # Expected totals derived from the spec.
    expected_machine = {_ctrl(x) for cs in EXPECTED_MACHINE.values() for x in cs}
    expected_inherited = {_ctrl(x) for cs in EXPECTED_INHERITED.values() for x in cs}
    expected_claimed = expected_machine | expected_inherited

    assert claimed == expected_claimed
    assert machine_verified == expected_machine
    assert len(machine_verified) == 20
    assert len(claimed) == 22
    assert len(catalog_controls - claimed) == 88          # controls with NO claiming module
    assert len(no_machine) == TOTAL_CONTROLS - 20 == 90   # no machine verificationMethod
    # The inherited pair is claimed but NOT machine-verified.
    assert expected_inherited <= no_machine
