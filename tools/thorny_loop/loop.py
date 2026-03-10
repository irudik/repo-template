"""Main orchestration loop for sparse thorny problems."""

from __future__ import annotations

import asyncio
import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .artifacts import RunPaths, build_run_paths, ensure_run_directories, load_manifest, make_run_id, save_manifest
from .codex_session import CodexSession
from .config import ThornyConfig, build_parser, load_config
from .context import build_context_bundle
from .planner import PlannerParseError, PlannerResponse, call_planner
from .planner_gate import should_call_planner
from .preflight import run_preflight
from .review import build_review_prompt, collect_review_artifacts, collect_review_requests
from .schemas import NextIncrement, PlannerDecision, RunManifest
from .verification import run_verification_commands, select_verification_commands


@dataclass
class ProgressSignals:
    """Signals used to halt unproductive loops."""

    no_progress: bool
    reasons: list[str]


def detect_no_progress(
    *,
    previous_diff: str,
    current_diff: str,
    previous_signature: str,
    current_signature: str,
    previous_objective: str,
    current_objective: str,
    changed_files: list[str],
) -> ProgressSignals:
    """Detect repeated failure patterns before the loop burns more planner budget."""

    reasons: list[str] = []
    if not changed_files:
        reasons.append("zero_file_changes_after_coder_turn")
    if previous_diff and current_diff and previous_diff.strip() == current_diff.strip():
        reasons.append("identical_diff_across_turns")
    if previous_signature and current_signature and previous_signature == current_signature:
        reasons.append("same_failure_signature_twice")
    if previous_objective and current_objective and previous_objective.strip() == current_objective.strip():
        reasons.append("planner_repeated_same_increment")
    return ProgressSignals(no_progress=bool(reasons), reasons=reasons)


def _current_changed_files(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _untracked_files(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture_worktree_snapshot(repo_root: Path) -> dict[str, dict[str, str]]:
    """Capture the current dirty worktree state so run-local edits can be isolated."""

    snapshot: dict[str, dict[str, str]] = {}
    for relative_path in _current_changed_files(repo_root):
        diff_result = subprocess.run(
            ["git", "diff", "--no-ext-diff", "--", relative_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        snapshot[relative_path] = {
            "kind": "tracked",
            "fingerprint": _sha256_text(diff_result.stdout),
        }

    for relative_path in _untracked_files(repo_root):
        file_path = repo_root / relative_path
        if not file_path.is_file():
            continue
        snapshot[relative_path] = {
            "kind": "untracked",
            "fingerprint": _sha256_file(file_path),
        }
    return snapshot


def diff_snapshot_paths(
    baseline_snapshot: dict[str, dict[str, str]],
    current_snapshot: dict[str, dict[str, str]],
) -> list[str]:
    """Return only paths whose dirty state changed since the run baseline."""

    changed_paths = {
        path
        for path in set(baseline_snapshot) | set(current_snapshot)
        if baseline_snapshot.get(path) != current_snapshot.get(path)
    }
    return sorted(changed_paths)


def _current_diff(repo_root: Path, max_chars: int) -> str:
    result = subprocess.run(
        ["git", "diff", "--unified=3"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    diff_text = result.stdout.strip()
    return diff_text[:max_chars]


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _write_json(path: Path, payload: dict) -> None:
    _write_text(path, json.dumps(payload, indent=2, sort_keys=True))


def _synthetic_decision(config: ThornyConfig, changed_paths: list[str], why_called: str) -> PlannerDecision:
    verification_commands = select_verification_commands(config, changed_paths or config.scope_paths)
    return PlannerDecision(
        status="continue",
        why_called=why_called,
        diagnosis="Planner gate skipped the external planner, so execute the task directly with a minimal increment.",
        risk_flags=[],
        next_increment=NextIncrement(
            objective=config.task,
            files_to_touch=list(changed_paths or config.scope_paths),
            constraints=[
                "Respect root and touched-path AGENTS instructions.",
                "Make the smallest workable edit.",
                "Do not commit, push, or create branches.",
            ],
            verification_commands=verification_commands,
            review_requests=[],
            acceptance_criteria=["Selected verification commands pass."],
        ),
        questions_for_user=[],
        stop_if=["No progress is detected twice."],
    )


def _save_planner_response(run_paths: RunPaths, planner_calls: int, response: PlannerResponse) -> None:
    _write_text(
        run_paths.run_dir / f"planner_call_{planner_calls:02d}_raw.md",
        response.raw_output,
    )
    _write_json(
        run_paths.run_dir / f"planner_call_{planner_calls:02d}.json",
        response.decision.model_dump(),
    )


def _build_coder_prompt(
    config: ThornyConfig,
    decision: PlannerDecision,
    *,
    failure_signature: str,
) -> str:
    file_scope = decision.next_increment.files_to_touch or config.scope_paths
    constraints = "\n".join(f"- {constraint}" for constraint in decision.next_increment.constraints)
    acceptance = "\n".join(f"- {criterion}" for criterion in decision.next_increment.acceptance_criteria)
    verification_commands = decision.next_increment.verification_commands or select_verification_commands(
        config,
        file_scope,
    )
    verify_block = "\n".join(f"- {command}" for command in verification_commands)
    return (
        f"Task: {config.task}\n\n"
        f"Current objective: {decision.next_increment.objective}\n"
        f"Allowed files to touch:\n" + "\n".join(f"- {path}" for path in file_scope) + "\n\n"
        f"Constraints:\n{constraints or '- None'}\n\n"
        f"Verification commands to satisfy:\n{verify_block}\n\n"
        f"Acceptance criteria:\n{acceptance or '- Verification passes'}\n\n"
        f"Latest failure signature:\n{failure_signature or 'None'}\n\n"
        "Respect the repo instructions and touched-path AGENTS files. "
        "Make the smallest reversible edit. Preserve style and Make conventions. "
        "Do not commit."
    )


def _final_summary_text(
    config: ThornyConfig,
    manifest: RunManifest,
    *,
    verification_results: list[str],
    open_issues: list[str],
) -> str:
    quality_reached = "reached" if manifest.status == "done" else "not reached"
    return (
        f"# Thorny Loop Final Summary\n\n"
        f"- Task: {config.task}\n"
        f"- Run id: {manifest.run_id}\n"
        f"- Planner model: {manifest.planner_model}\n"
        f"- Planner calls: {manifest.planner_calls}\n"
        f"- Coder turns: {manifest.coder_turns}\n"
        f"- Files changed: {', '.join(manifest.files_changed) or 'None'}\n"
        f"- Verification results: {', '.join(verification_results) or 'None'}\n"
        f"- Reviews run: {', '.join(manifest.reviews_run) or 'None'}\n"
        f"- Final status: {manifest.status}\n"
        f"- Quality gate {config.quality_gate_target}: {quality_reached}\n"
        f"- Planner estimated cost (USD): {manifest.usage_summary.estimated_cost_usd:.6f}\n"
        f"- Remaining open issues: {', '.join(open_issues) or 'None'}\n"
        f"- Recommended next action: {'Proceed with normal workflow.' if manifest.status == 'done' else 'Inspect the run directory and resolve the blocking issue.'}\n"
    )


def _load_or_create_run_paths(config: ThornyConfig) -> RunPaths:
    if config.resume_run_id or config.report_run_id:
        run_id = config.resume_run_id or config.report_run_id
    else:
        run_id = make_run_id(config.task)
    return build_run_paths(config.repo_root, run_id)


def _write_task_file(config: ThornyConfig, run_paths: RunPaths) -> None:
    _write_text(
        run_paths.task_file,
        "\n".join(
            [
                f"# Task",
                "",
                config.task,
                "",
                f"- Scope: {', '.join(config.scope_paths) or 'None'}",
                f"- Verify target: {config.verify_target or 'None'}",
                f"- Dry run: {int(config.dry_run)}",
            ]
        ),
    )


def _write_initial_plan_record(config: ThornyConfig, run_paths: RunPaths, decision: PlannerDecision) -> None:
    """Persist the first human-readable thorny-loop plan under quality_reports/plans."""

    plan_path = config.repo_root / "quality_reports" / "plans" / f"{run_paths.run_id}_thorny_loop.md"
    lines = [
        "# Thorny Loop Initial Plan",
        "",
        f"- Run ID: {run_paths.run_id}",
        f"- Task: {config.task}",
        f"- Planner model: {config.planner_model}",
        f"- Planner reason: {decision.why_called}",
        "",
        "## Diagnosis",
        decision.diagnosis,
        "",
        "## Next Increment",
        f"- Objective: {decision.next_increment.objective}",
        f"- Files to touch: {', '.join(decision.next_increment.files_to_touch) or 'None'}",
        f"- Constraints: {', '.join(decision.next_increment.constraints) or 'None'}",
        f"- Verification commands: {', '.join(decision.next_increment.verification_commands) or 'None'}",
        f"- Review requests: {', '.join(f'{request.skill}:{request.target}' for request in decision.next_increment.review_requests) or 'None'}",
        "",
        "## Stop Conditions",
    ]
    stop_conditions = decision.stop_if or ["No explicit stop conditions supplied."]
    lines.extend(f"- {condition}" for condition in stop_conditions)
    _write_text(plan_path, "\n".join(lines) + "\n")


def _print_summary(path: Path) -> int:
    if not path.exists():
        print(f"Missing report: {path}")
        return 1
    print(path.read_text())
    return 0


async def _run_cli_async(config: ThornyConfig, run_paths: RunPaths) -> int:
    """Run the thorny-loop flow while keeping the Codex session on one event loop."""

    if config.report_run_id:
        return _print_summary(run_paths.final_summary_file)

    ensure_run_directories(run_paths)
    existing_manifest = load_manifest(run_paths)
    if existing_manifest is not None and not config.task:
        config.task = existing_manifest.task
    if config.resume_run_id and existing_manifest is not None and existing_manifest.status in {"done", "blocked", "failed"}:
        return _print_summary(run_paths.final_summary_file)

    _write_task_file(config, run_paths)

    preflight_checks = run_preflight(config)
    state_summary = "No work performed yet."
    _write_text(run_paths.state_summary_file, state_summary)

    manifest = existing_manifest or RunManifest(
        run_id=run_paths.run_id,
        task=config.task,
        status="running",
        planner_model=config.planner_model,
    )
    save_manifest(run_paths, manifest)
    if run_paths.baseline_snapshot_file.exists():
        baseline_snapshot = json.loads(run_paths.baseline_snapshot_file.read_text())
    else:
        baseline_snapshot = capture_worktree_snapshot(config.repo_root)
        _write_json(run_paths.baseline_snapshot_file, baseline_snapshot)

    changed_paths = _current_changed_files(config.repo_root) or list(config.scope_paths)
    verification_commands = select_verification_commands(config, changed_paths)
    context_text, context_manifest = build_context_bundle(
        config,
        changed_paths=changed_paths,
        failure_signature=None,
        state_summary=state_summary,
    )
    _write_json(run_paths.context_manifest_file, context_manifest.model_dump())

    if config.dry_run:
        decision = _synthetic_decision(config, changed_paths, "initial")
        _write_initial_plan_record(config, run_paths, decision)
        summary_lines = [
            "# Thorny Loop Dry Run",
            "",
            f"- Task: {config.task}",
            f"- Run id: {run_paths.run_id}",
            f"- Preflight: {', '.join(f'{check.name}={check.status}' for check in preflight_checks)}",
            f"- Verification plan: {', '.join(verification_commands)}",
            f"- Context manifest: {run_paths.context_manifest_file.relative_to(config.repo_root).as_posix()}",
        ]
        _write_text(run_paths.final_summary_file, "\n".join(summary_lines) + "\n")
        manifest.status = "done"
        manifest.verify_steps = verification_commands
        save_manifest(run_paths, manifest)
        print(run_paths.final_summary_file.read_text())
        return 0

    planner_calls = manifest.planner_calls
    coder_turns = manifest.coder_turns
    previous_diff = ""
    previous_signature = ""
    previous_objective = ""
    failure_signature = None
    final_issues: list[str] = []

    use_planner, why_called = should_call_planner(
        config.task,
        config.scope_paths or changed_paths,
        iteration_index=planner_calls,
        failure_history=[],
    )

    decision = _synthetic_decision(config, changed_paths, why_called)
    if use_planner:
        try:
            planner_response = call_planner(
                config,
                task=config.task,
                context_text=context_text,
                why_called=why_called,
                effort=config.planner_effort_default,
                state_summary=state_summary,
            )
            planner_calls += 1
            manifest.planner_calls = planner_calls
            manifest.usage_summary = planner_response.usage_summary
            _save_planner_response(run_paths, planner_calls, planner_response)
            decision = planner_response.decision
        except (RuntimeError, PlannerParseError) as exc:
            final_issues.append(str(exc))
            if isinstance(exc, PlannerParseError):
                _write_text(run_paths.run_dir / f"planner_call_{planner_calls + 1:02d}_raw.md", exc.raw_output)
    _write_initial_plan_record(config, run_paths, decision)

    session = CodexSession(config)
    try:
        while coder_turns < config.hard_max_coder_turns and decision.status == "continue":
            coder_turns += 1
            manifest.coder_turns = coder_turns
            coder_prompt = _build_coder_prompt(
                config,
                decision,
                failure_signature=failure_signature.normalized_signature if failure_signature else "",
            )
            coder_result = await session.send_prompt(coder_prompt)
            _write_text(run_paths.run_dir / f"coder_turn_{coder_turns:02d}.md", coder_result.content)

            changed_paths = _current_changed_files(config.repo_root)
            manifest.files_changed = diff_snapshot_paths(
                baseline_snapshot,
                capture_worktree_snapshot(config.repo_root),
            )
            current_diff = _current_diff(config.repo_root, config.max_diff_chars)
            _write_text(run_paths.run_dir / f"round_{coder_turns:02d}.diff", current_diff)

            verify_commands = decision.next_increment.verification_commands or select_verification_commands(
                config,
                changed_paths,
            )
            verification_results = run_verification_commands(
                config.repo_root,
                verify_commands,
                round_index=coder_turns,
                run_dir=run_paths.run_dir,
                max_log_chars=config.max_log_chars,
            )
            manifest.verify_steps = [result.command for result in verification_results]
            failed_steps = [result for result in verification_results if result.exit_code != 0]
            if not failed_steps:
                manifest.status = "done"
                break

            failure_signature = failed_steps[-1].failure_signature
            if failure_signature is not None:
                _write_json(
                    run_paths.run_dir / f"failure_signature_{coder_turns:02d}.json",
                    failure_signature.model_dump(),
                )

            progress = detect_no_progress(
                previous_diff=previous_diff,
                current_diff=current_diff,
                previous_signature=previous_signature,
                current_signature=failure_signature.normalized_signature if failure_signature else "",
                previous_objective=previous_objective,
                current_objective=decision.next_increment.objective,
                changed_files=changed_paths,
            )
            previous_diff = current_diff
            previous_signature = failure_signature.normalized_signature if failure_signature else ""
            previous_objective = decision.next_increment.objective

            if progress.no_progress:
                final_issues.extend(progress.reasons)
                if planner_calls < config.max_planner_calls:
                    context_text, context_manifest = build_context_bundle(
                        config,
                        changed_paths=changed_paths,
                        failure_signature=failure_signature,
                        state_summary=(
                            f"Tried objective: {decision.next_increment.objective}\n"
                            f"Detected no progress: {', '.join(progress.reasons)}"
                        ),
                    )
                    _write_json(run_paths.context_manifest_file, context_manifest.model_dump())
                    try:
                        planner_response = call_planner(
                            config,
                            task=config.task,
                            context_text=context_text,
                            why_called="stalled",
                            effort=config.planner_effort_escalated,
                            state_summary=run_paths.state_summary_file.read_text(),
                        )
                        planner_calls += 1
                        manifest.planner_calls = planner_calls
                        manifest.usage_summary.input_tokens += planner_response.usage_summary.input_tokens
                        manifest.usage_summary.output_tokens += planner_response.usage_summary.output_tokens
                        manifest.usage_summary.total_tokens += planner_response.usage_summary.total_tokens
                        manifest.usage_summary.estimated_cost_usd += planner_response.usage_summary.estimated_cost_usd
                        _save_planner_response(run_paths, planner_calls, planner_response)
                        decision = planner_response.decision
                        continue
                    except (RuntimeError, PlannerParseError) as exc:
                        final_issues.append(str(exc))
                        if isinstance(exc, PlannerParseError):
                            _write_text(
                                run_paths.run_dir / f"planner_call_{planner_calls + 1:02d}_raw.md",
                                exc.raw_output,
                            )
                manifest.status = "blocked"
                break

            decision = PlannerDecision(
                status="continue",
                why_called="stalled",
                diagnosis="Verification failed; ask Codex for a minimal follow-up fix.",
                risk_flags=[],
                next_increment=NextIncrement(
                    objective="Fix the latest verification failure without broadening scope.",
                    files_to_touch=changed_paths or decision.next_increment.files_to_touch,
                    constraints=decision.next_increment.constraints,
                    verification_commands=verify_commands,
                    review_requests=decision.next_increment.review_requests,
                    acceptance_criteria=["The same verification command passes."],
                ),
                questions_for_user=[],
                stop_if=["The same failure signature repeats again."],
            )

        if manifest.status != "done":
            manifest.status = "blocked" if final_issues else "failed"

        if manifest.files_changed:
            review_requests = collect_review_requests(
                manifest.files_changed,
                decision.next_increment.review_requests,
            )
            for index, review_request in enumerate(review_requests, start=1):
                manifest.reviews_run.append(f"{review_request.skill}:{review_request.target}")
                review_result = await session.send_prompt(build_review_prompt(review_request, run_paths.run_dir))
                _write_text(
                    run_paths.reviews_dir / f"review_prompt_{index:02d}.md",
                    review_result.content,
                )
            collect_review_artifacts(config.repo_root, run_paths.reviews_dir)

    finally:
        await session.close()

    summary_text = _final_summary_text(
        config,
        manifest,
        verification_results=manifest.verify_steps,
        open_issues=final_issues,
    )
    _write_text(run_paths.final_summary_file, summary_text)
    save_manifest(run_paths, manifest)
    print(summary_text)
    return 0 if manifest.status == "done" else 1


def run_cli(argv: list[str] | None = None) -> int:
    """Parse CLI arguments and run the thorny-loop flow."""

    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config(args)
    run_paths = _load_or_create_run_paths(config)
    return asyncio.run(_run_cli_async(config, run_paths))
