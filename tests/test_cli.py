"""U13a — operator CLI driver (the one-command NV012 demo)."""

import json
import sys
from pathlib import Path

from typer.testing import CliRunner

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import cli  # noqa: E402

runner = CliRunner()


def _run(args, out: Path):
    return runner.invoke(cli.app, [*args, "--output-dir", str(out)])


# ---------------------------------------------------------------------------
# demo — happy path (all-covered)
# ---------------------------------------------------------------------------

def test_demo_all_covered_runs_full_chain(tmp_path):
    res = _run(["demo", "--evidence-set", "all-covered", "--auto"], tmp_path)
    assert res.exit_code == 0, res.output

    # Full chain markers present, incl. the SSP stub step.
    for marker in ("compile-order", "run-factory", "attest", "audit", "bom", "ssp"):
        assert marker in res.output
    # SPRS line printed to stdout.
    assert "SPRS:" in res.output and "score=" in res.output

    # output/bom.json written and mock (R12).
    bom_path = tmp_path / "bom.json"
    assert bom_path.exists()
    bom = json.loads(bom_path.read_text())
    assert bom["evidentiary_status"] == "mock"
    assert bom["contract_id"] == "NV012"
    assert len(bom["control_mapping"]) == 22
    # Audit artifacts written too.
    assert (tmp_path / "audit.json").exists()


# ---------------------------------------------------------------------------
# demo — gap set stops at Gate 1
# ---------------------------------------------------------------------------

def test_demo_gap_stops_at_gate1(tmp_path):
    res = _run(["demo", "--evidence-set", "gap"], tmp_path)
    assert res.exit_code != 0
    assert "Gate 1 REFUSED" in res.output
    assert "AC.L2-3.1.12" in res.output          # the named missing control
    # Factory never ran → no BOM written.
    assert not (tmp_path / "bom.json").exists()


# ---------------------------------------------------------------------------
# demo — contradiction set surfaces R13
# ---------------------------------------------------------------------------

def test_demo_contradiction_reports_r13(tmp_path):
    res = _run(["demo", "--evidence-set", "contradiction"], tmp_path)
    assert res.exit_code == 0, res.output
    assert "Contradictions (R13):" in res.output
    # A MET attestation over a failing oracle (mfa=False) → ≥1 contradiction.
    audit = json.loads((tmp_path / "audit.json").read_text())
    assert len(audit["contradictions"]) >= 1
    assert (tmp_path / "bom.json").exists()


# ---------------------------------------------------------------------------
# ssp subcommand — ImportError stub path
# ---------------------------------------------------------------------------

def test_ssp_stub_when_module_absent(tmp_path, monkeypatch):
    # Force `import documents.ssp` to raise ImportError.
    monkeypatch.setitem(sys.modules, "documents.ssp", None)
    res = _run(["ssp"], tmp_path)
    assert res.exit_code == 0
    assert "SSP: pending U12" in res.output


def test_ssp_present_does_not_crash(tmp_path):
    res = _run(["ssp"], tmp_path)
    assert res.exit_code == 0
    assert "SSP:" in res.output


# ---------------------------------------------------------------------------
# invalid evidence set
# ---------------------------------------------------------------------------

def test_demo_rejects_unknown_evidence_set(tmp_path):
    res = _run(["demo", "--evidence-set", "nope"], tmp_path)
    assert res.exit_code == 2
