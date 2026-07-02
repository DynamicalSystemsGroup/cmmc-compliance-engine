"""Provisioning backends for the Factory.

Exports the frozen `ProvisionBackend` protocol + `PlanResult` seam, the real
`TerraformBackend`, and a deterministic `FakeProvisionBackend` for tests (no
terraform). The Fake has a "non-compliant" variant (a non-US region) that drives
the PolicyCheck safety-valve test.
"""

from __future__ import annotations

import hashlib
import json

from pipeline.provision.base import (  # noqa: F401
    ApplyResult,
    PlannedResource,
    PlanResult,
    ProvisionBackend,
    ProvisionError,
    ProvisionUnavailable,
    TerraformUnavailable,
    assert_planresult_conformant,
    is_us_region,
    parse_plan_json,
)
from pipeline.provision.terraform import TerraformBackend  # noqa: F401

# The canonical Tier-1 provisioning shape used by the Fake: each planned
# resource_id matches a structural/tier1.ttl module local-name, and maps to the
# control(s) that module claims. This is the compliant (US-region) plan.
_TIER1_PLAN: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("OrgPolicy_USRegion", "terraform_data.org_policy", ("SC.L2-3.13.1",)),
    ("CMEK_KeyRing", "terraform_data.cmek", ("SC.L2-3.13.11", "SC.L2-3.13.16")),
    ("CUI_Users_Group", "terraform_data.iam", ("AC.L2-3.1.1",)),
    ("Workspace2SV_CUI_OU", "terraform_data.mfa", ("IA.L2-3.5.3",)),
    ("AuditLog_Export", "terraform_data.audit", ("AU.L2-3.3.1",)),
)


def _synth_plan_json(resources: tuple[PlannedResource, ...]) -> dict:
    """A minimal `terraform show -json`-shaped document for the Fake."""
    return {
        "format_version": "1.2",
        "terraform_version": "fake",
        "planned_values": {
            "root_module": {
                "resources": [
                    {
                        "address": r.address,
                        "mode": "managed",
                        "type": r.type,
                        "name": r.resource_id.lower(),
                        "values": r.values,
                    }
                    for r in resources
                ]
            }
        },
    }


class FakeProvisionBackend:
    """Deterministic ProvisionBackend for Factory tests — no terraform.

    `compliant=True` (default) yields an all-US-region Tier-1 plan. `compliant=
    False` flips the OrgPolicy resource's region to `europe-west1`, which the
    PolicyCheck stage rejects (the safety valve halts before Apply).
    """

    name = "fake-provision"

    def __init__(self, *, compliant: bool = True, bad_region: str = "europe-west1"):
        self.compliant = compliant
        self.bad_region = bad_region
        self._probed = False

    def _resources(self) -> tuple[PlannedResource, ...]:
        out: list[PlannedResource] = []
        for module, address, controls in _TIER1_PLAN:
            region = "us-central1"
            if not self.compliant and module == "OrgPolicy_USRegion":
                region = self.bad_region
            values = {
                "input": {
                    "cmmc_module": module,
                    "cmmc_control": ", ".join(controls),
                    "region": region,
                }
            }
            out.append(PlannedResource(
                resource_id=module,
                address=address,
                type="terraform_data",
                controls=controls,
                values=values,
                region=region,
            ))
        return tuple(out)

    def probe(self) -> None:
        self._probed = True  # always available (no external dependency)

    def validate(self) -> None:
        return None

    def plan(self) -> PlanResult:
        resources = self._resources()
        return PlanResult(plan_json=_synth_plan_json(resources), resources=resources)

    def apply(self) -> ApplyResult:
        resources = self._resources()
        state_hash = hashlib.sha256(
            json.dumps(
                {"resources": [r.resource_id for r in resources],
                 "compliant": self.compliant},
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        return ApplyResult(state_hash=state_hash, applied=True,
                           resource_count=len(resources))

    def describe(self) -> str:
        variant = "compliant" if self.compliant else f"non-compliant ({self.bad_region})"
        return f"FakeProvisionBackend ({variant}, deterministic, no terraform)"


__all__ = [
    "ProvisionBackend",
    "PlanResult",
    "PlannedResource",
    "ApplyResult",
    "TerraformBackend",
    "FakeProvisionBackend",
    "TerraformUnavailable",
    "ProvisionUnavailable",
    "ProvisionError",
    "assert_planresult_conformant",
    "is_us_region",
    "parse_plan_json",
]
