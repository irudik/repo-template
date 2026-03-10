"""Tests for context compaction."""

from __future__ import annotations

import unittest

from tools.thorny_loop.compaction import ContextSection, fit_sections_to_budget


class ContextBudgetTest(unittest.TestCase):
    """Ensure high-priority sections survive budget trimming."""

    def test_budget_keeps_high_priority_sections(self) -> None:
        sections = [
            ContextSection(name="High", text="A" * 200, priority=1),
            ContextSection(name="Low", text="B" * 2000, priority=9),
        ]

        output = fit_sections_to_budget(sections, budget_tokens=100)

        self.assertIn("## High", output)
        self.assertIn("A", output)


if __name__ == "__main__":
    unittest.main()
