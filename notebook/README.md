# The compliance engine — interactive walkthrough

A [marimo](https://marimo.io) dashboard that runs the **real** engine end-to-end
and tells the full compliance story: contract → obligations → controls → signed
Order → Factory assembly line → human attestation → proof artifacts.

Pick a scenario from the sidebar and the whole chain re-runs on the real code:

- **all-covered** — full chain completes → SPRS 110 / Final + mock BOM & SSP.
- **gap** — Gate 1 refuses and names the uncovered control; nothing is built.
- **contradiction** — a human signs MET over a *failed* machine check → the audit flags it.

Everything runs on fixture data with mock providers — no cloud, no credentials —
so every artifact is stamped **NON-EVIDENTIARY**.

## Run it

All commands from the **repo root** so the notebook can import the engine.

```bash
# one-time: install marimo (the only notebook dependency)
uv sync --group notebook
```

### Author / explore (interactive, editable)

```bash
uv run --group notebook marimo edit notebook/compliance_walkthrough.py
```

Opens the notebook in marimo's editor. Code cells are visible. Change the
**Scenario** dropdown in the sidebar and watch every cell downstream re-run.

### Present (read-only dashboard, no code)

```bash
uv run --group notebook marimo run notebook/compliance_walkthrough.py
```

Opens the notebook as a read-only app at `http://localhost:2718`. No code cells
visible — just the sidebar + four tabs. Ideal for demos and sharing.

### Export to static HTML

```bash
uv run --group notebook marimo export html-wasm notebook/compliance_walkthrough.py -o walkthrough/
```

Produces a self-contained static site in `walkthrough/`. Serve it with any HTTP
server:

```bash
python -m http.server --directory walkthrough/
```

**Caveat:** WASM export runs marimo's Python runtime in the browser via
Pyodide. The engine is deterministic, so it reproduces the same numbers, but
cold-start is slower than the server-backed `marimo run`.

## Structure

### Sidebar (always visible)

- **Scenario selector** — switch between all-covered, gap, contradiction
- **Live indicators** — controls required, modules claimed, Gate 1 status,
  SPRS score, contradiction count, machine-proven split
- **NON-EVIDENTIARY warning**
- **Glossary** — 15 terms in a collapsible accordion

### Tab 1: The Contract — *what must be true*

The story from contract to signed build order. Shows where obligations come from
(DFARS clause, SBIR text, Q&A), the COP signing ceremony (Compliance Officer
mockup), the obligation→control→module mapping, and Gate 1's planning coverage
check (green PASS or red REFUSAL naming the gap).

### Tab 2: The Factory — *make it true + prove it*

The 7-stage assembly line: load Order → fetch modules by hash → Terraform plan
(mock providers) → policy check → mock apply → evidence collection → oracle
outcomes. Includes the **control attestation screen** (Affirming Official
mockup), the override-justification flow, and a False Claims Act warning
callout.

### Tab 3: The Proof — *here's what we can show*

SPRS score dashboard, proven-vs-attested visual split, contradiction flag, BOM
preview (with content-addressed registry), SSP preview (with NON-EVIDENTIARY
banner), and the **auditor's view** — C3PAO re-verification screen, tamper
detection demo, before/after comparison (screenshots vs content-addressing),
named-graph substrate, timeline, and roles diagram.

### Tab 4: Coverage — *what the engine covers vs. what you own*

All 110 CMMC Level 2 controls in one filterable table. Three status categories:

- **✅ Covered** — engine checks this today (Terraform config, oracle criteria,
  attestation all wired).
- **🔧 Wire it** — machine-checkable via GCP / Workspace / GitHub / EDR APIs,
  but no evidence generator exists yet. See Track A in the self-assessment plan.
- **📋 On you** — requires policy documents, training records, physical
  inspection, or signed procedures. The oracle always returns `cantTell`.

Columns include SPRS weight (**Wt**), **No POA&M** flag (controls that cannot
be deferred — all 5-pt and 3-pt controls plus six specific 1-pt controls), and
**CSP** inheritance status (two PE controls handled by Google IL4). Bottom
section: per-family scorecard showing maximum SPRS points at risk by family.

### Engine adapter

[`_engine.py`](_engine.py) calls the same code paths the operator CLI
(`../cli.py`) uses — it never reimplements engine logic. The notebook is a
viewport: the signing screen mockups, auditor views, contract excerpts, and
False Claims Act warning are presentation-layer content, not engine output. Run
artifacts go to a throwaway temp directory, never the repo.

## Tests

```bash
uv run --group notebook pytest tests/test_notebook_smoke.py -v
```

Covers all three scenarios, determinism, invalid input, named-graph population,
and marimo file validity.
