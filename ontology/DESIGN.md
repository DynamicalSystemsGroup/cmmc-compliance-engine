# ontology/ — the `cmmc:` TBox (the Control Catalog, machine form)

**Purpose.** Hold the **Control Requirements Catalog** (Document 1) as RDF: the 110 NIST SP 800-171 Rev 2 controls as `cmmc:Control` individuals plus a thin integration ontology. This is the "law" layer, loaded into `<ce:ontology>`.

**Port from ADCS.** `ontology/rtm-edit.ttl` (source → built pattern), `ontology/rtm_shapes.ttl` (SHACL closure suite), `scripts/build_ontology.py` (ROBOT/ELK verification + triple-count budget). Keep the discipline: `cmmc:` introduces **no novel epistemic vocabulary** — its classes/properties subclass established standards.

**Design.**
- `cmmc:Control ⊑ sysml:RequirementDefinition` — a control is a requirement, so all ADCS traceability queries work unchanged.
- Per-control data properties mirror Document 1's columns: `cmmc:weight` (1|3|5), `cmmc:poamEligible` (bool), `cmmc:nonDeferrable` (bool), `cmmc:assessmentMethod` (Examine|Interview|Test), `cmmc:evidenceType`, `cmmc:family`.
- Framework layering via `cmmc:derivedFrom` (control → NIST req → DFARS/IL5/ITAR overlays), reusing ADCS requirement-derivation queries.
- Reuse EARL outcome lattice (`earl:passed/failed/inapplicable/untested/cantTell`) for control status — do **not** invent a status vocabulary.

**Build.** `cmmc-edit.ttl` is the hand-edited source; a built `cmmc.ttl` artifact is generated + verified (ROBOT merge + ELK reason + triple budget). Commit source before rebuild (ADCS ordering rule).

**Inputs:** `reference/control-catalog.md`. **Outputs:** `<ce:ontology>` graph; the authority a **SPRS oracle** reads for weights + POA&M legality.

**Related vocab (upstream).** The `cmmc:Obligation` type + `cmmc:derivesControls`
(obligation → control) live with the Order Compiler (`../order-compiler/obligations.ttl`);
the control catalog here is the shared target both the Compiler (Gate 1) and the
Factory (Gate 2) resolve against.

**SHACL shapes to add:** `ControlShape` (every `cmmc:Control` has id + text + weight + poamEligible); `PoamLegalityShape` (a control with `cmmc:weight > 1` MUST NOT carry a `cmmc:poamItem`).
