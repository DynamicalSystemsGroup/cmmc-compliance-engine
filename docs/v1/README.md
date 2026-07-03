# The Compliance Engine: a plain-English tour

This is a guided, chapter-by-chapter tour of what the Compliance Engine does, how it
works, and what it does not yet do. It is written for two readers at once: compliance
and operations staff who need to understand what the system produces and why they can
trust it, and engineers who need to understand how it is built. The explanations stay
plain enough to follow without a technical background, but precise enough to be correct.

## What this system is

The Compliance Engine ingests a signed description of what a contract requires and a
signed set of statements about how an organization satisfies each requirement, and it
emits a System Security Plan (SSP), a Bill of Materials (BOM) of the supporting
evidence, and a Supplier Performance Risk System (SPRS) score. Every automated check,
every piece of evidence, and every human sign-off is content-addressed and cross-linked,
and no requirement is recorded as met until a named, role-appropriate human signs a
statement to that effect.

It targets CMMC Level 2: the 110 security controls of NIST SP 800-171 Rev. 2, required
of U.S. defense contractors that handle Controlled Unclassified Information (CUI). It is
written in Python over an RDF named-graph store, drives real Terraform at plan level, and
produces byte-deterministic output from a given set of inputs.

## The two big ideas

Two ideas run through the whole tour. Neither is optional; both should come through in
every chapter that touches them.

1. **Provisioning and proving are the same action.** The environment is described by a
   signed Order, and the proof of compliance is produced from that same description, not
   gathered afterward by inspection.

2. **The attested-reference model.** Every control points at an authoritative source
   (the place where the truth of that control actually lives). The engine checks that a
   reference into that source is registered, resolves, is within its freshness window,
   and is signed by a human in the required role. This uniform check applies equally to a
   control a machine can measure and a control only a human can attest, which is what lets
   the engine cover all 110 controls rather than only the machine-measurable ones.

The catalog has 110 controls, and all 110 now have a claiming module. They split into 65
machine-verified, 43 attested-reference, and 2 CSP-inherited, across 39 modules total.

## Reading order

Read the chapters in order. Each builds on the one before it.

1. [00-what-is-this.md](00-what-is-this.md) — The problem, the two big ideas, the
   110-control coverage picture, the two machines, the two gates, and the honest limits.
2. [01-the-order.md](01-the-order.md) — The Order Compiler and Gate 1: how a contract
   becomes obligations, then a required-control set, then modules, then a signed Order.
3. [02-the-factory.md](02-the-factory.md) — The runtime pipeline: load the Order, fetch
   each module, run a real terraform plan, apply the policy and residency gate, run a
   mock apply, collect evidence, and run the oracles.
4. [03-machine-vs-human.md](03-machine-vs-human.md) — How a control becomes MET: the
   founding principle, verification versus validation, the attested-reference model in
   full, the oracle outcomes, and the contradiction guard.
5. [04-the-proof.md](04-the-proof.md) — The outputs (audit, SPRS, BOM, SSP) and proof by
   reproduction: how an assessor re-derives every result from the delivered BOM.
6. [05-try-it.md](05-try-it.md) — Run the three demo scenarios and read the exact output.
7. [06-glossary.md](06-glossary.md) — Every term used in the tour, A to Z.

The glossary at [06-glossary.md](06-glossary.md) can be read at any time. Jump to it
whenever a term is unfamiliar; the other chapters link to it on first use of a term.

## Honest limits

State these plainly before you start, so nothing here is mistaken for a finished product.
Chapter [00-what-is-this.md](00-what-is-this.md) covers each in detail.

- Every run today is non-evidentiary: evidence is fixture-backed and the terraform plan
  uses mock providers, so no run produces a submittable government artifact. When any weak
  input is present, the BOM and SSP are stamped NON-EVIDENTIARY, and there is no switch to
  remove that banner while mock inputs are present.
- The engine records claims; it does not make an organization compliant. A false claim
  still passes here. The human signer carries the accountability, and an assessor catches it.
- References are not resolved live yet, attestations are not cryptographically signed yet,
  and the engine does not talk to SPRS: a human files the computed score at the government
  portal.
- The 16 policy documents shipped under `src/compliance_engine/documents/policies/` are
  scaffolding and must be replaced with an organization's own adopted policies.

## A note for technical readers

This tour is the plain-English path into the system. The repository root README covers the
same system comprehensively for a technical reader, and the chapters here link into the
code as they go.

To begin the tour, read [00-what-is-this.md](00-what-is-this.md).
