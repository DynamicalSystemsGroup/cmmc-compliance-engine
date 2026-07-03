"""Signing abstraction for attestation records and artifacts.

Public API for cryptographically signing and verifying the bytes the engine
produces. Key-based signing only: a deterministic local Ed25519 signer (the
demo/fixture default), an honest unsigned `NullSigner`, and a deferred
cosign+Cloud KMS production signer. See `signer.py` for the algorithm details.
"""

from __future__ import annotations

from compliance_engine.signing.keys import (
    dev_key_id,
    dev_public_key_bytes,
    kms_key_ref_from_env,
)
from compliance_engine.signing.signer import (
    ALGO_COSIGN,
    ALGO_ED25519,
    ALGO_NONE,
    CosignKmsSigner,
    Ed25519LocalSigner,
    NullSigner,
    Signer,
    SigningError,
    default_local_signer,
    get_signer,
)

__all__ = [
    "Signer",
    "NullSigner",
    "Ed25519LocalSigner",
    "CosignKmsSigner",
    "get_signer",
    "default_local_signer",
    "SigningError",
    "ALGO_NONE",
    "ALGO_ED25519",
    "ALGO_COSIGN",
    "dev_key_id",
    "dev_public_key_bytes",
    "kms_key_ref_from_env",
]
