"""Gate 1 — planning-coverage audit (the Order Compiler's own SPARQL).

Gate 1 is the "no unmapped / no untestable claim" check run BEFORE an Order is
emitted. It answers, over the tier1 satisfy edge (`sysml:SatisfyRequirementUsage`)
and the CMMC catalog, three questions about the required control set the COP
resolved to:

  forward  — does every REQUIRED control have at least one claiming module?
             (a required control with no module ⇒ an unbuildable Order; the gap
             names the control and its cmmc:weight so severity is visible.)
  backward — does every INCLUDED module trace to at least one required control?
             (an included module claiming nothing required ⇒ an orphan.)
  no-paper — does every module that claims a required control carry a
             `cmmc:verificationMethod`? (a claim with no method is a paper claim
             — it cannot be machine- or manually-confirmed downstream.)

This is a SELF-CONTAINED report. It deliberately does NOT call
`traceability.audit.audit()` (that is the Factory-side, evidence-vs-requirement
audit); it mirrors that module's dataclass/render shape only. Any failure ⇒ the
compiler refuses to emit the Order.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rdflib import Dataset

from ontology.prefixes import CMMC, SYSML
from pipeline.dataset import graph_for

# SPARQL over the satisfy edge — (module, control) pairs.
_SATISFY_QUERY = """
SELECT ?module ?control WHERE {
    ?module a sysml:PartUsage ;
            sysml:ownedRelationship ?rel .
    ?rel a sysml:SatisfyRequirementUsage ;
         sysml:satisfiedRequirement ?control .
}
"""

# SPARQL for the verificationMethod on each module.
_METHOD_QUERY = """
SELECT ?module ?method WHERE {
    ?module a sysml:PartUsage ;
            cmmc:verificationMethod ?method .
}
"""

_INITNS = {"sysml": SYSML, "cmmc": CMMC}


@dataclass
class Failure:
    """One Gate 1 failure with a precise, human-readable reason."""
    subject: str          # control id or module local-name
    reason: str
    details: dict = field(default_factory=dict)


@dataclass
class DirectionResult:
    direction: str        # "forward" | "backward" | "no-paper-claim"
    passed: bool
    checked_count: int
    failures: list[Failure] = field(default_factory=list)

    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return (f"{self.direction:<16} {status:<5} "
                f"({self.checked_count} checked, {len(self.failures)} failures)")


@dataclass
class Gate1Report:
    forward: DirectionResult
    backward: DirectionResult
    untestable: DirectionResult
    required: frozenset          # required control ids
    included_modules: dict       # module_local -> sorted list of required controls it claims
    forward_map: dict            # control -> sorted list of claiming modules
    verification_methods: dict   # module_local -> sorted list of method strings

    @property
    def passed(self) -> bool:
        return self.forward.passed and self.backward.passed and self.untestable.passed

    def gap_controls(self) -> list[str]:
        return [f.subject for f in self.forward.failures]

    def orphan_modules(self) -> list[str]:
        return [f.subject for f in self.backward.failures]

    def paper_claim_modules(self) -> list[str]:
        return [f.subject for f in self.untestable.failures]

    def render(self) -> str:
        lines = [
            "Gate 1 — planning-coverage audit",
            f"  result: {'PASS' if self.passed else 'FAIL'}",
            f"  required controls: {len(self.required)}",
            f"  {self.forward.summary()}",
            f"  {self.backward.summary()}",
            f"  {self.untestable.summary()}",
        ]
        if not self.passed:
            lines.append("  gaps:")
            for f in (*self.forward.failures, *self.backward.failures,
                      *self.untestable.failures):
                extra = f" [{f.details}]" if f.details else ""
                lines.append(f"    - {f.subject}: {f.reason}{extra}")
        return "\n".join(lines)


def _satisfy_pairs(ds: Dataset):
    """Return (module_to_controls, control_to_modules) as local-name maps."""
    module_to_controls: dict[str, set[str]] = {}
    control_to_modules: dict[str, set[str]] = {}
    for row in ds.query(_SATISFY_QUERY, initNs=_INITNS):
        m = _local(row.module)
        c = _local(row.control)
        module_to_controls.setdefault(m, set()).add(c)
        control_to_modules.setdefault(c, set()).add(m)
    return module_to_controls, control_to_modules


def _verification_methods(ds: Dataset) -> dict[str, set[str]]:
    methods: dict[str, set[str]] = {}
    for row in ds.query(_METHOD_QUERY, initNs=_INITNS):
        methods.setdefault(_local(row.module), set()).add(str(row.method))
    return methods


def _local(uri) -> str:
    s = str(uri)
    for sep in ("#", "/"):
        if sep in s:
            s = s.rsplit(sep, 1)[-1]
    return s


def _control_weight(ds: Dataset, control_local: str):
    onto = graph_for(ds, "ontology")
    w = onto.value(CMMC[control_local], CMMC.weight)
    return int(w) if w is not None else None


def run_gate1(
    required: set[str],
    ds: Dataset,
    *,
    included_modules: set[str] | None = None,
) -> Gate1Report:
    """Run Gate 1 over the satisfy edge in `ds` for the `required` control set.

    `included_modules` (local names) overrides which modules the Order includes;
    if omitted, the included set is every module that claims a required control
    (so a well-formed Order never orphans). Pass an explicit set to audit a
    hand-picked module list (e.g. to detect an orphan).
    """
    required = frozenset(required)
    module_to_controls, control_to_modules = _satisfy_pairs(ds)
    methods = _verification_methods(ds)

    # -- forward: every required control has ≥1 claiming module --------------
    fwd_failures: list[Failure] = []
    forward_map: dict[str, list[str]] = {}
    for c in sorted(required):
        mods = control_to_modules.get(c, set())
        forward_map[c] = sorted(mods)
        if not mods:
            fwd_failures.append(Failure(
                subject=c,
                reason="required control has no claiming module",
                details={"weight": _control_weight(ds, c)},
            ))
    forward = DirectionResult("forward", not fwd_failures, len(required), fwd_failures)

    # -- included modules -----------------------------------------------------
    if included_modules is None:
        included = {m for m, cs in module_to_controls.items() if cs & required}
    else:
        included = set(included_modules)

    # -- backward: every included module traces to ≥1 required control -------
    bwd_failures: list[Failure] = []
    included_map: dict[str, list[str]] = {}
    for m in sorted(included):
        traced = module_to_controls.get(m, set()) & required
        included_map[m] = sorted(traced)
        if not traced:
            bwd_failures.append(Failure(
                subject=m,
                reason="included module claims no required control (orphan)",
                details={"claims": sorted(module_to_controls.get(m, set()))},
            ))
    backward = DirectionResult("backward", not bwd_failures, len(included), bwd_failures)

    # -- no paper claim: every module claiming a required control has a method -
    claiming = {m for m, cs in module_to_controls.items() if cs & required}
    paper_failures: list[Failure] = []
    for m in sorted(claiming):
        if not methods.get(m):
            paper_failures.append(Failure(
                subject=m,
                reason="claims a required control but has no cmmc:verificationMethod",
                details={"claims": sorted(module_to_controls[m] & required)},
            ))
    untestable = DirectionResult(
        "no-paper-claim", not paper_failures, len(claiming), paper_failures
    )

    return Gate1Report(
        forward=forward,
        backward=backward,
        untestable=untestable,
        required=required,
        included_modules=included_map,
        forward_map=forward_map,
        verification_methods={m: sorted(v) for m, v in methods.items()},
    )
