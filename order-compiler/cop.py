"""COP build + human attestation (the one human call in the Order Compiler).

The Contract Obligation Profile (COP) is AI-drafted, then a Compliance Officer
attests it — the single mandatory human sign-off before an Order can be
compiled. The attestation is recorded into `<ce:order>` reusing the ADCS
attestation pattern (`traceability/attestation.py`): an `earl:Assertion` /
`prov:Activity` asserted by the officer, with `earl:manual` mode (`auto=True`
downgrades to `earl:semiAuto` for scripted runs).

Two safety properties the attestation enforces (R11):
  - Per **deliverable** obligation, the officer must make an EXPLICIT affirmation
    "this imposes no environment control (no CUI/ITAR data on DSG infra)". That
    affirmation is recorded, not assumed — a plain deliverable resolves to {} and
    is affirmed; the affirmation is auditable.
  - A **CUI/ITAR-marked deliverable** is NEVER silently affirmed. `resolve()`
    raises `SpilloverReviewRequired` for it; `attest_cop` surfaces that (re-raises)
    unless the officer has explicitly acknowledged the spillover
    (`acknowledge_spillovers`), forcing the env-spillover review before Gate 1.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from rdflib import Dataset, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

from ontology.prefixes import CE, EARL, PROV
from pipeline.dataset import graph_for

import rule_library as rl

# The role that signs off the COP (stable individual).
ROLE_COMPLIANCE_OFFICER = CE["role-ComplianceOfficer"]

MODE_MANUAL = EARL.manual
MODE_SEMI_AUTO = EARL.semiAuto
OUTCOME_PASSED = EARL.passed


@dataclass
class COPAttestation:
    """Result of attesting a COP — also fully written into `<ce:order>`."""
    attestation_iri: URIRef
    cop_iri: URIRef
    officer: URIRef
    mode: str                       # "manual" | "semiAuto"
    outcome: str                    # "passed"
    affirmations: dict = field(default_factory=dict)   # obligation -> True (no env control)
    acknowledged_spillovers: frozenset = frozenset()

    @property
    def is_attested(self) -> bool:
        return self.outcome == "passed"


def attest_cop(
    ds: Dataset,
    obligations: dict[str, "rl.Obligation"],
    *,
    cop_iri: URIRef | None = None,
    officer: URIRef = ROLE_COMPLIANCE_OFFICER,
    auto: bool = False,
    acknowledge_spillovers: frozenset[str] | set[str] = frozenset(),
    catalog_path=None,
    now: str | None = None,
) -> COPAttestation:
    """Attest the COP, writing the attestation + per-deliverable affirmations
    into `<ce:order>`. Raises `rule_library.SpilloverReviewRequired` on an
    unacknowledged CUI/ITAR deliverable (surfacing the spillover before Gate 1).
    """
    cop_iri = cop_iri or CE["COP-NV012"]
    acknowledge_spillovers = frozenset(acknowledge_spillovers)
    order_g = graph_for(ds, "order")

    affirmations: dict[str, bool] = {}

    # -- per-deliverable affirmation / spillover surfacing --------------------
    for name, obl in sorted(obligations.items()):
        if obl.obligation_type != rl.DELIVERABLE:
            continue
        try:
            rl.resolve(obl, catalog_path=catalog_path)
        except rl.SpilloverReviewRequired:
            # CUI/ITAR deliverable — must NOT be silently affirmed.
            if name not in acknowledge_spillovers:
                raise
            # Acknowledged: the officer routed it to env-spillover review; it
            # does NOT get a "no environment control" affirmation.
            continue
        # Plain deliverable resolved to {} — record the explicit affirmation.
        aff = CE[f"affirmation/{name}"]
        order_g.add((aff, RDF.type, CE.DeliverableAffirmation))
        order_g.add((aff, CE.affirmsObligation, _obl_iri(obl, cop_iri)))
        order_g.add((aff, CE.noEnvironmentControl, Literal(True)))
        order_g.add((aff, RDFS.comment,
                     Literal("Deliverable imposes no environment control "
                             "(no CUI/ITAR data on DSG infrastructure).")))
        affirmations[name] = True

    # -- the attestation node -------------------------------------------------
    mode_iri = MODE_SEMI_AUTO if auto else MODE_MANUAL
    mode_short = "semiAuto" if auto else "manual"
    att = CE[f"attestation/COP/{_local(cop_iri)}"]
    stamp = now or datetime.now(timezone.utc).isoformat()

    order_g.add((att, RDF.type, CE.COPAttestation))
    order_g.add((att, RDF.type, EARL.Assertion))
    order_g.add((att, RDF.type, PROV.Activity))
    order_g.add((att, CE.attestsCOP, cop_iri))
    order_g.add((att, CE.attestationMode, mode_iri))
    order_g.add((att, CE.outcome, OUTCOME_PASSED))
    order_g.add((att, EARL.assertedBy, officer))
    order_g.add((att, PROV.wasAssociatedWith, officer))
    order_g.add((att, PROV.generatedAtTime, Literal(stamp, datatype=XSD.dateTime)))
    for name in affirmations:
        order_g.add((att, CE.hasAffirmation, CE[f"affirmation/{name}"]))
    order_g.add((officer, RDF.type, PROV.Agent))
    order_g.add((officer, RDFS.label, Literal("Compliance Officer")))

    return COPAttestation(
        attestation_iri=att,
        cop_iri=cop_iri,
        officer=officer,
        mode=mode_short,
        outcome="passed",
        affirmations=affirmations,
        acknowledged_spillovers=acknowledge_spillovers,
    )


def _obl_iri(obl: "rl.Obligation", cop_iri: URIRef) -> URIRef:
    return CE[obl.name]


def _local(uri: URIRef) -> str:
    s = str(uri)
    for sep in ("#", "/"):
        if sep in s:
            s = s.rsplit(sep, 1)[-1]
    return s
