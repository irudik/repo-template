# AGENTS.md -- Academic Project Development with Codex CLI

<!-- HOW TO USE: Replace [BRACKETED PLACEHOLDERS] with your project info.
     Keep this file under 32KB -- Codex loads it every session.
     Code-specific conventions are in code/AGENTS.md.
     LaTeX-specific conventions are in latex/AGENTS.md. -->

**Project:** [YOUR PROJECT NAME]
**Institution:** [YOUR INSTITUTION]
**Branch:** main

---

## Core Principles

- **Plan first** -- think through the approach before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile/render and confirm output at the end of every task
- **Single source of truth** -- `latex/manuscript.tex` is authoritative for the paper
- **Quality gates** -- nothing ships below 80/100
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong -> right` to MEMORY.md

---

## Folder Structure

```
[YOUR-PROJECT]/
├── AGENTS.md                    # This file (Codex instructions)
├── CLAUDE.md                    # Claude Code instructions
├── MEMORY.md                    # Persistent [LEARN] entries across sessions
├── Makefile                     # Root -- delegates to code/ and latex/
├── .codex/                      # Codex CLI config and rules
│   ├── config.toml              # Model, sandbox, approval settings
│   └── rules/
│       └── default.rules        # Command execution permissions (Starlark)
├── .agents/                     # Codex skills
│   └── skills/                  # Skill definitions
├── .claude/                     # Claude Code rules, skills, agents, hooks
├── code/                        # Analysis code with sub-Makefiles
│   ├── AGENTS.md                # R/Julia/Stata/MATLAB/Makefile conventions (Codex)
│   ├── Makefile                 # Delegates to sub-Makefiles
│   └── [task_group]/            # e.g., data cleaning, estimation, figures
│       ├── Makefile
│       └── *.R, *.jl, *.do, *.ado, or *.m
├── latex/                       # Paper manuscript and slides
│   ├── AGENTS.md                # LaTeX conventions (Codex)
│   ├── Makefile                 # pdflatex 3-pass build
│   ├── manuscript.tex           # Main paper
│   ├── slides.tex               # Presentation slides
│   ├── latex_extras/            # Preamble files (packages, commands, tables)
│   └── references/              # .bib and .bst files
├── output/                      # Code pipeline outputs
│   ├── figures/                 # Generated figures
│   ├── tables/                  # Generated tables
│   └── numbers/                 # Inline numbers for manuscript (\newcommand .txt files)
├── quality_reports/             # Plans, session logs, merge reports
└── templates/                   # Session log, quality report templates
```

---

## Commands

```bash
# Make (preferred -- builds everything)
make                               # Build all (code + latex)
make -n                            # Dry-run: show what would be built
make -C code                       # Build all code targets
make -C code/[task_group] all      # Build one task group
make -C latex                      # Compile manuscript

# LaTeX (manual fallback -- 3-pass, pdflatex)
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
| `/commit [msg]` | Stage, commit, PR, merge |
| `/data-analysis [dataset]` | End-to-end R analysis |
| `/refactor [file-or-dir]` | Verify-refactor-verify loop |
| `/verify-outputs [script]` | Checksum outputs, compare to reference |
| `/compare-branches [b1] [b2]` | Cross-branch output comparison |
| `/resume` | Recover context after compression/new session |
| `/setup-makefile [dir]` | Generate Makefile from directory contents |
| `/review-r [file]` | R code quality review |
| `/review-julia [file]` | Julia code quality review |
| `/review-stata [file]` | Stata code quality review |
| `/review-matlab [file]` | MATLAB code quality review |
| `/review-tex [file]` | LaTeX manuscript review |
| `/review-makefile [file]` | Makefile conventions review |
| `/review-comments [path]` | Clean up comments, docstrings, dead code |
| `/review-domain [file]` | Substantive domain review (identification, citations, code-theory) -- opt-in |
| `/proofread [file]` | Grammar, typos, overflow, consistency check -- opt-in |
| `/review-pr [PR#]` | Address PR review comments, commit fixes, resolve threads |
| `/matlab-optim-derivatives` | Audit MATLAB optimization derivatives |

---

## Current Project State

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Manuscript | `latex/manuscript.tex` | Template | Paper skeleton with standard sections |
| Slides | `latex/slides.tex` | Template | Presentation template |
| Code pipeline | `code/` | Template | Sub-Makefiles to be added per project |

---

## Orchestrator Protocol: Contractor Mode

> Use this full loop for multi-file or cross-cutting changes. For single-file R/Julia/Stata/MATLAB script tasks, use the simplified research orchestrator below.

**After a plan is approved, the orchestrator takes over autonomously.**

### The Loop

```
Plan approved -> orchestrator activates
  |
  Step 1: IMPLEMENT -- Execute plan steps
  |
  Step 2: VERIFY -- Run `make -n` to check staleness; build stale targets
  |         If Makefile exists: `make -C code/[dir] [target]` or `make -C latex`
  |         Otherwise: compile/render/run directly
  |         If verification fails -> fix -> re-verify
  |
  Step 3: REVIEW -- Run appropriate review skill (/review-r, /review-julia, /review-stata, /review-matlab, /review-tex)
  |
  Step 4: FIX -- Apply fixes (critical -> major -> minor)
  |
  Step 5: RE-VERIFY -- Confirm fixes are clean
  |
  Step 6: SCORE -- Apply quality-gates rubric
  |
  └── Score >= threshold?
        YES -> Continue to Step 7
        NO  -> Loop back to Step 3 (max 5 rounds)
              After max rounds -> continue to Step 7 with remaining issues
  |
  Step 7: OPTIONAL REVIEWS -- If the approved plan requests them:
  |         * Domain substance review -> run domain-reviewer agent
  |         * Proofreading -> run proofreader agent
  |         These run once on the final state, after the review-fix loop.
  |         They produce reports only -- fixes require user review.
  |         Skip this step if the plan does not request optional reviews.
  |
  Step 8: Present summary to user (including optional review reports)
```

### Limits

- **Main loop:** max 5 review-fix rounds
- **Critic-fixer sub-loop:** max 5 rounds
- **Verification retries:** max 2 attempts
- Never loop indefinitely

### "Just Do It" Mode

When user says "just do it" / "handle it":
- Skip final approval pause
- Auto-commit if score >= 80
- Still run the full verify-review-fix loop
- Still present the summary

---

## Refactoring Protocol

### Constraints

- NEVER change solver tolerances, options, or convergence criteria
- NEVER rename variables in numerical/hot-loop code
- NEVER change function signatures without explicit approval
- NEVER remove dead code unless explicitly instructed (flag it in section headers instead)
- The ONLY acceptable refactoring outcome is identical output

### Verify-Refactor-Verify Loop

1. Run target script, record output checksums (CSV only -- skip binary formats like RDS, .mat, PDF)
2. Apply style changes per language convention rules
3. Re-run, compare checksums
4. If mismatch: revert and report -- do not attempt to fix the mismatch

### Approved Transformations

- Comment style (headers, borders, docstrings)
- Whitespace and indentation
- Variable grouping and section organization
- Adding missing documentation
- Language-specific style conventions

### Prohibited Transformations (without explicit approval)

- Changing algorithm logic or control flow
- Renaming function parameters or return values
- Modifying solver configuration or tolerances
- Removing or restructuring error handling
- Changing data types or precision

When in doubt, ask before changing.

---

## Solver Debugging Protocol

When debugging numerical solver failures (MATLAB, Julia, Python):

### Diagnostic Checklist (follow in order)

1. **Dimensions first** -- verify all matrices are conformable, vectors are correct length
2. **NaN/Inf trace** -- find the first operation that produces NaN; trace backward
3. **Finite-difference check** -- validate analytic gradients/Hessians before suspecting derivative bugs
4. **Condition number** -- check key matrices (Jacobian, Hessian) for ill-conditioning
5. **Boundary check** -- verify variables respect bounds (non-negative shares, probabilities in [0,1])
6. **Input data** -- confirm data fed to solver contains no NaN/Inf/missing values
7. **Initial guess** -- check that x0 is feasible (satisfies bounds and constraints)

### Do NOT

- Change tolerances or solver options as a diagnostic step
- Change the solver algorithm without explicit approval
- Propose fixes before completing the diagnostic checklist
- Guess at root causes -- show evidence

Present diagnosis with evidence, then proposed fix. Wait for approval before implementing.

---

## Output Verification Formats

When comparing outputs before and after code changes:

| Format | Checksum-Stable? | How to Compare |
|--------|-----------------|----------------|
| CSV/TSV | Yes | MD5 checksum |
| RDS | No (R-version dependent) | Read and compare values, or convert to CSV |
| .dta | Partially | Read and compare values, or export to CSV first |
| .mat | Partially | Load and compare specific variables |
| JLD2 | Yes (Julia-version dependent) | MD5 or load-and-compare |
| PDF/PNG | No (renderer dependent) | Visual diff only |
| .tex (generated) | Yes | MD5 or text diff |

**Gold standard:** CSV checksums. Use these for refactoring verification. Skip binary formats.

---

## Research Orchestrator (Simplified)

> Use this simplified loop for single-file R/Julia/Stata/MATLAB script tasks.

```
Plan approved -> orchestrator activates
  |
  Step 1: IMPLEMENT -- Execute plan steps
  |
  Step 2: VERIFY -- Run `make -n` to check staleness; build stale targets
  |         If Makefile exists: `make -C code/[dir] [target]` or `make -C latex`
  |         Otherwise: `Rscript` / `julia` / `stata -b do` / `matlab -batch` / `pdflatex` directly
  |         R scripts: runs without error, outputs created
  |         Julia scripts: runs without error, CSV/JLD2 created
  |         Stata scripts: runs without error, .dta/.csv/.tex outputs created
  |         MATLAB scripts: runs without error, .mat/.csv outputs created
  |         Simulations: set.seed / Random.seed! / set seed / rng reproducibility
  |         Plots: PDF/PNG created, correct format
  |         If verification fails -> fix -> re-verify
  |
  Step 3: SCORE -- Apply quality-gates rubric
  |
  └── Score >= 80?
        YES -> Done (commit when user signals)
        NO  -> Fix blocking issues, re-verify, re-score
```

**No 5-round loops. No multi-agent reviews. Just: write, test, done.**

### Verification Checklist

- [ ] `make -n` shows no stale targets (or targets rebuilt successfully)
- [ ] Script runs without errors (R, Julia, Stata, and/or MATLAB)
- [ ] Language setup is explicit at top (`library()`, `using`, `version`, `rng`)
- [ ] No hardcoded absolute paths
- [ ] `set.seed()` / `Random.seed!()` / `set seed` / `rng()` once at top if stochastic
- [ ] Output files created at expected paths
- [ ] Tolerance checks pass (if applicable)
- [ ] No hardcoded computed results in manuscript prose
- [ ] Quality score >= 80

---

## Plan-First Workflow

**For any non-trivial task, plan before writing code.**

### The Protocol

1. **Think through the approach** before coding
2. **Check MEMORY.md** for `[LEARN]` entries relevant to this task
3. **Draft the plan** -- what changes, which files, in what order
4. **Save to disk** -- write to `quality_reports/plans/YYYY-MM-DD_short-description.md`
5. **Manuscript review opt-in** -- if the task touches manuscript or slides (`latex/`), ask:
   - "Include domain substance review?" (runs `domain-reviewer` agent)
   - "Include proofreading?" (runs `proofreader` agent)
   - Record the answers in the saved plan under an `## Optional Reviews` section
6. **Present to user** -- wait for approval
7. **Implement via orchestrator** after approval

### Plans on Disk

Plans survive context loss. Save every plan to:

```
quality_reports/plans/YYYY-MM-DD_short-description.md
```

Format: Status (DRAFT/APPROVED/COMPLETED), approach, files to modify, verification steps.

### Context Management

- Prefer auto-compression over manual context clearing
- Save important context to disk before it is lost
- Use context clearing only when the working context is genuinely polluted

### Session Recovery

After compression or a new session:
1. Read `AGENTS.md` and the most recent plan in `quality_reports/plans/`
2. Check `git log --oneline -10` and `git diff`
3. State what you understand the current task to be

---

## Quality Gates & Scoring Rubrics

### LaTeX Manuscript (.tex)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | pdflatex compilation failure | -100 |
| Critical | Typo in equation | -25 |
| Critical | Undefined citation | -15 |
| Critical | Hardcoded result (macro exists but unused) | -15 |
| Critical | Overfull hbox > 10pt | -10 |
| Major | Missing bibliography entries | -5 |
| Major | Likely computed result with no macro | -5 |
| Major | output/numbers/ file missing from Makefile dependencies | -5 |
| Minor | Long lines (>100 chars) | -1 (EXCEPT documented math formulas) |

### R Scripts (.R)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax errors | -100 |
| Critical | Domain-specific bugs (wrong estimand, incorrect formula) | -30 |
| Critical | Numerical errors (division by zero, unguarded NaN propagation) | -25 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing set.seed() | -10 |
| Major | Missing figure generation | -5 |

### Julia Scripts (.jl)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Runtime errors | -100 |
| Critical | Domain-specific bugs (wrong estimand, incorrect formula) | -30 |
| Critical | Numerical errors (NaN propagation, catastrophic cancellation, wrong precision) | -25 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Type instability in hot loops | -15 |
| Major | Missing `Random.seed!()` | -10 |
| Major | Abstract-typed struct fields | -5 |
| Major | Missing persistence (no CSV/JLD2 export) | -5 |
| Minor | Unfused broadcasts (`.+` instead of `@.`) | -2 |
| Minor | Globals captured in loops without `let` | -2 |

### Stata Scripts (.do / .ado)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Runtime errors | -100 |
| Critical | Domain-specific bugs (wrong estimand, incorrect formula) | -30 |
| Critical | Unchecked merge/reshape invariants (keys, `_merge`, panel state) | -25 |
| Critical | Hardcoded absolute paths or `cd` | -20 |
| Major | Missing `version` | -10 |
| Major | Missing `set seed` (if stochastic) | -10 |
| Major | `capture` without `_rc` checks or heavy global macro dependence | -5 |
| Major | Missing output persistence | -5 |
| Minor | Noisy `display` / `pause` / `set trace on` in production | -2 |

### MATLAB Scripts (.m)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Runtime errors | -100 |
| Critical | Domain-specific bugs (wrong objective, incorrect moment conditions) | -30 |
| Critical | Asymmetric Hessian | -25 |
| Critical | Gradient/Hessian sign errors | -25 |
| Critical | Gradient/Hessian dimension mismatch | -25 |
| Critical | Hardcoded absolute paths | -20 |
| Critical | Unchecked solver exitflag | -20 |
| Critical | Index consistency errors (off-by-one, bounds/parameter mismatch) | -20 |
| Major | Missing NaN/Inf guards | -10 |
| Major | Missing `rng()` (if stochastic) | -10 |
| Major | Missing output persistence | -5 |
| Minor | `i`/`j` as loop variables | -2 |
| Minor | Missing semicolons (unsuppressed output) | -1 |

### Makefile

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Circular dependencies | -100 |
| Critical | Missing prerequisites (stale builds) | -30 |
| Major | Missing `.PHONY` on non-file targets | -10 |
| Major | Absolute paths | -10 |
| Major | Directories not using order-only prerequisites | -5 |

### Enforcement

- **Score < 80:** Block commit. List blocking issues.
- **Score < 90:** Allow commit, warn. List recommendations.
- User can override with justification.

### Tolerance Thresholds (Research)

<!-- Customize for your domain -->

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Point estimates | [e.g., 1e-6] | [Numerical precision] |
| Standard errors | [e.g., 1e-4] | [MC variability] |
| Coverage rates | [e.g., +/- 0.01] | [MC with B reps] |

---

## Task Completion Verification Protocol

**At the end of EVERY task, verify the output works correctly.** This is non-negotiable.

### Make-First Verification

If a Makefile governs the files being modified:
1. Run `make -n` from the relevant directory to check what is stale
2. Build stale targets: `make -C code/[subdir] [target]` or `make -C latex`
3. Check exit code -- non-zero is a hard failure
4. Then proceed to file-specific checks below

### For LaTeX Manuscript:
1. Compile with `make -C latex` (preferred). Check for errors
2. Verify PDF was generated with non-zero size
3. Check for overfull hbox warnings
4. Check for undefined citations
5. Run `/review-tex` to check for hardcoded numbers in prose
6. Verify all dynamic number `\input{...}` files exist in `output/numbers/`

### For R Scripts:
1. Prefer `make -C code/[subdir] [target]`; fall back to `Rscript path/to/script.R`
2. Verify output files (PDF, RDS, CSV) were created with non-zero size
3. Spot-check estimates for reasonable magnitude

### For Julia Scripts:
1. Prefer `make -C code/[subdir] [target]`; fall back to `julia path/to/script.jl`
2. Verify output files (CSV, JLD2) were created with non-zero size
3. Check file sizes are plausible (not suspiciously small or empty)
4. If stochastic, verify reproducibility: run twice with same seed, diff outputs

### For Stata Scripts:
1. Prefer `make -C code/[subdir] [target]`; fall back to `stata -b do path/to/script.do`
2. Verify output files (`.dta`, `.csv`, `.tex`, `.txt`, or logs used downstream) were created with non-zero size
3. Check the batch log for Stata error codes and unexpected warnings
4. Spot-check key counts, merge assertions, or exported estimates for reasonable magnitude

### For MATLAB Scripts:
1. Prefer `make -C code/[subdir] [target]`; fall back to `matlab -batch "run('path/to/script.m')"`
2. Verify output files (`.mat`, `.csv`, `.tex`, or figures) were created with non-zero size
3. Check file sizes are plausible and solver output/logs show successful convergence where relevant

### Verification Checklist:
```
[ ] Output file created successfully
[ ] No compilation/render errors
[ ] Images/figures display correctly
[ ] Reported results to user
```

---

## Session Logging

**Location:** `quality_reports/session_logs/YYYY-MM-DD_description.md`
**Template:** `templates/session-log.md`

### Three Triggers (all proactive)

1. **Post-Plan Log** -- After plan approval, immediately capture: goal, approach, rationale, key context.
2. **Incremental Logging** -- Append 1-3 lines whenever: a design decision is made, a problem is solved, the user corrects something, or the approach changes. Do not batch.
3. **End-of-Session Log** -- When wrapping up: high-level summary, quality scores, open questions, blockers.

### Quality Reports

Generated **only at merge time** -- not at every commit or PR.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md` using `templates/quality-report.md`.

---

## Command Conventions

Issue one command per shell execution. Do not chain commands with `&&` or `;`. This keeps command execution predictable and matches the permission rules in `.codex/rules/default.rules`.

- **Independent commands** -- issue in parallel when possible (e.g., `git status` and `git diff`)
- **Dependent commands** -- issue sequentially, waiting for each result before the next (e.g., `git add` then `git commit`)

---

## Replication-First Protocol

**Core principle:** Replicate original results to the dot BEFORE extending.

### Phase 1: Inventory & Baseline

Before writing any code:
- Read the paper's replication README
- Inventory replication package: language, data files, scripts, outputs
- Record gold standard numbers from the paper
- Store targets in `quality_reports/[project]_replication_targets.md` or as RDS

### Phase 2: Translate & Execute

- Follow code conventions for all coding standards
- Translate line-by-line initially -- don't "improve" during replication
- Match original specification exactly
- Save all intermediate results as RDS or JLD2

#### Stata to R Translation Pitfalls

| Stata | R | Trap |
|-------|---|------|
| `reg y x, cluster(id)` | `feols(y ~ x, cluster = ~id)` | Stata clusters df-adjust differently from some R packages |
| `areg y x, absorb(id)` | `feols(y ~ x \| id)` | Check demeaning method matches |
| `probit` for PS | `glm(family=binomial(link="probit"))` | R default logit differs from probit defaults in some workflows |
| `bootstrap, reps(999)` | Depends on method | Match seed, reps, and bootstrap type exactly |

### Phase 3: Verify Match

| Type | Tolerance | Rationale |
|------|-----------|-----------|
| Integers (N, counts) | Exact match | No reason for any difference |
| Point estimates | < 0.01 | Rounding in paper display |
| Standard errors | < 0.05 | Bootstrap/clustering variation |
| P-values | Same significance level | Exact p may differ slightly |
| Percentages | < 0.1pp | Display rounding |

**If mismatch:** Do NOT proceed to extensions. Isolate which step introduces the difference.

#### Replication Report

Save to `quality_reports/[project]_replication_report.md`:

```markdown
# Replication Report: [Paper Author (Year)]
**Date:** [YYYY-MM-DD]
**Original language:** [Stata/R/etc.]
**R translation:** [script path]

## Summary
- **Targets checked / Passed / Failed:** N / M / K
- **Overall:** [REPLICATED / PARTIAL / FAILED]

## Results Comparison

| Target | Paper | Ours | Diff | Status |
|--------|-------|------|------|--------|

## Discrepancies (if any)
- **Target:** X | **Investigation:** ... | **Resolution:** ...

## Environment
- R version, key packages (with versions), data source
```

### Phase 4: Only Then Extend

After replication is verified (all targets PASS), commit and begin extensions.

---

## Workflow Quick Reference

**Model:** Contractor (you direct, Codex orchestrates)

```
Your instruction -> [PLAN] (if needed) -> Your approval -> [EXECUTE] -> [REPORT] -> Repeat
```

**Ask the user when:** Design forks, code ambiguity, replication edge cases, scope questions.
**Just execute when:** Obvious fixes, verification, documentation, plotting, deployment.
