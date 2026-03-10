"""Tests for thorny-loop config parsing."""

from __future__ import annotations

import os
import unittest
from argparse import Namespace
from pathlib import Path

from tools.thorny_loop.config import load_config


class ThornyConfigTest(unittest.TestCase):
    """Verify CLI/env precedence and scope normalization."""

    def setUp(self) -> None:
        self.repo_root = Path("/tmp/repo-template-test").resolve()
        self.environ_backup = os.environ.copy()

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self.environ_backup)

    def test_cli_overrides_environment(self) -> None:
        os.environ["TASK"] = "env task"
        os.environ["THORNY_MAX_PLANNER_CALLS"] = "2"
        args = Namespace(
            task="cli task",
            scope=["code", "latex/manuscript.tex"],
            verify=["make -n"],
            verify_target="",
            max_planner_calls=3,
            max_coder_turns=5,
            planner_effort="high",
            quality_gate=95,
            dry_run=True,
            resume="",
            report="",
        )

        config = load_config(args, repo_root=self.repo_root)

        self.assertEqual(config.task, "cli task")
        self.assertEqual(config.max_planner_calls, 3)
        self.assertEqual(config.hard_max_coder_turns, 5)
        self.assertEqual(config.quality_gate_target, 95)
        self.assertEqual(config.scope_paths, ["code", "latex/manuscript.tex"])
        self.assertEqual(config.explicit_verify_commands, ["make -n"])

    def test_env_scope_string_is_split_when_cli_scope_missing(self) -> None:
        os.environ["TASK"] = "env task"
        os.environ["SCOPE"] = "code/simulation latex/manuscript.tex"
        args = Namespace(
            task="",
            scope=None,
            verify=None,
            verify_target="",
            max_planner_calls=None,
            max_coder_turns=None,
            planner_effort=None,
            quality_gate=None,
            dry_run=False,
            resume="",
            report="",
        )

        config = load_config(args, repo_root=self.repo_root)

        self.assertEqual(config.task, "env task")
        self.assertEqual(config.scope_paths, ["code/simulation", "latex/manuscript.tex"])

    def test_legacy_background_opt_out_overrides_auto(self) -> None:
        os.environ["TASK"] = "env task"
        os.environ["THORNY_BACKGROUND_PLANNER"] = "auto"
        os.environ["THORNY_USE_BACKGROUND"] = "0"
        args = Namespace(
            task="",
            scope=None,
            verify=None,
            verify_target="",
            max_planner_calls=None,
            max_coder_turns=None,
            planner_effort=None,
            quality_gate=None,
            dry_run=False,
            resume="",
            report="",
        )

        config = load_config(args, repo_root=self.repo_root)

        self.assertEqual(config.background_planner, "never")


if __name__ == "__main__":
    unittest.main()
