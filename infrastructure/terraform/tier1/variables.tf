# Tier 1 IL4 enclave — input variables.

variable "project_id" {
  type        = string
  description = "GCP project id for the CUI enclave."
  default     = "nv012-cui-mock"
}

variable "org_id" {
  type        = string
  description = "GCP organization id (parent for org policies / folder)."
  default     = "000000000000"
}

variable "primary_region" {
  type        = string
  description = <<-EOT
    Primary GCP region for all CUI resources. MUST be a US region for
    SC.L2-3.13.1 (data residency) + the ITAR-120.54 residency basis. The
    plan-evidence generator's policy safety valve reads this out of the real
    plan JSON and FAILs the region check if it is non-US.
  EOT
  default     = "us-central1"
}

variable "kms_location" {
  type        = string
  description = "Cloud KMS keyring location (US multi-region by default)."
  default     = "us"
}

variable "cui_group_email" {
  type        = string
  description = "IAM group email for CUI users."
  default     = "cui-users@nv012.example.mil"
}

variable "log_bucket_name" {
  type        = string
  description = "GCS bucket name for the retained audit-log sink."
  default     = "nv012-cui-audit-logs"
}

variable "workspace_customer_id" {
  type        = string
  description = "Google Workspace customer id (mocked in terraform test)."
  default     = "C0mockcust"
}

variable "enable_workspace" {
  type        = bool
  description = <<-EOT
    Instantiate the real googleworkspace_* resources. Left false on the
    generator's offline `terraform plan` path (so the googleworkspace provider
    is never configured and no credentials are needed); set true under
    `terraform test`, where mock_provider stands in for the real API.
  EOT
  default     = false
}
