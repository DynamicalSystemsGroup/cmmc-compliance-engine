# 5-Day Tier 1 (IL4 CMMC) Buildout Plan

> **Goal:** Move from a Tier 0 Google Workspace + GCP setup to a functioning **Tier 1 IL4 CMMC enclave** for NV011 and NV012.  
> **Assumption:** Team agrees to the tiered model, with Tier 1 as the target for current CUI work. Tier 2 (IL5/GCC High) remains a later buildout.  
> **Sources:** Google Workspace CMMC Implementation Guide (2025), Google Cloud Assured Workloads docs, Google Cloud Identity docs, NIST SP 800-171 Rev 2, 32 CFR Part 170, Secureframe/CMMC Dashboard practitioner guidance.

---

## What "fully functioning Tier 1" means after 5 days

This is a **functional, auditable CUI enclave**, not a completed CMMC certification. After 5 days you will have:

- A defined CUI boundary in Google Workspace and GCP.
- A hardened Google Workspace CUI OU with Enterprise Plus + Assured Controls Plus.
- A dedicated GCP IL4 Assured Workloads folder and project.
- Central identity management via Google Workspace / Cloud Identity.
- MFA enforced for all CUI users.
- Non-FedRAMP services disabled for CUI users.
- Audit logs exported to a retention mechanism.
- A draft SSP and evidence folder.
- CUI users provisioned and trained on the new boundary.

After 5 days, the remaining work is documenting and closing the remaining NIST controls, not rebuilding infrastructure.

---

## Current state assumptions

- Google Workspace exists for Tier 0 (general company use).
- GCP account exists, but it is also Tier 0 / mixed-use and needs cleanup.
- No separate identity platform beyond Google Workspace Admin.
- No Cloud Identity organization or Assured Workloads folder exists yet.
- ~20-person team, with only a subset needing CUI access.

---

## Target architecture

```
Tier 0 (Google Workspace + GCP) — general company, no CUI
│
├─ Tier 1 (IL4) — CUI enclave
│   ├─ Google Workspace Enterprise Plus + Assured Controls Plus
│   │   └─ Dedicated CUI OU with hardened settings
│   └─ GCP Assured Workloads IL4 folder
│       └─ Dedicated project(s) for NV011 / NV012 compute/storage
│
└─ Tier 2 (IL5/ITAR) — future buildout on GCC High
```

Identity is unified through **Google Workspace / Cloud Identity**:
- Workspace Admin Console governs users, OUs, MFA, and Google app access.
- Cloud Identity (free tier) governs GCP access; upgrade to Premium later if you need advanced endpoint/context-aware access.
- Third-party apps can use Google Workspace as a SAML/OIDC IdP.

---

## Day 1 — Cleanup, licensing, and organization setup

### Morning: Inventory and licensing

1. **Audit current Google Workspace licenses.**
   - Open Admin Console → Billing → Subscriptions.
   - Document current edition and renewal dates.
   - Identify users who will be in the CUI enclave.

2. **Purchase/upgrade to Google Workspace Enterprise Plus.**
   - Only Enterprise Plus supports the Assured Controls Plus add-on.
   - You can upgrade existing licenses or add Enterprise Plus licenses only for CUI users.
   - Contact Google Workspace sales or a partner; this is quote-based, not self-service in all regions.

3. **Purchase Assured Controls Plus add-on.**
   - Required for CMMC Level 2 data sovereignty (U.S. data residency + U.S. personnel access).
   - Apply only to the CUI OU initially to control cost.

4. **Request Google's CMMC Customer Responsibility Matrix (CRM).**
   - Email your Google Workspace customer success manager or sales rep.
   - Ask for the latest CMMC Implementation Guide and CRM.
   - This document is your map of what Google inherits vs. what you must implement.

### Afternoon: Google Cloud organization and identity

5. **Set up a Google Cloud Organization for Tier 1.**
   - If you already have a Workspace domain, follow: `https://cloud.google.com/identity/docs/set-up-cloud-identity-admin`
   - Verify your domain in Google Cloud if not already done.
   - Create an organization node in the Resource Manager.

6. **Enable required billing and APIs.**
   - Enable `assuredworkloads.googleapis.com`.
   - Enable `cloudidentity.googleapis.com`.
   - Enable `orgpolicy.googleapis.com`.
   - Ensure a billing account is linked.

7. **Create an IAM structure for separation of duties.**
   - `assuredworkloads.admin` for the person building the enclave.
   - `roles/owner` scoped to specific projects, not the whole org.
   - Avoid giving CUI users Organization Admin.

### End of Day 1 deliverables

- [ ] Enterprise Plus licenses ordered or upgraded.
- [ ] Assured Controls Plus ordered.
- [ ] Google Cloud Organization created and verified.
- [ ] Billing and APIs enabled.
- [ ] CRM/CMMC guide requested from Google.
- [ ] List of CUI users finalized.

---

## Day 2 — Workspace hardening and CUI OU

### Morning: Create the CUI OU and baseline policies

1. **Create a CUI Organizational Unit (OU) in Workspace Admin Console.**
   - Path: Directory → Organizational units → Create new.
   - Name it `CUI-Users` or `Tier1-CUI`.
   - Move only the confirmed CUI users into this OU.

2. **Create role-based groups for separation of duties.**
   - `CUI-Users` — access CUI data and apps.
   - `CUI-Admins` — manage CUI OU settings but not super-admin.
   - `Workspace-Super-Admins` — existing IT admins, not CUI data handlers.
   - Ensure the same person is not in both CUI-Admins and CUI-Users if possible.

3. **Apply Assured Controls Plus to the CUI OU.**
   - Once licensing is active, go to Security → Assured Controls.
   - Select the CUI OU and enable Assured Controls Plus.
   - Confirm U.S. data residency and U.S. support personnel restrictions.

### Afternoon: Lock down services and sharing

4. **Disable non-FedRAMP-authorized services for the CUI OU.**
   - Go to Apps → Additional Google Services.
   - Disable services not on the FedRAMP High in-scope list.
   - Disable third-party Marketplace apps unless individually verified FedRAMP-authorized.
   - Keep in scope: Gmail, Calendar, Drive, Docs, Sheets, Slides, Meet, Chat, Keep, Vault, Forms, Sites.
   - Note: re-check Google's current list, as it changes.

5. **Configure Drive sharing and DLP.**
   - Apps → Google Workspace → Drive and Docs → Sharing settings.
   - For CUI OU: disable external sharing, disable sharing with non-CUI OUs if possible.
   - Set up DLP rules to detect/block CUI keywords or patterns leaving the OU.

6. **Configure Gmail routing and DLP.**
   - Apps → Google Workspace → Gmail → Routing / Compliance.
   - Block CUI from being sent to external domains.
   - Consider adding external recipient warning banners.

7. **Enable Vault retention and eDiscovery.**
   - Vault is included with Enterprise Plus.
   - Set retention policies for CUI OU consistent with legal/contractual requirements.

### End of Day 2 deliverables

- [ ] CUI OU created and CUI users moved.
- [ ] Assured Controls Plus applied to CUI OU.
- [ ] Non-authorized services disabled for CUI OU.
- [ ] Drive and Gmail DLP/sharing rules configured.
- [ ] Vault retention set.

---

## Day 3 — GCP cleanup and Assured Workloads IL4

### Morning: Clean up existing GCP resources

1. **Inventory all existing GCP projects and resources.**
   - Use `gcloud projects list` or Cloud Console → IAM & Admin → Manage resources.
   - Tag/mark projects as Tier 0 (general) or unknown.
   - Do not delete anything yet; only document.

2. **Move non-CUI projects out of the Tier 1 org if they are in-scope.**
   - If existing projects are under the same organization, isolate them into a separate `Tier0-Production` folder.
   - Keep them out of the Assured Workloads IL4 folder.

3. **Delete or quarantine unused/test resources.**
   - Shut down unused Compute Engine VMs, storage buckets, and service accounts.
   - Rotate or delete old service account keys.
   - Remove IAM bindings for former employees or contractors.

### Afternoon: Create the Assured Workloads IL4 folder

4. **Create the Assured Workloads folder.**
   - Console → Compliance → Assured Workloads → Create.
   - Select **Regulatory Controls** → **Data Boundary for IL4**.
   - Choose a U.S. region (e.g., `us-central1`, `us-east1`, `us-west1`).
   - Name it clearly, e.g., `aw-tier1-il4-cui`.
   - Optional: configure a CMEK project/key ring during creation.

5. **Create a dedicated project for NV011/NV012 inside the IL4 folder.**
   - Project name: `tier1-cui-nv011-nv012` or similar.
   - Enable only required services: Compute Engine, Cloud Storage, Cloud SQL, Cloud Logging, Cloud Monitoring, Cloud KMS, IAM.
   - Disable unused APIs.

6. **Apply organization policies for U.S. residency and restricted services.**
   - `constraints/gcp.resourceLocations` → allow U.S. regions only.
   - `constraints/gcp.restrictServiceUsage` → allow only FedRAMP-authorized/IL4-supported services.
   - `constraints/iam.disableServiceAccountKeyCreation` → enforce key management best practice.

### End of Day 3 deliverables

- [ ] GCP inventory completed; unused resources cleaned up.
- [ ] Assured Workloads IL4 folder created.
- [ ] Dedicated CUI project created inside the IL4 folder.
- [ ] Organization policies applied for U.S. residency and service restrictions.
- [ ] CMEK project/key ring configured (if optional step was taken).

---

## Day 4 — Identity, MFA, and access control

### Morning: MFA and authentication

1. **Enforce MFA for all CUI users.**
   - Security → Authentication → 2-Step Verification.
   - For CUI OU: enforce 2-Step Verification.
   - Prefer hardware security keys (Titan, YubiKey) or phishing-resistant passkeys.
   - Allow TOTP as a fallback only if hardware keys are not feasible.
   - Disable SMS/voice as allowed methods for CUI OU.

2. **Configure password and session policies.**
   - Minimum length, complexity, and expiration per NIST 800-63B guidance.
   - Short session timeouts for CUI OU.
   - Block sign-ins from untrusted locations if possible.

3. **Set up Context-Aware Access (if available with your edition).**
   - Security → Access and data control → Context-Aware Access.
   - Require company-managed devices or trusted IP ranges for CUI apps.
   - If not available, document compensating controls in SSP.

### Afternoon: Central identity and role-based access

4. **Use Google Workspace as the central identity platform for Tier 1.**
   - For Google Workspace apps: use OU-based access control.
   - For GCP: grant access via IAM using Google Workspace group membership.
   - For third-party tools (SIEM, etc.): configure SAML/OIDC SSO using Google Workspace as the IdP.
   - If you need advanced SSO/endpoint management, evaluate Cloud Identity Premium ($7.20/user/month) after Week 1.

5. **Create least-privilege IAM roles in GCP.**
   - CUI developers: `roles/editor` scoped to the CUI project only.
   - CUI analysts: custom role with read-only + storage access.
   - Admins: `roles/owner` scoped to CUI project only.
   - No one gets Organization-level permissions unless absolutely necessary.

6. **Map users to projects.**
   - Use Google Groups to manage access:
     - `gcp-cui-nv011-nv012-editors`
     - `gcp-cui-nv011-nv012-viewers`
   - Bind these groups to IAM roles in the CUI project.
   - Document the access matrix in the SSP.

### End of Day 4 deliverables

- [ ] MFA enforced for CUI OU.
- [ ] Password/session policies configured.
- [ ] Context-Aware Access configured or compensating controls documented.
- [ ] Google Workspace groups created for CUI and GCP access.
- [ ] GCP IAM roles assigned least-privilege.

---

## Day 5 — Logging, encryption, and documentation

### Morning: Logging and monitoring

1. **Configure audit log export from Workspace.**
   - Reports → Manage Reports → Export to BigQuery or SIEM.
   - At minimum, export Admin, Drive, Gmail, Login, Groups, and SAML logs.
   - If you do not have a SIEM yet, export to a dedicated Cloud Storage bucket in the IL4 project with lifecycle rules for 3-year retention.

2. **Enable GCP audit logs.**
   - IAM & Admin → Audit Logs.
   - Enable Data Access logs for Cloud Storage, Compute Engine, Cloud KMS, and IAM.
   - Export logs to Cloud Logging and to Cloud Storage for long-term retention.

3. **Set up basic alerting.**
   - Cloud Monitoring alerts for:
     - Unusual login locations.
     - IAM policy changes.
     - External sharing attempts in CUI OU.
   - Workspace Alert Center rules for suspicious login activity.

### Afternoon: Encryption and documentation

4. **Enable Client-Side Encryption (CSE) in Workspace.**
   - CSE is available with Enterprise Plus.
   - Enable for Gmail, Drive, Docs, Sheets, Slides, and Meet in the CUI OU.
   - Choose a key management partner (Google-validated list) or use Virtru as an alternative encryption layer.
   - Document key custody in the SSP.

5. **Enable encryption in GCP.**
   - Use default Google-managed encryption for data at rest.
   - For stronger control, use Customer-Managed Encryption Keys (CMEK) in Cloud KMS.
   - Document key management responsibilities.

6. **Start the System Security Plan (SSP).**
   - Create a folder structure: `SSP/`, `Evidence/`, `Policies/`, `POA&M/`.
   - Draft sections:
     - System description and CUI boundary.
     - Network/data flow diagrams.
     - Asset inventory.
     - Control mappings for the 110 NIST 800-171 Rev 2 controls.
     - Google CRM cross-reference.
   - Use a template or start with the CMMC Dashboard / Google Workspace CMMC Implementation Guide.

7. **Create an evidence collection workflow.**
   - Screenshot configurations as you go.
   - Save policy documents with version dates.
   - Export IAM/group lists.
   - Store evidence in the Tier 1 Cloud Storage bucket or a controlled location.

### End of Day 5 deliverables

- [ ] Workspace and GCP audit logs exported and retained.
- [ ] Basic alerting configured.
- [ ] CSE or equivalent encryption enabled for CUI OU.
- [ ] GCP encryption documented.
- [ ] SSP draft started with boundary and asset inventory.
- [ ] Evidence folder structure created.

---

## What remains after 5 days

The 5-day buildout gives you the **technical foundation**. You will still need to complete:

| Area | Remaining work | Estimated time |
|------|----------------|----------------|
| **SSP** | Finish all 110 control implementation statements and evidence references. | 1–2 weeks |
| **Gap assessment** | Self-assess against all 110 controls; calculate SPRS score. | 3–5 days |
| **POA&M** | Document eligible gaps with remediation dates. | 2–3 days |
| **Policies** | Formalize access control, incident response, configuration management, media protection, training policies. | 1–2 weeks |
| **Training** | Security awareness training for CUI users; document completion. | 1 week |
| **SIEM** | If not yet purchased, procure and integrate a FedRAMP-authorized SIEM (e.g., Splunk, Chronicle, Sentinel). | 1–4 weeks |
| **Device management** | Enroll CUI devices in endpoint management; enforce disk encryption, patching, screen locks. | 1–2 weeks |
| **Incident response** | Finalize and test IR plan; establish 72-hour DoD reporting path. | 1–2 weeks |
| **SPRS submission** | Enter self-assessment results, obtain CMMC UID, complete affirmation. | 1–3 days |

Target: complete the remaining SSP and documentation work within **2–3 weeks** after the 5-day buildout, so you are ready to submit to SPRS before award.

---

## Cost estimate for 5-day buildout (CUI subset only)

| Item | Approximate cost |
|------|------------------|
| Google Workspace Enterprise Plus | ~$26/user/month (CUI users only) |
| Assured Controls Plus | ~$15/user/month (CUI users only) |
| Cloud Identity Premium (optional) | ~$7.20/user/month |
| GCP IL4 resources (Compute, Storage, Logs) | ~$200–$1,000/month depending on usage |
| SIEM (optional in Week 1; required later) | ~$500–$3,000/month |
| External KMS partner or Virtru (if using CSE) | ~$2,000–$10,000/year |
| Consulting/partner support (optional but recommended) | $5,000–$20,000 one-time |

For a 5-person CUI team, the first-year software cost is roughly **$15,000–$40,000** plus the consultant if needed.

---

## Key decisions to make during the 5 days

1. **CSE vs. Virtru:** Do you use Google's native Client-Side Encryption or Virtru as the encryption layer? CSE is more native; Virtru may be faster to deploy.
2. **SIEM choice:** If you do not have a SIEM, pick one quickly. Google Chronicle is a natural fit but requires setup. Splunk or Microsoft Sentinel are alternatives.
3. **Google partner vs. DIY:** Given the 5-day timeline, a Google CMMC partner can accelerate licensing and configuration. Consider engaging one by Day 1.
4. **Cloud Identity Premium:** Do you need the advanced endpoint/context-aware features now, or can you defer until after CMMC submission?
5. **Device policy:** Will CUI users use company-managed devices only, or will you allow BYOD with strong compensating controls?

---

## Immediate next actions (before starting Day 1)

- [ ] Identify the 3–5 users who will be in the Tier 1 CUI enclave.
- [ ] Assign an owner for the 5-day buildout (ideally a technical lead with Workspace + GCP admin rights).
- [ ] Contact Google Workspace sales to start Enterprise Plus + Assured Controls Plus procurement.
- [ ] Contact Google Cloud sales or a CMMC partner to assist with Assured Workloads setup if needed.
- [ ] Reserve the 5 days on the calendar and block meetings for the buildout team.

---

## Official references

- Google Workspace CMMC Implementation Guide: `https://services.google.com/fh/files/misc/google_workspace_cmmc_implementation_guide_2025.pdf`
- Google Workspace FedRAMP Configuration Guide: `https://knowledge.workspace.google.com/admin/compliance/google-workspace-fedramp-configuration-guide`
- Google Cloud Assured Workloads docs: `https://cloud.google.com/assured-workloads/docs`
- Google Cloud Identity setup: `https://cloud.google.com/identity/docs/set-up-cloud-identity-admin`
- NIST SP 800-171 Rev 2: `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-171r2.pdf`
- CMMC 2.0 Final Rule: `https://public-inspection.federalregister.gov/2024-22905.pdf`

---

*This plan gets the technical enclave operational in 5 days. Full CMMC Level 2 documentation and SPRS submission are follow-on work estimated at 2–3 additional weeks.*
