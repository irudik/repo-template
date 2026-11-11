---
name: review-makefile
description: Review Make dependencies, script coverage, and output production. Use when build rules change or missing and stale outputs suggest dependency problems.
disable-model-invocation: true
argument-hint: "[path/to/Makefile or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

Resolve `$ARGUMENTS` to the requested files. Launch one `makefile-reviewer` agent for the full approved target scope
with a short, self-contained brief: files to review, what changed, what was
already checked, and no conclusion. Instruct the reviewer to read
`protocols/skills/review-makefile.md`; the main agent need not read that protocol
before delegation. Present the returned findings under `Reports and Updates`
in `protocols/writing.md`, saving a report only if the user requested one.
