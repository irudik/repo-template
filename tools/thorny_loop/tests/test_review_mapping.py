"""Tests for review skill mapping."""

from __future__ import annotations

import unittest

from tools.thorny_loop.review import collect_review_requests, map_changed_files_to_reviews
from tools.thorny_loop.schemas import ReviewRequest


class ReviewMappingTest(unittest.TestCase):
    """Ensure changed file types reuse the existing repo review skills."""

    def test_changed_files_map_to_expected_skills(self) -> None:
        requests = map_changed_files_to_reviews(
            [
                "code/simulation/model.jl",
                "code/tables/build.R",
                "latex/manuscript.tex",
                "tools/thorny_loop/loop.py",
            ]
        )
        pairs = {(request.skill, request.target) for request in requests}
        self.assertIn(("review-julia", "code/simulation/model.jl"), pairs)
        self.assertIn(("review-r", "code/tables/build.R"), pairs)
        self.assertIn(("review-tex", "latex/manuscript.tex"), pairs)
        self.assertNotIn(("review-comments", "tools/thorny_loop"), pairs)

    def test_explicit_planner_reviews_are_preserved(self) -> None:
        requests = collect_review_requests(
            ["tools/thorny_loop/loop.py"],
            [ReviewRequest(skill="review-comments", target="tools/thorny_loop")],
        )

        pairs = {(request.skill, request.target) for request in requests}
        self.assertIn(("review-comments", "tools/thorny_loop"), pairs)


if __name__ == "__main__":
    unittest.main()
