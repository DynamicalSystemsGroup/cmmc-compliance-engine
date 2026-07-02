# backends/ — the tiered content-addressed registry

**Purpose.** Persist evidence/BOM artifacts keyed by SHA-256, write-once, in
the correct compliance boundary per tier. Content-addressing is SHA-256 into
these stores — **not IPFS** (requirements doc §16.2; the ADCS engine is the
existence proof).

**Port from ADCS.** `pipeline/backends/` (Local / Flexo / Fuseki) already
abstracts persistence behind one interface with a fail-fast `probe()`
preflight. Add two implementations:

| Backend | Tier | Store | Immutability |
| --- | --- | --- | --- |
| `local.py` | dev | disk | — (dev only) |
| `gcs.py` | Tier 1 (IL4) | GCS in the Assured Workloads IL4 folder | Object Versioning + retention/Object Lock |
| `azure_blob.py` | Tier 2 (IL5) | Azure Blob in Azure Government | immutable-storage policy |

**Interface (inherited).**
```python
class Backend(Protocol):
    def probe(self) -> None: ...              # preflight; raise → fail fast (exit 2)
    def put(self, sha256: str, data: bytes, meta: dict) -> str: ...   # write-once
    def get(self, sha256: str) -> bytes: ...
    def index(self, contract_id: str, bom_hash: str) -> None: ...     # registry index
```

**Tier separation.** The "Tier 2 returns only a BOM hash to Tier 1" rule is
the ADCS per-substrate `rtm:operatedBy` auspices + named-graph partitioning:
Tier 1 submits an Order over mTLS; Tier 2 provisions, writes its own registry,
and hands back only the hash. IL5 data never flows down.

**Inputs:** artifacts from `evidence/`. **Outputs:** the registry + index
(`contract_id → latest BOM hash`, `bom_hash → artifact hashes`,
`control_id → BOMs claiming MET`).
