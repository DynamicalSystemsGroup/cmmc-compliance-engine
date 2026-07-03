# The Order

*Part of the v1 plain-English tour. Previous: [00-what-is-this.md](00-what-is-this.md).*

---

The Compliance Engine has two machines. This chapter is about the first one, the
**Order Compiler**. Its job is to turn a contract into a **signed Order** and to
refuse to produce one if the plan does not cover the contract's requirements.

The Order is the single input that drives everything downstream. The second
machine, the Factory (covered in [02-the-factory.md](02-the-factory.md)),
consumes a signed Order and does not accept anything else. So the Order Compiler
is where a written contract becomes a precise, machine-readable, tamper-evident
build plan.

New terms in this chapter (Order, obligation, COP, control, module,
authoritative source, reference, attestation role, Gate 1) are all defined in
[06-glossary.md](06-glossary.md).

The Order Compiler runs a four-step chain:

```
contract  ──▶  obligations (the COP)  ──▶  required controls  ──▶  modules  ──▶  Gate 1  ──▶  signed Order
              step 1                       step 2                  step 3        step 4       output
```

The code lives under `src/compliance_engine/order_compiler/`
(`cop.py`, `rule_library.py`, `compiler.py`, `gate1.py`).

---

## Step 1 — From contract to obligations (the COP)

A contract does not list security controls. It states what the work involves:
that it handles Controlled Unclassified Information (CUI), that access is limited
to U.S. persons under ITAR, that certain data must stay in the United States, and
so on. Someone has to read the contract and write those requirements down in a
structured, machine-readable form. That structured record is the **Contract
Obligation Profile**, referred to in the code as the **COP**.

Software does the drafting. It parses the contract's clauses and proposes a set
of **obligations** — one structured statement per requirement it finds. But
software does not get the final word here. A **Compliance Officer** reviews the
drafted obligations and **attests** them. That attestation is the single human
judgment on the input side of the engine, and it mirrors the single human
judgment on the output side (the Affirming Official, covered in
[03-machine-vs-human.md](03-machine-vs-human.md)). Machines draft; a named,
accountable human signs.

> Founding principle, input side: software drafts the contract's obligations, and
> a Compliance Officer attests them. The engine never treats a machine-drafted
> obligation as authoritative on its own.

### The spillover guard

There is one place in step 1 where the engine deliberately stops rather than
guess. If a deliverable is marked CUI or ITAR, the engine will **not silently
drop a requirement**. A **spillover guard** forces human review instead of
letting a sensitive requirement fall out of the profile unnoticed. The reasoning
is simple: quietly omitting a CUI or ITAR obligation is exactly the kind of
mistake that must never be automatic. When the guard fires, a human has to look
at the requirement and decide, on the record, rather than the software making the
requirement disappear.

The demo's contract inputs live under `fixtures/nv012/` (the drafted profile is
`cop_draft.ttl`).

---

## Step 2 — From obligations to required controls (the rule library)

Obligations are still written in the contract's language ("this handles CUI,"
"access is limited to U.S. persons"). The engine needs to translate them into the
common vocabulary that assessors actually use: **controls**.

A **control** is one specific security requirement from the standard. The
Compliance Engine targets **CMMC Level 2**, which is the **110 controls of NIST
SP 800-171 Rev. 2** — the security requirements that U.S. defense contractors
handling CUI must satisfy. The full catalog of 110 controls is the "law" layer of
the data model, stored in `data/ontology/cmmc-edit.ttl` under the `cmmc:`
namespace.

Two concrete examples of what a control is:

- **IA.L2-3.5.3** — use **multi-factor authentication** for access to privileged
  and non-privileged accounts.
- **SC.L2-3.13.16** — protect the **confidentiality of CUI at rest** (encrypt
  stored CUI).

The **rule library** (`src/compliance_engine/order_compiler/rule_library.py`)
maps each attested obligation to the controls it implies. An obligation like
"this work handles CUI, so we must meet CMMC Level 2" expands into the specific
set of catalog controls that obligation triggers. The output of step 2 is the
Order's **required-control set**: the exact list of controls this contract must
satisfy, drawn from the catalog of 110.

For the shipped demonstration contract, **NV012**, that required set is **22
controls** — a Tier-1 slice, not the whole catalog. More on that below.

---

## Step 3 — From controls to modules

Knowing *which* controls are required is not the same as knowing *how* each one
will be satisfied and proven. That mapping is the job of **modules**.

A **module** is a self-contained unit that claims responsibility for one or more
controls and declares exactly how each claim will be checked. Every module now
carries five things:

1. **The controls it claims** — which catalog controls this module is responsible
   for.
2. **An authoritative source** (`ce:AuthoritativeSource`) — the system that owns
   the ground truth for this class of evidence. That might be a cloud API, a
   learning-management system, an HR system, a document repository, or the
   engine's own run history.
3. **A reference into that source** (`ce:Reference`) — a resolvable pointer, with
   a URI, a freshness window, a last-verified timestamp, and a named custodian.
4. **A required attestation role** (`ce:attestationRole`) — which role a human
   must hold to sign off on this control.
5. **A verification method** — one of three: a **config-check oracle** (for
   controls a machine can measure), the **attested-reference oracle** (for
   controls that rest on a reference plus a human signature), or an
   **inheritance marker** (for controls inherited from the cloud service
   provider).

The verification method is what makes a module *testable*. A module that claims a
control but names no way to check it is not allowed — Gate 1 rejects it (see step
4).

The full structural model ships **39 modules** covering **all 110 controls**,
split by how each control is verified: **65 machine-verified** (config-check
oracle), **43 attested-reference**, and **2 CSP-inherited**. Here are one of each
of the two main kinds.

### A machine-verified module

Some controls can be measured directly against a system's real configuration.
Example: a module that claims the multi-factor-authentication control by checking
that **Workspace 2-Step Verification** is enforced. Its authoritative source is
the cloud/identity API that owns that configuration; its verification method is a
**config-check oracle** that reads the actual setting and compares it against the
required state. A machine can answer "is 2-Step Verification enforced?" without a
human in the loop, so the oracle can produce a machine assertion on its own — but
the control is still not marked *met* until a human attests it (see
[03-machine-vs-human.md](03-machine-vs-human.md)).

### A policy-and-records module

Many controls cannot be measured by reading a configuration, because the truth of
them lives in a document or a record, not in a running system. Example: a module
for the **incident-response plan** control. Its authoritative source is a
**document repository**; its reference is a pointer to the incident-response plan
document, with a freshness window and a named custodian; its required attestation
role is the role that owns that area; and its verification method is the
**attested-reference oracle**. The engine does not "read" whether an
incident-response plan is good. It checks that a registered reference to the plan
**resolves, is within its freshness window, and is signed by a human in the
required role**.

This uniform treatment — a machine-measurable control and a document-backed
control both go through a registered-reference-plus-signature check — is what lets
the engine cover all 110 controls, not only the ones a machine can measure. The
full model is explained in [03-machine-vs-human.md](03-machine-vs-human.md).

---

## Step 4 — Gate 1: does the plan cover the requirements?

Before an Order is emitted, the Order Compiler runs **Gate 1**, the
**planning-coverage** gate. Gate 1 asks whether the set of chosen modules
actually and provably covers the required-control set — *before anything is
built*. It has three parts:

- **Forward coverage.** Every required control has at least one claiming module.
  Nothing the contract requires is left without an owner.
- **Backward coverage.** Every included module traces back to a required control.
  Nothing extra sneaks in that the contract did not ask for.
- **No untestable claim.** Every claiming module names a verification method. A
  module cannot claim a control and then offer no way to check it.

If Gate 1 fails, **the Order is not emitted, and the gap is named.** The compiler
does not produce a partial or best-effort Order. It refuses and reports exactly
what is missing. Gate 1's code is
`src/compliance_engine/order_compiler/gate1.py`.

Gate 1 is the *planning* gate. There is a second gate, Gate 2, that runs much
later, at the close of the Bill of Materials, and asks a different question —
whether each control was actually *proven and attested*. Gate 2 is covered in
[03-machine-vs-human.md](03-machine-vs-human.md) and
[04-the-proof.md](04-the-proof.md). Keep the two straight: Gate 1 checks the
*plan*, Gate 2 checks the *proof*.

---

## The signed Order

When all four steps pass, the compiler emits the **Order**: a precise,
machine-readable record of exactly which controls this contract requires and
exactly which modules are responsible for them.

The Order is **"signed."** Today that means **hash-referenced**: the Order and
everything it points at are identified by their **SHA-256** content hashes.
"Signed" here means **fingerprinted** — the content is reduced to a fixed
fingerprint, so any change to the content produces a different fingerprint, and
the Factory can recompute those fingerprints later to confirm nothing was altered
between planning and building.

> Note: "signed = fingerprinted." True cryptographic signing (Sigstore/cosign)
> is future work. Today the guarantee is tamper-evidence through content hashing,
> not a cryptographic identity signature. See the honest-limits section of
> [00-what-is-this.md](00-what-is-this.md).

---

## The NV012 example, with real numbers

The shipped demonstration contract is **NV012**. Its Order requires **22
controls** — a Tier-1 slice of the catalog — and those 22 are covered by the
**10 baseline (Tier-1) modules**. Of the 22, **20 are machine-verified** and **2
are inherited from the cloud service provider**.

It is important to keep two numbers distinct:

- The **structural model claims all 110 controls** across its 39 modules.
- The **NV012 Order scopes to 22 controls.** An Order is compiled for a specific
  contract, and NV012's obligations expand to a 22-control required set, not the
  full 110.

Everything downstream for the NV012 demo — the Factory run, the SPRS score, the
Bill of Materials, the System Security Plan — is computed over those 22 required
controls, not over all 110.

When you run the all-covered demo, step 1 of the chain prints the compiled
Order's hash and its control count:

```
[1/6 compile-order] Order cdad6fb17f7cb53728276bb24de654c87b6725e31b9bd731efa7769234afbc85 (22 controls)
```

That hash is the Order's fingerprint. The Factory re-derives it before it will
run (see [02-the-factory.md](02-the-factory.md)).

---

## When the plan does not cover: the gap scenario

The demo ships a scenario, `--evidence-set gap`, that exercises Gate 1's refusal
path. Run it and the chain stops at step 1:

```
[demo] evidence-set=gap
[1/6 compile-order] Gate 1 REFUSED — Order NOT emitted. Obligation cites control ID 'XX.L2-3.99.99', which is not one of the 110 controls in cmmc-edit.ttl.
```

The run exits with **code 2** — the exit code for a Gate 1 refusal or bad
arguments. No Order is written.

There is a nuance worth stating plainly. Gate 1's forward check exists to catch a
*required-but-unclaimed* control — a requirement with no module to satisfy it.
But **all 110 real catalog controls now have a claiming module**, so with a
genuine catalog control that particular gap cannot occur. To demonstrate the
refusal path, the gap scenario therefore **injects a fake, non-catalog control
id, `XX.L2-3.99.99`.** The catalog validator rejects it *before* Gate 1, because
that id is not one of the 110 controls in `cmmc-edit.ttl`.

The lesson is the same either way: **the compiler refuses to emit an Order it
cannot fully cover, and it names the exact problem.** It does not paper over a gap
and continue.

---

## Summary

The Order Compiler turns a contract into a signed, machine-readable Order in four
steps: software drafts the contract's obligations and a Compliance Officer
attests them (with a spillover guard that refuses to silently drop a CUI or ITAR
requirement); the rule library maps those obligations to the required controls
drawn from the catalog of 110; those controls are assigned to modules that each
declare an authoritative source, a reference, a required attestation role, and a
verification method; and Gate 1 checks — forward, backward, and no-untestable-
claim — that the modules provably cover the requirements. If Gate 1 fails, no
Order is emitted and the gap is named. If it passes, the Order is emitted and
hash-referenced by SHA-256 — "signed" in the sense of fingerprinted, with true
cryptographic signing still to come. For the NV012 demo the Order scopes to 22
controls covered by the 10 baseline modules, even though the full structural
model claims all 110.

**Next: [02-the-factory.md](02-the-factory.md).**
