#!/usr/bin/env python3
"""Tests for byte-preserving root instruction merges.

The examples combine shared sections with project facts, missing sections, a
project manuscript location, and retired replication instructions.

Run with: python3 -m unittest tools.tests.test_merge_template_sections
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import merge_template_sections  # noqa: E402


def initialize_git_repository(repository: Path) -> None:
    """Create a repository on a named branch for branch-report tests."""

    repository.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "init", "-q", "-b", "section-test-branch", str(repository)],
        check=True,
        capture_output=True,
    )


def section_by_title(contents: bytes, title: str) -> bytes:
    """Return the exact bytes of one `##` section."""

    _, sections = merge_template_sections.parse_sections(contents)
    return next(section.contents for section in sections if section.title == title)


OLD_AGENTS_TITLE = (
    b"# AGENTS.md -- Academic Project Development with Codex CLI and Gemini CLI"
)
OLD_CLAUDE_TITLE = b"# CLAUDE.md -- Academic Project Development with Claude Code"
PROJECT_HEADER = b"\n\n**Project:** Example Project\n\n---\n\n"

PROJECT_CORE = (
    b"## Core Principles\n\n"
    b"- **Match process to risk** -- earlier wording\n"
    b"- **Single source of truth** -- the manuscript in `$MANUSCRIPT_DIR` "
    b"is\n"
    b"  authoritative for the paper and appendix\n"
    b"- **Project rule** -- an earlier project bullet\n\n"
    b"---\n\n"
)
PROJECT_AGENTS_SECTION = (
    b"## Manuscript Location\n\n"
    b"The manuscript stays in the coauthor's Overleaf checkout.\n\n"
    b"---\n\n"
)
PROJECT_FOLDER_SECTION = (
    b"## Folder Structure\n\n"
    b"Project-owned folder description with exact spacing.  \n\n"
    b"---\n\n"
)
PROJECT_AGENTS_COMMANDS = (
    b"## Commands\n\n"
    b"Project introduction that the shared path guidance replaces.\n\n"
    b"```bash\n"
    b"make project-agents-target\n"
    b"```\n\n"
    b"---\n\n"
)
PROJECT_CLAUDE_COMMANDS = (
    b"## Commands\n\n"
    b"```bash\n"
    b"make project-claude-target\n"
    b"```\n\n"
    b"---\n\n"
)
PROJECT_CLAUDE_SECTION = (
    b"## Git Authorization Boundary\n\n"
    b"A push instruction does not authorize a commit.\n\n"
)
RETIRED_REPLICATION = (
    b"## Replication-First Protocol\n\n"
    b"Retired instructions.\n\n"
    b"### Summary\n\n"
    b"A retired summary instruction.\n\n"
    b"## Replication Targets: [Paper Author (Year)]\n\n"
    b"Unfilled table.\n\n"
    b"## Results Comparison\n\n"
    b"Retired comparison.\n\n"
    b"## Discrepancies (if any)\n\n"
    b"Retired discrepancy notes.\n\n"
    b"## Environment\n\n"
    b"Retired environment notes.\n\n"
)


def earlier_section(title: str) -> bytes:
    """Return a section as an earlier template version would have carried it."""

    return f"## {title}\n\nEarlier template text for {title}.\n\n---\n\n".encode()


class TemplateSectionMergeTests(unittest.TestCase):
    """Only template-owned root sections should be replaced, inserted, or retired."""

    def setUp(self) -> None:
        self.workspace = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.workspace, True)
        self.target = self.workspace / "research-project"
        initialize_git_repository(self.target)

    def build_earlier_documents(self) -> None:
        """Write root files laid out as the longer earlier template had them."""

        target_agents = (
            OLD_AGENTS_TITLE
            + PROJECT_HEADER
            + PROJECT_CORE
            + PROJECT_AGENTS_SECTION
            + PROJECT_FOLDER_SECTION
            + PROJECT_AGENTS_COMMANDS
            + earlier_section("Quality Thresholds")
            + earlier_section("Risk-Based Workflow")
            + earlier_section("Solver Debugging Protocol")
            + b"## Diagnosis\n\nExample heading inside the solver section.\n\n"
            + RETIRED_REPLICATION
            + earlier_section("General Trace Protocol")
            + earlier_section("Quality Gates & Scoring Rubrics")
            + earlier_section("Command Conventions")
            + earlier_section("Workflow Quick Reference")
        )
        target_claude = (
            OLD_CLAUDE_TITLE
            + PROJECT_HEADER
            + PROJECT_CORE
            + PROJECT_CLAUDE_SECTION
            + PROJECT_FOLDER_SECTION
            + PROJECT_CLAUDE_COMMANDS
            + earlier_section("Skills Quick Reference")
            + earlier_section("Claude-Specific Notes")
            + earlier_section("Kimi Code CLI")
            + earlier_section("Gemini CLI")
            + earlier_section("Explicit Codex Handoff")
        )
        (self.target / "AGENTS.md").write_bytes(target_agents)
        (self.target / "CLAUDE.md").write_bytes(target_claude)

    def test_commands_is_the_only_project_section_with_shared_fence_preamble(self) -> None:
        """No other project-owned fenced section needs a partial template merge."""

        for file_name, owned_titles in merge_template_sections.OWNED_SECTION_TITLES.items():
            contents = (REPO_ROOT / file_name).read_bytes()
            _, sections = merge_template_sections.parse_sections(contents)
            sections_with_opening_prose: list[str] = []
            for section in sections:
                if section.title in owned_titles:
                    continue
                fence = merge_template_sections.FENCED_BLOCK.search(section.contents)
                if fence is None:
                    continue
                heading_end = section.contents.find(b"\n") + 1
                opening_prose = section.contents[heading_end : fence.start()].strip()
                if opening_prose:
                    sections_with_opening_prose.append(section.title)

            self.assertEqual(
                sections_with_opening_prose,
                list(merge_template_sections.SHARED_PREAMBLE_SECTION_TITLES[file_name]),
            )

    def test_every_template_section_is_owned_or_a_shared_preamble(self) -> None:
        """A template section nobody owns would never reach a project."""

        for file_name, owned_titles in merge_template_sections.OWNED_SECTION_TITLES.items():
            contents = (REPO_ROOT / file_name).read_bytes()
            _, sections = merge_template_sections.parse_sections(contents)
            known_titles = set(owned_titles) | set(
                merge_template_sections.SHARED_PREAMBLE_SECTION_TITLES[file_name]
            )

            self.assertEqual(
                [section.title for section in sections if section.title not in known_titles],
                [],
            )
            self.assertEqual(
                [title for title in owned_titles if title not in {s.title for s in sections}],
                [],
            )

    def test_merge_replaces_inserts_preserves_removes_and_repeats_cleanly(self) -> None:
        self.build_earlier_documents()
        template_agents = (REPO_ROOT / "AGENTS.md").read_bytes()
        template_claude = (REPO_ROOT / "CLAUDE.md").read_bytes()

        first = merge_template_sections.merge_repository(
            REPO_ROOT,
            self.target,
            apply=True,
        )
        second = merge_template_sections.merge_repository(
            REPO_ROOT,
            self.target,
            apply=True,
        )

        merged_agents = (self.target / "AGENTS.md").read_bytes()
        merged_claude = (self.target / "CLAUDE.md").read_bytes()
        self.assertTrue(first.has_changes)
        self.assertFalse(second.has_changes)
        self.assertEqual(first.branch, "section-test-branch")

        # Titles are updated and the project's own header lines are kept.
        self.assertTrue(
            merged_agents.startswith(
                b"# AGENTS.md -- Shared Instructions for Claude Code, Codex, and Antigravity"
            )
        )
        self.assertTrue(merged_claude.startswith(b"# CLAUDE.md -- Claude Code Instructions"))
        self.assertIn(b"**Project:** Example Project", merged_agents)

        # Project sections are untouched.
        self.assertEqual(
            section_by_title(merged_agents, "Manuscript Location"),
            PROJECT_AGENTS_SECTION,
        )
        self.assertEqual(
            section_by_title(merged_agents, "Folder Structure"),
            PROJECT_FOLDER_SECTION,
        )
        self.assertEqual(
            section_by_title(merged_claude, "Git Authorization Boundary"),
            PROJECT_CLAUDE_SECTION,
        )

        # Shared sections take the template text, except the project's own
        # statement of where the manuscript lives.
        merged_core = section_by_title(merged_agents, "Core Principles")
        self.assertIn(
            b"the manuscript in `$MANUSCRIPT_DIR` is\n"
            b"  authoritative for the paper and appendix",
            merged_core,
        )
        self.assertIn(b"**The code is ours to change**", merged_core)
        self.assertNotIn(b"an earlier project bullet", merged_core)
        self.assertEqual(
            section_by_title(merged_agents, "Risk-Based Workflow"),
            section_by_title(template_agents, "Risk-Based Workflow"),
        )

        # Commands keeps the project's command list under the shared prose.
        merged_agents_commands = section_by_title(merged_agents, "Commands")
        self.assertIn(
            b"Run all Make commands below from the repository root.",
            merged_agents_commands,
        )
        self.assertIn(b"make project-agents-target", merged_agents_commands)
        self.assertNotIn(
            b"Project introduction that the shared path guidance replaces.",
            merged_agents_commands,
        )
        self.assertIn("AGENTS.md: Commands", first.replaced_sections)

        # New sections arrive, in template order.
        for title in (
            "Where Things Are",
            "Defects That Block a Commit or Merge",
            "Changed Numbers in the Manuscript",
            "Records",
        ):
            self.assertIn(f"AGENTS.md: {title}", first.inserted_sections)
        self.assertLess(
            merged_agents.index(b"## Where Things Are"),
            merged_agents.index(b"## Commands"),
        )
        self.assertLess(
            merged_agents.index(b"## Risk-Based Workflow"),
            merged_agents.index(b"## Records"),
        )

        # Retired sections leave both files.
        for retired in (
            b"## Quality Thresholds",
            b"## Solver Debugging Protocol",
            b"## Diagnosis",
            b"## General Trace Protocol",
            b"## Quality Gates & Scoring Rubrics",
            b"## Command Conventions",
            b"## Workflow Quick Reference",
            b"## Replication-First Protocol",
            b"## Replication Targets: [Paper Author (Year)]",
            b"## Results Comparison",
        ):
            self.assertNotIn(retired, merged_agents)
        for retired in (
            b"## Core Principles",
            b"## Skills Quick Reference",
            b"## Claude-Specific Notes",
            b"## Kimi Code CLI",
            b"## Gemini CLI",
            b"## Explicit Codex Handoff",
        ):
            self.assertNotIn(retired, merged_claude)
        self.assertIn("CLAUDE.md: ## Kimi Code CLI", first.removed_sections)
        self.assertIn("AGENTS.md: ## Quality Thresholds", first.removed_sections)
        self.assertTrue(
            any("Replication-First Protocol" in item for item in first.removed_sections)
        )
        self.assertTrue(any("### Summary" in item for item in first.removed_sections))

        # Root CLAUDE.md gains the import and the Claude-only notes.
        self.assertEqual(
            section_by_title(merged_claude, "Shared Instructions"),
            section_by_title(template_claude, "Shared Instructions"),
        )
        self.assertIn(b"@AGENTS.md", merged_claude)
        self.assertIn("CLAUDE.md: Claude Code Notes", first.inserted_sections)

        # Project sections that an older CLAUDE.md repeated stay and are reported.
        self.assertEqual(
            section_by_title(merged_claude, "Commands"),
            PROJECT_CLAUDE_COMMANDS,
        )
        self.assertTrue(
            any("'Commands'" in warning for warning in first.warnings),
            first.warnings,
        )
        self.assertTrue(
            any("'Folder Structure'" in warning for warning in first.warnings),
            first.warnings,
        )

    def test_crlf_retired_kimi_folder_lines_and_title_are_updated(self) -> None:
        kimi_folder_section = (
            "## Folder Structure\n\n"
            "```\n"
            "├── .agents/                     # Codex/Kimi skill wrappers (both tools scan this)\n"
            "│   └── skills/                  # Skill definitions\n"
            "├── .kimi-code/                  # Kimi Code CLI example config\n"
            "│   └── config.toml.example      # Permission rules to merge into ~/.kimi-code/config.toml\n"
            "```\n\n"
        ).encode("utf-8")
        old_agents = (
            b"# AGENTS.md -- Academic Project Development with Codex CLI and Kimi Code CLI"
            + PROJECT_HEADER
            + PROJECT_CORE
            + kimi_folder_section
            + PROJECT_AGENTS_COMMANDS
        ).replace(b"\n", b"\r\n")
        (self.target / "AGENTS.md").write_bytes(old_agents)
        (self.target / "CLAUDE.md").write_bytes((REPO_ROOT / "CLAUDE.md").read_bytes())

        report = merge_template_sections.merge_repository(
            REPO_ROOT,
            self.target,
            apply=True,
        )

        merged_agents = (self.target / "AGENTS.md").read_bytes()
        self.assertTrue(report.has_changes)
        self.assertNotIn(b"Kimi", merged_agents)
        self.assertNotIn(b".kimi-code", merged_agents)
        self.assertTrue(
            merged_agents.startswith(
                b"# AGENTS.md -- Shared Instructions for Claude Code, Codex, and Antigravity"
            )
        )
        self.assertIn("AGENTS.md: Folder Structure", report.replaced_sections)

    def test_departed_root_file_is_neither_changed_nor_added(self) -> None:
        custom_claude = (
            OLD_CLAUDE_TITLE
            + PROJECT_HEADER
            + b"## Quality Thresholds\n\nProject thresholds.\n\n"
        )
        (self.target / "CLAUDE.md").write_bytes(custom_claude)
        tools_directory = self.target / "tools"
        tools_directory.mkdir()
        (tools_directory / "template_departures.toml").write_text(
            "[[departure]]\n"
            'path = "AGENTS.md"\n'
            'reason = "The project manages this file elsewhere."\n\n'
            "[[departure]]\n"
            'path = "CLAUDE.md"\n'
            'reason = "The project keeps different root instructions."\n'
        )
        before_claude = (self.target / "CLAUDE.md").read_bytes()

        report = merge_template_sections.merge_repository(
            REPO_ROOT,
            self.target,
            apply=True,
        )

        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertEqual((self.target / "CLAUDE.md").read_bytes(), before_claude)
        self.assertFalse(report.has_changes)
        self.assertEqual(
            [item.path for item in report.departures_honored],
            ["AGENTS.md", "CLAUDE.md"],
        )

    def test_default_command_mode_is_dry_run(self) -> None:
        arguments = merge_template_sections.parse_arguments(
            ["--repo", str(self.target)]
        )

        self.assertFalse(arguments.apply)


if __name__ == "__main__":
    unittest.main()
