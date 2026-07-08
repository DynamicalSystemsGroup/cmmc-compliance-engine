Here is the complete redesign skeleton.

---

Compliance Walkthrough — Redesign Plan

The core problem, stated plainly

The ADCS notebook IS the computation. Every cell is a visible step: sym_result = run_symbolic_analysis(params) → table of derived values → matplotlib figure with a requirement limit line. The reader sees mechanism.

Our notebook NARRATES computation. engine.run_factory_step(...) runs inside a hide_code=True cell and returns an opaque object. Every display cell is a layer of prose over a black box.

One rule for the rewrite: if a cell produces data, its code must be visible. hide_code=True is only for pure layout assembly cells.

---

What changes structurally

A. hide_code=True removed from all 8 spine cells:

- engine.build_dataset(scenario.value)
- engine.obligation_rows() / engine.required_control_set()
- engine.attest_cop_step()
- engine.gate1_preview()
- engine.compile_order_or_refusal()
- engine.run_factory_step() — the most important one
- engine.audit_step()
- engine.bom_step() / engine.ssp_step()

B. 4 matplotlib figures added (calling _viz.py which currently goes uncalled):

- Station 6: oracle_outcomes_chart(factory_state.oracles.outcomes)
- Station 9: sprs_gauge(audit_report.sprs.score, audit_report.sprs.status)
- Station 11: traceability_graph(required, oracle_outcomes, included_modules, contradictions)
- Station 12: coverage_family_chart(coverage)

C. Scenario picker moves above the prologue — the arc is the point, not an afterthought in the sidebar.

D. explain_control reformatted as a tree, not a flat string.

---

Section-by-section skeleton

────────────────────────────────────────────────────────────────
HEADER [REWRITE]
────────────────────────────────────────────────────────────────

# One contract, followed end to end

[scenario dropdown — here, at the top, before anything else]

"Pick `gap`: Gate 1 refuses. Nothing is built.
Pick `contradiction`: a human signs MET over a failed check.
Pick `all-covered`: the full chain proves out.

The arc is the point. Change the scenario — everything below
re-executes on the real engine."

────────────────────────────────────────────────────────────────
PROLOGUE [KEEP + 1 LINE]
────────────────────────────────────────────────────────────────
• Accordion: Why RDF / Why EARL / Why SHACL (keep)
• 8-graph table (keep)
• [ADD] one live line: "This run produced {N} total triples
across {8} named graphs." — pulled from graph_counts

────────────────────────────────────────────────────────────────
REACTIVE SPINE (lines 116–196) [EXPOSE CODE]
────────────────────────────────────────────────────────────────
Remove hide_code=True from every data-producing cell.
The reader should be able to see:

@app.cell
def _(engine, scenario):
ds, obligations = engine.build_dataset(scenario.value)
return ds, obligations

@app.cell
def _(ds, engine, order, order_ok, scenario):
if not order_ok:
factory_ok, factory_state, outdir = False, None, None
else:
outdir = engine.new_output_dir()
factory_state = engine.run_factory_step(
ds, order, scenario.value, outdir
)
factory_ok = not factory_state.halted
return factory_ok, factory_state, outdir

That IS the documentation. The function name tells you where to look.

────────────────────────────────────────────────────────────────
SIDEBAR [TRIM]
────────────────────────────────────────────────────────────────
• Remove the "where the artifact is" rail — it duplicates the
stations. Replace with a single bold SPRS badge:
SPRS 110 · Final (green)
SPRS — · REFUSED (red)
• Keep scenario picker + live indicators
• Keep NON-EVIDENTIARY callout

────────────────────────────────────────────────────────────────
STATION 0 — THE WHOLE PICTURE [KEEP]
────────────────────────────────────────────────────────────────
Mermaid flowchart + "two ideas" callout + honest limits.
No changes.

────────────────────────────────────────────────────────────────
STATION 1 — THE CONTRACT [KEEP]
────────────────────────────────────────────────────────────────
Obligations table. No changes.

────────────────────────────────────────────────────────────────
STATION 2 — OBLIGATIONS → CONTROLS [MINOR]
────────────────────────────────────────────────────────────────
• Add one visible line showing the resolution call:
required, markers = engine.required_control_set(obligations)
• Keep the required-controls list + scope warning.

────────────────────────────────────────────────────────────────
STATION 3 — COP SIGNED [KEEP]
────────────────────────────────────────────────────────────────
No changes.

────────────────────────────────────────────────────────────────
STATION 4 — GATE 1 [IMPROVE]
────────────────────────────────────────────────────────────────
For gap scenario — make the refusal dramatic, not just a callout:

"Gate 1 REFUSES. The plan has a hole.

Uncovered control: AC.L2-3.1.22

This control is required by the Order but no module claims it.
The assembly line stops HERE. Nothing is built. Nothing is
proven. Switch to all-covered or contradiction to see the
line run."

For all-covered — show all three gate dimensions as green stats,
then a clean PASS verdict.

────────────────────────────────────────────────────────────────
STATION 5 — THE SIGNED ORDER [KEEP]
────────────────────────────────────────────────────────────────
Hash + modules. No changes.

────────────────────────────────────────────────────────────────
STATION 6 — THE RUNTIME [ADD FIGURE]
────────────────────────────────────────────────────────────────
BEFORE the accordion of tables, add:

@app.cell ← code visible
def _(factory_ok, factory_state):
import _viz
fig = None
if factory_ok:
fig = _viz.oracle_outcomes_chart(
factory_state.oracles.outcomes
)
return (fig,)

@app.cell(hide_code=True) ← layout only
def _(fig, mo):
mo.vstack([
mo.md("### Oracle outcomes — what the machine found"),
mo.as_html(fig) if fig else mo.md("_(run a passing scenario)_"),
])

Colors: passed=green, failed=red, cantTell=amber, needsAction=orange.
This figure IS the station. The bars show you the split without reading
a table. The existing accordion (evidence, oracle table, module hashes)
becomes collapsible detail below it.

────────────────────────────────────────────────────────────────
STATION 7 — ATTESTED-REFERENCE MODEL [KEEP]
────────────────────────────────────────────────────────────────
No changes.

────────────────────────────────────────────────────────────────
STATION 8 — GATE 2 / HUMAN ATTESTS MET [TREE FORMAT]
────────────────────────────────────────────────────────────────
The per-control BOM table stays. Add colored row logic:
machine → green left-border
human → amber left-border
override → red left-border (contradiction)

The contradiction block is already good — keep it.

────────────────────────────────────────────────────────────────
STATION 8b — CONTROL INTERROGATION [REFORMAT]
────────────────────────────────────────────────────────────────
Replace the flat string with a tree, exactly like ADCS:

AC.L2-3.1.1 — Limit system access to authorized users
├── Oracle outcome: passed
├── Attestation: MET (machine-proven)
├── SPRS weight: 5 (non-deferrable — cannot be POA&M'd)
├── Evidence (2 artifacts):
│ ├── hash: abcd1234... addresses: AC.L2-3.1.1, AC.L2-3.1.2
│ └── hash: ef567890... addresses: AC.L2-3.1.1
└── Backing: machine

This goes into _interrogate.explain_control() — rewrite it to
return this format instead of the current flat dump.

────────────────────────────────────────────────────────────────
STATION 9 — PROOF OUTPUTS [ADD FIGURE]
────────────────────────────────────────────────────────────────
Lead with the gauge, not the stat boxes:

@app.cell
def _(audit_report, factory_ok):
import _viz
fig = None
if factory_ok and audit_report:
fig = _viz.sprs_gauge(
audit_report.sprs.score,
audit_report.sprs.status
)
return (fig,)

Below the gauge: show the arithmetic explicitly:

"SPRS = 110 − 5 (AC.L2-3.1.1) − 3 (IA.L2-3.5.3) − ... = 78"

Not just the number. The subtraction IS the story.
Then stat boxes, then BOM/SSP accordion.

────────────────────────────────────────────────────────────────
STATION 9b — PER-CONTROL SPRS BREAKDOWN [KEEP]
────────────────────────────────────────────────────────────────
Already added. No changes.

────────────────────────────────────────────────────────────────
STATION 10 — PROOF BY REPRODUCTION [KEEP]
────────────────────────────────────────────────────────────────
No changes.

────────────────────────────────────────────────────────────────
STATION 10b — HASH CHAIN DEMO [KEEP]
────────────────────────────────────────────────────────────────
Bug already fixed. No changes.

────────────────────────────────────────────────────────────────
STATION 11 — THE SUBSTRATE [ADD FIGURE]
────────────────────────────────────────────────────────────────
The graph is the centerpiece here — add it:

@app.cell
def _(factory_ok, factory_state, audit_report, order, required):
import _viz
fig = None
if factory_ok and audit_report:
fig = _viz.traceability_graph(
required,
factory_state.oracles.outcomes,
order.included_modules,
audit_report.contradictions,
)
return (fig,)

Order(blue) → Module(purple) → Control(green/red by outcome)
Contradiction halos in orange.
Triple counts table stays below as collapsible detail.

────────────────────────────────────────────────────────────────
STATION 12 — FULL 110 CONTROLS [ADD FIGURE]
────────────────────────────────────────────────────────────────
Lead with the stacked bar chart before the filterable table:

@app.cell
def _(coverage):
import _viz
fig = _viz.coverage_family_chart(coverage)
return (fig,)

14 families × 3 verification kinds (machine/attested/inherited).
The chart shows the structural coverage at a glance.
Filterable table stays below for drill-down.

────────────────────────────────────────────────────────────────
ASSEMBLY CELL [UPDATE]
────────────────────────────────────────────────────────────────
Add the 4 new figure cells to the vstack.
Order:
header → prologue → s1 → s2 → s3 → s4 → s5
→ s6 + oracle_fig → s7 → s8 → s8b → s9 + sprs_fig
→ s9_breakdown → s10 → s10b → s11 + graph_fig
→ s12 + coverage_fig → footer

---

What this still won't have (honest)

- v1→v2 design iteration arc — we don't have two structural model versions, so the "model hash invalidates, re-d ADCS doesn't exist here. The closest equivalent is switching gap→all-covered in the dropdown, which is lessdramatic because it's just a scenario flag, not an actual model change.
- Live lemma re-execution — our proofs aren't SymPy scripts with individual lemmas; they're attestation records. show the oracle outcome and evidence hashes but can't re-execute a symbolic proof lemma-by-lemma.

Those are architectural gaps in the engine, not the notebook. Everything else above is buildable today.

---

Ready to implement? I'd do it in this order: (1) expose spine cell code, (2) wire the 4 figures, (3) reformat the tree output in _interrogate.py, (4) rework the header/sidebar.
