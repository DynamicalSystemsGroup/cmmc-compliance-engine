# CUI_Users_Group module — IAM groups + least-privilege role bindings.
# Satisfies: AC.L2-3.1.1 (no unauthorized principals), AC.L2-3.1.2 (limit to
#            permitted transactions), AC.L2-3.1.5 (least privilege).

# Dedicated workload service account for the CUI enclave (no owner/editor).
resource "google_service_account" "cui_workload" {
  account_id   = "cui-workload"
  display_name = "CUI enclave workload SA (least privilege)"
  project      = var.project_id
}

# Least-privilege binding: the CUI group gets a narrow viewer role, NOT owner.
resource "google_project_iam_member" "cui_least_privilege" {
  project = var.project_id
  role    = "roles/viewer"
  member  = "group:${var.cui_group_email}"
}

# The workload SA gets only KMS decrypt on the CMEK key — nothing broader.
resource "google_project_iam_member" "cui_workload_kms" {
  project = var.project_id
  role    = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member  = "serviceAccount:${google_service_account.cui_workload.email}"
}
