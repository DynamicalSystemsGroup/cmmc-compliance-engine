"""Tests for the SPRS scorer + catalog-backed loader (U10 SPRS half).

SPRS (32 CFR §170.21/170.24): score = 110 − Σ(weight of non-MET).
  110      → Final;  88..109 → Conditional (POA&M);  <88 → Ineligible.
POA&M legality: only 1-point controls may be deferred, and six specific
1-pointers are excluded — a 3/5-pt OR an excluded control on a POA&M makes the
submission invalid regardless of score.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from traceability.sprs import (
    CONDITIONAL_FLOOR,
    FINAL,
    ControlStatus,
    load_control_statuses,
    score,
    sprs_from_catalog,
)

_CATALOG = Path(__file__).resolve().parents[1] / "ontology" / "cmmc-edit.ttl"

# The six excluded 1-pointers (nonDeferrable, poam_eligible False) per the plan.
_EXCLUDED_ONE_POINTERS = {
    "AC.L2-3.1.20", "AC.L2-3.1.22", "CA.L2-3.12.4",
    "PE.L2-3.10.3", "PE.L2-3.10.4", "PE.L2-3.10.5",
}


def _cs(control_id, weight, met, *, on_poam=False, poam_eligible=False):
    return ControlStatus(control_id, weight, met, on_poam=on_poam, poam_eligible=poam_eligible)


# --------------------------------------------------------------------------- #
# score() — pure computation
# --------------------------------------------------------------------------- #

class TestScore:
    def test_all_met_is_final_110_valid(self):
        controls = [_cs(f"C{i}", w, met=True) for i, w in enumerate([5, 5, 3, 1, 1])]
        r = score(controls)
        assert r.score == FINAL == 110
        assert r.status == "Final"
        assert r.valid_submission is True
        assert r.unmet == []

    def test_ineligible_edge_76(self):
        # five 5-pt + three 3-pt unmet → 110 - (25 + 9) = 76 → Ineligible.
        controls = [_cs(f"F{i}", 5, met=False) for i in range(5)]
        controls += [_cs(f"T{i}", 3, met=False) for i in range(3)]
        controls += [_cs("MET", 5, met=True)]
        r = score(controls)
        assert r.score == 76
        assert r.status == "Ineligible"
        assert len(r.unmet) == 8

    def test_conditional_floor_boundary_88_then_87(self):
        # 22 unmet 1-pointers → 110 - 22 = 88 → Conditional (the floor).
        at_floor = [_cs(f"P{i}", 1, met=False) for i in range(22)]
        r88 = score(at_floor)
        assert r88.score == CONDITIONAL_FLOOR == 88
        assert r88.status == "Conditional"

        # one more point of deduction → 87 → Ineligible (prove the boundary).
        below = at_floor + [_cs("P22", 1, met=False)]
        r87 = score(below)
        assert r87.score == 87
        assert r87.status == "Ineligible"

    def test_exact_110_is_final_not_conditional(self):
        r = score([_cs("A", 5, met=True)])
        assert r.score == 110 and r.status == "Final"


class TestPoamLegality:
    def test_five_point_on_poam_is_illegal(self):
        controls = [_cs("BIG", 5, met=False, on_poam=True, poam_eligible=False)]
        r = score(controls)
        assert "BIG" in r.illegal_poam
        assert r.valid_submission is False  # invalid regardless of score

    def test_excluded_one_pointer_on_poam_is_illegal(self):
        # weight 1 but poam_eligible False (a nonDeferrable excluded control).
        controls = [_cs("AC.L2-3.1.20", 1, met=False, on_poam=True, poam_eligible=False)]
        r = score(controls)
        assert "AC.L2-3.1.20" in r.illegal_poam
        assert r.valid_submission is False

    def test_legal_poam_eligible_one_pointer(self):
        controls = [_cs("AC.L2-3.1.10", 1, met=False, on_poam=True, poam_eligible=True)]
        r = score(controls)
        assert r.illegal_poam == []
        assert r.valid_submission is True
        assert r.score == 109 and r.status == "Conditional"


# --------------------------------------------------------------------------- #
# load_control_statuses() — catalog-backed
# --------------------------------------------------------------------------- #

class TestLoader:
    def test_loads_all_110_with_real_weights(self):
        statuses = load_control_statuses(_CATALOG, met_control_ids=set())
        assert len(statuses) == 110
        assert all(s.met is False for s in statuses)  # empty MET set

    def test_histogram_matches_catalog(self):
        statuses = load_control_statuses(_CATALOG, met_control_ids=set())
        non_variable = Counter(s.weight for s in statuses if not s.variable_weight)
        variable = [s for s in statuses if s.variable_weight]
        assert dict(non_variable) == {5: 42, 3: 14, 1: 52}
        assert len(variable) == 2
        # variable controls resolve to full weight (5) with partial weight 3.
        for s in variable:
            assert s.weight == 5 and s.weight_if_partial == 3

    def test_six_nondeferrable_load_poam_ineligible(self):
        by_id = {s.control_id: s for s in load_control_statuses(_CATALOG, met_control_ids=set())}
        for cid in _EXCLUDED_ONE_POINTERS:
            assert by_id[cid].weight == 1
            assert by_id[cid].poam_eligible is False
        # sanity: an eligible 1-pointer loads poam_eligible True.
        assert by_id["AC.L2-3.1.10"].poam_eligible is True

    def test_all_met_scores_110(self):
        all_ids = {s.control_id for s in load_control_statuses(_CATALOG, met_control_ids=set())}
        r = sprs_from_catalog(_CATALOG, met_control_ids=all_ids)
        assert r.score == 110 and r.status == "Final"
        assert r.valid_submission is True

    def test_met_set_drives_met(self):
        met = {"AC.L2-3.1.1"}
        statuses = load_control_statuses(_CATALOG, met_control_ids=met)
        met_rows = [s for s in statuses if s.met]
        assert [s.control_id for s in met_rows] == ["AC.L2-3.1.1"]

    def test_required_control_ids_subsets(self):
        required = {"AC.L2-3.1.1", "AC.L2-3.1.3"}
        statuses = load_control_statuses(
            _CATALOG, met_control_ids=required, required_control_ids=required,
        )
        assert {s.control_id for s in statuses} == required
        # both MET → no deduction over the required subset → Final.
        r = score(statuses)
        assert r.score == 110 and r.status == "Final"

    def test_poam_control_ids_flag_on_poam(self):
        # A required 5-pointer deferred to a POA&M → illegal.
        statuses = load_control_statuses(
            _CATALOG,
            met_control_ids=set(),
            poam_control_ids={"AC.L2-3.1.1"},
            required_control_ids={"AC.L2-3.1.1"},
        )
        r = score(statuses)
        assert "AC.L2-3.1.1" in r.illegal_poam
        assert r.valid_submission is False

    def test_loader_accepts_dataset(self):
        # Exercise the Dataset branch (default_union resolves control triples).
        from pipeline.dataset import create_dataset, load_into

        ds = create_dataset()
        load_into(ds, "ontology", _CATALOG)
        all_ids = {s.control_id for s in load_control_statuses(ds, met_control_ids=set())}
        assert len(all_ids) == 110
        r = sprs_from_catalog(ds, met_control_ids=all_ids)
        assert r.score == 110 and r.status == "Final"
