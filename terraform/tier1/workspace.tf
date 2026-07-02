# Workspace modules.
#   Workspace2SV_CUI_OU -> IA.L2-3.5.3/2/4 (phishing-resistant 2SV on CUI OU)
#   Drive_DLP_Rules     -> AC.L2-3.1.3      (control the flow of CUI)
#
# The Google Workspace API surface is only partially Terraform-manageable. The
# CUI users group IS manageable via googleworkspace_group; 2SV enforcement and
# DLP rules are not cleanly TF-manageable, so they are null_resource
# placeholders carrying their control tag in `triggers`.
#
# `enable_workspace` is false on the generator's offline plan path (so the
# googleworkspace provider is never configured and needs no credentials); it is
# set true under `terraform test`, where mock_provider stands in for the API.

resource "googleworkspace_group" "cui_users" {
  count = var.enable_workspace ? 1 : 0
  email = var.cui_group_email
  name  = "CUI Users"
}

resource "null_resource" "workspace_2sv_enforcement" {
  triggers = {
    cmmc_control = "ia-l2-3-5-3"
    module       = "Workspace2SV_CUI_OU"
    policy       = "phishing-resistant-2sv-enforced-on-CUI-OU"
  }
}

resource "null_resource" "drive_dlp_rules" {
  triggers = {
    cmmc_control = "ac-l2-3-1-3"
    module       = "Drive_DLP_Rules"
    policy       = "drive-gmail-dlp-cui-flow"
  }
}
