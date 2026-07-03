"""Named-graph dataset layout + TriG round-trip.

Adapted from the ADCS test_named_graphs.py. The ADCS version drove a full
`run_pipeline()`; here (substrate spine only) we populate the eight named
graphs directly and assert the quadstore surface behaves:

  - create_dataset() returns a Dataset with default_union=True.
  - There are exactly eight named graphs, using cmmc:/ce: (not adcs:/rtm:).
  - Writes via graph_for() route into the correct named graph.
  - A TriG export re-parses into identical per-graph triple counts.
  - The union Turtle export is a flat single graph (back-compat).
  - SPARQL without GRAPH clauses sees across all graphs (default_union).
  - graph_for()/query_named_graph() reject unknown layer names.
"""

from __future__ import annotations

import warnings

import pytest
from rdflib import Dataset, Graph, URIRef
from rdflib.namespace import RDF

from ontology.prefixes import (
    CE,
    NAMED_GRAPHS,
    G_ATTESTATIONS,
    G_AUDIT,
    G_EVIDENCE,
    G_ONTOLOGY,
    G_ORDER,
    G_PLAN,
    G_PLAN_EXECUTION,
    G_STRUCTURAL,
)
from pipeline.dataset import (
    create_dataset,
    export_trig,
    export_union_turtle,
    graph_for,
    load_into,
    query_named_graph,
    triples_by_graph,
)


# Distinct per-layer triple counts so a round-trip that shuffles graphs
# would be detected (each layer has a unique population size).
_LAYER_COUNTS = {
    "ontology": 7,
    "plan": 6,
    "structural": 5,
    "order": 4,
    "evidence": 8,
    "attestations": 3,
    "plan_execution": 9,
    "audit": 2,
}


def _populate(ds: Dataset) -> None:
    """Add a distinct number of triples to each of the eight named graphs."""
    for layer, n in _LAYER_COUNTS.items():
        g = graph_for(ds, layer)
        for i in range(n):
            g.add((CE[f"{layer}/s{i}"], RDF.type, CE[f"{layer}/Thing"]))


@pytest.fixture()
def populated() -> Dataset:
    ds = create_dataset()
    _populate(ds)
    return ds


def test_create_dataset_is_default_union():
    ds = create_dataset()
    assert isinstance(ds, Dataset)
    assert ds.default_union is True


def test_named_graphs_has_exactly_eight_layers():
    assert len(NAMED_GRAPHS) == 8
    assert set(NAMED_GRAPHS) == {
        "ontology", "plan", "structural", "order",
        "evidence", "attestations", "plan_execution", "audit",
    }


def test_named_graph_iris_use_ce_namespace():
    for iri in NAMED_GRAPHS.values():
        assert iri.startswith(str(CE))
    # The ADCS instance namespaces must be gone.
    for iri in NAMED_GRAPHS.values():
        assert "adcs-demo" not in iri
        assert "example.org" not in iri


def test_writes_route_to_correct_named_graph(populated):
    counts = triples_by_graph(populated)
    for layer, n in _LAYER_COUNTS.items():
        iri = NAMED_GRAPHS[layer]
        assert counts.get(iri) == n, (
            f"layer {layer} expected {n} triples in {iri}, got {counts.get(iri)}"
        )


def test_eight_graph_dataset_round_trips_trig(populated, tmp_path):
    """Export the 8-graph dataset as TriG, re-parse, assert identical
    per-graph counts."""
    before = _per_graph_quad_counts(populated)
    assert len(before) == 8, f"expected 8 populated graphs, got {len(before)}"

    trig = tmp_path / "engine.trig"
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        export_trig(populated, trig)

    reloaded = Dataset()
    reloaded.parse(trig, format="trig")
    after = _per_graph_quad_counts(reloaded)

    assert after == before, (
        f"TriG round-trip changed per-graph counts:\nbefore={before}\nafter={after}"
    )


def test_union_turtle_export_is_flat_single_graph(populated, tmp_path):
    """export_union_turtle collapses all named graphs into one flat graph
    whose size equals the sum of every layer."""
    ttl = tmp_path / "engine.ttl"
    export_union_turtle(populated, ttl)
    g = Graph()
    g.parse(ttl, format="turtle")
    assert len(g) == sum(_LAYER_COUNTS.values())


def test_default_union_sparql_sees_all_graphs(populated):
    """A GRAPH-clause-free SELECT counts triples across every layer."""
    rows = list(populated.query(
        "SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }"
    ))
    assert int(rows[0][0]) == sum(_LAYER_COUNTS.values())


def test_query_named_graph_scopes_to_one_layer(populated):
    rows = list(query_named_graph(
        populated, "evidence",
        "SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }",
    ))
    assert int(rows[0][0]) == _LAYER_COUNTS["evidence"]


def test_graph_for_rejects_unknown_layer(populated):
    with pytest.raises(KeyError, match="Unknown named-graph layer"):
        graph_for(populated, "nonexistent")


def test_query_named_graph_rejects_unknown_layer(populated):
    with pytest.raises(KeyError, match="Unknown named-graph layer"):
        query_named_graph(populated, "nonexistent", "SELECT * WHERE { ?s ?p ?o }")


def test_load_into_parses_ttl_into_layer(tmp_path):
    """load_into() parses a Turtle file into the requested named graph."""
    src = tmp_path / "src.ttl"
    src.write_text(
        "@prefix ce: <http://dynamicalsystems.group/compliance-engine/> .\n"
        "ce:a a ce:B . ce:c a ce:B .\n"
    )
    ds = create_dataset()
    added = load_into(ds, "structural", src)
    assert added == 2
    assert triples_by_graph(ds).get(G_STRUCTURAL) == 2


def test_all_eight_graph_constants_are_distinct():
    iris = {
        G_ONTOLOGY, G_PLAN, G_STRUCTURAL, G_ORDER,
        G_EVIDENCE, G_ATTESTATIONS, G_PLAN_EXECUTION, G_AUDIT,
    }
    assert len(iris) == 8


def _per_graph_quad_counts(ds: Dataset) -> dict[str, int]:
    """{graph_iri: quad_count} restricted to the eight planned graphs."""
    named = {URIRef(iri) for iri in NAMED_GRAPHS.values()}
    counts: dict[str, int] = {}
    for _, _, _, c in ds.quads((None, None, None, None)):
        if c in named:
            counts[str(c)] = counts.get(str(c), 0) + 1
    return counts
