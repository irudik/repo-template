"""Tests for default verification command selection."""

from __future__ import annotations

import unittest
from pathlib import Path

from tools.thorny_loop.config import ThornyConfig
from tools.thorny_loop.verification import select_verification_commands


class VerificationSelectionTest(unittest.TestCase):
    """Keep verification Make-first and scoped to touched areas."""

    def setUp(self) -> None:
        self.config = ThornyConfig(repo_root=Path("/tmp/repo-template-test"), task="verify")

    def test_cross_cutting_scope_adds_targeted_and_root_make(self) -> None:
        commands = select_verification_commands(
            self.config,
            ["code/simulation/main.jl", "latex/manuscript.tex"],
        )
        self.assertEqual(commands[0], "make -n")
        self.assertIn("make -C code/simulation", commands)
        self.assertIn("make -C latex", commands)
        self.assertIn("make", commands)


if __name__ == "__main__":
    unittest.main()
