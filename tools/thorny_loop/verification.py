"""Verification command selection and execution."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import ThornyConfig
from .failure_signatures import build_failure_signature
from .schemas import FailureSignature
from .util import command_is_blocked


@dataclass
class VerificationStepResult:
    """Result from a single verification command."""

    command: str
    exit_code: int
    stdout: str
    stderr: str
    failure_signature: FailureSignature | None


def select_verification_commands(config: ThornyConfig, changed_paths: list[str]) -> list[str]:
    """Choose verification commands using the repo's Make-first philosophy."""

    if config.explicit_verify_commands:
        return list(config.explicit_verify_commands)

    commands: list[str] = ["make -n"]
    touches_code = any(path == "code" or path.startswith("code/") for path in changed_paths)
    touches_latex = any(path == "latex" or path.startswith("latex/") for path in changed_paths)

    code_dirs = sorted(
        {
            "/".join(path.split("/")[:2]) if len(path.split("/")) >= 2 else "code"
            for path in changed_paths
            if path == "code" or path.startswith("code/")
        }
    )
    if touches_code:
        if code_dirs:
            commands.extend(f"make -C {code_dir}" for code_dir in code_dirs)
        else:
            commands.append("make -C code")
    if touches_latex:
        commands.append("make -C latex")
    if touches_code and touches_latex:
        commands.append("make")
    return commands


def run_verification_commands(
    repo_root: Path,
    commands: list[str],
    *,
    round_index: int,
    run_dir: Path,
    max_log_chars: int,
) -> list[VerificationStepResult]:
    """Run verification commands sequentially and save round logs."""

    stdout_log = run_dir / f"verify_round_{round_index:02d}_stdout.log"
    stderr_log = run_dir / f"verify_round_{round_index:02d}_stderr.log"
    results: list[VerificationStepResult] = []
    stdout_parts: list[str] = []
    stderr_parts: list[str] = []

    for command in commands:
        if command_is_blocked(command):
            raise ValueError(f"Blocked destructive verification command: {command}")
        completed = subprocess.run(
            command,
            cwd=repo_root,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
        )
        stdout_parts.append(f"$ {command}\n{completed.stdout}")
        stderr_parts.append(f"$ {command}\n{completed.stderr}")
        failure_signature = None
        if completed.returncode != 0:
            failure_signature = build_failure_signature(
                command,
                completed.returncode,
                completed.stdout,
                completed.stderr,
                max_chars=max_log_chars,
            )
        results.append(
            VerificationStepResult(
                command=command,
                exit_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                failure_signature=failure_signature,
            )
        )

    stdout_log.write_text("\n\n".join(stdout_parts))
    stderr_log.write_text("\n\n".join(stderr_parts))
    return results
