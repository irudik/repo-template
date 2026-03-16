---
name: review-comments
description: Review and clean up comments, docstrings, and documentation across specified files or directories
disable-model-invocation: true
argument-hint: "[file or directory path]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
workflow_stage: review
compatibility:
  - codex
  - claude-code
  - cursor
  - gemini-cli
version: 1.0.0
tags:
  - comments
  - documentation
  - cleanup
  - review
---

# Comment and Doc Cleanup

## Purpose

Clean up stale or misleading comments/docstrings, remove commented-out code, and align documentation with code reality.

## When to Use

- You want a pass over comments/docstrings for correctness.
- You need to remove commented-out code blocks.
- You want to sync README/docs with the codebase.

## Workflow

1. Identify scope: ask which files or directory to review. Default to the current working directory.
2. Identify style reference: if the user provides a reference file, read it and extract style conventions (comment density, section headers, inline comments, docstring format).
3. Explore files: for each file in scope, note:
   - Commented-out code blocks (comment lines containing code)
   - Comments referencing non-existent features or files
   - Docstrings that conflict with behavior
   - Verbose comments that restate mechanics
4. Check documentation: read README/docs and verify referenced files exist.
5. Present findings: summarize issues with file paths and line numbers, grouped by issue type.
6. Get approval: ask for confirmation before editing.
7. Make edits: remove commented-out code entirely, rewrite stale/misleading comments, fix docstrings.
8. Verify: run `rg` checks to confirm stale references are gone.

## Default Style (override with reference file)

- Section headers: `# ============================================================================`
- Inline comments: short, explain domain logic not code mechanics
- Do not prefix with "Economic intuition:"
- Use Unicode math notation where appropriate
- Delete rather than comment out unused code
- Docstrings: structured with `Arguments`/`Returns` sections
- Target ~15-20% comment density
