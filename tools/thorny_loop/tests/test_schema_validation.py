"""Tests for Pydantic schema validation."""

from __future__ import annotations

import unittest

from pydantic import ValidationError

from tools.thorny_loop.schemas import PlannerDecision


class PlannerSchemaValidationTest(unittest.TestCase):
    """Validate core planner decision schema behavior."""

    def test_valid_payload_passes(self) -> None:
        payload = {
            "status": "continue",
            "why_called": "initial",
            "diagnosis": "Cross-cutting task needs a minimal first increment.",
            "risk_flags": ["manuscript_claims"],
            "next_increment": {
                "objective": "Touch the config loader first.",
                "files_to_touch": ["tools/thorny_loop/config.py"],
                "constraints": ["Keep edits minimal"],
                "verification_commands": ["python3 -m unittest"],
                "review_requests": [{"skill": "review-comments", "target": "tools/thorny_loop"}],
                "acceptance_criteria": ["Config parses CLI and env values"],
            },
            "questions_for_user": [],
            "stop_if": ["Verification fails with the same root cause twice"],
        }

        decision = PlannerDecision.model_validate(payload)

        self.assertEqual(decision.status, "continue")
        self.assertEqual(decision.next_increment.review_requests[0].skill, "review-comments")

    def test_invalid_review_skill_fails(self) -> None:
        payload = {
            "status": "continue",
            "why_called": "initial",
            "diagnosis": "Invalid skill should fail validation.",
            "risk_flags": [],
            "next_increment": {
                "objective": "Test invalid skill",
                "files_to_touch": [],
                "constraints": [],
                "verification_commands": [],
                "review_requests": [{"skill": "review-makefile", "target": "Makefile"}],
                "acceptance_criteria": [],
            },
            "questions_for_user": [],
            "stop_if": [],
        }

        with self.assertRaises(ValidationError):
            PlannerDecision.model_validate(payload)


if __name__ == "__main__":
    unittest.main()
