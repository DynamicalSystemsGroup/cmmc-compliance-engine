"""Frozen ProvisionBackend protocol + the PlanResult seam schema.

The Factory provisions the Tier-1 environment through a ProvisionBackend. The
default implementation (`terraform.TerraformBackend`) shells to the real
`terraform` binary at PLAN level (mock providers); a future `LiveTerraformBackend`
that really `apply`s live cloud resources must be a *genuine swap* — same
protocol, same `PlanResult`. That is why `PlanResult` is pinned by a conformance
check (`assert_planresult_conformant`) rather than left implicit.

`PlanResult` carries the real `terraform show -json` document plus a normalized
list of `PlannedResource`s. Each planned resource has a **stable `resource_id`**
that is the join key across the whole back-half:
  (a) it matches a `structural/tier1.ttl` module local-name,
  (b) evidence artifacts reference it,
  (c) it appears in the BOM control-mapping (U11).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


class ProvisionUnavailable(RuntimeError):
    """Preflight found the provisioning substrate unusable (base class)."""


class TerraformUnavailable(ProvisionUnavailable):
    """The terraform binary is absent or `init -backend=false` failed."""


class ProvisionError(RuntimeError):
    """A provisioning step (validate/plan/apply) failed."""


@dataclass(frozen=True)
class PlannedResource:
    """One resource in a plan, normalized for the compliance back-half.

    resource_id — the stable join key (a tier1.ttl module local-name when the
                  resource carries a `cmmc_module` label; else the tf address).
    address     — the terraform address, e.g. "terraform_data.org_policy".
    type        — the terraform resource type.
    controls    — CMMC control ids this resource maps to (from `cmmc_control`).
    values      — the planned attribute values (from terraform show -json).
    region      — the resource's region/location if any (for the policy valve).
    """

    resource_id: str
    address: str
    type: str
    controls: tuple[str, ...] = ()
    values: dict = field(default_factory=dict)
    region: str | None = None


@dataclass(frozen=True)
class PlanResult:
    """The result of `ProvisionBackend.plan()` — the frozen provisioning seam."""

    plan_json: dict
    resources: tuple[PlannedResource, ...]

    def resource_ids(self) -> list[str]:
        return [r.resource_id for r in self.resources]

    def controls(self) -> list[str]:
        seen: list[str] = []
        for r in self.resources:
            for c in r.controls:
                if c not in seen:
                    seen.append(c)
        return seen

    def by_id(self, resource_id: str) -> PlannedResource | None:
        for r in self.resources:
            if r.resource_id == resource_id:
                return r
        return None

    def regions(self) -> dict[str, str]:
        return {r.resource_id: r.region for r in self.resources if r.region}


@dataclass(frozen=True)
class ApplyResult:
    """The result of `ProvisionBackend.apply()` (mock-provider apply for now)."""

    state_hash: str
    applied: bool = True
    resource_count: int = 0


@runtime_checkable
class ProvisionBackend(Protocol):
    """Provisioning substrate for the Factory. Frozen contract.

    Implementations:
      - TerraformBackend      (default): real `terraform` at plan level, mock providers
      - FakeProvisionBackend  (tests): deterministic canned PlanResult, no terraform
      - LiveTerraformBackend  (future): real apply — MUST be a drop-in swap
    """

    name: str

    def probe(self) -> None:
        """Preflight: raise ProvisionUnavailable if the substrate is unusable."""
        ...

    def validate(self) -> None:
        """Validate the provisioning config; raise ProvisionError on failure."""
        ...

    def plan(self) -> PlanResult:
        """Produce a PlanResult (real `terraform plan` → `show -json` for TF)."""
        ...

    def apply(self) -> ApplyResult:
        """Apply the plan (mock-provider apply now; live deferred)."""
        ...

    def describe(self) -> str:
        """One-line human description for the preflight banner."""
        ...


# ---------------------------------------------------------------------------
# Conformance — pin the PlanResult schema so a future backend is a real swap.
# ---------------------------------------------------------------------------

_PLANNED_RESOURCE_FIELDS = {
    "resource_id": str,
    "address": str,
    "type": str,
    "controls": tuple,
    "values": dict,
}


def assert_planresult_conformant(pr: object) -> None:
    """Raise AssertionError unless `pr` is a schema-conformant PlanResult.

    Used by the seam conformance test so TerraformBackend and any future
    LiveTerraformBackend are held to the identical contract.
    """
    assert isinstance(pr, PlanResult), f"not a PlanResult: {type(pr)!r}"
    assert isinstance(pr.plan_json, dict), "plan_json must be a dict"
    assert isinstance(pr.resources, tuple), "resources must be a tuple"
    for r in pr.resources:
        assert isinstance(r, PlannedResource), f"not a PlannedResource: {type(r)!r}"
        for fname, ftype in _PLANNED_RESOURCE_FIELDS.items():
            val = getattr(r, fname)
            assert isinstance(val, ftype), (
                f"PlannedResource.{fname} must be {ftype.__name__}, got {type(val).__name__}"
            )
        assert r.resource_id, "resource_id must be non-empty (the BOM join key)"
        for c in r.controls:
            assert isinstance(c, str), "each control id must be a str"
        assert r.region is None or isinstance(r.region, str), "region must be str|None"
    # resource_ids must be unique (they are the stable join key).
    ids = pr.resource_ids()
    assert len(ids) == len(set(ids)), f"resource_id values must be unique: {ids}"


# ---------------------------------------------------------------------------
# Shared plan-JSON parsing (terraform show -json → PlannedResource list)
# ---------------------------------------------------------------------------

_US_REGION_PREFIXES = ("us-", "us", "usgov")


def is_us_region(region: str | None) -> bool:
    """True if a region string denotes a US location (policy safety valve).

    US GCP regions are `us-central1`, `us-east1`, `usgov-...`, etc. Anything
    else (e.g. `europe-west1`, `asia-east1`) is treated as non-US.
    """
    if not region:
        return False
    return region.lower().startswith(_US_REGION_PREFIXES)


def parse_plan_json(plan_json: dict) -> tuple[PlannedResource, ...]:
    """Normalize a `terraform show -json` document into PlannedResources.

    Reads `planned_values.root_module.resources`. A resource may carry its
    compliance labels either in `values.input` (terraform_data) or
    `values.triggers` (null_resource): `cmmc_module` → resource_id,
    `cmmc_control` → control ids (comma/space separated), `region` → region.
    """
    root = (plan_json.get("planned_values", {}) or {}).get("root_module", {}) or {}
    resources = root.get("resources", []) or []
    out: list[PlannedResource] = []
    for res in resources:
        address = res.get("address", "")
        rtype = res.get("type", "")
        values = res.get("values", {}) or {}
        labels = values.get("input") or values.get("triggers") or {}
        if not isinstance(labels, dict):
            labels = {}
        module = labels.get("cmmc_module") or address
        controls_raw = labels.get("cmmc_control", "")
        controls = tuple(
            c.strip() for c in str(controls_raw).replace(",", " ").split() if c.strip()
        )
        region = labels.get("region") or values.get("region") or values.get("location")
        out.append(PlannedResource(
            resource_id=str(module),
            address=address,
            type=rtype,
            controls=controls,
            values=values,
            region=str(region) if region else None,
        ))
    return tuple(out)
