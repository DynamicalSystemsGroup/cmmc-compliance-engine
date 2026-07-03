"""Order compiler — obligations → controls → modules → hash-referenced Order.

The compiler is the join point of the Order Compiler front-half:

    obligations  --rule_library.resolve-->  required control set
                 --tier1 satisfy edge----->  claiming modules      (Gate 1)
                 --emit------------------->  hash-referenced Order  (into <ce:order>)

It REFUSES to emit an Order when:
  - the COP is not attested (human sign-off is mandatory), or
  - Gate 1 fails (a required control has no module / an orphan module / a paper
    claim). The Gate1Report travels on the raised exception so the caller can
    name the precise gap.

The emitted Order is content-addressed: it carries a hash of each included
module, the resolved control set, the COP, and a coverage-proof — plus a single
`ce:orderHash` over all of them, so the Factory can load the Order and
verify it byte-for-byte before executing.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from rdflib import BNode, Dataset, Graph, Literal, URIRef
from rdflib.namespace import RDF

from compliance_engine.ontology.prefixes import CE, CMMC, PROV
from compliance_engine.pipeline.dataset import graph_for
from compliance_engine.pipeline.evidence.hashing import _serialize_for_hash, hash_structural_model

from compliance_engine.order_compiler import rule_library as rl
from compliance_engine.order_compiler import gate1 as g1
from compliance_engine.order_compiler.cop import COPAttestation

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CATALOG_TTL = _REPO_ROOT / "data" / "ontology" / "cmmc-edit.ttl"
TIER1_TTL = _REPO_ROOT / "data" / "structural" / "tier1.ttl"
COP_DRAFT_TTL = _REPO_ROOT / "fixtures" / "nv012" / "cop_draft.ttl"

STANDARD = "NIST SP 800-171 Rev 2"
TARGET_TIER = "Tier1"
IMPACT_LEVEL = "IL4"


class UnattestedCOP(Exception):
    """The compiler was asked to emit an Order from an unattested COP."""


class Gate1Failed(Exception):
    """Gate 1 refused the Order. Carries the Gate1Report naming the gap(s)."""

    def __init__(self, report: "g1.Gate1Report"):
        self.report = report
        super().__init__(
            f"Gate 1 refused the Order:\n{report.render()}"
        )


@dataclass
class Order:
    """The compiled, hash-referenced Order (also emitted into `<ce:order>`)."""
    iri: URIRef
    contract: str
    tier: str
    impact_level: str
    standard: str
    cop_iri: URIRef
    required_controls: frozenset
    markers: frozenset
    included_modules: dict            # module_local -> content hash
    scope: dict
    cop_hash: str
    control_set_hash: str
    coverage_proof_hash: str
    order_hash: str
    gate1: "g1.Gate1Report" = field(default=None)


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------

def resolve_required_controls(
    obligations: dict[str, "rl.Obligation"],
    *,
    catalog_path: Path | None = None,
    acknowledge_spillovers: frozenset[str] | set[str] = frozenset(),
) -> tuple[frozenset, frozenset]:
    """Union the resolved control sets across all obligations.

    Deliverable obligations add no controls. A CUI/ITAR deliverable that has NOT
    been acknowledged raises `SpilloverReviewRequired` (surfacing before Gate 1).
    Returns (required_controls, policy_markers).
    """
    acknowledge_spillovers = frozenset(acknowledge_spillovers)
    required: set[str] = set()
    markers: set[str] = set()
    for name, obl in obligations.items():
        try:
            cs = rl.resolve(obl, catalog_path=catalog_path)
        except rl.SpilloverReviewRequired:
            if name not in acknowledge_spillovers:
                raise
            continue  # acknowledged spillover contributes no controls here
        required |= set(cs)
        markers |= cs.markers
    return frozenset(required), frozenset(markers)


# ---------------------------------------------------------------------------
# Hash helpers
# ---------------------------------------------------------------------------

def _sha256(obj) -> str:
    return hashlib.sha256(_serialize_for_hash(obj).encode()).hexdigest()


def _module_cbd(struct: Graph, module: URIRef) -> Graph:
    """Concrete bounded description of a module (module triples + owned bnodes)."""
    g = Graph()
    for p, o in struct.predicate_objects(module):
        g.add((module, p, o))
        if isinstance(o, BNode):
            for p2, o2 in struct.predicate_objects(o):
                g.add((o, p2, o2))
    return g


def _cop_hash(obligations: dict[str, "rl.Obligation"]) -> str:
    """Deterministic hash pinning the COP the Order derives from."""
    canonical = {
        name: {
            "type": obl.obligation_type,
            "data_marker": obl.data_marker,
            "source_ref": obl.source_ref,
            "derives": sorted(obl.derives),
        }
        for name, obl in obligations.items()
    }
    return _sha256(canonical)


# ---------------------------------------------------------------------------
# Compile
# ---------------------------------------------------------------------------

def compile_order(
    ds: Dataset,
    obligations: dict[str, "rl.Obligation"],
    cop_attestation: COPAttestation | None,
    *,
    contract: str = "NV012",
    scope: dict | None = None,
    catalog_path: Path | None = None,
    acknowledge_spillovers: frozenset[str] | set[str] = frozenset(),
    included_modules: set[str] | None = None,
    now: str | None = None,
) -> Order:
    """Compile a hash-referenced Order into `<ce:order>` — or refuse.

    `ds` must already hold the catalog in <ce:ontology> and tier1 in
    <ce:structural>. Raises UnattestedCOP / Gate1Failed / SpilloverReviewRequired
    (all: Order NOT emitted).
    """
    # -- human sign-off is mandatory -----------------------------------------
    if cop_attestation is None or not cop_attestation.is_attested:
        raise UnattestedCOP(
            "Refusing to compile: the COP is not attested by a Compliance "
            "Officer (human sign-off is mandatory)."
        )

    # -- obligations -> required controls ------------------------------------
    required, markers = resolve_required_controls(
        obligations,
        catalog_path=catalog_path,
        acknowledge_spillovers=acknowledge_spillovers,
    )

    # -- Gate 1 --------------------------------------------------------------
    report = g1.run_gate1(required, ds, included_modules=included_modules)
    if not report.passed:
        raise Gate1Failed(report)

    # -- included modules + content hashes -----------------------------------
    struct = graph_for(ds, "structural")
    included = sorted(report.included_modules)   # local names that passed backward
    module_hashes: dict[str, str] = {
        m: hash_structural_model(_module_cbd(struct, CE[m])) for m in included
    }

    # -- content-addressing hashes -------------------------------------------
    control_set_hash = _sha256({"controls": sorted(required)})
    cop_hash = _cop_hash(obligations)
    coverage_proof_hash = _sha256({
        "forward": {c: report.forward_map[c] for c in sorted(required)},
        "backward": report.included_modules,
        "verification": {m: report.verification_methods.get(m, []) for m in included},
    })
    scope = scope or _default_scope(obligations, markers)
    order_hash = _sha256({
        "contract": contract,
        "tier": TARGET_TIER,
        "impact_level": IMPACT_LEVEL,
        "standard": STANDARD,
        "scope": scope,
        "required_controls": sorted(required),
        "module_hashes": module_hashes,
        "cop_hash": cop_hash,
        "control_set_hash": control_set_hash,
        "coverage_proof_hash": coverage_proof_hash,
    })

    order = Order(
        iri=CE[f"Order-{contract}"],
        contract=contract,
        tier=TARGET_TIER,
        impact_level=IMPACT_LEVEL,
        standard=STANDARD,
        cop_iri=cop_attestation.cop_iri,
        required_controls=required,
        markers=markers,
        included_modules=module_hashes,
        scope=scope,
        cop_hash=cop_hash,
        control_set_hash=control_set_hash,
        coverage_proof_hash=coverage_proof_hash,
        order_hash=order_hash,
        gate1=report,
    )
    _emit_order(ds, order, cop_attestation, now=now)
    return order


def _default_scope(obligations, markers) -> dict:
    data_classes = sorted({
        obl.data_marker for obl in obligations.values() if obl.data_marker
    })
    return {
        "tier": TARGET_TIER,
        "impact_level": IMPACT_LEVEL,
        "data_classes": data_classes,
        "policy_markers": sorted(markers),
    }


def _emit_order(ds: Dataset, order: Order, att: COPAttestation, *, now=None) -> None:
    """Serialize the Order as RDF into `<ce:order>` so the Factory can load + verify it."""
    g = graph_for(ds, "order")
    o = order.iri
    stamp = now or datetime.now(timezone.utc).isoformat()

    g.add((o, RDF.type, CE.Order))
    g.add((o, RDF.type, PROV.Entity))
    g.add((o, CE.forContract, Literal(order.contract)))
    g.add((o, CE.targetTier, Literal(order.tier)))
    g.add((o, CE.impactLevel, Literal(order.impact_level)))
    g.add((o, CE.standard, Literal(order.standard)))
    g.add((o, CE.derivedFromCOP, order.cop_iri))
    g.add((o, PROV.wasDerivedFrom, order.cop_iri))
    g.add((o, CE.attestedByCOP, att.attestation_iri))
    g.add((o, CE.generatedAtTime, Literal(stamp)))

    # content-addressing hashes
    g.add((o, CE.copHash, Literal(order.cop_hash)))
    g.add((o, CE.controlSetHash, Literal(order.control_set_hash)))
    g.add((o, CE.coverageProofHash, Literal(order.coverage_proof_hash)))
    g.add((o, CE.orderHash, Literal(order.order_hash)))

    for c in sorted(order.required_controls):
        g.add((o, CE.requiresControl, CMMC[c]))
    for m in sorted(order.markers):
        g.add((o, CE.policyMarker, Literal(m)))
    for dc in order.scope.get("data_classes", []):
        g.add((o, CE.scopeDataClass, Literal(dc)))

    # included modules + per-module content hash (as hash-record nodes)
    for m, h in sorted(order.included_modules.items()):
        module_iri = CE[m]
        g.add((o, CE.includesModule, module_iri))
        mh = CE[f"Order-{order.contract}/modhash/{m}"]
        g.add((o, CE.hasModuleHash, mh))
        g.add((mh, CE.module, module_iri))
        g.add((mh, CE.contentHash, Literal(h)))


# ---------------------------------------------------------------------------
# Convenience: full front-half run from the fixture
# ---------------------------------------------------------------------------

def load_pipeline_dataset(
    *,
    catalog_ttl: Path = CATALOG_TTL,
    tier1_ttl: Path = TIER1_TTL,
    cop_ttl: Path = COP_DRAFT_TTL,
) -> tuple[Dataset, dict[str, "rl.Obligation"]]:
    """Build a Dataset with catalog/tier1/COP loaded, and the obligations dict."""
    from compliance_engine.pipeline.dataset import create_dataset, load_into

    ds = create_dataset()
    load_into(ds, "ontology", catalog_ttl)
    load_into(ds, "structural", tier1_ttl)
    load_into(ds, "order", cop_ttl)
    obligations = rl.load_obligations(cop_ttl)
    return ds, obligations
