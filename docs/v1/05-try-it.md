# 05 — Try it yourself

Copy-paste this and watch the whole thing run on your machine. No cloud account,
no credentials, nothing to sign up for. Unfamiliar words → [glossary](06-glossary.md).

The output shown below is the **real** output captured from this repo — yours will
match (the run is deterministic).

---

## Prerequisites

```bash
# 1. Install dependencies (uses uv — https://docs.astral.sh/uv/)
uv sync

# 2. terraform is OPTIONAL. The demo's default provisioner is a built-in fake
#    (no cloud, no terraform needed). You only need terraform installed if you
#    want to exercise the real plan-level path.
```

Everything below writes artifacts into a directory you choose with
`--output-dir`. We'll use `/tmp/...` so nothing clutters the repo.

---

## Scenario A — the happy path (all-covered)

Everything the contract requires is covered and signed off.

```bash
uv run python cli.py demo --evidence-set all-covered --auto --output-dir /tmp/nv012-all
```

Real output (trimmed — the per-control MET lines are omitted):

```
[demo] evidence-set=all-covered
[1/6 compile-order] Order cdad6fb17f7c… (22 controls)
[Preflight] Probing backends...
  Provision: FakeProvisionBackend (compliant, deterministic, no terraform)
  Storage:   Local filesystem (rdflib Dataset, persisted as output/engine.ttl + .trig)
  Provision probe: PASS
  Storage probe:   PASS
[2/6 run-factory] 7 evidence nodes, 6 oracle outcomes
  … 22 controls attested MET …
[3/6 attest] 22 control(s) attested (Gate 2)
[4/6 audit]
SPRS: score=110 status=Final valid_submission=True
Proven vs attested: 4 MET-by-machine / 18 MET-by-human-only
Contradictions (attested MET over failed machine check): 0
[5/6 bom] 4483673449ac… evidentiary_status=mock -> /tmp/nv012-all/bom.json
[6/6 ssp]
SSP: wrote /tmp/nv012-all/ssp.md (NON-EVIDENTIARY banner: present)
```

Exit code **0**. **What it proves:** the full chain runs end to end —
[Gate 1](06-glossary.md#gate-1) passes, the [Factory](06-glossary.md#factory)
completes, all 22 required controls are attested MET, the score is
**110 / Final**, and a **[BOM](06-glossary.md#bom) + [SSP](06-glossary.md#ssp)** are
produced. Note the honest lines: only **4** of the 22 are machine-proven; the rest
rest on human attestation. And the BOM/SSP are stamped **mock** (see "what's real
vs pretend" below).

## Scenario B — a coverage gap (gap)

Now require a control that nothing implements. This is the safety check.

```bash
uv run python cli.py demo --evidence-set gap --auto --output-dir /tmp/nv012-gap
```

Real output:

```
[demo] evidence-set=gap
[1/6 compile-order] Gate 1 REFUSED — Order NOT emitted. Missing module for required control(s): AC.L2-3.1.12
```

Exit code **2**. **What it proves:** [Gate 1](06-glossary.md#gate-1) is a real gate.
A required control (`AC.L2-3.1.12`) has no implementing [module](06-glossary.md#module),
so the compiler **refuses to emit an Order and names the missing control**. The
Factory never runs — **nothing downstream is built**. You cannot accidentally ship
a plan with a silent hole in it.

## Scenario C — a contradiction (contradiction)

Everything runs, but one machine check **fails** and a human signs it MET anyway
without a written override.

```bash
uv run python cli.py demo --evidence-set contradiction --auto --output-dir /tmp/nv012-con
```

Real output (tail):

```
[4/6 audit]
SPRS: score=110 status=Final valid_submission=True
Proven vs attested: 3 MET-by-machine / 19 MET-by-human-only
Contradictions (attested MET over failed machine check): 1
[5/6 bom] 047ac45af023… evidentiary_status=mock -> /tmp/nv012-con/bom.json
[6/6 ssp]
SSP: wrote /tmp/nv012-con/ssp.md (NON-EVIDENTIARY banner: present)
```

Exit code **0**. **What it proves:** the run *completes* and even scores 110/Final —
**but the audit flags 1 contradiction** and the SSP footer says
`contradictions: 1`. This is the design point from [04](04-the-proof.md#1-the-audit):
the score does not silently absorb the conflict; the MET-over-failed-oracle is
surfaced for a human to review. A 110 here is **not** clean.

---

## What lands in your output directory

After Scenario A, `ls /tmp/nv012-all/` shows:

| File / dir       | What it is |
| ---------------- | ---------- |
| `bom.json`       | The [BOM](06-glossary.md#bom) — the machine-readable proof file (control → resource → evidence hash → status → attester). |
| `ssp.md`         | The [SSP](06-glossary.md#ssp) — the human-readable government document with the 110-row [traceability matrix](06-glossary.md#vcrm) + the NON-EVIDENTIARY banner. |
| `audit.md`       | The [audit](06-glossary.md#audit) report (forward/backward pass, contradiction list, proven-vs-attested split) in Markdown. |
| `audit.json`     | The same audit, machine-readable. |
| `engine.trig`    | The full knowledge graph ([RDF](06-glossary.md#rdf) named graphs) the whole run was built from — the single source of truth. |
| `registry/`      | The content-addressed store: `objects/` (every artifact keyed by its hash) + `index.json` (contract → BOM → artifact hashes). |
| `run_state.json` | A snapshot of the Factory's internal state (order hash, evidence hashes, oracle outcomes, resources) for debugging. |

---

## What's real vs pretend right now (be honest)

This is **Phase I**. It runs a real software spine end to end, but:

- **Evidence is mock / fixture-backed.** The "config exports" are canned JSON files
  under `fixtures/nv012/`, not live pulls from a real Google/GCP tenant. That's why
  every BOM and SSP carries the **NON-EVIDENTIARY** mark and is **not submittable**.
- **Terraform is plan-level only.** The environment is *planned* with **mock
  providers** — no cloud is contacted and **nothing is deployed** (`apply`). The
  default demo provisioner is an in-memory fake.
- **Only ~7 evidence artifacts / ~6 machine checks; 4 of 22 machine-proven.** The
  rest of the required controls are human-attested (or CSP-inherited). And the
  score covers only the **22 required**, not all **110** modeled — **88** are out of
  NV012's scope.
- **Deferred:** cryptographic signing ([Sigstore](06-glossary.md#sigstore)),
  [IL5](06-glossary.md#il4--il5), live `terraform apply` + live compliance tests,
  and actual SPRS/PIEE submission. The engine *computes* the score; a human still
  submits it.

None of this is hidden by the tool — the banner, the "mock" stamp, and the
proven-vs-attested split are all there to keep you honest.

---

### In one sentence

Three commands show the whole system: **all-covered** → 110/Final + a mock BOM/SSP,
**gap** → Gate 1 refuses and names the hole, **contradiction** → it completes but
loudly flags the human-over-machine conflict — and everything it produces is marked
NON-EVIDENTIARY because the evidence is still pretend.

### Next: the [glossary](06-glossary.md) · or back to the [docs index](README.md)
