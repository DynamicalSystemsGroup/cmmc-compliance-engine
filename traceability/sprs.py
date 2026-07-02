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

FINAL = 110
CONDITIONAL_FLOOR = 88


@dataclass
class ControlStatus:
    control_id: str
    weight: int              # 1 | 3 | 5
    met: bool                # attested earl:passed
    on_poam: bool = False
    poam_eligible: bool = False   # cmmc:poamEligible from the catalog


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
