# `fixtures/nv012/` — mocked evidence exports for the NV012 run

These JSON files stand in for **real GCP / Google Workspace config exports**.
The mocked generators (`evidence/generators/*`, U6) read them and emit
`EvidenceArtifact`s; the oracles (`oracles/criteria.py`, U7) read each file's
`summary` dict and compare it to a machine criterion. Every artifact is marked
`evidentiary_status: "mock"` — it **addresses** a control but is **not** real
evidence (R12 non-evidentiary marker).

## Envelope schema (every file)

| Field                | Type        | Meaning                                                        |
| -------------------- | ----------- | -------------------------------------------------------------- |
| `source_system`      | string      | export origin, e.g. `workspace.2sv`, `gcp.kms`, `gcp.iam`      |
| `export_command`     | string      | the (illustrative) command that produced the raw export       |
| `collected_at`       | ISO-8601    | collection timestamp → `CollectionMetadata.collected_at`       |
| `collector_version`  | string      | mock collector version → `CollectionMetadata.collector_version`|
| `controls`           | string[]    | CMMC control id(s) this export **addresses** (`ce:addresses`)  |
| `evidentiary_status` | string      | always `"mock"` for fixtures                                   |
| `raw`                | object      | realistic GCP/Workspace-shaped payload (hashed as raw bytes)   |
| `summary`            | object      | **machine-readable** metrics the oracle reads (schema below)   |

The `source_system`, `export_command`, `collected_at`, and `collector_version`
fields map onto U6's `CollectionMetadata {source_system, export_command,
collected_at, collector_version}`.

## `summary` schema (keys = oracle `metric_key`s in `oracles/criteria.py`)

| `summary` key              | type    | criterion (control)          | passes when   |
| -------------------------- | ------- | ---------------------------- | ------------- |
| `mfa_enforced_privileged`  | bool    | `IA.L2-3.5.3` (`eq true`)    | `true`        |
| `fips_module_present`      | bool    | `SC.L2-3.13.11` (`eq true`)  | `true`        |
| `cui_encrypted_at_rest`    | bool    | `SC.L2-3.13.16` (`eq true`)  | `true`        |
| `unauthorized_principals`  | int     | `AC.L2-3.1.1` (`eq 0`)       | `0`           |
| `data_region`              | string  | `ITAR-120.54` (`eq "US"`)    | `"US"`        |

Each fixture file carries exactly one criterion's metric in its `summary`; the
generator run unions them into the per-control evidence summary.

## The three labelled sets

| Set              | Files                                                                 | Purpose (U13)                                                                                           |
| ---------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `all-covered/`   | all 5 exports, **every criterion passes**                            | happy path — Gate 1 passes, Factory completes, **SPRS 110/Final** (mock-marked).                        |
| `gap/`           | 4 exports — **omits `gcp_kms_cmvp.json`** (the FIPS module)          | drives a **Gate-1 refusal**: `SC.L2-3.13.11` has no claiming module/evidence → Order refused, gap named.|
| `contradiction/` | all 5 exports, but `mfa_enforced_privileged: false`                  | oracle for `IA.L2-3.5.3` **fails**; when the Affirming Official attests MET the audit's contradiction dimension fires (**MET-over-failed-oracle**, R13). |

### Set file inventory

- **`all-covered/`**: `workspace_2sv.json`, `gcp_kms_cmvp.json`,
  `gcp_cmek_at_rest.json`, `gcp_iam_bindings.json`, `gcp_org_policy_region.json`
- **`gap/`**: same **minus** `gcp_kms_cmvp.json` (FIPS evidence for
  `SC.L2-3.13.11` absent → the metric `fips_module_present` never appears).
- **`contradiction/`**: same five as `all-covered/`, with the MFA export patched
  so `mfa_enforced_privileged: false` (oracle `failed`).
