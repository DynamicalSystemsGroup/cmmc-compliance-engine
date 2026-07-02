# structural/ — the cloud topology + control→resource allocation

**Purpose.** Model the Tier 1 (IL4) and Tier 2 (IL5) cloud architecture as SysMLv2/RDF, and declare which design element (Terraform resource / Workspace setting) **satisfies** each control. This is the machine form of the Traceability Matrix's "implementation statement" column. Loaded into `<ce:structural>`.

**Port from ADCS.** `structural/satellite.ttl` + `structural/parameters.ttl` — same shape (design elements + `sysml:SatisfyRequirementUsage` linking element → requirement), retargeted from satellite hardware to cloud resources.

**Design.**
- Each provisioned resource is a `sysml:PartUsage` (e.g. `ce:WorkspaceCUI_OU`, `ce:AzureKeyVault_FIPS`).
- Allocation edge: resource `sysml:satisfyingElement` control (reuses the ADCS allocation query + the attestation module's evidence-presentation unchanged).
- Content mirrors `reference/guides/tier1-buildout-plan.md` (Tier 1) and the requirements doc §11 (Tier-specific evidence tables).

**Files.**
- `tier1.ttl` — Google Workspace Enterprise Plus + Assured Controls Plus OU, GCP Assured Workloads IL4 folder/project, IAM groups, CMEK, DLP, log export. **(stub present)**
- `tier2.ttl` — GCC High workspace, Azure Gov RG, Conditional Access, Key Vault FIPS HSM, NSG deny-all, diagnostic settings. *(Phase 3)*

**Inputs:** buildout guides + Terraform module metadata (`cmmc:controlsSatisfied` tags). **Outputs:** `<ce:structural>`; the allocation column of Document 2.
