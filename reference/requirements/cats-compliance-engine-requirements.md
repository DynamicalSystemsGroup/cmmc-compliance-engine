# CATs-Compliance Engine — Requirements Document

> **Status:** Draft for review  
> **Date:** 2026-07-02  
> **Scope:** Organization-wide SOPs for auditable, compliance-guaranteed cloud environment provisioning (CMMC Level 2, IL5, ITAR).  
> **Not in scope:** NV011/NV012 proposal execution; this is the reusable platform those proposals will consume.  

---

## 1. Problem Statement

DSG needs to provision cloud environments for defense contracts at multiple compliance tiers (IL4/CMMC Level 2, IL5/ITAR) and be able to **prove** to auditors, primes, and C3PAOs that every provisioned environment satisfies the required controls. The current state is a single Google Workspace tenant with no CUI boundary, no Assured Workloads, and no centralized identity or provisioning audit trail.

The risks of the current state:

- **Cannot bid CUI contracts without CMMC Level 2 status in SPRS.**
- **Cannot bid IL5/ITAR contracts without a FedRAMP High/IL5 platform.**
- **Manual provisioning is non-repeatable and non-auditable.**
- **C3PAO assessment evidence (screenshots, policies, config exports) is scattered and difficult to reproduce.**

The goal is to replace ad-hoc provisioning with an **auditable, re-executable compliance engine** that uses the CATs Order/Factory/BOM pattern but replaces IPFS with a custom content-addressed registry inside the organization's own cloud boundaries.

---

## 2. Design Thesis

> **Compliance is a provisioning artifact.**

Every environment provisioning run produces a **Bill of Materials (BOM)** that is a self-contained compliance record. The BOM contains cryptographic hashes of:

1. The **Order** (intent, target standard, contract scope, authorized personnel).
2. The **Terraform plan** (declared infrastructure).
3. The **Terraform state** (actual provisioned resources).
4. The **policy validation results** (OPA, Checkov, Trivy, Azure Policy, GCP Org Policy).
5. The **live-environment compliance tests** (MFA enforcement, encryption checks, access audits).
6. The **human approvals** and **digital signatures** along the chain.

The BOM is the **System Security Plan (SSP)** for that environment. Auditors can re-execute the Order to reproduce the environment and verify every control claim.

---

## 3. Actors and Stakeholders

| Actor | Role | Interaction with the engine |
|-------|------|-------------------------------|
| **Platform Engineer** | Builds and maintains the compliance engine | Authors Terraform modules, policy libraries, and Order templates. |
| **Compliance Officer** | Approves Tier 2 / high-risk provisioning | Required reviewer for IL5/ITAR Orders; attests to BOM accuracy. |
| **Project Lead** | Requests environment for a contract | Submits a provisioning Order via GitHub PR. |
| **Developer/Analyst** | Uses the provisioned environment | Receives least-privilege access through the central identity platform. |
| **C3PAO / Auditor** | Verifies compliance | Retrieves BOMs by hash and re-executes Orders to validate controls. |
| **Affirming Official** | Certifies SPRS score | Legally responsible for the accuracy of the compliance posture. |

---

## 4. Goals

### 4.1 Primary Goals

1. **Tiered Provisioning Chain:** Tier 0 hosts the controller that provisions Tier 1; Tier 1 hosts the controller that provisions Tier 2. No cross-tier shortcuts.
2. **Reusable Compliance Engine:** A CATs-inspired Order/Factory/BOM system that provisions and audits environments without depending on IPFS.
3. **Content-Addressed Audit Trail:** Every artifact (plan, state, test result, policy, signature) is stored with a SHA-256 hash in a registry inside the appropriate compliance boundary.
4. **Human-in-the-Loop Approval:** Every provisioning Order requires a single-person GitHub PR approval before execution, with stronger gates for Tier 2.
5. **Non-Repudiable Signatures:** Orders and BOMs are signed using OIDC-backed keyless signing (Sigstore cosign) with identity anchored in Google Workspace.
6. **Control Mapping Automation:** The BOM explicitly maps each provisioned resource to the NIST SP 800-171 / CMMC / IL5 / ITAR controls it satisfies.

### 4.2 Secondary Goals

1. **Start with Tier 1:** The first implemented Order provisions a hardened IL4 Google Workspace + GCP environment for CMMC Level 2.
2. **Defer Tier 2:** IL5/GCC High provisioning is designed into the architecture but implemented after Tier 1 is stable.
3. **Multi-Framework Support:** The same engine eventually supports CMMC Level 2, FedRAMP High, DoD IL5, and ITAR via different Order types and module sets.
4. **KOI Integration:** In the future, BOMs feed into KOI-Net as knowledge-graph nodes for real-time compliance posture queries.

---

## 5. Non-Goals

1. **IPFS as a transport layer.** The system does not use IPFS for content addressing or data movement. IPFS is replaced by a custom hash registry in GCS/Azure Blob.
2. **Full CATs reuse.** We reuse the *abstractions* (Order, Factory, BOM, Mesh) but not the existing CATs codebase directly. A new Python service is written for this purpose.
3. **Real-time continuous monitoring.** The first phase focuses on provisioning-time compliance evidence. Continuous drift detection is a future phase.
4. **Automatic remediation of drift.** Detecting drift is in scope; auto-remediation is out of scope for Phase 1.
5. **Third-party multi-tenant SaaS.** The engine runs inside DSG-controlled cloud boundaries (GCS IL4, Azure Government IL5), not in a shared SaaS platform.

---

## 6. Scope Boundaries

### 6.1 In Scope

- Provisioning of Google Workspace OUs, GCP projects, and GCP Assured Workloads folders for IL4/CMMC Level 2.
- Provisioning of Microsoft 365 GCC High tenants and Azure Government resource groups for IL5/ITAR.
- Content-addressed registry for Order/BOM artifacts in GCS (Tier 1) and Azure Blob (Tier 2).
- GitHub-based approval workflow with signed commits and environment gates.
- Policy-as-code validation (OPA, Trivy, Checkov) for Terraform plans.
- Post-provisioning cloud policy enforcement (Azure Policy, GCP Organization Policy).
- Control mapping to NIST SP 800-171 Rev 2, CMMC Level 2, DoD IL5, and ITAR requirements.

### 6.2 Out of Scope

- Development of the core CATs data-processing engine (see `cats/`).
- Replacement of KOI-Net or integration with it in Phase 1.
- SIEM implementation in Phase 1 (log export is in scope; SIEM analysis is not).
- Endpoint management / MDM in Phase 1.
- Physical security controls (inherited from CSP).
- Personnel security background checks (process is in scope; automation is not).

### 6.3 Deferred

- Automatic re-provisioning on BOM drift detection.
- Cross-cloud mesh networking beyond HTTPS + mTLS.
- Blockchain or distributed ledger for signatures (Sigstore Rekor is sufficient).
- Multi-party threshold signing for BOM attestation.

---

## 7. Conceptual Architecture

### 7.1 Tiered Provisioning Chain

```
┌─────────────────────────────────────────────────────────────────┐
│  TIER 0 — Public / Low-sensitivity                                │
│  Google Workspace (as-is) + GitHub                               │
│  ─────────────────────────────────────                          │
│  • Drafts and approves Orders via PR                             │
│  • Hosts GitHub Actions / workflow definitions                    │
│  • Cannot access Tier 1 or Tier 2 data                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ submits signed Order
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  TIER 1 — IL4 / CMMC Level 2                                      │
│  Google Workspace Enterprise Plus + Assured Controls Plus       │
│  GCP Assured Workloads IL4 folder                               │
│  GCS content-addressed registry                                 │
│  ─────────────────────────────────────                          │
│  • CATs-Compliance Controller (Tier 1)                            │
│  • Provisions GCP projects + Workspace CUI OUs                   │
│  • Hosts the registry for Tier 1 artifacts                       │
│  • Submits Orders to Tier 2 controller                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ submits signed Order (over mTLS)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  TIER 2 — IL5 / ITAR                                              │
│  Microsoft 365 GCC High                                         │
│  Azure Government                                                 │
│  Azure Blob content-addressed registry                          │
│  ─────────────────────────────────────                          │
│  • CATs-Compliance Controller (Tier 2)                          │
│  • Provisions GCC High workspaces + Azure Gov resource groups     │
│  • Hosts the registry for Tier 2 artifacts                       │
│  • Returns only BOM hash to Tier 1                               │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Order → Factory → BOM Flow

```
Order (JSON, signed)
    │
    ▼
Approval Gate (GitHub PR + Environment reviewer)
    │
    ▼
Factory (Python service in target tier)
    │
    ├── 1. Fetch Terraform modules from registry by hash
    ├── 2. terraform plan  → plan hash
    ├── 3. policy-as-code checks  → check result hashes
    ├── 4. terraform apply  → state hash
    ├── 5. live compliance tests  → test result hashes
    │
    ▼
BOM (JSON, signed)
    │
    ├── control mapping: resource → control → evidence hash
    ├── attestation: signed by execution identity + human approver
    └── stored in tier registry
```

---

## 8. Functional Requirements

### 8.1 Order Definition

An Order is a JSON document with the following conceptual schema:

```json
{
  "order_id": "uuid",
  "target_tier": "tier1|tier2",
  "target_standard": "CMMC_L2|IL5|ITAR|FEDRAMP_HIGH",
  "contract_id": "string",
  "project_scope": {
    "data_classes": ["CUI", "ITAR_TechnICAL_DATA"],
    "authorized_personnel": ["user@dsg.com"],
    "required_controls": ["IA.L2-3.5.3", "SC.L2-3.13.11"]
  },
  "modules": [
    {
      "name": "gcp_il4_project",
      "source_hash": "sha256:abc...",
      "variables": { ... }
    }
  ],
  "policies": [
    {
      "name": "require_us_region",
      "source_hash": "sha256:def..."
    }
  ],
  "approver_identities": ["compliance@dsg.com"]
}
```

**Requirements:**

- FR-1.1: Every Order must declare its target tier, standard, and contract scope.
- FR-1.2: Every Order must reference Terraform modules and policies by content hash.
- FR-1.3: Every Order must list required approver identities.
- FR-1.4: Orders must be signed before execution.

### 8.2 Approval Workflow

- FR-2.1: Orders are created as GitHub PRs against a repository containing Terraform modules and policy definitions.
- FR-2.2: PRs require at least one approving review from a CODEOWNER or required reviewer.
- FR-2.3: Commits on the PR branch must be signed (SSH or GPG).
- FR-2.4: After merge, the apply workflow targets a GitHub Environment with required reviewers.
- FR-2.5: For Tier 2 Orders, the GitHub Environment requires a second approval from a Compliance Officer.
- FR-2.6: The PR author cannot approve their own deployment (prevent self-review).

### 8.3 Factory Execution

- FR-3.1: The Factory retrieves all referenced modules and policies from the content-addressed registry by hash.
- FR-3.2: The Factory runs `terraform plan` and captures the binary plan and JSON plan output.
- FR-3.3: The Factory runs policy-as-code checks against the plan JSON.
- FR-3.4: If all checks pass, the Factory runs `terraform apply` using the exact binary plan.
- FR-3.5: The Factory captures the resulting Terraform state file and apply logs.
- FR-3.6: The Factory runs live compliance tests against the provisioned environment.
- FR-3.7: The Factory produces a BOM containing all hashes, control mappings, and attestations.
- FR-3.8: The Factory aborts and produces a failure BOM if any check or test fails.

### 8.4 Content-Addressed Registry

- FR-4.1: Tier 1 registry is hosted in GCS inside the Assured Workloads IL4 folder.
- FR-4.2: Tier 2 registry is hosted in Azure Blob Storage inside the Azure Government boundary.
- FR-4.3: Every stored artifact is keyed by its SHA-256 hash.
- FR-4.4: The registry supports write-once-read-many semantics; artifacts cannot be modified after write.
- FR-4.5: The registry logs all read and write operations for audit purposes.
- FR-4.6: Tier 1 can submit an Order to Tier 2, but Tier 2 data never flows down to Tier 1.

### 8.5 BOM Structure

The BOM is a JSON document with the following conceptual schema:

```json
{
  "bom_id": "uuid",
  "order_hash": "sha256:...",
  "execution": {
    "plan_hash": "sha256:...",
    "state_hash": "sha256:...",
    "apply_log_hash": "sha256:...",
    "started_at": "2026-07-02T12:00:00Z",
    "completed_at": "2026-07-02T12:05:00Z"
  },
  "policies": [
    { "name": "require_us_region", "result_hash": "sha256:...", "status": "PASS" }
  ],
  "compliance_tests": [
    { "name": "mfa_enforced", "result_hash": "sha256:...", "status": "PASS" }
  ],
  "control_mapping": [
    {
      "control": "SC.L2-3.13.11",
      "resource": "azurerm_key_vault.fips",
      "evidence_hash": "sha256:...",
      "status": "MET"
    }
  ],
  "attestations": [
    {
      "identity": "compliance@dsg.com",
      "mechanism": "sigstore-cosign-keyless",
      "signature_hash": "sha256:...",
      "timestamp": "2026-07-02T12:06:00Z"
    }
  ]
}
```

**Requirements:**

- FR-5.1: The BOM references every artifact by hash.
- FR-5.2: The BOM maps each provisioned resource to the controls it satisfies.
- FR-5.3: The BOM contains at least one human attestation.
- FR-5.4: The BOM is signed by the execution service identity and the human approver.
- FR-5.5: The BOM hash is returned to the requesting tier and recorded in a registry index.

### 8.6 Control Mapping

- FR-6.1: Each Terraform module declares the controls it satisfies via metadata.
- FR-6.2: The Factory aggregates module-level control claims into the BOM control mapping.
- FR-6.3: Policy-as-code results and live tests confirm or reject each control claim.
- FR-6.4: A control is marked `MET` only if all supporting evidence passes.
- FR-6.5: The BOM supports CMMC Level 2, IL5, FedRAMP High, and ITAR control mappings.

---

## 9. Non-Functional Requirements

### 9.1 Security

- NFR-1.1: All service-to-service communication between tiers uses mTLS.
- NFR-1.2: No long-lived cloud credentials are stored in GitHub; use OIDC-based short-lived credentials.
- NFR-1.3: Terraform state files are encrypted at rest and access is restricted to the execution service identity.
- NFR-1.4: Secrets are not stored in Terraform state; use cloud-native secret managers or ephemeral values.
- NFR-1.5: All registry writes are append-only; artifacts are immutable.
- NFR-1.6: Tier 2 environments require phishing-resistant MFA (hardware keys or FIDO2).
- NFR-1.7: Only U.S. persons can administer Tier 2 keys and environments for ITAR data.

### 9.2 Compliance

- NFR-2.1: The engine must produce evidence satisfying the NIST SP 800-171A assessment methods (Examine, Interview, Test).
- NFR-2.2: The BOM must be available for C3PAO review and re-execution.
- NFR-2.3: The engine must enforce U.S. data residency for Tier 1 and Tier 2.
- NFR-2.4: The engine must use FIPS 140-2/140-3 validated cryptographic modules for CUI/ITAR protection.
- NFR-2.5: Audit logs must be retained for 5 years for ITAR environments and 3 years for CMMC Level 2.
- NFR-2.6: The engine must support separation of duties between provisioning operators and approvers.

### 9.3 Auditability

- NFR-3.1: Every provisioning run is recorded with a unique BOM hash.
- NFR-3.2: Every state change produces a new BOM hash that references the previous one.
- NFR-3.3: The BOM contains enough information to reproduce the exact environment.
- NFR-3.4: Signatures are recorded in a public transparency log (Sigstore Rekor) for non-repudiation.
- NFR-3.5: All approvals are logged in GitHub's immutable audit log.

### 9.4 Reliability

- NFR-4.1: Terraform state locking prevents concurrent provisioning runs on the same environment.
- NFR-4.2: Failed provisioning runs produce a failure BOM with detailed error evidence.
- NFR-4.3: The engine supports idempotent re-execution of the same Order.

### 9.5 Usability

- NFR-5.1: Project leads can submit an Order by opening a PR with a simple JSON/YAML file.
- NFR-5.2: Approvers review and approve via the GitHub web UI.
- NFR-5.3: BOMs are human-readable JSON and machine-verifiable.

---

## 10. Identity and Signing Architecture

### 10.1 Single Source of Identity

Google Workspace is the authoritative directory. It federates to:

- **GitHub Enterprise Cloud** via SAML SSO.
- **GCP** via Cloud Identity / Workspace identity.
- **Azure/GCC High** via Google Cloud Directory Sync or manual user provisioning.

This ensures the identity that signs a commit, approves a PR, and operates cloud resources is the same identity.

### 10.2 Signing Mechanisms

| Artifact | Signing Mechanism | Why |
|----------|---------------------|-----|
| Git commits | SSH-signed commits + required signed commits branch protection | Simple, reuses existing SSH keys, non-repudiable in Git history. |
| Order/BOM | Sigstore cosign keyless signing via GitHub Actions OIDC | No key management; OIDC identity anchored in Workspace-backed GitHub; Rekor transparency log. |
| Cross-tier mTLS | Vault PKI issuing short-lived certs | Shared CA between GCP and Azure Gov; FIPS-compliant TLS; automated rotation. |
| Service-to-service within tier | GCP Workload Identity / Azure Managed Identity | Cloud-native, no long-lived secrets. |

### 10.3 Approval Chain

1. Developer signs commit and opens PR.
2. CODEOWNER approves PR (single person).
3. PR merges to `main`.
4. GitHub Actions workflow triggers plan job.
5. Plan job posts plan artifact and summary.
6. Apply job targets GitHub Environment (e.g., `il4-gcp` or `il5-gcc-high`).
7. Required reviewer approves environment deployment (single person; different from PR author).
8. Workflow receives OIDC token, authenticates to cloud, applies the plan.
9. Factory produces and signs the BOM.
10. BOM hash is recorded and returned.

---

## 11. Tier-Specific Requirements

### 11.1 Tier 1 — IL4 / CMMC Level 2

**Platform:** Google Workspace Enterprise Plus + Assured Controls Plus + GCP Assured Workloads IL4.

**Provisioning targets:**

- A dedicated Google Workspace OU for the contract's CUI users.
- A dedicated GCP project inside the Assured Workloads IL4 folder.
- IAM groups and least-privilege roles.
- MFA enforcement for the CUI OU.
- Drive/Gmail DLP and sharing restrictions.
- Audit log export to a GCS bucket in the IL4 project.
- Vault retention policies.

**Control evidence:**

| Control | Evidence |
|---------|----------|
| IA.L2-3.5.3 | Workspace 2-Step Verification policy export for CUI OU. |
| AC.L2-3.1.1 | IAM group membership and role assignments. |
| SC.L2-3.13.16 | GCS bucket encryption settings (CMEK). |
| AU.L2-3.3.1 | Audit log export configuration and retention policy. |
| CM.L2-3.4.1 | Terraform plan/state hash and baseline config. |

### 11.2 Tier 2 — IL5 / ITAR

**Platform:** Microsoft 365 GCC High + Azure Government.

**Provisioning targets:**

- A dedicated GCC High workspace for the contract.
- A dedicated Azure Government resource group.
- Azure AD Conditional Access with phishing-resistant MFA.
- Azure Key Vault with FIPS HSM for key management.
- Network segmentation with no direct internet egress.
- Azure Policy assignments for NIST 800-53 / FedRAMP High / CMMC.
- Azure Monitor / Log Analytics for audit logs.

**Control evidence:**

| Control | Evidence |
|---------|----------|
| SC.L2-3.13.11 | Azure Key Vault FIPS HSM configuration + CMVP certificate number. |
| ITAR 120.54 | U.S. residency policy, U.S. person key management attestation, end-to-end encryption proof. |
| IL5-specific | Physical isolation attestation, NACLC clearance records, BCAP routing documentation. |

---

## 12. Policy-as-Code Requirements

### 12.1 Pre-Deployment Checks

The Factory must run the following checks before `terraform apply`:

1. **Static analysis:** `terraform fmt -check`, `terraform validate`, `tflint`.
2. **Security scanning:** Trivy + Checkov against Terraform configs.
3. **Policy validation:** OPA Rego policies against `terraform show -json tfplan`.
4. **Naming/tagging:** Mandatory tags, approved resource locations, allowed resource types.

### 12.2 Post-Deployment Enforcement

After provisioning, cloud-native policy engines enforce the baseline:

- **GCP:** Organization Policy constraints (`constraints/gcp.resourceLocations`, `constraints/iam.disableServiceAccountKeyCreation`, etc.).
- **Azure:** Azure Policy assignments (NIST 800-53 Rev 5, FedRAMP High, CMMC initiatives).

### 12.3 Policy Library

- POL-1: Policies are versioned in Git alongside Terraform modules.
- POL-2: Policies are themselves content-addressed in the registry.
- POL-3: Policy changes follow the same PR approval workflow as infrastructure changes.

---

## 13. Data Model and Registry

### 13.1 Artifact Registry Schema

Every artifact stored in the registry has a metadata record:

```json
{
  "artifact_hash": "sha256:abc...",
  "artifact_type": "terraform-plan|terraform-state|policy-result|compliance-test|bom|order|signature",
  "tier": "tier1|tier2",
  "contract_id": "string",
  "created_at": "2026-07-02T12:00:00Z",
  "signed_by": "identity",
  "uri": "gs://tier1-registry/contract/abc..."  // or Azure equivalent
}
```

### 13.2 Registry Index

A separate index (Cloud SQL / Firestore in Tier 1, Azure Table Storage in Tier 2) maps:

- `contract_id` → latest BOM hash
- `bom_hash` → list of referenced artifact hashes
- `control_id` → list of BOMs claiming MET

### 13.3 Immutability

- REG-1: GCS Object Versioning and Azure Blob Versioning are enabled.
- REG-2: Tier 1 GCS bucket has Object Lock or retention policy.
- REG-3: Tier 2 Azure Blob has immutable storage policy.
- REG-4: Write operations are append-only; no artifact is overwritten.

---

## 14. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **GitHub compromise** | Attacker approves malicious Order | Require signed commits; prevent self-review; separate PR reviewer from environment reviewer. |
| **Terraform state exposure** | Secrets or resource metadata leaked | Encrypt state at rest; use remote backend with least-privilege IAM; avoid storing secrets in state. |
| **Policy bypass** | Non-compliant resources deployed | Pre-deployment OPA checks + post-deployment Azure/GCP policy enforcement. |
| **Tier 2 mTLS misconfiguration** | IL5 data leaked to Tier 1 | Use Vault PKI with short-lived certs; enforce mTLS at Tier 2 API gateway. |
| **Sigstore availability** | Cannot sign BOMs | Cache signing certs locally; fallback to GPG-signed BOMs for emergency. |
| **C3PAO rejects BOM format** | Assessment delayed | Document mapping to NIST 800-171A evidence methods; provide both BOM and traditional PDF SSP. |
| **Assured Workloads/Enterprise Plus procurement delays** | Cannot meet July 22 deadline | Place orders immediately; engage Google partner; have GCC High fallback ready. |

---

## 15. Assumptions and Dependencies

### 15.1 Assumptions

- DSG will purchase Google Workspace Enterprise Plus and Assured Controls Plus for CUI users.
- DSG will establish a Google Cloud Organization and enable Assured Workloads.
- DSG will eventually procure Microsoft 365 GCC High and Azure Government for Tier 2.
- DSG will use GitHub Enterprise Cloud (or public GitHub with SAML SSO) for the approval workflow.
- DSG personnel who access Tier 2 will be U.S. citizens with appropriate clearances.

### 15.2 Dependencies

- Google Workspace / Cloud Identity for SSO and user lifecycle.
- GitHub Actions with OIDC and Environments for CI/CD gating.
- Sigstore cosign for keyless signing.
- Terraform / OpenTofu for infrastructure provisioning.
- OPA / Checkov / Trivy for policy-as-code.
- HashiCorp Vault (optional but recommended) for cross-tier mTLS PKI.

---

## 16. Open Questions and Decisions

### 16.1 Questions Requiring User Decision

1. **Repository location:** Resolved — this document lives in `cmmc-research/requirements/`.
2. **First Order priority:** Should Phase 1 implement the Tier 1 Google Workspace + GCP provisioning Order first, or a simpler "dry-run" Order that validates a Terraform plan without applying it?
3. **Signing fallback:** Is GPG-signed BOM fallback acceptable, or do we require cosign keyless signing for all artifacts?
4. **Cross-tier PKI:** Do we use HashiCorp Vault for cross-tier mTLS, or do we accept cloud-native alternatives (Private CA + cert-manager) and accept the vendor lock-in?
5. **SIEM in Phase 1:** Do we build log export to GCS only in Phase 1, or also procure a SIEM (Chronicle, Splunk, Sentinel) immediately?
6. **Scope of first PR:** Should the first implementation PR include the full engine, or only the Order/Factory/BOM skeleton with a mocked Terraform runner?
7. **Terraform Cloud vs. self-managed:** Do we use Terraform Cloud/Enterprise for state management and run history, or a self-managed backend in GCS/Azure Blob?
8. **KOI integration:** Should the BOM schema be designed now to be ingestible by KOI-Net, or is that deferred until Phase 2?

### 16.2 Technical Decisions Documented

- **No IPFS:** The system uses SHA-256 hashes and cloud object storage instead of IPFS. (Existence proof: `ADCS-lifecycle-demo/` implements the full Order → evidence → attestation → BOM loop this way — bare SHA-256, named-graph store, no IPFS. See `concepts/adcs-to-cmmc-compliance-engine.md`.)
- **Tier 1 backend:** GCS inside the Assured Workloads IL4 folder.
- **Tier 2 backend:** Azure Blob Storage inside Azure Government.
- **Approval:** GitHub PR + GitHub Environment required reviewers (single-person approval).
- **Signing:** Sigstore cosign keyless via GitHub OIDC; Google Workspace as SSO anchor.
- **Cross-tier auth:** mTLS with Vault PKI (recommended) or cloud-native equivalent.
- **Policy engine:** OPA + Trivy + Checkov for pre-deployment; Azure Policy + GCP Org Policy for post-deployment.

---

## 17. Success Criteria

The project is successful when:

1. A Tier 1 environment can be provisioned by opening a GitHub PR and receiving a single approval.
2. The provisioning run produces a signed BOM that maps to at least 50 CMMC Level 2 controls with evidence hashes.
3. A C3PAO can retrieve the BOM and re-execute the Order to reproduce the environment.
4. No Tier 1 secret or state file is stored in Tier 0.
5. The system is ready to support NV011 and NV012 by July 22, 2026.
6. The architecture supports Tier 2 extension without redesign.

---

## 18. Phasing / Roadmap

### Phase 0 — Foundation (Days 1–5)

- Stand up Tier 1 Google Workspace + GCP Assured Workloads IL4 environment (per `cmmc-research/guides/tier1-buildout-plan.md`).
- Establish GitHub repo with CODEOWNERS, branch protection, signed commits, and environment reviewers.
- Configure GitHub OIDC → GCP Workload Identity Federation.

### Phase 1 — Tier 1 Compliance Engine (Weeks 2–4)

- Implement CATs-Compliance Controller skeleton (Order/Factory/BOM without IPFS).
- Implement the first Order: provision a Google Workspace CUI OU + GCP IL4 project.
- Integrate Terraform plan/state capture, Trivy/Checkov scanning, and OPA policy checks.
- Implement cosign keyless signing for BOMs.
- Store artifacts in GCS IL4 registry.

### Phase 2 — Multi-Framework Control Mapping (Weeks 5–6)

- Build the control mapping library for CMMC Level 2 and NIST SP 800-171 Rev 2.
- Generate BOMs that satisfy the NIST 800-171A Examine/Interview/Test evidence model.
- Support SPRS self-assessment submission workflow.

### Phase 3 — Tier 2 Design and Pilot (Weeks 7–10)

- Procure Microsoft 365 GCC High and Azure Government.
- Implement Tier 2 controller inside Tier 1 boundary.
- Implement cross-tier mTLS with Vault PKI.
- Implement the first Tier 2 Order: provision a GCC High workspace + Azure Gov resource group.
- Build IL5/ITAR control mapping.

### Phase 4 — Continuous Compliance and KOI Integration (Weeks 11+)

- Add drift detection and automated re-provisioning on policy change.
- Feed BOMs into KOI-Net for real-time compliance posture querying.
- Extend to FedRAMP High and other frameworks.

---

## 19. References

- `cmmc-research/guides/cmmc-0-to-100-guide.md` — CMMC Level 2 background research.
- `cmmc-research/guides/cmmc-bidding-plan.md` — DLA/DAF SBIR bidding plan.
- `cmmc-research/guides/tier1-buildout-plan.md` — Tier 1 environment buildout plan.
- `cmmc-research/requirements/compliance-evidence-requirements.md` — Compliance evidence mapping research.
- `cmmc-research/concepts/adcs-to-cmmc-compliance-engine.md` — Synthesis: how the ADCS traceability engine + the Control Requirements Catalog + the Traceability Matrix build this platform.
- `ADCS-lifecycle-demo/` — Working reference implementation of the Order → evidence → attestation → BOM loop (SHA-256, named-graph store; the design of record for content-addressing and attestation).
- `cats/cats/network/__init__.py` — Original CATs MeshClient implementation.
- `cats/cats/factory/__init__.py` — Original CATs Factory/Executor implementation.
- `cats/cats/service/__init__.py` — Original CATs Service orchestration.
- `cats/cats/node.py` — Original CATs Flask API endpoint.
- NIST SP 800-171 Rev 2: `https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final`
- 32 CFR Part 170 CMMC Final Rule: `https://public-inspection.federalregister.gov/2024-22905.pdf`
- DFARS 252.204-7021: `https://www.acquisition.gov/dfars/252.204-7021-cybersecurity-maturity-model-certification-level-2-requirements`
- GitHub OIDC docs: `https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers`
- Sigstore cosign: `https://docs.sigstore.dev/cosign/overview/`
- OPA Terraform tutorial: `https://www.openpolicyagent.org/docs/latest/terraform/`

---

*This document is a requirements draft. Implementation planning should address the open questions in Section 16 before proceeding.*
