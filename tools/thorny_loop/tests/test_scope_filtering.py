"""Tests for scope safety and destructive command filtering."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.thorny_loop.util import command_is_blocked, normalize_scope_paths


class ScopeFilteringTest(unittest.TestCase):
    """Verify repo-relative scope handling and blocked commands."""

    def test_normalize_scope_paths_rejects_escape(self) -> None:
        repo_root = Path("/tmp/repo-template-test").resolve()
        with self.assertRaises(ValueError):
            normalize_scope_paths(repo_root, ["../outside"])

    def test_command_block_list(self) -> None:
        self.assertTrue(command_is_blocked("git reset --hard HEAD"))
        self.assertTrue(command_is_blocked("rm -rf .git"))
        self.assertFalse(command_is_blocked("make -n"))


if __name__ == "__main__":
    unittest.main()
