#!/usr/bin/env python3
"""Validate shared skills, permissions, and routed project conventions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

WRAPPER_PROTOCOL_MARKERS = (
    "## Review Protocol",
    "### Review Categories",
    "## Workflow Phases",
    "## Proofreading Protocol",
    "## The Five-Lens Protocol",
)

REVIEW_AGENT_PROTOCOLS = {
    "domain-reviewer": "review-domain",
    "julia-reviewer": "review-julia",
    "makefile-reviewer": "review-makefile",
    "matlab-reviewer": "review-matlab",
    "proofreader": "proofread",
    "r-reviewer": "review-r",
    "stata-reviewer": "review-stata",
    "tex-reviewer": "review-tex",
}

CODE_CONVENTION_ROUTES = {
    "r-reviewer": "code/conventions/r.md",
    "julia-reviewer": "code/conventions/julia.md",
    "stata-reviewer": "code/conventions/stata.md",
    "matlab-reviewer": "code/conventions/matlab.md",
    "makefile-reviewer": "code/conventions/makefile.md",
}

WORKFLOW_REQUIRED_SNIPPETS = {
    "AGENTS.md": (
        "## Risk-Based Workflow",
        "### Selecting a Reviewer",
        "do not spawn one\nreviewer per file type",
        "Use a full multi-agent loop only when the user explicitly requests it",
        "Documentation or instruction-only changes do not require a Make dry run.",
        "Do not perform a scoring exercise after every routine edit.",
        "pause until the user says\n  whether to continue in the current session",
    ),
    "CLAUDE.md": (
        "routine work needs no plan",
        "Start a fresh session, or use `/clear`, when changing task or branch",
        "pause until the user says whether\n  to continue in the current session",
        "Allow one\nCodex fix and one Claude re-review by default.",
        "Do not pin Claude's `effortLevel` or model in tracked Claude project",
    ),
}

COMMIT_PROTOCOL_REQUIRED_SNIPPETS = (
    "If the current branch is a non-`main` branch, keep using it.",
    "If the current branch is `main`, detached, or the user explicitly asks for a",
    "Keep branch naming tool-neutral.",
    "Choose Make verification in proportion to the files being committed:",
    "Documentation and instruction-only changes require no Make dry run.",
)

COMMIT_PROTOCOL_FORBIDDEN_SNIPPETS = (
    "Always create a new branch.",
)

COMMIT_PROTOCOL_FORBIDDEN_PATTERNS = (
    re.compile(r"(?<!\.)codex/"),
)

PROTOCOL_REQUIRED_SNIPPETS = {
    "protocols/skills/compare-branches.md": (
        "run `make -n`",
        "rebuild them with `make`",
        "Output Verification Formats guidance in `AGENTS.md`",
    ),
    "protocols/skills/setup-makefile.md": (
        "`.R`, `.jl`, `.do`, `.ado`, and `.m`",
        "`export delimited`",
        "`file write`",
        "`$(STATA) -b do $<`",
        "file.path(\"..\", \"..\", \"output\")",
        "joinpath(\"..\", \"..\", \"output\")",
        "OUTPUT_ROOT ?= ../../output",
    ),
    "protocols/skills/verify-outputs.md": (
        "`export delimited`",
        "`putexcel`",
        "`esttab`",
        "`file write`",
    ),
    "protocols/skills/review-makefile.md": (
        "`.R`, `.jl`, `.do`, `.ado`, and `.m`",
        "`$(STATA) -b do $<`",
    ),
}

PATH_MODEL_REQUIRED_SNIPPETS = {
    "AGENTS.md": (
        "Run all Make commands below from the repository root.",
        "`make -C path` changes Make's working directory",
        "`code/[subdir]/` as the command's working directory",
        "`Rscript script.R`",
        "`julia script.jl`",
        "`stata -b do script.do`",
        "`matlab -batch \"run('script.m')\"`",
    ),
    "CLAUDE.md": (
        "Run all Make commands below from the repository root.",
        "`make -C path` changes Make's working directory",
    ),
    "code/AGENTS.md": (
        "conventions/shared.md",
        "conventions/r.md",
        "conventions/julia.md",
        "conventions/stata.md",
        "conventions/matlab.md",
        "conventions/makefile.md",
    ),
    "code/conventions/shared.md": (
        "paths in task-group Makefiles",
        "the scripts they run are relative to the task-group directory",
        "Do not add a `PROJECT_ROOT` variable merely",
        "Use forward slashes in any literal filepath",
    ),
    "code/conventions/r.md": (
        "script working directory",
        'output_root = file.path("..", "..", "output")',
    ),
    "code/conventions/julia.md": (
        "script working directory",
        'output_root = joinpath("..", "..", "output")',
    ),
    "code/conventions/stata.md": (
        "script working directory",
        'local output_root "../../output"',
    ),
    "code/conventions/matlab.md": (
        "script working directory",
        'output_root = fullfile("..", "..", "output");',
    ),
    "code/conventions/makefile.md": (
        "OUTPUT_ROOT = ../../output",
    ),
    "README.md": (
        "Run these Make commands from the project root.",
        "targets, prerequisites, and scripts use paths",
        "working-directory-relative",
        'output_root = file.path("..", "..", "output")',
        'output_root = joinpath("..", "..", "output")',
        'local output_root "../../output"',
        'output_root = fullfile("..", "..", "output");',
    ),
}

PATH_MODEL_FORBIDDEN_SNIPPETS = {
    "AGENTS.md": (
        "fall back to `Rscript path/to/script.R`",
        "fall back to `julia path/to/script.jl`",
        "fall back to `stata -b do path/to/script.do`",
        "fall back to `matlab -batch",
    ),
    "code/conventions/shared.md": (
        "relative to repository root",
        "Use repo-relative paths only",
    ),
    "code/conventions/r.md": (
        "code/analysis.R | output/tables",
        'file.path("output", "figures", "my_plot.pdf")',
    ),
    "code/conventions/julia.md": (
        'joinpath("output", "figures", "my_plot.pdf")',
    ),
    "code/conventions/stata.md": (
        'save "output/tables/my_results.dta", replace',
    ),
    "code/conventions/matlab.md": (
        'fullfile("output", "tables", "results.csv")',
    ),
}

CLAUDE_WRAPPER_REQUIRED_SNIPPETS = {
    "code/CLAUDE.md": (
        "[AGENTS.md](./AGENTS.md)",
        "source of truth",
        "conventions/shared.md",
    ),
    "latex/CLAUDE.md": ("[AGENTS.md](./AGENTS.md)", "source of truth"),
}

LEGACY_RULE_REFERENCE_GLOBS = (
    "README.md",
    "CLAUDE.md",
    "protocols/skills/*.md",
    ".claude/agents/*.md",
)


def load_claude_bash_permissions() -> set[str]:
    settings_path = REPO_ROOT / ".claude/settings.json.example"
    settings = json.loads(settings_path.read_text())
    permissions = settings["permissions"]["allow"]
    pattern = re.compile(r"Bash\(([^ ]+) \*\)")
    command_prefixes = set()

    for entry in permissions:
        match = pattern.fullmatch(entry)
        if match:
            command_prefixes.add(match.group(1))

    return command_prefixes


def load_codex_prefix_rules() -> set[str]:
    rules_path = REPO_ROOT / ".codex/rules/default.rules"
    pattern = re.compile(r'prefix_rule\(pattern=\["([^"]+)"\]')
    command_prefixes = set()

    for line in rules_path.read_text().splitlines():
        match = pattern.search(line)
        if match:
            command_prefixes.add(match.group(1))

    return command_prefixes


def collect_skill_names(base_dir: Path) -> set[str]:
    return {path.parent.name for path in base_dir.glob("*/SKILL.md")}


def collect_protocol_names() -> set[str]:
    return {path.stem for path in (REPO_ROOT / "protocols/skills").glob("*.md")}


def check_wrapper_protocol_refs(wrapper_dir: Path, errors: list[str]) -> None:
    for wrapper_path in wrapper_dir.glob("*/SKILL.md"):
        skill_name = wrapper_path.parent.name
        expected_ref = f"protocols/skills/{skill_name}.md"
        wrapper_text = wrapper_path.read_text()

        if expected_ref not in wrapper_text:
            errors.append(
                f"{wrapper_path.relative_to(REPO_ROOT)} is missing reference to {expected_ref}"
            )

        for marker in WRAPPER_PROTOCOL_MARKERS:
            if marker in wrapper_text:
                errors.append(
                    f"{wrapper_path.relative_to(REPO_ROOT)} still contains protocol marker '{marker}'"
                )


def check_agent_protocol_refs(errors: list[str]) -> None:
    agents_dir = REPO_ROOT / ".claude/agents"

    for agent_name, protocol_name in REVIEW_AGENT_PROTOCOLS.items():
        agent_path = agents_dir / f"{agent_name}.md"
        expected_ref = f"protocols/skills/{protocol_name}.md"
        agent_text = agent_path.read_text()

        if expected_ref not in agent_text:
            errors.append(
                f"{agent_path.relative_to(REPO_ROOT)} is missing reference to {expected_ref}"
            )

        for marker in WRAPPER_PROTOCOL_MARKERS:
            if marker in agent_text:
                errors.append(
                    f"{agent_path.relative_to(REPO_ROOT)} still contains protocol marker '{marker}'"
                )


def check_code_convention_routes(errors: list[str]) -> None:
    shared_path = REPO_ROOT / "code/conventions/shared.md"
    if not shared_path.is_file():
        errors.append("code/conventions/shared.md is missing")

    for agent_name, convention_name in CODE_CONVENTION_ROUTES.items():
        convention_path = REPO_ROOT / convention_name
        if not convention_path.is_file():
            errors.append(f"{convention_name} is missing")

        agent_path = REPO_ROOT / ".claude/agents" / f"{agent_name}.md"
        agent_text = agent_path.read_text()
        if "code/conventions/shared.md" not in agent_text:
            errors.append(
                f"{agent_path.relative_to(REPO_ROOT)} does not load the shared code convention"
            )
        if convention_name not in agent_text:
            errors.append(
                f"{agent_path.relative_to(REPO_ROOT)} does not load {convention_name}"
            )


def check_claude_project_defaults(errors: list[str]) -> None:
    settings_paths = (
        REPO_ROOT / ".claude/settings.json.example",
        REPO_ROOT / ".claude/settings.json",
    )

    for settings_path in settings_paths:
        if not settings_path.is_file():
            continue

        settings = json.loads(settings_path.read_text())
        for forbidden_key in ("effortLevel", "model"):
            if forbidden_key in settings:
                errors.append(
                    f"{settings_path.relative_to(REPO_ROOT)} pins Claude {forbidden_key}"
                )


def check_workflow_policy(errors: list[str]) -> None:
    for relative_path, snippets in WORKFLOW_REQUIRED_SNIPPETS.items():
        file_path = REPO_ROOT / relative_path
        file_text = file_path.read_text()
        for snippet in snippets:
            if snippet not in file_text:
                errors.append(
                    f"{relative_path} is missing workflow policy text: {snippet!r}"
                )


def check_commit_protocol_branch_policy(errors: list[str]) -> None:
    commit_protocol_path = REPO_ROOT / "protocols/skills/commit.md"
    commit_protocol_text = commit_protocol_path.read_text()

    for snippet in COMMIT_PROTOCOL_REQUIRED_SNIPPETS:
        if snippet not in commit_protocol_text:
            errors.append(
                f"{commit_protocol_path.relative_to(REPO_ROOT)} is missing branch-policy text: {snippet!r}"
            )

    for snippet in COMMIT_PROTOCOL_FORBIDDEN_SNIPPETS:
        if snippet in commit_protocol_text:
            errors.append(
                f"{commit_protocol_path.relative_to(REPO_ROOT)} still contains forbidden branch-policy text: {snippet!r}"
            )

    for pattern in COMMIT_PROTOCOL_FORBIDDEN_PATTERNS:
        if pattern.search(commit_protocol_text):
            errors.append(
                f"{commit_protocol_path.relative_to(REPO_ROOT)} still contains a tool-specific branch prefix matching {pattern.pattern!r}"
            )


def check_protocol_required_snippets(errors: list[str]) -> None:
    for relative_path, snippets in PROTOCOL_REQUIRED_SNIPPETS.items():
        protocol_path = REPO_ROOT / relative_path
        protocol_text = protocol_path.read_text()

        for snippet in snippets:
            if snippet not in protocol_text:
                errors.append(
                    f"{protocol_path.relative_to(REPO_ROOT)} is missing required protocol text: {snippet!r}"
                )


def check_path_model_snippets(errors: list[str]) -> None:
    for relative_path, snippets in PATH_MODEL_REQUIRED_SNIPPETS.items():
        file_path = REPO_ROOT / relative_path
        file_text = file_path.read_text()

        for snippet in snippets:
            if snippet not in file_text:
                errors.append(
                    f"{file_path.relative_to(REPO_ROOT)} is missing required path-model text: {snippet!r}"
                )

    for relative_path, snippets in PATH_MODEL_FORBIDDEN_SNIPPETS.items():
        file_path = REPO_ROOT / relative_path
        file_text = file_path.read_text()

        for snippet in snippets:
            if snippet in file_text:
                errors.append(
                    f"{file_path.relative_to(REPO_ROOT)} still contains forbidden path-model text: {snippet!r}"
                )


def check_claude_wrappers(errors: list[str]) -> None:
    for relative_path, snippets in CLAUDE_WRAPPER_REQUIRED_SNIPPETS.items():
        file_path = REPO_ROOT / relative_path
        file_text = file_path.read_text()

        for snippet in snippets:
            if snippet not in file_text:
                errors.append(
                    f"{file_path.relative_to(REPO_ROOT)} is missing required Claude-wrapper text: {snippet!r}"
                )


def check_no_legacy_rule_refs(errors: list[str]) -> None:
    for pattern in LEGACY_RULE_REFERENCE_GLOBS:
        for file_path in REPO_ROOT.glob(pattern):
            file_text = file_path.read_text()
            if ".claude/rules/" in file_text:
                errors.append(
                    f"{file_path.relative_to(REPO_ROOT)} still references deleted .claude/rules content"
                )


def check_claude_rules_dir(errors: list[str]) -> None:
    rule_files = sorted(
        path.relative_to(REPO_ROOT) for path in (REPO_ROOT / ".claude/rules").glob("*.md")
    )
    if rule_files:
        errors.append(f".claude/rules still contains markdown files: {rule_files}")


def main() -> int:
    errors: list[str] = []

    claude_permissions = load_claude_bash_permissions()
    codex_permissions = load_codex_prefix_rules()

    only_in_claude = sorted(claude_permissions - codex_permissions)
    only_in_codex = sorted(codex_permissions - claude_permissions)

    if only_in_claude:
        errors.append(f"Commands allowed only in Claude config: {only_in_claude}")
    if only_in_codex:
        errors.append(f"Commands allowed only in Codex config: {only_in_codex}")

    protocol_names = collect_protocol_names()
    claude_skill_names = collect_skill_names(REPO_ROOT / ".claude/skills")
    codex_skill_names = collect_skill_names(REPO_ROOT / ".agents/skills")

    protocol_only = sorted(protocol_names - claude_skill_names - codex_skill_names)
    claude_only = sorted(claude_skill_names - protocol_names)
    codex_only = sorted(codex_skill_names - protocol_names)
    wrapper_mismatch = sorted(claude_skill_names ^ codex_skill_names)

    if protocol_only:
        errors.append(f"Protocol files without matching skill wrappers: {protocol_only}")
    if claude_only:
        errors.append(f"Claude skill wrappers without matching protocols: {claude_only}")
    if codex_only:
        errors.append(f"Codex skill wrappers without matching protocols: {codex_only}")
    if wrapper_mismatch:
        errors.append(f"Skill wrapper mismatch between Claude and Codex: {wrapper_mismatch}")

    check_wrapper_protocol_refs(REPO_ROOT / ".claude/skills", errors)
    check_wrapper_protocol_refs(REPO_ROOT / ".agents/skills", errors)
    check_agent_protocol_refs(errors)
    check_code_convention_routes(errors)
    check_claude_project_defaults(errors)
    check_workflow_policy(errors)
    check_commit_protocol_branch_policy(errors)
    check_protocol_required_snippets(errors)
    check_path_model_snippets(errors)
    check_claude_wrappers(errors)
    check_no_legacy_rule_refs(errors)
    check_claude_rules_dir(errors)

    if errors:
        print("Template consistency check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Template consistency check passed.")
    print(f"- Shared protocols: {len(protocol_names)}")
    print(f"- Claude skill wrappers: {len(claude_skill_names)}")
    print(f"- Codex skill wrappers: {len(codex_skill_names)}")
    print(f"- Reviewed agent mappings: {len(REVIEW_AGENT_PROTOCOLS)}")
    print(f"- Allowed command families: {len(claude_permissions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
