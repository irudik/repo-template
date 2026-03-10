"""Shared utility helpers for the thorny-loop package."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterable


REPO_SENTINELS = ("AGENTS.md", "Makefile", "README.md")
DESTRUCTIVE_TOKENS = {
    "git reset --hard",
    "git clean -fd",
    "git clean -xdf",
    "rm -rf /",
    "rm -rf .git",
    "git checkout --",
    "git branch -D",
    "git push",
    "git commit",
}


def find_repo_root(start: Path | None = None) -> Path:
    """Return the nearest parent directory that looks like the repo root."""

    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if all((candidate / sentinel).exists() for sentinel in REPO_SENTINELS):
            return candidate
    raise FileNotFoundError("Could not locate repository root from current path.")


def slugify(text: str, *, limit: int = 48) -> str:
    """Create a filesystem-safe slug while preserving enough task detail."""

    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", text.strip().lower()).strip("-")
    if not cleaned:
        cleaned = "thorny-loop"
    return cleaned[:limit].rstrip("-")


def ensure_path_within_repo(repo_root: Path, candidate: Path) -> Path:
    """Resolve a path and reject anything outside the repository root."""

    resolved = candidate.resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"Path escapes repository root: {candidate}") from exc
    return resolved


def normalize_scope_paths(repo_root: Path, raw_paths: Iterable[str] | None) -> list[str]:
    """Normalize user-provided scope paths relative to the repository root."""

    normalized: list[str] = []
    if not raw_paths:
        return normalized
    for raw_path in raw_paths:
        raw_path = raw_path.strip()
        if not raw_path:
            continue
        safe_path = ensure_path_within_repo(repo_root, repo_root / raw_path)
        normalized.append(os.fspath(safe_path.relative_to(repo_root)))
    return sorted(dict.fromkeys(normalized))


def split_shell_like_list(raw_value: str | None) -> list[str]:
    """Split a space-delimited string into clean tokens without shell parsing."""

    if not raw_value:
        return []
    return [part for part in re.split(r"[\s,]+", raw_value.strip()) if part]


def trim_text(text: str, *, max_chars: int) -> str:
    """Trim text conservatively while keeping failure suffixes visible."""

    if len(text) <= max_chars:
        return text
    if max_chars < 32:
        return text[:max_chars]
    head = max_chars // 2
    tail = max_chars - head - len("\n...\n")
    return f"{text[:head]}\n...\n{text[-tail:]}"


def command_is_blocked(command: str) -> bool:
    """Return True when the command matches an explicitly blocked destructive token."""

    compact = " ".join(command.split())
    return any(token in compact for token in DESTRUCTIVE_TOKENS)
