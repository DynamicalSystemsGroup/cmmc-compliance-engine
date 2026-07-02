# CMMC Bidding Plan for DLA/DAF SBIR Proposals

> **Scope:** NV011 (DLA Digital Twin), NV012 (DLA Vendor Dependency), and NV018 (DAF JAG AI/ML).  
> **Requirement:** All three proposals specify **CMMC Level 2 (Self-Assessment)**.  
> **Sources verified:** 32 CFR Part 170 CMMC 2.0 Final Rule (Federal Register Docket DoD-2023-OS-0063), DFARS 252.204-7021 (Nov 2025), DFARS 252.204-7025 (Nov 2025), DFARS 252.204-7012 (May 2024), DFARS 252.204-7019/7020 (Nov 2023), NIST SP 800-171 Rev. 2.

---

## 1. What the Proposals Actually Require

| Proposal | Agency | CMMC Level | ITAR/EAR | CUI Handling | Award Timing Risk |
|----------|--------|------------|----------|--------------|-------------------|
| **NV011** | DLA | Level 2 (Self-Assessment) | Yes | CUI expected in Phase II / transition | **HIGH** — 12-month PoP spans Phase 2 (Nov 2026) |
| **NV012** | DLA | Level 2 (Self-Assessment) | Yes | CUI expected (vendor financial data, SFFAS 47) | **HIGH** — 12-month PoP spans Phase 2 |
| **NV018** | DAF | Level 2 (Self-Assessment) | Yes | IL5 platform; CUI in Phase II | **MEDIUM** — 6-month PoP may end before Phase 2, but award likely in late 2026 |

**Key contractual fact:** DFARS 252.204-7025(b)(1) states the solicitation-specified CMMC level is required **prior to award** for each contractor information system that will process, store, or transmit FCI or CUI.  
**Key timing fact:** CMMC Phase 2 begins **November 10, 2026**. After that date, most new CUI solicitations will require **Level 2 (C3PAO)** rather than Level 2 (Self). These solicitations explicitly say "Level 2 (Self-Assessment)," so they are Phase 1 solicitations.

---

## 2. What CMMC Level 2 (Self-Assessment) Means (Official)

### 2.1 Source Requirements

- **32 CFR § 170.14(c)(3):** CMMC Level 2 consists of the **110 security requirements in NIST SP 800-171 Rev. 2**.
- **32 CFR § 170.16:** Level 2 (Self) is conducted by the Organization Seeking Assessment (OSA) every 3 years, results entered into SPRS, and an affirmation is required annually after the Final CMMC Status Date.
- **DFARS 252.204-7021(d)(1):** The contractor must have and maintain a current CMMC status at the specified level (here, Level 2 (Self)) for all information systems that process, store, or transmit FCI or CUI.
- **DFARS 252.204-7021(d)(3):** Annual affirmation of continuous compliance by the affirming official in SPRS.
- **DFARS 252.204-7021(d):** The offeror must provide **CMMC Unique Identifier(s) (CMMC UIDs)** issued by SPRS for each in-scope information system.

### 2.2 Scoring Methodology

- **Starting score:** 110 points.
- **Deductions:** Each unmet requirement reduces the score by its assigned value (1, 3, or 5 points per 32 CFR § 170.24(c)(2)).
- **Final Level 2 (Self):** Score of **110** — all 110 requirements MET. Valid for 3 years.
- **Conditional Level 2 (Self):** Score of **88–109** (80% or higher) with only eligible requirements on a POA&M. Valid for **180 days**; all POA&M items must be closed and verified within 180 days or the status expires.
- **Below 88:** No CMMC status. **Not eligible for award** under a Level 2 requirement.

### 2.3 POA&M Restrictions (Critical)

Per **32 CFR § 170.21** and the CMMC Scoring Methodology:

- **Only 1-point requirements** may be placed on a POA&M.
- **3-point and 5-point requirements must be fully implemented** at the time of assessment or self-attestation.
- **Six additional 1-point requirements** are explicitly excluded from POA&M eligibility under 32 CFR § 170.21(a)(2)(iii)(A)-(F).
- **Practical result:** 63 of the 110 requirements cannot be deferred. They must be MET before SPRS submission or C3PAO engagement.

### 2.4 Non-Deferrable High-Weight Requirements (Must Be MET Before Award)

These are common failure points for cloud-only organizations:

| CMMC ID | NIST 800-171 Req | Weight | What It Requires |
|---------|------------------|--------|------------------|
| SC.L2-3.13.11 | FIPS-validated cryptography | 5 | FIPS 140-2/140-3 validated modules for CUI protection |
| IA.L2-3.5.3 | MFA for privileged access | 5 | MFA enforced for all privileged accounts |
| SC.L2-3.13.8 | Encrypt CUI in transit | 3 | FIPS-validated encryption for data in transit |
| SC.L2-3.13.16 | Encrypt CUI at rest | 3 | FIPS-validated encryption for data at rest |
| SC.L2-3.13.1 | Boundary protection | 3 | Firewalls, network segmentation |
| IA.L2-3.5.2 | MFA for local access | 3 | MFA for local access to CUI systems |
| IA.L2-3.5.4 | MFA for network access | 3 | MFA for network access to CUI systems |
| IR.L2-3.6.2 | Incident response testing | 3 | Tested incident response plan |
| CA.L2-3.12.4 | System Security Plan | 1 (excluded from POA&M) | Complete SSP documenting all 110 controls |

A handful of unmet 5-point requirements can drop a score from 110 to below 88, eliminating eligibility.

---

## 3. Additional Requirements Beyond CMMC

Because these proposals are **ITAR/EAR restricted**, CMMC is necessary but not sufficient:

1. **U.S. Person Access Controls** — ITAR-controlled technical data may only be accessed by U.S. persons unless export authorization is obtained.
2. **Work Performed in the U.S.** — DFARS/ITAR generally require all work to be performed in the United States unless a specific written exception is approved.
3. **Foreign National Restrictions** — DLA restricts foreign nationals to green card holders and dual citizens only; DAF requires disclosure of all non-U.S. citizens and permanent residents separately.
4. **Cloud Provider FedRAMP Authorization** — DFARS 252.204-7012(b)(2)(ii)(D) requires any CSP used to store, process, or transmit CUI to meet **FedRAMP Moderate baseline or equivalent**.
5. **Cage Code / SAM / UEI** — Required for DSIP submission and SPRS access.
6. **PIEE / SPRS Access** — Must request the SPRS Cyber Vendor User role and have a valid SAM registration.

---

## 4. Cloud Platform Reality Check

If DSG is currently using **Microsoft 365 Commercial**, that environment is **not acceptable** for CUI under DFARS 252.204-7012 (Microsoft 365 Commercial has lost FedRAMP status). Options:

| Platform | FedRAMP Status | CMMC Suitability |
|----------|----------------|------------------|
| **Microsoft 365 GCC High** | FedRAMP High, DoD IL5 | **Best for CUI/ITAR** — purpose-built for defense contractors |
| **Google Workspace** | FedRAMP High | **Viable** for CMMC/DFARS, but may require additional configuration (client-side encryption, org key mgmt) |
| **Microsoft 365 Commercial** | No longer FedRAMP compliant | **Not suitable** for CUI — must migrate |
| **AWS GovCloud / Azure Government** | FedRAMP High / DoD IL5 | Suitable for IaaS/PaaS hosting of CUI enclaves |

**Recommendation:** For an organization starting from zero with a cloud-only stack and ITAR exposure, **Microsoft 365 GCC High** is the lowest-risk path. It is more expensive than Google Workspace but removes the most guesswork for assessors and contracting officers.

---

## 5. The Bidding Plan: 0 → Award-Ready CMMC Level 2 (Self)

### Phase A — Pre-Submission (Complete by July 22, 2026)

These actions do not require a finished CMMC assessment but must be in progress before the proposal deadline.

| Action | Owner | Deadline | Evidence |
|--------|-------|----------|----------|
| Confirm SAM.gov registration, CAGE code, and UEI are current | Business Ops | July 8, 2026 | SAM entity record |
| Request PIEE / SPRS Cyber Vendor User role | Business Ops | July 8, 2026 | PIEE access confirmation |
| Identify the Affirming Official (senior executive) | Executive | July 8, 2026 | Internal designation memo |
| Brief Affirming Official on False Claims Act / personal liability | Legal / Compliance | July 10, 2026 | Briefing notes |
| Confirm cloud provider FedRAMP status and obtain Customer Responsibility Matrix (CRM) | IT / Security | July 12, 2026 | CRM + FedRAMP authorization letter |
| Make go/no-go decision on cloud migration (GCC High vs Google Workspace) | Executive | July 12, 2026 | Decision memo |
| Scope the CUI boundary for all three proposals: identify systems, people, data flows, and service providers | Compliance Lead | July 15, 2026 | Scope diagram, asset inventory, data flow map |
| Run an initial self-assessment against all 110 NIST SP 800-171 Rev. 2 controls using NIST SP 800-171A | Compliance Lead | July 18, 2026 | Draft SPRS score, gap list |
| Draft the System Security Plan (SSP) framework: control, implementation, responsible party, evidence, gaps | Compliance Lead | July 20, 2026 | SSP outline / draft |
| Enter CMMC status and obtain CMMC UIDs in SPRS **if score is 88+** (can be done post-submission but before award) | Affirming Official | Before award | SPRS CMMC UID(s) |
| Submit proposals to DSIP by deadline | Proposal Manager | July 22, 2026, 12:00 p.m. ET | DSIP submission confirmation |

### Phase B — Post-Submission to Award (July 22, 2026 → Award Date)

The goal is to achieve **Final Level 2 (Self)** or **Conditional Level 2 (Self)** in SPRS before award. Award timing is uncertain; plan for DAF awards ~90 days after close (~October 20, 2026) and DLA awards after the two-stage evaluation (likely November–December 2026).

| Action | Owner | Target | Notes |
|--------|-------|--------|-------|
| Finalize the SSP covering all 110 controls | Compliance Lead | Aug 15, 2026 | Must address each control, responsible party, evidence, and gap flags |
| Implement non-deferrable 5-point and 3-point controls first | IT / Security | Aug 31, 2026 | MFA everywhere, FIPS-validated encryption, org-controlled keys, tested IR plan |
| Implement remaining 1-point controls | IT / Security | Sep 30, 2026 | Policies, training, configuration baselines, access reviews |
| Build evidence library (screenshots, config exports, logs, training records, policies) | Compliance Lead | Oct 15, 2026 | Organized by control family |
| Conduct final self-assessment and calculate SPRS score | Compliance Lead | Oct 31, 2026 | Target 110; minimum 88 with POA&M |
| If score is 88–109: build a valid POA&M limited to eligible 1-point controls only | Compliance Lead | Nov 5, 2026 | 180-day clock starts at Conditional status date |
| Submit assessment results to SPRS and obtain CMMC UID(s) | Affirming Official | Nov 10, 2026 | Must be before award |
| Complete annual affirmation in SPRS | Affirming Official | Within SPRS workflow | Required for award eligibility |
| Provide CMMC UID(s) in proposal/award package as required by DFARS 252.204-7025(d) | Proposal Manager | At award | CMMC UID list |

### Phase C — After Award

| Action | Owner | Frequency | Notes |
|--------|-------|-----------|-------|
| Maintain continuous compliance | All | Ongoing | Annual affirmation; controls must stay implemented |
| Annual security awareness training | HR / Security | Annually | Required for all users with CUI access |
| Access reviews | IT / Security | Quarterly | Least-privilege verification |
| Vulnerability scans and patch management | IT / Security | Continuous | Required by NIST 800-171 SI family |
| Policy reviews | Compliance Lead | Annually | Update SSP when systems change |
| Close any open POA&M items within 180 days of Conditional status | Compliance Lead | Within 180 days | Failure to close = status expires |
| Monitor Phase 2 transition for existing contracts | Legal / Compliance | Ongoing | If options are exercised after Nov 2026, the contract may require C3PAO certification |

---

## 6. Per-Proposal Risk Notes

### NV011 & NV012 (DLA, 12 months, $100K each)

- **Highest risk:** The 12-month period of performance will almost certainly extend into **Phase 2 (Nov 10, 2026)**. Even though the solicitation says Level 2 (Self), the DLA may require C3PAO certification for option periods or if the solicitation is interpreted under Phase 2 rules.
- **Mitigation:** Achieve **Final Level 2 (Self)** before award. Simultaneously begin C3PAO readiness planning in case the contract transitions to C3PAO requirements. Book a C3PAO assessment slot early (current lead time: 6–9 months).
- **CUI exposure:** Phase II of these SBIRs likely involves DLA data/systems integration. Treat the CUI boundary as expanding over the contract lifecycle.

### NV018 (DAF, 6 months, $250K)

- **Medium risk:** The 6-month PoP may complete before Phase 2 if awarded promptly, but DAF awards are expected ~90 days after close (around October 2026). Performance would then run through early 2027, crossing Phase 2.
- **Mitigation:** Achieve Final Level 2 (Self) before award. The DAF proposal is evaluated on written merit only, so there is no oral presentation buffer time to fix CMMC gaps.
- **IL5 requirement:** The topic explicitly requires an IL5-compliant platform. GCC High or a FedRAMP High/DoD IL5 environment is effectively mandatory, not optional.

---

## 7. Decision Tree: Self-Assessment vs. C3PAO

```
Solicitation says "Level 2 (Self-Assessment)"
│
├─ Award occurs before Nov 10, 2026? 
│  ├─ YES → Level 2 (Self) sufficient for award
│  └─ NO  → Verify with Contracting Officer; Phase 2 may require C3PAO
│
├─ Contract extends into Phase 2 (Nov 2026+)?
│  ├─ YES → Plan for C3PAO certification regardless of initial self-assessment
│  └─ NO  → Self-assessment may suffice for full PoP
│
└─ Score < 88 on self-assessment?
   ├─ YES → Not eligible for award
   └─ NO  → Final (110) or Conditional (88-109) status accepted, subject to POA&M rules
```

---

## 8. Cost and Timeline Estimate

For a small business starting from zero with a cloud-only environment:

| Phase | Duration | Estimated Cost |
|-------|----------|----------------|
| Gap assessment + SSP drafting | 4–6 weeks | $3K–$15K |
| Remediation (MFA, encryption, logging, IR, policies) | 8–12 weeks | $10K–$50K |
| Self-assessment, SPRS submission, affirmation | 2–4 weeks | Internal labor + possible consultant |
| **Total to Level 2 (Self)** | **3–5 months** | **$15K–$65K** |
| C3PAO certification (if needed) | +2–4 months | +$30K–$75K |
| Annual maintenance | Ongoing | $20K–$40K/year |

This is significantly lower than the full C3PAO path because the solicitations currently allow self-assessment. However, if any of these contracts transition to Phase 2, the C3PAO cost must be added.

---

## 9. Free Federal Resources to Use First

Before spending on consultants, exhaust these:

- **APEX Accelerators** — free CMMC counseling for small defense contractors: `apexaccelerators.us`
- **Project Spectrum** — DoD-funded tools, training, and assessments: `projectspectrum.io`
- **NIST MEP Centers** — subsidized CMMC support for manufacturers: `nist.gov/mep`
- **NIST SP 800-171 Rev. 2** (official): `nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r2.pdf`
- **NIST SP 800-171A** (assessment guidance): `csrc.nist.gov/publications/detail/white-paper/2018/06/01/assessing-cui/nist-sp-800-171a`
- **Cyber AB Marketplace** — find authorized C3PAOs: `cyberab.org`
- **NARA CUI Registry**: `archives.gov/cui`

---

## 10. Immediate Next Steps (This Week)

1. **Confirm SAM/UEI/CAGE are active** and request PIEE/SPRS access.
2. **Designate the Affirming Official** and brief them on legal liability.
3. **Make the cloud decision:** GCC High vs Google Workspace. If M365 Commercial is in use, a migration is required before CUI handling.
4. **Draft the CUI boundary** for all three proposals on a single page.
5. **Run a free self-assessment against the 110 controls** to get a baseline SPRS score.
6. **Identify all 5-point and 3-point gaps** and assign owners.
7. **Engage an RPO or CMMC consultant** if the gap assessment shows a score below 88.
8. **Schedule a C3PAO assessment slot** now if there is any chance Phase 2 requirements will apply (likely for DLA contracts).

---

## 11. Official Source Citations

| Source | URL / Reference | Used For |
|--------|-----------------|----------|
| 32 CFR Part 170 CMMC 2.0 Final Rule | `public-inspection.federalregister.gov/2024-22905.pdf` | Level definitions, scoring, POA&M rules, affirmation requirements |
| DFARS 252.204-7021 | `acquisition.gov/dfars/part-252-solicitation-provisions-and-contract-clauses` (section 252.204-7021) | Contractor CMMC status, UID, flowdown, affirmation requirements |
| DFARS 252.204-7025 | Same as above, section 252.204-7025 | Solicitation notice requirements, pre-award CMMC status |
| DFARS 252.204-7012 | Same as above, section 252.204-7012 | NIST 800-171, cloud FedRAMP, cyber incident reporting |
| DFARS 252.204-7019/7020 | Same as above, sections 252.204-7019/7020 | NIST 800-171 assessment requirements and SPRS posting |
| NIST SP 800-171 Rev. 2 | `nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r2.pdf` | The 110 security requirements |
| NIST SP 800-171A | `csrc.nist.gov/publications/detail/white-paper/2018/06/01/assessing-cui/nist-sp-800-171a` | Assessment objectives and methods |

---

*Plan generated from official DoD/NIST sources. This is research, not legal advice; confirm all interpretations with your contracting officer and legal counsel.*
