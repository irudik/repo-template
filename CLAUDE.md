# CLAUDE.md -- Academic Project Development with Claude Code

<!-- HOW TO USE: Replace [BRACKETED PLACEHOLDERS] with your project info.
     Keep this root file under ~150 lines — Claude loads it every session.
     See README.md for full documentation. -->

**Project:** [YOUR PROJECT NAME]
**Institution:** [YOUR INSTITUTION]
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile/render and confirm output at the end of every task
- **Readable research code** -- prefer clear, reproducible, prose-like code
  over clever compactness; code should be easy for coauthors, referees, and
  future selves to audit
- **Single source of truth** -- `latex/manuscript.tex` is authoritative for the paper
- **Quality gates** -- nothing ships below 80/100
- **Template hygiene** -- in this template repo, remove branch-specific files under `quality_reports/` before merging to `main`; keep `main` fresh
- **Structured [LEARN] tags** -- when corrected or when you discover a durable lesson, save a structured `[LEARN:category]` entry to `MEMORY.md`

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.md                    # Root Claude Code instructions
├── AGENTS.md                    # Codex CLI instructions
├── MEMORY.md                    # Persistent [LEARN] entries across sessions
├── Makefile                     # Root — delegates to code/ and latex/
├── protocols/                   # Canonical shared skill bodies
│   └── skills/
│       └── *.md
├── .claude/                     # Claude Code: settings, wrappers, agents, hooks
├── .codex/                      # Codex CLI: config and permission rules
├── .agents/                     # Codex CLI: thin skill wrappers
├── code/                        # Analysis code with sub-Makefiles
│   ├── CLAUDE.md                # Claude loads this when working in code/
│   ├── Makefile                 # Delegates to sub-Makefiles
│   ├── [task_group]/            # e.g., data cleaning (R/Stata), simulation (Julia), or structural model (MATLAB)
│   │   ├── Makefile
│   │   └── *.R, *.jl, *.do, *.ado, or *.m
│   └── [task_group]/
│       ├── Makefile
│       └── ...
├── latex/                       # Paper manuscript and slides
│   ├── CLAUDE.md                # Claude loads this when working in latex/
│   ├── Makefile                 # pdflatex 3-pass build
│   ├── manuscript.tex           # Main paper
│   ├── slides.tex               # Presentation slides
│   ├── latex_extras/            # Preamble files (packages, commands, tables)
│   └── references/              # .bib and .bst files
├── output/                      # Code pipeline outputs
│   ├── figures/                 # Generated figures
│   ├── tables/                  # Generated tables
│   └── numbers/                 # Inline numbers for manuscript (\newcommand .txt files)
├── quality_reports/             # Plans, handoffs, session logs, merge reports
└── templates/                   # Session, handoff, learning, and quality templates
```

---

## Commands

```bash
# Make (preferred — builds everything)
make                               # Build all (code + latex)
make -n                            # Dry-run: show what would be built
make check-template                # Validate shared-skill and permission sync
make -C code                       # Build all code targets
make -C code/[task_group] all      # Build one task group
make -C latex                      # Compile manuscript

# LaTeX (manual fallback — 3-pass, pdflatex)
cd latex
export TEXINPUTS=.:./latex_extras/:../output/numbers/:../output/tables/:../output/figures/:
export BIBINPUTS=./references/:
export BSTINPUTS=./references/:
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for deployment |
| 95 | Excellence | Aspirational |

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/commit [msg]` | Stage, commit, PR, merge on the current non-`main` branch; create a branch only when needed |
| `/data-analysis [dataset]` | End-to-end R analysis |
| `/refactor [file-or-dir]` | Verify-refactor-verify loop |
| `/verify-outputs [script]` | Checksum outputs, compare to reference |
| `/compare-branches [b1] [b2]` | Cross-branch output comparison |
| `/resume-custom` | Recover context after compression/new session |
| `/trace [question]` | Trace an ambiguous result or failure back to its most likely cause |
| `/learn [insight]` | Save a durable, project-specific lesson to `MEMORY.md` |
| `/setup-makefile [dir]` | Generate Makefile from directory contents |
| `/review-r [file]` | R code quality review |
| `/review-julia [file]` | Julia code quality review |
| `/review-stata [file]` | Stata code quality review |
| `/review-matlab [file]` | MATLAB code quality review |
| `/review-tex [file]` | LaTeX hardcoded-number review for manuscripts and slides |
| `/review-makefile [file]` | Makefile conventions review |
| `/review-comments [path]` | Clean up comments, docstrings, dead code |
| `/review-domain [file]` | Substantive domain review (identification, citations, code-theory) — opt-in |
| `/proofread [file]` | Grammar, typos, overflow, consistency check — opt-in |
| `/review-pr [PR#]` | Address PR review comments, commit fixes, resolve threads |
| `/matlab-optim-derivatives` | Audit MATLAB optimization derivatives |

---

## Shared Skill Protocols

- Canonical shared skill bodies live in `protocols/skills/`
- `.claude/skills/` and `.agents/skills/` are thin wrappers around those files
- Review-oriented agents in `.claude/agents/` execute the same canonical protocols

## Claude Loading Model

- Root `CLAUDE.md` sets project-wide workflow rules
- `code/CLAUDE.md` loads when Claude works in `code/`
- `latex/CLAUDE.md` loads when Claude works in `latex/`
- Shared local conventions live in `AGENTS.md`, `code/AGENTS.md`, and
  `latex/AGENTS.md`
- `.claude/agents/` and `.claude/hooks/` remain Claude-only execution surfaces
  and mechanics

## Claude-Specific Notes

- Enter plan mode before non-trivial tasks and exit only after the user
  approves the plan
- Prefer auto-compression over `/clear`; use `/clear` only when context is
  genuinely polluted
- After compression or a new session, read `CLAUDE.md`, read the most recent
  plan in `quality_reports/plans/`, read the most recent relevant handoff in
  `quality_reports/handoffs/` if one exists, then inspect
  `git log --oneline -10` and `git diff`

## Explicit Codex Handoff

Delegate execution to Codex ONLY if the user explicitly asks during the original
task, planning prompt, or approval step, using phrasing such as "hand this to
Codex", "delegate execution to Codex", "Codex executes", or a `[codex]` marker
on plan steps. Otherwise follow the normal Claude flow.

During planning, record a `Codex Handoff` section with Codex-owned steps, the
saved plan path, acceptance criteria, expected verification commands, no-commit
default, and cautious handling for `data/` and `output/` symlinks. After plan
approval, send the approved plan to the `codex:codex-rescue` subagent in
write-capable mode.

Codex is the implementer for both the feature/fix and its verification. Codex
adds or updates the verification code needed to make the acceptance criteria
checkable, such as unit tests, fixtures, Makefile targets, data-property checks,
checksum scripts, or build checks. Before handing back, Codex self-reviews its
diff, verification design, and test/build/check results, fixes obvious gaps,
and reports exact evidence.

Claude is the planner and reviewer. Claude reviews Codex's code changes,
verification design, and reported results against the acceptance criteria,
confirms that relevant tests pass, and flags gaps for Codex to fix. Repeat the
Codex implement/self-review/verify step and Claude review step until Claude is
satisfied or the standard five-round contractor review-fix limit is reached. At
the limit, report remaining gaps instead of looping indefinitely. Claude does not
implement verification code or rerun full verification unless the user
explicitly asks.

---

## Current Project State

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Manuscript | `latex/manuscript.tex` | Template | Paper skeleton with standard sections |
| Slides | `latex/slides.tex` | Template | Presentation template |
| Code pipeline | `code/` | Template | Sub-Makefiles to be added per project |

---

## Plan-First Notes

For manuscript or slide tasks, ask during planning whether to include these optional review passes:
- `domain-reviewer` for substantive domain review (identification, derivations, citations, code-theory alignment)
- `proofreader` for grammar, typos, overflow, and consistency

For multi-file tasks, write short handoff notes under
`quality_reports/handoffs/` at major stage boundaries.

When a durable, project-specific lesson emerges, save it to `MEMORY.md` with a
structured `[LEARN:category]` block or use `/learn`.
