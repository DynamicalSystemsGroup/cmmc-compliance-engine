# reference/

Research and source material, consolidated here when `compliance-engine`
became the single source of truth. **This is background, not the design of
record** — where any file here conflicts with the top-level design docs, the
top-level docs win.

## The two authored documents (the engine's inputs)
- [`control-catalog.md`](control-catalog.md) — **Document 1**, the Control
  Requirements Catalog (the "law"): all 110 controls with weights + POA&M
  rules. Machine form: [`../ontology/cmmc-edit.ttl`](../ontology/cmmc-edit.ttl).
- [`traceability-matrix.md`](traceability-matrix.md) — **Document 2**, the
  Tier 1 Traceability Matrix (the "evidence"). Currently authored by hand
  (`Status: Planned`); the end state generates it from live evidence via the
  SSP compiler in [`../documents/`](../documents/).
- [`document-binding.md`](document-binding.md) — the Rosetta: how each column
  of Documents 1 & 2 binds to a fact in the graph the engine builds.

## Concepts (design rationale)
- [`concepts/adcs-to-cmmc-compliance-engine.md`](concepts/adcs-to-cmmc-compliance-engine.md)
  — the synthesis: why this engine = the ADCS traceability substrate + the two
  documents. **Read this to understand the design.**
- [`concepts/cmmc-as-a-CAT.md`](concepts/cmmc-as-a-CAT.md) — the origin vision
  (Order/Factory/BOM). Superseded on IPFS; kept for provenance.

## Requirements
- [`requirements/cats-compliance-engine-requirements.md`](requirements/cats-compliance-engine-requirements.md)
  — the platform spec (SHA-256, GitHub gates, Sigstore, tiers). The prior
  design-of-record; now realized by this repo.
- [`requirements/compliance-evidence-requirements.md`](requirements/compliance-evidence-requirements.md)
  — control→evidence mapping research (NIST/DoD/ITAR sourced).

## Guides
- [`guides/cmmc-0-to-100-guide.md`](guides/) — CMMC L2 roadmap · bidding plan ·
  Tier 1 5-day buildout · Google CUI enclave setup.

## Contracts & standards
- [`contracts/`](contracts/) — NV011 / NV012 solicitations + NV012 Q&A (the
  business driver: three DoD SBIRs requiring CMMC L2 / IL5 / ITAR).
- [`standards/`](standards/) — NIST SP 800-171 Rev 2 (the 110 controls).
