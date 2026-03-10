"""Tests for artifact path generation."""

from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path

from tools.thorny_loop.artifacts import build_run_paths, make_run_id


class ReportPathTest(unittest.TestCase):
    """Ensure run IDs and paths stay inside quality_reports/thorny_loop."""

    def test_make_run_id_is_stable_for_fixed_datetime(self) -> None:
        run_id = make_run_id(
            "Fix simulation outputs and manuscript numbers disagree",
            now=datetime(2026, 3, 9, 12, 34, 56),
        )
        self.assertEqual(run_id, "20260309_123456_fix-simulation-outputs-and-manuscript-numbers-di")

    def test_build_run_paths(self) -> None:
        repo_root = Path("/tmp/repo-template-test").resolve()
        run_paths = build_run_paths(repo_root, "20260309_123456_test-run")

        self.assertEqual(
            run_paths.run_dir,
            repo_root / "quality_reports" / "thorny_loop" / "20260309_123456_test-run",
        )
        self.assertEqual(run_paths.reviews_dir, run_paths.run_dir / "reviews")
        self.assertEqual(
            run_paths.baseline_snapshot_file,
            run_paths.run_dir / "baseline_worktree_snapshot.json",
        )
        self.assertEqual(run_paths.manifest_file, run_paths.run_dir / "manifest.json")


if __name__ == "__main__":
    unittest.main()
