# CMEK_KeyRing module — Cloud KMS CMEK keyring + key (FIPS-validated crypto).
# Satisfies: SC.L2-3.13.11 (FIPS module), SC.L2-3.13.10 (key management),
#            SC.L2-3.13.16 (CUI encrypted at rest).

resource "google_kms_key_ring" "cui" {
  name     = "cui-cmek"
  location = var.kms_location
  # NB: google_kms_key_ring has no `labels` argument; its control tag lives on
  # the companion terraform_data.cmmc_tag["CMEK_KeyRing"] (see main.tf).
}

resource "google_kms_crypto_key" "cui_cmek" {
  name     = "cui-cmek-key"
  key_ring = google_kms_key_ring.cui.id
  purpose  = "ENCRYPT_DECRYPT"

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "HSM" # HSM-backed => FIPS 140-2/3 validated module.
  }

  labels = {
    cmmc_control = "sc-l2-3-13-11"
    tier         = "tier1-il4"
  }
}
