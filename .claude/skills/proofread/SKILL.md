---
name: proofread
description: Run expert proofreading on academic documents. Checks grammar, typos, overflow risks, citation consistency, and academic quality for LaTeX, Quarto, and directly provided text-based files. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Proofread Wrapper

Use the canonical shared protocol in `protocols/skills/proofread.md`.

## Wrapper Workflow

1. Resolve the target scope from `$ARGUMENTS`.
2. Read `protocols/skills/proofread.md`.
3. Launch the `proofreader` agent for each target and instruct it to follow `protocols/skills/proofread.md`.
4. Present a concise summary of the findings.
