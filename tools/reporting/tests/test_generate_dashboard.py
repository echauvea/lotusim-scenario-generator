from __future__ import annotations

import hashlib
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

import yaml

REPORTING_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPORTING_DIR))

import generate_dashboard as dashboard  # noqa: E402


class DashboardCampaignTests(unittest.TestCase):
    def write_matrix(self, directory: Path, catalog_sha256: str) -> None:
        matrix = {
            "campaign": "test-v0.1",
            "catalog": "LOTUSim_Method_Catalog_v0.2.0.md",
            "catalog_version": "0.2.0",
            "catalog_sha256": catalog_sha256,
            "last_aggregation": {
                "date": "2026-07-19",
                "response_count": 1,
                "reviewer_count": 1,
            },
            "items": [
                {"id": "VQ-001", "status": "validé", "reviewer_count": 1},
                {"id": "VQ-002", "status": "pending", "covered_by": "VQ-001",
                 "reviewer_count": 1},
            ],
        }
        (directory / "items_test-v0.1.yaml").write_text(
            yaml.safe_dump(matrix, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    def test_content_change_makes_prior_validation_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            expert_dir = Path(tmp)
            original = b"catalog baseline"
            self.write_matrix(expert_dir, hashlib.sha256(original).hexdigest())
            current = {
                "LOTUSim_Method_Catalog": {
                    "version": "v0.2.0",
                    "sha256": hashlib.sha256(b"changed without version bump").hexdigest(),
                }
            }
            with patch.object(dashboard, "EXPERT_DIR", expert_dir):
                campaigns = dashboard.load_campaigns(current)
            self.assertEqual(campaigns[0]["validated"], 0)
            self.assertEqual(campaigns[0]["stale"], 1)
            self.assertEqual(campaigns[0]["reviewer_count"], 1)

    def test_campaign_matrix_rejects_expert_identities(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            expert_dir = Path(tmp)
            matrix = {
                "campaign": "unsafe-v0.1",
                "catalog": "LOTUSim_Method_Catalog_v0.2.0.md",
                "catalog_version": "0.2.0",
                "items": [{"id": "VQ-001", "status": "pending",
                           "reviewers": ["Expert Nominal"]}],
            }
            (expert_dir / "items_unsafe-v0.1.yaml").write_text(
                yaml.safe_dump(matrix, allow_unicode=True), encoding="utf-8")
            current = {
                "LOTUSim_Method_Catalog": {
                    "version": "v0.2.0",
                    "sha256": hashlib.sha256(b"catalog").hexdigest(),
                }
            }
            with patch.object(dashboard, "EXPERT_DIR", expert_dir):
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    dashboard.load_campaigns(current)

    def test_instrumentation_matrix_uses_absolute_count(self) -> None:
        rendered = dashboard.matrix_rows([{
            "name": "Method Catalog",
            "inventory": "2",
            "inventory_label": "méthodes",
            "campaigns": [{
                "instrumented": 35,
                "asked": 23,
                "exposed": 0,
                "validated": 0,
                "stale": 0,
            }],
        }])
        self.assertIn("<b>35</b><span>items · 23 questions</span>", rendered)
        self.assertNotIn("<b>100 %</b>", rendered)

    def test_current_commit_supports_linked_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "worktree"
            git_dir = base / "main.git" / "worktrees" / "dashboard"
            common = base / "main.git"
            root.mkdir()
            git_dir.mkdir(parents=True)
            (common / "refs" / "heads").mkdir(parents=True)
            (root / ".git").write_text(f"gitdir: {git_dir}\n", encoding="utf-8")
            (git_dir / "commondir").write_text("../..\n", encoding="utf-8")
            (git_dir / "HEAD").write_text("ref: refs/heads/topic\n", encoding="utf-8")
            (common / "refs" / "heads" / "topic").write_text(
                "1234567890abcdef\n", encoding="utf-8")
            with patch.object(dashboard, "ROOT", root), patch.dict(
                    dashboard.os.environ, {}, clear=True):
                self.assertEqual(dashboard.current_commit(), "1234567")


if __name__ == "__main__":
    unittest.main()
