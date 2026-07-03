"""Key material for the signing abstraction.

Two key sources live here, matching the two signer implementations:

- A **deterministic dev keypair** used by `Ed25519LocalSigner`. The private
  seed is derived by hashing a fixed constant, so the same Ed25519 key is
  reconstructed in every process. The engine relies on this determinism: a
  signature over the same content byte-reproduces across runs, machines, and
  CI, which keeps fixtures and golden artifacts stable. This key is a
  *development* key only; it is not secret and must never protect real trust.

- A **KMS key reference** for the real, deferred cosign path. The reference
  (a `gcpkms://...` URI) is read from the environment rather than hardcoded,
  so the production signer can be pointed at a Cloud KMS key without code
  changes. In this sandbox the variable is unset, so the reference is `None`
  and the cosign signer reports itself unavailable.
"""

from __future__ import annotations

import hashlib
import os

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)

# Constant seeded into SHA-256 to derive the deterministic dev private key.
# The "/v1" suffix lets us rotate the dev key deliberately if ever needed
# (a new suffix yields a new, still-deterministic key) without disturbing
# existing fixtures that pin the current key id.
_DEV_SEED_LABEL = b"compliance-engine/dev-signing-key/v1"

# Environment variable naming the Cloud KMS key for the real cosign path.
KMS_KEY_ENV = "CE_COSIGN_KMS_KEY"


def dev_private_key() -> Ed25519PrivateKey:
    """Return the deterministic development Ed25519 private key.

    The 32-byte seed is `sha256(_DEV_SEED_LABEL)`, so the exact same key is
    rebuilt in every process. This is a dev key, not a secret.
    """
    seed = hashlib.sha256(_DEV_SEED_LABEL).digest()
    return Ed25519PrivateKey.from_private_bytes(seed)


def dev_public_key() -> Ed25519PublicKey:
    """Return the public half of the deterministic dev key."""
    return dev_private_key().public_key()


def dev_public_key_bytes() -> bytes:
    """Return the raw (32-byte) Ed25519 public key bytes for the dev key."""
    return dev_public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw,
    )


def dev_key_id() -> str:
    """Return a stable short identifier for the dev key.

    Defined as the first 16 hex characters of `sha256(public_key_bytes)`.
    Because the dev key is deterministic, this id is stable across processes
    and is safe to embed in fixtures and attestation records.
    """
    return hashlib.sha256(dev_public_key_bytes()).hexdigest()[:16]


def kms_key_ref_from_env() -> str | None:
    """Return the Cloud KMS key reference for the real cosign path, if set.

    Reads `CE_COSIGN_KMS_KEY` (expected to be a `gcpkms://...` URI). Returns
    `None` when the variable is unset or empty, which is the signal used by
    `CosignKmsSigner.available()` to report the real path as unavailable.
    """
    ref = os.environ.get(KMS_KEY_ENV)
    if ref:
        return ref
    return None
