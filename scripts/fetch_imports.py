"""Refresh upstream ontologies into ontology/imports/ (NETWORK, opt-in).

Adapted from ADCS-lifecycle-demo/scripts/fetch_imports.py. Re-runnable /
idempotent: each upstream is fetched at its published IRI, parsed via rdflib,
and re-serialized as Turtle into ontology/imports/<name>.ttl.

The vendored copies are committed so the build (scripts/build_ontology.py) stays
OFFLINE and reproducible. This script exists only to REFRESH that vendored set —
**the build never calls it**, and default test runs never hit the network (the
network test is guarded by @pytest.mark.network + a RUN_NETWORK_TESTS gate).

OSLC RM/QM are DROPPED relative to ADCS (unused by the compliance engine).

Usage:
    uv run python -m scripts.fetch_imports
"""

from __future__ import annotations

import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from rdflib import Graph

IMPORTS_DIR = Path(__file__).resolve().parent.parent / "ontology" / "imports"


@dataclass(frozen=True)
class Source:
    name: str
    iri: str
    fetch_url: str
    format: str          # rdflib parser format: "turtle", "xml", ...
    output: str          # filename under ontology/imports/


SOURCES: list[Source] = [
    Source(
        name="PROV-O",
        iri="http://www.w3.org/ns/prov-o",
        fetch_url="https://www.w3.org/ns/prov-o.ttl",
        format="turtle",
        output="prov-o.ttl",
    ),
    Source(
        name="EARL",
        iri="http://www.w3.org/ns/earl#",
        fetch_url="https://www.w3.org/ns/earl.rdf",
        format="xml",
        output="earl.ttl",
    ),
    Source(
        name="OntoGSN",
        iri="https://w3id.org/OntoGSN/ontology",
        fetch_url="https://raw.githubusercontent.com/fortiss/OntoGSN/main/serializations/ontogsn.ttl",
        format="turtle",
        output="ontogsn.ttl",
    ),
    Source(
        name="P-PLAN",
        iri="http://purl.org/net/p-plan",
        fetch_url="https://vocab.linkeddata.es/p-plan/",
        format="xml",
        output="p-plan.ttl",
    ),
]


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "text/turtle, application/rdf+xml;q=0.9, */*;q=0.5",
            "User-Agent": "compliance-engine/fetch_imports.py",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:  # noqa: S310 (opt-in network)
        return response.read()


def fetch_one(source: Source) -> tuple[Source, int]:
    """Fetch and re-serialize one upstream ontology. Returns (source, triples)."""
    raw = _fetch(source.fetch_url)
    g = Graph()
    g.parse(data=raw, format=source.format, publicID=source.iri)
    out_path = IMPORTS_DIR / source.output
    g.serialize(destination=out_path, format="turtle")
    return source, len(g)


def fetch_all() -> int:
    """Refresh every vendored import. Returns the failure count."""
    IMPORTS_DIR.mkdir(parents=True, exist_ok=True)
    failures = 0
    for src in SOURCES:
        try:
            _, triples = fetch_one(src)
            print(f"  OK   {src.name:12} {triples:>5} triples -> {src.output}")
        except Exception as exc:  # pragma: no cover - network path
            print(f"  FAIL {src.name:12} {exc}", file=sys.stderr)
            failures += 1
    return failures


# --- Typer CLI --------------------------------------------------------------
try:
    import typer

    app = typer.Typer(add_completion=False, help="Refresh vendored imports (network).")

    @app.command()
    def main() -> None:
        """Fetch upstream ontologies into ontology/imports/ (opt-in network)."""
        print(f"Fetching upstream ontologies into ontology/imports/ ...")
        raise typer.Exit(1 if fetch_all() else 0)

except ImportError:  # pragma: no cover
    app = None


if __name__ == "__main__":
    if app is not None:
        app()
    else:  # pragma: no cover
        sys.exit(1 if fetch_all() else 0)
