from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

VALIDATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VALIDATION_DIR))

import aggregate_expert_review as aggregate  # noqa: E402
import generate_expert_review as generate  # noqa: E402


class AggregatePrivacyTests(unittest.TestCase):
    def test_expert_review_paths_stay_in_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repository"
            root.mkdir()
            inside = root / "validation" / "wording.yaml"
            outside = Path(tmp) / "outside.yaml"
            with patch.object(generate, "ROOT", root):
                self.assertEqual(generate.workspace_path(inside, "wording"), inside.resolve())
                with self.assertRaises(ValueError):
                    generate.workspace_path(outside, "wording")

    def test_tracked_matrix_keeps_counts_not_expert_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            matrix_path = root / "items_test-v0.1.yaml"
            responses = root / "responses"
            responses.mkdir()
            matrix_path.write_text(yaml.safe_dump({
                "campaign": "test-v0.1",
                "items": [{
                    "id": "VQ-001",
                    "question": {"format": "vf", "expected": "Vrai",
                                 "statement": "Affirmation"},
                    "status": "pending",
                }],
            }, allow_unicode=True, sort_keys=False), encoding="utf-8")
            (responses / "response.json").write_text(json.dumps({
                "campaign": "test-v0.1",
                "expert": "Expert Nominal",
                "answers": {"VQ-001": {"value": "Ça dépend", "comment": "Commentaire privé"}},
            }), encoding="utf-8")

            argv = ["aggregate_expert_review.py", "--matrix", str(matrix_path),
                    "--responses", str(responses)]
            with patch.object(sys, "argv", argv):
                self.assertEqual(aggregate.main(), 0)

            aggregated = yaml.safe_load(matrix_path.read_text(encoding="utf-8"))
            item = aggregated["items"][0]
            self.assertEqual(item["reviewer_count"], 1)
            self.assertNotIn("reviewers", item)
            self.assertEqual(aggregated["last_aggregation"]["reviewer_count"], 1)
            self.assertNotIn("responses", aggregated["last_aggregation"])
            self.assertNotIn("Expert Nominal", matrix_path.read_text(encoding="utf-8"))

            report = (root / "report_test-v0.1.md").read_text(encoding="utf-8")
            self.assertIn("Expert Nominal", report)
            self.assertIn("Commentaire privé", report)


if __name__ == "__main__":
    unittest.main()
