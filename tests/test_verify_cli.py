"""The `ce verify` command (KI-1 fix).

Guards that the tamper/SHACL re-verification command runs (it was dead code — a
bare `import traceability.verification` that raised ModuleNotFoundError), passes
on a clean NON-EVIDENTIARY demo run with an advisory (not a hard failure), and
still catches actual tampering.
"""

from __future__ import annotations

from pathlib import Path

from rdflib import RDF, Literal
from typer.testing import CliRunner

from compliance_engine.cli import _load_ds, _save_ds, app
from compliance_engine.ontology.prefixes import CE

runner = CliRunner()


def _demo(out: Path) -> Path:
    result = runner.invoke(app, ["demo", "--output-dir", str(out)])
    assert result.exit_code == 0, result.output
    return out


def test_verify_runs_and_passes_on_clean_mock_demo(tmp_path):
    out = _demo(tmp_path / "out")
    result = runner.invoke(app, ["verify", "--output-dir", str(out)])
    assert result.exit_code == 0, result.output
    assert "No tampering detected" in result.output
    # forward-traceability gaps on human-only controls are advisory on mock data
    assert "NON-EVIDENTIARY" in result.output


def test_verify_detects_tampering(tmp_path):
    out = _demo(tmp_path / "out")
    # Corrupt one evidence node's stored content hash on disk.
    ds = _load_ds(out)
    corrupted = False
    for g in ds.graphs():
        for ev in list(g.subjects(RDF.type, CE.Evidence)):
            ch = g.value(ev, CE.contentHash)
            if ch is not None:
                g.remove((ev, CE.contentHash, ch))
                g.add((ev, CE.contentHash, Literal("deadbeef" * 8)))
                corrupted = True
                break
        if corrupted:
            break
    assert corrupted, "no evidence node found to corrupt"
    _save_ds(ds, out)

    result = runner.invoke(app, ["verify", "--output-dir", str(out)])
    assert result.exit_code == 1
    assert "TAMPERING DETECTED" in result.output
