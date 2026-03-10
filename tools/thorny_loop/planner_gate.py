"""Planner gating rules for the sparse thorny-loop workflow."""

from __future__ import annotations

from collections.abc import Sequence

from .schemas import FailureSignature


FORCE_KEYWORDS = (
    "thorny",
    "gpt pro",
    "gpt-pro",
    "planner-coder",
    "deep loop",
    "planner loop",
)
RISK_KEYWORDS = (
    "econometric",
    "simulation",
    "manuscript",
    "claim",
    "numbers disagree",
    "output mismatch",
)


def _scope_is_cross_cutting(scope_paths: Sequence[str]) -> bool:
    top_levels = {path.split("/", 1)[0] for path in scope_paths if path}
    touches_code = any(path == "code" or path.startswith("code/") for path in scope_paths)
    touches_latex = any(path == "latex" or path.startswith("latex/") for path in scope_paths)
    return len(top_levels) > 1 or (touches_code and touches_latex)


def should_call_planner(
    task: str,
    scope_paths: Sequence[str],
    *,
    iteration_index: int,
    failure_history: Sequence[FailureSignature] | None = None,
    root_cause_unclear: bool = False,
    final_review: bool = False,
) -> tuple[bool, str]:
    """Return whether the planner should be called and why."""

    lowered_task = task.lower()
    failures = list(failure_history or [])

    if final_review:
        return True, "final_review"
    if any(keyword in lowered_task for keyword in FORCE_KEYWORDS):
        return True, "initial"
    if _scope_is_cross_cutting(scope_paths):
        return True, "cross_cutting"
    if iteration_index == 0 and any(keyword in lowered_task for keyword in RISK_KEYWORDS):
        return True, "initial"
    if root_cause_unclear and iteration_index >= 1:
        return True, "stalled"
    if len(failures) >= 2 and failures[-1].normalized_signature == failures[-2].normalized_signature:
        return True, "stalled"
    return False, "initial"
