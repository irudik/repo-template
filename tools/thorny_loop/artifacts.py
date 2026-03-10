"""Run-directory and artifact path helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .schemas import RunManifest
from .util import slugify


@dataclass(frozen=True)
class RunPaths:
    """Canonical paths used throughout a thorny-loop run."""

    run_id: str
    run_dir: Path
    reviews_dir: Path
    baseline_snapshot_file: Path
    task_file: Path
    context_manifest_file: Path
    state_summary_file: Path
    final_summary_file: Path
    manifest_file: Path


def make_run_id(task: str, *, now: datetime | None = None) -> str:
    """Create a stable run identifier from timestamp and task slug."""

    timestamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{slugify(task)}"


def build_run_paths(repo_root: Path, run_id: str) -> RunPaths:
    """Return the canonical run directory layout for a given run ID."""

    run_dir = repo_root / "quality_reports" / "thorny_loop" / run_id
    return RunPaths(
        run_id=run_id,
        run_dir=run_dir,
        reviews_dir=run_dir / "reviews",
        baseline_snapshot_file=run_dir / "baseline_worktree_snapshot.json",
        task_file=run_dir / "task.md",
        context_manifest_file=run_dir / "context_manifest.json",
        state_summary_file=run_dir / "state_summary.md",
        final_summary_file=run_dir / "final_summary.md",
        manifest_file=run_dir / "manifest.json",
    )


def ensure_run_directories(run_paths: RunPaths) -> None:
    """Create the canonical run directory structure."""

    run_paths.run_dir.mkdir(parents=True, exist_ok=True)
    run_paths.reviews_dir.mkdir(parents=True, exist_ok=True)


def save_manifest(run_paths: RunPaths, manifest: RunManifest) -> None:
    """Persist the current run manifest."""

    run_paths.manifest_file.write_text(json.dumps(manifest.model_dump(), indent=2, sort_keys=True))


def load_manifest(run_paths: RunPaths) -> RunManifest | None:
    """Load an existing run manifest when resuming or reporting."""

    if not run_paths.manifest_file.exists():
        return None
    return RunManifest.model_validate_json(run_paths.manifest_file.read_text())
