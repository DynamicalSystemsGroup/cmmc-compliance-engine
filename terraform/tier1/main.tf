# Tier 1 IL4 enclave — root wiring + the machine-readable control map.
#
# `local.cmmc_modules` mirrors structural/tier1.ttl EXACTLY: each key is a
# tier1.ttl module (ce:<Module>), listing the cmmc:Control ids it satisfies.
# One `terraform_data.cmmc_tag` per module carries that mapping into the plan
# JSON, so evidence/generators/terraform_plan.py can map planned resources →
# controls mechanically (no cloud, no guesswork). Resources that support GCP
# `labels` ALSO carry `cmmc_control = <slug>` inline (see kms.tf / logging.tf).
#
# Control-label slug convention (GCP label charset: [a-z0-9_-]):
#   cmmc:SC.L2-3.13.11  ->  "sc-l2-3-13-11"   (lowercased, '.'/'-' -> '-')
# The tag ALSO carries the exact control ids, so binding never has to reverse
# the slug.

locals {
  # module id (tier1.ttl) -> its controls + provenance flags. Mirrors tier1.ttl.
  cmmc_modules = {
    Workspace2SV_CUI_OU = {
      controls  = ["IA.L2-3.5.3", "IA.L2-3.5.2", "IA.L2-3.5.4"]
      resources = ["googleworkspace_group.cui_users", "null_resource.workspace_2sv_enforcement"]
      inherited = false
    }
    CMEK_KeyRing = {
      controls  = ["SC.L2-3.13.11", "SC.L2-3.13.10", "SC.L2-3.13.16"]
      resources = ["google_kms_key_ring.cui", "google_kms_crypto_key.cui_cmek"]
      inherited = false
    }
    CUI_Users_Group = {
      controls  = ["AC.L2-3.1.1", "AC.L2-3.1.2", "AC.L2-3.1.5"]
      resources = ["google_service_account.cui_workload", "google_project_iam_member.cui_least_privilege"]
      inherited = false
    }
    Drive_DLP_Rules = {
      controls  = ["AC.L2-3.1.3"]
      resources = ["null_resource.drive_dlp_rules"]
      inherited = false
    }
    OrgPolicy_USRegion = {
      controls  = ["SC.L2-3.13.1"]
      resources = ["google_org_policy_policy.resource_locations"]
      inherited = false
    }
    AuditLog_Export = {
      controls  = ["AU.L2-3.3.1", "AU.L2-3.3.2", "AU.L2-3.3.5"]
      resources = ["google_storage_bucket.audit_logs", "google_logging_project_sink.audit"]
      inherited = false
    }
    Disable_NonFedRAMP_Services = {
      controls  = ["CM.L2-3.4.6", "CM.L2-3.4.7"]
      resources = ["google_org_policy_policy.restrict_services"]
      inherited = false
    }
    Terraform_Baseline = {
      controls  = ["CM.L2-3.4.1", "CM.L2-3.4.2"]
      resources = ["null_resource.terraform_baseline"]
      inherited = false
    }
    Monitoring_Alerting = {
      controls  = ["SI.L2-3.14.3", "SI.L2-3.14.6"]
      resources = ["null_resource.monitoring_alerting"]
      inherited = false
    }
    VPC_Segmentation = {
      controls  = ["SC.L2-3.13.3", "SC.L2-3.13.4", "SC.L2-3.13.5",
                   "SC.L2-3.13.6", "SC.L2-3.13.7", "SC.L2-3.13.8",
                   "SC.L2-3.13.9", "SC.L2-3.13.15"]
      resources = ["google_compute_network.cui",
                   "google_compute_subnetwork.cui_private",
                   "google_compute_firewall.deny_all_ingress",
                   "google_compute_firewall.allow_internal_tls"]
      inherited = false
    }
    EndpointVerification_CrowdStrike = {
      controls  = ["SI.L2-3.14.2", "SI.L2-3.14.4", "SI.L2-3.14.7"]
      resources = ["null_resource.endpoint_edr"]
      inherited = false
    }
    MDM_ChromeOS = {
      controls  = ["AC.L2-3.1.16", "AC.L2-3.1.17", "AC.L2-3.1.18",
                   "AC.L2-3.1.19", "MP.L2-3.8.7"]
      resources = ["null_resource.mdm_chromeos"]
      inherited = false
    }
    SecurityCommandCenter = {
      controls  = ["RA.L2-3.11.2", "SI.L2-3.14.1", "SI.L2-3.14.5"]
      resources = ["null_resource.scc_vuln_mgmt"]
      inherited = false
    }
    WorkspaceAdmin_Policy = {
      controls  = ["IA.L2-3.5.1", "IA.L2-3.5.5", "IA.L2-3.5.6", "IA.L2-3.5.7",
                   "IA.L2-3.5.8", "IA.L2-3.5.9", "IA.L2-3.5.10", "IA.L2-3.5.11"]
      resources = ["null_resource.workspace_admin_policy"]
      inherited = false
    }
    VPNAccess_BeyondCorp = {
      controls  = ["AC.L2-3.1.12", "AC.L2-3.1.13", "AC.L2-3.1.14"]
      resources = ["null_resource.beyondcorp_remote"]
      inherited = false
    }
    ChangeManagement_GitHub = {
      controls  = ["CM.L2-3.4.3", "CM.L2-3.4.5"]
      resources = ["null_resource.github_change_mgmt"]
      inherited = false
    }
    CloudIdentity_RemoteMaintenance = {
      controls  = ["MA.L2-3.7.5"]
      resources = ["null_resource.ops_mfa"]
      inherited = false
    }
    CloudLogging_Config = {
      controls  = ["AU.L2-3.3.4", "AU.L2-3.3.7", "AU.L2-3.3.8", "AU.L2-3.3.9"]
      resources = ["google_storage_bucket.audit_logs", "google_logging_project_sink.audit"]
      inherited = false
    }
    OrgPolicy_Allowlist = {
      controls  = ["CM.L2-3.4.8", "CM.L2-3.4.9"]
      resources = ["null_resource.binauth_allowlist"]
      inherited = false
    }
    OrgPolicy_SessionControl = {
      controls  = ["AC.L2-3.1.8", "AC.L2-3.1.10", "AC.L2-3.1.11"]
      resources = ["null_resource.session_control"]
      inherited = false
    }
    AccessTransparency_ExternalSystems = {
      controls  = ["AC.L2-3.1.20"]
      resources = ["null_resource.vpc_service_controls"]
      inherited = false
    }
    IAMRoles_Privilege = {
      controls  = ["AC.L2-3.1.6", "AC.L2-3.1.7"]
      resources = ["null_resource.iam_privileged"]
      inherited = false
    }
    # CSP-inherited physical protection: NOT machine-provable at plan time
    # (MET-by-inheritance, human-attested). Tagged for traceability, but the
    # generator skips binding a plan-derived PASS for inherited modules.
    CSP_Physical_Inheritance = {
      controls  = ["PE.L2-3.10.1", "PE.L2-3.10.2"]
      resources = ["null_resource.csp_physical_inheritance"]
      inherited = true
    }
  }
}

# One tag resource per tier1.ttl module. Always present in the plan JSON with a
# fully-known `input` (terraform_data is built-in: no provider, no credentials).
resource "terraform_data" "cmmc_tag" {
  for_each = local.cmmc_modules

  input = {
    module    = each.key
    controls  = each.value.controls
    resources = each.value.resources
    region    = var.primary_region
    inherited = each.value.inherited
  }
}

# -- Terraform baseline (CM.L2-3.4.1/2) — IaC baseline + inventory marker. -----
resource "null_resource" "terraform_baseline" {
  triggers = {
    cmmc_control = "cm-l2-3-4-1"
    module       = "Terraform_Baseline"
    project      = var.project_id
  }
}

# -- Monitoring + alerting (SI.L2-3.14.3/6) — placeholder for the alerting -----
#    stack (alert policies require notification channels not modelled here).
resource "null_resource" "monitoring_alerting" {
  triggers = {
    cmmc_control = "si-l2-3-14-3"
    module       = "Monitoring_Alerting"
  }
}

# -- CSP-inherited physical protection (PE.L2-3.10.1/2) — inheritance marker. --
resource "null_resource" "csp_physical_inheritance" {
  triggers = {
    cmmc_control = "pe-l2-3-10-1"
    module       = "CSP_Physical_Inheritance"
    inherited     = "google-workspace-crm"
  }
}
