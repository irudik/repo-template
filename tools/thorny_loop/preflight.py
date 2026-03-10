"""Preflight checks for the thorny-loop workflow."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import ThornyConfig


@dataclass
class PreflightCheck:
    """One preflight check result."""

    name: str
    status: str
    detail: str


REQUIRED_DEPENDENCIES = ("openai", "agents", "dotenv", "pydantic")


def _git_status_summary(repo_root: Path) -> tuple[bool, str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    dirty = bool(result.stdout.strip())
    detail = "Working tree clean" if not dirty else "Uncommitted changes detected"
    return dirty, detail


def run_preflight(config: ThornyConfig) -> list[PreflightCheck]:
    """Run non-destructive environment checks before a thorny-loop run."""

    checks: list[PreflightCheck] = []
    repo_root = config.repo_root

    checks.append(
        PreflightCheck(
            name="repo_root",
            status="pass" if (repo_root / "AGENTS.md").exists() else "fail",
            detail=str(repo_root),
        )
    )

    api_key_present = bool(__import__("os").getenv("OPENAI_API_KEY"))
    checks.append(
        PreflightCheck(
            name="openai_api_key",
            status="pass" if api_key_present else "warn",
            detail="OPENAI_API_KEY present" if api_key_present else "OPENAI_API_KEY missing",
        )
    )

    missing_deps = [
        dependency
        for dependency in REQUIRED_DEPENDENCIES
        if importlib.util.find_spec(dependency) is None
    ]
    checks.append(
        PreflightCheck(
            name="python_dependencies",
            status="pass" if not missing_deps else "fail",
            detail="All required packages installed"
            if not missing_deps
            else f"Missing packages: {', '.join(missing_deps)}",
        )
    )

    codex_found = shutil.which(config.codex_mcp_command)
    npx_found = shutil.which("npx")
    node_found = shutil.which("node")
    if codex_found:
        status = "pass"
        detail = f"Using {config.codex_mcp_command}"
    elif npx_found and node_found:
        status = "warn"
        detail = "Falling back to npx codex mcp-server"
    else:
        status = "fail"
        detail = "Neither codex nor npx/node are available"
    checks.append(PreflightCheck(name="codex_mcp", status=status, detail=detail))

    dirty, detail = _git_status_summary(repo_root)
    checks.append(
        PreflightCheck(
            name="working_tree",
            status="warn" if dirty else "pass",
            detail=detail,
        )
    )
    return checks
