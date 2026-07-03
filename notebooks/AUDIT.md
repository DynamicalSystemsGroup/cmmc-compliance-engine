# Notebook Accuracy Audit — `compliance_walkthrough.py`

**Audited:** `notebook/compliance_walkthrough.py` + `notebook/_engine.py` + `notebook/README.md`  
**Method:** Static read + engine execution verification (`uv run python3` spot-checks)  
**Date:** 2026-07-03  
**Verdict:** 4 critical errors, 4 major errors, 4 minor issues. No issues in `_engine.py` or `README.md`.

---

## Summary Table

| # | File | Location | Severity | Finding |
|---|------|----------|----------|---------|
| F1 | walkthrough.py | tab1_obligations | **Critical** | Says "Three obligations" — engine loads 9 |
| F2 | walkthrough.py | tab1_controls callout | **Critical** | "88 controls out of scope for this contract" — false |
| F3 | walkthrough.py | tab3_auditor | **Critical** | `cli.py verify --bom` — command does not exist |
| F4 | walkthrough.py | tab1_cop_sign mockup | **Critical** | "SBIR Phase II" — should be Phase I |
| F5 | walkthrough.py | tab1_intro + tab1_cop_sign | **Major** | DFARS 252.204-7012 cited as the CMMC clause — wrong clause number |
| F6 | walkthrough.py | footer (line 1162) | **Major** | "~7 controls are machine-checked" — actual count is 6 oracles, 4 passing |
| F7 | walkthrough.py | tab2_factory callout | **Major** | Hardcoded list of 7 machine-checkable areas doesn't match actual oracle outcomes |
| F8 | walkthrough.py | tab2_attest FCA callout | **Major** | "22 potential false claims" — legally inaccurate framing |
| F9 | walkthrough.py | tab1_intro callout | **Minor** | "the act of building IS the proof" — overstated |
| F10 | walkthrough.py | sidebar scenario descriptions | **Minor** | "contradiction — human overrules failed machine check" — wrong word |
| F11 | walkthrough.py | tab2_factory success text | **Minor** | Lists 9 module descriptions for 10 modules |
| F12 | walkthrough.py | tab2_attest FCA callout | **Minor** | FCA penalty amounts are 2024 figures |

---

## Critical Findings

### F1 — Obligations count: says "Three", engine loads 9

**Location:** `tab1_obligations` (static text + flowchart)

**What it says:**
```
"Three obligations are extracted from the NV012 contract."
```
The Mermaid flowchart also labels the obligations node "3 Obligations CMMC L2 · US Persons · US Soil".

**What is true:**  
Running `compiler.load_pipeline_dataset()` against the actual `fixtures/nv012/cop_draft.ttl` returns **9 obligation objects**:

| Obligation | Type | Controls |
|------------|------|----------|
| OBL-NV012-ACCESS | data | 4 |
| OBL-NV012-AUDIT | environment | 3 |
| OBL-NV012-CONFIG | environment | 4 |
| OBL-NV012-CRYPTO | data | 3 |
| OBL-NV012-DELIV-TOOL | deliverable | 0 (spillover guard) |
| OBL-NV012-IDENTITY | personnel | 3 |
| OBL-NV012-MONITOR | environment | 2 |
| OBL-NV012-PHYS | environment | 2 |
| OBL-NV012-RESIDENCY | environment | 1 |

The "3" in the static text is a conceptual summary of the three top-level requirements (CMMC L2, US Persons, US Soil). But the dynamic `md_table` below it will render 9 rows, directly contradicting the "Three obligations" heading. A viewer reading the static text then seeing the table will be confused.

**Fix options:**  
- Change "Three obligations" → "Nine obligations, grouped under three top-level requirements (CMMC L2 identity, US data/crypto, and US residency)."  
- Or: change the conceptual framing to "Nine obligations extracted..." and update the Mermaid node label from "3 Obligations" to "9 Obligations".

---

### F2 — "88 controls out of scope for this contract" — false

**Location:** `tab1_controls`, `kind="warn"` callout

**What it says:**
```
"The other 88 controls in NIST 800-171 are out of scope for *this* contract."
```

**What is true:**  
The other 88 controls are out of scope for the **demo** (the Phase I Tier-1 slice). They are NOT out of scope for the NV012 contract itself. DFARS 252.204-7012 / 252.204-7021 and the CMMC L2 requirement attach all 110 NIST SP 800-171 controls to NV012 unconditionally. The canonical `order-compiler/obligations.ttl` has `OBL-CMMC-L2 → ALL-110-NIST-800-171` for exactly this reason.

What the `cop_draft.ttl` does is artificially scope the *demo run* to 22 controls that current Tier 1 modules can satisfy — so Gate 1 doesn't refuse. Its own comment says:
> "Unlike the canonical order-compiler/obligations.ttl (whose OBL-CMMC-L2 expands to all 110 controls), this draft is the Phase-I Tier-1 slice."

Telling a viewer (or a contracting officer, or a C3PAO) that 88 controls are "out of scope for this contract" is the most consequential accuracy error in the notebook. It implies a CMMC L2 contract can legitimately exclude most of its requirements. It cannot.

**Fix:**  
Change the callout to:
```
"The other 88 controls are not covered in this demo — the Phase I Tier-1 scope only.
 In a real NV012 self-assessment, all 110 controls must be addressed. See the
 self-assessment plan (docs/plans/2026-07-03-002-path-to-self-assessment.md) for
 how to extend coverage to all 110."
```

---

### F3 — `cli.py verify --bom bom.json` — command does not exist

**Location:** `tab3_auditor`, "C3PAO Re-Verification Screen" callout

**What it says:**
```
$ uv run python cli.py verify --bom bom.json
```

**What is true:**  
The CLI has these subcommands: `compile-order`, `run-factory`, `attest`, `audit`, `bom`, `ssp`, `demo`. There is no `verify` subcommand. If a viewer (or an assessor) copies this command and runs it, they get:

```
Error: No such command 'verify'.
```

The BOM verification functionality (re-hashing evidence nodes to detect tampering) exists in `traceability/verification.py` but is not exposed as a CLI command. The "C3PAO Re-Verification Screen" is a mockup of a planned capability, not a real one.

**Fix options:**  
- Add a `verify` subcommand to `cli.py` that calls `traceability.verification.verify()` on a stored BOM. This is the cleanest fix and makes the demo accurate.  
- Or: label the screen clearly as a **planned capability / design mockup** and note it's not yet a real command.

---

### F4 — "SBIR Phase II" in the COP signing mockup — should be Phase I

**Location:** `tab1_cop_sign`, "COP Attestation Screen" callout

**What it says:**
```
> **Contract:** NV012 (SBIR Phase II)
```

**What is true:**  
`fixtures/nv012/cop_draft.ttl`'s own header comment reads: *"Phase-I Tier-1 slice."* The notebook footer (line 1156) correctly says *"This is Phase I."* The demo is Phase I, not Phase II. The mockup is internally inconsistent with everything else in the notebook and the codebase.

**Fix:** Change `"NV012 (SBIR Phase II)"` → `"NV012 (SBIR Phase I)"`.

---

## Major Findings

### F5 — DFARS 252.204-7012 is the wrong clause number for CMMC

**Location:** `tab1_intro` callout (line 349) + `tab1_cop_sign` obligations table (line 444)

**What it says:**
```
"Every DoD contract includes DFARS 252.204-7012: 'The Contractor shall implement
NIST SP 800-171...' This boilerplate paragraph is the legal hook. It's why all
110 controls matter."
```
And in the source reference table:
```
| CMMC Level 2 required | SBIR Topic Text § 3.2, DFARS 252.204-7012 |
```

**What is true:**  
DFARS 252.204-7012 is *"Safeguarding Covered Defense Information and Cyber Incident Reporting"* — the older clause that required contractors to implement NIST SP 800-171 and report incidents. It does contain language about 800-171 implementation.

The clause that specifically mandates **CMMC Level 2** is **DFARS 252.204-7021** — *"Contractor Compliance with the Cybersecurity Maturity Model Certification Level Requirement."* This clause was added with CMMC 2.0 and is the correct legal hook for why a contractor must achieve CMMC Level 2. Contracts requiring CMMC L2 contain both clauses.

Citing only 252.204-7012 for the CMMC requirement is like citing the building code when you mean the fire marshal's permit — related, but not the direct authority.

**Fix:**  
Update both references: `DFARS 252.204-7012` → `DFARS 252.204-7012 (safeguarding/800-171) and DFARS 252.204-7021 (CMMC Level 2)`. In the obligations table source column: add `DFARS 252.204-7021` as the CMMC-specific cite.

---

### F6 — Footer: "~7 controls are machine-checked" — actual count is 6

**Location:** Footer callout, line 1162

**What it says:**
```
"Only ~7 controls are machine-checked; the rest ride on human attestation."
```

**What is true:**  
Running the engine against the `all-covered` scenario produces exactly **6 oracle outcomes**:

| Control | Outcome |
|---------|---------|
| AC.L2-3.1.1 | passed |
| IA.L2-3.5.3 | passed |
| ITAR-120.54 | passed |
| SC.L2-3.13.1 | cantTell |
| SC.L2-3.13.11 | passed |
| SC.L2-3.13.16 | passed |

Of these 6, exactly **4 are CMMC controls with passing oracles** (AC.L2-3.1.1, IA.L2-3.5.3, SC.L2-3.13.11, SC.L2-3.13.16) — matching the ACCEPTANCE.md's "4 machine / 18 human-only" finding. ITAR-120.54 is a policy-marker check, not a CMMC control. SC.L2-3.13.1 has an oracle but it returns `cantTell`.

The footer's "~7" is wrong in all interpretations:
- Oracle outcomes in the `outcomes` dict: **6** (not 7)  
- CMMC controls with passing oracles: **4** (not 7)  

The `_oracle_count` stat in Tab 2 is dynamic and correctly shows 6. The footer hardcodes "~7" and contradicts the live display.

**Fix:** Change `"~7 controls are machine-checked"` → `"~6 oracles run (4 CMMC controls pass; 2 are cantTell or non-CMMC)"`. Or simply remove the hardcoded "~7" and rely on the dynamic stat in Tab 2.

---

### F7 — Tab 2 callout: hardcoded list of machine-checked areas doesn't match oracle reality

**Location:** `tab2_factory`, the `kind="info"` callout below the evidence/oracle accordion (around line 646)

**What it says:**
```
f"Only **{_oracle_count}** controls are machine-checkable (MFA, FIPS encryption,
encryption-at-rest, unauthorized accounts, over-privileged accounts, log export,
US-region)"
```

This lists **7 areas**. The dynamic count `_oracle_count` is **6**. The two items that appear in the list but are NOT in the oracle outcomes are:
- **"over-privileged accounts"** — AC.L2-3.1.5 has no oracle criterion; it's human-attested only
- **"log export"** — AU.L2-3.3.1/2/5 have no oracle criteria; they're human-attested only

The parenthetical list is hardcoded. It describes 7 things that would be nice to machine-check but two of them aren't actually being checked. A viewer looking at the oracle outcomes table in the accordion will see that AC.L2-3.1.5 and AU.L2-3.3.x return nothing there, directly contradicting the callout.

Also note: `ITAR-120.54` appears in oracle outcomes (a policy-marker check) but is not mentioned in the callout. If you're listing what the oracle does, it should be there.

**Fix:** Update the parenthetical list to match actual oracle outcomes: `(IAM access control, MFA enforcement, FIPS-validated crypto, CUI encryption at rest, US-region policy, and ITAR US-persons check)`.

---

### F8 — "22 controls = up to 22 potential false claims" — legally inaccurate

**Location:** `tab2_attest`, False Claims Act callout (around line 720)

**What it says:**
```
"A CMMC assessment with 22 controls = up to 22 potential false claims."
```

**What is true:**  
Under 31 U.S.C. § 3729, a "claim" is a request for payment or approval submitted to the government. In a CMMC context, the **SPRS score submission** is the claim — it's one submission, not 22. Individual attestations within the self-assessment are not each "a claim" in the FCA sense; they're the substance that makes the single submission true or false.

The spirit of the warning is correct and important: attesting MET for a control you haven't satisfied creates FCA exposure. But the framing of "22 potential false claims" is legally wrong and could confuse someone who has actually read the statute. It could also seem alarmist in a way that undermines the credibility of the other warnings.

**Fix:** Replace with:
```
"A dishonest SPRS submission is one false claim to the government. The civil
penalty per claim is $13,946–$27,894 — plus treble damages on any contract funds
received while non-compliant. Each control you falsely attest MET is evidence of
that one claim's falsity."
```

---

## Minor Issues

### F9 — "the act of building the environment IS the proof" — overstated

**Location:** `tab1_intro` callout, closing sentence

**What it says:**
```
"you don't prove it separately — the act of building the environment IS the proof."
```

**What is true:**  
Building the environment is a *precondition* for proof, not proof itself. The proof is the audit chain: BOM, attestations, oracle outcomes, hashes. For 18 of the 22 covered controls, the oracle returns `cantTell` — the Affirming Official's signed attestation (Gate 2) is what makes those controls MET. A building without attestations is unproven.

The statement is a good rhetorical hook but is technically backward — the engine's whole point is that building and proving are *linked*, not that they're *identical*. It also undermines the Gate 2 and False Claims Act sections that follow.

**Fix:** `"you don't prove it separately — the act of building IS the evidence, and the evidence feeds the proof."` Or rephrase to: `"building the environment and documenting that you built it are the same action."`

---

### F10 — "contradiction — human overrules failed machine check"

**Location:** Sidebar scenario description

**What it says:**
```
"contradiction — human overrules failed machine check."
```

**What is true:**  
The human doesn't "overrule" the machine — the oracle outcome is preserved, published, and flagged. The system explicitly refuses to silently absorb the disagreement. "Overrules" implies the machine is wrong and the human wins; the actual behavior is that both positions are recorded and the contradiction is surfaced as a first-class audit finding. The SPRS score can still be 110 / Final but the audit marks it "not clean."

**Fix:** `"contradiction — human signs MET despite a failed machine check; contradiction flagged in audit."`

---

### F11 — Module list names 9 items for 10 modules

**Location:** `tab1_gate1`, Gate 1 PASS verdict text

**What it says:**
```
"The plan covers all 22 required controls with 10 modules (MFA enforcement,
encryption keys, IAM groups, DLP rules, US-region policy, audit-log export,
CSP-inherited physical controls, monitoring, and baseline Terraform config)."
```

**What is true:**  
The tier1.ttl has 10 `sysml:PartUsage` entries: `Workspace2SV_CUI_OU`, `CMEK_KeyRing`, `CUI_Users_Group`, `Drive_DLP_Rules`, `OrgPolicy_USRegion`, `AuditLog_Export`, `Disable_NonFedRAMP_Services`, `Terraform_Baseline`, `Monitoring_Alerting`, `CSP_Physical_Inheritance`. The parenthetical list has 9 items, missing `Disable_NonFedRAMP_Services` (the "disable non-FedRAMP services / least functionality" module).

**Fix:** Add `"least-functionality enforcement"` to the parenthetical, or just drop the parenthetical since the accordion below shows the full module list with hashes.

---

### F12 — FCA penalty amounts are 2024 figures

**Location:** `tab1_cop_sign` and `tab2_attest`, both cite `$13,946–$27,894`

**What is true:**  
The DOJ adjusts FCA civil penalty amounts annually in January under the Federal Civil Penalties Inflation Adjustment Act. The $13,946–$27,894 range is accurate for 2024. By mid-2026, the amounts have likely been updated once or twice (typically ~2–4% per adjustment). The 2026 floor is approximately $14,308–$14,960; ceiling approximately $28,619–$29,897 (exact amounts depend on the January 2025 and January 2026 adjustments).

The amounts in the notebook will understate the penalty exposure as time passes.

**Fix:** Add a note: `"(amounts adjusted annually by DOJ; verify current rates at 28 CFR §85.5)"`. Or update to 2026 figures when known.

---

## What Is Accurate

These frequently-scrutinized claims are correct:

- **Gate 1 three-part check** (forward / backward / untestable) — accurate against `gate1.py`
- **SPRS scoring thresholds** (110 = Final, 88–109 = Conditional, <88 = Ineligible) — accurate
- **POA&M rule** (only 1-pt controls; six excluded 1-pointers; 5-pt always invalid) — accurate
- **BOM content-addressing / tamper detection** — accurate; SHA-256 hash chain is real
- **SSP NON-EVIDENTIARY banner** — accurate; structurally non-omittable when `mock_present`
- **Contradiction behavior** (score doesn't drop; audit flags it; `110` with contradictions ≠ clean) — accurate
- **Seven factory stages** (Load → Fetch → Plan → Policy → MockApply → Evidence → Oracles) — accurate
- **Eight named graphs** — accurate; matches `LAYER_ORDER` in `_engine.py`
- **Gate 2 attestation structure** (adequacy + sufficiency justifications required) — accurate
- **`_engine.py` is clean** — all functions call real engine code; no reimplementation; no accuracy issues found
- **`README.md` is accurate** — all run instructions and structure descriptions verified

---

## Recommended Fix Priority

1. **F2** (88 controls "out of scope") — fix before any external showing; it misrepresents CMMC scope
2. **F3** (`cli.py verify` doesn't exist) — add the subcommand or label the mockup as "planned"
3. **F1** (obligations count mismatch) — fix the static text; the dynamic table already shows the truth
4. **F4** (Phase II → Phase I) — one-line fix
5. **F5** (DFARS clause number) — add 252.204-7021
6. **F7** (machine-checkable list) — update parenthetical to match oracle reality
7. **F6** (footer ~7 → 6) — update or delete the hardcoded count
8. **F8** (FCA false claims count) — fix the legal framing
9. F9–F12 — address before production use; non-blocking for demos
