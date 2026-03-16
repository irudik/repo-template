---
name: review-domain
description: Run the substantive domain review on manuscripts, slides, or lecture materials. Checks identification, derivations, citations, code-theory alignment, and logical consistency. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Domain Wrapper

Use the canonical shared protocol in `protocols/skills/review-domain.md`.

## Wrapper Workflow

1. Resolve the target scope from `$ARGUMENTS`.
2. Read `protocols/skills/review-domain.md`.
3. Launch the `domain-reviewer` agent for each target and instruct it to follow `protocols/skills/review-domain.md`.
4. Present a concise summary of the findings.
