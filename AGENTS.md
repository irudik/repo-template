# AGENTS.md -- Shared Instructions for Claude Code, Codex, and Antigravity

**Project:** [YOUR PROJECT NAME]
**Institution:** [YOUR INSTITUTION]

---

## Core Principles

- **The code is ours to change** -- the user and their coauthors own every
  file here, and nobody outside the project depends on it. When a task calls
  for it, rewrite or restructure existing code directly. Do not keep old
  versions beside new ones, add compatibility layers, or work around code you
  could fix. The exception is `/refactor`, a style cleanup that must leave
  outputs identical.
- **Match process to risk** -- plan and review in proportion to the chance
  and cost of a wrong result. A one-line change to an estimand or a solver
  can be riskier than a broad documentation edit.
- **Readable research code** -- prefer clear, reproducible code that
  coauthors and referees can audit over compact or clever code.
- **Plain-language writing** -- all prose follows `protocols/writing.md`:
  replies, reports, issues, commit messages, and comments. Write for an
  economist coauthor, never in programmer jargon.
- **Single source of truth** -- `latex/manuscript.tex` is authoritative for the paper
- **Generated numbers** -- computed results reach the manuscript only through
  macros written to `output/numbers/`, never typed by hand.

---

## Where Things Are

This file is loaded in every session, so it stays short. Read the files below
when the task needs them.

| Need | File |
|------|------|
| Any prose, including replies and reports | `protocols/writing.md` |
| Code under `code/` | `code/AGENTS.md`, which selects from `protocols/conventions/` |
| Manuscript and slides | `latex/AGENTS.md` |
| A numerical solver that fails | `protocols/solver-debugging.md` |
| A skill invoked as `/name` | `protocols/skills/<name>.md` |
| Handing work from Claude to Codex | `protocols/codex-handoff.md` |
| Lessons from earlier sessions | `MEMORY.md` |
| Plans, handoffs, session logs | `quality_reports/`, with layouts in `templates/` |

Analysis code lives in `code/[task_group]/`, each with its own Makefile.
Outputs go to `output/figures/`, `output/tables/`, and `output/numbers/`.
`.claude/skills/` and `.agents/skills/` hold thin wrappers around the shared
skill files.

Size limits: Antigravity cuts an instruction file at 24,000 bytes, and Codex
reads at most 32,768 bytes across all `AGENTS.md` files it loads. Keep this
file under 20,000 bytes; `make check-template` enforces that.

---

## Commands

Run all Make commands below from the repository root.
`make -C path` changes Make's working directory to `path`, so paths in that
Makefile and in the scripts its recipes run are relative to `path`, not to the
repository root.

Issue one command per shell call. Do not chain commands with `&&` or `;`, and
do not rely on `cd`, `export`, or a shell variable carrying over to the next
call: permission rules are evaluated per command, and shell state does not
persist between calls. Issue independent commands in parallel. For a sequence
you repeat, use a Make target.

```bash
make                               # Build all (code, then latex)
make -n                            # Dry run: show what would be built
make -C code                       # Build all code targets
make -C code/[task_group] all      # Build one task group
make -C latex                      # Compile manuscript and slides
make check-template                # Check the instruction files
```

---

## Risk-Based Workflow

Choose the lightest process that still gives credible evidence the result is
right.

| Work | Process |
|------|---------|
| Routine or bounded change | Make the change, check it, report. No saved plan, handoff, or reviewer. |
| Substantive change within one module | State the approach in a few sentences, then implement and check. Use one reviewer only when an independent reading adds material value. |
| High-risk work | Save a plan to `quality_reports/plans/YYYY-MM-DD_short-description.md`, then continue straight through implementation, checks, and one independent review. Fix every blocking defect the review finds. Ask for a second review only when those fixes were substantial. |
| Several reviewers or repeated rounds | Only when the user asks, or when the cause of a failure is still unclear after normal diagnosis and one review. State the open hypotheses, what each reviewer tests, and when to stop. |

High-risk work means: solver, derivative, tolerance, or convergence changes;
identification, estimands, or quantitative claims the manuscript depends on;
broad data-pipeline changes; destructive operations; and a final review
before a merge when a missed error would be costly.

A plan is a working record, saved as a file in the repository. Do not wait
for approval of it, and do not use a tool's plan mode or approval dialog,
unless the user asked to approve plans. An explicit request for a fuller or
lighter process overrides this table.

### Reviewers

Pick the one reviewer that covers the riskiest part of the change. Do not
start one reviewer per file type.

| Main risk | Skill |
|-----------|-------|
| R, Julia, Stata, or MATLAB code | `/review-r`, `/review-julia`, `/review-stata`, `/review-matlab` |
| Make dependencies | `/review-makefile` |
| Results and generated numbers in LaTeX | `/review-tex` |
| Identification, derivations, agreement between code and theory | `/review-domain`, only when the user asks |
| Grammar and presentation | `/proofread`, only when the user asks |
| Unclear cause of a result or failure | `/trace` |

Where the tool can start a subagent, hand the review to a fresh one, and
review in the main conversation only where it cannot. Give the reviewer a
self-contained brief: the files to read, what changed, the acceptance
criteria, and what has already been checked. Leave out your own conclusion,
because the value of a review is an independent reading. When the findings
come back, fix the blocking defects yourself.

### Working Without Stopping

Finish every part of the task before ending the turn. Carry on through the
whole workflow without asking for approval of a plan or of the next step. Do
not end a turn by offering to continue or by listing work you could do
yourself. When a decision is open, first finish all the work that does not
depend on the answer, then ask at the end of the turn; do not use a question
or approval dialog that halts the work midway. A new task or a different
branch within the same session is not a reason to stop; if the context has
grown large, say in one line that a fresh session would help, and continue.

These steps need no further approval:

- reading any file in the repository
- running the `make` targets, dry runs, tests, and scripts the task concerns
- rerunning a build or test after a fix, and retrying a command that timed
  out or found a file busy when it is safe to repeat
- creating and editing files in the directories the task concerns, including
  `latex/references/references.bib`
- creating a working branch when the current branch is `main`
- writing plans and notes under `quality_reports/`

These need the user's request: commits, pushes, merges, deleting or
overwriting data or outputs that cannot be rebuilt, and work beyond what was
asked, such as another module, another section of the paper, or an unrelated
cleanup. A request already given covers the action: when the user asked for a
commit or invoked `/commit`, do not confirm again.

Ordinary obstacles are not reasons to stop: errors, timeouts, failing tools,
empty results, a busy file. Diagnose them, then work through them with the
access you have. Deliberate blockers are different: a file protected by
`.claude/hooks/protect-files.sh`, a path marked not to be touched, access
withheld on purpose, a safety rule. Leave those alone, say what you found,
and look for another way to finish.

### Ask the User When

Ask before making a choice that the request and the documented specification
leave open, if it would change:

- estimates, identification, sample definitions, or manuscript claims;
- the structure of a quantitative or theory model: agents and their
  objectives, timing, state variables, functional forms, market structure,
  the equilibrium concept, or the assumptions behind a proposition;
- calibration targets, parameter values, or the solution or estimation
  method, including the solver algorithm, its tolerances, and its options.

A change the user explicitly asked for needs no question, even when estimates
move. Neither does a correction that restores the documented specification.
Resolve any other ambiguity with the documented default or the most
reasonable reading, and state the choice in the report.

### What Done Means

A task is done when the requested change is made, the checks relevant to what
changed have been run and pass, failures caused by the change are fixed, and
the report says what was verified and what was not. Choose checks by what
changed:

- code: build the relevant target with `make -C code/[task_group] [target]`
  and confirm the expected outputs exist and look plausible;
- a Makefile or its dependencies: a scoped `make -n`, then the build;
- LaTeX: `make -C latex`, with no undefined citations or missing inputs;
- instructions and documentation: no build.

Repeat a check only after a further change. If a check cannot be run, say so.

Write every reply and report for a reader who did not watch the work. Lead
with the outcome and what it means, give key numbers with units, name any
decision the reader has to make, and say in one line what was verified and
what was not. Leave out command logs and checklists, and keep it short.
`Reports and Updates` in `protocols/writing.md` has the full rule.

---

## Defects That Block a Commit or Merge

Fix these before a commit or merge. If the user wants to go ahead anyway,
name them in the report.

- a script, build, or compile that fails
- a wrong estimand, formula, objective, or moment condition
- an unguarded numerical error: NaN or Inf passing through, an unchecked
  solver exit status, or a gradient or Hessian with the wrong sign or
  dimension
- an unchecked merge or reshape (keys, match rates, panel structure)
- an absolute path, or stochastic code without a seed
- a computed result typed into the manuscript by hand, an undefined citation,
  or a missing `output/numbers/` input
- a Makefile with a missing prerequisite or a circular dependency

Everything else is advisory, including style, formatting, and line length.
Report it briefly and do not hold the work for it.

---

## Changed Numbers in the Manuscript

When a build can rewrite `output/numbers/`, record the macro definitions
beforehand and compare their contents afterward. Whenever a generated numeric
macro changes value, review every prose use of it as `latex/AGENTS.md`
describes, and report the old and new values.

---

## Records

Keep a record only when someone will use it.

- **Plan** -- for high-risk work, or when another session, person, or agent
  must pick the work up.
- **Handoff** (`quality_reports/handoffs/`, `templates/handoff.md`) -- only
  when context passes to another person, agent, branch, or session.
- **Session log** (`quality_reports/session_logs/`,
  `templates/session-log.md`) -- only when decisions must outlast the session.
- **Merge report** (`quality_reports/merges/`, `templates/quality-report.md`)
  -- only when the user asks for one at a merge.
- **`MEMORY.md`** -- a lesson that is specific to this project and likely to
  recur. Use `/learn`. Every entry states its reason and a review date;
  delete an entry once its reason no longer holds, because old cautions make
  agents hold back routine work.

After context compression or in a new session, follow
`protocols/skills/resume-custom.md`, then continue the task.

In the template repository itself, remove task-specific files under
`quality_reports/` before merging to `main`.
