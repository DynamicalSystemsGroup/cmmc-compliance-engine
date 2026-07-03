"""Tests for the signing abstraction (`compliance_engine.signing`).

Asserts the properties the engine relies on:
- Ed25519 round trip and tamper detection (content and signature).
- Determinism: the deterministic dev key yields identical signatures and a
  stable key id across independent signer instances.
- `NullSigner` accepts only the empty signature and never "signs".
- `get_signer` dispatch over all three algorithms, and its error on unknown.
- The deferred cosign path reports unavailable and raises here (cosign/KMS
  are absent from this sandbox).
"""

from __future__ import annotations

import pytest

from compliance_engine.signing import (
    ALGO_COSIGN,
    ALGO_ED25519,
    ALGO_NONE,
    CosignKmsSigner,
    Ed25519LocalSigner,
    NullSigner,
    SigningError,
    default_local_signer,
    dev_key_id,
    get_signer,
)

_CONTENT = b"attestation record: AC.L2-3.1.1 PASS"


def test_ed25519_round_trip():
    signer = Ed25519LocalSigner()
    sig = signer.sign(_CONTENT)
    assert signer.verify(_CONTENT, sig) is True


def test_ed25519_tamper_content_fails():
    signer = Ed25519LocalSigner()
    sig = signer.sign(_CONTENT)
    tampered = bytearray(_CONTENT)
    tampered[0] ^= 0x01
    assert signer.verify(bytes(tampered), sig) is False


def test_ed25519_tamper_signature_fails():
    signer = Ed25519LocalSigner()
    sig = bytearray(signer.sign(_CONTENT))
    sig[0] ^= 0x01
    assert signer.verify(_CONTENT, bytes(sig)) is False


def test_ed25519_deterministic_across_instances():
    a = Ed25519LocalSigner().sign(_CONTENT)
    b = Ed25519LocalSigner().sign(_CONTENT)
    assert a == b


def test_dev_key_id_is_stable():
    assert dev_key_id() == dev_key_id()
    assert Ed25519LocalSigner().key_id == dev_key_id()


def test_null_signer_verify_empty_signature():
    signer = NullSigner()
    assert signer.verify(_CONTENT, b"") is True
    assert signer.verify(_CONTENT, b"abc") is False


def test_null_signer_sign_raises():
    with pytest.raises(SigningError):
        NullSigner().sign(_CONTENT)


def test_get_signer_dispatch():
    assert isinstance(get_signer(ALGO_NONE), NullSigner)
    assert isinstance(get_signer(ALGO_ED25519), Ed25519LocalSigner)
    assert isinstance(get_signer(ALGO_COSIGN), CosignKmsSigner)


def test_get_signer_unknown_raises():
    with pytest.raises(SigningError):
        get_signer("totally-unknown-algo")


def test_default_local_signer_is_ed25519():
    signer = default_local_signer()
    assert isinstance(signer, Ed25519LocalSigner)
    assert signer.algo == ALGO_ED25519


def test_cosign_unavailable_and_raises():
    signer = CosignKmsSigner()
    assert signer.available() is False
    with pytest.raises(SigningError):
        signer.sign(_CONTENT)
    with pytest.raises(SigningError):
        signer.verify(_CONTENT, b"whatever")
