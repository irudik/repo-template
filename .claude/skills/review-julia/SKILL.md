---
name: review-julia
description: Review Julia research code for correctness, reproducibility, and numerical performance. Use for requested reviews or substantive changes that warrant independent review.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

Resolve `$ARGUMENTS` to the requested files. Launch one `julia-reviewer` agent for the full approved target scope
with a short, self-contained brief: files to review, what changed, what was
already checked, and no conclusion. Instruct the reviewer to read
`protocols/skills/review-julia.md`; the main agent need not read that protocol
before delegation. Present the returned findings under `Reports and Updates`
in `protocols/writing.md`, saving a report only if the user requested one.
