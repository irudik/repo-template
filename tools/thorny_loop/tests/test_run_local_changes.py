"""Tests for run-local changed-file tracking."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.thorny_loop.loop import capture_worktree_snapshot, diff_snapshot_paths


class RunLocalChangesTest(unittest.TestCase):
    """Ensure thorny-loop manifests exclude unrelated pre-existing worktree changes."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)
        self._git("init")
        self._write("already_dirty.txt", "baseline\n")
        self._write("later_changed.txt", "baseline\n")
        self._write("still_dirty.txt", "baseline\n")
        self._git("add", ".")
        self._git(
            "-c",
            "user.name=Test User",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-m",
            "initial",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _git(self, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=True,
        )

    def _write(self, relative_path: str, content: str) -> None:
        path = self.repo_root / relative_path
        path.write_text(content)

    def test_snapshot_delta_ignores_unchanged_baseline_dirty_files(self) -> None:
        self._write("already_dirty.txt", "baseline dirty\n")
        self._write("still_dirty.txt", "still dirty\n")
        baseline_snapshot = capture_worktree_snapshot(self.repo_root)

        self._write("already_dirty.txt", "baseline dirty plus run change\n")
        self._write("later_changed.txt", "run change only\n")
        current_snapshot = capture_worktree_snapshot(self.repo_root)

        changed_paths = diff_snapshot_paths(baseline_snapshot, current_snapshot)

        self.assertEqual(changed_paths, ["already_dirty.txt", "later_changed.txt"])

    def test_snapshot_delta_includes_new_untracked_files(self) -> None:
        baseline_snapshot = capture_worktree_snapshot(self.repo_root)

        self._write("new_file.txt", "created by run\n")
        current_snapshot = capture_worktree_snapshot(self.repo_root)

        changed_paths = diff_snapshot_paths(baseline_snapshot, current_snapshot)

        self.assertEqual(changed_paths, ["new_file.txt"])


if __name__ == "__main__":
    unittest.main()
