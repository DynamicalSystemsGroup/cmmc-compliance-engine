"""Compliance engine — interactive glass-walled walkthrough.

A reactive marimo dashboard that runs the real engine end-to-end and tells the
full compliance story: the contract → obligations → controls → the signed Order →
the Factory assembly line → the human attestation → the proof artifacts.

Three scenarios, four tabs, one reactive root: pick from the sidebar and watch
every cell re-execute on the real engine code. Mock fixture data, Terraform in preview only,
nothing deployed — every artifact stamped NON-EVIDENTIARY.

Run it:  uv run --group notebook marimo edit notebook/compliance_walkthrough.py
Read-only:  uv run --group notebook marimo run notebook/compliance_walkthrough.py
(from the repo root)
"""

import marimo

__generated_with = "0.23.13"
app = marimo.App(width="full")


# ═══════════════════════════════════════════════════════════════════════════════
# Imports + engine setup
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _():
    import sys as _sys
    from pathlib import Path as _Path

    try:
        _here = _Path(__file__).resolve().parent
    except NameError:
        _here = _Path.cwd()
        if _here.name != "notebook" and (_here / "notebook").is_dir():
            _here = _here / "notebook"
    for _p in (str(_here), str(_here.parent)):
        if _p not in _sys.path:
            _sys.path.insert(0, _p)

    import marimo as mo
    import _engine as engine

    return engine, mo


# ═══════════════════════════════════════════════════════════════════════════════
# Presentation helpers
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _():
    def md_table(rows, columns=None):
        """Render a list of dicts as a markdown table."""
        if not rows:
            return "_(none)_"
        _cols = columns or list(rows[0].keys())
        _head = "| " + " | ".join(_cols) + " |"
        _sep = "| " + " | ".join("---" for _ in _cols) + " |"
        _body = "\n".join(
            "| " + " | ".join(str(r.get(c, "")) for c in _cols) + " |" for r in rows
        )
        return "\n".join([_head, _sep, _body])

    def short(value, n=14):
        _s = str(value or "")
        return _s[:n] + "\u2026" if len(_s) > n else _s

    def join(items, sep=", "):
        return sep.join(str(x) for x in items) if items else "\u2014"

    return join, md_table, short


# ═══════════════════════════════════════════════════════════════════════════════
# Pipeline data cells — the reactive spine
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell
def _(engine, mo):
    scenario = mo.ui.dropdown(
        options=list(engine.SCENARIOS),
        value="all-covered",
        label="Scenario",
    )
    return (scenario,)


@app.cell
def _(engine, mo, scenario):
    ds, obligations = engine.build_dataset(scenario.value)
    return ds, obligations


@app.cell
def _(engine, obligations):
    obl_rows = engine.obligation_rows(obligations)
    required, markers = engine.required_control_set(obligations)
    return markers, obl_rows, required


@app.cell
def _(ds, engine, obligations):
    cop_att = engine.attest_cop_step(ds, obligations)
    return (cop_att,)


@app.cell
def _(ds, engine, required):
    g1 = engine.gate1_preview(required, ds)
    return (g1,)


@app.cell
def _(cop_att, ds, engine, obligations):
    order, refusal = engine.compile_order_or_refusal(ds, obligations, cop_att)
    order_ok = order is not None
    return order, order_ok, refusal


@app.cell
def _(ds, engine, mo, order, order_ok, scenario):
    if not order_ok:
        factory_ok, factory_state, outdir = False, None, None
    else:
        outdir = engine.new_output_dir()
        factory_state = engine.run_factory_step(ds, order, scenario.value, outdir)
        factory_ok = not factory_state.halted
    return factory_ok, factory_state, outdir


@app.cell
def _(ds, engine, factory_ok, factory_state, mo):
    if not factory_ok:
        attested = 0
    else:
        attested = engine.attest_step(ds, factory_state)
    return (attested,)


@app.cell
def _(ds, engine, factory_ok, mo, outdir):
    if not factory_ok:
        audit_report = None
    else:
        audit_report = engine.audit_step(ds, outdir)
    return (audit_report,)


@app.cell
def _(ds, engine, factory_ok, factory_state, mo, outdir):
    if not factory_ok:
        bom_result = None
    else:
        bom_result = engine.bom_step(factory_state, ds, outdir)
    return (bom_result,)


@app.cell
def _(audit_report, bom_result, ds, engine, factory_ok, mo, outdir):
    if not factory_ok:
        ssp_md = ""
    else:
        ssp_md = engine.ssp_step(ds, audit_report, bom_result, outdir)
    return (ssp_md,)


@app.cell
def _(bom_result, ds, engine):
    _bom = bom_result  # sequence after BOM step
    graph_counts = engine.named_graph_counts(ds)
    return (graph_counts,)


# ═══════════════════════════════════════════════════════════════════════════════
# Sidebar — scenario selector + live dashboard
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell
def _(
    attested,
    audit_report,
    factory_ok,
    g1,
    mo,
    order,
    order_ok,
    required,
    scenario,
):
    # --- Live indicator stats (update reactively) ---
    _stat_items = [
        mo.stat(
            value=str(len(required)),
            label="Controls Required",
            caption="of 110 in NIST 800-171",
            bordered=True,
        ),
        mo.stat(
            value=str(len(order.included_modules)) if order_ok else "\u2014",
            label="Modules Claimed",
            caption="cloud setup blocks",
            bordered=True,
        ),
        mo.stat(
            value="PASS" if g1.passed else "REFUSED",
            label="Gate 1",
            caption="planning coverage",
            bordered=True,
        ),
    ]

    if factory_ok and audit_report is not None:
        _s = audit_report.sprs
        _stat_items.append(
            mo.stat(
                value=f"{_s.score} / {_s.status}",
                label="SPRS Score",
                caption="valid" if _s.valid_submission else "invalid submission",
                bordered=True,
            )
        )
        _stat_items.append(
            mo.stat(
                value=str(len(audit_report.contradictions)),
                label="Contradictions",
                caption="human-over-machine flags",
                bordered=True,
            )
        )
        _stat_items.append(
            mo.stat(
                value=f"{audit_report.proven.machine_count} of {len(required)}",
                label="Machine-Proven",
                caption=f"{audit_report.proven.human_count} by human only",
                bordered=True,
            )
        )

    _sidebar = mo.sidebar(
        [
            mo.md("# Compliance Engine"),
            mo.md("*Building the secure environment and proving it's compliant are the same action.*"),
            mo.md("---"),
            scenario,
            mo.md(
                """
                **all-covered** \u2014 everything covered and signed off.
                **gap** \u2014 Gate 1 refuses; nothing is built.
                **contradiction** \u2014 human signs MET despite a failed machine check; contradiction flagged in audit.
                """
            ),
            mo.md("---"),
            mo.md("### Live Indicators"),
            mo.vstack(_stat_items, gap=0.5),
            mo.md("---"),
            mo.callout(
                mo.md(
                    "**NON-EVIDENTIARY**  \n"
                    "This is a mock run. Fixture data, mock providers, "
                    "nothing deployed. Not submittable."
                ),
                kind="warn",
            ),
            mo.md("---"),
            mo.accordion(
                {
                    "\U0001f4d6 Glossary": mo.md(
                        """
| Term | Plain meaning |
| --- | --- |
| **CMMC Level 2** | 110 security rules for DoD contractors handling CUI. |
| **Control** | One security rule (e.g. "require MFA"). |
| **COP** | Contract Obligation Profile — structured contract requirements. |
| **Order** | Signed, hash-referenced build order the Factory executes. |
| **Module** | Cloud setup piece (KMS keyring, IAM group) claiming a control. |
| **Evidence** | An artifact that *addresses* a control — never MET on its own. |
| **Oracle** | Automated check: evidence vs criterion → pass / fail / cantTell. |
| **Attestation** | Human's signed MET/NOT-MET judgment. Only this makes a control MET. |
| **Gate 1** | Planning gate — refuses if plan has uncovered controls. |
| **Gate 2** | Fulfillment gate — human attests each control MET. |
| **BOM** | Bill of Materials — machine-readable proof, content-addressed. |
| **SSP** | System Security Plan — human-readable government document. |
| **SPRS** | DoD scoreboard: 110 = clean, 88–109 = conditional, <88 = ineligible. |
| **NON-EVIDENTIARY** | Mock/practice artifact — not a real submission. |
| **False Claims Act** | Knowingly certifying false compliance = federal offense. |
| **C3PAO** | Certified Third-Party Assessment Organization — the outside auditor. |
| **SHA-256** | Cryptographic hash — a file's identity and tamper check. |
"""
                    ),
                }
            ),
        ]
    )
    return


# ═══════════════════════════════════════════════════════════════════════════════
# Tab 1: The Contract — what must be true
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell
def _(mo):
    mo.md("## \U0001f4cb The Contract  \u2014  _What must be true_")
    return


@app.cell
def _(mo):
    tab1_intro = mo.vstack(
        [
            mo.callout(
                mo.md(
                    "**The story.** The U.S. Department of Defense awards a contract "
                    "to a small business. The contract says: _\"This work handles CUI "
                    "(Controlled Unclassified Information). You must meet CMMC Level 2.\"_\n\n"
                    "That one sentence triggers **110 security rules** from NIST SP 800-171. "
                    "This demo contract \u2014 **NV012** \u2014 scopes to **22** of them for a "
                    "Tier-1 IL4 CUI enclave.\n\n"
                    "The question: **how do you prove you followed all 22 rules?** "
                    "The answer: **you don't prove it separately \u2014 building the "
                    "environment and documenting that you built it are the same action. "
                    "The environment IS the evidence; human attestation turns evidence into proof.**"
                ),
                kind="info",
            ),
            mo.mermaid(
                """
                flowchart LR
                    CONTRACT["Contract<br/>(NV012 SBIR)"] --> OBL["9 Obligations<br/>CMMC L2 · Identity · Crypto · Residency · Audit · Config · Monitor · Phys · Deliverable"]
                    OBL --> CTRL["22 Required<br/>Controls"]
                    CTRL --> COP["COP Attestation<br/>Compliance Officer signs"]
                    COP --> G1{{"GATE 1<br/>planning coverage"}}
                    G1 -->|pass| ORD["Signed Order<br/>10 modules<br/>fingerprinted"]
                    G1 -->|refuse| STOP["REFUSED<br/>names missing control"]
                    ORD --> FAC["Factory<br/>plan · evidence · oracles"]
                    FAC --> G2{{"GATE 2<br/>human attests MET"}}
                    G2 --> PROOF["BOM + SSP + SPRS<br/>the proof"]
                """
            ),
            mo.md(
                "### Where the obligations come from\n\n"
                "Every obligation is extracted from real contract text \u2014 not invented. "
                "The NV012 SBIR solicitation, its Q&A clarifications, and the DFARS clauses "
                "in the contract body are the source material. A Compliance Officer reads them, "
                "extracts the obligations, and attests: _\"Yes, these are what this contract requires.\"_"
            ),
            mo.callout(
                mo.md(
                    "**The DFARS clauses.** Every CMMC-required DoD contract includes two clauses: "
                    "**DFARS 252.204-7012** (\"_The Contractor shall implement NIST SP 800-171..._\" — "
                    "safeguarding and incident reporting) and **DFARS 252.204-7021** "
                    "(\"_Contractor Compliance with the Cybersecurity Maturity Model Certification "
                    "Level Requirement_\" — the clause that specifically mandates CMMC Level 2). "
                    "Together they are the legal hook. It's why all 110 controls matter."
                ),
                kind="neutral",
            ),
        ]
    )
    return (tab1_intro,)


@app.cell
def _(join, md_table, mo, obl_rows):
    _rows = [
        {
            "Obligation": r["obligation"],
            "Type": r["type"],
            "Marker": r["data_marker"] or "\u2014",
            "Resolves to": join(r["controls"]),
            "Note": r["note"] or "",
        }
        for r in obl_rows
    ]

    tab1_obligations = mo.vstack(
        [
            mo.md("### Step 1 \u2014 The contract's obligations"),
            mo.md(
                "Nine obligations are extracted from the NV012 contract, grouped under three "
                "top-level requirements: CMMC Level 2, US-persons identity, and US-soil data "
                "residency. Each obligation expands to the specific controls it demands. "
                "A deliverable obligation trips a spillover guard \u2014 it never resolves silently."
            ),
            mo.md(md_table(_rows)),
            mo.callout(
                mo.md(
                    "**What this means.** The nine NV012 obligations expand to **22 specific "
                    "security rules** that this Phase I demo implements. The other 88 controls "
                    "in NIST 800-171 are required by the contract (DFARS 252.204-7021 mandates "
                    "all 110) but are not yet claimed by any Tier-1 module \u2014 they are "
                    "out of scope for *this demo*, not out of scope for the contract."
                ),
                kind="info",
            ),
        ]
    )
    return (tab1_obligations,)


@app.cell
def _(mo, required):
    tab1_controls = mo.vstack(
        [
            mo.md("### Step 2 \u2014 The required control set"),
            mo.md(
                f"The 22 controls required by NV012 (of 110 in the full catalog):\n\n"
                f"`{', '.join(sorted(required))}`"
            ),
            mo.hstack(
                [
                    mo.stat(value=str(len(required)), label="Required", caption="of 110 total", bordered=True),
                    mo.stat(value="88", label="Demo scope", caption="required but not yet covered", bordered=True),
                ],
                justify="center",
                gap="2rem",
            ),
            mo.callout(
                mo.md(
                    "**Key honesty point.** The SPRS score (110 / Final) is computed over "
                    "**these 22 controls**, not all 110. \"110\" means \"all 22 required "
                    "controls are MET\" \u2014 not \"all 110 were tested.\""
                ),
                kind="warn",
            ),
        ]
    )
    return (tab1_controls,)


@app.cell
def _(mo):
    tab1_cop_sign = mo.vstack(
        [
            mo.md("### Step 3 \u2014 The Compliance Officer signs the COP"),
            mo.md(
                "Before anything is built, a human reviews the extracted obligations against "
                "the source contract and signs. This is the **only human judgment** in the "
                "Order Compiler \u2014 everything downstream is automatic."
            ),
            mo.callout(
                mo.md(
                    "**COP Attestation Screen**\n\n"
                    "> **Compliance Officer:** J. Chen  \n"
                    "> **Contract:** NV012 (SBIR Phase I)  \n"
                    "> **Date:** 2026-06-15 14:32 UTC\n\n"
                    "| Obligation | Source |\n"
                    "|---|---|\n"
                    "| CMMC Level 2 required | SBIR Topic Text \u00a7 3.2, DFARS 252.204-7012 + 252.204-7021 |\n"
                    "| US Persons only (ITAR) | Q&A Clarification #7 |\n"
                    "| US Soil data residency (ITAR) | Q&A Clarification #7 |\n\n"
                    "_\"I attest that these obligations accurately reflect the requirements "
                    "of contract NV012. I understand that under the False Claims Act "
                    "(31 U.S.C. \u00a7 3729), knowingly certifying false information to the "
                    "U.S. government is a federal offense carrying treble damages and civil "
                    "penalties of $13,946\u2013$27,894 per claim "
                    "(adjusted annually by DOJ under 28 CFR \u00a785.5; verify current rates).\"_\n\n"
                    "**[ \u2705 I ATTEST ]**  (signed)"
                ),
                kind="success",
            ),
            mo.callout(
                mo.md(
                    "**In this demo:** the Compliance Officer auto-affirms (AI-assisted draft "
                    "pre-approved). A real run requires a manual signature carrying "
                    "False-Claims-Act accountability."
                ),
                kind="info",
            ),
        ]
    )
    return (tab1_cop_sign,)


@app.cell
def _(g1, mo, required):
    _stats = mo.hstack(
        [
            mo.stat(value=g1.forward.summary(), label="Forward", caption="control \u2192 module", bordered=True),
            mo.stat(value=g1.backward.summary(), label="Backward", caption="module \u2192 control", bordered=True),
            mo.stat(value=g1.untestable.summary(), label="Testable", caption="every claim checkable", bordered=True),
        ],
        justify="center",
        gap="2rem",
    )

    if g1.passed:
        _verdict = mo.vstack(
            [
                mo.callout(
                    mo.md(
                        "**Gate 1 PASSES** \u2014 every required control is covered by a "
                        "testable module. The Order may emit."
                    ),
                    kind="success",
                ),
                mo.md(
                    "The plan covers all **22 required controls** with **10 modules** "
                    "(MFA enforcement, encryption keys, IAM groups, DLP rules, US-region "
                    "policy, audit-log export, least-functionality enforcement, "
                    "CSP-inherited physical controls, monitoring, "
                    "and baseline Terraform config). Every module traces back to a required "
                    "control, and every claim has a verification method."
                ),
            ]
        )
    else:
        _gaps = ", ".join(g1.gap_controls())
        _verdict = mo.callout(
            mo.md(
                f"**Gate 1 REFUSES** \u2014 the plan has a hole.\n\n"
                f"**Uncovered control: `{_gaps}`**\n\n"
                f"This control is required by the contract but no module claims to satisfy it. "
                f"The Order is **not emitted**. Nothing is built. You cannot proceed \u2014 "
                f"the machine would rather stop and name the problem than build something "
                f"unproven.\n\n"
                f"_Next step: add a module that satisfies `{_gaps}`, or document a scope "
                f"exclusion, then recompile._"
            ),
            kind="danger",
        )

    tab1_gate1 = mo.vstack(
        [
            mo.md("### Step 4 \u2014 Gate 1: planning coverage"),
            mo.md(
                "**Before anything is built**, the system refuses to proceed unless:  \n"
                "1. Every required control has a module claiming it (forward).  \n"
                "2. Every module traces back to a required control (backward).  \n"
                "3. Every claim has a testable verification method."
            ),
            _stats,
            _verdict,
        ]
    )
    return (tab1_gate1,)


# ═══════════════════════════════════════════════════════════════════════════════
# Tab 2: The Factory — make it true and prove it
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell
def _(mo):
    mo.md("## \U0001f3ed The Factory  \u2014  _Make it true + prove it_")
    return


@app.cell
def _(factory_ok, mo, order_ok):
    if not order_ok:
        tab2_empty = mo.callout(
            mo.md(
                "**The Factory never ran.** Gate 1 refused the Order, so nothing was built. "
                "Switch to the **all-covered** or **contradiction** scenario to see the "
                "Factory in action."
            ),
            kind="danger",
        )
    else:
        tab2_empty = mo.md("")

    tab2_header = mo.vstack(
        [
            mo.callout(
                mo.md(
                    "The **Factory** is an assembly line. It takes the signed Order and "
                    "executes 7 stages: load \u2192 fetch \u2192 plan \u2192 policy check "
                    "\u2192 mock apply \u2192 evidence collection \u2192 oracle checks. "
                    "**It never declares a control MET** \u2014 it only gathers facts and "
                    "runs automated checks. The final call belongs to a human."
                ),
                kind="info",
            ),
            tab2_empty,
        ]
    )
    return (tab2_empty, tab2_header)


@app.cell
def _(factory_ok, factory_state, join, md_table, mo, order_ok, short):
    mo.stop(not order_ok)

    _st = factory_state

    # --- Evidence table ---
    _ev_rows = [
        {
            "Evidence": short(str(e["iri"]).rsplit("/", 1)[-1]),
            "Controls addressed": join(e["controls"]),
            "Summary keys": join(list(e["summary"].keys())[:4]),
        }
        for e in _st.evidence_index
    ]

    # --- Oracle outcomes ---
    _or_rows = [
        {"Control": c, "Oracle outcome": o}
        for c, o in sorted(_st.oracles.outcomes.items())
    ]

    # --- Modules fetched ---
    _mod_rows = [
        {"Module": m, "Content hash": short(h)}
        for m, h in sorted(_st.fetch.module_hashes.items())
    ]

    _oracle_count = len(_st.oracles.outcomes)

    tab2_factory = mo.vstack(
        [
            mo.md("### The assembly line"),
            mo.mermaid(
                """
                flowchart LR
                    L["1. Load Order<br/>re-check fingerprints"] --> F["2. Fetch Modules<br/>verify by hash"]
                    F --> P["3. Terraform Plan<br/>mock providers"]
                    P --> PC["4. Policy Check<br/>US-region, etc."]
                    PC --> A["5. Mock Apply<br/>no cloud touched"]
                    A --> E["6. Collect Evidence<br/>7 artifacts"]
                    E --> O["7. Run Oracles<br/>pass / fail / cantTell"]
                """
            ),
            mo.hstack(
                [
                    mo.stat(value=len(_st.fetch.module_hashes), label="Modules fetched", bordered=True),
                    mo.stat(value=len(_st.plan.resource_ids), label="Planned resources", bordered=True),
                    mo.stat(value="PASS" if _st.policy_check.passed else "FAIL", label="Pre-apply policy", bordered=True),
                    mo.stat(value=_st.evidence.evidence_node_count, label="Evidence nodes", bordered=True),
                    mo.stat(value=_oracle_count, label="Machine oracles", bordered=True),
                ],
                justify="center",
                gap="1.5rem",
            ),
            mo.callout(
                mo.md(
                    "**Terraform runs in preview only, with mock providers.** No cloud is "
                    "contacted. No credentials are used. Nothing is deployed. You get a "
                    "genuine, detailed preview of what *would* be built \u2014 without "
                    "building anything."
                ),
                kind="warn",
            ),
            mo.accordion(
                {
                    "Evidence artifacts (each addresses \u22651 control)": mo.md(md_table(_ev_rows)),
                    "Oracle outcomes (pass / fail / cantTell)": mo.md(md_table(_or_rows)),
                    "Modules fetched by content hash": mo.md(md_table(_mod_rows)),
                }
            ),
            mo.callout(
                mo.md(
                    f"**{_oracle_count}** oracle checks run: IAM access control "
                    f"(AC.L2-3.1.1), MFA enforcement (IA.L2-3.5.3), FIPS-validated "
                    f"crypto (SC.L2-3.13.11), CUI encryption at rest (SC.L2-3.13.16), "
                    f"US-region policy (SC.L2-3.13.1, returns cantTell), and ITAR "
                    f"US-persons check. The remaining required controls have "
                    f"**no machine test** \u2014 the oracle honestly returns **cantTell** "
                    f"rather than faking a check it can't run. Those controls are for a "
                    f"human to judge."
                ),
                kind="info",
            ),
        ]
    )
    return (tab2_factory,)


@app.cell
def _(attested, factory_ok, mo, order_ok, required):
    mo.stop(not order_ok)

    tab2_attest = mo.vstack(
        [
            mo.md("### The human signs \u2014 Gate 2"),
            mo.md(
                "A machine can gather evidence and run checks, but it can **never** declare "
                "a control satisfied. Only the **Affirming Official** does that \u2014 and "
                "they carry the legal accountability."
            ),
            mo.callout(
                mo.md(
                    "**Control Attestation Screen**  \n\n"
                    "> **Affirming Official:** M. Rivera  \n"
                    "> **Control:** IA.L2-3.5.3 \u2014 _\"Use multi-factor authentication "
                    "for local and network access to privileged accounts.\"_  \n"
                    "> **Evidence:** MFA config export (hash: `4bba2d0a...`), Oracle: **passed**\n\n"
                    "**Adequacy justification:** _\"Google Workspace 2-Step Verification "
                    "enforced on the CUI users group. Hardware security keys required for "
                    "privileged accounts.\"_\n\n"
                    "**Sufficiency justification:** _\"MFA config export shows enforcement "
                    "policy is active. Oracle confirms mfa_enforced_privileged = true.\"_\n\n"
                    "---\n\n"
                    "_\"I certify that control IA.L2-3.5.3 is MET. I understand that under "
                    "the False Claims Act (31 U.S.C. \u00a7 3729), knowingly certifying false "
                    "information to the U.S. government is a federal offense.\"_\n\n"
                    "**[ \u2705 I CERTIFY THIS CONTROL IS MET ]**  (signed, 2026-06-15 14:45 UTC)"
                ),
                kind="success",
            ),
            mo.callout(
                mo.md(
                    "**What happens when oracle says FAIL but the human signs MET anyway?**  \n"
                    "A third field appears: **Override Justification** (required). The human "
                    "must explain: _\"The oracle checks X, but we satisfy the control a "
                    "different way, documented here.\"_ If this field is left blank, the "
                    "system **flags a contradiction** in the audit \u2014 even if the score "
                    "is 110 / Final."
                ),
                kind="warn",
            ),
            mo.callout(
                mo.md(
                    f"**{attested} of {len(required)} controls attested MET** by the NV012 "
                    f"Affirming Official \u2014 each with a written adequacy + sufficiency "
                    f"rationale. Machine-checked controls carry their real oracle outcome. "
                    f"A MET-over-failed-check without written justification becomes a "
                    f"visible contradiction in the audit."
                ),
                kind="success",
            ),
            mo.callout(
                mo.md(
                    "### \u26a0\ufe0f The False Claims Act\n\n"
                    "**31 U.S.C. \u00a7 3729.** Knowingly submitting a false claim to the U.S. "
                    "government carries:\n"
                    "- **Treble damages** (3x the government's loss)\n"
                    "- **$13,946\u2013$27,894** civil penalty **per false claim** "
                    "(adjusted annually by DOJ under 28 CFR \u00a785.5)\n\n"
                    "An SPRS submission is **one** claim to the government. Each control "
                    "you falsely attest MET is evidence of that claim's falsity \u2014 and "
                    "every MET that can't be substantiated compounds your exposure. "
                    "**A single dishonest submission isn't a slap on the wrist \u2014 it's "
                    "potential bankruptcy and prison.** This is why the system refuses to let "
                    "a machine sign. Only a human, with their name and accountability on the "
                    "line, can mark a control MET."
                ),
                kind="danger",
            ),
        ]
    )
    return (tab2_attest,)


# ═══════════════════════════════════════════════════════════════════════════════
# Tab 3: The Proof — here's what we can show
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell
def _(mo):
    mo.md("## \U0001f512 The Proof  \u2014  _Here's what we can show_")
    return


@app.cell
def _(audit_report, factory_ok, mo, order_ok):
    mo.stop(not order_ok)

    if not factory_ok or audit_report is None:
        tab3_header = mo.callout(
            mo.md("_The Factory halted before producing proof artifacts._"),
            kind="danger",
        )
    else:
        tab3_header = mo.md("")

    tab3_intro = mo.vstack(
        [
            mo.callout(
                mo.md(
                    "**Four outputs, one chain.** The Factory produces an **audit** "
                    "(is the paper trail unbroken?), an **SPRS score** (the DoD scoreboard), "
                    "a content-addressed **BOM** (the tamper-evident proof file), and a "
                    "byte-stable **SSP** (the human-readable government document). All four "
                    "are compiled from the same RDF knowledge graph \u2014 they can't "
                    "disagree. And because every artifact is content-addressed by SHA-256, "
                    "an auditor can **re-verify everything without trusting you.**"
                ),
                kind="info",
            ),
            tab3_header,
        ]
    )
    return (tab3_header, tab3_intro)


@app.cell
def _(audit_report, factory_ok, md_table, mo, order_ok):
    mo.stop(not order_ok or not factory_ok)

    _sprs = audit_report.sprs
    _con = audit_report.contradictions

    # --- SPRS score dashboard ---
    _score_color = "success" if _sprs.score >= 110 else ("warn" if _sprs.score >= 88 else "danger")

    _sprs_stats = mo.hstack(
        [
            mo.stat(
                value=str(_sprs.score),
                label="SPRS Score",
                caption=_sprs.status,
                bordered=True,
            ),
            mo.stat(
                value=str(_sprs.valid_submission),
                label="Valid Submission",
                caption="POA&M rules satisfied",
                bordered=True,
            ),
            mo.stat(
                value=str(audit_report.proven.machine_count),
                label="Machine-Proven",
                caption="oracle passed + human attested",
                bordered=True,
            ),
            mo.stat(
                value=str(audit_report.proven.human_count),
                label="Human-Attested Only",
                caption="no machine check available",
                bordered=True,
            ),
            mo.stat(
                value=str(len(_con)),
                label="Contradictions",
                caption="MET over failed oracle",
                bordered=True,
            ),
        ],
        justify="center",
        gap="1.5rem",
    )

    # --- Proven-vs-attested visual ---
    _machine = audit_report.proven.machine_count
    _human = audit_report.proven.human_count
    _total = _machine + _human
    _bar_width = 40
    _machine_bar = int(_machine / _total * _bar_width) if _total else 0
    _bar = "\u2588" * _machine_bar + "\u2591" * (_bar_width - _machine_bar)

    _proven_viz = mo.md(
        f"### Proven vs. Attested\n\n"
        f"`{_bar}`\n\n"
        f"**{_machine}** machine-proven (oracle passed + human attested)  \n"
        f"**{_human}** human-attested only (documentary, inherited, or no oracle)\n\n"
        f"_Most \"MET\"s in a real assessment are human-judged, not machine-proven. "
        f"The system doesn't blur this \u2014 it counts and prints the split._"
    )

    # --- Contradiction flag ---
    if _con:
        _con_rows = [
            {"Control": c.control, "Oracle": c.oracle_outcome, "Override?": str(c.has_override)}
            for c in _con
        ]
        _con_flag = mo.callout(
            mo.md(
                "### \u26a0\ufe0f CONTRADICTION FLAGGED\n\n"
                "A human attested MET while the machine oracle **failed**, with no written "
                "override justification. The score does **not** silently absorb this \u2014 "
                "a 110 here is **not clean**.\n\n"
                + md_table(_con_rows)
            ),
            kind="danger",
        )
    else:
        _con_flag = mo.callout(
            mo.md("**No contradictions.** Every human MET call agrees with (or has no) machine check."),
            kind="success",
        )

    tab3_audit = mo.vstack(
        [
            mo.md("### The Audit + SPRS Score"),
            _sprs_stats,
            _proven_viz,
            _con_flag,
            mo.callout(
                mo.md(
                    "**Score key:** 110 = Final (all required controls MET). 88\u2013109 = "
                    "Conditional (POA&M fix-it plan allowed for 1-point controls only). "
                    "Below 88 = Ineligible.  \n"
                    "**POA&M legality:** Only 1-point controls may be deferred. Putting a "
                    "3- or 5-point control (or one of six excluded 1-pointers) on a POA&M "
                    "makes the submission automatically invalid \u2014 regardless of the score."
                ),
                kind="info",
            ),
        ]
    )
    return (tab3_audit,)


@app.cell
def _(bom_result, factory_ok, md_table, mo, order_ok, short):
    mo.stop(not order_ok or not factory_ok)

    _map = [
        {
            "Control": r.control_id,
            "Status": r.status,
            "Oracle": r.oracle_outcome or "\u2014",
            "Attestation": r.attestation_outcome or "\u2014",
            "# Evidence": str(len(r.evidence_hashes)),
        }
        for r in bom_result.control_mapping
    ]

    tab3_bom = mo.vstack(
        [
            mo.md("### The BOM \u2014 Bill of Materials"),
            mo.hstack(
                [
                    mo.stat(value=short(bom_result.bom_hash), label="BOM hash", bordered=True),
                    mo.stat(value=bom_result.evidentiary_status, label="Evidentiary status", bordered=True),
                    mo.stat(value=str(len(bom_result.control_mapping)), label="Controls mapped", bordered=True),
                ],
                justify="center",
                gap="2rem",
            ),
            mo.callout(
                mo.md(
                    "The **BOM** (`bom.json`) is the machine-readable proof file. For each "
                    "required control it records: resource \u2192 evidence hash \u2192 oracle "
                    "outcome \u2192 attestation outcome \u2192 status \u2192 who signed. "
                    "It is stored **write-once** under its own SHA-256 hash in a "
                    "content-addressed registry \u2014 change one byte and the address no "
                    "longer matches. Tampering is instantly detectable."
                ),
                kind="info",
            ),
            mo.callout(
                mo.md(
                    f"**Evidentiary status: `{bom_result.evidentiary_status}`.** The BOM "
                    f"inherits the weakest mark from its inputs. Because this run uses "
                    f"fixture-backed (mock) evidence, the entire BOM is stamped **mock** "
                    f"\u2014 not submittable. You cannot launder pretend evidence into a "
                    f"real-looking BOM."
                ),
                kind="warn",
            ),
            mo.accordion(
                {"Control mapping (control \u2192 status \u2192 evidence)": mo.md(md_table(_map))}
            ),
        ]
    )
    return (tab3_bom,)


@app.cell
def _(factory_ok, mo, order_ok, ssp_md):
    mo.stop(not order_ok or not factory_ok)

    _banner = "NON-EVIDENTIARY" in ssp_md
    _head = "\n".join(ssp_md.splitlines()[:30])

    tab3_ssp = mo.vstack(
        [
            mo.md("### The SSP \u2014 System Security Plan"),
            mo.callout(
                mo.md(
                    "The **SSP** (`ssp.md`) is the human-readable government document. Its "
                    "centerpiece is the **110-row traceability matrix** (VCRM) \u2014 one row "
                    "per NIST 800-171 control, listing implementation, responsible party, "
                    "evidence hash, status, and POA&M reference.\n\n"
                    "It is **not hand-written.** It's compiled deterministically from the "
                    "same RDF graph as the BOM, so it can't disagree with the data. Identical "
                    "inputs produce a byte-for-byte identical document. And it **structurally "
                    "cannot omit** its NON-EVIDENTIARY banner when mock evidence is present."
                ),
                kind="info",
            ),
            mo.callout(
                mo.md(
                    f"NON-EVIDENTIARY banner present: **{_banner}**. There is no switch to "
                    f"turn it off."
                ),
                kind="warn" if _banner else "danger",
            ),
            mo.accordion(
                {"SSP preview (first 30 lines)": mo.md("```\n" + _head + "\n```")}
            ),
        ]
    )
    return (tab3_ssp,)


@app.cell
def _(audit_report, bom_result, factory_ok, mo, order_ok, short):
    mo.stop(not order_ok or not factory_ok)

    tab3_auditor = mo.vstack(
        [
            mo.md("### The Auditor's View \u2014 Proof by Reproduction"),
            mo.md(
                "The core claim: **an auditor doesn't have to trust you.** A C3PAO assessor "
                "receives the BOM and can re-verify everything independently."
            ),
            mo.callout(
                mo.md(
                    "**C3PAO Re-Verification Screen**\n\n"
                    "```\n"
                    "$ uv run python cli.py verify --output-dir output/\n\n"
                    "Re-hashing all evidence nodes in the audit dataset...\n"
                    "  Checking SHACL shapes for attestation completeness...\n\n"
                    "Dataset intact. No tampering detected. SHACL shapes conform.\n"
                    "```\n\n"
                    "The `verify` subcommand re-hashes every evidence node stored in the "
                    "RDF dataset and checks that content hashes still match \u2014 then runs "
                    "the SHACL attestation suite. Any altered byte in any evidence node "
                    "causes a mismatch and exits with code 1.\n\n"
                    "_Time elapsed: 3 seconds. Manual equivalent: ~2 weeks of inspection._"
                ),
                kind="success",
            ),
            mo.callout(
                mo.md(
                    "**What if someone tampered with the BOM?**\n\n"
                    "```\n"
                    "BOM hash:  4483673449ac...\n"
                    "Recomputed: a1b2c3d4e5f6...\n\n"
                    "TAMPERING DETECTED.\n"
                    "This BOM has been altered since it was signed.\n"
                    "```\n\n"
                    "Change one byte \u2014 even a single character in a justification text "
                    "\u2014 and the SHA-256 hash changes completely. The math catches it "
                    "instantly. **The fingerprint IS the proof of integrity.**"
                ),
                kind="danger",
            ),
            mo.callout(
                mo.md(
                    "### Why this beats a folder of screenshots\n\n"
                    "**The old way:** a compliance officer takes screenshots of admin console "
                    "settings, pastes them into a Word document, assembles a 3-ring binder. "
                    "It's slow, error-prone, and goes stale the moment someone changes a "
                    "setting. An auditor has to trust that the screenshots are real and "
                    "current.\n\n"
                    "**This system:** the environment is built from a signed plan. The act of "
                    "building it IS the proof. Every artifact is content-addressed. The "
                    "auditor doesn't trust you \u2014 they trust the math. They re-run the "
                    "same checks, re-compute the same hashes, and the fingerprints either "
                    "match or they don't."
                ),
                kind="info",
            ),
        ]
    )
    return (tab3_auditor,)


@app.cell
def _(factory_ok, graph_counts, md_table, mo, order_ok):
    mo.stop(not order_ok)

    _rows = [
        {"Named Graph": f"<ce:{r['layer']}>", "Triples": str(r["triples"])}
        for r in graph_counts
    ]

    tab3_substrate = mo.vstack(
        [
            mo.md("### The Substrate \u2014 One queryable knowledge graph"),
            mo.md(
                "Every stage writes its own **named graph** into one RDF dataset \u2014 "
                "controls, the Order, evidence, attestations, the audit \u2014 all separated "
                "but queryable together. This is what makes the whole chain re-executable "
                "and tamper-evident."
            ),
            mo.md(md_table(_rows)),
            mo.callout(
                mo.md(
                    "### The timeline\n\n"
                    "```\n"
                    "Contract Award \u2500\u2500\u25b6 COP Signing \u2500\u2500\u25b6 Environment Build \u2500\u2500\u25b6 Assessment \u2500\u2500\u25b6 Delivery\n"
                    "                      \u2191                  \u2191                   \u2191\n"
                    "                 Compliance            Factory               C3PAO\n"
                    "                 Officer               runs here             verifies\n"
                    "                 signs here\n"
                    "```\n\n"
                    "**Roles:**  \n"
                    "- **Compliance Officer** \u2014 reads the contract, extracts obligations, signs the COP.  \n"
                    "- **Order Compiler** (machine) \u2014 obligations \u2192 controls \u2192 modules, runs Gate 1.  \n"
                    "- **Factory** (machine) \u2014 executes the Order, gathers evidence, runs oracles.  \n"
                    "- **Affirming Official** (human) \u2014 signs each control MET, carries legal accountability.  \n"
                    "- **C3PAO Assessor** (human) \u2014 re-verifies the BOM by hash, re-runs checks."
                ),
                kind="neutral",
            ),
        ]
    )
    return (tab3_substrate,)


# ═══════════════════════════════════════════════════════════════════════════════
# Tab 4: Coverage — what the engine handles vs. what's on you
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(engine):
    coverage = engine.get_coverage_data()
    cov_families = ["All"] + sorted({r["family"] for r in coverage})
    return coverage, cov_families


@app.cell(hide_code=True)
def _(cov_families, mo):
    cov_family = mo.ui.dropdown(options=cov_families, value="All", label="Family")
    cov_status = mo.ui.dropdown(
        options=["All", "covered", "machine", "human"],
        value="All",
        label="Status",
    )
    return cov_family, cov_status


@app.cell(hide_code=True)
def _(coverage, cov_family, cov_status, md_table, mo):
    _STATUS_LABEL = {
        "covered": "✅ Covered",
        "machine": "🔧 Machine-possible",
        "human":   "📋 Human-only",
    }
    _WHO_LABEL = {
        "covered": "engine",
        "machine": "wire it",
        "human":   "you",
    }

    _filtered = [
        r for r in coverage
        if (cov_family.value == "All" or r["family"] == cov_family.value)
        and (cov_status.value == "All" or r["status"] == cov_status.value)
    ]

    _n_cov = sum(1 for r in coverage if r["status"] == "covered")
    _n_mac = sum(1 for r in coverage if r["status"] == "machine")
    _n_hum = sum(1 for r in coverage if r["status"] == "human")

    _table_rows = [
        {
            "Control": r["id"],
            "Wt": str(r["weight"]),
            "Status": _STATUS_LABEL[r["status"]],
            "Handled by": _WHO_LABEL[r["status"]],
            "No POA&M": "yes" if r["non_deferrable"] else "",
            "CSP": "inherited" if r["inherited"] else "",
            "Requirement": (r["text"][:110] + "…") if len(r["text"]) > 110 else r["text"],
        }
        for r in _filtered
    ]

    # Per-family summary scorecard (all 110, ignores filter)
    _families_order = ["AC", "AT", "AU", "CA", "CM", "IA", "IR", "MA", "MP", "PE", "PS", "RA", "SC", "SI"]
    _scorecard_rows = []
    for _fam in _families_order:
        _fc = [r for r in coverage if r["family"] == _fam]
        _scorecard_rows.append({
            "Family": _fam,
            "Total": str(len(_fc)),
            "✅ Covered": str(sum(1 for r in _fc if r["status"] == "covered")),
            "🔧 Wire it": str(sum(1 for r in _fc if r["status"] == "machine")),
            "📋 You": str(sum(1 for r in _fc if r["status"] == "human")),
            "Max pts at risk": str(sum(r["weight"] for r in _fc if r["status"] != "covered")),
        })

    tab4_coverage = mo.vstack(
        [
            mo.callout(
                mo.md(
                    "**Three categories across all 110 CMMC Level 2 controls.**\n\n"
                    "✅ **Covered** — the engine checks this today: Terraform config, "
                    "oracle criteria, and attestation are all wired.\n\n"
                    "🔧 **Machine-possible** — no evidence generator yet, but a GCP / "
                    "Workspace / GitHub / EDR API call could verify this automatically. "
                    "See `docs/plans/2026-07-03-002-path-to-self-assessment.md` Track A.\n\n"
                    "📋 **Human-only** — policy, training record, physical inspection, or "
                    "signed procedure. The oracle always returns **cantTell**. On you."
                ),
                kind="info",
            ),
            mo.callout(
                mo.md(
                    "**Column guide:**  \n"
                    "**Wt** — SPRS points deducted if NOT MET (`110 − Σ weight` = your score).  \n"
                    "**No POA&M** — if \"yes\", this control cannot be deferred. NOT MET at "
                    "submission makes the entire filing invalid regardless of score. Applies "
                    "to all 5-pt and 3-pt controls, plus six specific 1-pt controls.  \n"
                    "**CSP** — \"inherited\" means Google IL4 handles this physically; you "
                    "attest it as inherited rather than self-implementing.  \n"
                    "**Handled by** — \"engine\" = automated today; \"wire it\" = add an "
                    "evidence generator; \"you\" = write the policy or procedure."
                ),
                kind="neutral",
            ),
            mo.hstack(
                [
                    mo.stat(value=str(_n_cov), label="✅ Covered", caption="engine checks today", bordered=True),
                    mo.stat(value=str(_n_mac), label="🔧 Wire it", caption="add evidence generators", bordered=True),
                    mo.stat(value=str(_n_hum), label="📋 On you", caption="policy & procedure", bordered=True),
                ],
                justify="center",
                gap="1.5rem",
            ),
            mo.hstack([cov_family, cov_status], gap="2rem"),
            mo.md(f"**{len(_filtered)} of 110 controls** shown"),
            mo.md(md_table(
                _table_rows,
                columns=["Control", "Wt", "Status", "Handled by", "No POA&M", "CSP", "Requirement"],
            )),
            mo.md("### Summary by family"),
            mo.md(md_table(
                _scorecard_rows,
                columns=["Family", "Total", "✅ Covered", "🔧 Wire it", "📋 You", "Max pts at risk"],
            )),
            mo.callout(
                mo.md(
                    "**Max pts at risk** = total SPRS weight across all uncovered controls "
                    "in that family. Getting to 110/Final means driving this to zero across "
                    "every family — by wiring evidence generators (Track A) and completing "
                    "the human attestation program (Track B)."
                ),
                kind="neutral",
            ),
        ],
        gap=1.5,
    )
    return (tab4_coverage,)


# ═══════════════════════════════════════════════════════════════════════════════
# Assemble the four tabs
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell
def _(
    mo,
    tab1_controls,
    tab1_cop_sign,
    tab1_gate1,
    tab1_intro,
    tab1_obligations,
    tab2_attest,
    tab2_factory,
    tab2_header,
    tab3_audit,
    tab3_auditor,
    tab3_bom,
    tab3_intro,
    tab3_ssp,
    tab3_substrate,
    tab4_coverage,
):
    mo.ui.tabs(
        {
            "\U0001f4cb The Contract": mo.vstack(
                [
                    tab1_intro,
                    tab1_obligations,
                    tab1_controls,
                    tab1_cop_sign,
                    tab1_gate1,
                ],
                gap=1.5,
            ),
            "\U0001f3ed The Factory": mo.vstack(
                [
                    tab2_header,
                    tab2_factory,
                    tab2_attest,
                ],
                gap=1.5,
            ),
            "\U0001f512 The Proof": mo.vstack(
                [
                    tab3_intro,
                    tab3_audit,
                    tab3_bom,
                    tab3_ssp,
                    tab3_auditor,
                    tab3_substrate,
                ],
                gap=1.5,
            ),
            "\U0001f4ca Coverage": tab4_coverage,
        }
    )
    return


# ═══════════════════════════════════════════════════════════════════════════════
# Footer — honesty panel
# ═══════════════════════════════════════════════════════════════════════════════

@app.cell
def _(mo):
    mo.callout(
        mo.md(
            """
            ### What's real vs. mock right now

            This is **Phase I**. The software spine is fully wired end to end, but:

            - **Evidence is fixture-backed**, not pulled from a live cloud → every artifact
              is `mock` and every BOM/SSP is **NON-EVIDENTIARY** (not submittable).
            - **Terraform runs in preview only, with mock providers** — nothing is deployed,
              no credentials.
            - **Only 6 oracle checks run** (4 CMMC controls pass; 1 returns cantTell; 1 is an
              ITAR policy-marker check); the rest ride on human attestation.
              The SPRS score covers only the **22 required** for this Phase I demo — the other
              **88** are required by the contract but not yet covered by any Tier-1 module.
            - **Deferred:** cryptographic signing (Sigstore), live `terraform apply` + live
              compliance tests, IL5, and actual SPRS/PIEE submission.

            None of this is hidden — the banner, the `mock` stamp, and the machine-vs-human
            split are all there to keep the demo honest. The *mechanism* is fully wired;
            only the evidence is stand-in.
            """
        ),
        kind="neutral",
    )
    return


if __name__ == "__main__":
    app.run()
