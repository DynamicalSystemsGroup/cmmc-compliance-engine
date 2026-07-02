# CMMC 2.0 Level 2: 0 → 100% Compliance Roadmap

> Research findings compiled from DoD source material, CMMC practitioners, C3PAO guidance, and compliance vendors as of mid-2026.  
> This document is designed to complement your COO’s outline and provide concrete next steps for an organization starting from zero with a cloud-first environment.

---

## 1. Executive Summary

CMMC 2.0 Level 2 applies to any DoD contractor that handles **Controlled Unclassified Information (CUI)**. It is built on the **110 security requirements of NIST SP 800-171 Rev. 2**, organized into 14 control families. There is no “audit” separate from these 110 controls; the entire program is a verification mechanism layered on top of requirements that have been contractually mandated since 2017 through DFARS 252.204-7012.

For an organization starting from zero—especially a small, cloud-only team—the path is manageable but it is a project, not a form. The most important facts:

- **Phase 1 (now through Nov 9, 2026):** “Level 2 (Self)” is still valid in some solicitations.
- **Phase 2 (begins Nov 10, 2026):** Mandatory **C3PAO certification** replaces self-attestation for most CUI contracts.
- **Honest timeline:** 6–12 months from standing start to assessment readiness; 9–12 months is the conservative planning estimate.
- **Honest budget:** $50,000–$200,000+ all-in for a first Level 2 C3PAO certification; the C3PAO fee itself is often the third-largest cost after remediation and documentation.
- **C3PAO scarcity:** roughly 83 authorized C3PAOs serving more than 118,000 contractors; slots are already booking 6–9 months out.
- **Legal risk:** the Affirming Official certifies the accuracy of the SPRS score under False Claims Act exposure, including treble damages on affected contracts.

The single highest-leverage decision is **scoping the CUI boundary aggressively**. A cloud-only environment with a small team is easier to scope and control than a large on-premise footprint, but you still must build the documentation, policies, and evidence from scratch.

---

## 2. The CMMC 2.0 Timeline (Four Phases)

| Phase | Dates | What Changes |
|-------|-------|--------------|
| **Phase 1** | Nov 10, 2025 – Nov 9, 2026 | New contracts require Level 1 self-assessment for FCI and Level 2 self-assessment for many CUI contracts. High-priority CUI contracts may already require C3PAO. |
| **Phase 2** | **Nov 10, 2026** | **Level 2 C3PAO certification becomes mandatory for most CUI contracts.** Self-attestation alone is no longer sufficient for the majority of CUI solicitations. |
| **Phase 3** | Nov 10, 2027 | Level 2 C3PAO certification required for option periods/renewals of contracts awarded after Nov 2025. Level 3 DIBCAC assessments begin for highest-sensitivity programs. |
| **Phase 4** | Nov 10, 2028 | Full implementation across all applicable DoD acquisitions. No waivers, no grace periods. |

**Strategic implication:** Primes are already screening subcontractors by CMMC posture before Phase 2. A low or missing SPRS score can cause a subcontractor to be quietly delisted from bid packages even before the formal deadline.

---

## 3. The 0 → 100% Roadmap at a Glance

1. **Read your contracts** — identify DFARS clauses 252.204-7021, 7019, 7020, 7012.
2. **Define scope** — map every system, process, person, and service provider that touches CUI.
3. **Build the System Security Plan (SSP)** — document all 110 controls, responsible parties, evidence, and gaps.
4. **Run a gap assessment** — use Examine, Interview, Test against all 110 controls.
5. **Calculate SPRS score** — 110 = Final; 88–109 = Conditional (180 days); <88 = No CMMC Status.
6. **Build the POA&M** — only for eligible 1-point gaps; 3-point and 5-point controls must be met before attestation.
7. **Remediate** — prioritize high-weight controls, implement technical controls, generate evidence.
8. **Submit to SPRS** — enter the Level 2 self-assessment (now) or obtain C3PAO certification (Phase 2).
9. **Annual affirmation** — senior executive reaffirms compliance; evidence is kept continuously current.
10. **Maintain / recertify** — certification is valid 3 years; reassessment required at the end of the cycle.

---

## 4. Step 1: Read the Contract and Determine the Required Level

Before spending money, confirm exactly what the contract requires.

### Key DFARS Clauses to Find

| Clause | Meaning |
|--------|---------|
| **DFARS 252.204-7021** | The CMMC clause. Specifies Level 1, Level 2 (Self), or Level 2 (C3PAO). |
| **DFARS 252.204-7019** | Requires an NIST 800-171 self-assessment and SPRS score; predecessor to 7021. |
| **DFARS 252.204-7020** | Requires a current SPRS score to be provided to the contracting officer. |
| **DFARS 252.204-7012** | “Safeguarding Covered Defense Information.” If present, you handle CUI and must implement the 110 controls. |

### Level Determination

- **Level 1** — only Federal Contract Information (FCI). 15 practices from FAR 52.204-21. Self-assessed annually. No POA&Ms allowed. Pass/fail.
- **Level 2** — CUI is involved. 110 NIST SP 800-171 Rev. 2 controls. Either self-assessment (non-prioritized CUI outside the Defense Organizational Index Grouping) or C3PAO certification (most defense CUI contracts).
- **Level 3** — highest-sensitivity programs, adds NIST SP 800-172 requirements. Government-led DIBCAC assessment. Rare for small contractors.

**Planning assumption:** if your contract involves CUI and is in the defense supply chain, plan for **Level 2 C3PAO certification** unless the solicitation explicitly says “Level 2 (Self)” and you are confident it will not extend into Phase 2.

### Flow-Down from Primes

Prime contractors must flow CMMC requirements to subcontractors handling FCI or CUI. A prime with Level 2 (C3PAO) will require a CUI subcontractor to also hold Level 2 (C3PAO). You cannot bid on subcontracts requiring Level 2 without the certification already in hand.

---

## 5. Step 2: Define the CUI Scope

Scoping is the highest-leverage activity in the entire program. The scope defines which systems, people, data flows, and facilities are assessed.

### Asset Categories to Document

| Category | Definition | Assessment Treatment |
|----------|------------|----------------------|
| **CUI Assets** | Process, store, or transmit CUI. | Fully in scope; all controls apply. |
| **Security Protection Assets** | Provide security functions (firewall, SIEM, EDR, IDP) but do not hold CUI. | In scope; assessed for their security function. |
| **Contractor Risk Managed Assets** | Could interact with CUI but are prevented by policy/technical controls. | Documented and risk-managed; limited assessment. |
| **Specialized Assets** | IoT, OT, lab equipment, etc. | Risk-based documentation; may be scoped narrowly. |
| **Out-of-Scope Assets** | No CUI interaction, no security function. | Explicitly excluded with justification. |

### Scope-Reduction Tactics

- **CUI Enclave:** isolate all CUI processing into a single logical environment (e.g., a dedicated tenant, VPC, or managed enclave). This can reduce in-scope systems by 60% or more.
- **Cloud-first architecture:** a cloud-only environment is generally easier to scope and control than on-premise infrastructure.
- **Limit data copies:** restrict downloads, local storage, email forwarding, and removable media for CUI.
- **Document everything:** the SSP is the boundary document. Undocumented assets do not get the benefit of inherited controls.

### Critical Evidence to Produce

- Network diagrams showing CUI boundaries and data flows.
- Asset inventory with CUI classification.
- Data flow diagrams: CUI entry points, movement, storage, and exit paths.
- List of service providers and their FedRAMP / CMMC status.

---

## 6. Step 3: Build the System Security Plan (SSP)

The SSP is the core document. It is what a C3PAO reads first and what a contracting officer expects to exist.

### What the SSP Must Cover

For each of the 110 NIST SP 800-171 Rev. 2 controls, the SSP should include:

1. **Control statement** — the requirement text.
2. **Implementation description** — how the control is implemented in your environment.
3. **Responsible party** — name/role accountable for the control.
4. **Evidence references** — policies, configuration screenshots, logs, diagrams, training records, vendor attestations.
5. **Gap flag** — if not fully implemented, identify it and link to the POA&M.

### Additional SSP Content

- System description and mission.
- CUI boundary and scope.
- Network architecture and data flows.
- Inventory of systems, software, and services.
- Roles and responsibilities.
- Risk assessment methodology.
- Continuous monitoring strategy.
- Incident response capabilities.
- Policy cross-reference matrix.

### Controls Marked “Not Applicable”

Any control deemed not applicable requires a written justification explaining why it does not apply to the scoped environment. “We are a cloud company” is not enough; the justification must tie to the specific architecture.

### SSP Maintenance

The SSP is a living document. Major changes (new systems, new CUI flows, new vendors, new locations) require updates. At minimum, conduct a full review every three years.

---

## 7. Step 4: Run a Gap Assessment Against All 110 Controls

A gap assessment is a structured evaluation of the current state against the 110 controls. It is not a pass/fail exercise; it is the baseline that determines budget, timeline, and remediation priority.

### The Three DoD-Approved Assessment Methods

| Method | What It Means | Example Evidence |
|--------|---------------|------------------|
| **Examine** | Review documentation, configurations, policies, records. | SSP, screenshots, config exports, policy documents, network diagrams. |
| **Interview** | Speak with responsible personnel to confirm understanding and execution. | Recorded interviews, attestations, meeting notes. |
| **Test** | Validate technical configurations through observation or tooling. | Vulnerability scans, log queries, MFA configuration checks, access reviews. |

### Assessment Objectives

Each of the 110 controls expands into multiple assessment objectives in NIST SP 800-171A. A control is scored **MET** only when all objectives supporting it are satisfied. Partial implementation is useful for internal planning but does not count toward certification.

### Typical Starting Point for Cloud-First Small Organizations

Starting from zero, a small cloud-based organization will often score in the **60–85 range** on a first self-assessment. This is normal. The most common gaps are:

- Multi-factor authentication not rigorously enforced everywhere.
- Audit logging and monitoring insufficient or not centralized.
- Incident response plan exists on paper but has not been tested.
- Configuration management baselines and change control missing.
- Media protection policies undefined or unenforced.
- FIPS-validated encryption not documented.
- Key management not under organizational control.

### Recommended Approach

- Use a free or paid self-assessment tool first to estimate the SPRS score and identify top gaps.
- If budget allows, engage a CMMC Registered Provider Organization (RPO) or consultant for a validated gap assessment.
- Do not remediate blindly; prioritize by SPRS point weight and business impact.

---

## 8. Step 5: Understand SPRS Scoring and POA&M Rules

### SPRS Score Calculation

The Supplier Performance Risk System (SPRS) is the DoD’s central database for contractor cybersecurity posture. The score is calculated from the NIST 800-171 assessment:

- **Baseline:** 110 points (perfect compliance).
- **Deductions:** 1, 3, or 5 points per unmet control, depending on the control’s security weight.
- **Starting from scratch with no controls:** can score approximately **-203**.

### Score Thresholds and Status

| Score | Status | Validity | Meaning |
|-------|--------|----------|---------|
| **110** | Final Level 2 | 3 years | All 110 controls MET. Full contract eligibility. Annual affirmation required. |
| **88–109** | Conditional Level 2 | 180 days | Eligible for award, but all POA&M gaps must be closed within 180 days. |
| **<88** | No CMMC Status | — | Not eligible for CUI contracts. |

### POA&M Eligibility Rules (Critical)

- **Only 1-point controls** can be deferred to a POA&M.
- **3-point and 5-point controls must be fully implemented** before assessment or attestation.
- **Six additional 1-point controls** are explicitly excluded from POA&M eligibility under 32 CFR 170.21(a)(2)(iii)(A)-(F).
- **Practical result:** **63 of the 110 controls cannot be deferred.** They must be done before the C3PAO arrives or before you self-attest.
- **POA&M closeout:** every item must be remediated and verified within **180 days** of receiving Conditional status. The same C3PAO must verify closeout.

### High-Impact Non-Deferrable Controls

These are the highest-weight and most commonly failed controls:

- **SC.L2-3.13.11** — FIPS 140-2/140-3 validated cryptography for CUI protection (5-point).
- **SC.L2-3.13.8 / 3.13.16** — encrypt CUI in transit and at rest (3-point).
- **IA.L2-3.5.3** — multi-factor authentication for privileged access (5-point).
- **IA.L2-3.5.2 / 3.5.4** — MFA for local / network access (3-point).
- **IR.L2-3.6.2** — incident response plan tested (3-point).
- **AC.L2-3.1.20 / 3.1.22** — specific access controls (non-deferrable).
- **CA.L2-3.12.4** — the SSP itself must be complete (non-deferrable).
- **All Physical Protection (PE) controls** — PE.L2-3.10.3 through 3.10.5 (non-deferrable).

A few missing 5-point controls can drop a score from 110 to below 88. For example, five 5-point controls and three 3-point controls unmet = 34 points deducted, leaving a score of 76—**below the conditional floor**.

---

## 9. Step 6: Remediate and Generate Evidence

### Remediation Priority Order

1. **High-weight non-deferrable controls** (5-point and 3-point) first.
2. **The six excluded 1-point controls** and the SSP completeness control.
3. **Foundation controls** that enable other controls: identity, logging, patching, configuration baselines.
4. **Remaining 1-point gaps** that can be deferred if needed.

### Common Remediation Areas for Cloud-Only Organizations

#### Identity and Access
- Enforce MFA on all CUI systems, all privileged accounts, and all remote access.
- Eliminate shared accounts and service accounts with weak credentials.
- Implement least privilege and role-based access control.
- Conduct access reviews quarterly.

#### Encryption and Key Management
- Use **FIPS 140-2/140-3 validated** cryptographic modules.
- Encrypt CUI at rest and in transit.
- Maintain **organizational control** of encryption keys; avoid provider-managed keys where the provider can decrypt your data without your authorization.
- Document CMVP certificate numbers for all modules protecting CUI.

#### Logging and Monitoring
- Centralize logs from all CUI systems and security tools.
- Ensure log integrity and tamper protection.
- Synchronize clocks to authoritative time sources.
- Retain logs for investigation and incident response.

#### Incident Response
- Document an incident response plan with roles, escalation, and containment steps.
- Conduct at least one tabletop exercise or simulation before assessment.
- Establish a 72-hour reporting path to DoD for CUI-related cyber incidents.
- Preserve forensic evidence for at least 90 days.

#### Configuration Management
- Document baseline configurations for all systems in scope.
- Implement a change control process with approval, testing, and rollback steps.
- Track all changes and review them regularly.

#### Media Protection
- Define acceptable and unacceptable media for CUI.
- Sanitize media before disposal or reuse.
- Mark and control physical and digital media containing CUI.

### Evidence Collection

Assessors grade evidence, not intent. Build an evidence library as you go:

- Configuration screenshots and exports.
- Policy documents with version control and approval dates.
- Training completion records.
- Access review logs.
- Vulnerability scan and patch reports.
- Incident response exercise records.
- Vendor contracts and FedRAMP authorization letters.
- Network diagrams and data flow maps.

---

## 10. Step 7: Cloud Provider Considerations

A cloud-only environment does not automatically satisfy CMMC. The cloud provider covers some controls, but you must document which ones are inherited and ensure the provider is authorized.

### Cloud Platform Comparison

| Platform | FedRAMP Status | CMMC Suitability |
|----------|----------------|------------------|
| **Microsoft 365 Commercial** | No longer FedRAMP compliant | **Not suitable** for CUI/DFARS. Must migrate. |
| **Microsoft 365 GCC High** | FedRAMP High, DoD IL5 | **Gold standard** for CUI/ITAR. Most straightforward. |
| **Google Workspace** | FedRAMP High | **Suitable** for CMMC/DFARS with proper configuration and gap closure. Can inherit IL4 controls via Google Assured Workloads. |
| **AWS GovCloud / Azure Government** | FedRAMP High / DoD IL5 | Suitable for IaaS/PaaS hosting of CUI environments. |

### Key Rule

DFARS 252.204-7012 requires any cloud service used to store, process, or transmit defense information to be **FedRAMP Moderate authorized or equivalent**. For CUI, FedRAMP High is the safer posture.

### Inherited Controls

Cloud providers publish customer responsibility matrices and System Security Plans (SSPs) under NDA. You must:

- Identify which controls the provider inherits.
- Identify which controls remain your responsibility.
- Document the provider’s FedRAMP authorization and scope.
- Confirm the provider’s controls actually cover the services you use (not all service tiers are in the same authorization boundary).

### Important Caveat for Google Workspace

Google Workspace can meet CMMC/DFARS requirements, but gaps often require manual configuration or third-party tools. For example, client-side encryption and organizational key management may be needed to satisfy high-weight encryption controls.

---

## 11. Step 8: Submit to SPRS (Self-Assessment Path)

For contracts still eligible for Level 2 (Self) in Phase 1, submission is done through the **Procurement Integrated Enterprise Environment (PIEE)**.

### Prerequisites

- Valid SAM.gov registration and current CAGE code.
- PIEE account with the **SPRS Cyber Vendor User** role.
- Completed SSP.
- Calculated SPRS score and POA&M (if applicable).

### Submission Steps (Level 2 Self)

1. Request PIEE access at `sprs.csd.disa.mil/access.htm`.
2. Log in to PIEE at `piee.eb.mil` and select **SPRS → Cyber Reports**.
3. Select your CAGE hierarchy and click **Run Cyber Reports**.
4. In the **CMMC Assessments / CMMC Level 2 (Self)** tab, select **Add New Level 2 CMMC Self-Assessment**.
5. Enter compliance status for each of the 110 requirements. Click **Requirement Objectives** for detailed guidance per requirement.
6. Navigate through each requirement family using **Save and Continue**.
7. Add assessing scope, employee count, and included CAGEs.
8. Review your score. If 88 or above, proceed to affirmation.
9. Affirm or transfer to the **Affirming Official (AO)**.

### Affirmation

The AO must be a senior executive who can certify the accuracy of the score. The affirmation is a legal statement. Under the **False Claims Act**, an inaccurate score—even unintentional—can expose the organization and the individual to significant liability, including treble damages.

---

## 12. Step 9: C3PAO Certification Path (Phase 2 and Beyond)

For most CUI contracts starting November 10, 2026, a C3PAO certification is required.

### What a C3PAO Does

A Certified Third-Party Assessment Organization (C3PAO) is authorized by the Cyber AB to conduct independent CMMC Level 2 assessments. The C3PAO:

- Reviews the SSP and evidence.
- Interviews personnel.
- Tests technical controls.
- Enters results into the DoD’s eMASS system, which feeds SPRS.
- Issues a Certificate of CMMC Status valid for **3 years** (if all controls are met or conditional status is achieved).

### Before Booking a C3PAO

Do not engage a C3PAO until the following are complete:

- SSP is finalized and assessable.
- All 63 non-deferrable controls are implemented and evidenced.
- SPRS score is 88 or above on internal assessment (ideally 110).
- POA&M is limited to eligible 1-point gaps only.
- Staff has been trained and can articulate security processes.
- Evidence is organized and accessible.

### Booking Timeline

Because of assessor scarcity, **book the C3PAO slot before you feel ready**. A typical reservation requires evidence of meaningful progress, but you do not need to be at 110. Waiting until you are “ready” often means missing the Phase 2 deadline.

### Assessment Duration

Expect a **60–120 day** assessment window from kickoff to certification decision, plus the time required to schedule the engagement.

### Closeout for Conditional Status

If you receive Conditional status (88–109), you have **180 days** to:

1. Close every POA&M item.
2. Complete a closeout assessment with the same C3PAO.
3. Achieve Final CMMC Status.

If the closeout is not completed within 180 days, the Conditional status expires.

---

## 13. Cost and Timeline Estimates

### Realistic Timeline

| Phase | Duration | Notes |
|-------|----------|-------|
| Contract review & scoping | 2–4 weeks | Define CUI boundary before any remediation. |
| Gap assessment | 3–6 weeks | Internal or consultant-led. |
| SSP & documentation | 4–8 weeks | Parallel with remediation. |
| Remediation (high-priority) | 2–4 months | MFA, encryption, logging, IR, config management. |
| Mock assessment & evidence prep | 3–4 weeks | Catch gaps between “we do it” and “we can prove it.” |
| C3PAO engagement | 2–4 months | Includes scheduling, evidence review, interviews, testing. |
| **Total from standing start** | **6–12 months** | Conservative plan: 9–12 months. |

### Realistic Cost Breakdown (Level 2 C3PAO)

| Cost Category | Typical Range |
|---------------|---------------|
| Gap assessment | $3,500–$20,000 |
| Remediation & implementation | $10,000–$150,000 |
| Documentation (SSP, POA&M, policies) | $12,000–$60,000 |
| C3PAO assessment | $30,000–$75,000 |
| Technology & tooling | $10,000–$50,000 |
| Consulting / vCISO | $15,000–$40,000 |
| Training | $2,000–$10,000 |
| **Total first year** | **$50,000–$200,000+** |
| Annual maintenance | $20,000–$40,000 |

The DoD’s published estimate of $104,670–$118,000 is for the **assessment alone**, not the full compliance program. Small contractors often spend $98,000–$305,000 in the first year when starting from a low baseline.

### Three Paths to Compliance

| Approach | Total Cost | Timeline | Best For |
|----------|------------|----------|----------|
| Full-service consultant | $75K–$200K+ | 6–12 months | Budget available, no internal expertise. |
| Platform + DIY | $15K–$75K | 6–18 months | Some IT knowledge, budget pressure. |
| Pure DIY | $5K–$30K | 12–24 months | Strong internal IT, very tight budget. |

Most small contractors use a hybrid: DIY the straightforward controls, use a platform for tracking, and bring in a consultant for scoping, SSP, or assessment prep.

---

## 14. Free and Low-Cost Resources

Before paying for private consulting, exhaust these federal resources:

- **APEX Accelerators** — free advisory services for small defense contractors. Find your office at `apexaccelerators.us`.
- **Project Spectrum** — DoD-funded cybersecurity tools, training, and assessments for small DIB businesses. `projectspectrum.io`.
- **NIST MEP Centers** — hands-on CMMC support, often subsidized for manufacturers. `nist.gov/mep`.
- **NIST SP 800-171 Rev. 2** — official publication. `nvlpubs.nist.gov`.
- **Cyber AB Marketplace** — find authorized C3PAOs and RPOs. `cyberab.org`.
- **NARA CUI Registry** — official CUI categories and markings. `archives.gov/cui`.

---

## 15. Common Pitfalls and How to Avoid Them

| Pitfall | Why It Happens | How to Avoid |
|---------|----------------|--------------|
| **Over-scoping** | Treating the whole company as CUI in scope. | Build a CUI enclave; document only what touches CUI. |
| **Under-scoping** | Missing CUI copies on laptops, email, or cloud sync. | Map all data flows; restrict downloads and forwarding. |
| **Assuming the cloud provider handles CMMC** | Not documenting inherited controls and customer responsibilities. | Get the provider’s responsibility matrix and FedRAMP letter. |
| **MFA not everywhere** | Deployed for some systems but not all CUI systems. | Enforce MFA on all CUI access and privileged access. |
| **FIPS encryption not documented** | Using “encryption” without validated modules. | Identify CMVP certificate numbers and FIPS-approved modes. |
| **Incident response plan on paper only** | No exercise or reporting procedure. | Conduct a tabletop exercise; document the 72-hour DoD reporting path. |
| **POA&M abuse** | Trying to defer 3-point or 5-point controls. | Only defer eligible 1-point controls; close all others before assessment. |
| **Evidence collected last minute** | No continuous evidence library. | Build evidence as you implement; organize by control family. |
| **Waiting to book a C3PAO** | Thinking you must be “ready” first. | Book early; use lead time to finish remediation. |
| **Inflating the SPRS score** | Pressure to bid or win. | Score honestly; False Claims Act exposure is real. |

---

## 16. Quick-Start Checklist for the Next 90 Days

Use this if you are starting from zero today:

- [ ] Pull all active contracts and identify DFARS 252.204-7021, 7019, 7020, 7012.
- [ ] Determine if the contract is FCI only or CUI, and whether it says “Level 2 (Self)” or “Level 2 (C3PAO).”
- [ ] Map the CUI boundary: systems, people, data flows, vendors, locations.
- [ ] Run a free or paid gap assessment against all 110 NIST SP 800-171 Rev. 2 controls.
- [ ] Calculate an estimated SPRS score.
- [ ] Identify all 5-point and 3-point gaps and create a remediation plan for them first.
- [ ] Validate your cloud provider’s FedRAMP status and inherited controls.
- [ ] Start drafting the SSP with the 110 controls, responsible parties, and evidence references.
- [ ] Enforce MFA on all CUI and privileged access.
- [ ] Begin centralizing logging and establish a log retention policy.
- [ ] Draft an incident response plan and schedule a tabletop exercise.
- [ ] If Phase 2 applies, contact at least 3 C3PAOs for scheduling and pricing.
- [ ] Identify the Affirming Official and brief them on legal liability.

---

## 17. Sources and Further Reading

This document synthesizes the following sources:

- DoD CMMC 2.0 Final Rule (32 CFR Part 170) and DFARS 48 CFR Acquisition Rule.
- DoD CIO CMMC guidance: `dodcio.defense.gov/CMMC/about/`.
- NIST SP 800-171 Rev. 2: `nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r2.pdf`.
- NARA CUI Registry: `archives.gov/cui`.
- SPRS Quick Entry Guide Version 4.0 (February 2025).
- Cyber AB Marketplace: `cyberab.org`.
- Practitioner guidance from Torchsec, Free Gap Assessment, Kyberstorm, Elevate Consult, Theodosian, CMMCGap, Secureframe, BEMO, and others.

**Note:** CMMC is a rapidly evolving regulatory program. Verify all deadlines, fee schedules, and technical requirements with the DoD, NIST, Cyber AB, and your contracting officer before making final decisions.

---

*Document compiled for internal planning. This is research, not legal or compliance advice.*
