# order-compiler/ — contract → signed Order (separate upstream tool)

**Purpose.** Turn a contract into a proof-carrying **Order** the Factory can
execute. This is a **standalone tool** (chosen seam): its only output is a
signed Order file handed over the fence to the Factory. It is *not* wired into
the Factory runtime — Orders can be produced, reviewed, and version-controlled
independently.

**Why it exists.** An Order must not be hand-waved ("just give me CMMC L2"). If
it is, the downstream proof is proof of the wrong thing. The Compiler makes the
Order a *compiled projection* of the contract, carrying its own derivation.

## Pipeline (contract → Order)

```
A. Intake         hash the contract artifacts (SBIR topic PDF, Q&A, DFARS clauses)
B. COP            extract obligations → Contract Obligation Profile
                    ** AI drafts, a Compliance Officer ATTESTS ** (the one human call)
                    clause library forces obligations: cite 7012 ⇒ CUI/800-171,
                    7021 ⇒ CMMC status, ITAR topic ⇒ US-person + residency + e2e
C. Obligation→Control   resolve each obligation to its required control set
                    (rule library, versioned + regulation-cited)
D. Control→Module resolve required controls to the modules that CLAIM them
                    (module metadata: cmmc:controlsSatisfied)
E. GATE 1          planning coverage:
                    - forward: every required control has a claiming module
                    - backward: every module traces to a required control
                    - no claim without a testable method
                    fail ⇒ Order does NOT emit
F. Emit           compile the signed Order (references COP hash, control-set
                    hash, coverage-proof hash) → hand to the Factory
```

## The COP is the pivotal artifact
A structured, content-addressed reading of the contract. Each obligation is a
first-class node (`cmmc:Obligation`, stub in `obligations.ttl`) with: source
(hashed clause / Q&A ref), type (framework | hosting | data | personnel |
environment | **deliverable**), `cmmc:derivesControls`, and `attestedBy`. Two
layers: obligations on **DSG's environment** (drive the Order) vs. obligations
on the **deliverable** (tagged, but not provisioned). See a worked NV012
example in `obligations.ttl`.

## Reusable Contract Profiles (SOPs)
NV011 and NV012 share a profile (DLA SBIR, CMMC L2 + ITAR + CUI, Phase I
offeror-hosted). Author the profile `DLA-SBIR-CUI-ITAR-Phase1` once; instantiate
per-contract Orders by filling only the deltas (contract_id, personnel, data
classes). First contract is expensive; the rest are near-free.

## Ports from ADCS
The ADCS requirement-derivation model (`satellite req → ADCS req`, with
forward/backward audit) is the template — we extend it one level up
(`contract → obligation → control`) and reuse the same bidirectional-audit
mechanism for Gate 1.

## Files
`obligations.ttl` (COP vocab + NV012 example, stub) · `DESIGN.md`.
**Inputs:** contract artifacts under `../reference/contracts/`.
**Outputs:** a signed Order file (consumed by `../pipeline/`); the `<ce:order>`
graph recording the derivation.
