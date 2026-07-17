from __future__ import annotations

import sys
import unittest
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VALIDATION_DIR))

from validate_referentials import (  # noqa: E402
    ValidationReport,
    duplicates,
    is_ontology_subtype,
    type_compatible,
    validate_effect,
    validate_family_effect_boundaries,
    validate_reverse_state_side,
    validate_repository,
)


class ValidationHelpersTest(unittest.TestCase):
    def test_duplicates(self) -> None:
        self.assertEqual(duplicates(["A", "B", "A", "C", "B"]), ["A", "B"])

    def test_transitive_ontology_subtype(self) -> None:
        parents = {"PatrolBoat": {"Platform"}, "Platform": {"PhysicalEntity"}}
        self.assertTrue(is_ontology_subtype("PatrolBoat", "PhysicalEntity", parents))
        self.assertFalse(is_ontology_subtype("PhysicalEntity", "Platform", parents))

    def test_union_type_compatibility(self) -> None:
        types = {"SM-TY-010": {"union_of": ["nmo:SpatialRegion", "nmo:Route"]}}
        self.assertTrue(type_compatible("nmo:Route", "SM-TY-010", types, {}))
        self.assertFalse(type_compatible("nmo:Platform", "SM-TY-010", types, {}))

    def test_orphan_reverse_state_reference_is_reported(self) -> None:
        state = {
            "id": "SM-ST-001",
            "producers": [{"kind": "task", "ref": "TC-001-S01"}],
        }
        report = ValidationReport()
        validate_reverse_state_side(state, "producers", {}, report)
        self.assertEqual(report.errors[0][0], "STATE010")

    def test_direct_world_effect_on_derived_state_is_reported(self) -> None:
        report = ValidationReport()
        state = {"category": "world", "persistence": "derived_fluent"}
        validate_effect("TC-001-S01", "SM-ST-001", "effect:world", {}, state, {"SM-ST-001": {"TC-001-S01"}}, report)
        self.assertEqual(report.errors[0][0], "SEM022")

    def test_ISR_direct_world_effect_is_reported(self) -> None:
        report = ValidationReport()
        semantics = {"operational_effects": {"world": {"add": [{"state_ref": "SM-ST-001"}], "remove": []}}}
        validate_family_effect_boundaries("TC-003-S01", "SF-01", semantics, report)
        self.assertEqual(report.errors[0][0], "SEM023")


class CurrentRepositoryTest(unittest.TestCase):
    def test_current_repository_is_consistent(self) -> None:
        root = Path(__file__).resolve().parents[3]
        report = validate_repository(root)
        details = "\n".join(f"[{code}] {location}: {message}" for code, location, message in report.errors)
        self.assertTrue(report.ok, details)


if __name__ == "__main__":
    unittest.main()
