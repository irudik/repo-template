"""Deterministic failure extraction for verification steps."""

from __future__ import annotations

import os
import re

from .schemas import FailureSignature
from .util import trim_text


ERROR_LINE_PATTERNS = (
    re.compile(r"^make: \*\*\* .*", re.IGNORECASE),
    re.compile(r"^error: .*", re.IGNORECASE),
    re.compile(r"^fatal: .*", re.IGNORECASE),
    re.compile(r"^traceback .*", re.IGNORECASE),
    re.compile(r"^julia> .*", re.IGNORECASE),
    re.compile(r"^! .*", re.IGNORECASE),
    re.compile(r"undefined control sequence", re.IGNORECASE),
    re.compile(r"l\.\d+", re.IGNORECASE),
)


def _normalize_line(line: str) -> str:
    normalized = os.fspath(line).strip().lower()
    normalized = re.sub(r"/[^ \t:]+", "<path>", normalized)
    normalized = re.sub(r"line \d+", "line <n>", normalized)
    normalized = re.sub(r"\b\d+\b", "<n>", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def _pick_error_line(stdout: str, stderr: str) -> str:
    merged_lines = [line for line in (stderr.splitlines() + stdout.splitlines()) if line.strip()]
    for line in merged_lines:
        if any(pattern.search(line) for pattern in ERROR_LINE_PATTERNS):
            return line.strip()
    return merged_lines[-1].strip() if merged_lines else ""


def build_failure_signature(
    command: str,
    exit_code: int,
    stdout: str,
    stderr: str,
    *,
    max_chars: int = 2000,
) -> FailureSignature:
    """Create a normalized failure signature for loop control and planner context."""

    error_line = _pick_error_line(stdout, stderr)
    normalized_signature = _normalize_line(error_line or f"{command} exit {exit_code}")
    merged = "\n".join([part for part in (stderr.strip(), stdout.strip()) if part])
    relevant_tail = trim_text(merged, max_chars=max_chars)
    return FailureSignature(
        command=command,
        exit_code=exit_code,
        normalized_signature=normalized_signature,
        first_error_line=error_line,
        relevant_tail=relevant_tail,
    )
