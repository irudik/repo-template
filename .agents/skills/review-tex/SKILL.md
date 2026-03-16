---
name: review-tex
description: Run the LaTeX review protocol on manuscript and slides. Detects hardcoded numbers, checks citation consistency, and verifies compilation. Can auto-fix when the source is unambiguous.
workflow_stage: review
compatibility:
  - codex
  - claude-code
version: 1.0.0
tags:
  - latex
  - manuscript
  - hardcoded-numbers
  - citations
---

# Review LaTeX Wrapper

Use the canonical shared protocol in `protocols/skills/review-tex.md`.

## Wrapper Workflow

1. Read `protocols/skills/review-tex.md`.
2. Treat that file as the single source of truth for the substantive workflow.
3. Apply the protocol to the provided argument(s).
4. Keep this file limited to Codex metadata and wrapper guidance.
