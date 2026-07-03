"""Backend abstraction tests (LocalBackend only).

Adapted from the ADCS test_backends.py, dropping the Flexo/Fuseki/txnlog
mocked-HTTP cases (those backends are not ported). LocalBackend is
exercised live against tmp_path.

Scenarios:
  - get_backend("local") returns a LocalBackend; unknown names raise.
  - LocalBackend.persist() writes .ttl + .trig and re-reads them.
  - probe() succeeds on a writable dir and raises BackendUnavailable on a
    non-writable one.
  - record_uri()/emit_service_node() are no-ops for the local filesystem.
"""

from __future__ import annotations

import warnings

import pytest
from rdflib import Dataset, Graph
from rdflib.namespace import RDF

from ontology.prefixes import CE, G_EVIDENCE, G_ONTOLOGY
from pipeline.backends import get_backend
from pipeline.backends.base import BackendUnavailable, StoreBackend
from pipeline.backends.local import LocalBackend
from pipeline.dataset import create_dataset, graph_for


@pytest.fixture()
def dataset() -> Dataset:
    """A small two-layer dataset to persist."""
    ds = create_dataset()
    onto = graph_for(ds, "ontology")
    for i in range(5):
        onto.add((CE[f"ontology/s{i}"], RDF.type, CE["Control"]))
    ev = graph_for(ds, "evidence")
    for i in range(3):
        ev.add((CE[f"evidence/e{i}"], RDF.type, CE["Evidence"]))
    return ds


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def test_factory_returns_local():
    backend = get_backend("local")
    assert isinstance(backend, LocalBackend)


def test_local_backend_satisfies_protocol():
    assert isinstance(LocalBackend(), StoreBackend)


def test_factory_rejects_unknown_backend():
    with pytest.raises(ValueError, match="Unknown backend"):
        get_backend("not-a-backend")


# ---------------------------------------------------------------------------
# LocalBackend.persist (live)
# ---------------------------------------------------------------------------

def test_local_backend_writes_and_rereads(dataset, tmp_path):
    """persist() writes engine.ttl + engine.trig; both re-parse and the
    TriG preserves the named graphs."""
    backend = LocalBackend()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        counts = backend.persist(dataset, tmp_path)

    ttl = tmp_path / "engine.ttl"
    trig = tmp_path / "engine.trig"
    assert ttl.exists() and trig.exists()

    # Returned per-graph counts cover the layers we populated.
    assert counts.get(G_ONTOLOGY) == 5
    assert counts.get(G_EVIDENCE) == 3

    # Flat union re-reads with the full triple total.
    flat = Graph()
    flat.parse(ttl, format="turtle")
    assert len(flat) == 8

    # TriG re-reads and keeps the two named graphs.
    reloaded = Dataset()
    reloaded.parse(trig, format="trig")
    named = {str(c.identifier) for c in reloaded.contexts() if len(c) > 0}
    assert G_ONTOLOGY in named
    assert G_EVIDENCE in named


def test_local_backend_describe():
    assert "Local filesystem" in LocalBackend().describe()


def test_local_backend_name():
    assert LocalBackend().name == "local"


# ---------------------------------------------------------------------------
# record_uri / emit_service_node — no-ops for the local filesystem
# ---------------------------------------------------------------------------

def test_local_backend_record_uri_returns_none():
    assert LocalBackend().record_uri("evidence") is None


def test_local_backend_emit_service_node_returns_none():
    g = Graph()
    assert LocalBackend().emit_service_node(g, None) is None
    assert len(g) == 0


# ---------------------------------------------------------------------------
# probe (preflight)
# ---------------------------------------------------------------------------

def test_local_backend_probe_succeeds_on_writable_dir(tmp_path):
    LocalBackend().probe(output_dir=tmp_path)
    assert not (tmp_path / ".probe").exists()  # sentinel cleaned up


def test_local_backend_probe_fails_on_unwritable_dir(tmp_path):
    target = tmp_path / "readonly"
    target.mkdir()
    target.chmod(0o555)
    try:
        with pytest.raises(BackendUnavailable, match="not writable"):
            LocalBackend().probe(output_dir=target)
    finally:
        target.chmod(0o755)  # restore so pytest can clean up
