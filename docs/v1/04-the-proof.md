# 04 — The proof: what the machine produces and how to read it

You've seen the environment get built and checked (→ [02 — The Factory](02-the-factory.md)).
Now: **what does the machine hand you at the end, and how do you read it without
being fooled?**

Every unfamiliar word links to the [glossary](06-glossary.md). The numbers below
are the **real** output of the NV012 demo (→ [05 — Try it](05-try-it.md)), not
made-up examples.

There are four outputs. Two are checks (the **audit** and the **SPRS score**),
two are documents (the **BOM** and the **SSP**). Then there's the idea that ties
them together: **proof by reproduction**.

---

## 1. The audit — "does the chain hold together?"

Think of a paper trail. The audit walks it **both directions** and reports
whether it's unbroken:

- **Forward:** every required control has something implementing it **and** a
  human sign-off. (Demo: `Forward PASS (22 checked, 0 failures)`.)
- **Backward:** every sign-off actually points at evidence for the *right*
  control — no sign-off floating free. (Demo: `Backward PASS (5 checked, 0 failures)`.)

Then it adds two things you must not skip:

- **The contradiction list (R13).** A red-flag list. It catches any control a
  human marked **MET** while the machine check for that same control **failed** —
  *unless* the human wrote down a justification for overruling the machine. An
  unexplained override is exactly the kind of thing an assessor needs to see, so
  the system surfaces it separately instead of hiding it inside the score.
- **The proven-vs-attested split.** One honest line: how many MET controls the
  machine actually *proved* versus how many rest on **human judgment alone**.
  Demo (all-covered): **`4 MET-by-machine / 18 MET-by-human-only`**.

> ⚠ **The single most important honesty point in this whole system:** a score of
> "110 / Final" with **`contradictions: 1`** is **not** a clean result. The score
> and the contradiction list are *separate on purpose*. Always read both.

## 2. The SPRS score — and what "110" really means

[SPRS](06-glossary.md#sprs) is the government's compliance scoreboard. The rule is
simple:

```
score = 110 − (sum of the weights of the controls that are NOT MET)
```

Each control is worth **1, 3, or 5 points** by how much it matters. Land on:

- **110 → Final** (everything in scope is MET)
- **88–109 → Conditional** (you may proceed with a [POA&M](06-glossary.md#poam) — a
  dated fix-it plan)
- **below 88 → Ineligible**

The demo prints `SPRS: score=110 status=Final valid_submission=True`.

**Here is the honesty that matters most.** The score is computed over **the
Order's required set — about 22 controls for NV012 — not all 110.** So:

> **"110 / Final" means "all 22 controls this contract requires were marked MET."
> It does NOT mean "all 110 controls were tested."**

And even within those 22, only a handful are *machine-proven*. The full picture:

```
110  controls modeled in the catalog (the whole CMMC Level 2 rulebook)
 22  required by the NV012 Order          ← the score is computed over THESE
  7  evidence artifacts / ~6 machine oracle checks produced by the Factory
  4  of the 22 end up machine-PROVEN (oracle passed AND a human attested)
 18  of the 22 rest on human attestation (documentary / inherited)
 88  controls entirely out of NV012's scope
```

**POA&M legality (a hard rule).** Only **1-point** controls may be deferred onto a
fix-it plan. Put a **3- or 5-point** control (or one of six specifically excluded
1-pointers) on a POA&M and the submission is **automatically invalid** — the code
flags `valid_submission=False` **regardless of the number**. A high score with an
illegal deferral is not a pass.

## 3. The BOM — the single machine-readable proof file

The **BOM** ([Bill of Materials](06-glossary.md#bom), written to `bom.json`) is the
one file that pins the whole run. For **each required control** it records a row:

```
control_id        AC.L2-3.1.1
resource_ids      ["CUI_Users_Group"]                         ← what provisioned it
evidence_hashes   ["4bba2d0adcbb…", "6c69bdddaea3…"]          ← the evidence, by hash
oracle_outcome    passed                                       ← what the machine found
attestation_outcome passed                                     ← what the human signed
status            MET                                          ← driven by the HUMAN
```

Plus the list of who attested each control. Two properties make it trustworthy:

- **It inherits the weakest mark.** If *any* input is mock/fixture-backed, the whole
  BOM is stamped `evidentiary_status: "mock"`. You can't launder pretend evidence
  into a real-looking BOM. (Demo BOM: `evidentiary_status=mock`.)
- **It is content-addressed and stored write-once.** The BOM gets its own
  [SHA-256](06-glossary.md#sha-256) hash (demo: `4483673449ac…`). It's saved in a
  **[registry](06-glossary.md#registry)** — a store where **the file's hash IS its
  address**. Change one byte and the address no longer matches, so tampering is
  instantly detectable. Write-once means an address can never be silently
  overwritten.

The registry keeps a tiny two-level index so anyone can look it up later:
`contract "NV012" → latest BOM hash → the list of every artifact hash` (demo: 19
artifact hashes under the BOM).

## 4. The SSP — the same facts as the government document

The **[SSP](06-glossary.md#ssp)** (`ssp.md`) is the required human-readable
artifact: a System Security Plan whose centerpiece is the **110-row traceability
matrix** ([VCRM](06-glossary.md#vcrm)) — one row per control listing implementation,
responsible party, evidence location, evidence hash, status, gaps, and POA&M
reference.

It is **not** hand-written. It's compiled straight from the same data as the BOM,
so it can't disagree with the graph. Two guarantees:

- **Byte-stable:** identical inputs produce a byte-for-byte identical document, and
  `documents.ssp build --check` re-compiles and fails if the delivered file has
  drifted from the data.
- **It cannot hide the mock warning.** When the run is fixture-backed, the SSP
  *structurally* emits a big **NON-EVIDENTIARY** banner at the top and stamps it in
  the footer — there is no switch to turn it off. The demo SSP opens with:
  *"⚠ NON-EVIDENTIARY — fixture-derived / auto-attested … not a submittable SSP."*
  Its footer reads: `SPRS summary: score 110 (Final); 4 MET-by-machine / 18
  MET-by-human-only; contradictions: 0.`

## 5. Proof by reproduction — why this beats a folder of screenshots

The core claim of the whole engine: **an auditor doesn't have to trust you.** Given
the delivered BOM, a [C3PAO](06-glossary.md#c3pao) assessor can:

1. **Resolve** every artifact by its hash from the registry,
2. **Re-hash** each one and confirm the fingerprint still matches (tamper check),
3. **Re-run** the plan-level checks and confirm the control→resource→evidence
   mapping and the oracle outcomes match what the BOM records.

If every fingerprint matches, the delivery is exactly what was signed. The
step-by-step version is in **[docs/AUDITOR-GUIDE.md](../AUDITOR-GUIDE.md)**.

---

### In one sentence

The machine produces an **audit** (is the chain unbroken, and where does the human
overrule the machine?), an **SPRS score** (computed over the ~22 required controls,
not all 110), a content-addressed **BOM** (the tamper-evident proof file, stamped
"mock" here), and a byte-stable **SSP** (the government document, which can't hide
its NON-EVIDENTIARY banner) — all re-checkable by hash.

### Next: [05 — Try it yourself](05-try-it.md)
