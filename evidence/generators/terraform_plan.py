"""Plan-time Terraform evidence generator (U14).

Runs **real** ``terraform`` at plan level against ``terraform/tier1/`` with mock
providers (no credentials, no cloud, no live apply), reads the resulting plan
JSON, maps each planned resource to the ``cmmc:`` control(s) it satisfies, runs
a policy check on the real plan output, and binds the results through the U6
evidence layer as ``ce:PolicyCheck`` / ``ce:Evidence`` nodes that **address**
controls (never attest).

How it stays cloud-free:
- The HCL carries every module→control mapping in ``terraform_data.cmmc_tag``
  resources (built-in; always fully-known in plan JSON — no provider, no creds).
- ``terraform plan`` runs create-only with a dummy ``GOOGLE_OAUTH_ACCESS_TOKEN``:
  create planning never mints a token, so it succeeds offline.
- ``enable_workspace`` defaults false, so the googleworkspace provider is never
  configured on the plan path.

``evidentiary_status`` is ``"mock-plan"`` — a plan-time, mock-provider signal
(distinct from the U6 config-export path's ``"mock"``): the evidence proves the
IaC *plans* to the right shape, not that a live cloud is in that state.

Policy safety valve: a built-in residency check reads the real plan JSON and
FAILs ``SC.L2-3.13.1`` when any planned region/location is non-US. Where OPA /
Checkov / Trivy are installed they can augment this (best-effort hook); absent
them, the built-in check is the floor so the plan is never un-checked.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from evidence.binding import CollectionMetadata, bind_evidence
from evidence.generators import EvidenceArtifact, Generator, GeneratorContext

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TF_DIR = REPO_ROOT / "terraform" / "tier1"

# Union of the machine-verifiable controls (non-inherited modules) this path can
# address — mirrors terraform/tier1/main.tf ↔ structural/tier1.ttl.
MACHINE_CONTROLS: list[str] = sorted({
    "IA.L2-3.5.3", "IA.L2-3.5.2", "IA.L2-3.5.4",
    "SC.L2-3.13.11", "SC.L2-3.13.10", "SC.L2-3.13.16",
    "AC.L2-3.1.1", "AC.L2-3.1.2", "AC.L2-3.1.5", "AC.L2-3.1.3",
    "SC.L2-3.13.1",
    "AU.L2-3.3.1", "AU.L2-3.3.2", "AU.L2-3.3.5",
    "CM.L2-3.4.6", "CM.L2-3.4.7", "CM.L2-3.4.1", "CM.L2-3.4.2",
    "SI.L2-3.14.3", "SI.L2-3.14.6",
})

# The control whose evidence is the residency safety valve.
REGION_CONTROL = "SC.L2-3.13.1"

EVIDENTIARY_STATUS = "mock-plan"


class TerraformUnavailable(RuntimeError):
    """Raised when the ``terraform`` binary is absent, so tests can skip cleanly."""


def _is_us_region(value: str) -> bool:
    """True if a region/location string denotes a US location."""
    v = str(value).strip().lower()
    if not v:
        return True  # empty → not a residency signal
    if "us-locations" in v:
        return True
    # strip an "in:" org-policy prefix
    v = v.split(":", 1)[-1]
    return v == "us" or v.startswith("us-") or v.startswith("us")


class TerraformPlanGenerator:
    """Generator: real ``terraform plan`` → control-addressed plan evidence.

    Implements the U6 :class:`Generator` protocol. ``tf_vars`` are passed as
    ``-var`` flags (e.g. ``{"primary_region": "europe-west1"}`` to exercise the
    residency safety valve).
    """

    controls: list[str] = MACHINE_CONTROLS

    def __init__(
        self,
        tf_dir: Path | str = DEFAULT_TF_DIR,
        tf_vars: dict[str, str] | None = None,
        terraform_bin: str | None = None,
    ) -> None:
        self.tf_dir = Path(tf_dir)
        self.tf_vars = dict(tf_vars or {})
        self.terraform_bin = terraform_bin

    # -- terraform invocation ------------------------------------------------

    def _resolve_binary(self) -> str:
        tf = self.terraform_bin or shutil.which("terraform")
        if not tf:
            raise TerraformUnavailable("terraform binary not found on PATH")
        return tf

    def _run(self, tf: str, *args: str, env: dict | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [tf, f"-chdir={self.tf_dir}", *args],
            capture_output=True, text=True, env=env, timeout=300,
        )

    def _plan_env(self) -> dict:
        import os
        env = dict(os.environ)
        # Dummy token: create-only plan never mints it, so no cloud is contacted.
        env.setdefault("GOOGLE_OAUTH_ACCESS_TOKEN", "mock-plan-no-cloud")
        env.setdefault("GOOGLE_PROJECT", self.tf_vars.get("project_id", "nv012-cui-mock"))
        return env

    def plan_json(self) -> dict:
        """Run init/validate/plan/show and return the parsed plan JSON.

        Raises :class:`TerraformUnavailable` if terraform is absent, and
        ``RuntimeError`` if a terraform step fails.
        """
        tf = self._resolve_binary()
        env = self._plan_env()

        init = self._run(tf, "init", "-backend=false", "-input=false", env=env)
        if init.returncode != 0:
            raise RuntimeError(f"terraform init failed:\n{init.stderr or init.stdout}")

        validate = self._run(tf, "validate", env=env)
        if validate.returncode != 0:
            raise RuntimeError(f"terraform validate failed:\n{validate.stderr or validate.stdout}")

        with tempfile.NamedTemporaryFile(suffix=".tfplan", delete=False) as fh:
            plan_path = fh.name
        try:
            var_args = [f"-var={k}={v}" for k, v in self.tf_vars.items()]
            plan = self._run(tf, "plan", "-input=false", f"-out={plan_path}", *var_args, env=env)
            if plan.returncode != 0:
                raise RuntimeError(f"terraform plan failed:\n{plan.stderr or plan.stdout}")
            show = self._run(tf, "show", "-json", plan_path, env=env)
            if show.returncode != 0:
                raise RuntimeError(f"terraform show failed:\n{show.stderr or show.stdout}")
            return json.loads(show.stdout)
        finally:
            Path(plan_path).unlink(missing_ok=True)

    def terraform_version(self, tf: str | None = None) -> str:
        try:
            tf = tf or self._resolve_binary()
        except TerraformUnavailable:
            return "unknown"
        out = subprocess.run([tf, "version", "-json"], capture_output=True, text=True, timeout=30)
        try:
            return json.loads(out.stdout).get("terraform_version", "unknown")
        except Exception:
            return "unknown"

    # -- plan JSON → evidence artifacts -------------------------------------

    @staticmethod
    def _planned_resources(plan: dict) -> list[dict]:
        return plan.get("planned_values", {}).get("root_module", {}).get("resources", [])

    @classmethod
    def _region_signals(cls, resources: list[dict]) -> list[str]:
        """All region/location strings that bear on data residency."""
        signals: list[str] = []
        for r in resources:
            vals = r.get("values", {})
            if r["type"] == "terraform_data":
                reg = vals.get("input", {}).get("region")
                if reg:
                    signals.append(reg)
            if r["type"] in ("google_kms_key_ring", "google_storage_bucket"):
                if vals.get("location"):
                    signals.append(vals["location"])
            if r["address"].endswith("resource_locations"):
                try:
                    for v in vals["spec"][0]["rules"][0]["values"][0]["allowed_values"]:
                        signals.append(v)
                except (KeyError, IndexError, TypeError):
                    pass
        return signals

    def artifacts_from_plan(self, plan: dict) -> list[EvidenceArtifact]:
        resources = self._planned_resources(plan)
        tags = [r for r in resources
                if r["type"] == "terraform_data" and "controls" in r.get("values", {}).get("input", {})]

        signals = self._region_signals(resources)
        non_us = [s for s in signals if not _is_us_region(s)]
        region_ok = not non_us

        version = self.terraform_version()
        collected_at = datetime.now(timezone.utc).isoformat()
        md = CollectionMetadata(
            source_system="terraform.plan",
            export_command=(f"terraform -chdir={self.tf_dir} init -backend=false && "
                            "validate && plan -out=<tmp> && show -json <tmp>"),
            collected_at=collected_at,
            collector_version=f"terraform {version}",
        )

        artifacts: list[EvidenceArtifact] = []
        for tag in sorted(tags, key=lambda r: r["values"]["input"]["module"]):
            inp = tag["values"]["input"]
            module = inp["module"]
            controls = list(inp["controls"])
            resource_ids = list(inp.get("resources", []))
            inherited = bool(inp.get("inherited", False))

            # Inherited modules (CSP physical) are MET-by-inheritance / human-
            # attested — there is nothing in a terraform plan to machine-verify.
            if inherited:
                continue

            addresses_region = REGION_CONTROL in controls
            passed = region_ok if addresses_region else True
            status = "PASS" if passed else "FAIL"

            summary: dict = {
                "module": module,
                "resource_ids": resource_ids,
                "controls": controls,
                "planned": True,
                "region": inp.get("region"),
            }
            if addresses_region:
                summary["data_region"] = "US" if region_ok else "NON-US"

            detail = (f"plan check for module {module}: {status}"
                      + (f"; non-US residency signals: {sorted(set(non_us))}"
                         if addresses_region and not region_ok else ""))
            result = {
                "status": status,
                "detail": detail,
                "check": "terraform-plan-residency" if addresses_region else "terraform-plan-presence",
                "module": module,
                "resource_ids": resource_ids,
                "metrics": summary,
            }
            raw = {"module": module, "controls": controls, "resources": resource_ids,
                   "region": inp.get("region"), "result": result}

            artifacts.append(EvidenceArtifact(
                raw_bytes=json.dumps(raw, sort_keys=True).encode("utf-8"),
                summary=summary,
                controls=controls,
                collection_metadata=md,
                evidentiary_status=EVIDENTIARY_STATUS,
                method="policy-check",
                source_file=f"terraform/tier1 :: {module}",
                tool="terraform-plan",
                result=result,
            ))
        return artifacts

    # -- Generator protocol + binding ---------------------------------------

    def collect(self, ctx: GeneratorContext | None = None) -> list[EvidenceArtifact]:
        """Run terraform and return plan-derived evidence artifacts.

        Raises :class:`TerraformUnavailable` when the binary is absent (tests
        skip rather than error).
        """
        return self.artifacts_from_plan(self.plan_json())

    def bind(self, graph, ctx: GeneratorContext | None = None,
             artifacts: list[EvidenceArtifact] | None = None) -> list:
        """Collect (if needed) and bind each artifact via the U6 evidence layer.

        Returns the list of bound ``ce:Evidence`` IRIs.
        """
        if artifacts is None:
            artifacts = self.collect(ctx)
        return [bind_evidence(graph, art) for art in artifacts]


# Protocol conformance smoke check.
assert isinstance(TerraformPlanGenerator(), Generator)
