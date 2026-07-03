"""The ontology build pipeline (offline, deterministic, budget-gated)."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

from scripts.build_ontology import (
    TRIPLE_BUDGET,
    VENDORED,
    build,
)
from scripts import fetch_imports

CMMC = Namespace("http://dynamicalsystems.group/ontology/cmmc#")
_ROOT = Path(__file__).resolve().parent.parent
_IMPORTS = _ROOT / "ontology" / "imports"


def _build(tmp_path, **kw):
    out = tmp_path / "cmmc.ttl"
    man = tmp_path / "cmmc_manifest.json"
    rc = build(out_file=out, manifest_file=man, verbose=False, **kw)
    return rc, out, man


def test_build_succeeds_and_emits_artifact_and_manifest(tmp_path):
    rc, out, man = _build(tmp_path)
    assert rc == 0
    assert out.exists() and man.exists()


def test_built_ttl_reloads_with_exactly_110_controls(tmp_path):
    _, out, _ = _build(tmp_path)
    g = Graph()
    g.parse(out, format="turtle")
    controls = set(g.subjects(RDF.type, CMMC.Control))
    assert len(controls) == 110


def test_manifest_shape(tmp_path):
    _, _, man = _build(tmp_path)
    m = json.loads(man.read_text())
    assert m["offline"] is True
    assert m["artifact"]["total_triples"] == 1057
    assert m["triple_budget"]["value"] == TRIPLE_BUDGET
    assert m["triple_budget"]["headroom"] == TRIPLE_BUDGET - 1057
    # input hashes recorded for provenance
    assert len(m["edit_source"]["sha256"]) == 64
    assert len(m["shapes_source"]["sha256"]) == 64
    # every vendored import hashed + counted, OSLC dropped
    assert set(m["imports"]) == {"PROV-O", "EARL", "OntoGSN", "P-PLAN"}
    for info in m["imports"].values():
        assert len(info["sha256"]) == 64
        assert info["total_triples"] > 0
        assert info["missing_terms"] == []


def test_build_is_offline_vendored_imports_present():
    # OSLC dropped; the four needed imports are vendored in-repo.
    assert {vi.filename for vi in VENDORED} == {
        "prov-o.ttl", "earl.ttl", "ontogsn.ttl", "p-plan.ttl"
    }
    for vi in VENDORED:
        assert (_IMPORTS / vi.filename).exists(), f"missing vendored {vi.filename}"


def test_build_is_reproducible_byte_identical(tmp_path):
    _, out1, man1 = _build(tmp_path / "a")
    _, out2, man2 = _build(tmp_path / "b")
    assert out1.read_bytes() == out2.read_bytes()
    # manifests differ only by nothing here (same input paths) -> identical
    assert json.loads(man1.read_text())["build_time"] == json.loads(man2.read_text())["build_time"]
    assert out1.read_bytes() == out2.read_bytes()


def test_source_date_epoch_controls_build_time(tmp_path, monkeypatch):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1000000000")  # 2001-09-09T01:46:40Z
    _, _, man = _build(tmp_path)
    m = json.loads(man.read_text())
    assert m["build_time"] == "2001-09-09T01:46:40Z"


def test_over_budget_build_fails_and_writes_nothing(tmp_path):
    out = tmp_path / "cmmc.ttl"
    man = tmp_path / "cmmc_manifest.json"
    rc = build(out_file=out, manifest_file=man, triple_budget=5, verbose=False)
    assert rc == 1
    assert not out.exists()          # gate fires BEFORE writing the artifact
    assert not man.exists()


def test_fetch_imports_drops_oslc():
    names = {s.name for s in fetch_imports.SOURCES}
    assert names == {"PROV-O", "EARL", "OntoGSN", "P-PLAN"}
    assert not any("OSLC" in n for n in names)


@pytest.mark.network
@pytest.mark.skipif(
    not os.environ.get("RUN_NETWORK_TESTS"),
    reason="network refresh path — set RUN_NETWORK_TESTS=1 to run",
)
def test_fetch_imports_refresh_network(tmp_path):  # pragma: no cover - opt-in
    # Only runs when explicitly opted in; the build itself never needs this.
    assert fetch_imports.fetch_all() == 0
