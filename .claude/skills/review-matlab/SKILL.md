---
name: review-matlab
description: Review MATLAB research code for model agreement, solver convergence, and derivative correctness. Use for requested reviews or substantive numerical changes.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

Resolve `$ARGUMENTS` to the requested files. Launch one `matlab-reviewer` agent for the full approved target scope
with a short, self-contained brief: files to review, what changed, what was
already checked, and no conclusion. Instruct the reviewer to read
`protocols/skills/review-matlab.md`; the main agent need not read that protocol
before delegation. Present the returned findings under `Reports and Updates`
in `protocols/writing.md`, saving a report only if the user requested one.
