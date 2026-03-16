---
name: review-tex
description: Run the LaTeX review protocol on manuscript and slides. Checks for hardcoded numbers, citation consistency, and compilation issues. Auto-fixes unambiguous hardcoded values; produces a report for ambiguous cases.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review LaTeX Wrapper

Use the canonical shared protocol in `protocols/skills/review-tex.md`.

## Wrapper Workflow

1. Resolve the target scope from `$ARGUMENTS`.
2. Read `protocols/skills/review-tex.md`.
3. Launch the `tex-reviewer` agent for each target and instruct it to follow `protocols/skills/review-tex.md`.
4. Present a concise summary of the findings.
