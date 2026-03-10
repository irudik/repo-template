"""CLI entrypoint for the sparse thorny-loop workflow."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _bootstrap_repo_path() -> None:
    repo_root = _repo_root()
    repo_root_str = os.fspath(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)


def _try_reexec_with_local_venv() -> None:
    if os.getenv("_THORNY_BOOTSTRAPPED") == "1":
        return
    repo_root = _repo_root()
    for candidate in (repo_root / ".venv-thorny" / "bin" / "python", repo_root / ".venv" / "bin" / "python"):
        if candidate.exists():
            env = os.environ.copy()
            env["_THORNY_BOOTSTRAPPED"] = "1"
            os.execve(os.fspath(candidate), [os.fspath(candidate), os.fspath(Path(__file__).resolve()), *sys.argv[1:]], env)


def main() -> int:
    _bootstrap_repo_path()
    try:
        from tools.thorny_loop.loop import run_cli
    except ModuleNotFoundError:
        _try_reexec_with_local_venv()
        raise
    return run_cli()


if __name__ == "__main__":
    raise SystemExit(main())
