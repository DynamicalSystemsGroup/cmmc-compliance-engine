# documents/ — the compiled SSP (and the Traceability Matrix view)

**Purpose.** Compile the **System Security Plan** deterministically from the
graph — "the BOM *is* the SSP." Also renders the Traceability Matrix
(Document 2) as a byte-stable view. No hand-maintained SSP; rebuild it.

**Port from ADCS.** `documents/design_description.py` (DDVS-001 compiler) is
the direct template — a pure function of (union quads, input bytes) that
produces byte-identical Markdown, with a `--check` drift gate. Retarget the
section headings from an engineering design description to the SSP structure
required by `reference/guides/cmmc-0-to-100-guide.md` §6:

| DDVS-001 section | → SSP section |
| --- | --- |
| Front matter (baseline commit, dataset SHA-256) | System identification + baseline |
| Requirement derivation | Framework applicability (800-171 → CMMC → IL5/ITAR) |
| Requirement allocation | CUI boundary + control→resource responsibility |
| Verification Cross-Reference Matrix | **The 110-control implementation table** (Document 2) |
| Requirement detail (evidence + attestation + GSN) | Per-control: implementation, evidence hashes, MET/gap, POA&M |
| Colophon (per-graph triple counts, fingerprint) | Evidence-package manifest + dataset fingerprint |

**Why this matters for the assessor.** The compiler gives you a traditional,
always-current PDF/Markdown SSP *for free* — defusing the "C3PAO rejects a
novel BOM format" risk (requirements doc §14). Lead with the familiar
document; the content-addressed graph backs it.

**Files.** `ssp.py` — the compiler (Phase 0). **Inputs:** the persisted
dataset (`output/rtm.trig` analogue). **Outputs:** `output/ssp.md`; the
`--check` drift gate keeps the SSP from silently diverging from evidence.
