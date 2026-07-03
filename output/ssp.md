<!-- AUTO-GENERATED ARTIFACT - DO NOT EDIT.
     Deterministic view compiled from the RDF dataset by documents/ssp.py.
     Edit the dataset (re-run the pipeline), then rebuild:
       uv run python -m documents.ssp build --input <dataset.trig> -->

# SSP-NV012 — NV012 System Security Plan + Traceability Matrix (Document 2)

> ⚠ **NON-EVIDENTIARY — fixture-derived / auto-attested.**
> Evidentiary status present: mock. This is a demonstration artifact, **not a submittable SSP**.

## 1. System identification and CUI boundary

| Field | Value |
| --- | --- |
| Document ID | SSP-NV012 |
| System | NV012 Tier 1 IL4 CUI enclave |
| CUI boundary | Google Workspace Enterprise Plus + GCP Assured Workloads (IL4) |
| Dataset | output/engine.trig |
| Dataset SHA-256 | 29bbe4df54e50fb88586eb721c31b19a90858b0357db6eaf88a50019d4cad88a |
| Quad count | 2057 |
| Document date | 2026-07-03T02:52:38.484883+00:00 |
| Evidentiary status | NON-EVIDENTIARY (mock) |
| Compiler | documents/ssp.py |

## 2. Framework applicability

Scope: NIST SP 800-171 Rev. 2 / CMMC Level 2 (110 controls). Status is the
recorded human attestation (EARL outcome via `STATUS_LABEL`); evidence
*addresses* controls but never *attests* them. The machine-checkable subset
is verified by oracles; the remainder is human-attested from documentary
evidence.

## 3. Verification Cross-Reference Matrix (VCRM) — Document 2

One row per control (all 110). Status is the attestation outcome; a control
with no attestation is PLANNED (a gap).

| Control | Implementation | Responsible party | Evidence location | Evidence hash | Status | Gap notes | POA&M ref |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AC.L2-3.1.1 | IAM groups + least-privilege role bindings for CUI access | NV012 Affirming Official | nv012/contradiction/gcp_iam_bindings.json | 4bba2d0adcbb, 6c69bdddaea3 | MET | - | - |
| AC.L2-3.1.10 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.11 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.12 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.13 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.14 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.15 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.16 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.17 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.18 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.19 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.2 | IAM groups + least-privilege role bindings for CUI access | NV012 Affirming Official | - | - | MET | - | - |
| AC.L2-3.1.20 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.21 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.22 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.3 | Drive + Gmail DLP rules (control the flow of CUI) | NV012 Affirming Official | - | - | MET | - | - |
| AC.L2-3.1.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.5 | IAM groups + least-privilege role bindings for CUI access | NV012 Affirming Official | - | - | MET | - | - |
| AC.L2-3.1.6 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.7 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.8 | - | - | - | - | PLANNED | not attested (planned) | - |
| AC.L2-3.1.9 | - | - | - | - | PLANNED | not attested (planned) | - |
| AT.L2-3.2.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| AT.L2-3.2.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| AT.L2-3.2.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| AU.L2-3.3.1 | Workspace + GCP audit log export to retained Cloud Storage bucket | NV012 Affirming Official | - | - | MET | - | - |
| AU.L2-3.3.2 | Workspace + GCP audit log export to retained Cloud Storage bucket | NV012 Affirming Official | - | - | MET | - | - |
| AU.L2-3.3.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| AU.L2-3.3.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| AU.L2-3.3.5 | Workspace + GCP audit log export to retained Cloud Storage bucket | NV012 Affirming Official | - | - | MET | - | - |
| AU.L2-3.3.6 | - | - | - | - | PLANNED | not attested (planned) | - |
| AU.L2-3.3.7 | - | - | - | - | PLANNED | not attested (planned) | - |
| AU.L2-3.3.8 | - | - | - | - | PLANNED | not attested (planned) | - |
| AU.L2-3.3.9 | - | - | - | - | PLANNED | not attested (planned) | - |
| CA.L2-3.12.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| CA.L2-3.12.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| CA.L2-3.12.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| CA.L2-3.12.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| CM.L2-3.4.1 | Terraform baseline configuration + resource inventory (IaC) | NV012 Affirming Official | - | - | MET | - | - |
| CM.L2-3.4.2 | Terraform baseline configuration + resource inventory (IaC) | NV012 Affirming Official | - | - | MET | - | - |
| CM.L2-3.4.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| CM.L2-3.4.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| CM.L2-3.4.5 | - | - | - | - | PLANNED | not attested (planned) | - |
| CM.L2-3.4.6 | Disable non-FedRAMP-authorized services for the CUI OU (least functionality) | NV012 Affirming Official | - | - | MET | - | - |
| CM.L2-3.4.7 | Disable non-FedRAMP-authorized services for the CUI OU (least functionality) | NV012 Affirming Official | - | - | MET | - | - |
| CM.L2-3.4.8 | - | - | - | - | PLANNED | not attested (planned) | - |
| CM.L2-3.4.9 | - | - | - | - | PLANNED | not attested (planned) | - |
| IA.L2-3.5.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| IA.L2-3.5.10 | - | - | - | - | PLANNED | not attested (planned) | - |
| IA.L2-3.5.11 | - | - | - | - | PLANNED | not attested (planned) | - |
| IA.L2-3.5.2 | Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU | NV012 Affirming Official | - | - | MET | - | - |
| IA.L2-3.5.3 | Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU | NV012 Affirming Official | nv012/contradiction/workspace_2sv.json | 191fda68120a | MET | - | - |
| IA.L2-3.5.4 | Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU | NV012 Affirming Official | - | - | MET | - | - |
| IA.L2-3.5.5 | - | - | - | - | PLANNED | not attested (planned) | - |
| IA.L2-3.5.6 | - | - | - | - | PLANNED | not attested (planned) | - |
| IA.L2-3.5.7 | - | - | - | - | PLANNED | not attested (planned) | - |
| IA.L2-3.5.8 | - | - | - | - | PLANNED | not attested (planned) | - |
| IA.L2-3.5.9 | - | - | - | - | PLANNED | not attested (planned) | - |
| IR.L2-3.6.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| IR.L2-3.6.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| IR.L2-3.6.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| MA.L2-3.7.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| MA.L2-3.7.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| MA.L2-3.7.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| MA.L2-3.7.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| MA.L2-3.7.5 | - | - | - | - | PLANNED | not attested (planned) | - |
| MA.L2-3.7.6 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.5 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.6 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.7 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.8 | - | - | - | - | PLANNED | not attested (planned) | - |
| MP.L2-3.8.9 | - | - | - | - | PLANNED | not attested (planned) | - |
| PE.L2-3.10.1 | CSP-inherited physical protection (Google IL4 data-center controls) | NV012 Affirming Official | - | - | MET | - | - |
| PE.L2-3.10.2 | CSP-inherited physical protection (Google IL4 data-center controls) | NV012 Affirming Official | - | - | MET | - | - |
| PE.L2-3.10.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| PE.L2-3.10.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| PE.L2-3.10.5 | - | - | - | - | PLANNED | not attested (planned) | - |
| PE.L2-3.10.6 | - | - | - | - | PLANNED | not attested (planned) | - |
| PS.L2-3.9.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| PS.L2-3.9.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| RA.L2-3.11.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| RA.L2-3.11.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| RA.L2-3.11.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.1 | GCP Org Policy: US-only resource locations + restricted service usage | NV012 Affirming Official | nv012/contradiction/gcp_org_policy_region.json | 385f07ca2e58, 5f8e7ef2f8ff | MET | - | - |
| SC.L2-3.13.10 | Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto) | NV012 Affirming Official | - | - | MET | - | - |
| SC.L2-3.13.11 | Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto) | NV012 Affirming Official | nv012/contradiction/gcp_kms_cmvp.json | 3c4af60bc144 | MET | - | - |
| SC.L2-3.13.12 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.13 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.14 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.15 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.16 | Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto) | NV012 Affirming Official | nv012/contradiction/gcp_cmek_at_rest.json | 52eb61a61772 | MET | - | - |
| SC.L2-3.13.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.3 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.5 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.6 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.7 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.8 | - | - | - | - | PLANNED | not attested (planned) | - |
| SC.L2-3.13.9 | - | - | - | - | PLANNED | not attested (planned) | - |
| SI.L2-3.14.1 | - | - | - | - | PLANNED | not attested (planned) | - |
| SI.L2-3.14.2 | - | - | - | - | PLANNED | not attested (planned) | - |
| SI.L2-3.14.3 | Cloud Monitoring + Workspace Alert Center (security alert monitoring/response) | NV012 Affirming Official | - | - | MET | - | - |
| SI.L2-3.14.4 | - | - | - | - | PLANNED | not attested (planned) | - |
| SI.L2-3.14.5 | - | - | - | - | PLANNED | not attested (planned) | - |
| SI.L2-3.14.6 | Cloud Monitoring + Workspace Alert Center (security alert monitoring/response) | NV012 Affirming Official | - | - | MET | - | - |
| SI.L2-3.14.7 | - | - | - | - | PLANNED | not attested (planned) | - |

## 4. Per-control detail

### AC.L2-3.1.1

**Statement.** Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: IAM groups + least-privilege role bindings for CUI access
- Verification method: oracle-iam-least-privilege

- Attestation: ATT-AC.L2-3.1.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.350542+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.2

**Statement.** Limit system access to the types of transactions and functions that authorized users are permitted to execute.

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: IAM groups + least-privilege role bindings for CUI access
- Verification method: oracle-iam-least-privilege

- Attestation: ATT-AC.L2-3.1.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.357538+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### AC.L2-3.1.3

**Statement.** Control the flow of CUI in accordance with approved authorizations.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Drive + Gmail DLP rules (control the flow of CUI)
- Verification method: oracle-drive-dlp-rules

- Attestation: ATT-AC.L2-3.1.3 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.363684+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### AC.L2-3.1.5

**Statement.** Employ the principle of least privilege, including for specific security functions and privileged accounts.

- Family: AC · Weight: 3 · POA&M-eligible: false
- Implementation: IAM groups + least-privilege role bindings for CUI access
- Verification method: oracle-iam-least-privilege

- Attestation: ATT-AC.L2-3.1.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.370110+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### AU.L2-3.3.1

**Statement.** Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.

- Family: AU · Weight: 5 · POA&M-eligible: false
- Implementation: Workspace + GCP audit log export to retained Cloud Storage bucket
- Verification method: oracle-auditlog-export

- Attestation: ATT-AU.L2-3.3.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.376617+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### AU.L2-3.3.2

**Statement.** Ensure that the actions of individual system users can be uniquely traced to those users, so they can be held accountable for their actions.

- Family: AU · Weight: 3 · POA&M-eligible: false
- Implementation: Workspace + GCP audit log export to retained Cloud Storage bucket
- Verification method: oracle-auditlog-export

- Attestation: ATT-AU.L2-3.3.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.383038+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### AU.L2-3.3.5

**Statement.** Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.

- Family: AU · Weight: 5 · POA&M-eligible: false
- Implementation: Workspace + GCP audit log export to retained Cloud Storage bucket
- Verification method: oracle-auditlog-export

- Attestation: ATT-AU.L2-3.3.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.389794+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### CM.L2-3.4.1

**Statement.** Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Terraform baseline configuration + resource inventory (IaC)
- Verification method: oracle-terraform-baseline

- Attestation: ATT-CM.L2-3.4.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.396055+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### CM.L2-3.4.2

**Statement.** Establish and enforce security configuration settings for information technology products employed in organizational systems.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Terraform baseline configuration + resource inventory (IaC)
- Verification method: oracle-terraform-baseline

- Attestation: ATT-CM.L2-3.4.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.402282+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### CM.L2-3.4.6

**Statement.** Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Disable non-FedRAMP-authorized services for the CUI OU (least functionality)
- Verification method: oracle-restrict-service-usage

- Attestation: ATT-CM.L2-3.4.6 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.408553+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### CM.L2-3.4.7

**Statement.** Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Disable non-FedRAMP-authorized services for the CUI OU (least functionality)
- Verification method: oracle-restrict-service-usage

- Attestation: ATT-CM.L2-3.4.7 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.414633+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### IA.L2-3.5.2

**Statement.** Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems.

- Family: IA · Weight: 5 · POA&M-eligible: false
- Implementation: Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU
- Verification method: oracle-mfa-2sv-enforced

- Attestation: ATT-IA.L2-3.5.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.420857+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### IA.L2-3.5.3

**Statement.** Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.

- Family: IA · Weight: 5 · POA&M-eligible: false
- Implementation: Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU
- Verification method: oracle-mfa-2sv-enforced

- Attestation: ATT-IA.L2-3.5.3 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.427473+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.4

**Statement.** Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.

- Family: IA · Weight: 1 · POA&M-eligible: true
- Implementation: Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU
- Verification method: oracle-mfa-2sv-enforced

- Attestation: ATT-IA.L2-3.5.4 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.433721+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### PE.L2-3.10.1

**Statement.** Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals.

- Family: PE · Weight: 5 · POA&M-eligible: false
- Implementation: CSP-inherited physical protection (Google IL4 data-center controls)
- Verification method: inherited:google-workspace-crm

- Attestation: ATT-PE.L2-3.10.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.439896+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### PE.L2-3.10.2

**Statement.** Protect and monitor the physical facility and support infrastructure for organizational systems.

- Family: PE · Weight: 5 · POA&M-eligible: false
- Implementation: CSP-inherited physical protection (Google IL4 data-center controls)
- Verification method: inherited:google-workspace-crm

- Attestation: ATT-PE.L2-3.10.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.446120+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### SC.L2-3.13.1

**Statement.** Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems.

- Family: SC · Weight: 5 · POA&M-eligible: false
- Implementation: GCP Org Policy: US-only resource locations + restricted service usage
- Verification method: oracle-orgpolicy-us-residency

- Attestation: ATT-SC.L2-3.13.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.452905+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.10

**Statement.** Establish and manage cryptographic keys for cryptography employed in organizational systems.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto)
- Verification method: oracle-cmek-fips-keyring

- Attestation: ATT-SC.L2-3.13.10 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.459169+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### SC.L2-3.13.11

**Statement.** Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.

- Family: SC · Weight: 5 · POA&M-eligible: false
- Implementation: Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto)
- Verification method: oracle-cmek-fips-keyring

- Attestation: ATT-SC.L2-3.13.11 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.465832+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.16

**Statement.** Protect the confidentiality of CUI at rest.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto)
- Verification method: oracle-cmek-fips-keyring

- Attestation: ATT-SC.L2-3.13.16 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.472156+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SI.L2-3.14.3

**Statement.** Monitor system security alerts and advisories and take action in response.

- Family: SI · Weight: 5 · POA&M-eligible: false
- Implementation: Cloud Monitoring + Workspace Alert Center (security alert monitoring/response)
- Verification method: oracle-monitoring-alerts

- Attestation: ATT-SI.L2-3.14.3 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.478602+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

### SI.L2-3.14.6

**Statement.** Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.

- Family: SI · Weight: 5 · POA&M-eligible: false
- Implementation: Cloud Monitoring + Workspace Alert Center (security alert monitoring/response)
- Verification method: oracle-monitoring-alerts

- Attestation: ATT-SI.L2-3.14.6 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-03T02:52:38.484883+00:00
  - Adequacy assumption: Implementation reviewed; control met by human/inherited determination.
  - Sufficiency justification: No machine oracle for this control; attested MET on documentary/CSP basis.

## 5. Colophon

| Layer | Named graph | Triples |
| --- | --- | --- |
| attestations | `http://dynamicalsystems.group/compliance-engine/attestations` | 432 |
| audit | `http://dynamicalsystems.group/compliance-engine/audit` | 115 |
| evidence | `http://dynamicalsystems.group/compliance-engine/evidence` | 149 |
| ontology | `http://dynamicalsystems.group/compliance-engine/ontology` | 1057 |
| order | `http://dynamicalsystems.group/compliance-engine/order` | 150 |
| plan | `http://dynamicalsystems.group/compliance-engine/plan` | 0 |
| plan_execution | `http://dynamicalsystems.group/compliance-engine/plan-execution` | 36 |
| structural | `http://dynamicalsystems.group/compliance-engine/structural` | 118 |

Dataset SHA-256: `29bbe4df54e50fb88586eb721c31b19a90858b0357db6eaf88a50019d4cad88a`

Document date (max prov:generatedAtTime): 2026-07-03T02:52:38.484883+00:00

SPRS summary: score 110 (Final); 3 MET-by-machine / 19 MET-by-human-only; contradictions: 1.

Artifact hashes (BOM): 19

- `00693338fb29c30f553937069f1ec3b7285cd4f02a089d18e8d029522c40e3ea`
- `0ed2eedf228cfa815e80d241f2bfd62368616ba6ef2ee40ef91c317dc9e8c4a7`
- `10bee86a3f6d301f24538c1caa533a0fcd7121faa529c0c9721c28497e23fae1`
- `191fda68120a6adc9fca4f33ba139b877250d416887d0b7b01ac5ac91355ff72`
- `385f07ca2e587097c8fdb83a7175af8d073717180b8e9db3670d7e5bc346897e`
- `3c4af60bc14480071afa3b9486fa7514484a9b6dcc77846d325e57f2955d47ac`
- `45b70ef22dcb69f47a8943271206d860d8f770af1549614893f972302241af0d`
- `4bba2d0adcbb48ec02d9b82a9ec4c9655c13c20b39c35136630de23b08f32f12`
- `52eb61a61772b7878d6db0b96ae3441d5f1bb66f0f1bf5cbc7565481acf23cde`
- `59a6617d68a550cd248b61f625156d0e6b71c6c4b69c989419766456f5dc833f`
- `5c41b30cc0ef81407debf3fb91b9912a1a1da06de9752eccb96dd597af1d96a0`
- `5f8e7ef2f8ffc747ece0831bf33066eb499c1f12b2c5f5bb7e8768ce1fe921fa`
- `6c69bdddaea378c058139148d6865c4cba32f0b00b86c9d24f2ba2aafb2b97c1`
- `70d573b23771a8c3d14ec76cd557a37722ca3fc8ca97246dce7bfc454d70bcf7`
- `82e5d2082cc9fb90786e3aeca299c3331a8cfbdb2e486a832c257cb6bd10d9c4`
- `b5e9a6da66f8d13b6a81113c09cf7f0d704b9d621a6300aeee0d3df2e3e7ca29`
- `cdad6fb17f7cb53728276bb24de654c87b6725e31b9bd731efa7769234afbc85`
- `ce20d3b1b76ec95c37328a20ddc89ff47cf667bcbb417c0757a43f8e110581b8`
- `ea589346e8b68f5865c4abe045628dce5b9ae61a03a92585b1a082fd59c77982`

**NON-EVIDENTIARY stamp:** statuses present — mock. Not a submittable SSP (mock evidence).

Rebuild and drift-check:

```bash
uv run python -m documents.ssp build --input output/engine.trig
uv run python -m documents.ssp build --check
```
