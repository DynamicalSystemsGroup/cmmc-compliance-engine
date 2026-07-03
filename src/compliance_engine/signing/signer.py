"""Signer abstraction for attestation records and artifacts.

The engine cryptographically binds trust to the bytes it produces. Rather than
scatter `cryptography` and `subprocess` calls across the pipeline, every
producer signs through one small `Signer` interface and every consumer verifies
through it. Three algorithms are supported, each a concrete `Signer`:

- `ALGO_NONE` (`NullSigner`): no cryptographic signature. Trust is external —
  git history, a private registry, an out-of-band channel. There is nothing to
  sign; verification only accepts the empty signature. This is the honest
  "unsigned" record rather than a fake signature.

- `ALGO_ED25519` (`Ed25519LocalSigner`): a real, *deterministic* local Ed25519
  signature using the dev key from `keys.py`. It is the default for demos,
  fixtures, and tests because the same content always yields the same signature
  bytes, so golden artifacts stay stable.

- `ALGO_COSIGN` (`CosignKmsSigner`): the real, production path — `cosign
  sign-blob` / `verify-blob` against a Cloud KMS key. It is DEFERRED: the
  `cosign` binary and GCP KMS are absent from this sandbox, so the signer
  reports itself unavailable and raises a clear `SigningError` rather than
  pretending to work. The subprocess wiring is implemented so the real path is
  a matter of environment, not code.

`get_signer(algo)` dispatches by algorithm name; `default_local_signer()`
returns the Ed25519 signer used everywhere a demo/fixture default is wanted.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import typing
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from compliance_engine.signing.keys import (
    dev_key_id,
    dev_private_key,
    dev_public_key_bytes,
    kms_key_ref_from_env,
)

# Algorithm identifiers. These strings are stable and are what attestation
# records persist to name the signer that produced a signature.
ALGO_NONE = "none"
ALGO_ED25519 = "ed25519-v1"
ALGO_COSIGN = "cosign-v1"

__all__ = [
    "ALGO_NONE",
    "ALGO_ED25519",
    "ALGO_COSIGN",
    "SigningError",
    "Signer",
    "NullSigner",
    "Ed25519LocalSigner",
    "CosignKmsSigner",
    "get_signer",
    "default_local_signer",
]


class SigningError(RuntimeError):
    """Raised when signing or verifying cannot be performed.

    Distinct from a verification *failure* (which returns `False`): this is
    raised when the operation itself is impossible — an unsigned algorithm was
    asked to sign, an unknown algorithm was requested, or the deferred
    cosign+KMS path was invoked without the binary or key present.
    """


@typing.runtime_checkable
class Signer(typing.Protocol):
    """Structural interface every signer implements.

    `algo` names the algorithm (one of the `ALGO_*` constants). `sign` returns
    the detached signature bytes for `content`; `verify` returns whether `sig`
    authenticates `content`. `available` reports whether this signer can
    actually run in the current environment.
    """

    algo: str

    def sign(self, content: bytes) -> bytes:
        """Return the detached signature over `content`."""
        ...

    def verify(self, content: bytes, sig: bytes) -> bool:
        """Return whether `sig` authenticates `content`."""
        ...

    def available(self) -> bool:
        """Return whether this signer can operate in this environment."""
        ...


class NullSigner:
    """The honest "unsigned" signer: trust is external (git/registry).

    There is no signature to produce, so `sign` always raises. `verify` accepts
    only the empty signature, `b""`, which is the byte string an unsigned
    record carries; any non-empty bytes are rejected because this algorithm
    never emitted them.
    """

    algo = ALGO_NONE

    def sign(self, content: bytes) -> bytes:
        raise SigningError(
            "NullSigner cannot sign: the 'none' algorithm carries no signature "
            "(trust is external, e.g. git history or a private registry)"
        )

    def verify(self, content: bytes, sig: bytes) -> bool:
        return sig == b""

    def available(self) -> bool:
        return True


class Ed25519LocalSigner:
    """Real, deterministic local Ed25519 signer using the dev key.

    Backed by the deterministic dev key from `keys.py`, so a signature over
    identical content byte-reproduces across processes — the property fixtures
    and golden artifacts depend on. `verify` never raises: an invalid signature
    (including one over tampered content) returns `False`.
    """

    algo = ALGO_ED25519

    def __init__(self) -> None:
        self._private_key = dev_private_key()
        self.public_key_bytes = dev_public_key_bytes()
        self.key_id = dev_key_id()

    def sign(self, content: bytes) -> bytes:
        return self._private_key.sign(content)

    def verify(self, content: bytes, sig: bytes) -> bool:
        public_key = Ed25519PublicKey.from_public_bytes(self.public_key_bytes)
        try:
            public_key.verify(sig, content)
        except InvalidSignature:
            return False
        return True

    def available(self) -> bool:
        return True


class CosignKmsSigner:
    """Real production signer over `cosign sign-blob` + Cloud KMS (DEFERRED).

    `available()` is `True` only when the `cosign` binary is on `PATH` and a
    KMS key reference is configured via `CE_COSIGN_KMS_KEY`. In this sandbox
    neither is present, so `available()` is `False` and both `sign` and
    `verify` raise `SigningError` with a clear message instead of attempting a
    subprocess call. The subprocess wiring below is implemented so that, given
    the binary and key, the real path works without further code changes.
    """

    algo = ALGO_COSIGN

    def __init__(self) -> None:
        self.kms_key_ref = kms_key_ref_from_env()

    def _cosign_path(self) -> str | None:
        return shutil.which("cosign")

    def available(self) -> bool:
        return self._cosign_path() is not None and self.kms_key_ref is not None

    def _require_available(self) -> None:
        if not self.available():
            raise SigningError(
                "cosign+KMS not available in this environment: it requires the "
                "'cosign' binary on PATH and a Cloud KMS key reference in "
                "CE_COSIGN_KMS_KEY (gcpkms://...). This path is deferred in the "
                "current sandbox."
            )

    def sign(self, content: bytes) -> bytes:
        self._require_available()
        cosign = typing.cast(str, self._cosign_path())
        with tempfile.TemporaryDirectory() as tmp:
            blob = Path(tmp) / "blob"
            blob.write_bytes(content)
            result = subprocess.run(
                [
                    cosign,
                    "sign-blob",
                    "--key",
                    typing.cast(str, self.kms_key_ref),
                    "--yes",
                    "--output-signature",
                    "-",
                    str(blob),
                ],
                capture_output=True,
                check=False,
            )
            if result.returncode != 0:
                raise SigningError(
                    "cosign sign-blob failed: "
                    + result.stderr.decode("utf-8", "replace").strip()
                )
            # cosign emits the detached signature on stdout.
            return result.stdout.strip()

    def verify(self, content: bytes, sig: bytes) -> bool:
        self._require_available()
        cosign = typing.cast(str, self._cosign_path())
        with tempfile.TemporaryDirectory() as tmp:
            blob = Path(tmp) / "blob"
            sig_file = Path(tmp) / "blob.sig"
            blob.write_bytes(content)
            sig_file.write_bytes(sig)
            result = subprocess.run(
                [
                    cosign,
                    "verify-blob",
                    "--key",
                    typing.cast(str, self.kms_key_ref),
                    "--signature",
                    str(sig_file),
                    str(blob),
                ],
                capture_output=True,
                check=False,
            )
            return result.returncode == 0


def get_signer(algo: str) -> Signer:
    """Return the `Signer` for `algo`, or raise `SigningError` if unknown."""
    if algo == ALGO_NONE:
        return NullSigner()
    if algo == ALGO_ED25519:
        return Ed25519LocalSigner()
    if algo == ALGO_COSIGN:
        return CosignKmsSigner()
    raise SigningError(f"unknown signing algorithm: {algo!r}")


def default_local_signer() -> Signer:
    """Return the default signer for demos, fixtures, and tests.

    Always the deterministic `Ed25519LocalSigner`, so artifacts signed by the
    default path reproduce byte-for-byte.
    """
    return Ed25519LocalSigner()
