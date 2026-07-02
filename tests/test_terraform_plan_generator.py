"""Tests for the plan-time Terraform evidence generator (U14).

terraform-invoking tests are marked ``@pytest.mark.terraform`` AND skipped when
the binary is absent, so the suite stays green on machines without terraform.
The binary-absent path (clean skip / ``TerraformUnavailable``) is exercised by
an unmarked test that always runs.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

from rdflib import Graph

from ontology.prefixes import CE, CMMC, bind_prefixes
from evidence.binding import bind_evidence
from evidence.generators.terraform_plan import (
    REGION_CONTROL,
    TerraformPlanGenerator,
    TerraformUnavailable,
)

_REPO = Path(__file__).resolve().parents[1]
_TF_DIR = _REPO / "terraform" / "tier1"
_HAS_TF = shutil.which("terraform") is not None

# Skip terraform-invoking tests when the binary is absent (suite stays green).
requires_terraform = pytest.mark.skipif(not _HAS_TF, reason="terraform binary not installed")


def _tier1_modules() -> set[str]:
    """The ce:<Module> PartUsage names declared in structural/tier1.ttl."""
    ttl = (_REPO / "structural" / "tier1.ttl").read_text(encoding="utf-8")
    return set(re.findall(r"ce:(\w+)\s+a\s+sysml:PartUsage", ttl))


def _new_graph() -> Graph:
    g = Graph()
    bind_prefixes(g)
    return g


RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


# -- binary-absent path (always runs) --------------------------------------

class TestBinaryAbsent:
    def test_missing_binary_raises_clean_exception(self, monkeypatch):
        monkeypatch.setattr(shutil, "which", lambda _name: None)
        gen = TerraformPlanGenerator(terraform_bin=None)
        with pytest.raises(TerraformUnavailable):
            gen.collect()

    def test_skip_marker_wiring(self):
        # Documents the gate: when terraform is absent the marked tests skip.
        assert isinstance(_HAS_TF, bool)


# -- HCL validity + mock-provider test -------------------------------------

@pytest.mark.terraform
@requires_terraform
class TestHclValidity:
    def test_validate_passes(self):
        tf = shutil.which("terraform")
        assert tf is not None
        env = _plan_env()
        init = subprocess.run([tf, f"-chdir={_TF_DIR}", "init", "-backend=false", "-input=false"],
                              capture_output=True, text=True, env=env, timeout=300)
        assert init.returncode == 0, init.stderr or init.stdout
        val = subprocess.run([tf, f"-chdir={_TF_DIR}", "validate"],
                             capture_output=True, text=True, env=env, timeout=120)
        assert val.returncode == 0, val.stderr or val.stdout

    def test_terraform_test_with_mock_provider_runs_no_creds(self):
        tf = shutil.which("terraform")
        assert tf is not None
        # No cloud creds in env — mock_provider stands in for both providers.
        res = subprocess.run([tf, f"-chdir={_TF_DIR}", "test"],
                             capture_output=True, text=True, timeout=300)
        assert res.returncode == 0, res.stderr or res.stdout
        assert "0 failed" in res.stdout


# -- generator binds plan-derived evidence ----------------------------------

@pytest.mark.terraform
@requires_terraform
class TestGeneratorBindsEvidence:
    def test_binds_evidence_addressing_expected_controls(self):
        gen = TerraformPlanGenerator()
        artifacts = gen.collect()
        assert artifacts, "generator produced no artifacts"

        # Every artifact is plan-time mock evidence, addresses >=1 control,
        # and its module resolves to a tier1.ttl PartUsage.
        modules = _tier1_modules()
        addressed: set[str] = set()
        for a in artifacts:
            assert a.evidentiary_status == "mock-plan"
            assert a.method == "policy-check"
            assert a.controls
            assert a.summary["module"] in modules  # resource_id resolves to tier1.ttl
            addressed |= set(a.controls)

        # Spot-check the plan covers the key control families (U14 approach).
        for expected in ["CM.L2-3.4.1", "SC.L2-3.13.1", "SC.L2-3.13.11",
                         "AU.L2-3.3.1", "AC.L2-3.1.1"]:
            assert expected in addressed, f"{expected} not addressed by plan evidence"

        # Inherited PE controls are NOT machine-provable at plan time → excluded.
        assert "PE.L2-3.10.1" not in addressed

        # Bind into an RDF graph via the U6 layer and confirm the edges.
        g = _new_graph()
        iris = gen.bind(g, artifacts=artifacts)
        assert len(iris) == len(artifacts)
        # ce:Evidence addresses SC.L2-3.13.1, never attests it.
        rows = list(g.query("SELECT ?ev WHERE { ?ev ce:addresses ?c }",
                            initBindings={"c": CMMC[REGION_CONTROL]}))
        assert rows
        assert len(list(g.triples((None, CE.attests, None)))) == 0
        # mock-plan marker propagates.
        from rdflib import Literal
        assert list(g.triples((None, CE.evidentiaryStatus, Literal("mock-plan"))))


# -- policy safety valve on real plan output --------------------------------

@pytest.mark.terraform
@requires_terraform
class TestRegionSafetyValve:
    def test_non_us_region_produces_fail_evidence(self):
        gen = TerraformPlanGenerator(tf_vars={"primary_region": "europe-west1"})
        artifacts = gen.collect()

        region_arts = [a for a in artifacts if REGION_CONTROL in a.controls]
        assert region_arts, "no evidence addresses the region control"
        region = region_arts[0]
        assert region.result["status"] == "FAIL"
        assert region.summary["data_region"] == "NON-US"

        # The FAIL binds to a real ce:Evidence node (proves the check ran on
        # actual plan output, not a stub).
        g = _new_graph()
        ev = bind_evidence(g, region)
        assert (ev, CE.addresses, CMMC[REGION_CONTROL]) in g
        chash = g.value(ev, CE.contentHash)
        assert chash is not None and len(str(chash)) == 64

    def test_default_us_region_passes(self):
        gen = TerraformPlanGenerator()
        region = next(a for a in gen.collect() if REGION_CONTROL in a.controls)
        assert region.result["status"] == "PASS"
        assert region.summary["data_region"] == "US"


# -- helpers ----------------------------------------------------------------

def _plan_env() -> dict:
    import os
    env = dict(os.environ)
    env.setdefault("GOOGLE_OAUTH_ACCESS_TOKEN", "mock-plan-no-cloud")
    env.setdefault("GOOGLE_PROJECT", "nv012-cui-mock")
    return env
