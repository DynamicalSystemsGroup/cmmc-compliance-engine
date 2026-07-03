# Compliance Engine

**A build system where "provision the cloud environment" and "prove it's compliant" are the same action.**

> **New here? Start with the [plain-English tour](docs/v1/README.md).** It explains
> the whole system from scratch — no compliance or cloud background needed — and
> ends with a runnable demo. Every acronym below is defined in the
> [glossary](docs/v1/06-glossary.md).

Defense contractors that handle CUI (Controlled Unclassified Information) must
meet **CMMC Level 2** — a checklist of 110 security controls from NIST SP 800-171 —
and submit a **System Security Plan (SSP)** describing how each control is met.
Today that proof is assembled by hand: screenshots, spreadsheets, binders.

This engine flips it: every environment is _born_ from a signed, policy-checked
infrastructure **Order** and ships with a re-executable proof of compliance — a
signed **BOM** (Bill of Materials) that doubles as the SSP. Compliance is not
gathered after the fact by inspecting an existing setup; it is a **byproduct of
provisioning**.

> **Design of record.** Where any document under [`reference/`](reference/)
> conflicts with this repo, this repo wins. (`reference/` is background research —
> safe to skip entirely.)

---

## Two systems, one chain

The work splits into two decoupled systems that hand a single file over the fence:

```
   CONTRACT (the solicitation text, its Q&A, and standard DoD clauses)
        │
        ▼
┌───────────────────────────┐   separate upstream tool
│   ORDER COMPILER          │   order-compiler/
│   contract → obligations  │   • AI drafts the obligations, a human attests them
│   → controls → modules    │   • proves PLANNING COVERAGE (Gate 1)
│   → a signed ORDER file   │   • emits a proof-carrying Order
└───────────────────────────┘
        │  Order file (signed, hash-referenced)
        ▼
┌───────────────────────────┐   the engine (this repo's runtime)
│   THE FACTORY             │   pipeline/ + evidence/ oracles/ traceability/
│   fetch modules by hash   │   • terraform plan → policy-as-code check
│   → apply (BUILDS it)     │   • terraform apply → live compliance tests
│   → live tests → BOM      │   • proves FULFILLMENT (Gate 2), human attests
│   → sign → registry       │   • BOM = SSP, stored write-once
└───────────────────────────┘
        │  BOM hash
        ▼
   AUDITOR (a certified CMMC assessor, "C3PAO") re-executes the Order →
   rebuilds the identical environment → re-runs checks → confirms the
   fingerprints match. Proof by reproduction, not a folder of screenshots.
```

**The Order Compiler is a separate tool** (a chosen seam): its only output is a
signed Order file. The Factory consumes Orders and doesn't care how they were
made.

## The two coverage gates (why the mapping is _real_)

The engine's honesty rests on refusing to proceed unless traceability is complete
in both directions:

- **Gate 1 — Planning coverage** (Order Compiler, before anything is built):
  every control the contract requires has ≥1 module _claiming_ it, every module
  traces back to a required control, and no claim lacks a testable method.
  Missing coverage ⇒ **the Order won't emit.**
- **Gate 2 — Proven fulfillment** (Factory, at BOM close): a control is MET only
  when its claim's evidence _passes_ and a human _attests_. The BOM's
  control-mapping is audited against the Order's required-control set. A claim
  whose live test fails ⇒ **the BOM is invalid.**

Planning-coverage is a promise; proven-fulfillment is the receipt. Both are
content-addressed and bidirectionally audited.

## The founding principle

> **Evidence does not verify requirements; evidence supports a human judgment
> that requirements are satisfied.**

Machines provision, gather evidence, and run automated checks (`earl:automatic`).
Only a human — the Affirming Official — attests a control MET (`earl:manual`),
carrying the legal (False Claims Act) accountability. The same line governs the
one judgment the Compiler makes: **AI drafts the contract's obligations; a
Compliance Officer attests them.**

The traceability substrate (content-addressed hashing, human attestation,
bidirectional audit, deterministic document compilation over an RDF named-graph
store) is reused from a prior internal project, `ADCS-lifecycle-demo` — a
satellite requirements-traceability engine. **You do not need that repo to
understand or run this one**; this repo adds the front half it lacked: the
Order → Factory → BOM provisioning loop.

## The two authored documents

- **Control Requirements Catalog** ([`reference/control-catalog.md`](reference/control-catalog.md),
  machine form [`ontology/cmmc-edit.ttl`](ontology/cmmc-edit.ttl)): the 110
  controls with their weights. The "law."
- **Traceability Matrix** ([`reference/traceability-matrix.md`](reference/traceability-matrix.md)):
  control → resource → evidence → status. Generated per build as the BOM's
  control-mapping and rendered inside the SSP.

## Repo map

| Path                                 | What it is                                                                                                                                              |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`cli.py`](cli.py)                   | **The operator entry point** — `demo` drives the whole chain; each stage is a subcommand                                                                |
| [`order-compiler/`](order-compiler/) | Separate upstream tool: contract → obligations → controls → modules → signed Order (Gate 1)                                                             |
| [`pipeline/`](pipeline/)             | The Factory: executes an Order — fetch by hash → plan → policy check → evidence → checks; also the write-once registry (local today; GCS/Azure planned) |
| [`evidence/`](evidence/)             | SHA-256 hashing + evidence binding + the evidence generators (fixture-backed today)                                                                     |
| [`oracles/`](oracles/)               | The automated pass/fail/can't-tell checks — one criterion per machine-checkable control                                                                 |
| [`traceability/`](traceability/)     | Human attestation (Gate 2), bidirectional audit, SPRS score + POA&M legality                                                                            |
| [`structural/`](structural/)         | Data: which Terraform module claims which control (`tier1.ttl`)                                                                                         |
| [`ontology/`](ontology/)             | The control catalog as RDF vocabulary + SHACL validation shapes                                                                                         |
| [`documents/`](documents/)           | Deterministic **SSP compiler** (renders the BOM's facts as the government document)                                                                     |
| [`terraform/`](terraform/)           | Real Tier-1 infrastructure-as-code modules (driven at plan level, mock providers)                                                                       |
| [`fixtures/`](fixtures/nv012/)       | The NV012 demo's mock evidence, in three scenario variants                                                                                              |
| [`docs/`](docs/)                     | Documentation — see routing below                                                                                                                       |
| [`reference/`](reference/)           | Background research (guides, standards, requirements) — **safe to skip entirely**                                                                       |

## Documentation — where to start, by audience

| You are…                      | Read                                                                                     |
| ----------------------------- | ---------------------------------------------------------------------------------------- |
| **New to the project**        | [`docs/v1/`](docs/v1/README.md) — the plain-English tour (start at 00, ~45 min)          |
| **An operator** (just run it) | ["Run the NV012 demo"](#run-the-nv012-demo) below                                        |
| **A developer**               | [`ARCHITECTURE.md`](ARCHITECTURE.md) then [`docs/AS-BUILT.md`](docs/AS-BUILT.md)         |
| **An assessor / auditor**     | [`docs/AUDITOR-GUIDE.md`](docs/AUDITOR-GUIDE.md) — how to re-verify a delivered BOM      |
| **Checking what's proven**    | [`docs/ACCEPTANCE.md`](docs/ACCEPTANCE.md) — the acceptance sign-off and scenario matrix |

## Status

**Runnable, end to end, on mock data.** The full chain is implemented and tested
(293 tests): ontology build, Order compilation + Gate 1, real Terraform
plan-level provisioning (mock providers), evidence/oracles, Gate 2 attestation,
audit + SPRS, BOM + registry, and the deterministic SSP. Live `terraform apply`,
real evidence collectors, cryptographic signing (Sigstore), and cloud registry
backends (GCS/Azure) are Phase II — see [`ROADMAP.md`](ROADMAP.md).

## Run the NV012 demo

NV012 is an example DoD SBIR contract (SBIR = the DoD's small-business R&D
program) that the demo ships with as its input. One command drives the whole
chain — compile the Order → run the Factory (real `terraform plan`, mock
providers) → attest → audit + SPRS → BOM → SSP.

**Prereqs.** `uv sync`. No cloud account or credentials are needed: the demo
defaults to a mock provisioner (`--backend fake`) and fixture-backed evidence.
`terraform` (≥ 1.4) is optional and only used with `--backend terraform`.

**The three scenarios** (each is one copy-pasteable command):

```bash
# 1. Happy path — full chain, writes the BOM + audit + SSP + registry, exit 0
uv run python cli.py demo --evidence-set all-covered --auto

# 2. Coverage gap — Gate 1 REFUSES before anything is built, exit 2
uv run python cli.py demo --evidence-set gap --auto

# 3. Contradiction — completes, but the audit flags the human-over-machine conflict, exit 0
uv run python cli.py demo --evidence-set contradiction --auto
```

What to expect:

- **`all-covered`** → compiles the Order (22 required controls), runs all six
  stages, attests every required control MET, and prints
  `SPRS: score=110 status=Final valid_submission=True`, then
  `Proven vs attested: 4 MET-by-machine / 18 MET-by-human-only` and
  `Contradictions (attested MET over failed machine check): 0`. SPRS is scored
  over the **Order's required-control set** (the controls this environment is
  responsible for), all MET → full score. Exit **0**.
- **`gap`** → Gate 1 refuses and names the missing 5-point control
  (`AC.L2-3.1.12` has no claiming module): `Gate 1 REFUSED — Order NOT emitted.`
  The Factory never runs and **no artifacts are written**. Exit **2**.
- **`contradiction`** → the same happy chain, but a human attests MET over a
  failing machine oracle (MFA off), so the audit reports
  `Contradictions (attested MET over failed machine check): 1`. The BOM is
  still written — the conflict is surfaced, not swallowed. Exit **0**.

Artifacts written under `--output-dir` (default `output/`):

| Artifact                  | What it is                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------- |
| `bom.json`                | the BOM — control-mapping + attestations + artifact hashes (canonical JSON)                 |
| `ssp.md`                  | the SSP — the human-readable government document with the 110-row traceability matrix       |
| `audit.md` / `audit.json` | bidirectional audit + SPRS score / POA&M-legality + the contradiction list                  |
| `registry/`               | write-once, content-addressed object store + two-level index (`contract → BOM → artifacts`) |
| `engine.trig`             | the full `<ce:*>` named-graph dataset for the run                                           |
| `run_state.json`          | the finalized `PipelineState` summary (per-stage results)                                   |

Exit codes: **0** success · **1** Factory safety-valve halt (a pre-apply policy
check failed, e.g. a non-US region — nothing was applied) · **2** Gate-1 refusal
or bad arguments.

> **This run is NON-EVIDENTIARY.** Evidence is fixture-backed and the environment
> is provisioned by a mock provider, so every artifact carries
> `evidentiary_status: "mock"` and the emitted BOM is **not a submittable SSP** —
> it demonstrates the mechanism, not a real assessment.

Other subcommands run the stages individually against `--output-dir`:
`compile-order`, `run-factory`, `attest`, `audit`, `bom`, `ssp`. Run
`uv run python cli.py --help` for the full list.

_Design material, not legal advice. Verify all CMMC/ITAR interpretations with the contracting officer, C3PAO, and counsel._
