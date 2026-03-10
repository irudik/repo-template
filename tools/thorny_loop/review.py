"""Review skill selection and Codex-driven execution helpers."""

from __future__ import annotations

import shutil
from pathlib import Path

from .schemas import ReviewRequest


def _deduplicate_review_requests(review_requests: list[ReviewRequest]) -> list[ReviewRequest]:
    """Keep review requests stable while removing duplicates."""

    unique: dict[tuple[str, str], ReviewRequest] = {}
    for review_request in review_requests:
        unique[(review_request.skill, review_request.target)] = review_request
    return list(unique.values())


def map_changed_files_to_reviews(changed_files: list[str]) -> list[ReviewRequest]:
    """Map changed files to the repo's existing review skills."""

    review_requests: list[ReviewRequest] = []
    for changed_file in changed_files:
        if changed_file.endswith(".R"):
            review_requests.append(ReviewRequest(skill="review-r", target=changed_file))
        elif changed_file.endswith(".jl"):
            review_requests.append(ReviewRequest(skill="review-julia", target=changed_file))
        elif changed_file.endswith(".tex"):
            review_requests.append(ReviewRequest(skill="review-tex", target=changed_file))
    return _deduplicate_review_requests(review_requests)


def collect_review_requests(
    changed_files: list[str],
    planned_review_requests: list[ReviewRequest],
) -> list[ReviewRequest]:
    """Combine automatic language reviews with planner-requested reviews."""

    return _deduplicate_review_requests(
        [
            *map_changed_files_to_reviews(changed_files),
            *planned_review_requests,
        ]
    )


def build_review_prompt(review_request: ReviewRequest, run_dir: Path) -> str:
    """Tell Codex to invoke the existing repo skill and keep the report on disk."""

    return (
        f"Use the repo skill `{review_request.skill}` on `{review_request.target}`.\n"
        "Do not edit source files in this review step.\n"
        "Save the normal review artifact in the repo's standard location, then summarize the result.\n"
        f"Also mention that this thorny-loop run directory is `{run_dir.relative_to(run_dir.parents[2]).as_posix()}`."
    )


def collect_review_artifacts(repo_root: Path, run_reviews_dir: Path) -> list[str]:
    """Copy the newest review reports into the run-local reviews directory."""

    run_reviews_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for review_path in sorted((repo_root / "quality_reports").glob("*_review.md")):
        destination = run_reviews_dir / review_path.name
        shutil.copy2(review_path, destination)
        copied.append(destination.relative_to(repo_root).as_posix())
    return copied
