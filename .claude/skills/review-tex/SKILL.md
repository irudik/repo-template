---
name: review-tex
description: Run the LaTeX review protocol on manuscript and slides. Detects hardcoded numeric results, distinguishes manuscript from slide contexts, and auto-fixes unambiguous values when the source is clear.
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
