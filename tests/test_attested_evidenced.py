"""Attested-reference chain wired end to end: human attestation backed by
machine-recorded document evidence (resolve -> hash -> git commit -> signed upload),
with real teeth (a stale / dead-link / wrong-signer reference is NOT marked MET).

These tests deliberately include NEGATIVE cases: a stale reference and a dead-link
reference must drop the control out of MET, and a tampered upload receipt must fail
to verify. A test that only asserted the happy path would pass even if the gate had
no teeth — the point here is that it does.
"""

from __future__ import annotations

import dataclasses
import json
import pathlib
import tempfile
from datetime import datetime, timedelta, timezone

from typer.testing import CliRunner

from compliance_engine import cli
from compliance_engine.oracles.attested_reference import evaluate_attested_reference
from compliance_engine.order_compiler import compiler
from compliance_engine.pipeline.evidence import doc_evidence
from compliance_engine.traceability.references import load_attested_controls

runner = CliRunner()

_SSP_URI = "file://documents/policies/POL_SSP_SystemDescription.md"
_SSP_CONTROL = "CA.L2-3.12.4"


# ---------------------------------------------------------------------------
# Document evidence capture: resolve -> hash -> git -> signed upload receipt
# ---------------------------------------------------------------------------

def test_capture_resolves_hashes_and_signs_upload_receipt():
    ev = doc_evidence.capture("REF_POL_SSP_v1", _SSP_URI, "Sayer Tindall (AO)")
    assert ev.exists is True
    assert ev.resolved_path and ev.resolved_path.endswith("POL_SSP_SystemDescription.md")
    assert ev.sha256 and len(ev.sha256) == 64          # real SHA-256 of the file
    assert ev.git_commit and len(ev.git_commit) == 40  # real commit that produced it
    assert ev.upload_sig_algo == "ed25519-v1" and ev.upload_sig
    # The signed upload receipt re-verifies (offline, deterministic).
    assert doc_evidence.verify_upload_receipt(ev) is True


def test_capture_dead_link_yields_unresolved_and_no_receipt():
    ev = doc_evidence.capture("REF_BOGUS", "file://documents/policies/DOES_NOT_EXIST.md", "AO")
    assert ev.exists is False
    assert ev.sha256 is None
    assert doc_evidence.verify_upload_receipt(ev) is False


def test_tampered_upload_receipt_fails_verification():
    ev = doc_evidence.capture("REF_POL_SSP_v1", _SSP_URI, "Sayer Tindall (AO)")
    # Flip the recorded content hash — the receipt no longer covers these bytes.
    tampered = dataclasses.replace(ev, sha256="0" * 64)
    assert doc_evidence.verify_upload_receipt(tampered) is False


# ---------------------------------------------------------------------------
# Reference views + the oracle's teeth (fresh passes, stale/dead-link fail)
# ---------------------------------------------------------------------------

def _ssp_control():
    ds, _obl = compiler.load_pipeline_dataset()
    attested = load_attested_controls(ds)
    assert _SSP_CONTROL in attested, "CA.L2-3.12.4 must map to an attested-reference module"
    return attested[_SSP_CONTROL]


def test_reference_view_built_from_graph():
    ac = _ssp_control()
    assert ac.reference_id == "REF_POL_SSP_v1"
    assert ac.required_role == "Role_AffirmingOfficial"
    assert ac.view is not None and ac.view.uri == _SSP_URI
    assert ac.view.last_verified is not None and ac.view.freshness_days >= 1


def test_oracle_passes_on_fresh_resolved_role_signed_reference():
    from compliance_engine.traceability.attestation_store import load_all

    ac = _ssp_control()
    ev = doc_evidence.capture(ac.reference_id, ac.uri, ac.custodian)
    view = dataclasses.replace(ac.view, resolved_ok=ev.exists)
    records = load_all(pathlib.Path(cli.__file__).resolve().parent.parent.parent / "data" / "attestations")
    # "now" one day after lastVerified — comfortably fresh.
    now = ac.view.last_verified + timedelta(days=1)
    result = evaluate_attested_reference(_SSP_CONTROL, view, ac.required_role, records, now=now)
    assert result.outcome == "passed", result.message


def test_oracle_fails_when_reference_is_stale():
    """TEETH: a reference past its freshness window must NOT pass."""
    from compliance_engine.traceability.attestation_store import load_all

    ac = _ssp_control()
    ev = doc_evidence.capture(ac.reference_id, ac.uri, ac.custodian)
    view = dataclasses.replace(ac.view, resolved_ok=ev.exists)
    records = load_all(pathlib.Path(cli.__file__).resolve().parent.parent.parent / "data" / "attestations")
    # "now" a decade after lastVerified — far beyond any freshness window.
    now = ac.view.last_verified + timedelta(days=4000)
    result = evaluate_attested_reference(_SSP_CONTROL, view, ac.required_role, records, now=now)
    assert result.outcome == "failed"
    assert "stale" in (result.reason or "").lower() or "stale" in result.message.lower()


def test_oracle_fails_on_dead_link():
    """TEETH: a reference whose document does not resolve must NOT pass."""
    from compliance_engine.traceability.attestation_store import load_all

    ac = _ssp_control()
    view = dataclasses.replace(ac.view, resolved_ok=False)  # doc did not resolve
    records = load_all(pathlib.Path(cli.__file__).resolve().parent.parent.parent / "data" / "attestations")
    now = ac.view.last_verified + timedelta(days=1)
    result = evaluate_attested_reference(_SSP_CONTROL, view, ac.required_role, records, now=now)
    assert result.outcome == "failed"
    assert result.reason == "reference-unresolvable"


# ---------------------------------------------------------------------------
# End to end through the CLI: the control is attested-evidenced and MET
# ---------------------------------------------------------------------------

def test_ce_demo_full_marks_ca_3_12_4_attested_evidenced():
    out = pathlib.Path(tempfile.mkdtemp(prefix="ce-ae-"))
    result = runner.invoke(cli.app, ["demo", "--full", "--output-dir", str(out)])
    assert result.exit_code == 0, result.output
    bom = json.loads((out / "bom.json").read_text())
    row = next(r for r in bom["control_mapping"] if r["control_id"] == _SSP_CONTROL)
    assert row["status"] == "MET"
    assert row["evidence_backing"] == "attested-evidenced"
    assert row["evidence_hashes"], "attested-evidenced control must carry a document hash"
    assert row["reference_id"] == "REF_POL_SSP_v1"
    assert row["git_commit"], "the git commit that produced the document must be recorded"
    assert row["oracle_outcome"] == "passed"

    # 43 policy controls should move from bare human-only to machine-backed.
    backings = [r["evidence_backing"] for r in bom["control_mapping"]]
    assert backings.count("attested-evidenced") >= 40


def test_manifest_carries_document_provenance():
    out = pathlib.Path(tempfile.mkdtemp(prefix="ce-ae-"))
    assert runner.invoke(cli.app, ["demo", "--full", "--output-dir", str(out)]).exit_code == 0
    manifest = json.loads((out / "package" / "manifest.json").read_text())
    row = next(c for c in manifest["controls"] if c["control"] == _SSP_CONTROL)
    assert row["evidence_backing"] == "attested-evidenced"
    assert row["git_commit"]
    # The attestation is asserted by the real Affirming Official, not a boilerplate name.
    assert row["attestation"]["official"] == "Sayer Tindall"
