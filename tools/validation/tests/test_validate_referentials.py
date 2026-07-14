from __future__ import annotations

import sys
import unittest
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VALIDATION_DIR))

from validate_referentials import (  # noqa: E402
    duplicates,
    is_ontology_subtype,
    type_compatible,
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


class CurrentRepositoryTest(unittest.TestCase):
    def test_current_repository_is_consistent(self) -> None:
        root = Path(__file__).resolve().parents[3]
        report = validate_repository(root)
        details = "\n".join(f"[{code}] {location}: {message}" for code, location, message in report.errors)
        self.assertTrue(report.ok, details)


if __name__ == "__main__":
    unittest.main()
