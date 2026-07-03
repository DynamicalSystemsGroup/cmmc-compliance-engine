"""RDF namespace constants for the compliance engine.

The `cmmc:` ontology is an integration / application ontology — a thin
layer assembled from established upstream vocabularies. Custom `cmmc:`
terms are limited to convenience subclasses (a control IS a SysMLv2
requirement), content-addressing properties, and SHACL targets. Every
epistemic concept comes from an imported standard.

Upstream vocabularies (ported unchanged from the ADCS lifecycle demo):
- PROV-O      : provenance spine
- SysMLv2     : structural model + requirements (local namespace)
- EARL        : assertion pattern + outcome lattice + mode
- OntoGSN     : Goal / Strategy / Solution / Assumption / Justification
- P-PLAN      : declarative pipeline plan + step ordering
- OSLC RM/QM  : tool-interop aliases for requirement satisfaction / validation
- SHACL       : closure rules (well-formedness invariants)
- Dublin Core : metadata

Two instance namespaces are local to this engine:
- ``cmmc:`` — the Control Requirements Catalog TBox/ABox (the "law" layer)
- ``ce:``   — compliance-engine instance data (orders, evidence, BOMs,
              plan-execution activities, named-graph IRIs)
"""

from rdflib import Namespace

# Layer 1 — W3C / IETF standards
PROV = Namespace("http://www.w3.org/ns/prov#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
EARL = Namespace("http://www.w3.org/ns/earl#")
SH = Namespace("http://www.w3.org/ns/shacl#")

# Layer 1 — Community ontologies
GSN = Namespace("https://w3id.org/OntoGSN/ontology#")
P_PLAN = Namespace("http://purl.org/net/p-plan#")
OSLC_RM = Namespace("http://open-services.net/ns/rm#")
OSLC_QM = Namespace("http://open-services.net/ns/qm#")

# Layer 2 — SysMLv2
# Local namespace used throughout instance data; a control (cmmc:Control)
# subclasses sysml:RequirementDefinition so all ADCS traceability queries
# work unchanged.
SYSML = Namespace("https://www.omg.org/spec/SysML/2.0/")

# Layer 3 — Local integration vocabulary + instance namespaces
# CMMC is the Control Requirements Catalog namespace (retargeted from rtm:).
# CE is the compliance-engine instance namespace (retargeted from adcs:).
CMMC = Namespace("http://dynamicalsystems.group/ontology/cmmc#")
CE = Namespace("http://dynamicalsystems.group/compliance-engine/")

# Named-graph IRIs (Flexo-compatible quadstore layout). Eight graphs, one
# per lifecycle layer. Retargeted from the ADCS eight-graph layout: the
# ADCS `context` graph is replaced by `order` (the signed Order is this
# engine's input), and every IRI moves under the ce: namespace.
G_ONTOLOGY = "http://dynamicalsystems.group/compliance-engine/ontology"
G_PLAN = "http://dynamicalsystems.group/compliance-engine/plan"
G_STRUCTURAL = "http://dynamicalsystems.group/compliance-engine/structural"
G_ORDER = "http://dynamicalsystems.group/compliance-engine/order"
G_EVIDENCE = "http://dynamicalsystems.group/compliance-engine/evidence"
G_ATTESTATIONS = "http://dynamicalsystems.group/compliance-engine/attestations"
G_PLAN_EXECUTION = "http://dynamicalsystems.group/compliance-engine/plan-execution"
G_AUDIT = "http://dynamicalsystems.group/compliance-engine/audit"

NAMED_GRAPHS = {
    "ontology": G_ONTOLOGY,
    "plan": G_PLAN,
    "structural": G_STRUCTURAL,
    "order": G_ORDER,
    "evidence": G_EVIDENCE,
    "attestations": G_ATTESTATIONS,
    "plan_execution": G_PLAN_EXECUTION,
    "audit": G_AUDIT,
}

# All prefixes for graph binding. Note: rtm:/adcs:/sat: are intentionally
# absent — they were retargeted to cmmc:/ce: for this engine.
PREFIXES = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "prov": str(PROV),
    "dcterms": str(DCTERMS),
    "earl": str(EARL),
    "sh": str(SH),
    "gsn": str(GSN),
    "p-plan": str(P_PLAN),
    "oslc_rm": str(OSLC_RM),
    "oslc_qm": str(OSLC_QM),
    "sysml": str(SYSML),
    "cmmc": str(CMMC),
    "ce": str(CE),
}


def bind_prefixes(graph):
    """Bind all project prefixes to an rdflib Graph or Dataset."""
    for prefix, uri in PREFIXES.items():
        graph.bind(prefix, uri)
    return graph
