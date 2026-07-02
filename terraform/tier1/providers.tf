# Tier 1 IL4 enclave — providers.
#
# Two real providers (GCP + Google Workspace). The generator's plan-time path
# (evidence/generators/terraform_plan.py) runs `terraform plan` with a dummy
# GOOGLE_OAUTH_ACCESS_TOKEN and no cloud: create-only plans never mint a token,
# so the plan succeeds offline. `terraform test` replaces BOTH providers with
# mock_provider blocks (see tests/tier1.tftest.hcl) so plan+apply run with no
# credentials and no cloud at all.

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
    googleworkspace = {
      source  = "hashicorp/googleworkspace"
      version = "~> 0.7"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.primary_region
  # No `credentials` here on purpose: the mock-provider (terraform test) and the
  # plan-only generator path both run without real credentials. In a real run,
  # credentials come from the environment (ADC / GOOGLE_CREDENTIALS).
}

provider "googleworkspace" {
  customer_id = var.workspace_customer_id
}
