"""SPRS score + POA&M-legality gate.

SCAFFOLD — the compliance-specific extension to the ADCS audit. No ADCS
analogue; this encodes 32 CFR Part 170 scoring.

SPRS score = 110 - Σ(weight of each control not MET).
  110      -> Final Level 2      (all controls MET)
  88..109  -> Conditional Level 2 (POA&M, 180-day closeout)
  < 88     -> No CMMC status      (ineligible for award)

POA&M legality (32 CFR §170.21): only 1-point controls may be deferred, and
six specific 1-point controls are excluded. A 3- or 5-point control on a POA&M
is a HARD ERROR — the submission is invalid, not merely low.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rdflib import Dataset, Graph

FINAL = 110
CONDITIONAL_FLOOR = 88


@dataclass
class ControlStatus:
    control_id: str
    weight: int              # 1 | 3 | 5 (variable controls resolve to their max)
    met: bool                # attested earl:passed
    on_poam: bool = False
    poam_eligible: bool = False   # cmmc:poamEligible from the catalog
    # Additive metadata (backward-compatible; score() ignores these). The
    # variable-weight controls (IA.L2-3.5.3, SC.L2-3.13.11) carry the partial
    # weight for a future partial-credit hook — Phase I scores full `weight`.
    variable_weight: bool = False
    weight_if_partial: int | None = None


@dataclass
class SprsResult:
    score: int
    status: str                          # "Final" | "Conditional" | "Ineligible"
    illegal_poam: list[str] = field(default_factory=list)
    unmet: list[str] = field(default_factory=list)

    @property
    def valid_submission(self) -> bool:
        """A submission with any illegal POA&M item is invalid regardless of score."""
        return not self.illegal_poam


def score(controls: list[ControlStatus]) -> SprsResult:
    """Compute SPRS score and enforce POA&M legality.

    NOTE: `met` is the human attestation outcome (earl:passed). This function
    does NOT infer MET from oracle results — only attestation establishes it.
    """
    deductions = sum(c.weight for c in controls if not c.met)
    s = FINAL - deductions
    unmet = [c.control_id for c in controls if not c.met]

    # Illegal POA&M: any non-eligible control (weight > 1, or explicitly
    # excluded) placed on a POA&M.
    illegal = [
        c.control_id for c in controls
        if c.on_poam and (c.weight > 1 or not c.poam_eligible)
    ]

    if s >= FINAL:
        status = "Final"
    elif s >= CONDITIONAL_FLOOR:
        status = "Conditional"
    else:
        status = "Ineligible"

    return SprsResult(score=s, status=status, illegal_poam=illegal, unmet=unmet)


# --------------------------------------------------------------------------- #
# Catalog-backed loader (dependency injection — the graph dependency stays OUT
# of score()).
# --------------------------------------------------------------------------- #

# Namespace for the CMMC control catalog. Imported lazily so importing this
# module for the pure scorer never requires rdflib.
_CMMC_URI = "http://dynamicalsystems.group/ontology/cmmc#"


def _as_bool(literal, default: bool = False) -> bool:
    """Coerce an rdflib boolean Literal (or None) to a Python bool."""
    if literal is None:
        return default
    try:
        return bool(literal.toPython())
    except AttributeError:
        return bool(literal)


def _catalog_graph(source: "str | Path | Graph | Dataset"):
    """Return a queryable RDF graph for the catalog.

    Accepts a path to a Turtle catalog, or an already-built rdflib
    ``Graph``/``Dataset`` (a Dataset built by ``pipeline.dataset.create_dataset``
    has ``default_union=True``, so control triples resolve across named graphs).
    """
    from rdflib import Graph

    if isinstance(source, (str, Path)):
        g = Graph()
        g.parse(str(source), format="turtle")
        return g
    return source


def load_control_statuses(
    dataset_or_catalog_path: "str | Path | Graph | Dataset",
    *,
    met_control_ids: set[str],
    poam_control_ids: set[str] = frozenset(),
    required_control_ids: set[str] | None = None,
) -> list[ControlStatus]:
    """Build ``ControlStatus`` rows from the CMMC catalog + a caller-supplied MET set.

    The graph dependency lives HERE, not in ``score()``: the MET set arrives as a
    plain parameter, so U10's ``audit.py`` can derive ``met_control_ids`` from the
    U9 attestation graph (every control with a ``ce:attests`` + ``earl:passed``
    outcome — **including CSP-inherited-and-attested controls**, which the caller
    simply includes in ``met_control_ids``) and hand them in without changing this
    function.

    Per control, reads ``cmmc:weight`` and ``cmmc:poamEligible`` from the catalog:
      - ``met``          = ``control_id in met_control_ids``
      - ``on_poam``      = ``control_id in poam_control_ids``
      - ``poam_eligible``= ``cmmc:poamEligible`` (the six ``nonDeferrable``
                            1-pointers load as ``poam_eligible=False``)
      - variable-weight controls resolve to ``cmmc:weight`` (full/max); their
        ``cmmc:weightIfPartial`` is captured for a future partial-credit hook.

    If ``required_control_ids`` is given, only those controls are scored (the
    Order's required set); otherwise all 110.
    """
    from rdflib import RDF, Namespace

    cmmc = Namespace(_CMMC_URI)
    graph = _catalog_graph(dataset_or_catalog_path)

    statuses: list[ControlStatus] = []
    for ctl in graph.subjects(RDF.type, cmmc.Control):
        cid_lit = graph.value(ctl, cmmc.controlId)
        if cid_lit is None:
            continue
        control_id = str(cid_lit)
        if required_control_ids is not None and control_id not in required_control_ids:
            continue

        weight_lit = graph.value(ctl, cmmc.weight)
        if weight_lit is None:
            continue  # a control with no SPRS weight is not scorable
        weight = int(weight_lit)

        wip_lit = graph.value(ctl, cmmc.weightIfPartial)
        statuses.append(ControlStatus(
            control_id=control_id,
            weight=weight,
            met=control_id in met_control_ids,
            on_poam=control_id in poam_control_ids,
            poam_eligible=_as_bool(graph.value(ctl, cmmc.poamEligible)),
            variable_weight=_as_bool(graph.value(ctl, cmmc.variableWeight)),
            weight_if_partial=int(wip_lit) if wip_lit is not None else None,
        ))
    return statuses


def sprs_from_catalog(
    dataset_or_catalog_path: "str | Path | Graph | Dataset",
    *,
    met_control_ids: set[str],
    poam_control_ids: set[str] = frozenset(),
    required_control_ids: set[str] | None = None,
) -> SprsResult:
    """Convenience: load statuses from the catalog, then score them."""
    return score(load_control_statuses(
        dataset_or_catalog_path,
        met_control_ids=met_control_ids,
        poam_control_ids=poam_control_ids,
        required_control_ids=required_control_ids,
    ))
