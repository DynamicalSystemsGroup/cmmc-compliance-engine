# evidence/ — content hashing + RDF binding + generators

**Purpose.** Turn provisioning outputs into hashed `rtm:Evidence` nodes bound to the controls they address. Evidence **addresses** a control; it never **satisfies** one (only attestation does). Loaded into `<ce:evidence>`.

**Port from ADCS — much of this is reused as-is.**
- `evidence/hashing.py` → **reuse verbatim.** SHA-256 over canonical content is domain-agnostic. (`hash_docker_image` also transfers directly to Terraform module hashing.)
- `evidence/binding.py` → **reuse, relabel.** `bind_proof_evidence` / `bind_simulation_evidence` become `bind_check_evidence` / `bind_config_evidence`; the PROV execution-metadata capture (where/how a check ran) transfers unchanged.
- ADCS `analysis/` engines (SymPy/scipy) → replaced by `generators/` (policy-as-code + config export).

**generators/** (see `generators/DESIGN.md`) — the compliance analogues of the ADCS analysis engines:
- **Static (pre-apply):** `terraform show -json`, Checkov, Trivy, OPA/Rego → check-result evidence.
- **Live (post-apply):** config exporters — Workspace 2SV policy JSON, GCP Org Policy, IAM bindings, Azure Conditional Access, Key Vault + CMVP cert, diagnostic/log settings → config-export evidence.

**Contract every generator honors:**
1. Emit a raw artifact (JSON/text) → SHA-256 via `hashing.py`.
2. Write the artifact to the tier registry (`backends/`) keyed by hash.
3. Bind an `rtm:Evidence` node: `rtm:contentHash`, `rtm:evidenceMethod`, `rtm:addresses cmmc:<control>`, `prov:wasGeneratedBy` the collection activity, `rtm:documentRef` into the registry.

**Inputs:** live cloud/tenant + Terraform state. **Outputs:** `<ce:evidence>`; the evidence-hash + evidence-location columns of Document 2.
