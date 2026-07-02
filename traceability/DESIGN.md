# traceability/ — attestation, audit, SPRS score

**Purpose.** The human boundary + the completeness math. Three parts:

## attestation.py — the Affirming Official's determination
Port ADCS `traceability/attestation.py` almost verbatim. It is the ONLY
producer of a "control MET" claim. Emits, per control:
- `rtm:attests cmmc:<control>` + `rtm:hasOutcome` (EARL: passed=MET,
  failed=NOT MET, inapplicable=N/A, untested=PLANNED).
- adequacy `gsn:Assumption` + sufficiency `gsn:Justification` (the gap-notes
  column of Document 2 when not MET).
- `prov:qualifiedAssociation` → agent + `prov:hadRole` (Affirming Official /
  Compliance Officer / Project Lead — the responsible-party column).
- `rtm:hasEvidence` → the addressing evidence artifacts.
Declined attestations are well-formed (an honestly-assessed NOT MET), so the
audit distinguishes "not attested" from "attested-but-failing" — the
difference between an accurate SPRS score and a false claim.

## audit.py — bidirectional traceability
Port ADCS `traceability/audit.py` unchanged in shape:
- **forward:** every `cmmc:Control` reached by addressing evidence + an
  attestation (else it's a gap).
- **backward:** every attestation backed by evidence that declares
  `rtm:addresses` on the same control.
- **coverage matrix** → *is* the Traceability Matrix (Document 2), generated.
- **Gate 2:** the audit runs against the **Order's required-control set** — every
  control the Order committed to must come back MET, or the BOM is not compliant.

## sprs.py — SPRS score + POA&M-legality gate (NEW, stub present)
The compliance-specific addition. Reads `cmmc:weight` per control, subtracts
for every non-MET control, and **hard-fails** any 3-/5-point control parked on
a POA&M (32 CFR §170.21). Emits the 110 = Final / 88–109 = Conditional / <88 =
ineligible verdict. This is the "what we must do vs. what we've proved"
reconciliation, computed — not asserted.

**Inputs:** the full dataset. **Outputs:** `<ce:attestations>`, `<ce:audit>`;
the status/gap/POA&M columns of Document 2; the SPRS submission number.
