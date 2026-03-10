"""Tests for planner JSON extraction and repair."""

from __future__ import annotations

import unittest
from types import SimpleNamespace

from tools.thorny_loop.planner import _wait_for_background_response, extract_plan_json, parse_planner_decision


class PlanParsingTest(unittest.TestCase):
    """Verify planner outputs are marker-parsed and locally repaired."""

    def test_marker_extraction(self) -> None:
        raw_output = """
Noise
PLAN_JSON_BEGIN
{"status":"done","why_called":"final_review","diagnosis":"Done","risk_flags":[],"next_increment":{"objective":"None","files_to_touch":[],"constraints":[],"verification_commands":[],"review_requests":[],"acceptance_criteria":[]},"questions_for_user":[],"stop_if":[]}
PLAN_JSON_END
"""
        payload = extract_plan_json(raw_output)
        self.assertIn('"status":"done"', payload)

    def test_parse_decision_without_markers_uses_repair(self) -> None:
        raw_output = """
```json
{"status":"blocked","why_called":"stalled","diagnosis":"Need user input","risk_flags":[],"next_increment":{"objective":"Stop","files_to_touch":[],"constraints":[],"verification_commands":[],"review_requests":[],"acceptance_criteria":[]},"questions_for_user":["Choose a target"],"stop_if":["Missing decision"]}
```
"""
        decision = parse_planner_decision(raw_output)
        self.assertEqual(decision.status, "blocked")
        self.assertEqual(decision.why_called, "stalled")

    def test_background_response_is_polled_until_complete(self) -> None:
        queued = SimpleNamespace(id="resp_123", status="queued")
        completed = SimpleNamespace(
            id="resp_123",
            status="completed",
            output_text="PLAN_JSON_BEGIN {} PLAN_JSON_END",
        )

        class FakeResponses:
            def __init__(self) -> None:
                self.calls = 0

            def retrieve(self, response_id: str) -> SimpleNamespace:
                self.calls += 1
                self.last_response_id = response_id
                return completed

        fake_client = SimpleNamespace(responses=FakeResponses())

        resolved = _wait_for_background_response(
            fake_client,
            queued,
            timeout_seconds=1,
            poll_interval_seconds=0,
        )

        self.assertIs(resolved, completed)
        self.assertEqual(fake_client.responses.calls, 1)
        self.assertEqual(fake_client.responses.last_response_id, "resp_123")


if __name__ == "__main__":
    unittest.main()
