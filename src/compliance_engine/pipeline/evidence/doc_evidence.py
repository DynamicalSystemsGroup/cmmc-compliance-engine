"""Document evidence capture — the machine-recorded artifact behind a human attestation.

A Track B control (policy / training / personnel — CA.L2-3.12.4 "maintain the SSP",
for example) cannot be measured by a config oracle. Its truth lives in a document in
an authoritative source. This module turns the ``ce:Reference`` URI for such a control
into a *machine-recorded* evidence artifact so the human attestation is no longer a bare
"trust me":

    1. RESOLVE   the ce:uri to the real file on disk (a dead link is caught here).
    2. HASH      its bytes with SHA-256 — the content fingerprint the attestation cites.
    3. PROVENANCE capture the git commit that last changed it (author + date) — this is
       "the CO edited the doc and committed it," recorded from git, not typed by hand.
    4. RECEIPT   sign an upload receipt over (reference, sha256, git_commit, uploaded_by)
       with the local Ed25519 signer — "the official signed that he uploaded this."

The result is bound into the ``<ce:evidence>`` named graph as a ``ce:DocumentEvidence``
node. When the run persists to the append-only Flexo tier, that node is committed with
everything else, so it earns a Flexo version id — the durable "uploaded into Flexo"
anchor an assessor can resolve later.

This module does NOT judge the *substance* of the document — that is the human's job,
captured in the AO attestation. It records the bureaucratic, machine-checkable facts:
the doc exists, here is its exact content hash, here is the commit that produced it, and
here is a signature proving who lodged it.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

import compliance_engine

# Reference URIs are written file://documents/policies/X.md as a *logical* path into
# the authoritative doc store; the store physically lives under the package directory.
_DOCS_BASE = Path(compliance_engine.__file__).resolve().parent          # src/compliance_engine
_REPO_ROOT = _DOCS_BASE.parent.parent                                   # repo root


@dataclass(frozen=True)
class DocEvidence:
    """A machine-recorded evidence artifact behind an attested-reference control."""
    reference_id: str
    uri: str
    resolved_path: str | None          # repo-relative path, or None if unresolvable
    exists: bool                       # did the URI resolve to a real file?
    sha256: str | None                 # content fingerprint (None if unresolvable)
    git_commit: str | None             # last commit that touched the file
    git_author: str | None
    git_committed_at: str | None       # ISO-8601
    uploaded_by: str                   # the official who lodged it
    upload_sig: str | None             # base64 Ed25519 sig over the upload receipt
    upload_sig_algo: str               # signer.algo, or "none" if unsigned/unresolvable

    @property
    def short_hash(self) -> str:
        return (self.sha256 or "")[:12]


def resolve_uri(uri: str) -> Path | None:
    """Map a ``file://documents/...`` reference URI to a real file on disk.

    Tries the package doc store first (where the policy docs live), then the repo
    root, so a logical ``file://documents/policies/X.md`` resolves regardless of the
    physical layout. Returns None if nothing resolves (a dead link — the oracle turns
    that into a hard ``reference-unresolvable`` failure)."""
    if not uri:
        return None
    rel = uri
    for prefix in ("file://", "file:"):
        if rel.startswith(prefix):
            rel = rel[len(prefix):]
            break
    rel = rel.lstrip("/")
    for base in (_DOCS_BASE, _REPO_ROOT):
        candidate = (base / rel).resolve()
        if candidate.is_file():
            return candidate
    return None


def _git_provenance(path: Path) -> tuple[str | None, str | None, str | None]:
    """Return (commit, author, iso_date) of the last commit touching ``path``.

    Uses ``git log -1``; returns (None, None, None) if git is unavailable or the file
    is untracked (an honest 'no recorded provenance' rather than a fabricated value)."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%H%x1f%an%x1f%aI", "--", str(path)],
            cwd=_REPO_ROOT, capture_output=True, text=True, timeout=10, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return (None, None, None)
    line = out.stdout.strip()
    if out.returncode != 0 or not line:
        return (None, None, None)
    parts = line.split("\x1f")
    if len(parts) != 3:
        return (None, None, None)
    return (parts[0], parts[1], parts[2])


def _upload_receipt_bytes(reference_id: str, sha256: str, git_commit: str | None,
                          uploaded_by: str) -> bytes:
    """Canonical bytes the upload signature covers."""
    payload = {
        "reference": reference_id,
        "sha256": sha256,
        "git_commit": git_commit or "",
        "uploaded_by": uploaded_by,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def capture(reference_id: str, uri: str, uploaded_by: str, *, signer=None) -> DocEvidence:
    """Resolve, hash, capture git provenance, and sign an upload receipt for one
    reference. An unresolvable URI yields a DocEvidence with exists=False (no hash,
    no receipt) — the oracle turns that into a hard failure downstream."""
    path = resolve_uri(uri)
    if path is None:
        return DocEvidence(
            reference_id=reference_id, uri=uri, resolved_path=None, exists=False,
            sha256=None, git_commit=None, git_author=None, git_committed_at=None,
            uploaded_by=uploaded_by, upload_sig=None, upload_sig_algo="none",
        )
    sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    commit, author, committed_at = _git_provenance(path)

    # Sign the upload receipt: "this official lodged this exact content / commit."
    import base64

    from compliance_engine.signing import default_local_signer

    signer = signer or default_local_signer()
    sig = signer.sign(_upload_receipt_bytes(reference_id, sha256, commit, uploaded_by))
    try:
        rel = str(path.relative_to(_REPO_ROOT))
    except ValueError:
        rel = str(path)
    return DocEvidence(
        reference_id=reference_id, uri=uri, resolved_path=rel, exists=True,
        sha256=sha256, git_commit=commit, git_author=author, git_committed_at=committed_at,
        uploaded_by=uploaded_by,
        upload_sig=base64.b64encode(sig).decode("ascii"), upload_sig_algo=signer.algo,
    )


def verify_upload_receipt(ev: DocEvidence) -> bool:
    """Re-verify the signed upload receipt. False if unsigned/unresolvable or the
    signature does not check out (offline, deterministic)."""
    if not ev.exists or not ev.sha256 or ev.upload_sig_algo == "none" or not ev.upload_sig:
        return False
    import base64

    from compliance_engine.signing import SigningError, get_signer

    try:
        signer = get_signer(ev.upload_sig_algo)
        return signer.verify(
            _upload_receipt_bytes(ev.reference_id, ev.sha256, ev.git_commit, ev.uploaded_by),
            base64.b64decode(ev.upload_sig, validate=True),
        )
    except (SigningError, ValueError):
        return False


def bind_doc_evidence(graph, ev: DocEvidence):
    """Materialize a DocEvidence into the evidence graph as a ce:DocumentEvidence node.

    Returns the node IRI. Records the content hash, git provenance, uploader, and signed
    upload receipt so the attestation can point at machine-recorded facts, and so the
    node travels into Flexo with the rest of the evidence graph."""
    from rdflib import Literal, URIRef
    from rdflib.namespace import RDF

    from compliance_engine.ontology.prefixes import CE, PROV

    node = CE[f"DE-{ev.reference_id}"]
    graph.add((node, RDF.type, CE.DocumentEvidence))
    graph.add((node, CE.reference, CE[ev.reference_id]))
    graph.add((node, CE.uri, URIRef(ev.uri)))
    graph.add((node, CE.uploadedBy, Literal(ev.uploaded_by)))
    if ev.sha256:
        graph.add((node, CE.contentHash, Literal(ev.sha256)))
    if ev.resolved_path:
        graph.add((node, CE.resolvedPath, Literal(ev.resolved_path)))
    if ev.git_commit:
        graph.add((node, CE.gitCommit, Literal(ev.git_commit)))
    if ev.git_author:
        graph.add((node, CE.gitAuthor, Literal(ev.git_author)))
    if ev.git_committed_at:
        graph.add((node, CE.gitCommittedAt, Literal(ev.git_committed_at)))
    if ev.upload_sig:
        graph.add((node, CE.uploadReceiptSig, Literal(ev.upload_sig)))
        graph.add((node, CE.uploadReceiptSigAlgo, Literal(ev.upload_sig_algo)))
    # Attribute the upload to the official (prov), and link the reference back.
    graph.add((node, PROV.wasAttributedTo, Literal(ev.uploaded_by)))
    graph.add((CE[ev.reference_id], CE.documentEvidence, node))
    return node
