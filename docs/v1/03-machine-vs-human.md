# 03 · Machines check, only humans certify

*Part of the v1 plain-English tour. Previous: [02 · The Factory](02-the-factory.md).*

---

## The most important idea in the whole system

If you remember only one thing from this entire tour, remember this:

> **A machine can *check a fact*. Only a person can *certify that a rule is met* —
> and that person is on the hook for it.**

Everything else — the Order, the Factory, the oracles, the final documents — is
built to protect that one line. Let's unpack it slowly, because two words that
sound almost identical are doing very different jobs.

---

## Verification vs Validation (they are not the same word twice)

- **Verification** = *a machine automatically checks a fact.*
  "The config file says multi-factor login is turned on." That's a mechanical,
  yes/no reading of data. No judgment, no accountability — just a measurement.

- **Validation** = *a responsible human certifies the requirement is genuinely
  met.* "I, the Affirming Official, certify this control is truly satisfied, and I
  understand I'm legally accountable for saying so."

### The spell-checker analogy

A spell-checker (verification) can flag every typo in a letter. It is fast,
tireless, and useful. But it **cannot sign the letter**. When the letter goes out
under your name, *you* signed it (validation) — and if it lies, *you* are
responsible, not the spell-checker.

Same here. The machine flags what it can measure. The **human signs** — and carries
the legal weight.

> **Affirming Official** = the accountable human who signs off that a control is
> met. "Legally accountable" is not decoration: under the **False Claims Act**,
> knowingly certifying something false to the government is a serious offense. That
> real-world liability is *exactly* why the system won't let a machine do the
> signing. (See [06 · Glossary](06-glossary.md).)

---

## The rule the whole system obeys

> **Evidence addresses; only attestation attests.**

Two verbs, chosen on purpose:

- **Evidence** can only **address** a control — *point at it*, say "I'm about this
  topic." A piece of evidence (like an MFA config export) is attached to the
  control it's relevant to, and that's *all* it can do. It can never declare the
  control met.
- An **attestation** — a human's signed judgment — is the **only** thing that can
  **attest**: mark a control **MET**.

In the machine's own vocabulary, evidence uses a link that literally means
"addresses," and only a human attestation uses the link that means "attests."
Nowhere in the system can evidence reach over and stamp something MET. It's not a
matter of policy or good behavior — it's wired in. ([02 · The Factory](02-the-factory.md)
is careful to only ever *address* controls with evidence.)

So a control becomes **MET** only when an Affirming Official signs an attestation
that says so. Not when a config looks right. Not when an oracle passes. **Only when
a human signs.**

---

## Oracles: pass, fail, or "can't tell"

An **oracle** is a small automated test that reads one fact and returns one of
three answers:

- **pass** — the fact meets the rule (MFA is on).
- **fail** — the fact breaks the rule (data is in the wrong region).
- **can't tell** (`cantTell`) — *there is no machine test for this control.*

That third answer is the honest heart of the design. Most security controls are
things like "screen personnel before granting access" or "train staff on insider
threat" — there is **no config field** a machine can read to check them. So the
oracle doesn't guess and it doesn't fake a pass. It says **can't tell**, which is a
polite way of saying *"a human has to judge this one."*

**How rare are machine checks? Only 7 controls have an oracle at all:**

| Control | What the oracle reads |
| --- | --- |
| `IA.L2-3.5.3` | multi-factor login enforced for privileged accounts |
| `SC.L2-3.13.11` | FIPS-validated encryption module present |
| `SC.L2-3.13.16` | stored data ("at rest") is encrypted |
| `AC.L2-3.1.1` | zero unauthorized accounts have access |
| `AC.L2-3.1.5` | zero over-privileged access bindings |
| `AU.L2-3.3.1` | audit-log export is enabled |
| `ITAR-120.54` | data region is US-only |

*(These are the exact entries in `oracles/criteria.py`.)* Every other control in a
run resolves to **can't tell** → a human decides. "Can't tell" isn't failure; it's
the machine staying in its lane.

---

## The contradiction check (R13): the system won't lie to itself

Here's the subtle danger the design guards against. Suppose:

1. an oracle for a control runs and says **fail** (the machine sees a problem), but
2. a human signs an attestation saying that same control is **MET**, and
3. there's **no written override justification** explaining the disagreement.

That's a **contradiction** — the human and the machine flatly disagree, with no
explanation. A naive system would just trust the human's "MET" and print a clean
report. This one **refuses to**. It **surfaces the conflict** as a first-class flag
(this rule is called **R13**), so an auditor sees it plainly instead of it hiding
under a green checkmark.

Two honest outcomes are allowed:

- The official adds a written **override justification** ("the oracle checks X, but
  we satisfy the control a different way, documented here") → the contradiction is
  **cleared** (the disagreement is now explained).
- No justification → the contradiction **stays flagged** in the audit and in the
  final document.

**See it live:** the demo's `--evidence-set contradiction` run does exactly this.
It attests a control MET while its oracle failed, with no override — and the run
reports **`contradictions: 1`**. The conflict is shown, not swallowed.
([02 · The Factory](02-the-factory.md) lists the three demo scenarios.)

---

## The honesty payoff: most "MET"s are human, not machine-proven

Put the last two sections together and something important falls out.

Because only **7** controls have an oracle, and a real NV012 run scopes to about
**22** controls, **most controls in a run have no machine proof at all** — they're
**MET** because a human (or an inherited/CSP control) attested them, not because a
machine measured them.

The system doesn't hide this — it *counts and prints it*. A real demo run reports:

```
Proven vs attested: 4 MET-by-machine / 18 MET-by-human-only
```

Four controls were backed by a passing oracle. Eighteen were marked MET on human
judgment alone. Both are legitimate — but they are **not the same kind of
evidence**, and the system makes you look at the split instead of blurring it into
one reassuring number. (And remember: this whole run is **NON-EVIDENTIARY** anyway,
because the underlying facts are mock — see [02 · The Factory](02-the-factory.md).)

That is the entire ethic of this project in one number: **don't let a pile of
attestations look like a pile of proofs.**

---

## In one sentence

Machines **verify** facts and can only *point at* controls; a human **Affirming
Official** is the only one who can *attest* a control **MET** (and is legally
accountable for it) — so oracles honestly say "can't tell" for the many controls
they can't measure, the system **flags** any human/machine contradiction instead of
trusting it, and it openly reports how few "MET"s are actually machine-proven.

**Next:** [04 · The proof — BOM, SSP, and the Matrix](04-the-proof.md) — what the
run finally produces, and why it's stamped NON-EVIDENTIARY.
