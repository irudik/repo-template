---
name: thorny-loop
description: Use the optional sparse GPT Pro planner plus Codex loop for thorny multi-step repo tasks that need explicit diagnosis, repeated verification, or code-manuscript coordination.
workflow_stage: escalation
compatibility:
  - codex
version: 1.0.0
tags:
  - planner
  - codex
  - orchestration
  - verification
---

# Thorny Loop

Use this workflow only for genuinely thorny tasks. Ordinary tasks should stay on the standard contractor workflow.

## When to Use It

- The task spans multiple directories or both `code/` and `latex/`
- Verification or review failures keep repeating
- The root cause is still unclear after ordinary iterations
- The change could affect econometric correctness, simulation logic, or manuscript claims
- The task requires coordinating edits, Make targets, outputs, and review artifacts
- The user explicitly asks for GPT Pro, a thorny loop, or a planner-coder loop

## Default Invocation

Prefer the external repo command, not a nested Codex session:

```bash
python3 tools/thorny_loop/main.py --task "..."
make thorny TASK="..."
```

Nested invocation inside an active Codex session is opt-in only. Use it only if the user explicitly requests nested execution and network access is available for the planner call.

## Required and Optional Args

- Required: `--task` or `TASK="..."`
- Optional scope: `--scope path1 path2` or `SCOPE="path1 path2"`
- Optional verification override: `--verify "make -C code/foo"` or `VERIFY="make -C code/foo"`
- Optional planner limit: `--max-planner-calls N` or `MAX_PLANNER_CALLS=N`
- Optional coder limit: `--max-coder-turns N` or `MAX_CODER_TURNS=N`
- Optional planner effort: `--planner-effort medium|high`

## Behavior

- Planner: sparse `gpt-5.4-pro` calls only when the problem is thorny enough to justify cost
- Coder: persistent Codex MCP session in the current repo
- Verification: existing Make-first workflow
- Reviews: existing repo skills such as `review-r`, `review-julia`, `review-tex`, `review-comments`
- Safety: no auto-commit, no auto-push, no branch creation

## Artifacts

- Per-run artifacts: `quality_reports/thorny_loop/<timestamp>_<slug>/`
- Initial human-readable plan: `quality_reports/plans/`
- Templates: `templates/thorny_loop_*.md`
