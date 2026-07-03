"""FlexoBackend / FakeFlexoStore tests (offline, deterministic).

Flexo MMS is a versioned, git-like RDF quadstore that will run self-hosted
in an IL4 enclave. The live server is not reachable in this sandbox, so
these tests exercise the offline FakeFlexoStore simulation plus the
connection-guarded real-endpoint path — no network is required.

Scenarios:
  - FlexoBackend satisfies the StoreBackend protocol.
  - probe() is available when backed by a FakeFlexoStore; the guarded
    real-endpoint-unreachable case fails fast (BackendUnavailable, no hang).
  - persist() -> load() round-trips a small multi-graph Dataset with
    identical quads.
  - Append-only versioning: two commits of the same ref with different
    content retain two distinct versions; the earlier one is still
    resolvable unchanged (immutability).
  - Content addressing is stable and deterministic.
"""

from __future__ import annotations

import time
import warnings

import pytest
from rdflib import Dataset, Graph, URIRef
from rdflib.namespace import RDF

from compliance_engine.ontology.prefixes import (
    CE,
    G_EVIDENCE,
    G_ONTOLOGY,
    G_ORDER,
)
from compliance_engine.pipeline.backends.base import BackendUnavailable, StoreBackend
from compliance_engine.pipeline.backends.flexo import FakeFlexoStore, FlexoBackend
from compliance_engine.pipeline.dataset import create_dataset, graph_for


@pytest.fixture()
def dataset() -> Dataset:
    """A small three-layer dataset to persist."""
    ds = create_dataset()
    onto = graph_for(ds, "ontology")
    for i in range(5):
        onto.add((CE[f"ontology/s{i}"], RDF.type, CE["Control"]))
    ev = graph_for(ds, "evidence")
    for i in range(3):
        ev.add((CE[f"evidence/e{i}"], RDF.type, CE["Evidence"]))
    order = graph_for(ds, "order")
    order.add((CE["order/o0"], RDF.type, CE["Order"]))
    return ds


def _quads(ds: Dataset) -> set:
    """(s, p, o, graph_iri) tuples over the populated ce: named graphs."""
    out = set()
    for ctx in ds.contexts():
        iri = str(ctx.identifier)
        for s, p, o in ctx:
            out.add((s, p, o, iri))
    return out


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------

def test_flexo_backend_satisfies_protocol(tmp_path):
    assert isinstance(FlexoBackend(store_root=tmp_path), StoreBackend)


def test_flexo_backend_name(tmp_path):
    assert FlexoBackend(store_root=tmp_path).name == "flexo"


def test_flexo_backend_describe(tmp_path):
    assert "Flexo MMS" in FlexoBackend(store_root=tmp_path).describe()


def test_flexo_record_uri_maps_layer(tmp_path):
    backend = FlexoBackend(store_root=tmp_path)
    assert backend.record_uri("evidence") == URIRef(G_EVIDENCE)
    assert backend.record_uri("not-a-layer") is None


def test_flexo_emit_service_node(tmp_path):
    backend = FlexoBackend(store_root=tmp_path)
    g = Graph()
    org = CE["org/host"]
    service = backend.emit_service_node(g, org)
    assert service is not None
    assert (service, CE["operatedBy"], org) in g


# ---------------------------------------------------------------------------
# probe (preflight)
# ---------------------------------------------------------------------------

def test_probe_available_with_fake_store(tmp_path):
    """Fake-store mode is always reachable and offline."""
    FlexoBackend(store_root=tmp_path).probe()  # does not raise


def test_probe_fails_fast_on_unreachable_endpoint():
    """Real-endpoint mode fails fast (BackendUnavailable, no hang)."""
    # RFC 5737 TEST-NET-1 address on a closed port; the 3s timeout bounds it.
    backend = FlexoBackend(endpoint="http://192.0.2.1:9/flexo")
    start = time.monotonic()
    with pytest.raises(BackendUnavailable, match="unreachable"):
        backend.probe()
    assert time.monotonic() - start < 10  # bounded, does not hang


def test_endpoint_mode_has_no_fake_store():
    backend = FlexoBackend(endpoint="http://192.0.2.1:9/flexo")
    assert backend.store is None


# ---------------------------------------------------------------------------
# persist / load round-trip
# ---------------------------------------------------------------------------

def test_persist_load_round_trip(dataset, tmp_path):
    """persist() then load() yields identical quads across named graphs."""
    backend = FlexoBackend(store_root=tmp_path)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        counts = backend.persist(dataset, tmp_path)

    assert counts.get(G_ONTOLOGY) == 5
    assert counts.get(G_EVIDENCE) == 3
    assert counts.get(G_ORDER) == 1

    reloaded = backend.load()
    assert _quads(reloaded) == _quads(dataset)


def test_persist_creates_one_version(dataset, tmp_path):
    backend = FlexoBackend(store_root=tmp_path)
    backend.persist(dataset, tmp_path)
    assert len(backend.store.history(backend.ref)) == 1


# ---------------------------------------------------------------------------
# Append-only versioning / immutability
# ---------------------------------------------------------------------------

def test_append_only_retains_prior_version(dataset, tmp_path):
    """A second persist with different content yields a new version while
    the earlier version remains resolvable unchanged."""
    backend = FlexoBackend(store_root=tmp_path)
    backend.persist(dataset, tmp_path)
    v1 = backend.store.history(backend.ref)[-1]
    v1_quads = _quads(backend.load(v1))

    # Mutate the dataset (add evidence) and persist again.
    ev = graph_for(dataset, "evidence")
    ev.add((CE["evidence/e99"], RDF.type, CE["Evidence"]))
    backend.persist(dataset, tmp_path)

    history = backend.store.history(backend.ref)
    assert len(history) == 2
    v2 = history[-1]
    assert v1 != v2

    # Earlier version is unchanged (immutability).
    assert _quads(backend.load(v1)) == v1_quads
    # Latest reflects the new content.
    assert (CE["evidence/e99"], RDF.type, CE["Evidence"], G_EVIDENCE) in _quads(
        backend.load(v2)
    )
    assert _quads(backend.load()) == _quads(backend.load(v2))  # None -> latest


def test_store_commit_is_append_only(tmp_path):
    """FakeFlexoStore.commit appends; earlier version resolves unchanged."""
    store = FakeFlexoStore(tmp_path)
    g1 = Graph(identifier=URIRef(G_ONTOLOGY))
    g1.add((CE["a"], RDF.type, CE["Control"]))
    v1 = store.commit("main", {G_ONTOLOGY: g1})

    g2 = Graph(identifier=URIRef(G_ONTOLOGY))
    g2.add((CE["a"], RDF.type, CE["Control"]))
    g2.add((CE["b"], RDF.type, CE["Control"]))
    v2 = store.commit("main", {G_ONTOLOGY: g2})

    assert store.history("main") == [v1, v2]
    assert v1 != v2
    assert len(store.resolve("main", v1)[G_ONTOLOGY]) == 1
    assert len(store.resolve("main", v2)[G_ONTOLOGY]) == 2
    assert len(store.resolve("main")[G_ONTOLOGY]) == 2  # latest


def test_resolve_unknown_version_raises(tmp_path):
    store = FakeFlexoStore(tmp_path)
    g = Graph(identifier=URIRef(G_ONTOLOGY))
    g.add((CE["a"], RDF.type, CE["Control"]))
    store.commit("main", {G_ONTOLOGY: g})
    with pytest.raises(KeyError):
        store.resolve("main", "deadbeef")


# ---------------------------------------------------------------------------
# Content addressing determinism
# ---------------------------------------------------------------------------

def test_content_addressing_is_deterministic(tmp_path):
    """Identical content commits to the same version id across two stores."""
    def _make(root):
        store = FakeFlexoStore(root)
        g = Graph(identifier=URIRef(G_ONTOLOGY))
        for i in range(4):
            g.add((CE[f"s{i}"], RDF.type, CE["Control"]))
        return store.commit("main", {G_ONTOLOGY: g})

    v_a = _make(tmp_path / "a")
    v_b = _make(tmp_path / "b")
    assert v_a == v_b


def test_graph_hash_stable_for_identical_graph(tmp_path):
    """Same triples -> same per-graph content hash regardless of insert order."""
    store = FakeFlexoStore(tmp_path)

    g1 = Graph(identifier=URIRef(G_ONTOLOGY))
    g1.add((CE["a"], RDF.type, CE["Control"]))
    g1.add((CE["b"], RDF.type, CE["Control"]))
    store.commit("refA", {G_ONTOLOGY: g1})

    g2 = Graph(identifier=URIRef(G_ONTOLOGY))
    g2.add((CE["b"], RDF.type, CE["Control"]))  # reversed insertion order
    g2.add((CE["a"], RDF.type, CE["Control"]))
    store.commit("refB", {G_ONTOLOGY: g2})

    assert store.graph_hash("refA", G_ONTOLOGY) == store.graph_hash("refB", G_ONTOLOGY)
