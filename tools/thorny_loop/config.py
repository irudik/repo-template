"""Configuration loading for the thorny-loop command surface."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator, model_validator

from .util import find_repo_root, normalize_scope_paths, split_shell_like_list


class ThornyConfig(BaseModel):
    """Merged CLI/environment configuration for one thorny-loop run."""

    repo_root: Path
    task: str = ""
    scope_paths: list[str] = Field(default_factory=list)
    explicit_verify_commands: list[str] = Field(default_factory=list)
    verify_target: str = ""
    planner_model: str = "gpt-5.4-pro"
    planner_effort_default: str = "medium"
    planner_effort_escalated: str = "high"
    max_planner_calls: int = 2
    hard_max_planner_calls: int = 3
    coder_steps_per_plan: int = 2
    hard_max_coder_turns: int = 6
    planner_max_output_tokens: int = 1800
    context_budget_tokens: int = 7000
    max_log_chars: int = 12000
    max_diff_chars: int = 12000
    quality_gate_target: int = 90
    background_planner: str = "auto"
    use_previous_response_id: bool = False
    dry_run: bool = False
    resume_run_id: str = ""
    report_run_id: str = ""
    codex_mcp_command: str = "codex"
    codex_mcp_args: list[str] = Field(default_factory=lambda: ["mcp-server"])

    @field_validator("planner_effort_default", "planner_effort_escalated")
    @classmethod
    def validate_effort(cls, value: str) -> str:
        """Keep effort levels within the intended sparse-planner settings."""

        allowed = {"medium", "high", "xhigh"}
        if value not in allowed:
            raise ValueError(f"Unsupported planner effort: {value}")
        return value

    @field_validator("quality_gate_target")
    @classmethod
    def validate_quality_gate(cls, value: int) -> int:
        """Restrict quality gates to the documented repo thresholds."""

        allowed = {80, 90, 95}
        if value not in allowed:
            raise ValueError(f"Quality gate must be one of {sorted(allowed)}")
        return value

    @model_validator(mode="after")
    def validate_task_requirement(self) -> "ThornyConfig":
        """Require a task only for fresh runs."""

        if not self.task and not self.resume_run_id and not self.report_run_id:
            raise ValueError("A task is required unless --resume or --report is used.")
        return self


def build_parser() -> argparse.ArgumentParser:
    """Build the thorny-loop CLI parser."""

    parser = argparse.ArgumentParser(description="Sparse GPT Pro planner + Codex thorny loop")
    parser.add_argument("--task", default="", help="Task description for the thorny loop")
    parser.add_argument(
        "--scope",
        nargs="*",
        default=None,
        help="Optional repo-relative scope paths",
    )
    parser.add_argument(
        "--verify",
        action="append",
        default=None,
        help="Explicit verification command (repeatable)",
    )
    parser.add_argument("--verify-target", default="", help="Optional named verify target")
    parser.add_argument("--max-planner-calls", type=int, default=None)
    parser.add_argument("--max-coder-turns", type=int, default=None)
    parser.add_argument("--planner-effort", default=None)
    parser.add_argument("--quality-gate", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", default="", help="Resume an existing run ID")
    parser.add_argument("--report", default="", help="Print a final report for an existing run ID")
    return parser


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def _background_setting_from_env() -> str:
    """Resolve planner background mode with legacy opt-out taking precedence."""

    legacy_value = os.getenv("THORNY_USE_BACKGROUND")
    configured_value = os.getenv("THORNY_BACKGROUND_PLANNER")

    if legacy_value is not None:
        normalized_legacy = legacy_value.strip().lower()
        if normalized_legacy in {"0", "false", "no", "off"}:
            return "never"
        if normalized_legacy in {"1", "true", "yes", "on"}:
            return configured_value or "always"

    return configured_value or "never"


def load_config(args: argparse.Namespace, *, repo_root: Path | None = None) -> ThornyConfig:
    """Load environment variables and CLI overrides into a validated config."""

    resolved_repo_root = repo_root or find_repo_root()
    load_dotenv(resolved_repo_root / ".env", override=False)

    scope_paths = normalize_scope_paths(
        resolved_repo_root,
        args.scope if args.scope is not None else split_shell_like_list(os.getenv("SCOPE")),
    )

    explicit_verify_commands = args.verify or []
    if not explicit_verify_commands and os.getenv("VERIFY"):
        explicit_verify_commands = [os.getenv("VERIFY", "")]

    planner_effort_default = os.getenv(
        "THORNY_PLANNER_EFFORT_DEFAULT",
        os.getenv("THORNY_PLANNER_REASONING_EFFORT", "medium"),
    )
    planner_effort_escalated = os.getenv("THORNY_PLANNER_EFFORT_ESCALATED", "high")
    if args.planner_effort:
        planner_effort_default = args.planner_effort

    hard_max_coder_turns = _env_int("THORNY_HARD_MAX_CODER_TURNS", 6)

    config = ThornyConfig(
        repo_root=resolved_repo_root,
        task=args.task or os.getenv("TASK", ""),
        scope_paths=scope_paths,
        explicit_verify_commands=explicit_verify_commands,
        verify_target=args.verify_target or os.getenv("VERIFY_TARGET", ""),
        planner_model=os.getenv("THORNY_PLANNER_MODEL", "gpt-5.4-pro"),
        planner_effort_default=planner_effort_default,
        planner_effort_escalated=planner_effort_escalated,
        max_planner_calls=args.max_planner_calls
        if args.max_planner_calls is not None
        else _env_int("THORNY_MAX_PLANNER_CALLS", 2),
        hard_max_planner_calls=_env_int("THORNY_HARD_MAX_PLANNER_CALLS", 3),
        coder_steps_per_plan=_env_int("THORNY_CODER_STEPS_PER_PLAN", 2),
        hard_max_coder_turns=args.max_coder_turns
        if args.max_coder_turns is not None
        else hard_max_coder_turns,
        planner_max_output_tokens=_env_int("THORNY_PLANNER_MAX_OUTPUT_TOKENS", 1800),
        context_budget_tokens=_env_int("THORNY_CONTEXT_BUDGET_TOKENS", 7000),
        max_log_chars=_env_int("THORNY_MAX_LOG_CHARS", 12000),
        max_diff_chars=_env_int("THORNY_MAX_DIFF_CHARS", 12000),
        quality_gate_target=args.quality_gate
        if args.quality_gate is not None
        else _env_int("THORNY_DEFAULT_QUALITY_GATE", 90),
        background_planner=_background_setting_from_env(),
        use_previous_response_id=os.getenv("THORNY_USE_PREVIOUS_RESPONSE_ID", "0") == "1",
        dry_run=args.dry_run,
        resume_run_id=args.resume,
        report_run_id=args.report,
        codex_mcp_command=os.getenv("THORNY_Codex_MCP_COMMAND", "codex"),
        codex_mcp_args=split_shell_like_list(os.getenv("THORNY_Codex_MCP_ARGS", "mcp-server")),
    )
    return config
