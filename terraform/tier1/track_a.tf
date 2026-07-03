# Track A machine modules — null_resource placeholders where the target API
# isn't cleanly Terraform-manageable (CrowdStrike, GitHub, Chrome Cloud Mgmt,
# BeyondCorp policy, Workspace Admin identity policy, SCC scan schedules).
# Each placeholder carries its module + control mapping in `triggers` so the
# plan-JSON binding path resolves them the same as any real resource. Live
# evidence resolution happens through the fixture-backed generators today, and
# via API resolvers per authoritative-source in the live phase.

resource "null_resource" "endpoint_edr" {
  triggers = {
    module       = "EndpointVerification_CrowdStrike"
    authsrc      = "CrowdStrike"
    cmmc_control = "si-l2-3-14-2"
  }
}

resource "null_resource" "mdm_chromeos" {
  triggers = {
    module       = "MDM_ChromeOS"
    authsrc      = "Chrome_Cloud_Mgmt"
    cmmc_control = "ac-l2-3-1-18"
  }
}

resource "null_resource" "scc_vuln_mgmt" {
  triggers = {
    module       = "SecurityCommandCenter"
    authsrc      = "GCP_SCC"
    cmmc_control = "ra-l2-3-11-2"
  }
}

resource "null_resource" "workspace_admin_policy" {
  triggers = {
    module       = "WorkspaceAdmin_Policy"
    authsrc      = "Workspace_AdminSDK"
    cmmc_control = "ia-l2-3-5-1"
  }
}

resource "null_resource" "beyondcorp_remote" {
  triggers = {
    module       = "VPNAccess_BeyondCorp"
    authsrc      = "GCP_BeyondCorp"
    cmmc_control = "ac-l2-3-1-13"
  }
}

resource "null_resource" "github_change_mgmt" {
  triggers = {
    module       = "ChangeManagement_GitHub"
    authsrc      = "GitHub_API"
    cmmc_control = "cm-l2-3-4-5"
  }
}

resource "null_resource" "ops_mfa" {
  triggers = {
    module       = "CloudIdentity_RemoteMaintenance"
    authsrc      = "Workspace_AdminSDK"
    cmmc_control = "ma-l2-3-7-5"
  }
}

resource "null_resource" "binauth_allowlist" {
  triggers = {
    module       = "OrgPolicy_Allowlist"
    authsrc      = "GCP_BinaryAuth"
    cmmc_control = "cm-l2-3-4-8"
  }
}

resource "null_resource" "session_control" {
  triggers = {
    module       = "OrgPolicy_SessionControl"
    authsrc      = "GCP_CloudIdentity"
    cmmc_control = "ac-l2-3-1-11"
  }
}

resource "null_resource" "vpc_service_controls" {
  triggers = {
    module       = "AccessTransparency_ExternalSystems"
    authsrc      = "GCP_VPCServiceControls"
    cmmc_control = "ac-l2-3-1-20"
  }
}

resource "null_resource" "iam_privileged" {
  triggers = {
    module       = "IAMRoles_Privilege"
    authsrc      = "GCP_IAM"
    cmmc_control = "ac-l2-3-1-6"
  }
}
