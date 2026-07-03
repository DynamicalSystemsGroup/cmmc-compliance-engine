# Org Policy modules.
#   OrgPolicy_USRegion          -> SC.L2-3.13.1  (US-only resource locations;
#                                   ALSO the ITAR-120.54 residency basis)
#   Disable_NonFedRAMP_Services -> CM.L2-3.4.6/7 (least functionality)

locals {
  # US regions map to the built-in "us-locations" value group; a non-US region
  # (the safety-valve variant) flows straight through as an explicit region, so
  # the plan JSON carries the residency violation for the generator to catch.
  region_is_us      = can(regex("^us(-|$)", var.primary_region))
  allowed_locations = local.region_is_us ? ["in:us-locations"] : ["in:${var.primary_region}"]
}

resource "google_org_policy_policy" "resource_locations" {
  name   = "projects/${var.project_id}/policies/gcp.resourceLocations"
  parent = "projects/${var.project_id}"

  spec {
    rules {
      values {
        allowed_values = local.allowed_locations
      }
    }
  }
}

resource "google_org_policy_policy" "restrict_services" {
  name   = "projects/${var.project_id}/policies/gcp.restrictServiceUsage"
  parent = "projects/${var.project_id}"

  spec {
    rules {
      # Deny-by-default: only FedRAMP-authorized services may be enabled.
      values {
        denied_values = ["ALL_UNSPECIFIED"]
      }
    }
  }
}

resource "google_org_policy_policy" "disable_sa_key_creation" {
  name   = "projects/${var.project_id}/policies/iam.disableServiceAccountKeyCreation"
  parent = "projects/${var.project_id}"

  spec {
    rules {
      enforce = "TRUE"
    }
  }
}
