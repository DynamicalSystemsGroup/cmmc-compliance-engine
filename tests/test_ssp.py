"""Tests for the SSP + Traceability Matrix compiler (U12a).

Ported from ADCS `test_design_description.py`: byte-stability, data-derived
document date, the drift gate, plus the CMMC-specific VCRM column set and the
R12 NON-EVIDENTIARY banner. The fixture loads the committed catalog + tier1
allocation (all 110 controls) and adds a couple of evidence + attestation nodes
inline.
"""

from __future__ import annotations

from pathlib import Path

from rdflib import BNode, Literal
from rdflib.namespace import RDF, RDFS, XSD
from typer.testing import CliRunner

from ontology.prefixes import CE, CMMC, EARL, GSN, PROV
from pipeline.dataset import create_dataset, graph_for, load_into
from documents.ssp import (
    SprsSummary,
    app,
    compile_ssp,
    dataset_fingerprint,
    document_date,
)

_REPO = Path(__file__).resolve().parents[1]
_CATALOG = _REPO / "ontology" / "cmmc-edit.ttl"
_TIER1 = _REPO / "structural" / "tier1.ttl"

runner = CliRunner()

_VCRM_HEADER = ("| Control | Implementation | Responsible party | Evidence location "
                "| Evidence hash | Status | Gap notes | POA&M ref |")


def _add_evidence(g, ev_id, control_id, content_hash, *, status=None,
                  source_file="fixtures/x.json", gen_time=None):
    ev = CE[f"evidence/{ev_id}"]
    g.add((ev, RDF.type, CE.Evidence))
    g.add((ev, CE.contentHash, Literal(content_hash)))
    g.add((ev, CE.resultSummary, Literal(f"summary for {control_id}")))
    g.add((ev, CE.addresses, CMMC[control_id]))
    g.add((ev, CE.sourceFile, Literal(source_file)))
    if status:
        g.add((ev, CE.evidentiaryStatus, Literal(status)))
    if gen_time:
        g.add((ev, PROV.generatedAtTime, Literal(gen_time, datatype=XSD.dateTime)))
    return ev


def _add_attestation(g, att_id, control_id, outcome, official, adequacy, sufficiency,
                     *, timestamp="2026-07-01T00:00:00+00:00", override=None):
    att = CE[f"att/{att_id}"]
    agent = CE[f"agent/{official.replace(' ', '-')}"]
    adq = BNode()
    suf = BNode()
    g.add((att, RDF.type, CE.Attestation))
    g.add((att, CE.attests, CMMC[control_id]))
    g.add((att, CE.hasOutcome, outcome))
    g.add((att, PROV.wasAssociatedWith, agent))
    g.add((att, PROV.generatedAtTime, Literal(timestamp, datatype=XSD.dateTime)))
    g.add((agent, RDFS.label, Literal(official)))
    g.add((att, GSN.inContextOf, adq))
    g.add((adq, RDF.type, GSN.Assumption))
    g.add((adq, GSN.statement, Literal(adequacy)))
    g.add((att, GSN.inContextOf, suf))
    g.add((suf, RDF.type, GSN.Justification))
    g.add((suf, GSN.statement, Literal(sufficiency)))
    if override:
        g.add((att, CMMC.overrideJustification, Literal(override)))
    return att


def _base_dataset(*, mock=False, max_time="2026-07-02T12:00:00+00:00"):
    ds = create_dataset()
    load_into(ds, "ontology", _CATALOG)
    load_into(ds, "structural", _TIER1)
    ev_g = graph_for(ds, "evidence")
    att_g = graph_for(ds, "attestations")

    _add_evidence(ev_g, "iam", "AC.L2-3.1.1", "a" * 64,
                  status="mock" if mock else None,
                  gen_time="2026-07-01T09:00:00+00:00")
    _add_evidence(ev_g, "region", "SC.L2-3.13.1", "b" * 64,
                  status="mock-plan" if mock else None,
                  gen_time=max_time)
    _add_attestation(att_g, "a1", "AC.L2-3.1.1", EARL.passed, "Jane Official",
                     "Implementation adequate.", "Evidence sufficient for MET.")
    return ds


def _write_trig(ds, path: Path) -> Path:
    ds.serialize(destination=str(path), format="trig")
    return path


# --------------------------------------------------------------------------- #
# Determinism
# --------------------------------------------------------------------------- #

class TestDeterminism:
    def test_compile_twice_byte_identical(self, tmp_path):
        trig = _write_trig(_base_dataset(), tmp_path / "d.trig")
        a = create_dataset(); a.parse(trig, format="trig")
        b = create_dataset(); b.parse(trig, format="trig")
        doc_a = compile_ssp(a, dataset_path=trig)
        doc_b = compile_ssp(b, dataset_path=trig)
        assert doc_a == doc_b
        assert doc_a.endswith("\n") and not doc_a.endswith("\n\n")

    def test_fingerprint_stable_across_reparse(self, tmp_path):
        trig = _write_trig(_base_dataset(), tmp_path / "d.trig")
        a = create_dataset(); a.parse(trig, format="trig")
        b = create_dataset(); b.parse(trig, format="trig")
        # Blank-node GSN nodes relabel on each parse; fingerprint must not move.
        assert dataset_fingerprint(a) == dataset_fingerprint(b)

    def test_document_date_is_max_generated_at_not_wall_clock(self):
        early = _base_dataset(max_time="2026-07-02T12:00:00+00:00")
        late = _base_dataset(max_time="2026-09-09T09:09:09+00:00")
        assert document_date(early) == "2026-07-02T12:00:00+00:00"
        assert document_date(late) == "2026-09-09T09:09:09+00:00"
        # The date tracks the mutated timestamp, and appears in the document.
        assert "2026-09-09T09:09:09+00:00" in compile_ssp(late)


# --------------------------------------------------------------------------- #
# VCRM / Document 2
# --------------------------------------------------------------------------- #

class TestVcrm:
    def test_all_110_controls_listed_with_status(self):
        ds = _base_dataset()
        doc = compile_ssp(ds)
        from documents.queries import CONTROLS_FULL, query_to_dicts
        ids = [r["controlId"] for r in query_to_dicts(ds, CONTROLS_FULL)]
        assert len(ids) == 110
        for cid in ids:
            assert f"| {cid} |" in doc, f"{cid} missing from VCRM"

    def test_matrix_column_set_matches_document_2(self):
        doc = compile_ssp(_base_dataset())
        assert _VCRM_HEADER in doc

    def test_attested_control_shows_met_unattested_shows_planned(self):
        doc = compile_ssp(_base_dataset())
        # AC.L2-3.1.1 is attested passed -> MET; pick an unattested control.
        met_row = next(l for l in doc.splitlines() if l.startswith("| AC.L2-3.1.1 |"))
        assert "| MET |" in met_row
        planned_row = next(l for l in doc.splitlines() if l.startswith("| AU.L2-3.3.2 |"))
        assert "| PLANNED |" in planned_row
        assert "not attested" in planned_row

    def test_implementation_and_official_populated(self):
        doc = compile_ssp(_base_dataset())
        row = next(l for l in doc.splitlines() if l.startswith("| AC.L2-3.1.1 |"))
        assert "Jane Official" in row              # responsible party
        assert "least-privilege" in row.lower()    # tier1 module label


# --------------------------------------------------------------------------- #
# R12 non-evidentiary banner
# --------------------------------------------------------------------------- #

class TestR12Banner:
    def test_mock_dataset_renders_banner_and_colophon_stamp(self):
        doc = compile_ssp(_base_dataset(mock=True))
        assert "NON-EVIDENTIARY" in doc
        # Banner near the top (before the VCRM).
        assert doc.index("NON-EVIDENTIARY") < doc.index("Verification Cross-Reference")
        # Stamped in the colophon too (cannot be omitted).
        assert "NON-EVIDENTIARY stamp:" in doc
        assert "mock" in doc and "mock-plan" in doc

    def test_evidentiary_dataset_has_no_banner(self):
        doc = compile_ssp(_base_dataset(mock=False))
        assert "NON-EVIDENTIARY" not in doc
        assert "| Evidentiary status | evidentiary |" in doc


# --------------------------------------------------------------------------- #
# Colophon hooks (SPRS + BOM)
# --------------------------------------------------------------------------- #

class TestColophonHooks:
    def test_sprs_hook_pending_when_none(self):
        doc = compile_ssp(_base_dataset())
        assert "SPRS summary: pending audit (U10/U11 integration)." in doc

    def test_sprs_hook_renders_when_provided(self):
        summary = SprsSummary(score=110, status="Final", met_by_machine=5,
                              met_by_human_only=105, contradiction_count=0)
        doc = compile_ssp(_base_dataset(), sprs_summary=summary)
        assert "score 110 (Final)" in doc
        assert "5 MET-by-machine / 105 MET-by-human-only" in doc
        assert "contradictions: 0" in doc

    def test_bom_hook_falls_back_to_committed_hashes(self):
        doc = compile_ssp(_base_dataset())
        # Falls back to the committed ce:contentHash values (two evidence nodes).
        assert "committed ce:contentHash (BOM pending)" in doc
        assert f"- `{'a' * 64}`" in doc

    def test_bom_hook_uses_supplied_hashes(self):
        doc = compile_ssp(_base_dataset(), bom_artifact_hashes=["c" * 64])
        assert "Artifact hashes (BOM): 1" in doc
        assert f"- `{'c' * 64}`" in doc


# --------------------------------------------------------------------------- #
# CLI drift gate
# --------------------------------------------------------------------------- #

class TestCliDriftGate:
    def test_build_then_check_clean_then_drift(self, tmp_path):
        trig = _write_trig(_base_dataset(), tmp_path / "d.trig")
        out = tmp_path / "ssp.md"

        r = runner.invoke(app, ["build", "--input", str(trig), "--output", str(out)])
        assert r.exit_code == 0, r.output
        assert out.exists()

        r = runner.invoke(app, ["build", "--input", str(trig), "--output", str(out), "--check"])
        assert r.exit_code == 0, r.output

        out.write_bytes(out.read_bytes() + b"tampered\n")
        r = runner.invoke(app, ["build", "--input", str(trig), "--output", str(out), "--check"])
        assert r.exit_code == 1

    def test_check_missing_output_exits_2(self, tmp_path):
        trig = _write_trig(_base_dataset(), tmp_path / "d.trig")
        r = runner.invoke(app, ["build", "--input", str(trig),
                                "--output", str(tmp_path / "never.md"), "--check"])
        assert r.exit_code == 2

    def test_missing_input_exits_2(self, tmp_path):
        r = runner.invoke(app, ["build", "--input", str(tmp_path / "nope.trig"),
                                "--output", str(tmp_path / "o.md")])
        assert r.exit_code == 2
