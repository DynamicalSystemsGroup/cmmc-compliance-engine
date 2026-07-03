"""Build the assembled cmmc.ttl from cmmc-edit.ttl + vendored imports.

Adapted from ADCS-lifecycle-demo/scripts/build_ontology.py. This is the
Python-only, OFFLINE, DETERMINISTIC build path. It produces:

  - ontology/cmmc.ttl              the assembled artifact
  - ontology/cmmc_manifest.json    build provenance (input hashes + counts)

Build steps:

  1. Load cmmc-edit.ttl (the 110-control edit ontology).
  2. Validate that every upstream term cmmc-edit references actually exists in
     the corresponding vendored ontology (cmmc:/ce:/sysml: are locally-defined,
     never dangling). cmmc-edit references no upstream terms today, so this is a
     well-formedness guard for future edits.
  3. Re-serialize the edit graph as cmmc.ttl with a deterministic build header.
  4. Enforce the triple-count budget (parsimony gate).
  5. Emit the manifest: artifact SHA-256, vendored-import hashes + triple counts,
     axiom counts, and the reproducible build time.

The SysMLv2 term-map / OSLC / equivalence-axiom machinery from the ADCS build is
DROPPED (cmmc: subclasses sysml: directly; no CSV term map, no OSLC imports).

Determinism: NO datetime.now() anywhere on the build path. The build time comes
from SOURCE_DATE_EPOCH (Reproducible Builds standard) or a fixed default, so the
same inputs always yield byte-identical cmmc.ttl + manifest. The build never
touches the network; refresh the vendored set via scripts/fetch_imports.py.

Usage:
    uv run python -m scripts.build_ontology
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from rdflib import Graph, URIRef
from rdflib.namespace import RDFS

ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_DIR = ROOT / "data" / "ontology"
IMPORTS_DIR = ONTOLOGY_DIR / "imports"

EDIT_FILE = ONTOLOGY_DIR / "cmmc-edit.ttl"
SHAPES_FILE = ONTOLOGY_DIR / "cmmc_shapes.ttl"
OUT_FILE = ONTOLOGY_DIR / "cmmc.ttl"
MANIFEST_FILE = ONTOLOGY_DIR / "cmmc_manifest.json"

# Local (this-engine) namespaces: never validated against a vendored import.
CMMC_NS = "http://dynamicalsystems.group/ontology/cmmc#"
CE_NS = "http://dynamicalsystems.group/compliance-engine/"
SYSML_NS = "https://www.omg.org/spec/SysML/2.0/"

# Deterministic default build time (used when SOURCE_DATE_EPOCH is unset). A
# fixed constant — NOT datetime.now() — so builds are reproducible offline.
DEFAULT_BUILD_TIME = "2026-07-02T00:00:00Z"

# Parsimony gate. cmmc: is an integration ontology: it encodes Document 1's 110
# controls + a thin TBox, and should not grow unbounded. The gate fails the
# build if the assembled artifact exceeds the budget. Bumping it is deliberate,
# not silent drift — update the rationale when you do.
#
# History:
#   R4: built cmmc.ttl is 1057 triples (110 controls x ~9 props +
#     14 families + TBox). Budget set to 1200 (~143 headroom, ~13%) — room for
#     small TBox additions without inviting scope creep.
TRIPLE_BUDGET = 1200
TRIPLE_BUDGET_RATIONALE = (
    "Integration-ontology parsimony gate. The built cmmc.ttl encodes the 110 "
    "NIST SP 800-171 Rev.2 controls (Document 1) plus a thin TBox and 14 "
    "families (~1057 triples). Budget 1200 leaves a modest margin for small "
    "TBox additions; raising it requires updating this rationale."
)


def _reproducible_build_time() -> str:
    """Return a build_time stable across machines for the same source state.

    SOURCE_DATE_EPOCH (Reproducible Builds standard) wins; otherwise the fixed
    DEFAULT_BUILD_TIME constant. Never datetime.now() — the build must be
    byte-reproducible offline.
    """
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch and epoch.isdigit():
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
    return DEFAULT_BUILD_TIME


@dataclass(frozen=True)
class VendoredImport:
    name: str
    iri: str
    filename: str
    namespace: str  # namespace prefix of terms we expect to find here


# OSLC RM/QM are DROPPED (not used by the compliance engine). SysMLv2's full OMG
# rendering is not vendored — cmmc: subclasses the local sysml: namespace.
VENDORED: list[VendoredImport] = [
    VendoredImport("PROV-O",  "http://www.w3.org/ns/prov-o",       "prov-o.ttl",  "http://www.w3.org/ns/prov#"),
    VendoredImport("EARL",    "http://www.w3.org/ns/earl#",        "earl.ttl",    "http://www.w3.org/ns/earl#"),
    VendoredImport("OntoGSN", "https://w3id.org/OntoGSN/ontology", "ontogsn.ttl", "https://w3id.org/OntoGSN/ontology#"),
    VendoredImport("P-PLAN",  "http://purl.org/net/p-plan",        "p-plan.ttl",  "http://purl.org/net/p-plan#"),
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _referenced_terms(edit_graph: Graph, namespace: str) -> set[str]:
    """Local-name set of terms in `namespace` referenced by edit_graph.

    Excludes the namespace IRI itself (empty local name)."""
    referenced: set[str] = set()
    for s, p, o in edit_graph:
        for term in (s, p, o):
            if isinstance(term, URIRef) and str(term).startswith(namespace):
                local = str(term)[len(namespace):]
                if local:
                    referenced.add(local)
    return referenced


def _defined_terms(import_graph: Graph, namespace: str) -> set[str]:
    """Local-name set of terms in `namespace` defined (appear as a subject)."""
    defined: set[str] = set()
    for s in import_graph.subjects(unique=True):
        if isinstance(s, URIRef) and str(s).startswith(namespace):
            defined.add(str(s)[len(namespace):])
    return defined


def _validate_references(edit_graph: Graph) -> tuple[dict[str, dict], list[str]]:
    """For each vendored import, confirm every referenced term is defined.

    Returns (per-import-info, error-list). cmmc:/ce:/sysml: are local and never
    checked. per-import-info: {name: {iri, namespace, filename, sha256,
    total_triples, referenced_terms, referenced_count, missing_terms}}.
    """
    info: dict[str, dict] = {}
    errors: list[str] = []
    for vi in VENDORED:
        path = IMPORTS_DIR / vi.filename
        if not path.exists():
            errors.append(
                f"Vendored import missing: {vi.filename}. "
                f"Run `uv run python -m scripts.fetch_imports`."
            )
            continue
        g = Graph()
        g.parse(path, format="turtle")
        referenced = _referenced_terms(edit_graph, vi.namespace)
        defined = _defined_terms(g, vi.namespace)
        missing = [m for m in sorted(referenced - defined) if m]
        if missing:
            errors.extend(
                f"{vi.name}: cmmc-edit references {vi.namespace}{m} "
                f"which is not defined in vendored {vi.filename}"
                for m in missing
            )
        info[vi.name] = {
            "iri": vi.iri,
            "namespace": vi.namespace,
            "filename": vi.filename,
            "sha256": _sha256(path),
            "total_triples": len(g),
            "referenced_terms": sorted(referenced),
            "referenced_count": len(referenced),
            "missing_terms": missing,
        }
    return info, errors


def _count_subclass_axioms(g: Graph) -> int:
    return sum(1 for _ in g.triples((None, RDFS.subClassOf, None)))


def _count_subproperty_axioms(g: Graph) -> int:
    return sum(1 for _ in g.triples((None, RDFS.subPropertyOf, None)))


def build(
    *,
    edit_file: Path = EDIT_FILE,
    shapes_file: Path = SHAPES_FILE,
    out_file: Path = OUT_FILE,
    manifest_file: Path = MANIFEST_FILE,
    triple_budget: int | None = None,
    verbose: bool = True,
) -> int:
    """Assemble cmmc.ttl + manifest. Returns 0 on success, 1 on any gate failure.

    Fully parametrized so tests can build into a tmp dir and simulate an
    over-budget failure without touching the committed ontology.
    """
    edit_file = Path(edit_file)
    out_file = Path(out_file)
    manifest_file = Path(manifest_file)
    budget = TRIPLE_BUDGET if triple_budget is None else triple_budget

    def log(msg: str) -> None:
        if verbose:
            print(msg)

    log(f"Building ontology from {edit_file.name} ...")
    edit_graph = Graph()
    edit_graph.parse(edit_file, format="turtle")
    log(f"  {edit_file.name}: {len(edit_graph)} triples")

    # Step 2: validate referenced upstream terms exist in their vendored import.
    import_info, ref_errors = _validate_references(edit_graph)
    if ref_errors:
        for e in ref_errors:
            print(f"  ERROR  {e}", file=sys.stderr)
        return 1

    # Step 3: assemble the out graph (edit graph, re-bound prefixes).
    out_graph = Graph()
    out_graph += edit_graph
    for prefix, ns in edit_graph.namespaces():
        out_graph.bind(prefix, ns)

    total_triples = len(out_graph)

    # Step 4: parsimony gate BEFORE writing, so an over-budget build emits nothing.
    if total_triples > budget:
        print(
            f"  ERROR  cmmc.ttl exceeds triple budget: {total_triples} > {budget}",
            file=sys.stderr,
        )
        print(f"         Rationale: {TRIPLE_BUDGET_RATIONALE}", file=sys.stderr)
        print(
            "         To raise the budget, bump TRIPLE_BUDGET in "
            "scripts/build_ontology.py and update the rationale.",
            file=sys.stderr,
        )
        return 1
    headroom = budget - total_triples

    build_time = _reproducible_build_time()
    header = (
        "# =============================================================================\n"
        "# AUTO-GENERATED ARTIFACT — DO NOT EDIT DIRECTLY\n"
        "#\n"
        f"# Built {build_time} by scripts/build_ontology.py from:\n"
        "#   - ontology/cmmc-edit.ttl\n"
        "#   - ontology/imports/*.ttl (reference validation only)\n"
        "#\n"
        "# To make changes: edit cmmc-edit.ttl and re-run "
        "`uv run python -m scripts.build_ontology`.\n"
        "# =============================================================================\n\n"
    )
    body_bytes = out_graph.serialize(format="turtle").encode("utf-8")
    final_bytes = header.encode("utf-8") + body_bytes

    out_file.parent.mkdir(parents=True, exist_ok=True)
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(final_bytes)
    artifact_sha = _sha256_bytes(final_bytes)
    log(
        f"  Wrote {out_file.name} ({total_triples} triples, "
        f"sha256={artifact_sha[:12]}...)"
    )
    log(f"  Parsimony: {total_triples}/{budget} triples ({headroom} headroom)")

    # Step 5: manifest (deterministic — sorted keys, no wall-clock).
    manifest = {
        "build_time": build_time,
        "artifact": {
            "path": f"data/ontology/{out_file.name}",
            "sha256": artifact_sha,
            "total_triples": total_triples,
            "subclass_axioms": _count_subclass_axioms(out_graph),
            "subproperty_axioms": _count_subproperty_axioms(out_graph),
        },
        "triple_budget": {
            "value": budget,
            "rationale": TRIPLE_BUDGET_RATIONALE,
            "headroom": headroom,
        },
        "edit_source": {
            "path": f"data/ontology/{edit_file.name}",
            "sha256": _sha256(edit_file),
        },
        "shapes_source": {
            "path": f"data/ontology/{Path(shapes_file).name}",
            "sha256": _sha256(shapes_file),
        },
        "imports": import_info,
        "offline": True,
        "notes": "Python assembly only; offline + reproducible (no network, no wall-clock).",
    }
    manifest_file.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    log(f"  Wrote {manifest_file.name}")
    return 0


# --- Typer CLI --------------------------------------------------------------
try:
    import typer

    app = typer.Typer(add_completion=False, help="Build the assembled cmmc.ttl + manifest.")

    @app.command()
    def main() -> None:
        """Assemble ontology/cmmc.ttl + ontology/cmmc_manifest.json (offline)."""
        raise typer.Exit(build())

except ImportError:  # pragma: no cover - typer is a declared dependency
    app = None


if __name__ == "__main__":
    if app is not None:
        app()
    else:  # pragma: no cover
        sys.exit(build())
