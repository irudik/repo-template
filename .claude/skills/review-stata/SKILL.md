---
name: review-stata
description: Run the Stata code review protocol on Stata scripts. Checks code quality, reproducibility, data-state safety, and professional standards. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Stata Wrapper

Use the canonical shared protocol in `protocols/skills/review-stata.md`.

## Wrapper Workflow

1. Resolve the target scope from `$ARGUMENTS`.
2. Read `protocols/skills/review-stata.md`.
3. Launch the `stata-reviewer` agent for each target and instruct it to follow `protocols/skills/review-stata.md`.
4. Present a concise summary of the findings.
