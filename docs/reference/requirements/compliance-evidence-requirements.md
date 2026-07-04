# Compliance Evidence Requirements for Cloud Environment Provisioning

## CMMC Level 2 (Self) · IL5/DoD Impact Level 5 · ITAR

> Research compiled from NIST, DoD, DISA, Federal Register, DFARS, ITAR (22 CFR), and practitioner guidance as of July 2026.

> **Note: Addressing-notation note (2026-07-02).** The BOM examples in §6 use IPFS-style CID strings (`bafybei…`) because they were drafted against the original `concepts/cmmc-as-a-CAT.md` framing. The platform does **not** use IPFS: every `*_cid` field and every `bafybei…` value below is **illustrative**. The canonical form is a **SHA-256 hash keyed into the tiered cloud registry** (GCS for Tier 1, Azure Blob for Tier 2), per `requirements/cats-compliance-engine-requirements.md` §5/§16.2 and as implemented in `ADCS-lifecycle-demo/evidence/hashing.py`. Read `…_cid: "bafybei…"` as `…_hash: "sha256:…"`. The control-mapping research itself is unaffected by this substitution.

---

## 1. Regulatory Framework Summary

Each framework layers on the others; a provisioning engine must satisfy all simultaneously for DoD contracts with ITAR exposure:

| Framework              | Authority                  | Trigger                        | Controls Baseline                                                                               |
| ---------------------- | -------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------- |
| **CMMC Level 2**       | 32 CFR Part 170            | DFARS 252.204-7021 in contract | NIST SP 800-171 Rev 2 (110 controls)                                                            |
| **DFARS 252.204-7012** | DoD acquisition regulation | CUI/CDI handling               | NIST SP 800-171 + FedRAMP Moderate for CSPs                                                     |
| **DoD IL5**            | DISA CC SRG                | NSS/CUI-High data              | FedRAMP High + NIST 800-53 Rev 5 IL5 overlay (~178 additional NSS controls)                     |
| **ITAR**               | 22 CFR Parts 120-130       | USML technical data            | 22 CFR § 120.54 cloud carveout (end-to-end encryption); U.S.-person access; contractual addenda |

### DFARS 252.204-7012(b)(2)(ii)(D) — Cloud Provider Requirement

> "If the Contractor intends to use an external cloud service provider to store, process, or transmit any covered defense information in performance of this contract, the Contractor shall require and ensure that the cloud service provider meets security requirements equivalent to those established by the Government for the Federal Risk and Authorization Management Program (FedRAMP) Moderate baseline."

**Source:** [DFARS 252.204-7012, acquisition.gov](https://www.acquisition.gov/dfars/252.204-7012-safeguarding-covered-defense-information-and-cyber-incident-reporting)

### ITAR § 120.54 Cloud Carveout (March 2020 Amendment)

Unclassified technical data stored in the cloud is **not** considered an export if:

1. Secured using **end-to-end encryption** (FIPS 140-2/140-3 validated modules)
2. Cryptographic keys managed exclusively by **U.S. persons**
3. Data residency restricted to **U.S. soil**
4. Cloud provider contractually prohibits **foreign-person access**

**Source:** [22 CFR § 120.54; DDTC Cloud Storage FAQ (2019); ITAR Consultant](https://itarconsultant.us/blog/itar-and-cloud-computing-aws-govcloud-azure-government-and-whats-actually-requir/)

---

## 2. CMMC Level 2: Controls That Must Be Evidenced

### 2.1 The 110 NIST SP 800-171 Rev 2 Controls — 14 Families

Source: [32 CFR § 170.14(c)(3)](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170/subpart-D/section-170.14); [NIST SP 800-171 Rev 2](https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final)

| Family                          | Code      | # Controls | Key Provisioning Evidence                                                                                |
| ------------------------------- | --------- | ---------- | -------------------------------------------------------------------------------------------------------- |
| Access Control                  | AC (3.1)  | 22         | IAM policy exports, RBAC role assignments, conditional access policies, remote access VPN config         |
| Awareness & Training            | AT (3.2)  | 3          | Training completion records, insider threat program documentation                                        |
| Audit & Accountability          | AU (3.3)  | 9          | Log export configuration, SIEM integration, NTP config, log protection/IAM, retention policy             |
| Configuration Management        | CM (3.4)  | 9          | Terraform state/plan, baseline config exports, change control logs, approved-service catalog             |
| Identification & Authentication | IA (3.5)  | 11         | MFA enforcement policy, password policies, identity provider (Entra ID / Google Workspace) config export |
| Incident Response               | IR (3.6)  | 3          | IR plan document, tabletop exercise record, DIBNet reporting procedure                                   |
| Maintenance                     | MA (3.7)  | 6          | Maintenance logs, remote-support session records, MFA enforcement for remote maintenance                 |
| Media Protection                | MP (3.8)  | 9          | Encryption-at-rest config, backup encryption, media sanitization policy, DLP rules                       |
| Personnel Security              | PS (3.9)  | 2          | Background check records, termination/transfer access revocation logs                                    |
| Physical Protection             | PE (3.10) | 6          | CSP physical security attestation (inherited), alternate-site (remote work) policy                       |
| Risk Assessment                 | RA (3.11) | 3          | Vulnerability scan reports, patch remediation tracking, risk assessment document                         |
| Security Assessment             | CA (3.12) | 4          | SSP document, POA&M tracker, continuous monitoring config                                                |
| System & Comms Protection       | SC (3.13) | 16         | FIPS-validated module evidence (CMVP cert #), firewall rules, boundary config, data-flow diagrams        |
| System & Info Integrity         | SI (3.14) | 7          | Endpoint protection config, patch cadence report, alert/remediation workflow                             |

### 2.2 SPRS Scoring and POA&M Constraints

Source: [32 CFR § 170.24](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170/subpart-D/section-170.24), [32 CFR § 170.21](https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170/subpart-D/section-170.21)

| Score  | Status              | Meaning                           |
| ------ | ------------------- | --------------------------------- |
| 110    | Final Level 2       | All controls MET; 3-year validity |
| 88-109 | Conditional Level 2 | 180-day POA&M closeout window     |
| <88    | No CMMC Status      | Not eligible for CUI contracts    |

**Critical POA&M rule:** Only 1-point controls can be deferred. All 3-point and 5-point controls **must be fully implemented** before SPRS submission. 64 of 110 controls are effectively non-deferrable (58 by weight + 6 excluded 1-point controls).

### 2.3 Highest-Weight (Non-Deferrable) Controls Most Relevant to Provisioning

| CMMC ID       | Control                             | Weight                      | Provisioning Evidence Example                                                               |
| ------------- | ----------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------- |
| SC.L2-3.13.11 | FIPS-validated cryptography for CUI | **5**                       | KMS config with CMVP certificate #, `azurerm_key_vault` module output, TLS 1.2+ enforcement |
| IA.L2-3.5.3   | MFA for privileged access           | **5**                       | Conditional Access policy export, MFA enforcement across all privileged accounts            |
| SC.L2-3.13.8  | Encrypt CUI in transit              | **3**                       | TLS config on all endpoints, HTTPS-only enforcement, VPN encryption                         |
| SC.L2-3.13.16 | Encrypt CUI at rest                 | **3**                       | Storage account encryption settings, disk encryption, CMK config                            |
| AC.L2-3.1.1   | Limit system access                 | **5**                       | IAM role assignments, group membership, documented access policies                          |
| AC.L2-3.1.2   | RBAC enforcement                    | **5**                       | Role definitions, least-privilege role assignments                                          |
| AC.L2-3.1.12  | Monitor/control remote access       | **5**                       | VPN config with logging, remote access policy                                               |
| CM.L2-3.4.1   | Baseline configurations             | **5**                       | Terraform plan/state, CIS/DISA STIG benchmark scan results                                  |
| CM.L2-3.4.2   | Security config settings            | **5**                       | Organization policy exports, hardening standard application                                 |
| AU.L2-3.3.1   | Create and retain audit logs        | **5**                       | Log sink config, retention policy, SIEM integration                                         |
| AU.L2-3.3.2   | Trace user actions uniquely         | **5**                       | No shared accounts, unique user IDs in all logs                                             |
| RA.L2-3.11.2  | Vulnerability scanning              | **5**                       | Scan schedule, scan reports, remediation tracking                                           |
| CA.L2-3.12.4 | System Security Plan                | **1** (excluded from POA&M) | Complete SSP with all 110 controls documented                                               |

---

## 3. IL5/DoD Impact Level 5 — Additional Requirements

### 3.1 IL5 vs IL4 Comparison

Source: [Second Front DoD CC SRG Guide](https://www.secondfront.com/resources/blog/achieving-dod-cc-srg-compliance-navigating-fedramp-and-disa-impact-levels-il4-vs-il5/)

| Requirement                  | IL4                               | IL5                                                |
| ---------------------------- | --------------------------------- | -------------------------------------------------- |
| Data sensitivity             | CUI, non-critical mission data    | Higher-sensitivity CUI, CUI-High, unclassified NSS |
| FedRAMP baseline             | Moderate + IL4 FedRAMP+ controls  | High + IL5/NSS FedRAMP+ controls                   |
| Infrastructure isolation     | Logical/virtual separation        | **Physical separation** required                   |
| Network routing              | NIPRNet via BCAP only             | NIPRNet via BCAP; **no internet**                  |
| Personnel                    | U.S. citizens, nationals, persons | **U.S. citizens only**; ADP-2/NACLC clearance      |
| NIST 800-53 Rev 5 transition | 38 removed, 22 added              | 47 removed, **178 added (40% net increase)**       |

### 3.2 IL5-Specific Evidence Requirements

1. **Physical isolation attestation** — CSP documentation proving dedicated federal community cloud (e.g., AWS GovCloud, Azure Government)
2. **NACLC clearance records** — for personnel accessing the environment
3. **BCAP connection documentation** — all traffic routed through DISA Boundary Cloud Access Point
4. **No-internet connectivity proof** — network configuration showing no direct internet egress
5. **IL5 FedRAMP+ control implementation** — ~178 additional NSS-specific controls beyond FedRAMP High
6. **Phishing-resistant MFA** — hardware tokens or FIDO2/WebAuthn (not SMS/TOTP)
7. **Zero Trust architecture** components — micro-segmentation, continuous verification
8. **Supply chain provenance** — SBOM for all software components

### 3.3 Platform Requirements

Only platforms with **DISA Provisional Authorization at IL5** are acceptable for IL5 workloads:

- AWS GovCloud (US) with DISA IL5 PA
- Azure Government with DISA IL5 PA
- Pre-accredited PaaS (e.g., Second Front Game Warden) for inheritance

---

## 4. ITAR Technical Data Handling Requirements

### 4.1 The Seven Non-Negotiable ITAR Cloud Requirements

Source: [ITAR Consultant, Jared Clark (Certify Consulting), March 2026](https://itarconsultant.us/blog/itar-and-cloud-computing-aws-govcloud-azure-government-and-whats-actually-requir/); [22 CFR §§ 120.50, 120.53, 120.54]

| #   | Requirement                                           | Evidence                                             | Provisioning Hook                                         |
| --- | ----------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| 1   | **U.S.-only data residency**                          | Region restriction policies, data replication audit  | `resourceLocations` constraint: U.S. only                 |
| 2   | **Executed ITAR contractual addendum**                | Signed addendum with CSP                             | Document CID in BOM                                       |
| 3   | **Foreign-person access prohibition**                 | CSP contractual language, access audit               | IAM: no foreign-national principals                       |
| 4   | **U.S.-person-only key management**                   | KMS IAM policies, key admin citizenship verification | KMS: restrict `roles/cloudkms.admin` to U.S. person group |
| 5   | **Access control + audit logging (5-year retention)** | RBAC + CloudTrail/Azure Monitor config               | Export to immutable storage, 5-year lifecycle             |
| 6   | **Employee verification and training**                | Citizenship/LPR verification, ITAR training records  | Not directly provisionable; attestation in BOM            |
| 7   | **Written ITAR cloud policy (TCP addendum)**          | Cloud use policy in Technology Control Plan          | Document CID in BOM                                       |

### 4.2 ITAR Encryption Carveout (22 CFR § 120.54)

**Source:** [22 CFR § 120.54; DDTC March 2020 Amendment; Dinsmore legal analysis](https://www.dinsmore.com/publications/new-itar-end-to-end-encryption-rule-will-promote-efficient-defense-technical-data-storage-and-transmission-but-some-risks-remain/)

Conditions for cloud-stored ITAR data to NOT constitute an export:

- End-to-end encryption using **FIPS 140-2/140-3 validated** cryptographic modules
- Encryption keys **not accessible** to foreign persons
- Data stored and processed exclusively on **U.S. soil**
- **DDTC does not certify any cloud platform** — the contractor bears all compliance responsibility

---

## 5. Acceptable Evidence Types (NIST SP 800-171A Triad)

Source: [NIST SP 800-171A](https://csrc.nist.gov/pubs/sp/800/171/a/final); [DoD NIST SP 800-171 Assessment Methodology](https://www.acq.osd.mil/asda/dpc/cp/cyber/safeguarding.html)

### 5.1 Three Assessment Methods

| Method        | What It Means                                           | Example Evidence                                                                 |
| ------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Examine**   | Review documentation, configurations, policies, records | SSP, screenshots, config exports, policy docs, network diagrams, FedRAMP letters |
| **Interview** | Speak with responsible personnel                        | Recorded interviews, attestation statements, meeting notes                       |
| **Test**      | Validate technical configs through observation/tooling  | Vulnerability scans, log queries, MFA config checks, access reviews              |

A control is scored **MET** only when **all** assessment objectives in 800-171A support it.

### 5.2 Evidence Inventory by Control Family

| Family | Primary Evidence Artifacts                                                                                        |
| ------ | ----------------------------------------------------------------------------------------------------------------- |
| AC     | IAM policy exports, RBAC role lists, conditional access policies, VPN config, session timeout config              |
| AT     | Training completion records (dated, per-user), role-based curriculum                                              |
| AU     | Log source inventory, SIEM integration doc, NTP config, log access controls, retention policy                     |
| CM     | Terraform state (immutable baseline), CIS/DISA benchmark scan, change control tickets, approved-service allowlist |
| IA     | MFA enforcement config, password policies, identity provider export, shared-account audit                         |
| IR     | IR plan document, tabletop exercise record, DIBNet reporting procedure test                                       |
| MA     | Maintenance logs, remote support session approvals, tool inventory                                                |
| MP     | Encryption-at-rest settings, backup encryption config, DLP rules, media sanitization records                      |
| PS     | Background check verification, offboarding checklist with timestamps                                              |
| PE     | CSP physical security attestation (inherited), alternate-site policy document                                     |
| RA     | Vulnerability scan reports (dated), patch compliance report, risk assessment document                             |
| CA     | SSP document (complete, dated), POA&M tracker, continuous monitoring dashboard                                    |
| SC     | FIPS module CMVP certificate numbers, firewall rule exports, data-flow diagram, TLS config                        |
| SI     | Endpoint protection status report, patch cadence report, alert response workflow                                  |

---

## 6. How a Provisioning BOM Maps to Controls

Based on the CATs Order/Factory/BOM pattern (see `cmmc-research/concepts/cmmc-as-a-CAT.md`; `cats/cats/factory/__init__.py`; and the working reference implementation in `ADCS-lifecycle-demo/`):

> **Notation:** the `bafybei…` / `*_cid` values below are illustrative — the platform keys artifacts by **SHA-256 hash in the tiered registry**, not IPFS CID. See the addressing-notation note at the top of this document.

### 6.1 BOM Structure for Compliance Evidence

```json
{
    "order": {
        "target_standard": "CMMC_Level2_IL5_ITAR",
        "contract_id": "NV018-2026",
        "scope": {
            "data_classes": ["CUI", "ITAR_Technical_Data"],
            "personnel": ["user_ids..."],
            "environment": "gcc_high_us_gov_virginia"
        }
    },
    "infrastructure": {
        "tf_plan_cid": "bafybei...",
        "tf_state_cid": "bafybei...",
        "modules": [
            {
                "name": "entra_id_mfa",
                "controls_satisfied": ["IA.L2-3.5.3", "IA.L2-3.5.2"]
            },
            {
                "name": "azure_key_vault_fips",
                "controls_satisfied": ["SC.L2-3.13.11"]
            },
            {
                "name": "network_segmentation",
                "controls_satisfied": ["SC.L2-3.13.1", "SC.L2-3.13.5"]
            },
            {
                "name": "audit_log_export",
                "controls_satisfied": ["AU.L2-3.3.1", "AU.L2-3.3.2"]
            }
        ]
    },
    "compliance_tests": {
        "policy_validations": [
            {
                "test": "azure_policy_cis_benchmark",
                "result_cid": "bafybei...",
                "status": "PASS"
            },
            {
                "test": "opa_network_rules",
                "result_cid": "bafybei...",
                "status": "PASS"
            },
            {
                "test": "fips_module_check",
                "result_cid": "bafybei...",
                "status": "PASS"
            },
            {
                "test": "itar_access_audit",
                "result_cid": "bafybei...",
                "status": "PASS"
            }
        ]
    },
    "control_mapping": [
        {
            "control": "SC.L2-3.13.11",
            "resource": "azurerm_key_vault.fips",
            "evidence_cid": "bafybei...",
            "status": "MET"
        },
        {
            "control": "IA.L2-3.5.3",
            "resource": "azuread_conditional_access.mfa",
            "evidence_cid": "bafybei...",
            "status": "MET"
        },
        {
            "control": "AC.L2-3.1.1",
            "resource": "azuread_group.cui_users",
            "evidence_cid": "bafybei...",
            "status": "MET"
        },
        {
            "control": "ITAR-120.54",
            "resource": "kms_cmk_us_person_only",
            "evidence_cid": "bafybei...",
            "status": "MET"
        }
    ],
    "attestation": {
        "signed_by": "affirming_official_cid",
        "timestamp": "2026-07-02T12:00:00Z",
        "signature_cid": "bafybei..."
    }
}
```

### 6.2 Evidence Collection During Provisioning — Per-Control Mapping

Each Terraform module or provisioning step generates evidence that maps to specific controls:

| Provisioning Step                                 | Resource/Module                       | Controls Satisfied           | Evidence Type             | Evidence Artifact                  |
| ------------------------------------------------- | ------------------------------------- | ---------------------------- | ------------------------- | ---------------------------------- |
| Create resource group with U.S. region constraint | `azurerm_resource_group` + org policy | ITAR residency, SC.L2-3.13.1 | Config export             | Org policy: `resourceLocations:us` |
| Deploy Key Vault with FIPS HSM                    | `azurerm_key_vault` (FIPS SKU)        | SC.L2-3.13.11, ITAR key mgmt | Module output + CMVP cert | Key Vault config + certificate #   |
| Enforce MFA via Conditional Access                | `azuread_conditional_access_policy`   | IA.L2-3.5.3, IA.L2-3.5.2     | Policy export             | CA policy JSON                     |
| Create CUI user/group structure                   | `azuread_group`, `azuread_user`       | AC.L2-3.1.1, AC.L2-3.1.2     | Group membership + IAM    | User/group export                  |
| Deploy NSG with deny-all                          | `azurerm_network_security_group`      | SC.L2-3.13.1, SC.L2-3.13.6   | NSG rule export           | NSG config                         |
| Enable diagnostic settings → Log Analytics        | `azurerm_monitor_diagnostic_setting`  | AU.L2-3.3.1, AU.L2-3.3.2     | Log config + retention    | Diag settings export               |
| Configure Storage Account with CMK                | `azurerm_storage_account` + CMK       | SC.L2-3.13.16, SC.L2-3.13.8  | Encryption config         | Storage encryption settings        |
| Apply CIS/DISA benchmark via Azure Policy         | `azurerm_policy_assignment`           | CM.L2-3.4.1, CM.L2-3.4.2     | Compliance scan result    | Policy compliance report           |
| Deploy DLP rules for CUI/ITAR                     | `purview_dlp_policy` or equiv.        | AC.L2-3.1.3, ITAR            | DLP policy + test result  | DLP config + test log              |
| Enable CloudTrail/Azure Monitor                   | Logging infrastructure                | AU.L2-3.3.1–3.3.9            | Log capture config        | Log sink + retention config        |

### 6.3 Automated Control Assertion Flow

```
Order CID (target: IL5+ITAR+CMMC_L2)
  │
  ▼
Factory provisions environment via Terraform
  │
  ├── Captures tf_plan_cid (immutable intent)
  ├── Captures tf_state_cid (immutable result)
  │
  ▼
Compliance test suite executes against live environment
  │
  ├── Azure Policy / OPA rules → result CID
  ├── CIS benchmark scan → result CID
  ├── FIPS module verification → CMVP cert check → result CID
  ├── ITAR access audit (U.S. person only) → result CID
  ├── MFA enforcement audit → result CID
  │
  ▼
Control mapping generated:
  control_id → resource → evidence_cid → status
  │
  ▼
BOM assembled with all CIDs
  │
  ▼
BOM signed by Affirming Official → attestation CID
  │
  ▼
BOM published to SPRS / assessor → retrievable by CID
```

### 6.4 Key Design Principles

1. **Immutability:** Every evidence artifact is content-addressed (CID). The BOM is a Merkle-like tree of proofs. Tampering is detectable by CID mismatch.
2. **Reproducibility:** A C3PAO can re-execute the Order to reproduce the environment and verify the BOM. No static screenshots needed.
3. **Continuous compliance:** Each new Terraform apply produces a new BOM CID. Drift is detectable by diffing CID chains.
4. **Tier separation:** Tier 1 (IL4) submits a provisioning Order to Tier 2 (IL5). Tier 2 executes, generates a BOM, and returns only the BOM CID to Tier 1. IL5 data never flows down.
5. **Living SSP:** The control mapping within the BOM replaces the static PDF SSP. The BOM is the SSP.

---

## 7. Cloud Platform Compliance Matrix

| Platform                                     | FedRAMP | IL4 | IL5           | ITAR Capable          | CMMC L2 Fit                |
| -------------------------------------------- | ------- | --- | ------------- | --------------------- | -------------------------- |
| **Azure Government**                         | High    | Yes | Yes (DISA PA) | Yes (with addendum)   | Best for IL5/ITAR          |
| **M365 GCC High**                            | High    | Yes | Yes           | Yes (with addendum)   | Gold standard for CUI/ITAR |
| **AWS GovCloud (US)**                        | High    | Yes | Yes (DISA PA) | Yes (with addendum)   | Best for IaaS workloads    |
| **Google Workspace (Enterprise Plus + ACP)** | High    | Yes | **No**        | Requires extra config | Viable for IL4 CUI only    |
| **GCP Assured Workloads IL4**                | High    | Yes | **No**        | Requires extra config | Viable for IL4 CUI only    |

**Source:** [cmmc-research/guides/cmmc-bidding-plan.md](cmmc-research/guides/cmmc-bidding-plan.md); [cmmc-research/guides/google-cui-enclave.md](cmmc-research/guides/google-cui-enclave.md); [Second Front IL5 Guide](https://www.secondfront.com/resources/blog/achieving-dod-cc-srg-compliance-navigating-fedramp-and-disa-impact-levels-il4-vs-il5/)

---

## 8. Official Source Index

| Source                                   | URL                                                                              | Key Content                                                     |
| ---------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 32 CFR Part 170 (CMMC Final Rule)        | https://www.ecfr.gov/current/title-32/subtitle-A/chapter-I/subchapter-G/part-170 | Level definitions, scoring, POA&M rules                         |
| DFARS 252.204-7012                       | https://www.acquisition.gov/dfars/252.204-7012                                   | NIST 800-171 mandate, CSP FedRAMP req, cyber incident reporting |
| DFARS 252.204-7021                       | https://www.acquisition.gov/dfars/252.204-7021                                   | CMMC status requirement, UID, annual affirmation                |
| DFARS 252.204-7025                       | https://www.acquisition.gov/dfars/252.204-7025                                   | Solicitation notice, pre-award CMMC                             |
| NIST SP 800-171 Rev 2                    | https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final                              | 110 security requirements                                       |
| NIST SP 800-171A                         | https://csrc.nist.gov/pubs/sp/800/171/a/final                                    | Assessment procedures (Examine/Interview/Test)                  |
| DoD CC SRG (DISA)                        | https://public.cyber.mil/dccs/dccs-documents/                                    | IL4/IL5 requirements, BCAP, physical separation                 |
| 22 CFR §§ 120-130 (ITAR)                 | https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M                     | ITAR cloud carveout, export controls                            |
| NARA CUI Registry                        | https://www.archives.gov/cui                                                     | CUI categories and markings                                     |
| Cyber AB Marketplace                     | https://cyberab.org                                                              | Authorized C3PAOs and RPOs                                      |
| DoD NIST 800-171 Assessment Methodology  | https://www.acq.osd.mil/asda/dpc/cp/cyber/safeguarding.html                      | SPRS scoring math                                               |
| NIST SP 800-171 Controls Matrix (GitHub) | https://github.com/capetron/nist-800-171-controls-matrix                         | 110 controls with weights, evidence, mappings                   |

---

_Compiled July 2, 2026. This is research, not legal advice. Verify all requirements with your contracting officer, C3PAO, and legal counsel._
