"""Machine-checkable control criteria — verification, not validation.

SCAFFOLD, patterned on ADCS-lifecycle-demo/analysis/oracle.py.

An oracle pulls `metric_key` from an evidence artifact's `summary` dict and
compares it to `threshold` via `comparator`. A control with NO criterion here
returns `cantTell` on purpose: it must be human-attested from documentary
evidence. The oracle NEVER asserts a control is MET — only the Affirming
Official does that.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

OUTCOME_PASSED = "passed"
OUTCOME_FAILED = "failed"
OUTCOME_CANTTELL = "cantTell"

_COMPARATORS = {
    "eq": lambda v, t: v == t,
    "ne": lambda v, t: v != t,
    "le": lambda v, t: v <= t,
    "ge": lambda v, t: v >= t,
    "in": lambda v, t: v in t,
}


@dataclass(frozen=True)
class Criterion:
    control_id: str
    metric_key: str          # key into an evidence artifact's summary dict
    comparator: str          # eq | ne | le | ge | in
    threshold: Any
    label: str = ""


@dataclass(frozen=True)
class OracleResult:
    control_id: str
    metric_value: Any
    outcome: str             # passed | failed | cantTell
    detail: str


# Single source of truth for machine-checkable controls. EXAMPLES — extend
# toward the ~70 controls that have an automatable signal. The ~40 that do
# not (policy/training/PS/IR/physical) are intentionally ABSENT → cantTell.
CRITERIA: dict[str, Criterion] = {
    "IA.L2-3.5.3":   Criterion("IA.L2-3.5.3", "mfa_enforced_privileged", "eq", True,
                               "MFA enforced for privileged access"),
    "SC.L2-3.13.11": Criterion("SC.L2-3.13.11", "fips_module_present", "eq", True,
                               "FIPS-validated crypto module present (CMVP cert)"),
    "SC.L2-3.13.16": Criterion("SC.L2-3.13.16", "cui_encrypted_at_rest", "eq", True,
                               "CUI encrypted at rest (CMK)"),
    "AC.L2-3.1.1":   Criterion("AC.L2-3.1.1", "unauthorized_principals", "eq", 0,
                               "no unauthorized principals with access"),
    # ITAR residency (modelled as a pseudo-control id)
    "ITAR-120.54":   Criterion("ITAR-120.54", "data_region", "eq", "US",
                               "data residency US-only"),
}


def evaluate(summary: dict[str, Any], control_id: str,
             criteria: dict[str, Criterion] = CRITERIA) -> OracleResult:
    """Evaluate one control's criterion against an evidence summary dict."""
    crit = criteria.get(control_id)
    if crit is None:
        return OracleResult(control_id, None, OUTCOME_CANTTELL,
                            "no machine-readable criterion — requires human attestation")
    if crit.metric_key not in summary:
        return OracleResult(control_id, None, OUTCOME_CANTTELL,
                            f"metric {crit.metric_key!r} absent from evidence")
    value = summary[crit.metric_key]
    ok = _COMPARATORS[crit.comparator](value, crit.threshold)
    return OracleResult(
        control_id, value,
        OUTCOME_PASSED if ok else OUTCOME_FAILED,
        f"{crit.metric_key} = {value!r} {crit.comparator} {crit.threshold!r} "
        f"-> {'pass' if ok else 'fail'} (config-level)",
    )
