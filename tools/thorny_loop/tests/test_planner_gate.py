"""Tests for sparse planner gating."""

from __future__ import annotations

import unittest

from tools.thorny_loop.planner_gate import should_call_planner
from tools.thorny_loop.schemas import FailureSignature


class PlannerGateTest(unittest.TestCase):
    """Ensure planner calls stay sparse and evidence-driven."""

    def test_explicit_thorny_keyword_triggers_planner(self) -> None:
        should_call, why_called = should_call_planner(
            "Use the thorny loop for this task",
            ["tools/thorny_loop"],
            iteration_index=0,
        )
        self.assertTrue(should_call)
        self.assertEqual(why_called, "initial")

    def test_cross_cutting_scope_triggers_planner(self) -> None:
        should_call, why_called = should_call_planner(
            "Update code and manuscript together",
            ["code/simulation", "latex/manuscript.tex"],
            iteration_index=0,
        )
        self.assertTrue(should_call)
        self.assertEqual(why_called, "cross_cutting")

    def test_repeated_failure_signature_triggers_stalled_planner(self) -> None:
        failure = FailureSignature(
            command="make -C latex",
            exit_code=2,
            normalized_signature="undefined control sequence",
            first_error_line="! Undefined control sequence.",
            relevant_tail="...",
        )
        should_call, why_called = should_call_planner(
            "Keep trying",
            ["latex/manuscript.tex"],
            iteration_index=1,
            failure_history=[failure, failure],
        )
        self.assertTrue(should_call)
        self.assertEqual(why_called, "stalled")


if __name__ == "__main__":
    unittest.main()
