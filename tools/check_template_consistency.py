#!/usr/bin/env python3
"""Validate shared-skill and permission consistency for the repo template."""

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

COMMIT_PROTOCOL_REQUIRED_SNIPPETS = (
    "If the current branch is a non-`main` branch, keep using it.",
    "If the current branch is `main`, detached, or the user explicitly asks for a",
    "Keep branch naming tool-neutral.",
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
        "Output Verification Formats guidance in `AGENTS.md` or",
        "`.claude/rules/verification-formats.md`",
    ),
    "protocols/skills/setup-makefile.md": (
        "`.R`, `.jl`, `.do`, `.ado`, and `.m`",
        "`export delimited`",
        "`file write`",
        "`$(STATA) -b do $<`",
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
    check_commit_protocol_branch_policy(errors)
    check_protocol_required_snippets(errors)

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
