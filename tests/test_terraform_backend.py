"""TerraformBackend mechanism tests against a self-contained HCL fixture.

Marked @pytest.mark.terraform and skipped if the binary is absent. Points the
backend at tests/fixtures/tf_min/ (NOT terraform/tier1/). Run:

    uv run pytest -m terraform tests/test_terraform_backend.py -q
"""

import shutil
from pathlib import Path

import pytest

from compliance_engine.pipeline.provision import (
    PlanResult,
    TerraformBackend,
    TerraformUnavailable,
    assert_planresult_conformant,
)

TF_MIN = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "tf_min"

pytestmark = [
    pytest.mark.terraform,
    pytest.mark.skipif(
        shutil.which("terraform") is None, reason="terraform binary not installed"
    ),
]

@pytest.fixture()
def backend() -> TerraformBackend:
    return TerraformBackend(chdir=TF_MIN)

def test_probe_succeeds_on_fixture(backend):
    backend.probe()  # init -backend=false must succeed offline (terraform_data)

def test_validate_passes_on_fixture(backend):
    backend.probe()
    backend.validate()

def test_plan_show_json_yields_conformant_planresult(backend):
    backend.probe()
    pr = backend.plan()
    assert isinstance(pr, PlanResult)
    # Seam conformance — pins the schema so LiveTerraformBackend is a real swap.
    assert_planresult_conformant(pr)
    # The fixture's two resources parse with their compliance labels.
    ids = set(pr.resource_ids())
    assert {"OrgPolicy_USRegion", "CMEK_KeyRing"} <= ids
    # cmmc_control labels map to control ids.
    assert "SC.L2-3.13.1" in pr.controls()
    assert "SC.L2-3.13.11" in pr.controls()
    # regions parsed (US).
    assert all(r.startswith("us") for r in pr.regions().values())

def test_planned_resources_carry_stable_join_key(backend):
    """resource_id (the BOM join key) matches a tier1.ttl module local-name."""
    backend.probe()
    pr = backend.plan()
    org = pr.by_id("OrgPolicy_USRegion")
    assert org is not None
    assert org.type == "terraform_data"
    assert "SC.L2-3.13.1" in org.controls
    assert org.region == "us-central1"

def test_missing_binary_raises_terraform_unavailable():
    """A bogus binary name ⇒ TerraformUnavailable from probe()."""
    b = TerraformBackend(chdir=TF_MIN, binary="terraform-does-not-exist")
    with pytest.raises(TerraformUnavailable):
        b.probe()
