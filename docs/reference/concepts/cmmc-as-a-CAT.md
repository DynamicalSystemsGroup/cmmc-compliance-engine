## “Compliance-as-a-CAT”

> **Note: Status — origin vision (2026-07-02).** This is the *first* framing of "Compliance-as-a-CAT," kept for its conceptual leap: treat environment provisioning as an Order that produces a Compliance BOM. Two things have since been settled and **supersede this document where they conflict**:
>
> 1. **No IPFS.** This doc pins artifacts to IPFS and says "CID" throughout because early CATs used IPFS. The platform does **not**. Content-addressing is done with **SHA-256 hashes stored in a tiered cloud registry** (GCS for Tier 1, Azure Blob for Tier 2). Wherever this doc says "IPFS," "pin," "MeshClient," or "CID," read **"SHA-256 content hash in the tiered registry."** The authoritative decision is `requirements/cats-compliance-engine-requirements.md` §5 and §16.2.
> 2. **There is already a reference implementation.** `ADCS-lifecycle-demo/` implements this exact Order → evidence → attestation → BOM loop with bare SHA-256 (no IPFS) and a named-graph store — which is what validated decision #1. The buildout mapping this vision onto it is `concepts/adcs-to-cmmc-compliance-engine.md`.
>
> Read this doc for the *idea*; read those two for the *design of record*.

---

Treat each Tier 2 environment provisioning as a **CAT Order** that produces a **Compliance BOM**.

The Order specifies:

- **Target standard**: IL5, ITAR, CMMC Level 2 (C3PAO), DFARS 252.204-7012, etc.
- **Inputs**: contract ID, project scope, authorized personnel, required data classes.
- **Transformations**: Terraform modules, policy validation scripts, compliance tests.
- **Infrastructure**: GCC High tenant, Azure Government resource group, network rules, IAM roles, DLP policies, encryption settings.

The **Factory** executes the Order by:

1. Running Terraform to provision the GCC High / Azure IL5 environment.
2. Capturing the `tfstate` and plan output.
3. Running compliance assertions against the live environment (e.g., Azure Policy, Open Policy Agent, CIS benchmarks, custom NIST 800-171 control checks).
4. Generating a **BOM** that contains:
    - CID of the Terraform plan.
    - CID of the `tfstate`.
    - CID of each compliance test result.
    - CID of the generated policy/configuration exports.
    - A signed attestation that the environment satisfies the target standard.

The BOM is the compliance proof. Anyone — internal security, a C3PAO, a prime contractor — can retrieve it by CID and re-execute the same Order to reproduce the environment and verify the result.

---

## Creative extensions

### 1. Immutable, content-addressed tfstate

Instead of storing `tfstate` in a generic S3 bucket or Terraform Cloud, pin it to IPFS through the CATs MeshClient. The state file becomes tamper-evident. Every change to the environment produces a new CID. If someone later claims the environment was misconfigured, you can diff the CID chain and see exactly when the drift occurred.

> **Reconciliation:** not IPFS. `tfstate` is hashed with SHA-256 and stored write-once in the tiered registry (GCS IL4 / Azure Blob IL5); each apply produces a new hash, and the hash chain gives the same tamper-evident drift history without IPFS. See the top banner and requirements doc §13.3.

### 2. “Compliance Orders” as SOPs

Your organization’s standard operating procedures become executable CAT Orders. For example:

- **SOP-IL5-001**: Provision a new GCC High project workspace for ITAR technical data.
- **SOP-CMMC-017**: Revoke all access and archive resources when a project ends.

Each SOP is a content-addressed Order. When an operator runs it, the Factory produces a BOM that proves the SOP was followed exactly. This turns human compliance processes into machine-verifiable provenance.

### 3. Automated control mapping

Each Terraform module is tagged with the CMMC/NIST controls it satisfies. After provisioning, the Factory generates a mapping like:

| Control       | Resource                                            | Evidence CID | Status |
| ------------- | --------------------------------------------------- | ------------ | ------ |
| SC.L2-3.13.11 | `azurerm_key_vault` FIPS module                     | `bafybei...` | MET    |
| IA.L2-3.5.3   | `azuread_conditional_access_policy` MFA enforcement | `bafybei...` | MET    |
| AC.L2-3.1.1   | `azuread_group` CUI-Users                           | `bafybei...` | MET    |

This becomes the living SSP. The C3PAO does not have to read a static PDF; they can re-execute the BOM and verify each control independently.

### 4. Continuous compliance via CAT mesh

Tier 1 and Tier 2 run as separate CAT Mesh nodes. Tier 1 can submit a provisioning Order to Tier 2 without the IL5 data ever flowing down. Tier 2 executes the Order, generates a BOM, and returns only the BOM CID to Tier 1. The asymmetric information flow you described earlier happens naturally: Tier 2 can pull context from Tier 1, but Tier 1 only sees attestation hashes, not the high-side data.

### 5. Re-executable C3PAO evidence packages

When a C3PAO arrives, you do not hand them a folder of screenshots. You hand them a set of BOM CIDs. They can:

- Re-run the Terraform plan to reproduce the infrastructure.
- Re-run the compliance tests.
- Verify that the live environment matches the recorded state.
- Check that every policy change since the last assessment is content-addressed.

This reduces assessment time and increases trust.

### 6. “Digital twin” of the compliance posture

KOI (or a similar knowledge graph) could ingest CATs BOMs as graph nodes. The graph becomes a real-time model of your compliance posture: nodes are controls, resources, projects, and people; edges are content-addressed proofs. When a project ends and its resources are spun down, the graph updates automatically. You can query it: “Which projects currently satisfy IA.L2-3.5.3?” and get an answer backed by CIDs.

---

## A possible architecture

```
Tier 0 (Google Workspace)
    ↓ submits Order CID
Tier 1 CAT Node (IL4 GCP)
    ↓ dispatches provisioning Order to Tier 2
Tier 2 CAT Node (IL5 / GCC High / Azure Gov)
    ↓ executes Terraform modules
    ↓ runs compliance tests
    ↓ captures tfstate
    ↓ produces Compliance BOM
    ↓ returns BOM CID to Tier 1
```

Each Tier 2 CAT Node is a small Kubernetes service running inside a GCC High / Azure Government environment. It exposes a minimal API:

- `POST /provision` — accepts a CAT Order, runs Terraform, returns BOM.
- `POST /verify` — re-executes a BOM, compares live state to recorded state, returns diff.
- `POST /archive` — runs the de-provisioning SOP, returns archive BOM.

The Terraform modules are stored as content-addressed artifacts on IPFS. The CAT Node retrieves the exact module version by CID, so module drift is impossible.

> **Reconciliation:** "on IPFS" → "in the content-addressed registry (GCS/Azure Blob), keyed by SHA-256." Module drift is prevented by pinning the exact hash in the Order, exactly as the requirements doc specifies (FR-1.2, FR-3.1).

---

## What this gets you

- **Auditability**: Every environment, every change, every control claim has a CID.
- **Reproducibility**: You can rebuild any environment from a BOM.
- **Non-repudiation**: The BOM is signed; you cannot retroactively claim a control was met if it was not recorded.
- **Automation**: Provisioning and compliance checking become the same operation.
- **Scalability**: Each new contract gets its own workspace by running a standard Order.
- **Separation of tiers**: Tier 1 does not need to see Tier 2 data; it only sees proofs.

---

## Open questions to narrow this down

1. **Scope**: Are you thinking about this for just GCC High/Azure IL5, or should it also handle the Tier 1 IL4 provisioning on GCP?
2. **Compliance framework**: CMMC Level 2 only, or do you want the same system to support ITAR, FedRAMP High, NIST 800-53, etc.?
3. **Terraform backend**: Do you want to keep using Terraform Cloud/Enterprise, or should CATs itself manage the state via IPFS? _(**Resolved:** neither as originally posed — state lives in a self-managed backend, GCS/Azure Blob inside the compliance boundary, hashed with SHA-256. See requirements doc §16.2.)_
4. **Verification engine**: Terraform + `terraform validate` only, or do you want policy-as-code (OPA, Sentinel, Azure Policy) as part of the BOM?
5. **Human-in-the-loop**: Should the provisioning Order require an approval signature before execution, or fully automated?
