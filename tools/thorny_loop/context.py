"""Context assembly for planner calls."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .compaction import ContextSection, fit_sections_to_budget
from .config import ThornyConfig
from .consistency import detect_consistency_risk
from .schemas import ContextManifest, FailureSignature
from .util import trim_text


def _read_trimmed(path: Path, *, max_chars: int) -> str:
    if not path.exists():
        return ""
    return trim_text(path.read_text(), max_chars=max_chars)


def _git_output(repo_root: Path, args: list[str], *, max_chars: int) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    merged = "\n".join(part for part in (result.stdout, result.stderr) if part)
    return trim_text(merged, max_chars=max_chars)


def _latest_matching_files(root: Path, pattern: str, *, limit: int = 3) -> list[Path]:
    candidates = sorted(root.glob(pattern), key=lambda path: path.stat().st_mtime, reverse=True)
    return candidates[:limit]


def build_context_bundle(
    config: ThornyConfig,
    *,
    changed_paths: list[str],
    failure_signature: FailureSignature | None,
    state_summary: str,
) -> tuple[str, ContextManifest]:
    """Build a token-aware planner context bundle from the relevant repo surface."""

    repo_root = config.repo_root
    manifest = ContextManifest(task=config.task, scope_paths=list(config.scope_paths))
    sections: list[ContextSection] = []

    def add_file_section(name: str, path: Path, priority: int, max_chars: int = 2200) -> None:
        text = _read_trimmed(path, max_chars=max_chars)
        if text:
            sections.append(ContextSection(name=name, text=text, priority=priority))
            manifest.included_files.append(path.relative_to(repo_root).as_posix())

    add_file_section("Root AGENTS", repo_root / "AGENTS.md", 1, max_chars=4500)
    add_file_section("Project Memory", repo_root / "MEMORY.md", 2, max_chars=1400)
    add_file_section("Root Makefile", repo_root / "Makefile", 2, max_chars=1400)

    if any(path == "code" or path.startswith("code/") for path in config.scope_paths + changed_paths):
        add_file_section("Code AGENTS", repo_root / "code" / "AGENTS.md", 2, max_chars=2200)
        add_file_section("Code Makefile", repo_root / "code" / "Makefile", 3, max_chars=1400)

    if any(path == "latex" or path.startswith("latex/") for path in config.scope_paths + changed_paths):
        add_file_section("LaTeX AGENTS", repo_root / "latex" / "AGENTS.md", 2, max_chars=2200)
        add_file_section("LaTeX Makefile", repo_root / "latex" / "Makefile", 3, max_chars=1400)

    sections.append(
        ContextSection(
            name="Task",
            text=config.task,
            priority=1,
        )
    )
    sections.append(
        ContextSection(
            name="Rolling State Summary",
            text=state_summary.strip() or "No prior state summary available.",
            priority=1,
        )
    )
    sections.append(
        ContextSection(
            name="Git Status",
            text=_git_output(repo_root, ["status", "--short"], max_chars=1200) or "Working tree clean.",
            priority=1,
        )
    )
    sections.append(
        ContextSection(
            name="Git Diff",
            text=_git_output(repo_root, ["diff", "--unified=3"], max_chars=config.max_diff_chars),
            priority=2,
        )
    )

    if failure_signature is not None:
        sections.append(
            ContextSection(
                name="Latest Failure Signature",
                text=(
                    f"Command: {failure_signature.command}\n"
                    f"Exit code: {failure_signature.exit_code}\n"
                    f"Signature: {failure_signature.normalized_signature}\n"
                    f"First error line: {failure_signature.first_error_line}\n"
                    f"{failure_signature.relevant_tail}"
                ),
                priority=1,
            )
        )

    consistency = detect_consistency_risk(repo_root, changed_paths or config.scope_paths, config.task)
    if consistency.risky:
        sections.append(
            ContextSection(
                name="Manuscript Coupling",
                text=(
                    "Referenced outputs:\n"
                    + "\n".join(f"- {path}" for path in consistency.referenced_outputs[:20])
                    + "\n\n"
                    + consistency.manuscript_excerpt
                ),
                priority=2,
            )
        )
        manifest.notes.append("Code/output changes may affect manuscript-facing claims.")

    latest_logs = _latest_matching_files(
        repo_root / "quality_reports",
        "**/verify_round_*_stderr.log",
        limit=2,
    )
    for log_path in latest_logs:
        text = _read_trimmed(log_path, max_chars=1800)
        if text:
            sections.append(
                ContextSection(
                    name=f"Recent Verification Log: {log_path.name}",
                    text=text,
                    priority=4,
                )
            )
            manifest.included_logs.append(log_path.relative_to(repo_root).as_posix())

    for changed_path in changed_paths[:3]:
        candidate = repo_root / changed_path
        if candidate.is_file():
            add_file_section(f"Scoped File: {changed_path}", candidate, 3, max_chars=1800)

    latest_reviews = _latest_matching_files(repo_root / "quality_reports", "*_review.md", limit=3)
    for review_path in latest_reviews:
        text = _read_trimmed(review_path, max_chars=1600)
        if text:
            sections.append(
                ContextSection(
                    name=f"Recent Review: {review_path.name}",
                    text=text,
                    priority=5,
                )
            )
            manifest.included_reviews.append(review_path.relative_to(repo_root).as_posix())

    context_text = fit_sections_to_budget(sections, budget_tokens=config.context_budget_tokens)
    return context_text, manifest
