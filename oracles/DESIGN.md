# oracles/ — machine control checks (verification, not validation)

**Purpose.** Compare one machine-readable observation from an evidence
artifact against a control's acceptance criterion and emit a fully-specified
EARL outcome. This is **verification** (`earl:mode = earl:automatic`) — an
*input* to the Affirming Official's judgment, never a substitute for it.

**Port from ADCS.** `analysis/oracle.py` is the direct template: an
`ACCEPTANCE_CRITERIA` table + `evaluate_*` functions returning
`passed | failed | cantTell`. The RDF side (persisting the outcome as an
`earl:Assertion`) ports from `traceability/oracle_assertion.py`.

**The critical guardrail (inherited).** A control with **no** machine-checkable
criterion returns `earl:cantTell` — the oracle never fabricates a verdict it
cannot compute. ~40 of 110 controls (policy, training, PS, IR, physical) are
`cantTell` by nature and MUST be human-attested from documentary evidence.
This is what stops the engine from silently auto-passing "we say we do it"
without "we can prove it."

**What the oracle verifies is a config claim, not the control.** "Azure Policy
reports MFA enforced" is an observation about a model of the system; the
Affirming Official still attests the control MET. Preserve this discipline
verbatim — it is CMMC's legal reality (False Claims Act) and the ADCS ethic.

**Files.** `criteria.py` — the criteria table + evaluator (stub present).
**Inputs:** evidence `summary` dicts from `evidence/generators/`.
**Outputs:** `rtm:ControlCheckAssertion` nodes in `<ce:audit>`; feeds the
status column of Document 2 (as evidence for the attestation, not the status
itself).
