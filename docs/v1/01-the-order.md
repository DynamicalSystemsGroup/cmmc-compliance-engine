# 01 — The Order

The first machine is the **Order Compiler**. Its whole job is to turn a contract
into a **signed Order** — a precise, tamper-evident build order — and to refuse
if the plan doesn't actually cover the requirements. Let's walk through it in
plain English, using the real example the demo ships with: a contract called
**NV012**.

> New words here — **Order, COP, control, module, Gate 1, attestation** — are all
> in the [glossary](06-glossary.md).

## Step 1 — From contract to obligations (the COP)

A human reads the contract. For NV012 that means the SBIR topic text, its
question-and-answer clarifications, and the standard DoD contract clauses (the
**DFARS** clauses). With AI drafting help, they write down the contract's
**obligations** in plain, structured form — things like:

- "This work handles CUI, so we must meet **CMMC Level 2**."
- "Access is limited to **US persons** (an ITAR requirement)."
- "The data must stay in the **United States**."

This list of obligations is called the **COP** — the **Contract Obligation
Profile**. It's the contract, restated as "here is what we are on the hook for."

Then the one human judgment in this machine happens: a **Compliance Officer
attests** (signs off on) the COP — *"yes, these really are the obligations."*
Everything downstream is automatic; this is the single human call at the front.

> A CUI/ITAR deliverable can't be waved through: if an obligation would quietly
> drop a requirement, the compiler stops and asks a human to review it, instead
> of silently ignoring it.

## Step 2 — From obligations to controls

Each obligation is expanded into the specific security **controls** it requires.

**What's a control?** ELI5: **one specific security rule.** For example:

- `IA.L2-3.5.3` = "Use multi-factor authentication (MFA) for logins."
- `SC.L2-3.13.16` = "Encrypt sensitive data at rest."

The full catalog has **110** of these controls (the whole NIST 800-171 rulebook,
stored in the repo as data). An obligation like "CMMC Level 2" expands to the
controls that apply to *this* environment.

## Step 3 — From controls to modules

Each required control is matched to a **module** — a real piece of cloud setup
that **claims** to satisfy it.

**What's a module?** ELI5: **a specific thing you turn on or configure in the
cloud**, plus a note saying which control it satisfies and how to test it. For
example:

- A module "**Google Workspace 2-Step Verification on the CUI group**" claims to
  satisfy the MFA control `IA.L2-3.5.3`.
- A module "**encryption keys managed in Cloud KMS**" claims to satisfy the
  encrypt-at-rest control `SC.L2-3.13.16`.

A module also records **how its claim can be checked** — either an automated
check (an **oracle**, covered in [02](02-the-factory.md)) or a note that it's
verified by a human, or **inherited** from the cloud provider (e.g. the physical
security of Google's data centers is Google's responsibility, not ours).

## Step 4 — Gate 1: cover everything, or refuse

Now the safety check runs **before anything is built**. **Gate 1** asks three
questions about the plan:

1. **Forward:** does *every* required control have at least one module claiming
   it? (No uncovered rules.)
2. **Backward:** does *every* included module trace back to a required control?
   (No stray setup that isn't tied to a requirement.)
3. **No untestable claims:** does every claiming module say *how* its claim is
   verified?

If any answer is **no**, the Order is **refused** — and the refusal **names
exactly what's missing.** Nothing gets built on a plan with a hole in it.

If all three pass, the compiler emits a **signed Order**: a file listing the
required controls, the chosen modules, and a set of **SHA-256 fingerprints**
(hashes) of its own contents.

> **"Signed" here means fingerprinted, not cryptographically signed.** Every part
> of the Order is hashed with SHA-256, so if anyone changes a byte later, the
> fingerprints won't match and the tampering is caught. True cryptographic
> signing (Sigstore) is **deferred** — planned, not built yet. See
> [glossary: SHA-256, Sigstore](06-glossary.md).

## The NV012 example (real numbers)

When you run the demo on the NV012 contract:

- The Order ends up requiring **22 controls** — the scope of this **Tier-1**
  environment (an IL4 CUI enclave). Note: that's 22 of the 110, because this
  particular environment is only responsible for those 22. The other 88 are out
  of scope for *this* Order.
- Those 22 controls are covered by **10 modules** (MFA, encryption keys, IAM
  access groups, data-loss-prevention rules, US-region policy, audit-log export,
  disabling non-approved services, a Terraform baseline, monitoring/alerting, and
  the CSP-inherited physical controls).
- Gate 1 passes, so the Order is emitted.

### The "gap" demo — see a refusal happen

The demo has a scenario that deliberately breaks coverage. If you run it with the
`gap` setting, an extra required control — `AC.L2-3.1.12` ("monitor and control
remote access sessions") — is added **with no module claiming it.** Gate 1
refuses:

```
Gate 1 REFUSED — Order NOT emitted.
Missing module for required control(s): AC.L2-3.1.12
```

The Factory never runs, and no build happens. That's the point: **the machine
would rather stop and name the hole than build something it can't prove.**

## What the Order hands off

The result is one **signed Order file**, fingerprinted end to end. It's the only
thing the next machine needs. The Factory will take it, rebuild the exact modules
it names (verified by matching hashes), and execute the build — that's
**[02 — The Factory](02-the-factory.md)**.

## In one sentence

The Order Compiler turns a contract into a fingerprinted build order — obligations
→ controls → modules — and **refuses to emit it unless every required rule is
covered by a testable module.**

**Next: [02 — The Factory](02-the-factory.md)**
