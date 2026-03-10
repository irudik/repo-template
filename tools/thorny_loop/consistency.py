"""Research-specific consistency helpers for code/output/manuscript coordination."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .util import trim_text


INPUT_PATTERN = re.compile(r"\\input\{([^}]+)\}")
GRAPHICS_PATTERN = re.compile(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}")


@dataclass
class ConsistencyFinding:
    """Describe manuscript coupling that may require planner visibility."""

    risky: bool
    referenced_outputs: list[str]
    manuscript_excerpt: str


def _candidate_outputs(reference: str) -> list[str]:
    if reference.startswith("output/"):
        return [reference]
    candidates: list[str] = []
    if reference.endswith(".txt"):
        candidates.append(f"output/numbers/{reference}")
    if reference.endswith(".pdf") or reference.endswith(".png"):
        candidates.append(f"output/figures/{reference}")
    if reference.endswith(".tex") or reference.endswith(".csv"):
        candidates.append(f"output/tables/{reference}")
    return candidates or [reference]


def scan_manuscript_for_outputs(repo_root: Path) -> dict[str, list[int]]:
    """Map manuscript output references to line numbers."""

    manuscript_path = repo_root / "latex" / "manuscript.tex"
    if not manuscript_path.exists():
        return {}
    references: dict[str, list[int]] = {}
    for line_number, line in enumerate(manuscript_path.read_text().splitlines(), start=1):
        matches = INPUT_PATTERN.findall(line) + GRAPHICS_PATTERN.findall(line)
        for match in matches:
            for candidate in _candidate_outputs(match):
                references.setdefault(candidate, []).append(line_number)
    return references


def detect_consistency_risk(repo_root: Path, changed_paths: list[str], task: str) -> ConsistencyFinding:
    """Detect when code/output changes may alter manuscript-facing claims."""

    touches_code = any(path == "code" or path.startswith("code/") for path in changed_paths)
    touches_outputs = any(path == "output" or path.startswith("output/") for path in changed_paths)
    references = scan_manuscript_for_outputs(repo_root)
    risky_task = any(
        keyword in task.lower()
        for keyword in ("manuscript", "claim", "numbers disagree", "output mismatch", "simulation")
    )
    risky = bool(references) and (touches_code or touches_outputs or risky_task)
    if not risky:
        return ConsistencyFinding(risky=False, referenced_outputs=[], manuscript_excerpt="")

    manuscript_path = repo_root / "latex" / "manuscript.tex"
    manuscript_text = manuscript_path.read_text() if manuscript_path.exists() else ""
    excerpt = trim_text(manuscript_text, max_chars=2500)
    return ConsistencyFinding(
        risky=True,
        referenced_outputs=sorted(references.keys()),
        manuscript_excerpt=excerpt,
    )
