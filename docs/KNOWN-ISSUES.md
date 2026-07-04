# Known issues

Tracked, honestly-stated defects and gaps. Each entry says what is wrong, why it
is not already fixed, and how to fix it.

---

## KI-1: `ce verify` was broken and did not conform on the mock demo — RESOLVED

**Status:** RESOLVED (2026-07-03). Was pre-existing (predated `feat/signed-provenance`,
confirmed on `main`). Fix + regression test below.

**Resolution.**
- Fixed the import (`from compliance_engine.traceability import verification`) and a
  second bug in the same command (it read `m.evidence_iri/expected_hash/actual_hash`,
  but `ReverificationMismatch` fields are `evidence/expected/actual`).
- `verify` now separates the **tamper check** (re-hash every evidence node — always a
  hard failure on a mismatch) from the **SHACL closure** suite. On a NON-EVIDENTIARY
  (mock) run, closure findings for human-only controls are reported as an advisory,
  not a hard failure; on real evidence they remain hard failures.
- Fixed two real closure violations surfaced along the way: the downstream P-Plan
  activities lacked a `prov:wasAssociatedWith` agent (ActivityAgentShape), and the
  SOP step definitions (`plan.ttl`) were not loaded at verification time so
  `correspondsToStep` targets were untyped (PlanInstantiationShape). `verify_shacl`
  now loads `plan.ttl` alongside the data.
- Added `tests/test_verify_cli.py`: `ce verify` passes on a clean mock demo (with the
  advisory) and exits non-zero on tampering.

Net: `ce verify` on the demo now prints "No tampering detected" plus a clear
NON-EVIDENTIARY advisory and exits 0; a corrupted evidence hash prints "TAMPERING
DETECTED" and exits 1.

**Original diagnosis (for the record).** The `verify` command had two independent
problems:

1. **Import bug (hard crash).** Its body does `import traceability.verification`
   (a bare top-level import) instead of
   `from compliance_engine.traceability import verification`. The `traceability`
   package lives under `src/compliance_engine/traceability/`, so the bare import
   resolves nowhere and the command raises `ModuleNotFoundError: No module named
   'traceability'` before it does any work. This line is present on `main`
   (`git show main:src/compliance_engine/cli.py`, line 511), so the bug predates
   this branch. No test invokes the `verify` command, so it has never been a
   passing path — the crash went unnoticed.

2. **Shapes are written for real evidence, not the mock demo.** Even with the
   import fixed, `verification.verify(ds)` runs the full closure/verification SHACL
   suite, which assumes real evidence. On the shipped **NON-EVIDENTIARY** demo it
   reports non-conformance for reasons that are expected on mock data — e.g.
   human-only controls that legitimately have no addressing evidence — mixed with a
   pyshacl inference artifact (a phantom blank-node `p-plan:Activity` flagged for a
   missing `correspondsToStep`, even though every real activity in the dataset has
   exactly one). So the command is not expected to conform on a practice run.

**What this does NOT affect.** This is a different command from `ce verify-package`
(the Phase E audit-package re-verification), which is fully wired and passes:
`ce verify-package` verifies the signed manifest, re-hashes every bundled artifact,
and checks the control->signed-policy chain. The demo, the notebook, `ce package`,
and the whole test suite (396 passing) are unaffected.

**Why it was not fixed here.** It is a pre-existing bug in a command that is not one
of the six signed-provenance items and is not part of the demo/notebook path.
Fixing the import is a one-liner, but making `verify` *behave sensibly* also
requires deciding how it should report on NON-EVIDENTIARY data and running down the
pyshacl inference artifact — a separate, self-contained task. During the
signed-provenance work an opportunistic import fix was made and then reverted to
keep that change set scoped; the command was left exactly as found.

**How to fix (follow-up).**
1. Change `import traceability.verification` to
   `from compliance_engine.traceability import verification` (and use
   `verification.verify(...)`).
2. Have `verify` detect a NON-EVIDENTIARY dataset and print a clear message that
   full SHACL conformance is expected only on real evidence (so mock-data gaps read
   as "expected on a practice run", not as a crash or regression).
3. Investigate the phantom-blank-node `p-plan:Activity` finding (likely a pyshacl
   inference setting in `traceability/verification.py`); confirm the real dataset
   conforms on the `PlanInstantiationShape` (it does — all 12 activities carry
   exactly one `correspondsToStep`).
4. Add a test that invokes `verify` so it can never silently rot again.

**Note on provenance hygiene (already fixed).** The signed-provenance work initially
introduced one real SHACL violation here — evidence nodes and oracle assertions
already carry a generating activity, and the new P-Plan binding added a second
`prov:wasGeneratedBy` (violating the max-one-generating-activity shape). That was
fixed: those nodes are now tied to their plan Variable via `correspondsToVariable`
only. Every `prov:Entity` the run produces has at most one generating activity.
