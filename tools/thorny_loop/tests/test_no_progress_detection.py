"""Tests for no-progress detection."""

from __future__ import annotations

import unittest

from tools.thorny_loop.loop import detect_no_progress


class NoProgressDetectionTest(unittest.TestCase):
    """Stop repeated failure loops when the signal is clear."""

    def test_identical_diff_and_signature_count_as_no_progress(self) -> None:
        result = detect_no_progress(
            previous_diff="diff --git a b",
            current_diff="diff --git a b",
            previous_signature="make-error",
            current_signature="make-error",
            previous_objective="Fix latex build",
            current_objective="Fix latex build",
            changed_files=["latex/manuscript.tex"],
        )

        self.assertTrue(result.no_progress)
        self.assertIn("identical_diff_across_turns", result.reasons)
        self.assertIn("same_failure_signature_twice", result.reasons)


if __name__ == "__main__":
    unittest.main()
