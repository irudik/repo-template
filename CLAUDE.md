# CLAUDE.md -- Claude Code Instructions

---

## Shared Instructions

@AGENTS.md

The file imported above holds the project rules shared with Codex and
Antigravity. Put shared rules there. This file holds only what is specific to
Claude Code; keep it under 200 lines.

---

## Claude Code Notes

- `code/CLAUDE.md` and `latex/CLAUDE.md` import the `AGENTS.md` beside them
  when Claude works in those directories.
- Reviewer agents in `.claude/agents/` follow the shared skill files in
  `protocols/skills/`. They return their findings to the main conversation
  and do not save report files.
- `.claude/hooks/protect-files.sh` blocks edits to the files it lists. A
  blocked edit is a deliberate blocker, as described under
  `Working Without Stopping` in `AGENTS.md`.
- Do not pin Claude's `effortLevel` or model in tracked Claude project
  settings. A skill wrapper may set `effort` for a mechanical skill.
- Hand work to Codex only when the user asks for it, with wording such as
  "hand this to Codex" or "Codex executes", or with a `[codex]` marker on
  plan steps. Then follow `protocols/codex-handoff.md`.
