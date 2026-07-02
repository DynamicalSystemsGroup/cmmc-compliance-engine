# evidence/generators/ — policy-as-code + config-export engines

The compliance analogues of ADCS `analysis/` (SymPy/scipy). Each generator
produces evidence for one or more controls, hashes it, stores it, and binds it.

## Two families

**Static (pre-apply)** — run against the Terraform plan JSON:
| Generator | Tool | Example controls |
| --- | --- | --- |
| `tf_plan.py` | `terraform show -json` | CM.L2-3.4.1 (baseline config) |
| `checkov.py` | Checkov | SC.*, AC.* misconfig checks |
| `trivy.py` | Trivy | SI.* vulnerability/config |
| `opa.py` | OPA/Rego | region, tagging, allowed-services |

**Live (post-apply)** — export live tenant/cloud config:
| Generator | Source | Example controls |
| --- | --- | --- |
| `workspace.py` | Admin SDK: 2SV, DLP, sharing | IA.L2-3.5.3, AC.L2-3.1.3 |
| `gcp_policy.py` | Org Policy, IAM bindings | AC.L2-3.1.1/2, SC.L2-3.13.x |
| `azure_ca.py` | Conditional Access, Key Vault | IA.L2-3.5.3, SC.L2-3.13.11 |
| `cmvp.py` | CMVP certificate lookup | SC.L2-3.13.11 (FIPS) |
| `logging.py` | log-sink + retention config | AU.L2-3.3.1/2 |

## Interface (every generator implements)

```python
class Generator(Protocol):
    controls: list[str]                     # cmmc control ids it addresses
    def collect(self, ctx: RunContext) -> list[EvidenceArtifact]: ...
```

`EvidenceArtifact` carries the raw bytes + a machine-readable `summary` dict
whose keys are exactly what `oracles/criteria.py` reads (e.g.
`{"mfa_enforced_privileged": True, "key_admin_region": "US"}`). This is the
seam between evidence and oracle: the generator observes, the oracle judges
the observation against the control's criterion.

## Phase 0 note
Ship **mocked** generators first (return canned `summary` dicts) so the whole
pipeline runs end-to-end and produces an SSP before any live cloud wiring —
mirrors the ADCS `--auto` path.
