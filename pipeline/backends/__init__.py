"""Pluggable persistence backends for the compliance-engine Dataset.

The runtime always builds the Dataset locally (in-memory rdflib). The
backend's job is to *persist* that dataset — writing to disk for the
local case. Remote backends (Flexo MMS, Fuseki) from the ADCS demo are
intentionally omitted here; the write-once tier registry is the
production persistence target.

The choice of backend is transparent to every other stage: SPARQL
queries, SHACL validation, and the audit module all continue to run
against the local Dataset. Backend integration is the persistence step
at the end of the pipeline.

Selection: `--backend=local` on the CLI (default: local).
"""

from pipeline.backends.base import StoreBackend, get_backend  # noqa: F401
