<!-- AUTO-GENERATED ARTIFACT - DO NOT EDIT.
     Deterministic view compiled from the RDF dataset by documents/ssp.py.
     Edit the dataset (re-run the pipeline), then rebuild:
       uv run python -m documents.ssp build --input <dataset.trig> -->

# SSP-NV012 — NV012 System Security Plan + Traceability Matrix (Document 2)

> **NON-EVIDENTIARY — fixture-derived / auto-attested.**
> Evidentiary status present: mock. This is a demonstration artifact, **not a submittable SSP**.

## 1. System identification and CUI boundary

| Field | Value |
| --- | --- |
| Document ID | SSP-NV012 |
| System | NV012 Tier 1 IL4 CUI enclave |
| CUI boundary | Google Workspace Enterprise Plus + GCP Assured Workloads (IL4) |
| Dataset | output/engine.trig |
| Dataset SHA-256 | 7610cea52d9f174ce5501cc7aaa5264b76ab088fd316ec4fd06485d67888f136 |
| Quad count | 7309 |
| Document date | 2026-07-07T17:57:12.300619+00:00 |
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
| AC.L2-3.1.1 | IAM groups + least-privilege role bindings for CUI access | NV012 Affirming Official | nv012/all-covered/gcp_iam_bindings.json | 4bba2d0adcbb, 6c69bdddaea3 | MET | - | - |
| AC.L2-3.1.10 | Cloud Identity session control + failed-login lockout | NV012 Affirming Official | nv012/all-covered/gcp_session_control.json | 8959f24468b8 | MET | - | - |
| AC.L2-3.1.11 | Cloud Identity session control + failed-login lockout | NV012 Affirming Official | nv012/all-covered/gcp_session_control.json | 8959f24468b8 | MET | - | - |
| AC.L2-3.1.12 | BeyondCorp Enterprise remote access + TLS enforcement | NV012 Affirming Official | nv012/all-covered/beyondcorp_remote.json | 753946a895a2 | MET | - | - |
| AC.L2-3.1.13 | BeyondCorp Enterprise remote access + TLS enforcement | NV012 Affirming Official | nv012/all-covered/beyondcorp_remote.json | 753946a895a2 | MET | - | - |
| AC.L2-3.1.14 | BeyondCorp Enterprise remote access + TLS enforcement | NV012 Affirming Official | nv012/all-covered/beyondcorp_remote.json | 753946a895a2 | MET | - | - |
| AC.L2-3.1.15 | Remote access authorization (SSP appendix) | Sayer Tindall | - | - | MET | - | - |
| AC.L2-3.1.16 | Chrome Cloud Management + Endpoint Verification (MDM) | NV012 Affirming Official | nv012/all-covered/chrome_mdm.json | df6706e07d44 | MET | - | - |
| AC.L2-3.1.17 | Chrome Cloud Management + Endpoint Verification (MDM) | NV012 Affirming Official | nv012/all-covered/chrome_mdm.json | df6706e07d44 | MET | - | - |
| AC.L2-3.1.18 | Chrome Cloud Management + Endpoint Verification (MDM) | NV012 Affirming Official | nv012/all-covered/chrome_mdm.json | df6706e07d44 | MET | - | - |
| AC.L2-3.1.19 | Chrome Cloud Management + Endpoint Verification (MDM) | NV012 Affirming Official | nv012/all-covered/chrome_mdm.json | df6706e07d44 | MET | - | - |
| AC.L2-3.1.2 | IAM groups + least-privilege role bindings for CUI access | NV012 Affirming Official | nv012/all-covered/gcp_iam_access_enforcement.json | 9c2e2dd99b27 | MET | - | - |
| AC.L2-3.1.20 | VPC Service Controls perimeter — external system authorization | NV012 Affirming Official | nv012/all-covered/gcp_vpc_service_controls.json | b6c67e930e8a | MET | - | - |
| AC.L2-3.1.21 | Remote access authorization (SSP appendix) | Sayer Tindall | - | - | MET | - | - |
| AC.L2-3.1.22 | Remote access authorization (SSP appendix) | Sayer Tindall | - | - | MET | - | - |
| AC.L2-3.1.3 | Drive + Gmail DLP rules (control the flow of CUI) | NV012 Affirming Official | nv012/all-covered/gcp_iam_access_enforcement.json | 9c2e2dd99b27 | MET | - | - |
| AC.L2-3.1.4 | Separation of duties (RACI matrix) | Sayer Tindall | - | - | MET | - | - |
| AC.L2-3.1.5 | IAM groups + least-privilege role bindings for CUI access | NV012 Affirming Official | nv012/all-covered/gcp_iam_access_enforcement.json | 9c2e2dd99b27 | MET | - | - |
| AC.L2-3.1.6 | GCP IAM policy + audit-log signals for privileged use | NV012 Affirming Official | nv012/all-covered/gcp_iam_privileged.json | 594252df359f | MET | - | - |
| AC.L2-3.1.7 | GCP IAM policy + audit-log signals for privileged use | NV012 Affirming Official | nv012/all-covered/gcp_iam_privileged.json | 594252df359f | MET | - | - |
| AC.L2-3.1.8 | Cloud Identity session control + failed-login lockout | NV012 Affirming Official | nv012/all-covered/gcp_session_control.json | 8959f24468b8 | MET | - | - |
| AC.L2-3.1.9 | Login banner policy (system-use notification) | Sayer Tindall | - | - | MET | - | - |
| AT.L2-3.2.1 | Annual security awareness + role-based training program | Sayer Tindall | - | - | MET | - | - |
| AT.L2-3.2.2 | Annual security awareness + role-based training program | Sayer Tindall | - | - | MET | - | - |
| AT.L2-3.2.3 | Annual security awareness + role-based training program | Sayer Tindall | - | - | MET | - | - |
| AU.L2-3.3.1 | Workspace + GCP audit log export to retained Cloud Storage bucket | NV012 Affirming Official | nv012/all-covered/gcp_cloud_audit.json | 2690e5e9a376 | MET | - | - |
| AU.L2-3.3.2 | Workspace + GCP audit log export to retained Cloud Storage bucket | NV012 Affirming Official | nv012/all-covered/gcp_cloud_audit.json | 2690e5e9a376 | MET | - | - |
| AU.L2-3.3.3 | Audit management procedure (log review cadence + reports) | Sayer Tindall | - | - | MET | - | - |
| AU.L2-3.3.4 | Cloud Logging sinks + NTP + IAM on log buckets | NV012 Affirming Official | nv012/all-covered/gcp_cloud_logging.json | dbbec2757568 | MET | - | - |
| AU.L2-3.3.5 | Workspace + GCP audit log export to retained Cloud Storage bucket | NV012 Affirming Official | nv012/all-covered/gcp_cloud_audit.json | 2690e5e9a376 | MET | - | - |
| AU.L2-3.3.6 | Audit management procedure (log review cadence + reports) | Sayer Tindall | - | - | MET | - | - |
| AU.L2-3.3.7 | Cloud Logging sinks + NTP + IAM on log buckets | NV012 Affirming Official | nv012/all-covered/gcp_cloud_logging.json | dbbec2757568 | MET | - | - |
| AU.L2-3.3.8 | Cloud Logging sinks + NTP + IAM on log buckets | NV012 Affirming Official | nv012/all-covered/gcp_cloud_logging.json | dbbec2757568 | MET | - | - |
| AU.L2-3.3.9 | Cloud Logging sinks + NTP + IAM on log buckets | NV012 Affirming Official | nv012/all-covered/gcp_cloud_logging.json | dbbec2757568 | MET | - | - |
| CA.L2-3.12.1 | Continuous monitoring: engine run history + POA&M tracker | Sayer Tindall | - | - | MET | - | - |
| CA.L2-3.12.2 | Continuous monitoring: engine run history + POA&M tracker | Sayer Tindall | - | - | MET | - | - |
| CA.L2-3.12.3 | Continuous monitoring: engine run history + POA&M tracker | Sayer Tindall | - | - | MET | - | - |
| CA.L2-3.12.4 | System Security Plan supplement (system description) | Sayer Tindall | - | - | MET | - | - |
| CM.L2-3.4.1 | Terraform baseline configuration + resource inventory (IaC) | NV012 Affirming Official | nv012/all-covered/gcp_config_baseline.json | 75ad3c7ecdfa | MET | - | - |
| CM.L2-3.4.2 | Terraform baseline configuration + resource inventory (IaC) | NV012 Affirming Official | nv012/all-covered/gcp_config_baseline.json | 75ad3c7ecdfa | MET | - | - |
| CM.L2-3.4.3 | GitHub branch protection + required reviews | NV012 Affirming Official | nv012/all-covered/github_branch_protection.json | a911dd6a6276 | MET | - | - |
| CM.L2-3.4.4 | Configuration management: security impact analysis procedure | Sayer Tindall | - | - | MET | - | - |
| CM.L2-3.4.5 | GitHub branch protection + required reviews | NV012 Affirming Official | nv012/all-covered/github_branch_protection.json | a911dd6a6276 | MET | - | - |
| CM.L2-3.4.6 | Disable non-FedRAMP-authorized services for the CUI OU (least functionality) | NV012 Affirming Official | nv012/all-covered/gcp_config_baseline.json | 75ad3c7ecdfa | MET | - | - |
| CM.L2-3.4.7 | Disable non-FedRAMP-authorized services for the CUI OU (least functionality) | NV012 Affirming Official | nv012/all-covered/gcp_config_baseline.json | 75ad3c7ecdfa | MET | - | - |
| CM.L2-3.4.8 | Binary Authorization — image allowlist / user-installed software | NV012 Affirming Official | nv012/all-covered/gcp_binauth_allowlist.json | e1bec3138a1e | MET | - | - |
| CM.L2-3.4.9 | Binary Authorization — image allowlist / user-installed software | NV012 Affirming Official | nv012/all-covered/gcp_binauth_allowlist.json | e1bec3138a1e | MET | - | - |
| IA.L2-3.5.1 | Workspace Admin identity lifecycle + password policy | NV012 Affirming Official | nv012/all-covered/workspace_admin_policy.json | 2d9165ac19f5 | MET | - | - |
| IA.L2-3.5.10 | Workspace Admin identity lifecycle + password policy | NV012 Affirming Official | nv012/all-covered/workspace_admin_policy.json | 2d9165ac19f5 | MET | - | - |
| IA.L2-3.5.11 | Workspace Admin identity lifecycle + password policy | NV012 Affirming Official | nv012/all-covered/workspace_admin_policy.json | 2d9165ac19f5 | MET | - | - |
| IA.L2-3.5.2 | Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU | NV012 Affirming Official | nv012/all-covered/workspace_auth_hardening.json | d0cea0ecf9b3 | MET | - | - |
| IA.L2-3.5.3 | Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU | NV012 Affirming Official | nv012/all-covered/workspace_2sv.json | 6549f40b7941 | MET | - | - |
| IA.L2-3.5.4 | Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU | NV012 Affirming Official | nv012/all-covered/workspace_auth_hardening.json | d0cea0ecf9b3 | MET | - | - |
| IA.L2-3.5.5 | Workspace Admin identity lifecycle + password policy | NV012 Affirming Official | nv012/all-covered/workspace_admin_policy.json | 2d9165ac19f5 | MET | - | - |
| IA.L2-3.5.6 | Workspace Admin identity lifecycle + password policy | NV012 Affirming Official | nv012/all-covered/workspace_admin_policy.json | 2d9165ac19f5 | MET | - | - |
| IA.L2-3.5.7 | Workspace Admin identity lifecycle + password policy | NV012 Affirming Official | nv012/all-covered/workspace_admin_policy.json | 2d9165ac19f5 | MET | - | - |
| IA.L2-3.5.8 | Workspace Admin identity lifecycle + password policy | NV012 Affirming Official | nv012/all-covered/workspace_admin_policy.json | 2d9165ac19f5 | MET | - | - |
| IA.L2-3.5.9 | Workspace Admin identity lifecycle + password policy | NV012 Affirming Official | nv012/all-covered/workspace_admin_policy.json | 2d9165ac19f5 | MET | - | - |
| IR.L2-3.6.1 | Incident Response Plan + annual tabletop exercise | Sayer Tindall | - | - | MET | - | - |
| IR.L2-3.6.2 | Incident Response Plan + annual tabletop exercise | Sayer Tindall | - | - | MET | - | - |
| IR.L2-3.6.3 | Incident Response Plan + annual tabletop exercise | Sayer Tindall | - | - | MET | - | - |
| MA.L2-3.7.1 | Maintenance policy: approved vendor list + maintenance log | Sayer Tindall | - | - | MET | - | - |
| MA.L2-3.7.2 | Maintenance policy: approved vendor list + maintenance log | Sayer Tindall | - | - | MET | - | - |
| MA.L2-3.7.3 | Maintenance policy: approved vendor list + maintenance log | Sayer Tindall | - | - | MET | - | - |
| MA.L2-3.7.4 | Maintenance policy: approved vendor list + maintenance log | Sayer Tindall | - | - | MET | - | - |
| MA.L2-3.7.5 | Cloud Identity MFA for ops / break-glass roles | NV012 Affirming Official | nv012/all-covered/workspace_ops_mfa.json | d51b18159d04 | MET | - | - |
| MA.L2-3.7.6 | Maintenance policy: approved vendor list + maintenance log | Sayer Tindall | - | - | MET | - | - |
| MP.L2-3.8.1 | Media protection: labeling, storage, sanitization (NIST SP 800-88) | Sayer Tindall | - | - | MET | - | - |
| MP.L2-3.8.2 | Media protection: labeling, storage, sanitization (NIST SP 800-88) | Sayer Tindall | - | - | MET | - | - |
| MP.L2-3.8.3 | Media protection: labeling, storage, sanitization (NIST SP 800-88) | Sayer Tindall | - | - | MET | - | - |
| MP.L2-3.8.4 | Media protection: labeling, storage, sanitization (NIST SP 800-88) | Sayer Tindall | - | - | MET | - | - |
| MP.L2-3.8.5 | Media protection: labeling, storage, sanitization (NIST SP 800-88) | Sayer Tindall | - | - | MET | - | - |
| MP.L2-3.8.6 | Media protection: labeling, storage, sanitization (NIST SP 800-88) | Sayer Tindall | - | - | MET | - | - |
| MP.L2-3.8.7 | Chrome Cloud Management + Endpoint Verification (MDM) | NV012 Affirming Official | nv012/all-covered/chrome_mdm.json | df6706e07d44 | MET | - | - |
| MP.L2-3.8.8 | Media protection: labeling, storage, sanitization (NIST SP 800-88) | Sayer Tindall | - | - | MET | - | - |
| MP.L2-3.8.9 | Media protection: labeling, storage, sanitization (NIST SP 800-88) | Sayer Tindall | - | - | MET | - | - |
| PE.L2-3.10.1 | CSP-inherited physical protection (Google IL4 data-center controls) | NV012 Affirming Official | - | - | MET | - | - |
| PE.L2-3.10.2 | CSP-inherited physical protection (Google IL4 data-center controls) | NV012 Affirming Official | - | - | MET | - | - |
| PE.L2-3.10.3 | Physical access (visitor log + badge + WFH agreements) | Sayer Tindall | - | - | MET | - | - |
| PE.L2-3.10.4 | Physical access (visitor log + badge + WFH agreements) | Sayer Tindall | - | - | MET | - | - |
| PE.L2-3.10.5 | Physical access (visitor log + badge + WFH agreements) | Sayer Tindall | - | - | MET | - | - |
| PE.L2-3.10.6 | Physical access (visitor log + badge + WFH agreements) | Sayer Tindall | - | - | MET | - | - |
| PS.L2-3.9.1 | Personnel security: background screening + offboarding | Sayer Tindall | - | - | MET | - | - |
| PS.L2-3.9.2 | Personnel security: background screening + offboarding | Sayer Tindall | - | - | MET | - | - |
| RA.L2-3.11.1 | Formal risk assessment + finding tracker | Sayer Tindall | - | - | MET | - | - |
| RA.L2-3.11.2 | GCP Security Command Center — vulnerability management | NV012 Affirming Official | nv012/all-covered/gcp_scc_findings.json | 4472a35663ce | MET | - | - |
| RA.L2-3.11.3 | Formal risk assessment + finding tracker | Sayer Tindall | - | - | MET | - | - |
| SC.L2-3.13.1 | GCP Org Policy: US-only resource locations + restricted service usage | NV012 Affirming Official | nv012/all-covered/gcp_org_policy_region.json | 385f07ca2e58, 5f8e7ef2f8ff | MET | - | - |
| SC.L2-3.13.10 | Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto) | NV012 Affirming Official | nv012/all-covered/gcp_sc_si_monitoring.json | 3923ae07c201 | MET | - | - |
| SC.L2-3.13.11 | Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto) | NV012 Affirming Official | nv012/all-covered/gcp_kms_cmvp.json | 3c4af60bc144 | MET | - | - |
| SC.L2-3.13.12 | Collaborative computing / mobile code / VoIP policies | Sayer Tindall | - | - | MET | - | - |
| SC.L2-3.13.13 | Collaborative computing / mobile code / VoIP policies | Sayer Tindall | - | - | MET | - | - |
| SC.L2-3.13.14 | Collaborative computing / mobile code / VoIP policies | Sayer Tindall | - | - | MET | - | - |
| SC.L2-3.13.15 | VPC network segmentation (subnetworks + firewalls + Cloud Armor) | NV012 Affirming Official | nv012/all-covered/gcp_vpc_segmentation.json | 2a64f51ac186 | MET | - | - |
| SC.L2-3.13.16 | Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto) | NV012 Affirming Official | nv012/all-covered/gcp_cmek_at_rest.json | 52eb61a61772 | MET | - | - |
| SC.L2-3.13.2 | Security engineering principles (NIST SP 800-160 Vol.1) | Sayer Tindall | - | - | MET | - | - |
| SC.L2-3.13.3 | VPC network segmentation (subnetworks + firewalls + Cloud Armor) | NV012 Affirming Official | nv012/all-covered/gcp_vpc_segmentation.json | 2a64f51ac186 | MET | - | - |
| SC.L2-3.13.4 | VPC network segmentation (subnetworks + firewalls + Cloud Armor) | NV012 Affirming Official | nv012/all-covered/gcp_vpc_segmentation.json | 2a64f51ac186 | MET | - | - |
| SC.L2-3.13.5 | VPC network segmentation (subnetworks + firewalls + Cloud Armor) | NV012 Affirming Official | nv012/all-covered/gcp_vpc_segmentation.json | 2a64f51ac186 | MET | - | - |
| SC.L2-3.13.6 | VPC network segmentation (subnetworks + firewalls + Cloud Armor) | NV012 Affirming Official | nv012/all-covered/gcp_vpc_segmentation.json | 2a64f51ac186 | MET | - | - |
| SC.L2-3.13.7 | VPC network segmentation (subnetworks + firewalls + Cloud Armor) | NV012 Affirming Official | nv012/all-covered/gcp_vpc_segmentation.json | 2a64f51ac186 | MET | - | - |
| SC.L2-3.13.8 | VPC network segmentation (subnetworks + firewalls + Cloud Armor) | NV012 Affirming Official | nv012/all-covered/gcp_vpc_segmentation.json | 2a64f51ac186 | MET | - | - |
| SC.L2-3.13.9 | VPC network segmentation (subnetworks + firewalls + Cloud Armor) | NV012 Affirming Official | nv012/all-covered/gcp_vpc_segmentation.json | 2a64f51ac186 | MET | - | - |
| SI.L2-3.14.1 | GCP Security Command Center — vulnerability management | NV012 Affirming Official | nv012/all-covered/gcp_scc_findings.json | 4472a35663ce | MET | - | - |
| SI.L2-3.14.2 | CrowdStrike Falcon EDR — malware + endpoint integrity | NV012 Affirming Official | nv012/all-covered/crowdstrike_edr.json | 78748c996698 | MET | - | - |
| SI.L2-3.14.3 | Cloud Monitoring + Workspace Alert Center (security alert monitoring/response) | NV012 Affirming Official | nv012/all-covered/gcp_sc_si_monitoring.json | 3923ae07c201 | MET | - | - |
| SI.L2-3.14.4 | CrowdStrike Falcon EDR — malware + endpoint integrity | NV012 Affirming Official | nv012/all-covered/crowdstrike_edr.json | 78748c996698 | MET | - | - |
| SI.L2-3.14.5 | GCP Security Command Center — vulnerability management | NV012 Affirming Official | nv012/all-covered/gcp_scc_findings.json | 4472a35663ce | MET | - | - |
| SI.L2-3.14.6 | Cloud Monitoring + Workspace Alert Center (security alert monitoring/response) | NV012 Affirming Official | nv012/all-covered/gcp_sc_si_monitoring.json | 3923ae07c201 | MET | - | - |
| SI.L2-3.14.7 | CrowdStrike Falcon EDR — malware + endpoint integrity | NV012 Affirming Official | nv012/all-covered/crowdstrike_edr.json | 78748c996698 | MET | - | - |

## 4. Per-control detail

### AC.L2-3.1.1

**Statement.** Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: IAM groups + least-privilege role bindings for CUI access
- Verification method: oracle-iam-least-privilege

- Attestation: ATT-AC.L2-3.1.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.879189+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.10

**Statement.** Use session lock with pattern-hiding displays to prevent access and viewing of data after a period of inactivity.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud Identity session control + failed-login lockout
- Verification method: oracle-session-control

- Attestation: ATT-AC.L2-3.1.10 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.893680+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.11

**Statement.** Terminate (automatically) a user session after a defined condition.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud Identity session control + failed-login lockout
- Verification method: oracle-session-control

- Attestation: ATT-AC.L2-3.1.11 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.906487+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.12

**Statement.** Monitor and control remote access sessions.

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: BeyondCorp Enterprise remote access + TLS enforcement
- Verification method: oracle-beyondcorp-remote-access

- Attestation: ATT-AC.L2-3.1.12 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.918916+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.13

**Statement.** Employ cryptographic mechanisms to protect the confidentiality of remote access sessions.

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: BeyondCorp Enterprise remote access + TLS enforcement
- Verification method: oracle-beyondcorp-remote-access

- Attestation: ATT-AC.L2-3.1.13 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.932787+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.14

**Statement.** Route remote access via managed access control points.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: BeyondCorp Enterprise remote access + TLS enforcement
- Verification method: oracle-beyondcorp-remote-access

- Attestation: ATT-AC.L2-3.1.14 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.945292+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.15

**Statement.** Authorize remote execution of privileged commands and remote access to security-relevant information.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Remote access authorization (SSP appendix)
- Verification method: oracle-attested-reference

- Attestation: ATT-AC.L2-3.1.15 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:10.958455+00:00
  - Adequacy assumption: Written authorization for remote privileged execution; portable storage prohibited on external systems; no CUI on publicly accessible systems.
  - Sufficiency justification: SSP appendix reviewed and signed within annual cadence.

### AC.L2-3.1.16

**Statement.** Authorize wireless access prior to allowing such connections.

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: Chrome Cloud Management + Endpoint Verification (MDM)
- Verification method: oracle-mdm-policy

- Attestation: ATT-AC.L2-3.1.16 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.971267+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.17

**Statement.** Protect wireless access using authentication and encryption.

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: Chrome Cloud Management + Endpoint Verification (MDM)
- Verification method: oracle-mdm-policy

- Attestation: ATT-AC.L2-3.1.17 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.984282+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.18

**Statement.** Control connection of mobile devices.

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: Chrome Cloud Management + Endpoint Verification (MDM)
- Verification method: oracle-mdm-policy

- Attestation: ATT-AC.L2-3.1.18 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:10.997215+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.19

**Statement.** Encrypt CUI on mobile devices and mobile computing platforms.

- Family: AC · Weight: 3 · POA&M-eligible: false
- Implementation: Chrome Cloud Management + Endpoint Verification (MDM)
- Verification method: oracle-mdm-policy

- Attestation: ATT-AC.L2-3.1.19 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.010453+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.2

**Statement.** Limit system access to the types of transactions and functions that authorized users are permitted to execute.

- Family: AC · Weight: 5 · POA&M-eligible: false
- Implementation: IAM groups + least-privilege role bindings for CUI access
- Verification method: oracle-iam-least-privilege

- Attestation: ATT-AC.L2-3.1.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.023311+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.20

**Statement.** Verify and control/limit connections to and use of external systems.

- Family: AC · Weight: 1 · POA&M-eligible: false
- Implementation: VPC Service Controls perimeter — external system authorization
- Verification method: oracle-vpc-sc-perimeter

- Attestation: ATT-AC.L2-3.1.20 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.036071+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.21

**Statement.** Limit use of portable storage devices on external systems.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Remote access authorization (SSP appendix)
- Verification method: oracle-attested-reference

- Attestation: ATT-AC.L2-3.1.21 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.048705+00:00
  - Adequacy assumption: Written authorization for remote privileged execution; portable storage prohibited on external systems; no CUI on publicly accessible systems.
  - Sufficiency justification: SSP appendix reviewed and signed within annual cadence.

### AC.L2-3.1.22

**Statement.** Control CUI posted or processed on publicly accessible systems.

- Family: AC · Weight: 1 · POA&M-eligible: false
- Implementation: Remote access authorization (SSP appendix)
- Verification method: oracle-attested-reference

- Attestation: ATT-AC.L2-3.1.22 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.061202+00:00
  - Adequacy assumption: Written authorization for remote privileged execution; portable storage prohibited on external systems; no CUI on publicly accessible systems.
  - Sufficiency justification: SSP appendix reviewed and signed within annual cadence.

### AC.L2-3.1.3

**Statement.** Control the flow of CUI in accordance with approved authorizations.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Drive + Gmail DLP rules (control the flow of CUI)
- Verification method: oracle-drive-dlp-rules

- Attestation: ATT-AC.L2-3.1.3 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.073870+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.4

**Statement.** Separate the duties of individuals to reduce the risk of malevolent activity without collusion.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Separation of duties (RACI matrix)
- Verification method: oracle-attested-reference

- Attestation: ATT-AC.L2-3.1.4 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.087226+00:00
  - Adequacy assumption: RACI matrix separates approval from execution for sensitive changes; GitHub required-reviewers enforces technically.
  - Sufficiency justification: RACI matrix + branch-protection config reviewed within annual cadence.

### AC.L2-3.1.5

**Statement.** Employ the principle of least privilege, including for specific security functions and privileged accounts.

- Family: AC · Weight: 3 · POA&M-eligible: false
- Implementation: IAM groups + least-privilege role bindings for CUI access
- Verification method: oracle-iam-least-privilege

- Attestation: ATT-AC.L2-3.1.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.100303+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.6

**Statement.** Use non-privileged accounts or roles when accessing nonsecurity functions.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: GCP IAM policy + audit-log signals for privileged use
- Verification method: oracle-iam-privileged-use

- Attestation: ATT-AC.L2-3.1.6 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.112990+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.7

**Statement.** Prevent non-privileged users from executing privileged functions and capture the execution of such functions in audit logs.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: GCP IAM policy + audit-log signals for privileged use
- Verification method: oracle-iam-privileged-use

- Attestation: ATT-AC.L2-3.1.7 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.125970+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.8

**Statement.** Limit unsuccessful logon attempts.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud Identity session control + failed-login lockout
- Verification method: oracle-session-control

- Attestation: ATT-AC.L2-3.1.8 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.138527+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AC.L2-3.1.9

**Statement.** Provide privacy and security notices consistent with applicable CUI rules.

- Family: AC · Weight: 1 · POA&M-eligible: true
- Implementation: Login banner policy (system-use notification)
- Verification method: oracle-attested-reference

- Attestation: ATT-AC.L2-3.1.9 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.151427+00:00
  - Adequacy assumption: Login banner text (U.S. Government interest, consent to monitoring, DoD warning) present at all CUI system logins.
  - Sufficiency justification: Workspace + GCP + VPN banners verified; policy doc reviewed within annual cadence.

### AT.L2-3.2.1

**Statement.** Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of the applicable policies, standards, and procedures related to the security of those systems.

- Family: AT · Weight: 5 · POA&M-eligible: false
- Implementation: Annual security awareness + role-based training program
- Verification method: oracle-attested-reference

- Attestation: ATT-AT.L2-3.2.1 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.164675+00:00
  - Adequacy assumption: Annual training program covers CUI handling, phishing, insider threat, mobile device, and role-based ops/eng content.
  - Sufficiency justification: LMS completion records on file for all personnel with CUI system access for the current cycle.

### AT.L2-3.2.2

**Statement.** Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.

- Family: AT · Weight: 5 · POA&M-eligible: false
- Implementation: Annual security awareness + role-based training program
- Verification method: oracle-attested-reference

- Attestation: ATT-AT.L2-3.2.2 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.178054+00:00
  - Adequacy assumption: Annual training program covers CUI handling, phishing, insider threat, mobile device, and role-based ops/eng content.
  - Sufficiency justification: LMS completion records on file for all personnel with CUI system access for the current cycle.

### AT.L2-3.2.3

**Statement.** Provide security awareness training on recognizing and reporting potential indicators of insider threat.

- Family: AT · Weight: 1 · POA&M-eligible: true
- Implementation: Annual security awareness + role-based training program
- Verification method: oracle-attested-reference

- Attestation: ATT-AT.L2-3.2.3 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.190952+00:00
  - Adequacy assumption: Annual training program covers CUI handling, phishing, insider threat, mobile device, and role-based ops/eng content.
  - Sufficiency justification: LMS completion records on file for all personnel with CUI system access for the current cycle.

### AU.L2-3.3.1

**Statement.** Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.

- Family: AU · Weight: 5 · POA&M-eligible: false
- Implementation: Workspace + GCP audit log export to retained Cloud Storage bucket
- Verification method: oracle-auditlog-export

- Attestation: ATT-AU.L2-3.3.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.203691+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AU.L2-3.3.2

**Statement.** Ensure that the actions of individual system users can be uniquely traced to those users, so they can be held accountable for their actions.

- Family: AU · Weight: 3 · POA&M-eligible: false
- Implementation: Workspace + GCP audit log export to retained Cloud Storage bucket
- Verification method: oracle-auditlog-export

- Attestation: ATT-AU.L2-3.3.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.216866+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AU.L2-3.3.3

**Statement.** Review and update logged events.

- Family: AU · Weight: 1 · POA&M-eligible: true
- Implementation: Audit management procedure (log review cadence + reports)
- Verification method: oracle-attested-reference

- Attestation: ATT-AU.L2-3.3.3 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.230024+00:00
  - Adequacy assumption: Audit procedure defines logged event types + review cadence + report generation.
  - Sufficiency justification: Procedure doc + sample log review report reviewed within 90-day cadence.

### AU.L2-3.3.4

**Statement.** Alert in the event of an audit logging process failure.

- Family: AU · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud Logging sinks + NTP + IAM on log buckets
- Verification method: oracle-cloud-logging-config

- Attestation: ATT-AU.L2-3.3.4 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.242902+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AU.L2-3.3.5

**Statement.** Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.

- Family: AU · Weight: 5 · POA&M-eligible: false
- Implementation: Workspace + GCP audit log export to retained Cloud Storage bucket
- Verification method: oracle-auditlog-export

- Attestation: ATT-AU.L2-3.3.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.255758+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AU.L2-3.3.6

**Statement.** Provide audit record reduction and report generation to support on-demand analysis and reporting.

- Family: AU · Weight: 1 · POA&M-eligible: true
- Implementation: Audit management procedure (log review cadence + reports)
- Verification method: oracle-attested-reference

- Attestation: ATT-AU.L2-3.3.6 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.268327+00:00
  - Adequacy assumption: Audit procedure defines logged event types + review cadence + report generation.
  - Sufficiency justification: Procedure doc + sample log review report reviewed within 90-day cadence.

### AU.L2-3.3.7

**Statement.** Provide a system capability that compares and synchronizes internal system clocks with an authoritative source to generate time stamps for audit records.

- Family: AU · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud Logging sinks + NTP + IAM on log buckets
- Verification method: oracle-cloud-logging-config

- Attestation: ATT-AU.L2-3.3.7 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.281454+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AU.L2-3.3.8

**Statement.** Protect audit information and audit logging tools from unauthorized access, modification, and deletion.

- Family: AU · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud Logging sinks + NTP + IAM on log buckets
- Verification method: oracle-cloud-logging-config

- Attestation: ATT-AU.L2-3.3.8 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.294600+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### AU.L2-3.3.9

**Statement.** Limit management of audit logging functionality to a subset of privileged users.

- Family: AU · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud Logging sinks + NTP + IAM on log buckets
- Verification method: oracle-cloud-logging-config

- Attestation: ATT-AU.L2-3.3.9 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.307749+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### CA.L2-3.12.1

**Statement.** Periodically assess the security controls in organizational systems to determine if the controls are effective in their application.

- Family: CA · Weight: 5 · POA&M-eligible: false
- Implementation: Continuous monitoring: engine run history + POA&M tracker
- Verification method: oracle-attested-reference

- Attestation: ATT-CA.L2-3.12.1 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.330231+00:00
  - Adequacy assumption: Continuous monitoring program defines events, cadence, reviewer, and POA&M process; annual self-assessment scheduled using this compliance engine.
  - Sufficiency justification: Engine run history + POA&M tracker current within 90-day cadence.

### CA.L2-3.12.2

**Statement.** Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational systems.

- Family: CA · Weight: 3 · POA&M-eligible: false
- Implementation: Continuous monitoring: engine run history + POA&M tracker
- Verification method: oracle-attested-reference

- Attestation: ATT-CA.L2-3.12.2 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.343742+00:00
  - Adequacy assumption: Continuous monitoring program defines events, cadence, reviewer, and POA&M process; annual self-assessment scheduled using this compliance engine.
  - Sufficiency justification: Engine run history + POA&M tracker current within 90-day cadence.

### CA.L2-3.12.3

**Statement.** Monitor security controls on an ongoing basis to ensure the continued effectiveness of the controls.

- Family: CA · Weight: 5 · POA&M-eligible: false
- Implementation: Continuous monitoring: engine run history + POA&M tracker
- Verification method: oracle-attested-reference

- Attestation: ATT-CA.L2-3.12.3 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.356859+00:00
  - Adequacy assumption: Continuous monitoring program defines events, cadence, reviewer, and POA&M process; annual self-assessment scheduled using this compliance engine.
  - Sufficiency justification: Engine run history + POA&M tracker current within 90-day cadence.

### CA.L2-3.12.4

**Statement.** Develop, document, and periodically update system security plans that describe system boundaries, system environments of operation, how security requirements are implemented, and the relationships with or connections to other systems.

- Family: CA · Weight: 1 · POA&M-eligible: false
- Implementation: System Security Plan supplement (system description)
- Verification method: oracle-attested-reference

- Attestation: ATT-CA.L2-3.12.4 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.370282+00:00
  - Adequacy assumption: System description supplement accurately captures the CUI system (Workspace + GCP Assured Workloads IL4), authorized users, data flows, and interconnections.
  - Sufficiency justification: Signed by the Affirming Official; matches the as-built configuration.

### CM.L2-3.4.1

**Statement.** Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Terraform baseline configuration + resource inventory (IaC)
- Verification method: oracle-terraform-baseline

- Attestation: ATT-CM.L2-3.4.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.383560+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### CM.L2-3.4.2

**Statement.** Establish and enforce security configuration settings for information technology products employed in organizational systems.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Terraform baseline configuration + resource inventory (IaC)
- Verification method: oracle-terraform-baseline

- Attestation: ATT-CM.L2-3.4.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.396795+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### CM.L2-3.4.3

**Statement.** Track, review, approve or disapprove, and log changes to organizational systems.

- Family: CM · Weight: 1 · POA&M-eligible: true
- Implementation: GitHub branch protection + required reviews
- Verification method: oracle-github-change-mgmt

- Attestation: ATT-CM.L2-3.4.3 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.409881+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### CM.L2-3.4.4

**Statement.** Analyze the security impact of changes prior to implementation.

- Family: CM · Weight: 1 · POA&M-eligible: true
- Implementation: Configuration management: security impact analysis procedure
- Verification method: oracle-attested-reference

- Attestation: ATT-CM.L2-3.4.4 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.423498+00:00
  - Adequacy assumption: SIA procedure requires impact analysis before any CUI-affecting config change; user-installed software requires written approval.
  - Sufficiency justification: GitHub change log + procedure doc reviewed within 180-day cadence.

### CM.L2-3.4.5

**Statement.** Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational systems.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: GitHub branch protection + required reviews
- Verification method: oracle-github-change-mgmt

- Attestation: ATT-CM.L2-3.4.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.436372+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### CM.L2-3.4.6

**Statement.** Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Disable non-FedRAMP-authorized services for the CUI OU (least functionality)
- Verification method: oracle-restrict-service-usage

- Attestation: ATT-CM.L2-3.4.6 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.450073+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### CM.L2-3.4.7

**Statement.** Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Disable non-FedRAMP-authorized services for the CUI OU (least functionality)
- Verification method: oracle-restrict-service-usage

- Attestation: ATT-CM.L2-3.4.7 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.463453+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### CM.L2-3.4.8

**Statement.** Apply deny-by-exception (blacklisting) policy to prevent the use of unauthorized software or deny-all, permit-by-exception (whitelisting) policy to allow the execution of authorized software.

- Family: CM · Weight: 5 · POA&M-eligible: false
- Implementation: Binary Authorization — image allowlist / user-installed software
- Verification method: oracle-binauth-allowlist

- Attestation: ATT-CM.L2-3.4.8 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.476818+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### CM.L2-3.4.9

**Statement.** Control and monitor user-installed software.

- Family: CM · Weight: 1 · POA&M-eligible: true
- Implementation: Binary Authorization — image allowlist / user-installed software
- Verification method: oracle-binauth-allowlist

- Attestation: ATT-CM.L2-3.4.9 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.489867+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.1

**Statement.** Identify system users, processes acting on behalf of users, and devices.

- Family: IA · Weight: 5 · POA&M-eligible: false
- Implementation: Workspace Admin identity lifecycle + password policy
- Verification method: oracle-workspace-admin-policy

- Attestation: ATT-IA.L2-3.5.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.502932+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.10

**Statement.** Store and transmit only cryptographically-protected passwords.

- Family: IA · Weight: 5 · POA&M-eligible: false
- Implementation: Workspace Admin identity lifecycle + password policy
- Verification method: oracle-workspace-admin-policy

- Attestation: ATT-IA.L2-3.5.10 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.516186+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.11

**Statement.** Obscure feedback of authentication information.

- Family: IA · Weight: 1 · POA&M-eligible: true
- Implementation: Workspace Admin identity lifecycle + password policy
- Verification method: oracle-workspace-admin-policy

- Attestation: ATT-IA.L2-3.5.11 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.529209+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.2

**Statement.** Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems.

- Family: IA · Weight: 5 · POA&M-eligible: false
- Implementation: Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU
- Verification method: oracle-mfa-2sv-enforced

- Attestation: ATT-IA.L2-3.5.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.542653+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.3

**Statement.** Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.

- Family: IA · Weight: 5 · POA&M-eligible: false
- Implementation: Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU
- Verification method: oracle-mfa-2sv-enforced

- Attestation: ATT-IA.L2-3.5.3 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.556532+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.4

**Statement.** Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.

- Family: IA · Weight: 1 · POA&M-eligible: true
- Implementation: Google Workspace 2-Step Verification (phishing-resistant) enforced on CUI OU
- Verification method: oracle-mfa-2sv-enforced

- Attestation: ATT-IA.L2-3.5.4 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.569463+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.5

**Statement.** Prevent reuse of identifiers for a defined period.

- Family: IA · Weight: 1 · POA&M-eligible: true
- Implementation: Workspace Admin identity lifecycle + password policy
- Verification method: oracle-workspace-admin-policy

- Attestation: ATT-IA.L2-3.5.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.582509+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.6

**Statement.** Disable identifiers after a defined period of inactivity.

- Family: IA · Weight: 1 · POA&M-eligible: true
- Implementation: Workspace Admin identity lifecycle + password policy
- Verification method: oracle-workspace-admin-policy

- Attestation: ATT-IA.L2-3.5.6 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.595482+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.7

**Statement.** Enforce a minimum password complexity and change of characters when new passwords are created.

- Family: IA · Weight: 1 · POA&M-eligible: true
- Implementation: Workspace Admin identity lifecycle + password policy
- Verification method: oracle-workspace-admin-policy

- Attestation: ATT-IA.L2-3.5.7 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.608612+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.8

**Statement.** Prohibit password reuse for a specified number of generations.

- Family: IA · Weight: 1 · POA&M-eligible: true
- Implementation: Workspace Admin identity lifecycle + password policy
- Verification method: oracle-workspace-admin-policy

- Attestation: ATT-IA.L2-3.5.8 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.621450+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IA.L2-3.5.9

**Statement.** Allow temporary password use for system logons with an immediate change to a permanent password.

- Family: IA · Weight: 1 · POA&M-eligible: true
- Implementation: Workspace Admin identity lifecycle + password policy
- Verification method: oracle-workspace-admin-policy

- Attestation: ATT-IA.L2-3.5.9 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.635287+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### IR.L2-3.6.1

**Statement.** Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.

- Family: IR · Weight: 5 · POA&M-eligible: false
- Implementation: Incident Response Plan + annual tabletop exercise
- Verification method: oracle-attested-reference

- Attestation: ATT-IR.L2-3.6.1 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.648153+00:00
  - Adequacy assumption: IR plan defines IC/Security Officer roles, detection criteria, escalation, and DoD/CISA 72-hour reporting chain.
  - Sufficiency justification: 2026 tabletop exercise completed and report on file; plan reviewed within annual cadence.

### IR.L2-3.6.2

**Statement.** Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization.

- Family: IR · Weight: 5 · POA&M-eligible: false
- Implementation: Incident Response Plan + annual tabletop exercise
- Verification method: oracle-attested-reference

- Attestation: ATT-IR.L2-3.6.2 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.661221+00:00
  - Adequacy assumption: IR plan defines IC/Security Officer roles, detection criteria, escalation, and DoD/CISA 72-hour reporting chain.
  - Sufficiency justification: 2026 tabletop exercise completed and report on file; plan reviewed within annual cadence.

### IR.L2-3.6.3

**Statement.** Test the organizational incident response capability.

- Family: IR · Weight: 1 · POA&M-eligible: true
- Implementation: Incident Response Plan + annual tabletop exercise
- Verification method: oracle-attested-reference

- Attestation: ATT-IR.L2-3.6.3 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.674140+00:00
  - Adequacy assumption: IR plan defines IC/Security Officer roles, detection criteria, escalation, and DoD/CISA 72-hour reporting chain.
  - Sufficiency justification: 2026 tabletop exercise completed and report on file; plan reviewed within annual cadence.

### MA.L2-3.7.1

**Statement.** Perform maintenance on organizational systems.

- Family: MA · Weight: 3 · POA&M-eligible: false
- Implementation: Maintenance policy: approved vendor list + maintenance log
- Verification method: oracle-attested-reference

- Attestation: ATT-MA.L2-3.7.1 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.686758+00:00
  - Adequacy assumption: Approved-vendor list current; sanitization procedure before off-site maintenance; diagnostic media scan procedure; escort policy for visitor maintenance.
  - Sufficiency justification: Vendor list signed; maintenance event log current.

### MA.L2-3.7.2

**Statement.** Provide controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance.

- Family: MA · Weight: 5 · POA&M-eligible: false
- Implementation: Maintenance policy: approved vendor list + maintenance log
- Verification method: oracle-attested-reference

- Attestation: ATT-MA.L2-3.7.2 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.699574+00:00
  - Adequacy assumption: Approved-vendor list current; sanitization procedure before off-site maintenance; diagnostic media scan procedure; escort policy for visitor maintenance.
  - Sufficiency justification: Vendor list signed; maintenance event log current.

### MA.L2-3.7.3

**Statement.** Ensure equipment removed for off-site maintenance is sanitized of any CUI.

- Family: MA · Weight: 1 · POA&M-eligible: true
- Implementation: Maintenance policy: approved vendor list + maintenance log
- Verification method: oracle-attested-reference

- Attestation: ATT-MA.L2-3.7.3 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.712938+00:00
  - Adequacy assumption: Approved-vendor list current; sanitization procedure before off-site maintenance; diagnostic media scan procedure; escort policy for visitor maintenance.
  - Sufficiency justification: Vendor list signed; maintenance event log current.

### MA.L2-3.7.4

**Statement.** Check media containing diagnostic and test programs for malicious code before the media are used in organizational systems.

- Family: MA · Weight: 3 · POA&M-eligible: false
- Implementation: Maintenance policy: approved vendor list + maintenance log
- Verification method: oracle-attested-reference

- Attestation: ATT-MA.L2-3.7.4 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.725832+00:00
  - Adequacy assumption: Approved-vendor list current; sanitization procedure before off-site maintenance; diagnostic media scan procedure; escort policy for visitor maintenance.
  - Sufficiency justification: Vendor list signed; maintenance event log current.

### MA.L2-3.7.5

**Statement.** Require multifactor authentication to establish nonlocal maintenance sessions via external network connections and terminate such connections when nonlocal maintenance is complete.

- Family: MA · Weight: 5 · POA&M-eligible: false
- Implementation: Cloud Identity MFA for ops / break-glass roles
- Verification method: oracle-remote-maintenance-mfa

- Attestation: ATT-MA.L2-3.7.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.738687+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### MA.L2-3.7.6

**Statement.** Supervise the maintenance activities of maintenance personnel without required access authorization.

- Family: MA · Weight: 1 · POA&M-eligible: true
- Implementation: Maintenance policy: approved vendor list + maintenance log
- Verification method: oracle-attested-reference

- Attestation: ATT-MA.L2-3.7.6 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.751771+00:00
  - Adequacy assumption: Approved-vendor list current; sanitization procedure before off-site maintenance; diagnostic media scan procedure; escort policy for visitor maintenance.
  - Sufficiency justification: Vendor list signed; maintenance event log current.

### MP.L2-3.8.1

**Statement.** Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital.

- Family: MP · Weight: 3 · POA&M-eligible: false
- Implementation: Media protection: labeling, storage, sanitization (NIST SP 800-88)
- Verification method: oracle-attested-reference

- Attestation: ATT-MP.L2-3.8.1 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.764703+00:00
  - Adequacy assumption: Media labeled per NARA 32 CFR Part 2002; storage + access controls documented; sanitization per NIST SP 800-88 Rev.1.
  - Sufficiency justification: Media inventory + at least one sanitization record on file; portable storage policy enforced via MDM.

### MP.L2-3.8.2

**Statement.** Limit access to CUI on system media to authorized users.

- Family: MP · Weight: 3 · POA&M-eligible: false
- Implementation: Media protection: labeling, storage, sanitization (NIST SP 800-88)
- Verification method: oracle-attested-reference

- Attestation: ATT-MP.L2-3.8.2 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.778250+00:00
  - Adequacy assumption: Media labeled per NARA 32 CFR Part 2002; storage + access controls documented; sanitization per NIST SP 800-88 Rev.1.
  - Sufficiency justification: Media inventory + at least one sanitization record on file; portable storage policy enforced via MDM.

### MP.L2-3.8.3

**Statement.** Sanitize or destroy system media containing CUI before disposal or release for reuse.

- Family: MP · Weight: 5 · POA&M-eligible: false
- Implementation: Media protection: labeling, storage, sanitization (NIST SP 800-88)
- Verification method: oracle-attested-reference

- Attestation: ATT-MP.L2-3.8.3 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.790931+00:00
  - Adequacy assumption: Media labeled per NARA 32 CFR Part 2002; storage + access controls documented; sanitization per NIST SP 800-88 Rev.1.
  - Sufficiency justification: Media inventory + at least one sanitization record on file; portable storage policy enforced via MDM.

### MP.L2-3.8.4

**Statement.** Mark media with necessary CUI markings and distribution limitations.

- Family: MP · Weight: 1 · POA&M-eligible: true
- Implementation: Media protection: labeling, storage, sanitization (NIST SP 800-88)
- Verification method: oracle-attested-reference

- Attestation: ATT-MP.L2-3.8.4 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.803342+00:00
  - Adequacy assumption: Media labeled per NARA 32 CFR Part 2002; storage + access controls documented; sanitization per NIST SP 800-88 Rev.1.
  - Sufficiency justification: Media inventory + at least one sanitization record on file; portable storage policy enforced via MDM.

### MP.L2-3.8.5

**Statement.** Control access to media containing CUI and maintain accountability for media during transport outside of controlled areas.

- Family: MP · Weight: 1 · POA&M-eligible: true
- Implementation: Media protection: labeling, storage, sanitization (NIST SP 800-88)
- Verification method: oracle-attested-reference

- Attestation: ATT-MP.L2-3.8.5 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.816147+00:00
  - Adequacy assumption: Media labeled per NARA 32 CFR Part 2002; storage + access controls documented; sanitization per NIST SP 800-88 Rev.1.
  - Sufficiency justification: Media inventory + at least one sanitization record on file; portable storage policy enforced via MDM.

### MP.L2-3.8.6

**Statement.** Implement cryptographic mechanisms to protect the confidentiality of CUI stored on digital media during transport unless otherwise protected by alternative physical safeguards.

- Family: MP · Weight: 1 · POA&M-eligible: true
- Implementation: Media protection: labeling, storage, sanitization (NIST SP 800-88)
- Verification method: oracle-attested-reference

- Attestation: ATT-MP.L2-3.8.6 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.828952+00:00
  - Adequacy assumption: Media labeled per NARA 32 CFR Part 2002; storage + access controls documented; sanitization per NIST SP 800-88 Rev.1.
  - Sufficiency justification: Media inventory + at least one sanitization record on file; portable storage policy enforced via MDM.

### MP.L2-3.8.7

**Statement.** Control the use of removable media on system components.

- Family: MP · Weight: 5 · POA&M-eligible: false
- Implementation: Chrome Cloud Management + Endpoint Verification (MDM)
- Verification method: oracle-mdm-policy

- Attestation: ATT-MP.L2-3.8.7 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.841566+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### MP.L2-3.8.8

**Statement.** Prohibit the use of portable storage devices when such devices have no identifiable owner.

- Family: MP · Weight: 3 · POA&M-eligible: false
- Implementation: Media protection: labeling, storage, sanitization (NIST SP 800-88)
- Verification method: oracle-attested-reference

- Attestation: ATT-MP.L2-3.8.8 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.854470+00:00
  - Adequacy assumption: Media labeled per NARA 32 CFR Part 2002; storage + access controls documented; sanitization per NIST SP 800-88 Rev.1.
  - Sufficiency justification: Media inventory + at least one sanitization record on file; portable storage policy enforced via MDM.

### MP.L2-3.8.9

**Statement.** Protect the confidentiality of backup CUI at storage locations.

- Family: MP · Weight: 1 · POA&M-eligible: true
- Implementation: Media protection: labeling, storage, sanitization (NIST SP 800-88)
- Verification method: oracle-attested-reference

- Attestation: ATT-MP.L2-3.8.9 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.867690+00:00
  - Adequacy assumption: Media labeled per NARA 32 CFR Part 2002; storage + access controls documented; sanitization per NIST SP 800-88 Rev.1.
  - Sufficiency justification: Media inventory + at least one sanitization record on file; portable storage policy enforced via MDM.

### PE.L2-3.10.1

**Statement.** Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals.

- Family: PE · Weight: 5 · POA&M-eligible: false
- Implementation: CSP-inherited physical protection (Google IL4 data-center controls)
- Verification method: inherited:google-workspace-crm

- Attestation: ATT-PE.L2-3.10.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.880256+00:00
  - Adequacy assumption: Control satisfied by the cloud service provider and inherited.
  - Sufficiency justification: CSP shared-responsibility inheritance; no customer-side machine check applies.

### PE.L2-3.10.2

**Statement.** Protect and monitor the physical facility and support infrastructure for organizational systems.

- Family: PE · Weight: 5 · POA&M-eligible: false
- Implementation: CSP-inherited physical protection (Google IL4 data-center controls)
- Verification method: inherited:google-workspace-crm

- Attestation: ATT-PE.L2-3.10.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.892921+00:00
  - Adequacy assumption: Control satisfied by the cloud service provider and inherited.
  - Sufficiency justification: CSP shared-responsibility inheritance; no customer-side machine check applies.

### PE.L2-3.10.3

**Statement.** Escort visitors and monitor visitor activity.

- Family: PE · Weight: 1 · POA&M-eligible: false
- Implementation: Physical access (visitor log + badge + WFH agreements)
- Verification method: oracle-attested-reference

- Attestation: ATT-PE.L2-3.10.3 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.905591+00:00
  - Adequacy assumption: Visitor escort policy + visitor log; badge issuance/revocation procedure; WFH agreements per employee define alternate-work-site CUI safeguards.
  - Sufficiency justification: Visitor log + badge log + WFH agreements on file; annual review complete.

### PE.L2-3.10.4

**Statement.** Maintain audit logs of physical access.

- Family: PE · Weight: 1 · POA&M-eligible: false
- Implementation: Physical access (visitor log + badge + WFH agreements)
- Verification method: oracle-attested-reference

- Attestation: ATT-PE.L2-3.10.4 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.918184+00:00
  - Adequacy assumption: Visitor escort policy + visitor log; badge issuance/revocation procedure; WFH agreements per employee define alternate-work-site CUI safeguards.
  - Sufficiency justification: Visitor log + badge log + WFH agreements on file; annual review complete.

### PE.L2-3.10.5

**Statement.** Control and manage physical access devices.

- Family: PE · Weight: 1 · POA&M-eligible: false
- Implementation: Physical access (visitor log + badge + WFH agreements)
- Verification method: oracle-attested-reference

- Attestation: ATT-PE.L2-3.10.5 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.931240+00:00
  - Adequacy assumption: Visitor escort policy + visitor log; badge issuance/revocation procedure; WFH agreements per employee define alternate-work-site CUI safeguards.
  - Sufficiency justification: Visitor log + badge log + WFH agreements on file; annual review complete.

### PE.L2-3.10.6

**Statement.** Enforce safeguarding measures for CUI at alternate work sites.

- Family: PE · Weight: 1 · POA&M-eligible: true
- Implementation: Physical access (visitor log + badge + WFH agreements)
- Verification method: oracle-attested-reference

- Attestation: ATT-PE.L2-3.10.6 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.943830+00:00
  - Adequacy assumption: Visitor escort policy + visitor log; badge issuance/revocation procedure; WFH agreements per employee define alternate-work-site CUI safeguards.
  - Sufficiency justification: Visitor log + badge log + WFH agreements on file; annual review complete.

### PS.L2-3.9.1

**Statement.** Screen individuals prior to authorizing access to organizational systems containing CUI.

- Family: PS · Weight: 3 · POA&M-eligible: false
- Implementation: Personnel security: background screening + offboarding
- Verification method: oracle-attested-reference

- Attestation: ATT-PS.L2-3.9.1 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.956382+00:00
  - Adequacy assumption: Background screening policy defines scope + frequency; offboarding checklist enforces revocation within 24h of separation.
  - Sufficiency justification: Background check attestations per employee on file; no ex-employees have active credentials as of last audit.

### PS.L2-3.9.2

**Statement.** Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers.

- Family: PS · Weight: 5 · POA&M-eligible: false
- Implementation: Personnel security: background screening + offboarding
- Verification method: oracle-attested-reference

- Attestation: ATT-PS.L2-3.9.2 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.968961+00:00
  - Adequacy assumption: Background screening policy defines scope + frequency; offboarding checklist enforces revocation within 24h of separation.
  - Sufficiency justification: Background check attestations per employee on file; no ex-employees have active credentials as of last audit.

### RA.L2-3.11.1

**Statement.** Periodically assess the risk to organizational operations (including mission, functions, image, or reputation), organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI.

- Family: RA · Weight: 3 · POA&M-eligible: false
- Implementation: Formal risk assessment + finding tracker
- Verification method: oracle-attested-reference

- Attestation: ATT-RA.L2-3.11.1 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:11.981398+00:00
  - Adequacy assumption: Risk assessment enumerates assets, threats, likelihood/impact ratings, and risk decisions.
  - Sufficiency justification: Signed dated assessment on file; finding tracker current with target remediation dates.

### RA.L2-3.11.2

**Statement.** Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities affecting those systems and applications are identified.

- Family: RA · Weight: 5 · POA&M-eligible: false
- Implementation: GCP Security Command Center — vulnerability management
- Verification method: oracle-scc-vuln-mgmt

- Attestation: ATT-RA.L2-3.11.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:11.993873+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### RA.L2-3.11.3

**Statement.** Remediate vulnerabilities in accordance with risk assessments.

- Family: RA · Weight: 1 · POA&M-eligible: true
- Implementation: Formal risk assessment + finding tracker
- Verification method: oracle-attested-reference

- Attestation: ATT-RA.L2-3.11.3 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:12.007380+00:00
  - Adequacy assumption: Risk assessment enumerates assets, threats, likelihood/impact ratings, and risk decisions.
  - Sufficiency justification: Signed dated assessment on file; finding tracker current with target remediation dates.

### SC.L2-3.13.1

**Statement.** Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems.

- Family: SC · Weight: 5 · POA&M-eligible: false
- Implementation: GCP Org Policy: US-only resource locations + restricted service usage
- Verification method: oracle-orgpolicy-us-residency

- Attestation: ATT-SC.L2-3.13.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.020322+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.10

**Statement.** Establish and manage cryptographic keys for cryptography employed in organizational systems.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto)
- Verification method: oracle-cmek-fips-keyring

- Attestation: ATT-SC.L2-3.13.10 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.033161+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.11

**Statement.** Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.

- Family: SC · Weight: 5 · POA&M-eligible: false
- Implementation: Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto)
- Verification method: oracle-cmek-fips-keyring

- Attestation: ATT-SC.L2-3.13.11 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.045851+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.12

**Statement.** Prohibit remote activation of collaborative computing devices and provide indication of devices in use to users present at the device.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: Collaborative computing / mobile code / VoIP policies
- Verification method: oracle-attested-reference

- Attestation: ATT-SC.L2-3.13.12 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:12.058913+00:00
  - Adequacy assumption: Camera/mic disable in CUI spaces; mobile code allowlist; VoIP usage policy.
  - Sufficiency justification: Workspace + device policies enforce; policy doc reviewed within annual cadence.

### SC.L2-3.13.13

**Statement.** Control and monitor the use of mobile code.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: Collaborative computing / mobile code / VoIP policies
- Verification method: oracle-attested-reference

- Attestation: ATT-SC.L2-3.13.13 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:12.072299+00:00
  - Adequacy assumption: Camera/mic disable in CUI spaces; mobile code allowlist; VoIP usage policy.
  - Sufficiency justification: Workspace + device policies enforce; policy doc reviewed within annual cadence.

### SC.L2-3.13.14

**Statement.** Control and monitor the use of Voice over Internet Protocol (VoIP) technologies.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: Collaborative computing / mobile code / VoIP policies
- Verification method: oracle-attested-reference

- Attestation: ATT-SC.L2-3.13.14 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:12.084862+00:00
  - Adequacy assumption: Camera/mic disable in CUI spaces; mobile code allowlist; VoIP usage policy.
  - Sufficiency justification: Workspace + device policies enforce; policy doc reviewed within annual cadence.

### SC.L2-3.13.15

**Statement.** Protect the authenticity of communications sessions.

- Family: SC · Weight: 5 · POA&M-eligible: false
- Implementation: VPC network segmentation (subnetworks + firewalls + Cloud Armor)
- Verification method: oracle-vpc-segmentation

- Attestation: ATT-SC.L2-3.13.15 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.097445+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.16

**Statement.** Protect the confidentiality of CUI at rest.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: Cloud KMS CMEK + Workspace CSE key management (FIPS-validated crypto)
- Verification method: oracle-cmek-fips-keyring

- Attestation: ATT-SC.L2-3.13.16 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.110062+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.2

**Statement.** Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational systems.

- Family: SC · Weight: 5 · POA&M-eligible: false
- Implementation: Security engineering principles (NIST SP 800-160 Vol.1)
- Verification method: oracle-attested-reference

- Attestation: ATT-SC.L2-3.13.2 — **MET** by Sayer Tindall
  - Timestamp: 2026-07-07T17:57:12.122446+00:00
  - Adequacy assumption: Security engineering principles document least privilege, defense in depth, fail-secure defaults, separation of duties, and minimized attack surface per NIST SP 800-160 Vol.1.
  - Sufficiency justification: Architecture review doc signed within annual cadence.

### SC.L2-3.13.3

**Statement.** Separate user functionality from system management functionality.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: VPC network segmentation (subnetworks + firewalls + Cloud Armor)
- Verification method: oracle-vpc-segmentation

- Attestation: ATT-SC.L2-3.13.3 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.135029+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.4

**Statement.** Prevent unauthorized and unintended information transfer via shared system resources.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: VPC network segmentation (subnetworks + firewalls + Cloud Armor)
- Verification method: oracle-vpc-segmentation

- Attestation: ATT-SC.L2-3.13.4 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.148204+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.5

**Statement.** Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.

- Family: SC · Weight: 5 · POA&M-eligible: false
- Implementation: VPC network segmentation (subnetworks + firewalls + Cloud Armor)
- Verification method: oracle-vpc-segmentation

- Attestation: ATT-SC.L2-3.13.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.160681+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.6

**Statement.** Deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception).

- Family: SC · Weight: 5 · POA&M-eligible: false
- Implementation: VPC network segmentation (subnetworks + firewalls + Cloud Armor)
- Verification method: oracle-vpc-segmentation

- Attestation: ATT-SC.L2-3.13.6 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.173240+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.7

**Statement.** Prevent remote devices from simultaneously establishing non-remote connections with organizational systems and communicating via some other connection to resources in external networks (i.e., split tunneling).

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: VPC network segmentation (subnetworks + firewalls + Cloud Armor)
- Verification method: oracle-vpc-segmentation

- Attestation: ATT-SC.L2-3.13.7 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.185848+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.8

**Statement.** Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards.

- Family: SC · Weight: 3 · POA&M-eligible: false
- Implementation: VPC network segmentation (subnetworks + firewalls + Cloud Armor)
- Verification method: oracle-vpc-segmentation

- Attestation: ATT-SC.L2-3.13.8 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.198719+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SC.L2-3.13.9

**Statement.** Terminate network connections associated with communications sessions at the end of the sessions or after a defined period of inactivity.

- Family: SC · Weight: 1 · POA&M-eligible: true
- Implementation: VPC network segmentation (subnetworks + firewalls + Cloud Armor)
- Verification method: oracle-vpc-segmentation

- Attestation: ATT-SC.L2-3.13.9 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.211259+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SI.L2-3.14.1

**Statement.** Identify, report, and correct system flaws in a timely manner.

- Family: SI · Weight: 5 · POA&M-eligible: false
- Implementation: GCP Security Command Center — vulnerability management
- Verification method: oracle-scc-vuln-mgmt

- Attestation: ATT-SI.L2-3.14.1 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.224619+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SI.L2-3.14.2

**Statement.** Provide protection from malicious code at designated locations within organizational systems.

- Family: SI · Weight: 5 · POA&M-eligible: false
- Implementation: CrowdStrike Falcon EDR — malware + endpoint integrity
- Verification method: oracle-endpoint-edr

- Attestation: ATT-SI.L2-3.14.2 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.237073+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SI.L2-3.14.3

**Statement.** Monitor system security alerts and advisories and take action in response.

- Family: SI · Weight: 5 · POA&M-eligible: false
- Implementation: Cloud Monitoring + Workspace Alert Center (security alert monitoring/response)
- Verification method: oracle-monitoring-alerts

- Attestation: ATT-SI.L2-3.14.3 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.250237+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SI.L2-3.14.4

**Statement.** Update malicious code protection mechanisms when new releases are available.

- Family: SI · Weight: 5 · POA&M-eligible: false
- Implementation: CrowdStrike Falcon EDR — malware + endpoint integrity
- Verification method: oracle-endpoint-edr

- Attestation: ATT-SI.L2-3.14.4 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.262798+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SI.L2-3.14.5

**Statement.** Perform periodic scans of organizational systems and real-time scans of files from external sources as files are downloaded, opened, or executed.

- Family: SI · Weight: 3 · POA&M-eligible: false
- Implementation: GCP Security Command Center — vulnerability management
- Verification method: oracle-scc-vuln-mgmt

- Attestation: ATT-SI.L2-3.14.5 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.275179+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SI.L2-3.14.6

**Statement.** Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.

- Family: SI · Weight: 5 · POA&M-eligible: false
- Implementation: Cloud Monitoring + Workspace Alert Center (security alert monitoring/response)
- Verification method: oracle-monitoring-alerts

- Attestation: ATT-SI.L2-3.14.6 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.287510+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

### SI.L2-3.14.7

**Statement.** Identify unauthorized use of organizational systems.

- Family: SI · Weight: 3 · POA&M-eligible: false
- Implementation: CrowdStrike Falcon EDR — malware + endpoint integrity
- Verification method: oracle-endpoint-edr

- Attestation: ATT-SI.L2-3.14.7 — **MET** by NV012 Affirming Official
  - Timestamp: 2026-07-07T17:57:12.300619+00:00
  - Adequacy assumption: Implementation reviewed against the provisioned configuration.
  - Sufficiency justification: Machine oracle + config evidence sufficient for the Phase-I mock run.

## 5. Colophon

| Layer | Named graph | Triples |
| --- | --- | --- |
| attestations | `http://dynamicalsystems.group/compliance-engine/attestations` | 2357 |
| audit | `http://dynamicalsystems.group/compliance-engine/audit` | 1783 |
| evidence | `http://dynamicalsystems.group/compliance-engine/evidence` | 786 |
| ontology | `http://dynamicalsystems.group/compliance-engine/ontology` | 1057 |
| order | `http://dynamicalsystems.group/compliance-engine/order` | 354 |
| plan | `http://dynamicalsystems.group/compliance-engine/plan` | 0 |
| plan_execution | `http://dynamicalsystems.group/compliance-engine/plan-execution` | 293 |
| structural | `http://dynamicalsystems.group/compliance-engine/structural` | 679 |

Dataset SHA-256: `7610cea52d9f174ce5501cc7aaa5264b76ab088fd316ec4fd06485d67888f136`

Document date (max prov:generatedAtTime): 2026-07-07T17:57:12.300619+00:00

SPRS summary: score 110 (Final); 108 MET-by-machine / 2 MET-by-human-only; contradictions: 0.

Artifact hashes (BOM): 82

- `00693338fb29c30f553937069f1ec3b7285cd4f02a089d18e8d029522c40e3ea`
- `00bcfd580b52bafaf2228a159b675c11b06b6719d36a470c54510daf45192841`
- `02b35ae9966c949a3a8b050ba1a5b39a698248404abeb6ff366cb9cc43ce95be`
- `06cb72f393a6d46393c940a23246d506bd6ec24a6bf2dbdefc61e312603e5b3c`
- `072558ed5a4093921e411d5c87f3082d1fe97ccdc737cdab61f959c9d9a8bb22`
- `0ed2eedf228cfa815e80d241f2bfd62368616ba6ef2ee40ef91c317dc9e8c4a7`
- `0f4442a470be7e99b7a9936a8a822c7f2dc0278899d1fd30127b7a724b3d711c`
- `10bee86a3f6d301f24538c1caa533a0fcd7121faa529c0c9721c28497e23fae1`
- `16841fa1f816e1147f8766632e244e15285d57866efe2b0be59653709c1132ab`
- `180dde084fb16478a30290be831ebf3981dca349959cb6784a78ce8807261f2e`
- `182a76ef5a66727c534d1ccd8fb1964730d2cb84fdeee2ba142a0413d3f382ee`
- `19b16764e49d14e6f6942d1c7dc1b950610bba5aef75b5ba8f21c185c8955516`
- `240d2c650431b08bb7ecc7e89dcfa9b57b0d013b873b02640f15ec3ef2fa2e69`
- `2690e5e9a376ed929cedfc9ae51b2bc7c2aa600c5347d63247036b2a104842a3`
- `2a64f51ac186a4af034db0ab9b5c56f00c86587dc4a60f455a2f86688c806c3c`
- `2d9165ac19f597a87ad36a01ebd58f042cdea08287d3b6a8325ad1297d03daba`
- `3572f47e4ecf05277025cef3e09c53d476027908054dc2f4e7a30fe47775db52`
- `36c4d7355280f4230f67d23aaf3e90e79551c19727faad9169971887a9bcd333`
- `385f07ca2e587097c8fdb83a7175af8d073717180b8e9db3670d7e5bc346897e`
- `3923ae07c2016872f227b66e10a806b8754ae8e64e8126289dc50c4179830c49`
- `3c4af60bc14480071afa3b9486fa7514484a9b6dcc77846d325e57f2955d47ac`
- `4472a35663cebbc9ec59579789d76db8ebd76fca2a5942cf5c5bc891e5af8583`
- `4588056ec807f49a6ddd42a383289d3bb6d883ef50c6a29ad1c330e361fe7b1d`
- `45b70ef22dcb69f47a8943271206d860d8f770af1549614893f972302241af0d`
- `46854b1f1236bbc9a02a71ae82e57924a77e7782f63751d113e5e7175c0345df`
- `4ac684c2c745b9e089e31d43e6aabb5fa75c6e1eb261f0dc02ddca2a9ca03110`
- `4bba2d0adcbb48ec02d9b82a9ec4c9655c13c20b39c35136630de23b08f32f12`
- `52eb61a61772b7878d6db0b96ae3441d5f1bb66f0f1bf5cbc7565481acf23cde`
- `54f4e36505afc95a51970473c01f2ae84b427ce29b559c1ccb4de9d2910646d9`
- `5725677498b414e229ecc641b723a7e8120affbbc89e18acc133831895dfb438`
- `594252df359f78bd131ed2d4944c62907b779167f547596cc320378c69406a69`
- `59a6617d68a550cd248b61f625156d0e6b71c6c4b69c989419766456f5dc833f`
- `5aa6e088007fab5ef6b5b8db1c5d6d65d190ec16483786aae44ecedb50f51803`
- `5c41b30cc0ef81407debf3fb91b9912a1a1da06de9752eccb96dd597af1d96a0`
- `5f8e7ef2f8ffc747ece0831bf33066eb499c1f12b2c5f5bb7e8768ce1fe921fa`
- `618cca5c6a8b5754110f12d12793eb66b6c0f1a157601c21422cdbec61fbea12`
- `6549f40b7941e00ae547750979c6a06ca36b640939dae098981394e4248dd3be`
- `69dcbba5163957c242c6c0795526f1b4010a23e92c1c575ac92ed38d5d11f1c3`
- `6c69bdddaea378c058139148d6865c4cba32f0b00b86c9d24f2ba2aafb2b97c1`
- `6ce12e8ab8fe645b2baefcaad9bc34ac04b98b047ceb436561e9d8e44428f11a`
- `70d573b23771a8c3d14ec76cd557a37722ca3fc8ca97246dce7bfc454d70bcf7`
- `71518eb5abf470d29cc44d7d43ded285a268dc775f0eae602edc42bc278fcdd2`
- `753946a895a2cb9963971ad499cfb0efe07ee3ad06f61d060d5035596421c853`
- `75ad3c7ecdfadfc75a9b15354b9cd3f31a2bd6127a30dc91f1a4c5cc8f831c47`
- `78748c9966987bfedd68a2453a0eca06763c63d93df1a5ee3db598c507c498f4`
- `7bd99136884d5c631f4e85e907faf9bb05355091e8d765e5b7d841a65fdd6514`
- `7bf8baba37a2344c1d8dddf135eb500e4cf768754c29bdccfb4b55183338398d`
- `7c647de4e6e837b3a54f0a514b6f54f81a493520702e5265c4483ac51b34b4f4`
- `82547e55fc7112a6d34cea355f171477576cfa939bf7075bb55b27134c6b50ad`
- `82e5d2082cc9fb90786e3aeca299c3331a8cfbdb2e486a832c257cb6bd10d9c4`
- `8959f24468b8f262147051cfa413d1beebea65bd15144dcb01afd7b32689d86e`
- `8f21848dc6379e97a94f8a7ab57398eff0f79e70c263890f95eb6ae32c1e5a9a`
- `951bd49a4439703fb33ac5d505697bbac13f8803712bf37766bfab9333a770bf`
- `999cec0bfdc05236ca3756db65624a72ed395ef3a6994f9d3cf266981f720113`
- `9ab7579fe94b5f346b31d899bb9e9824ee4cbf4a43b7d729942a13736625d0f0`
- `9c2e2dd99b27429246d159b75a6a7bbc9b0b72aea0aceec114825f5729d3fdb7`
- `a24a3a009e50c11885add90a6b7e2c2134ba648e4042bb18a9c327be73b4884a`
- `a89a3c0e2b297354d49d0d041e5ef8944dfb372f9a123a882066e0cd7c13e695`
- `a911dd6a6276701fffb7957d3a0dcbf8618bd137b391f2c8636734eebdcb3d55`
- `a9a40a16b2050da39e04747b60a7e0a3615657eb0e4a80e692c4926057364b84`
- `ae495c9b8f2c0e81e94149adf9c42bfbf85cbe7a91dd4b14c544d9a15440fc77`
- `b5e9a6da66f8d13b6a81113c09cf7f0d704b9d621a6300aeee0d3df2e3e7ca29`
- `b6c67e930e8a45acefac192bf87956bcf8a39faf35630792a4568daa2cc354bc`
- `ba9e49d5a3f641ff1f1e39cdc16292d6fcbda1e73c9293ceb591936e5ecfc7e9`
- `bd099d38da87e0823280b1478fd84354a7fdbf99b967652d990582cf1be663d5`
- `bebab0adde65490b3c2ae58ca2698bd5412a9160fa1392a70190caabddffc454`
- `c0a98ce6e1da83ca761c6340c33df652b5e100747a63dce7e36506a19e24d5a0`
- `c227e4157499aeba329299268c7893009ccc7425a62f7aee8e68d9a3de44908b`
- `cde1f27066a7135ae7f16a9fd1bcc5fa4bdb7ac1c92f52a29c0778d362daa0d0`
- `ce20d3b1b76ec95c37328a20ddc89ff47cf667bcbb417c0757a43f8e110581b8`
- `d0cea0ecf9b3ce6dc1ef4d2466dd8575067e9a45c0deae9b3d0f704ee46444a4`
- `d51b18159d04d6edf398258392cbd60434bf1609a8b89b6ee5eb5b08a47ffa52`
- `dbbec27575687acd6dd7f477539165531ff5ed1a7bff42d1f53983e165dd4584`
- `df6706e07d448f632c0f7304eb2d1ce5d78b55f7908fe70eb1535809d42df746`
- `e10a155015bcf4aedda9c2c83e35b5f29b9b0f33f401224d2a4f8600e331c134`
- `e1bec3138a1ea59f82170a1bb8b5be92f8efcf66e6345736c2651501c258763a`
- `e2aace316858ca915c076150d78d7813121c47dcea8be7b84f685c9ad8d444b2`
- `e72ac1c82bac4a12f4f40dd1f34742735f70b4c202cad3c3884a0d8c3f158796`
- `ea589346e8b68f5865c4abe045628dce5b9ae61a03a92585b1a082fd59c77982`
- `eb35fb9a5824185a5f88571035735c8a938dbbb56877a3d689d215c9e21ea393`
- `ef2f0ed929c198a8f27a0db8dcab61d2d026438c2590d7f9cfb26a934ab50dae`
- `f8899a4f032f1cace69f666903cd25ca3962adc0f8c1b71e79b9c8bd268cf085`

**NON-EVIDENTIARY stamp:** statuses present — mock. Not a submittable SSP (mock evidence).

Rebuild and drift-check:

```bash
uv run python -m documents.ssp build --input output/engine.trig
uv run python -m documents.ssp build --check
```
