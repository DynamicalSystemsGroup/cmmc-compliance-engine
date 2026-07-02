# Minimal self-contained HCL fixture for U8 TerraformBackend tests.
# Uses the built-in `terraform_data` resource (no external provider, so
# `terraform init -backend=false` works offline). Each resource carries the
# compliance labels (cmmc_module / cmmc_control / region) that
# pipeline/provision/base.parse_plan_json lifts into a PlanResult. This is NOT
# terraform/tier1/ (U14 owns that) — it exists only to exercise the mechanism.

terraform {
  required_version = ">= 1.4"
}

# A US-region resource mapping to a real tier1.ttl module + control.
resource "terraform_data" "org_policy" {
  input = {
    cmmc_module  = "OrgPolicy_USRegion"
    cmmc_control = "SC.L2-3.13.1"
    region       = "us-central1"
  }
}

resource "terraform_data" "cmek" {
  input = {
    cmmc_module  = "CMEK_KeyRing"
    cmmc_control = "SC.L2-3.13.11, SC.L2-3.13.16"
    region       = "us-central1"
  }
}
