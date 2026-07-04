"""Audit-package report: render package/manifest.json into a human report.

The signed manifest (traceability/package.py) is the source of truth. This module
renders it into a clean, self-contained HTML report and, when the ``weasyprint``
binary is available, a paged PDF. The PDF is a human rendering of the signed
manifest, not a second source of truth: its cover and footer carry the manifest
hash and signature so a reader can re-verify the underlying package with
``uv run ce verify-package``.

Design: minimal, government-report restraint. One serif body face, a single slate
accent, horizontal rules only, no color-coded chrome, no emoji. Print CSS sets a
running header, page numbers, and a repeated NON-EVIDENTIARY stamp on mock runs.

PDF engine: the ``weasyprint`` CLI is invoked via subprocess (its own native libs),
which avoids the Python-binding system-library issues. If the binary is absent, the
HTML is still written and the caller is told to install weasyprint or print the HTML.
"""

from __future__ import annotations

import hashlib
import html
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]

# Plain-text labels (no emoji) for the coverage/verification kinds.
_KIND_LABEL = {
    "machine": "Machine-verified",
    "attested": "Attested-reference",
    "inherited": "CSP-inherited",
    "unclaimed": "Unclaimed",
}


def _esc(value) -> str:
    return html.escape(str(value if value is not None else ""))


def _short(h: str, n: int = 16) -> str:
    return h[:n] + "…" if h and len(h) > n else (h or "")


# ---------------------------------------------------------------------------
# Full-catalog coverage (for the appendix) — read live from the graph
# ---------------------------------------------------------------------------

def _catalog_coverage() -> list[dict]:
    """All 110 controls with weight, requirement text, and verification kind
    (machine / attested / inherited), derived from the catalog + structural model."""
    from rdflib import RDF, Graph

    from compliance_engine.ontology.prefixes import CMMC

    catalog = Graph()
    catalog.parse(_REPO_ROOT / "data" / "ontology" / "cmmc-edit.ttl", format="turtle")
    struct = Graph()
    struct.parse(_REPO_ROOT / "data" / "structural" / "tier1.ttl", format="turtle")

    def _cid(node) -> str:
        return str(node).split("#")[-1].split("/")[-1]

    kinds: dict[str, set[str]] = {}
    for module, _p, ctrl in struct.triples((None, CMMC.controlsSatisfied, None)):
        vm = struct.value(module, CMMC.verificationMethod)
        vm_s = str(vm) if vm is not None else ""
        if vm_s.endswith("oracle-attested-reference"):
            kind = "attested"
        elif vm_s.startswith("inherited"):
            kind = "inherited"
        else:
            kind = "machine"
        kinds.setdefault(_cid(ctrl), set()).add(kind)

    def classify(cid: str) -> str:
        ks = kinds.get(cid)
        if not ks:
            return "unclaimed"
        if "attested" in ks:
            return "attested"
        if ks == {"inherited"}:
            return "inherited"
        return "machine"

    rows: list[dict] = []
    for ctrl in catalog.subjects(RDF.type, CMMC.Control):
        cid = str(catalog.value(ctrl, CMMC.controlId) or "")
        if not cid:
            continue
        text = str(catalog.value(ctrl, CMMC.text) or "")
        try:
            weight = int(str(catalog.value(ctrl, CMMC.weight) or "1"))
        except (ValueError, TypeError):
            weight = 1
        rows.append({"id": cid, "weight": weight, "kind": classify(cid), "text": text})
    rows.sort(key=lambda r: (r["id"].split(".")[0], r["id"]))
    return rows


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

_CSS = """
:root { --ink:#1a1a1a; --slate:#1f3a5f; --muted:#5b6673; --rule:#c9d1da; --stamp:#8a1f1f; }
* { box-sizing: border-box; }
html { font-size: 10.5pt; }
body { font-family: Georgia, "Times New Roman", serif; color: var(--ink);
       line-height: 1.5; margin: 0; }
h1,h2,h3 { font-family: Georgia, serif; color: var(--slate); font-weight: 600;
           line-height: 1.25; }
h1 { font-size: 22pt; margin: 0 0 .2em; }
h2 { font-size: 14pt; margin: 1.6em 0 .5em; padding-bottom: .2em;
     border-bottom: 2px solid var(--slate); }
h3 { font-size: 11.5pt; margin: 1.1em 0 .3em; }
p { margin: .5em 0; }
a { color: var(--slate); }
code, .mono { font-family: "SFMono-Regular", Menlo, Consolas, monospace; font-size: 9pt; }
.muted { color: var(--muted); }
.small { font-size: 9pt; }
table { width: 100%; border-collapse: collapse; margin: .6em 0; font-size: 9pt; }
th { text-align: left; border-bottom: 1.5px solid var(--slate); padding: 4px 8px 4px 0;
     color: var(--slate); font-weight: 600; }
td { border-bottom: .5px solid var(--rule); padding: 4px 8px 4px 0; vertical-align: top; }
tr { page-break-inside: avoid; }
.stat-row { display: flex; gap: 1.2em; margin: .8em 0; flex-wrap: wrap; }
.stat { border: .5px solid var(--rule); padding: .5em .8em; min-width: 8em; }
.stat .n { font-size: 15pt; color: var(--slate); font-weight: 600; }
.stat .l { font-size: 8pt; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }
.banner { border: 1.5px solid var(--stamp); color: var(--stamp); padding: .6em .9em;
          margin: 1em 0; font-weight: 600; }
.kv { margin: .2em 0; }
.kv b { color: var(--slate); font-weight: 600; }
.cover { height: 92vh; display: flex; flex-direction: column; justify-content: center;
         page-break-after: always; }
.cover .sub { font-size: 13pt; color: var(--muted); margin-top: .2em; }
.cover .meta { margin-top: 2.4em; }
hr.soft { border: none; border-top: .5px solid var(--rule); margin: 1.2em 0; }
"""

_PAGE_CSS = """
@page {
  size: Letter; margin: 2.2cm 2cm 2cm 2cm;
  @top-center { content: "%(header)s"; font-family: Georgia, serif; font-size: 8pt;
                color: #5b6673; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages);
                  font-family: Georgia, serif; font-size: 8pt; color: #5b6673; }
  @bottom-left { content: "%(stamp)s"; font-family: Georgia, serif; font-size: 8pt;
                 color: #8a1f1f; }
}
@page :first { @top-center { content: ""; } }
"""


def _stat(n, label) -> str:
    return f'<div class="stat"><div class="n">{_esc(n)}</div><div class="l">{_esc(label)}</div></div>'


def _cover(m: dict, sig: dict, manifest_sha: str, non_evidentiary: bool) -> str:
    banner = ""
    if non_evidentiary:
        banner = ('<div class="banner">NON-EVIDENTIARY &mdash; fixture-derived / mock '
                  'provisioning. This is a reproducible demonstration artifact, not a '
                  'submittable government package.</div>')
    return f"""
    <section class="cover">
      <h1>CMMC Level 2 Audit Package</h1>
      <div class="sub">Contract {_esc(m.get('contract'))} &middot; System Security Plan, Bill of Materials, and traceability of record</div>
      {banner}
      <div class="meta small">
        <div class="kv"><b>SPRS score:</b> {_esc(m.get('sprs',{}).get('score'))} ({_esc(m.get('sprs',{}).get('status'))}) &middot; valid submission: {_esc(m.get('sprs',{}).get('valid_submission'))}</div>
        <div class="kv"><b>BOM hash:</b> <span class="mono">{_esc(m.get('bom_hash'))}</span></div>
        <div class="kv"><b>Manifest hash:</b> <span class="mono">{_esc(manifest_sha)}</span></div>
        <div class="kv"><b>Signature:</b> {_esc(sig.get('sig_algo'))} &middot; key {_esc(sig.get('key_id'))}</div>
        <div class="kv muted">Verify the underlying package offline: <code>uv run ce verify-package --output-dir &lt;dir&gt;</code></div>
      </div>
    </section>
    """


def _summary(m: dict) -> str:
    sprs = m.get("sprs", {})
    pv = m.get("proven_vs_attested", {})
    controls = m.get("controls", [])
    met = sum(1 for c in controls if c.get("status") == "MET")
    prov = m.get("provenance", {})
    rows = "".join(_stat(x, l) for x, l in [
        (f"{sprs.get('score')} / {sprs.get('status')}", "SPRS score"),
        (str(sprs.get("valid_submission")), "Valid submission"),
        (f"{met} / {len(controls)}", "Controls met"),
        (f"{pv.get('machine', 0)} / {pv.get('human_only', 0)}", "Machine / human-only"),
        (str(len(m.get("contradictions", []))), "Contradictions"),
        ("OK" if prov.get("sop_adherence_ok") else "DEVIATION", "SOP adherence"),
    ])
    return f"""
    <h2>Executive summary</h2>
    <p>This package covers the {len(controls)} control(s) required by contract
    {_esc(m.get('contract'))}. The SPRS score is computed over that required set, weighted
    1/3/5 per control. Each control is recorded as met only where its evidence passed its
    oracle and a named human attested it in the required role.</p>
    <div class="stat-row">{rows}</div>
    """


def _integrity(m: dict, sig: dict, manifest_sha: str) -> str:
    arts = "".join(
        f"<tr><td>{_esc(a.get('name'))}</td><td class='mono'>{_esc(a.get('sha256'))}</td></tr>"
        for a in m.get("artifacts", [])
    )
    return f"""
    <h2>Integrity and verification</h2>
    <p>Every artifact is content-addressed by SHA-256; the manifest is signed. An
    assessor re-derives the record without trusting the producer: resolve each artifact
    by hash, re-hash to confirm it is unchanged, and verify the manifest signature and
    the control-to-signed-policy chain.</p>
    <div class="kv small"><b>Manifest signature:</b> {_esc(sig.get('sig_algo'))}, key {_esc(sig.get('key_id'))}</div>
    <div class="kv small"><b>Manifest hash (SHA-256):</b> <span class="mono">{_esc(manifest_sha)}</span></div>
    <p class="small">Re-verify offline: <code>uv run ce verify-package --output-dir &lt;dir&gt;</code></p>
    <h3>Bundled artifacts</h3>
    <table><thead><tr><th>Artifact</th><th>SHA-256</th></tr></thead><tbody>{arts}</tbody></table>
    """


def _provenance(m: dict) -> str:
    prov = m.get("provenance", {})
    steps = ", ".join(prov.get("executed_steps", []))
    dev = prov.get("deviations", [])
    dev_html = ("<p class='small'>Deviations: " + _esc("; ".join(dev)) + "</p>") if dev else \
               "<p class='small'>No deviations: the run followed the SOP.</p>"
    return f"""
    <h2>Provenance</h2>
    <p>The whole lineage &mdash; contract, obligations, required controls, the signed Order,
    evidence, oracle assertions, attestations, and the BOM/SSP &mdash; is recorded as a
    provenance graph and checked against the standard operating procedure.</p>
    <div class="kv small"><b>SOP adherence:</b> {'passed' if prov.get('sop_adherence_ok') else 'DEVIATION'}</div>
    <p class="small"><b>Executed steps:</b> {_esc(steps)}</p>
    {dev_html}
    """


def _matrix(m: dict) -> str:
    rows = []
    for c in m.get("controls", []):
        att = c.get("attestation", {})
        refs = ", ".join(r.get("ref", "") for r in c.get("policy_references", [])) or "—"
        rows.append(
            f"<tr><td class='mono'>{_esc(c.get('control'))}</td>"
            f"<td>{_esc(c.get('status'))}</td>"
            f"<td>{_esc(c.get('evidence_backing'))}</td>"
            f"<td>{_esc(c.get('oracle_outcome') or '—')}</td>"
            f"<td>{_esc(att.get('outcome') or '—')}</td>"
            f"<td class='small'>{_esc(refs)}</td></tr>"
        )
    return f"""
    <h2>Control traceability matrix</h2>
    <p class="small muted">Evidence backing: <b>machine</b> = sign-off backed by a passing
    oracle over resolvable evidence; <b>override</b> = MET over a failed check (requires a
    written justification and appended evidence); <b>human-only</b> = no passing machine
    measurement, rests on human judgment.</p>
    <table><thead><tr><th>Control</th><th>Status</th><th>Evidence backing</th>
    <th>Oracle</th><th>Attestation</th><th>Policy ref</th></tr></thead>
    <tbody>{''.join(rows)}</tbody></table>
    """


def _policies(m: dict) -> str:
    pol = m.get("policies", [])
    if not pol:
        return ""
    rows = "".join(
        f"<tr><td class='mono'>{_esc(p.get('ref'))}</td><td class='small'>{_esc(p.get('source'))}</td>"
        f"<td class='small'>{_esc(p.get('version') or '—')}</td>"
        f"<td class='small'>{'signed' if p.get('signature') else '—'}</td></tr>"
        for p in pol
    )
    return f"""
    <h2>Signed-policy inventory</h2>
    <p class="small">The authoritative-source references behind the attested (policy)
    controls. Each resolves to a version-pinned artifact and is verified for freshness and
    a role-appropriate signature.</p>
    <table><thead><tr><th>Reference</th><th>Source</th><th>Version</th><th>Signature</th></tr></thead>
    <tbody>{rows}</tbody></table>
    """


def _contradictions(m: dict) -> str:
    con = m.get("contradictions", [])
    if not con:
        return ("<h2>Contradictions</h2><p>None. Every human MET call agrees with its "
                "machine check, or the control had no machine check to disagree with.</p>")
    rows = "".join(
        f"<tr><td class='mono'>{_esc(c.get('control'))}</td><td>{_esc(c.get('oracle_outcome'))}</td></tr>"
        for c in con
    )
    return f"""
    <h2>Contradictions</h2>
    <div class="banner">{len(con)} control(s) attested MET over a failed machine check.
    Each must carry a written override justification and appended evidence; review them.</div>
    <table><thead><tr><th>Control</th><th>Oracle outcome</th></tr></thead><tbody>{rows}</tbody></table>
    """


def _appendix_catalog(m: dict) -> str:
    try:
        catalog = _catalog_coverage()
    except Exception:
        return ""
    in_scope = {c.get("control") for c in m.get("controls", [])}
    rows = "".join(
        f"<tr><td class='mono'>{_esc(r['id'])}</td><td>{_esc(r['weight'])}</td>"
        f"<td class='small'>{_esc(_KIND_LABEL.get(r['kind'], r['kind']))}</td>"
        f"<td>{'yes' if r['id'] in in_scope else '—'}</td>"
        f"<td class='small'>{_esc(r['text'][:80] + ('…' if len(r['text']) > 80 else ''))}</td></tr>"
        for r in catalog
    )
    n_mac = sum(1 for r in catalog if r["kind"] == "machine")
    n_att = sum(1 for r in catalog if r["kind"] == "attested")
    n_inh = sum(1 for r in catalog if r["kind"] == "inherited")
    return f"""
    <h2>Appendix A &mdash; Full control catalog (all 110)</h2>
    <p class="small">The complete NIST SP 800-171 Rev. 2 catalog and how each control is
    verified in the model: {n_mac} machine-verified, {n_att} attested-reference, {n_inh}
    CSP-inherited. "In this Order" marks the controls required by this contract and scored
    above; the rest are out of scope for this Order.</p>
    <table><thead><tr><th>Control</th><th>Wt</th><th>Verified by</th><th>In this Order</th>
    <th>Requirement</th></tr></thead><tbody>{rows}</tbody></table>
    """


def build_report_html(manifest: dict, sig: dict) -> str:
    """Render the manifest + signature into a self-contained HTML report string."""
    manifest_sha = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    weak = manifest.get("evidentiary_status") in {
        "mock", "mock-plan", "attested-reference-mock", "auto", "automatic", "semiAuto",
    }
    header = f"{manifest.get('contract', '')} · CMMC L2 Audit Package"
    stamp = "NON-EVIDENTIARY" if weak else ""
    page_css = _PAGE_CSS % {"header": _esc(header), "stamp": stamp}
    body = "".join([
        _cover(manifest, sig, manifest_sha, weak),
        _summary(manifest),
        _integrity(manifest, sig, manifest_sha),
        _provenance(manifest),
        _matrix(manifest),
        _policies(manifest),
        _contradictions(manifest),
        _appendix_catalog(manifest),
        '<hr class="soft"><p class="small muted">This report renders the signed audit-package '
        'manifest. The manifest is the source of truth; this document is a human rendering of it.</p>',
    ])
    return (f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
            f"<title>{_esc(header)}</title><style>{_CSS}{page_css}</style></head>"
            f"<body>{body}</body></html>")


# ---------------------------------------------------------------------------
# Render (HTML + PDF)
# ---------------------------------------------------------------------------

@dataclass
class ReportResult:
    html_path: Path
    pdf_path: Path | None
    pdf_engine: str | None      # "weasyprint" or None
    note: str = ""


def weasyprint_available() -> bool:
    return shutil.which("weasyprint") is not None


def render_report(package_dir: Path, *, out_dir: Path | None = None) -> ReportResult:
    """Read package/manifest.json (+ manifest.sig), write report.html, and produce
    report.pdf via the weasyprint CLI when available. Degrades to HTML-only otherwise."""
    package_dir = Path(package_dir)
    out_dir = Path(out_dir) if out_dir else package_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = package_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"no manifest.json in {package_dir}; build the package first "
            f"(uv run ce package)."
        )
    manifest = json.loads(manifest_path.read_text())
    sig_path = package_dir / "manifest.sig"
    sig = json.loads(sig_path.read_text()) if sig_path.exists() else {}

    html_str = build_report_html(manifest, sig)
    html_path = out_dir / "report.html"
    html_path.write_text(html_str, encoding="utf-8")

    if not weasyprint_available():
        return ReportResult(
            html_path=html_path, pdf_path=None, pdf_engine=None,
            note=("weasyprint not found; wrote HTML only. Install weasyprint "
                  "(https://weasyprint.org) or open report.html and print to PDF."),
        )
    pdf_path = out_dir / "report.pdf"
    try:
        subprocess.run(
            ["weasyprint", str(html_path), str(pdf_path)],
            check=True, capture_output=True, timeout=120,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        detail = getattr(exc, "stderr", b"")
        detail = detail.decode("utf-8", "replace")[:200] if isinstance(detail, bytes) else str(exc)
        return ReportResult(
            html_path=html_path, pdf_path=None, pdf_engine=None,
            note=f"weasyprint failed ({detail}); wrote HTML only.",
        )
    return ReportResult(html_path=html_path, pdf_path=pdf_path, pdf_engine="weasyprint")
