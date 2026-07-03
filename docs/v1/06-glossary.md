# 06 — Glossary (plain English, A–Z)

Every term a newcomer hits, in one to three plain sentences. "In this repo:"
points at where the thing lives in the code.

---

### ADCS
A prior internal project (`ADCS-lifecycle-demo`, a *satellite* requirements-
traceability engine) whose substrate — content-addressed hashing, human
attestation, bidirectional audit, deterministic document compilation over
[RDF](#rdf) named graphs — this repo reuses. Mentioned only as lineage: **you do
not need it to understand or run this repo.**

### Affirming Official
The human who formally signs off that a control is satisfied. Only their
[attestation](#attestation) — not a machine check — makes a control officially
[MET](#met--not-met). In this repo: the `Affirming Official` role on each attestation.

### apply (terraform)
The Terraform step that **actually creates** cloud resources. This engine does
**not** run apply in Phase I — it stops at [plan](#plan-terraform). See [Terraform](#terraform).

### Attestation
A recorded human judgment that a control is MET (or NOT MET), with two written
reasons: *adequacy* (is the implementation good enough?) and *sufficiency* (is the
evidence enough to conclude MET?). In this repo: `traceability/attestation.py`,
emitted as `ce:attests` + `ce:hasOutcome`.

### Audit
A two-direction check that the paper trail is unbroken: every required control has
a module + sign-off ([forward](#gate-2)), and every sign-off points at the right
control's evidence (backward). It also produces the [contradiction](#contradiction-r13)
list and the proven-vs-attested split. In this repo: `traceability/audit.py`.

### BOM
**Bill of Materials** — the single machine-readable proof file (`bom.json`). For each
required control it lists resource → evidence hash → oracle outcome → attestation
outcome → status, plus who signed. It gets its own [SHA-256](#sha-256) and is stored
[write-once](#registry). If any input is mock, the whole BOM is stamped `"mock"`. In
this repo: `traceability/bom.py`.

### C3PAO
A **Certified Third-Party Assessment Organization** — the outside auditor accredited
to assess CMMC compliance. The whole "[proof by reproduction](04-the-proof.md#5-proof-by-reproduction)"
design exists so a C3PAO can re-verify a delivery without trusting screenshots. See
[docs/AUDITOR-GUIDE.md](../AUDITOR-GUIDE.md).

### cantTell
An [oracle](#oracle) outcome meaning "the machine could not decide" (e.g. the metric
it needed was absent). It is honest uncertainty — never silently treated as a pass.

### CMMC Level 2
**Cybersecurity Maturity Model Certification, Level 2** — the U.S. Department of
Defense program that requires contractors handling sensitive information to prove
they implement the 110 [NIST SP 800-171](#nist-sp-800-171) controls.

### content-addressing
Storing a file under an address that **is** a hash of its own bytes, so identical
content always gets the same address and any change produces a different address.
That makes tampering instantly detectable. See [SHA-256](#sha-256) and [registry](#registry).

### contradiction
A red flag: a control a human marked **MET** while its machine [oracle](#oracle)
**failed** (or was absent), with **no written override justification**. The system
lists these separately from the score so an unexplained human-over-machine call can't
hide. In this repo: the contradiction dimension in `traceability/audit.py` (referred
to as rule "R13" in internal code comments).

### control
One specific security requirement (e.g. "enforce multi-factor authentication"). CMMC
Level 2 has 110. In this repo: `cmmc:Control` in `ontology/cmmc-edit.ttl`.

### control weight
How many points a control is worth in the [SPRS](#sprs) score: **1, 3, or 5** by how
much it matters. Not-MET controls subtract their weight from 110.

### COP
**Contract Obligation Profile** — the structured statement of what a specific contract
requires (its [obligations](#obligation)), which the [Order Compiler](#order-compiler)
turns into a required-control set. In this repo: `fixtures/nv012/cop_draft.ttl`.

### CUI
**Controlled Unclassified Information** — sensitive-but-unclassified government
information that contractors must protect. The reason CMMC exists.

### DFARS
**Defense Federal Acquisition Regulation Supplement** — the contract clauses that
make protecting [CUI](#cui) (and hitting CMMC) a legal obligation for DoD contractors.

### EARL
**Evaluation and Report Language** — a small standard vocabulary for recording
test/assessment outcomes (`passed`, `failed`, `cantTell`, …). This engine reuses it
for both oracle results and attestation outcomes instead of inventing its own.

### evidence
An artifact that **addresses** a control — a config export, a policy check result, a
plan-time terraform check. Evidence *supports* a decision; it never by itself makes a
control MET (only [attestation](#attestation) does). In this repo: `<ce:evidence>` +
`evidence/`.

### Factory
The stage that executes a compiled [Order](#order): provision (plan) → policy-check →
collect evidence → run oracles, recording every step. In this repo: `pipeline/runner.py`.
See [02 — The Factory](02-the-factory.md).

### fingerprint
Everyday word for a [hash](#hash) — a short string that uniquely stands in for a
file's exact bytes.

### Gate 1
The **planning** gate, inside the [Order Compiler](#order-compiler): the Order is only
emitted if every required control has an implementing [module](#module) and every
module traces back to a required control. A gap → refusal, and the missing control is
named. In this repo: `order-compiler/gate1.py`.

### Gate 2
The **evidence/attestation** gate, at audit time: does every control actually have
evidence and a human sign-off? The two gates share report structure but ask different
questions. In this repo: the forward/backward checks in `traceability/audit.py`.

### hash
A fixed-length fingerprint computed from a file's bytes; the same bytes always give
the same hash, and any change gives a different one. This engine uses [SHA-256](#sha-256).

### HCL
**HashiCorp Configuration Language** — the language [Terraform](#terraform) files are
written in. In this repo: `terraform/tier1/*.tf` describes the CUI enclave.

### IL4 / IL5
**Impact Level 4 / 5** — DoD cloud security tiers for increasingly sensitive data.
NV012 targets **IL4**; IL5 support is deferred.

### ITAR
**International Traffic in Arms Regulations** — U.S. export-control rules; relevant here
as a data-residency requirement (keep certain data on U.S. soil / U.S.-person access).

### MET / NOT MET
The official status of a control after a human [attestation](#attestation): MET =
satisfied, NOT MET = not satisfied. `N/A` and [cantTell](#canttell) also exist; an
un-attested control is `PLANNED` (a gap).

### mock provider
A stand-in for a real [Terraform](#terraform) cloud provider used by `terraform test`,
so a [plan](#plan-terraform) (and a fake apply) runs with **no credentials and no
cloud**. It's how "provision = prove" works offline.

### module
A buildout resource that implements one or more controls (e.g. the KMS keyring, the
IAM group, the log sink). In this repo: `structural/tier1.ttl` maps each module to the
controls it satisfies.

### named graph
A labeled sub-section of the [RDF](#rdf) knowledge graph (e.g. `<ce:evidence>`,
`<ce:attestations>`), so different kinds of facts stay separated but queryable
together. In this repo: the eight layers in `ontology/prefixes.py`.

### NIST SP 800-171
The U.S. standards document listing the 110 security requirements ("controls") for
protecting [CUI](#cui) in non-federal systems. CMMC Level 2 is essentially "prove you
do these 110."

### NON-EVIDENTIARY
The banner/stamp a [BOM](#bom) or [SSP](#ssp) carries when the run is mock /
fixture-backed. It means: this is a demonstration artifact, **not** a submittable
compliance document. The [SSP](#ssp) cannot omit it when mock inputs are present.

### NV012
The example DoD [SBIR](#sbir) contract the demo ships with — the input the whole
chain runs on. Its Order requires 22 of the 110 controls. In this repo:
`fixtures/nv012/`.

### obligation
One requirement pulled from a contract's [COP](#cop) (a data type, a deliverable, an
overlay). The [Order Compiler](#order-compiler) resolves obligations into the set of
required controls.

### oracle
An automated check that compares a piece of evidence against a control's machine
criterion and returns `passed` / `failed` / [cantTell](#canttell). Oracles are
*supporting* signal only — they never make a control MET. In this repo: `oracles/`.

### Order
The compiled, hash-referenced work order the [Factory](#factory) executes: the required
controls, the modules that cover them, and content hashes tying it together. Emitted
only if [Gate 1](#gate-1) passes. In this repo: `order-compiler/compiler.py`.

### Order Compiler
The front half of the system: it turns a contract's [COP](#cop) into a required-control
set, runs [Gate 1](#gate-1), and emits an [Order](#order) — or refuses with a named gap.
See [01 — The Order](01-the-order.md).

### plan (terraform)
The Terraform step that computes **what would change** without creating anything. This
engine runs plan (with [mock providers](#mock-provider)) to prove the environment is
described correctly — it never runs [apply](#apply-terraform).

### POA&M
**Plan of Action and Milestones** — a dated fix-it plan for a not-yet-MET control. Only
**1-point** controls may be deferred this way; deferring a 3/5-point control (or one of
six excluded 1-pointers) makes the submission automatically invalid.

### PROV
**PROV-O** — a W3C standard vocabulary for recording provenance: who did what, when,
and from what. This engine uses it to record how every activity and artifact was
produced.

### provisioning
Creating/configuring the actual cloud resources (identities, keys, policies, logging).
Here it's done at [plan](#plan-terraform) level only — described and checked, not
deployed.

### RDF
**Resource Description Framework** — a way of storing facts as a graph of
subject–predicate–object statements, so everything (controls, evidence, attestations)
lives in one queryable knowledge graph. In this repo: the `.trig`/`.ttl` files and
`pipeline/dataset.py`.

### registry
A content-addressed, **write-once** store where a file's [SHA-256](#sha-256) hash IS its
address (`objects/<hash>`), plus a small index resolving `contract → BOM → artifact
hashes`. Tampering changes the address, so it's caught immediately. In this repo:
`pipeline/registry.py`.

### SBIR
Small Business Innovation Research — the DoD's small-business R&D contracting
program. The demo's example contract ([NV012](#nv012)) is an SBIR topic; its
solicitation text and Q&A are where the obligations come from.

### SHA-256
The specific cryptographic [hash](#hash) function this engine uses (a 64-character hex
fingerprint). It's the backbone of [content-addressing](#content-addressing): the hash
of an artifact is both its identity and its tamper check. In this repo: `evidence/hashing.py`.

### SHACL
**Shapes Constraint Language** — rules that check an [RDF](#rdf) graph is well-formed
(e.g. "every evidence node must have a content hash"). The engine's structural guardrails.

### Sigstore
An ecosystem for cryptographically **signing** artifacts. Deferred in Phase I — today
artifacts are referenced by bare [SHA-256](#sha-256) (`registry://<hash>`), which is a
content reference, **not** a signature.

### SPRS
**Supplier Performance Risk System** — the DoD scoreboard. Score = `110 − (weights of
not-MET controls)`; 110 = Final, 88–109 = Conditional (with a [POA&M](#poam)), below 88
= Ineligible. Computed over the **Order's required set**, not all 110. In this repo:
`traceability/sprs.py`.

### SSP
**System Security Plan** — the required human-readable government document. Here it's
compiled deterministically from the graph, includes the 110-row [VCRM](#vcrm), is
byte-stable, and structurally cannot hide its [NON-EVIDENTIARY](#non-evidentiary)
banner. In this repo: `documents/ssp.py`.

### Terraform
An infrastructure-as-code tool: you describe cloud resources in [HCL](#hcl) files and it
figures out how to create them. This engine uses it at [plan](#plan-terraform) level with
[mock providers](#mock-provider). In this repo: `terraform/tier1/` + `pipeline/provision/`.

### Tier 1
The name for this build's target environment: an IL4 CUI enclave (Google Workspace
Enterprise Plus + GCP Assured Workloads). In this repo: `structural/tier1.ttl` +
`terraform/tier1/`.

### VCRM
**Verification Cross-Reference Matrix** — the traceability matrix at the heart of the
[SSP](#ssp): one row per control with implementation, responsible party, evidence
location, evidence hash, status, gap notes, and POA&M reference. Also called Document 2.

### verification vs validation
**Verification** = an automated check whose result is fully determined (an
[oracle](#oracle), a hash re-check). **Validation** = a human judgment
([attestation](#attestation)). Evidence informs validation; only validation makes a
control [MET](#met--not-met). Getting this line right is the whole point of the system.

---

### Back to the [docs index](README.md) · or re-read [04 — The proof](04-the-proof.md)
