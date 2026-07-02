# pipeline/ — the Factory (executes an Order, produces a BOM)

**Purpose.** The runtime **back half**. Take a signed Order (from the separate
`order-compiler/`), build the environment from it, and produce a signed BOM
that is the compliance proof. The Factory's only input is an Order file — it is
decoupled from how the Order was made.

**Port from ADCS.** `pipeline/runner.py` (PipelineState + per-stage free
functions + fail-fast preflight probe) and `pipeline/plan.ttl` (the p-plan SOP)
transfer directly. Keep the Typer narrow-waist CLI and the "no silent degrade"
preflight. Every stage emits a `p-plan:Activity` so the build process is itself
queryable — proof the SOP was followed.

## Factory stages (executing one Order)

```
0  Load Order          verify signature; load required-control set + module refs
   Approval gate       GitHub PR + environment reviewer (separation of duties;
                         Tier 2 needs a second Compliance-Officer approval)
1  Fetch by hash       pull the exact modules + policies from the registry
2  terraform plan      → plan hash                             [static evidence]
3  policy-as-code      OPA/Checkov/Trivy on the plan → check hashes
                         FAILS HERE ⇒ STOP before building anything
4  terraform apply     BUILDS the real environment → state hash [gated]
5  live tests          run oracles/ against what was built → test hashes
6  assemble BOM        control-mapping: resource → control → evidence hash
6.5 closure rules      SHACL suite (incl. PoamLegalityShape)
7  GATE 2 attestation  Affirming Official: MET/NOT MET per control  [HUMAN]
7a audit               forward/backward vs. the Order's required-control set;
                         SPRS score + POA&M-legality (traceability/sprs.py)
8  sign + store        Sigstore-sign the BOM; write-once to the tier registry;
                         return the BOM hash
```

Steps 2–5 are **provisioning that emits evidence as a byproduct** — not
after-the-fact scraping. The pre-apply policy check (step 3) is the safety
valve: a non-compliant blueprint never gets built.

## The Order (input)
A signed file naming: target tier + standard, contract id, scope (data classes,
authorized personnel), and the module/policy **hashes** to use. It also carries
its derivation (COP hash, control-set hash, coverage-proof hash) so the Factory
can confirm Gate 1 held before it starts. See `../order-compiler/`.

## Re-execution (`/verify`)
An auditor re-runs the same Order to rebuild the identical environment and
digest-compares — the ADCS `compute.reproduce` loop retargeted to Terraform.

**Files.** `runner.py` (Factory orchestrator, stub), `plan.ttl` (SOP model,
stub). **Inputs:** a signed Order. **Outputs:** the full dataset + a signed,
stored BOM.
