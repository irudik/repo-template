---
name: proofread
description: Review academic text for grammar, typos, consistency, and layout risks without editing. Use only when the user asks for it.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

Resolve `$ARGUMENTS` to the requested files. Launch one `proofreader` agent for the full approved target scope
with a short, self-contained brief: files to review, what changed, what was
already checked, and no conclusion. Instruct the reviewer to read
`protocols/skills/proofread.md`; the main agent need not read that protocol
before delegation. Present the returned findings under `Reports and Updates`
in `protocols/writing.md`, saving a report only if the user requested one.
