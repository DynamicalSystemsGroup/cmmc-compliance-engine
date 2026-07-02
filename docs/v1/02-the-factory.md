# 02 · The Factory — how the environment gets built and checked

*Part of the v1 plain-English tour. Previous: [01 · The Order](01-the-order.md).*

---

## Why this exists (the one big idea)

Most compliance works like this: someone sets up a system, then *later* an auditor
walks around with a checklist asking "is this secure? is that encrypted?" and
writes down what they're told.

This system flips it. **The environment is *built* from a signed plan, and the act
of building it *is* the proof.** There's no separate "now go prove it" step —
proving happens *because* you built it from a checkable recipe.

The **Factory** is the part that does that building-and-checking. It takes the
signed **Order** (the recipe produced in [doc 01](01-the-order.md)) and runs it
through an assembly line of stages. Think of a real factory line: the raw
materials come in one end (the Order), each station does one job, and a record of
everything follows the product down the belt.

> **Order** = a signed file that lists exactly which security controls this
> project must meet and which cloud-setup "modules" are supposed to meet them.
> (Full definition in [06 · Glossary](06-glossary.md).)

One thing to hold onto from the very start: **the Factory does not decide whether
anything "passed."** It *builds*, *gathers facts*, and *runs automated checks*.
The final "yes, this is genuinely met" call belongs to a human — that's
[doc 03](03-machine-vs-human.md).

---

## The assembly line, stage by stage

Here's the whole line. Then we'll walk each station.

```
  signed ORDER
      │
      ▼
  1. Load the Order      ── re-check the fingerprints (tamper check)
  2. Fetch the modules   ── pull each cloud-setup module, by fingerprint
  3. Plan                ── REAL terraform dry-run (no cloud touched)
  4. Policy check        ── inspect the plan; a violation HALTS the line
  5. Apply (pretend)     ── simulated build (real build is Phase II)
  6. Collect evidence    ── gather machine-readable facts about the setup
  7. Run the oracles     ── automated pass / fail / can't-tell checks
      │
      ▼
  a run record (everything that happened) → handed to a human
```

### 1. Load the Order — "is this the real, untampered plan?"

The Order arrived as a file with **fingerprints** on it. A fingerprint here is a
**SHA-256 hash**: run a file's bytes through a standard math function and you get a
short string that changes completely if even one byte changes. (Think of it as a
wax seal that visibly cracks if someone opened the envelope.)

The Factory doesn't *trust* the fingerprints on the Order — it **re-computes them
itself** from the Order's contents and checks they match. If the recomputed hash
doesn't equal the one written in the Order, the Factory stops immediately with an
"Order tampered" error. (In the code: `run_stage_load_order` recomputes the order
hash and raises `OrderVerificationError` on a mismatch.)

**Why it matters:** nobody can quietly edit the recipe after it was signed.

### 2. Fetch the modules — "get the exact building blocks named in the Order"

The Order references a set of **modules** — reusable chunks of cloud setup (e.g.
"turn on multi-factor login for the sensitive-data group," "encrypt stored data").
Each module has its own fingerprint. The Factory pulls each one and **re-derives
its hash**, comparing it to what the Order expected. Wrong hash → wrong or altered
module → stop.

**Why it matters:** you're building from *exactly* the blocks the plan promised,
not a lookalike.

### 3. Plan — the real Terraform part (and the honest catch)

This is the stage people most often misunderstand, so plainly:

**Terraform** is an industry-standard tool that lets you write cloud setup *as
code* — a text description of "I want a login policy here, an encryption key
there." Instead of clicking around a cloud console, you write it down. Terraform
can then either **`plan`** (a *dry run*: "here's exactly what I *would* create or
change") or **`apply`** ("actually go do it").

The Factory runs a **real `terraform plan`** on **real infrastructure-as-code**
(the files under `terraform/tier1/` — IAM, KMS/encryption, logging, org-policy,
Workspace) and reads back the machine-readable result (`terraform show -json`).

**The honest catch — read this carefully:** it runs with **mock providers**. A
"provider" is the plug-in that talks to a specific cloud (Google, AWS, …). A
*mock* provider is a stand-in that answers as if a cloud were there but **never
connects to one**. So the plan is computed for real, but:

- **no real cloud is contacted**,
- **no credentials are used** (the code literally feeds a fake token like
  `mock-plan-no-cloud`),
- **nothing is deployed.**

You get a genuine, detailed preview of *what would be built* — without building
anything. That preview is the raw material the safety check reads next.

### 4. Policy check — the safety valve ("provision = prove")

Now the Factory inspects that **real plan** for rule violations — for example, is
any data being placed in a **non-US region**? (US-only data residency is a real
requirement for this contract.)

If the plan violates policy, the Factory **halts right here — before "apply."**
Nothing downstream runs. (In the code: `run_stage_policycheck` calls
`state.halt(...)` on failure, "halting before Apply.")

**This is the heart of "provision = prove."** The check reads the *actual build
plan the machine produced*, not a human ticking a box that says "yes we're
US-only." The plan either shows a compliant setup or it doesn't. A wrong plan can't
sneak past by being described nicely.

### 5. Apply — pretend, for now

In the finished Phase-II system, "apply" would take the approved plan and **build
the live environment**. Today it's a **mock apply**: a simulated version that lets
the rest of the line run end-to-end without standing up real cloud infrastructure.
So no real environment exists yet — this is a rehearsal of the full assembly line.

### 6. Collect evidence — "gather the facts"

**Evidence** = small machine-readable facts about the environment: *Is multi-factor
login on? Is stored data encrypted? Which region is the data in? How many
over-privileged accounts are there?*

Today these facts come from **fixture files** — hand-written mock data that stands
in for what a real cloud would report. Because the facts are mock, every piece of
evidence is stamped as non-real. There are actually **two** such stamps:

- **`mock`** — a fixture "config export" (pretend cloud settings).
- **`mock-plan`** — evidence derived from the real-but-mock-provider Terraform plan
  (stage 3). It proves *the plan*, not a live system — so it's still not real
  evidence.

Any run containing either stamp is flagged **NON-EVIDENTIARY** all the way through
to the final documents. That's the system refusing to let a rehearsal be mistaken
for the real thing. (More on the outputs in
[04 · The proof](04-the-proof.md).)

Crucially, each piece of evidence **points at** the control(s) it's about — it
"addresses" a control. It does **not** say the control is *met*. Hold that thought;
it's the whole subject of [doc 03](03-machine-vs-human.md).

### 7. Run the oracles — automated checks

An **oracle** is a tiny automated test: it reads *one* fact and compares it to
*one* rule, then says **pass**, **fail**, or **can't tell**. Example: the MFA
oracle reads `mfa_enforced_privileged` and passes only if it's `true`.

Only **7** controls in this whole system have an oracle (MFA, FIPS encryption,
encryption-at-rest, unauthorized-principals, IAM-count, log-export, US-region).
Every other control has **no** machine test — the oracle honestly returns
**can't tell**. That's not a bug; it's the system refusing to fake a check it can't
actually run. The full explanation — and why "can't tell" is the honest answer —
is [doc 03](03-machine-vs-human.md).

---

## What comes out: a run record, not a verdict

Everything above is collected into one **run record** (in the code, a
`PipelineState`): which modules were fetched, the plan result, whether the policy
gate halted, every evidence fact, every oracle outcome.

Notice what's *missing* from that list: any statement that a control is **MET**.
The Factory deliberately **does not** make that call. It assembles the facts and a
tidy record — then hands the whole thing to a human to judge. That hand-off is the
next doc.

---

## Three "what-if" runs you can try

The demo (`cli.py demo`, see [05 · Try it](05-try-it.md)) has a
`--evidence-set` switch that feeds the Factory three different fixture worlds:

| `--evidence-set` | What it simulates | What the Factory does |
| --- | --- | --- |
| `all-covered` | every required control has good evidence | line runs to the end; a clean run record |
| `gap` | a required control has **no module claiming it** | the *Order* is refused at Gate 1 (before the Factory even starts) — the line never runs |
| `contradiction` | a control's evidence makes its oracle **fail**, yet it's still attested MET | line runs, but the conflict gets flagged later (R13 — see doc 03) |

These aren't three different programs — they're the same Factory fed three
different fact-worlds, so you can watch it behave honestly in each.

---

## In one sentence

The Factory takes the signed Order, re-checks its fingerprints, runs a **real**
(but cloud-free, mock-provider) Terraform plan, **halts** if that plan breaks
policy, gathers machine-readable (today: mock) facts, runs the 7 automated oracle
checks, and packages it all into a run record — **without ever declaring a control
"met."**

**Next:** [03 · Machines check, only humans certify](03-machine-vs-human.md) — the
single most important idea in the whole system.
