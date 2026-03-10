"""Tests for deterministic failure signature extraction."""

from __future__ import annotations

import unittest

from tools.thorny_loop.failure_signatures import build_failure_signature


class FailureSignatureTest(unittest.TestCase):
    """Normalize noisy stderr into repeatable signatures."""

    def test_signature_normalizes_line_numbers(self) -> None:
        signature_one = build_failure_signature(
            "make -C latex",
            2,
            "",
            "! Undefined control sequence.\nl.123 \\badmacro",
        )
        signature_two = build_failure_signature(
            "make -C latex",
            2,
            "",
            "! Undefined control sequence.\nl.456 \\badmacro",
        )

        self.assertEqual(signature_one.normalized_signature, signature_two.normalized_signature)


if __name__ == "__main__":
    unittest.main()
