---
title: "Path to CMMC Level 2 Self-Assessment — NV012"
type: plan
status: active
date: 2026-07-03
---

# Path to CMMC Level 2 Self-Assessment

**Objective:** Take the compliance engine from its current Phase I / Tier 1 demo (22 controls)
to a completed, submittable CMMC Level 2 self-assessment covering all 110 NIST SP 800-171 controls
before contract award on DLA26BZ03-NV012.

**Current state at plan creation:**
- Engine: 293 tests passing; Gate 1 / Gate 2 / SPRS / SSP / BOM all working
- Coverage: 22 of 110 controls in `structural/tier1.ttl`; evidence is fixture-backed (mock)
- All output is NON-EVIDENTIARY by design — not submittable yet

---

## The Three Tracks

Every remaining control falls into exactly one of three tracks. The tracks run in parallel
after their prerequisites are met. Nothing blocks starting all three today.

| Track | Controls | Engine work | Org work |
|-------|----------|-------------|----------|
| **A — Expand machine coverage** | ~44 controls | New modules + evidence generators + oracle criteria | Configure the GCP/Workspace controls they verify |
| **B — Human attestation program** | ~44 controls | New policy-module entries in structural layer; attestation records | Write policies, implement procedures, collect evidence |
| **C — Live evidence integration** | All 110 | Replace mock fixtures with real GCP/Workspace API calls | Grant API service account access to production project |

The intersection is Gate 2: every control, machine-verified or not, requires an Affirming
Official to attest MET. Track A makes that attestation defensible with machine evidence;
Track B makes it defensible with policy evidence. Track C makes it real.

---

## Track A — Expand Machine Coverage

### What this means in the engine

For each new control, three files need updating:

1. **`structural/tier1.ttl`** — add a `sysml:PartUsage` entry claiming the control with a
   machine oracle IRI (`cmmc:verificationMethod ce:oracle-<slug>`)
2. **`evidence/generators/`** — add or extend a generator that queries the real GCP/Workspace
   API for the relevant config key
3. **`oracles/criteria.py`** — add a `CRITERIA` entry that maps the evidence keys to a
   pass/fail decision

One new generator can claim multiple controls (e.g., a single `WorkspaceAdminGenerator` that
pulls the full admin policy object can feed IA.3.5.5 through IA.3.5.11).

### New modules to add (by GCP/Workspace service)

#### Module: `VPNAccess_BeyondCorp` — Remote access controls
Claims: AC.L2-3.1.12, AC.L2-3.1.13, AC.L2-3.1.14, AC.L2-3.1.15
- GCP source: BeyondCorp Enterprise / Cloud VPN config export
- Oracle: verify remote sessions route through managed proxy; TLS enforced; no split tunnel
- AC.3.1.15 (authorize privileged commands remotely) → `cmmc:verificationMethod "manual:remote-access-policy"` — requires a policy document

#### Module: `WorkspaceAdmin_Policy` — Identity lifecycle + password controls
Claims: IA.L2-3.5.1, IA.L2-3.5.5, IA.L2-3.5.6, IA.L2-3.5.7, IA.L2-3.5.8, IA.L2-3.5.9, IA.L2-3.5.10, IA.L2-3.5.11
- GCP source: Workspace Admin SDK `GET /admin/directory/v1/customer/{customerId}/policies`
- Oracle: verify identifier reuse period ≥ 90 days; inactive accounts disabled after ≤ 30 days;
  password complexity/history enforced; temporary passwords expire at first use; stored hashed
- IA.3.5.11 (obscure auth feedback) → `cmmc:verificationMethod "manual:ui-review"` — visual check only

#### Module: `OrgPolicy_SessionControl` — Session lock + termination
Claims: AC.L2-3.1.10, AC.L2-3.1.11
- GCP source: Cloud Identity session duration policy
- Oracle: verify idle session timeout ≤ 15 minutes; session termination conditions configured

#### Module: `AccessTransparency_ExternalSystems` — External connections
Claims: AC.L2-3.1.20
- GCP source: VPC Service Controls perimeter config export
- Oracle: verify external system connections enumerated and authorized

#### Module: `ChangeManagement_GitHub` — Change control
Claims: CM.L2-3.4.3, CM.L2-3.4.5
- Source: GitHub branch protection rules API (`GET /repos/{owner}/{repo}/branches/{branch}/protection`)
- Oracle: verify required reviews ≥ 1; force push blocked; change log entries exist per commit

#### Module: `OrgPolicy_Allowlist` — Software allowlisting
Claims: CM.L2-3.4.8, CM.L2-3.4.9
- GCP source: Binary Authorization policy + Container Analysis config
- Oracle: verify deny-by-default image policy active; user software approval workflow documented

#### Module: `CloudLogging_Config` — Audit log integrity
Claims: AU.L2-3.3.4, AU.L2-3.3.7, AU.L2-3.3.8, AU.L2-3.3.9
- GCP source: Cloud Logging sinks + NTP config + IAM on log buckets
- Oracle: log failure alerting policy exists; NTP sources configured; log bucket access restricted

#### Module: `SecurityCommandCenter` — Vulnerability management
Claims: RA.L2-3.11.2, SI.L2-3.14.1, SI.L2-3.14.5
- GCP source: Security Command Center findings export
- Oracle: scan last run within 30 days; critical/high findings have remediation dates

#### Module: `EndpointVerification_CrowdStrike` — Malware + endpoint integrity
Claims: SI.L2-3.14.2, SI.L2-3.14.4, SI.L2-3.14.7
- Source: CrowdStrike Falcon API (or equivalent EDR) sensor status export
- Oracle: verify AV definitions updated within 24h; all managed endpoints covered; anomaly
  detection active

#### Module: `VPC_Segmentation` — Network architecture
Claims: SC.L2-3.13.3, SC.L2-3.13.4, SC.L2-3.13.5, SC.L2-3.13.6, SC.L2-3.13.7,
        SC.L2-3.13.8, SC.L2-3.13.9, SC.L2-3.13.15
- GCP source: VPC network config + firewall rules export + Cloud Armor policy
- Oracle: CUI subnet isolated from public; default-deny ingress; TLS 1.2+ enforced;
  split tunnel disabled; session tokens bound to TLS; idle connections closed

#### Module: `MDM_ChromeOS` — Mobile + portable storage
Claims: AC.L2-3.1.16, AC.L2-3.1.17, AC.L2-3.1.18, AC.L2-3.1.19, MP.L2-3.8.7
- GCP source: Chrome Browser Cloud Management policy + Google Endpoint Verification
- Oracle: WiFi policy requires 802.1X or WPA3-Enterprise; device enrollment enforced;
  disk encryption required; USB/removable media blocked for CUI OU

#### Module: `CloudIdentity_RemoteMaintenance` — Maintenance access MFA
Claims: MA.L2-3.7.5
- GCP source: Workspace Admin + Cloud Identity policy for ops roles
- Oracle: verify MFA required for all accounts in `ops-*` / `break-glass-*` groups

### Priority order for Track A

Add modules in descending SPRS weight, non-deferrable first. The top 10 new modules
(by worst-case score loss if unmet) are:

| Priority | Module | Controls added | Max pts recovered |
|----------|--------|----------------|-------------------|
| 1 | VPC_Segmentation | 8 controls (SC) | 28 pts |
| 2 | EndpointVerification_CrowdStrike | 3 controls (SI) | 13 pts |
| 3 | MDM_ChromeOS | 5 controls (AC+MP) | 13 pts |
| 4 | SecurityCommandCenter | 3 controls (RA+SI) | 11 pts |
| 5 | WorkspaceAdmin_Policy | 8 controls (IA) | 10 pts |
| 6 | ChangeManagement_GitHub | 2 controls (CM) | 6 pts |
| 7 | VPNAccess_BeyondCorp | 4 controls (AC) | 6 pts |
| 8 | OrgPolicy_SessionControl | 2 controls (AC) | 2 pts |
| 9 | CloudLogging_Config | 4 controls (AU) | 4 pts |
| 10 | CloudIdentity_RemoteMaintenance | 1 control (MA) | 5 pts |

---

## Track B — Human Attestation Program

These controls cannot be machine-verified. The oracle always returns `cantTell`. The path
to MET is: (1) write the policy/procedure, (2) implement and collect evidence, (3) the
Affirming Official attests MET with a reference to the evidence artifact.

In the engine: add a `ce:PolicyModule` (a new `sysml:PartUsage` type with
`cmmc:verificationMethod "manual:<policy-ref>"`) to `structural/tier1.ttl` for each.
Gate 1 will accept any claiming module — the type doesn't matter, only that one exists.
The evidence is attached to the Gate 2 attestation, not the oracle.

### Documents to write

#### 1. System Security Plan (SSP) — CA.L2-3.12.4 (wt=1, non-deferrable)
The engine generates the SSP from its own run state. The missing piece is the
*human-authored substance*: system description, data flows, roles, authorized users,
physical environment, and interconnections. Write this as a YAML or RDF supplement that
the engine merges into the generated SSP. This is the root document; all other policies
reference it.

**Done when:** `ssp.md` contains a complete system description section; the NON-EVIDENTIARY
banner is absent because evidence is real (Track C).

#### 2. Security Awareness Training Program — AT.L2-3.2.1 (wt=5), AT.L2-3.2.2 (wt=5), AT.L2-3.2.3 (wt=1)
- Define annual training curriculum covering: CUI handling, phishing, insider threat,
  password hygiene, mobile device policy
- Role-based supplement for ops/engineering: incident response roles, key management,
  secure config change procedures
- Evidence: LMS completion records (name, date, score) for every person with system access
- **Start immediately** — this has the longest lead time (training takes calendar time)

#### 3. Incident Response Plan — IR.L2-3.6.1 (wt=5), IR.L2-3.6.2 (wt=5), IR.L2-3.6.3 (wt=1)
- Define: roles (Incident Commander, Security Officer), detection criteria, escalation
  thresholds, DoD reporting chain (US-CERT/CISA 72-hour window), post-incident review
- Define tabletop exercise schedule (annual minimum)
- Evidence: signed plan document + at least one completed tabletop exercise report
- **Schedule a tabletop drill** — the drill evidence takes weeks to produce

#### 4. Risk Assessment — RA.L2-3.11.1 (wt=3), RA.L2-3.11.3 (wt=1)
- Formal risk assessment: asset inventory, threat enumeration, likelihood/impact ratings,
  risk decisions (accept / mitigate / transfer)
- Remediation tracker linked to finding dates and target dates
- Evidence: dated assessment document + open/closed finding log

#### 5. Personnel Security — PS.L2-3.9.1 (wt=3), PS.L2-3.9.2 (wt=5)
- Background screening policy: when required, scope, frequency
- Offboarding checklist: account revocation, credential rotation, badge return,
  equipment recovery — must be completed within 24h of separation
- Evidence: signed background check attestation per employee + completed offboarding
  checklists for any terminations
- **PS.9.2 is 5-pt non-deferrable** — if an ex-employee has live credentials at audit
  time, this fails regardless of the policy document

#### 6. Configuration Management Policy — CM.L2-3.4.4 (wt=1), CM.L2-3.4.9 (wt=1)
- Security impact analysis procedure before any config change (references CM.4.3/4.5
  GitHub controls from Track A)
- User-installed software approval process
- Evidence: the change log entries themselves + a one-page procedure document

#### 7. Maintenance Policy — MA.L2-3.7.1 (wt=3), MA.L2-3.7.2 (wt=5), MA.L2-3.7.3 (wt=1),
                             MA.L2-3.7.4 (wt=3), MA.L2-3.7.6 (wt=1)
- Approved maintenance personnel list + tool inventory
- CUI sanitization procedure before off-site maintenance
- Diagnostic media scan procedure
- Visitor/escort policy for maintenance access
- Evidence: signed approved vendor list + any maintenance event log entries

#### 8. Media Protection Policy — MP.L2-3.8.1–6, MP.L2-3.8.8, MP.L2-3.8.9 (8 controls)
- CUI media labeling requirements (NARA 32 CFR Part 2002 markings)
- Physical media storage/access controls
- Media sanitization procedure (NIST SP 800-88 Rev.1 — Clear/Purge/Destroy by media type)
- Portable storage prohibition (backup to MDM policy from Track A)
- Evidence: media inventory log + at least one sanitization record

#### 9. Audit Management Procedure — AU.L2-3.3.3 (wt=1), AU.L2-3.3.6 (wt=1)
- Define which event types are logged (authentication, privilege use, config change, data access)
- Audit reduction / report generation procedure (who reviews, how often)
- Evidence: the procedure document + a sample log review report

#### 10. Security Engineering Principles — SC.L2-3.13.2 (wt=5)
- Document the architectural security principles applied: least privilege, defense in depth,
  fail-secure defaults, separation of duties, minimize attack surface
- Reference: NIST SP 800-160 Vol.1 as the baseline
- Evidence: architecture review document (can be the AS-BUILT.md with a sign-off block)

#### 11. Remote Access Authorization — AC.L2-3.1.15 (wt=1), AC.L2-3.1.21 (wt=1), AC.L2-3.1.22 (wt=1, non-deferrable)
- Written authorization for remote execution of privileged commands
- Portable storage prohibition on external systems
- No CUI on publicly accessible systems — verify and attest
- Evidence: policy appendix to SSP

#### 12. Physical Access (office-side) — PE.L2-3.10.3–6 (4 controls, all 1-pt)
- Visitor escort policy + visitor log
- Physical access device management (badge/key issuance and revocation procedure)
- Alternate work site (home office) CUI safeguards
- Evidence: visitor log, badge issuance log, remote work agreement per employee

#### 13. Collaborative Computing / Mobile Code / VoIP — SC.L2-3.13.12–14 (3 controls, all 1-pt)
- Camera/microphone disable policy in CUI spaces
- Mobile code authorization (allowed JavaScript sources, no ActiveX)
- VoIP usage policy if applicable
- Evidence: documented policy + Workspace/device settings showing enforcement

#### 14. Separation of Duties — AC.L2-3.1.4 (wt=1)
- Written role definition showing no single person can approve + execute a sensitive change
- Reference GitHub required-reviews from Track A as technical enforcement
- Evidence: RACI matrix or role description document

#### 15. Ongoing Monitoring — CA.L2-3.12.3 (wt=5), CA.L2-3.12.1 (wt=5), CA.L2-3.12.2 (wt=3)
- Formal monitoring program: what is monitored, how often, who reviews
- Annual self-assessment schedule (this engine IS the assessment tool — document its use)
- POA&M process for any gaps found
- Evidence: this plan + the engine run outputs + any open POA&M items

### Policy-module pattern for tier1.ttl

For each policy document above, add one entry to `structural/tier1.ttl` like:

```turtle
ce:POL_AT_Training a sysml:PartUsage ;
    rdfs:label "Security awareness and role-based training program" ;
    sysml:ownedRelationship [
        a sysml:SatisfyRequirementUsage ;
        sysml:satisfyingElement ce:POL_AT_Training ;
        sysml:satisfiedRequirement cmmc:AT.L2-3.2.1 , cmmc:AT.L2-3.2.2 , cmmc:AT.L2-3.2.3
    ] ;
    cmmc:controlsSatisfied cmmc:AT.L2-3.2.1 , cmmc:AT.L2-3.2.2 , cmmc:AT.L2-3.2.3 ;
    cmmc:verificationMethod "manual:training-completion-records" .
```

This satisfies Gate 1 (a claiming module exists) while being explicit that verification
is manual. The oracle will return `cantTell`; Gate 2 is where the Affirming Official
attests MET with a reference to the training completion records.

---

## Track C — Live Evidence Integration

This track converts the engine from a demo into a real assessment tool. It is prerequisite
to removing the NON-EVIDENTIARY banner from the SSP.

### Step C1: GCP service account + API permissions

Create a least-privilege service account with read-only access to:
- Cloud Asset Inventory API (`cloudasset.googleapis.com`)
- Cloud Identity / Workspace Admin SDK (read-only admin role)
- Security Command Center API (read-only viewer)
- Binary Authorization API
- Cloud Logging API (log viewer)
- VPC / Compute resource metadata

Store the service account key in a secrets manager (not in the repo). Pass via environment
variable `GOOGLE_APPLICATION_CREDENTIALS`.

### Step C2: Real evidence generator per Track A module

For each generator in Track A, write a real implementation class alongside the existing
mock (or gated by an `--evidence-mode real|mock` flag). The real class:
1. Calls the GCP API / GitHub API / EDR API
2. Returns the same `CollectionMetadata` dict shape as the mock
3. The hash chain (`evidence/hashing.py`) is unchanged — it hashes whatever the generator returns

The mock fixtures remain as the CI path. Real evidence runs only when `GOOGLE_APPLICATION_CREDENTIALS`
and `EVIDENCE_MODE=real` are set.

### Step C3: Terraform plan against real state

Replace the mock Terraform plan fixture with a real `terraform plan -out=plan.bin` against
the production project. The `TerraformPlanGenerator` already supports a real binary path —
the `chdir` arg needs to point to the live HCL in `terraform/tier1/`.

### Step C4: Update the COP

Replace `fixtures/nv012/cop_draft.ttl` with a COP that derives all controls being claimed.
Two options:
- **Option A (simpler):** Expand `cop_draft.ttl` by adding controls as Track A and B modules
  are added to `tier1.ttl`. The COP derives exactly what the structural layer can satisfy.
- **Option B (canonical):** Switch to `order-compiler/obligations.ttl` (`OBL-CMMC-L2 → ALL-110`)
  once all 110 have claiming modules. This is the correct production path.

Use Option A throughout development; switch to Option B as the final submission preparation step.

### Step C5: Remove the NON-EVIDENTIARY banner trigger

`documents/ssp.py` emits the banner when `mock_present=True`. With real evidence, this becomes
False. No code change needed — the banner is self-extinguishing once evidence is real.

---

## Sequencing and Milestones

```
Week 0–1:  Start Track B documents with longest lead times
           → Training program curriculum written
           → IR plan drafted + tabletop scheduled
           → Risk assessment initiated

           Start Track A engine work on highest-impact modules
           → VPC_Segmentation (SC, 8 controls)
           → EndpointVerification_CrowdStrike (SI, 3 controls)

Week 2–3:  Track A continues
           → MDM_ChromeOS (AC+MP, 5 controls)
           → WorkspaceAdmin_Policy (IA, 8 controls)
           → VPNAccess_BeyondCorp (AC, 4 controls)
           → SecurityCommandCenter (RA+SI, 3 controls)

           Track B milestones
           → Personnel security policy + background check records in place
           → Maintenance policy drafted

Week 3–4:  Track C integration
           → Service account provisioned
           → First real evidence generator live (VPC_Segmentation)
           → Real Terraform plan wired

Week 4–5:  Track A completes remaining modules
           → ChangeManagement_GitHub, CloudLogging_Config, CloudIdentity_RemoteMaintenance
           → OrgPolicy_Allowlist, OrgPolicy_SessionControl

           Track B remaining documents drafted
           → Media protection, audit procedure, PE, collaborative computing policies

Week 5–6:  All 110 controls have claiming modules in tier1.ttl
           → Gate 1 passes against all 110 when COP expanded to full set
           → cop_draft.ttl updated or obligations.ttl switched in

Week 6:    Tabletop drill (IR.3.6.3 evidence)
           Training completion records collected for all personnel

Week 7–8:  Gate 2 attestation pass
           → Affirming Official reviews each control
           → MET / NOT MET entered for all 110
           → POA&M items identified for any NOT MET

Week 8–9:  Final run
           → cli.py demo (or cli.py run) with real evidence, real COP, all 110
           → SPRS score calculated, SSP generated (no NON-EVIDENTIARY banner)
           → BOM and SSP reviewed

Week 9–10: Submission
           → SPRS score submitted at sprs.pmrt.mil
           → SSP filed in contractor record
           → POA&M submitted for any deferred 1-point controls
```

---

## Done Definition — Submission Checklist

Before filing, every item below must be true:

### Engine
- [ ] All 110 CMMC L2 controls have a claiming module in `structural/tier1.ttl`
- [ ] Gate 1 passes with the full-110 COP (`obligations.ttl`)
- [ ] Every machine-possible control has a real evidence generator (no mock fixtures in
      the production evidence set)
- [ ] `evidentiary_status` field in BOM is `real` (not `mock`)
- [ ] SSP is generated without the NON-EVIDENTIARY banner
- [ ] SPRS score ≥ 88 (Conditional) or 110 (Final); `valid_submission=True`
- [ ] `illegal_poam` is empty (no 5-pt or excluded 1-pt controls on POA&M)
- [ ] Contradiction count = 0 (no MET attestation over a failed oracle without override)

### Organizational
- [ ] All personnel with CUI system access have completed annual security awareness training
      (completion records dated within last 12 months)
- [ ] Role-based training completed by all with elevated access
- [ ] Incident Response Plan signed and dated
- [ ] At least one tabletop exercise completed with written report
- [ ] Risk assessment completed and signed
- [ ] POA&M exists for any NOT MET controls (open items with target dates)
- [ ] SSP system description section is accurate and human-authored
- [ ] Background screening documented for all CUI-access personnel
- [ ] Offboarding checklist exists; no ex-employees have active credentials
- [ ] All policies signed by the Affirming Official

### Submission
- [ ] SPRS score submitted at `sprs.pmrt.mil` under the correct cage code
- [ ] Self-assessment date recorded in SPRS (within 3 years of submission)
- [ ] SSP retained in contractor records (minimum 3 years)
- [ ] Contracting officer notified per DFARS 252.204-7020

---

## What Will Remain NOT MET (and why that's acceptable)

A perfect SPRS 110 / Final is possible on paper but nearly impossible in the first
self-assessment for a small contractor. In practice, 88–110 with a POA&M is the norm.

Controls most likely to remain NOT MET in the first cycle:
- **AU.L2-3.3.6** (audit reduction/reporting process) — requires a documented review cadence
  that may not be fully operationalized yet; 1 pt, POA&M-eligible
- **MP.L2-3.8.3** (media sanitization) — requires at least one documented sanitization event
  as evidence; may not have occurred yet; 5 pts, NOT POA&M-eligible → must fix
- **AC.L2-3.1.4** (separation of duties) — for a small team this may genuinely be hard to
  implement; 1 pt, POA&M-eligible

Any 5-point or non-deferrable control left NOT MET is a problem — it either drops you to
Conditional (score 88–109) or invalidates the submission. The engine will tell you exactly
which ones as you enter Gate 2 attestations.

---

## What the Engine Cannot Do For You

The engine automates collection, scoring, and reporting. It cannot:
- Substitute for an actual training program
- Manufacture policy documents
- Conduct a background check
- Perform a tabletop exercise
- Make an organizational decision about risk acceptance
- Sign the Affirming Official attestation on behalf of a human

The SPRS score is only as honest as the Gate 2 attestations. The Affirming Official's
signature is personal liability under 18 U.S.C. § 1001 (false statements to the federal
government). Do not attest MET for a control where the evidence does not support it.

---

## Open Questions Before Starting

1. **Who is the Affirming Official?** This must be a senior employee with organizational
   authority. For a small contractor this is typically the owner or a designated security officer.

2. **Is there an existing cloud project?** Track C assumes a GCP project with Workspace
   Enterprise Plus exists. If the GCP environment is hypothetical, Track A engine work can
   still proceed with real Terraform HCL (offline providers) and real policy API mocks.

3. **EDR coverage:** SI.3.14.2/4/5 assume an endpoint detection tool (CrowdStrike, SentinelOne,
   or equivalent). If none is deployed, deploy one before attempting Track A for SI.

4. **Physical office environment:** The PE.3.10.3–6 controls (visitor log, badge access,
   alternate work sites) require a real physical environment. Fully remote teams with no
   company office may be able to scope these differently — check with your C3PAO.

5. **C3PAO vs. self-assessment:** CMMC L2 allows self-assessment for most contracts. If the
   specific contract requires a C3PAO-conducted assessment (check the contract's DFARS clauses),
   the self-assessment artifacts from this engine are still the input to that assessment — the
   engine does not need to change, but you'll have an independent assessor reviewing everything.
