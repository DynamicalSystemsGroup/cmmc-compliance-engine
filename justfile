# compliance-engine — operator justfile
# Run `just` to list all recipes.

output := "output"
scenario := "all-covered"   # all-covered | gap | contradiction

# ── list all recipes ──────────────────────────────────────────────────────────

[private]
default:
    @just --list --unsorted

# ── setup ─────────────────────────────────────────────────────────────────────

# Install all dependency groups (dev + notebook)
install:
    uv sync --all-groups

# Install only the notebook extras (marimo, matplotlib, networkx)
install-notebook:
    uv sync --group notebook

# ── full demos (one command, every stage) ─────────────────────────────────────

# Happy path: 22-control NV012 slice → SPRS 110 / Final
demo:
    uv run ce demo --evidence-set all-covered --auto --output-dir {{output}}

# Gate 1 refusal: injected uncovered control, nothing built, exit 2
demo-gap:
    uv run ce demo --evidence-set gap --auto --output-dir {{output}}

# Contradiction: human signs MET over a failed oracle; audit surfaces it
demo-contradiction:
    uv run ce demo --evidence-set contradiction --auto --output-dir {{output}}

# Full 110-control catalog run + render the assessor report
demo-full:
    uv run ce demo --evidence-set all-covered --full --report --auto --output-dir {{output}}

# Persist run to the append-only Flexo tier (offline-simulated)
demo-flexo:
    uv run ce demo --evidence-set all-covered --auto --store-backend flexo --output-dir {{output}}

# Run all three scenarios back-to-back
demo-all: demo demo-gap demo-contradiction

# ── individual pipeline stages ────────────────────────────────────────────────

# Stage 1+2: compile the COP → Gate 1 → signed Order
compile-order:
    uv run ce compile-order --evidence-set {{scenario}} --auto --output-dir {{output}}

# Stage 3: run the Factory (provision plan + evidence + oracles)
run-factory:
    uv run ce run-factory --evidence-set {{scenario}} --output-dir {{output}}

# Stage 4: Gate 2 — auto-attest each control the Factory produced an outcome for
attest:
    uv run ce attest --output-dir {{output}}

# Stage 5: bidirectional audit + SPRS score; writes audit.md / audit.json
audit:
    uv run ce audit --output-dir {{output}}

# Stage 6: assemble the BOM; writes bom.json
bom:
    uv run ce bom --output-dir {{output}}

# Stage 7: render the SSP from the persisted dataset; writes ssp.md
ssp:
    uv run ce ssp --output-dir {{output}}

# ── verification + packaging ──────────────────────────────────────────────────

# Re-hash every evidence node (tamper check) + run SHACL closure suite
verify:
    uv run ce verify --output-dir {{output}}

# Assemble + sign the audit package (manifest.json + manifest.sig + report.html)
package:
    uv run ce package --output-dir {{output}}

# Re-verify the signed audit package offline: signature + artifact hashes + chain
verify-package:
    uv run ce verify-package --output-dir {{output}}

# Re-render the assessor report from an existing package (HTML + PDF if weasyprint)
report:
    uv run ce report --output-dir {{output}}

# Full assessor workflow: demo → package → verify-package
ship: demo package verify-package

# ── notebook ──────────────────────────────────────────────────────────────────

# Open the walkthrough notebook for editing (hot-reload)
edit:
    uv run --group notebook marimo edit notebooks/compliance_walkthrough.py

# Serve the walkthrough as a read-only app
serve:
    uv run --group notebook marimo run notebooks/compliance_walkthrough.py

# Export the walkthrough to a self-contained HTML file
export-html:
    uv run --group notebook marimo export html notebooks/compliance_walkthrough.py \
        --no-include-code -o {{output}}/index.html

# Export the walkthrough with code visible (for the published ADCS-style view)
export-html-with-code:
    uv run --group notebook marimo export html notebooks/compliance_walkthrough.py \
        -o {{output}}/index.html

# ── tests ─────────────────────────────────────────────────────────────────────

# Run the default suite (skips live, network, and terraform tests)
test:
    uv run pytest -q

# Run only tests that match a keyword or file  (e.g. just test-k sprs)
test-k *args:
    uv run pytest -q -k "{{args}}"

# Run tests that need the terraform binary (skipped automatically when absent)
test-terraform:
    uv run pytest -q -m terraform

# Run all tests including live + network (requires external connectivity)
test-all:
    uv run pytest -q -m "" --override-ini="addopts="

# Run with coverage report
test-cov:
    uv run pytest -q --cov=compliance_engine --cov-report=term-missing

# Notebook smoke test only
test-notebook:
    uv run pytest -q tests/test_notebook_smoke.py

# ── lint / format ─────────────────────────────────────────────────────────────

# Check code style (no fixes)
lint:
    uv run ruff check .

# Auto-fix lint issues and reformat
fmt:
    uv run ruff check --fix .
    uv run ruff format .

# ── clean ─────────────────────────────────────────────────────────────────────

# Remove generated output artifacts (keeps registry objects)
clean:
    rm -f {{output}}/audit.json {{output}}/audit.md \
          {{output}}/bom.json {{output}}/ssp.md \
          {{output}}/run_state.json {{output}}/index.html
    rm -rf {{output}}/package

# Remove everything in output/ including the registry
clean-all:
    rm -rf {{output}}
