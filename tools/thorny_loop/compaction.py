"""Context-budget helpers used before planner calls."""

from __future__ import annotations

from dataclasses import dataclass

from .util import trim_text


@dataclass(frozen=True)
class ContextSection:
    """A named context section with a priority for budget trimming."""

    name: str
    text: str
    priority: int


def estimate_tokens(text: str) -> int:
    """Use a conservative character heuristic for token budgeting."""

    return max(1, len(text) // 4)


def fit_sections_to_budget(sections: list[ContextSection], *, budget_tokens: int) -> str:
    """Keep higher-priority sections intact while trimming low-priority context first."""

    ordered = sorted(sections, key=lambda section: section.priority)
    included: list[str] = []
    running_tokens = 0
    for section in ordered:
        section_block = f"## {section.name}\n{section.text.strip()}\n"
        section_tokens = estimate_tokens(section_block)
        if running_tokens + section_tokens <= budget_tokens:
            included.append(section_block)
            running_tokens += section_tokens
            continue
        remaining_chars = max((budget_tokens - running_tokens) * 4, 0)
        if remaining_chars < 120:
            continue
        trimmed_block = f"## {section.name}\n{trim_text(section.text.strip(), max_chars=remaining_chars)}\n"
        included.append(trimmed_block)
        break
    return "\n".join(included).strip()
