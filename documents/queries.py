"""SSP / Traceability-Matrix SPARQL.

Thin extension over the shared `traceability/queries.py` (U9): re-exports the
shared query runner + attestation/evidence views, and adds the control-catalog,
implementation, evidence-location, and POA&M views the VCRM (Document 2) needs.
All queries assume the union view of the Dataset (`default_union=True`) and are
run through `query_to_dicts`, which returns sorted-friendly lists of dicts.
"""

from __future__ import annotations

# Re-export the shared runner + the attestation/evidence detail views so the
# compiler imports everything document-related from one place.
from traceability.queries import (  # noqa: F401
    ALL_ATTESTATIONS,
    ATTESTATION_DETAIL,
    CONTROL_OUTCOMES,
    EVIDENCE_DETAIL,
    UNATTESTED_CONTROLS,
    query_to_dicts,
)

# All 110 controls with the catalog columns the VCRM reads.
CONTROLS_FULL = """
SELECT ?controlId ?text ?family ?weight ?poamEligible WHERE {
    ?control a cmmc:Control ;
             cmmc:controlId ?controlId ;
             cmmc:text ?text ;
             cmmc:weight ?weight .
    OPTIONAL { ?control cmmc:family ?family }
    OPTIONAL { ?control cmmc:poamEligible ?poamEligible }
}
ORDER BY ?controlId
"""

# control -> implementing module label + its verification method (structural
# tier1.ttl satisfy allocation, via the direct cmmc:controlsSatisfied edge).
CONTROL_IMPLEMENTATION = """
SELECT ?controlId ?moduleLabel ?verification WHERE {
    ?module cmmc:controlsSatisfied ?control .
    ?control cmmc:controlId ?controlId .
    OPTIONAL { ?module rdfs:label ?moduleLabel }
    OPTIONAL { ?module cmmc:verificationMethod ?verification }
}
ORDER BY ?controlId ?moduleLabel
"""

# control -> addressing evidence: content hash, location, evidentiary status.
EVIDENCE_LOCATION = """
SELECT ?controlId ?ev ?contentHash ?status ?sourceFile ?documentRef WHERE {
    ?ev a ce:Evidence ;
        ce:addresses ?control ;
        ce:contentHash ?contentHash .
    ?control cmmc:controlId ?controlId .
    OPTIONAL { ?ev ce:evidentiaryStatus ?status }
    OPTIONAL { ?ev ce:sourceFile ?sourceFile }
    OPTIONAL { ?ev ce:documentRef ?documentRef }
}
ORDER BY ?controlId ?contentHash
"""

# control -> POA&M reference (cmmc:poamItem), when one is committed.
POAM_REFS = """
SELECT ?controlId ?poamItem WHERE {
    ?control a cmmc:Control ;
             cmmc:controlId ?controlId ;
             cmmc:poamItem ?poamItem .
}
ORDER BY ?controlId ?poamItem
"""

# Every evidentiary-status literal present in the dataset (drives the R12 gate).
EVIDENTIARY_STATUSES = """
SELECT DISTINCT ?status WHERE { ?ev ce:evidentiaryStatus ?status }
ORDER BY ?status
"""

# Maximum prov:generatedAtTime across the dataset — the data-derived doc date.
MAX_GENERATED_AT = """
SELECT (MAX(?t) AS ?maxTime) WHERE { ?s prov:generatedAtTime ?t }
"""

# All content hashes committed in <ce:evidence> — the BOM-hook fallback.
EVIDENCE_HASHES = """
SELECT DISTINCT ?contentHash WHERE { ?ev a ce:Evidence ; ce:contentHash ?contentHash }
ORDER BY ?contentHash
"""
