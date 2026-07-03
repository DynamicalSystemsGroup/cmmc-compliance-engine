"""Determinism tests for `evidence/hashing.py` (rdflib only).

Ported from ADCS-lifecycle-demo determinism tests (`tests/test_symbolic.py`
TestHashing, `tests/test_traceability.py`). Asserts:
- same input bytes -> identical SHA-256; different input -> different hash;
- `hash_structural_model` is stable across two parses of the same graph;
- `hash_check_result` / `hash_config_export` are deterministic.
"""

from __future__ import annotations

from rdflib import Graph

from compliance_engine.pipeline.evidence.hashing import (
    hash_check_result,
    hash_config_export,
    hash_evidence,
    hash_structural_model,
)

# A small RDF document with a blank node, so the canonical N-Triples +
# blank-node flattening path is exercised.
_TTL = """
@prefix ce: <https://example.org/ce#> .
@prefix cmmc: <https://example.org/cmmc#> .

ce:System-NV012 a ce:System ;
    ce:label "NV012 CUI enclave" ;
    ce:addresses cmmc:IA.L2-3.5.3 ;
    ce:collectionMetadata [
        ce:sourceSystem "workspace.2sv" ;
        ce:collectorVersion "mock-0.1.0"
    ] .
"""

_TTL_DIFFERENT = _TTL.replace("NV012 CUI enclave", "NV099 CUI enclave")


def _parse(ttl: str) -> Graph:
    g = Graph()
    g.parse(data=ttl, format="turtle")
    return g


class TestStructuralModelHash:
    def test_is_64_hex_chars(self):
        h = hash_structural_model(_parse(_TTL))
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_deterministic_across_two_parses(self):
        # Two independent parses of the same source produce the same hash,
        # even though blank-node ids differ between parses.
        h1 = hash_structural_model(_parse(_TTL))
        h2 = hash_structural_model(_parse(_TTL))
        assert h1 == h2

    def test_different_graph_different_hash(self):
        assert hash_structural_model(_parse(_TTL)) != hash_structural_model(
            _parse(_TTL_DIFFERENT)
        )


class TestEvidenceHash:
    def test_same_input_same_hash(self):
        a = hash_evidence("model-abc", proof_hash="p1", sim_hash="s1")
        b = hash_evidence("model-abc", proof_hash="p1", sim_hash="s1")
        assert a == b
        assert len(a) == 64

    def test_different_input_different_hash(self):
        base = hash_evidence("model-abc", proof_hash="p1", sim_hash="s1")
        assert base != hash_evidence("model-XYZ", proof_hash="p1", sim_hash="s1")
        assert base != hash_evidence("model-abc", proof_hash="p2", sim_hash="s1")
        assert base != hash_evidence("model-abc", proof_hash="p1", sim_hash="s2")

    def test_optional_hashes_default_none(self):
        # Absent proof/sim hashes are distinct from a present one.
        assert hash_evidence("m") != hash_evidence("m", proof_hash="p1")


class TestCheckResultHash:
    _RESULT = {"status": "PASS", "detail": "no violations", "raw": {"passed": 3}}

    def test_deterministic(self):
        a = hash_check_result("opa", "AC.L2-3.1.1", self._RESULT)
        b = hash_check_result("opa", "AC.L2-3.1.1", dict(self._RESULT))
        assert a == b
        assert len(a) == 64

    def test_key_order_independent(self):
        # sort_keys=True => insertion order of the result dict is irrelevant.
        reordered = {"raw": {"passed": 3}, "detail": "no violations", "status": "PASS"}
        assert hash_check_result("opa", "AC.L2-3.1.1", self._RESULT) == hash_check_result(
            "opa", "AC.L2-3.1.1", reordered
        )

    def test_different_tool_or_control_or_result_differs(self):
        base = hash_check_result("opa", "AC.L2-3.1.1", self._RESULT)
        assert base != hash_check_result("checkov", "AC.L2-3.1.1", self._RESULT)
        assert base != hash_check_result("opa", "SC.L2-3.13.11", self._RESULT)
        assert base != hash_check_result(
            "opa", "AC.L2-3.1.1", {**self._RESULT, "status": "FAIL"}
        )


class TestConfigExportHash:
    _CONFIG = {"enforcedIn2Sv": True, "orgUnitPath": "/Privileged"}

    def test_deterministic(self):
        a = hash_config_export("workspace.2sv", "IA.L2-3.5.3", self._CONFIG)
        b = hash_config_export("workspace.2sv", "IA.L2-3.5.3", dict(self._CONFIG))
        assert a == b
        assert len(a) == 64

    def test_different_config_differs(self):
        base = hash_config_export("workspace.2sv", "IA.L2-3.5.3", self._CONFIG)
        assert base != hash_config_export(
            "workspace.2sv", "IA.L2-3.5.3", {**self._CONFIG, "enforcedIn2Sv": False}
        )
        assert base != hash_config_export("gcp.org_policy", "IA.L2-3.5.3", self._CONFIG)
