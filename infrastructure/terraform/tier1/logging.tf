# AuditLog_Export module — audit log sink to retained Cloud Storage.
# Satisfies: AU.L2-3.3.1 (create/retain audit logs), AU.L2-3.3.2 (trace user
#            actions), AU.L2-3.3.5 (correlate/report).

resource "google_storage_bucket" "audit_logs" {
  name                        = var.log_bucket_name
  location                    = var.primary_region
  force_destroy               = false
  uniform_bucket_level_access = true

  retention_policy {
    # 7 years — CUI audit retention.
    retention_period = 220752000
  }

  labels = {
    cmmc_control = "au-l2-3-3-1"
    tier         = "tier1-il4"
  }
}

resource "google_logging_project_sink" "audit" {
  name        = "cui-audit-sink"
  destination = "storage.googleapis.com/${google_storage_bucket.audit_logs.name}"

  # Route all admin-activity + data-access audit logs.
  filter = "logName:\"cloudaudit.googleapis.com\""

  unique_writer_identity = true
}
