---
name: review-comments
description: Review or clean up misleading comments, docstrings, and documentation. Use when documentation may disagree with code or the user requests comment cleanup.
disable-model-invocation: true
argument-hint: "[file or directory path]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
workflow_stage: review
compatibility:
  - codex
  - claude-code
  - cursor
  - antigravity
version: 1.0.0
tags:
  - comments
  - documentation
  - cleanup
  - review
---

Read `protocols/skills/review-comments.md` and apply it to `$ARGUMENTS`.
