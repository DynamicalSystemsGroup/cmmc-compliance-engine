"""TerraformBackend — real `terraform` at plan level with mock providers.

Shells to the installed `terraform` binary:

    terraform -chdir=<dir> init -backend=false     (offline; no remote backend)
    terraform -chdir=<dir> validate
    terraform -chdir=<dir> plan -out=<tmp> -input=false
    terraform -chdir=<dir> show -json <tmp>         → parsed into a PlanResult
    terraform -chdir=<dir> apply -auto-approve <tmp> (mock-provider apply)

`chdir` defaults to `terraform/tier1` (U14's real HCL); tests point it at the
self-contained `tests/fixtures/tf_min/`. The compliance labels on each resource
(`cmmc_module` / `cmmc_control` / `region`) are read from the plan JSON — see
`base.parse_plan_json`.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from pipeline.provision.base import (
    ApplyResult,
    PlanResult,
    ProvisionError,
    TerraformUnavailable,
    parse_plan_json,
)

_DEFAULT_CHDIR = "terraform/tier1"


class TerraformBackend:
    name = "terraform"

    def __init__(
        self,
        chdir: str | Path = _DEFAULT_CHDIR,
        *,
        binary: str = "terraform",
        timeout: int = 120,
    ):
        self.chdir = str(chdir)
        self.binary = binary
        self.timeout = timeout
        self._planfile: str | None = None

    # -- process helper ------------------------------------------------------
    def _run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        cmd = [self.binary, f"-chdir={self.chdir}", *args]
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=self.timeout,
        )
        if check and proc.returncode != 0:
            raise ProvisionError(
                f"`{' '.join(cmd)}` failed (exit {proc.returncode}):\n"
                f"{proc.stderr.strip() or proc.stdout.strip()}"
            )
        return proc

    # -- protocol ------------------------------------------------------------
    def probe(self) -> None:
        if shutil.which(self.binary) is None:
            raise TerraformUnavailable(
                f"terraform binary {self.binary!r} not found on PATH"
            )
        if not Path(self.chdir).is_dir():
            raise TerraformUnavailable(f"terraform dir {self.chdir!r} does not exist")
        proc = self._run("init", "-backend=false", "-input=false", check=False)
        if proc.returncode != 0:
            raise TerraformUnavailable(
                f"`terraform init -backend=false` failed in {self.chdir!r}:\n"
                f"{proc.stderr.strip() or proc.stdout.strip()}"
            )

    def validate(self) -> None:
        self._run("validate", "-no-color")

    def plan(self) -> PlanResult:
        # init is idempotent + cheap; ensures providers/builtins are ready.
        self._run("init", "-backend=false", "-input=false")
        planfile = tempfile.NamedTemporaryFile(
            prefix="ce-tfplan-", suffix=".bin", delete=False,
        ).name
        self._planfile = planfile
        self._run("plan", "-input=false", "-no-color", f"-out={planfile}")
        show = self._run("show", "-json", planfile)
        plan_json = json.loads(show.stdout)
        return PlanResult(plan_json=plan_json, resources=parse_plan_json(plan_json))

    def apply(self) -> ApplyResult:
        """Mock-provider apply. Applies the saved plan and hashes the resulting
        state JSON as the state hash. Live cloud apply is deferred."""
        planfile = self._planfile
        if planfile is None:
            # apply requires a prior plan; produce one if the caller skipped it.
            self.plan()
            planfile = self._planfile
        assert planfile is not None
        self._run("apply", "-input=false", "-no-color", "-auto-approve", planfile)
        state = self._run("show", "-json")
        state_json = json.loads(state.stdout)
        state_hash = hashlib.sha256(
            json.dumps(state_json, sort_keys=True).encode("utf-8")
        ).hexdigest()
        resources = (
            (state_json.get("values", {}) or {})
            .get("root_module", {}).get("resources", []) or []
        )
        return ApplyResult(state_hash=state_hash, applied=True,
                           resource_count=len(resources))

    def describe(self) -> str:
        return f"Terraform (plan-level, mock providers) at {self.chdir}"
