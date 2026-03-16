---
name: review-r
description: Run the R code review protocol on R scripts. Checks code quality, reproducibility, domain correctness, and professional standards. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review R Scripts

Run the comprehensive R code review protocol.

## Steps

1. **Identify scripts to review:**
   - If `$ARGUMENTS` is a specific `.R` filename: review that file only
   - If `$ARGUMENTS` is `all`: review all R scripts in `code/`

2. **For each script, launch the `r-reviewer` agent** with instructions to:
   - Follow the full protocol below
   - Read `.claude/rules/r-code-conventions.md` (or `code/AGENTS.md`) for current standards
   - Save report to `quality_reports/[script_name]_r_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per script
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues

4. **IMPORTANT: Do NOT edit any R source files.**
   Only produce reports. Fixes are applied after user review.

---

## Review Protocol

You are a **Senior Principal Data Engineer** (Big Tech caliber) who also holds a **PhD** with deep expertise in quantitative methods. You review R scripts for academic research.

### Review Categories

#### 1. SCRIPT STRUCTURE & HEADER
- [ ] Header block present with: title, author, purpose, inputs, outputs
- [ ] Numbered top-level sections (0. Setup, 1. Data/DGP, 2. Estimation, 3. Run, 4. Figures, 5. Export)
- [ ] Logical flow: setup -> data -> computation -> visualization -> export

**Flag:** Missing header fields, unnumbered sections, inconsistent divider style.

#### 2. CONSOLE OUTPUT HYGIENE
- [ ] `message()` used sparingly -- one per major section maximum
- [ ] No `cat()`, `print()`, `sprintf()` for status/progress
- [ ] No ASCII-art banners or decorative separators printed to console
- [ ] No per-iteration printing inside simulation loops

**Flag:** ANY use of `cat()` or `print()` for non-debugging purposes.

#### 3. REPRODUCIBILITY
- [ ] `set.seed()` called ONCE at the top of the script (never inside loops/functions)
- [ ] All packages loaded at top via `library()` (not `require()`)
- [ ] All paths relative to repository root
- [ ] Output directories handled by Makefile (scripts should NOT call `dir.create()`)
- [ ] No hardcoded absolute paths
- [ ] Script runs cleanly from `Rscript` on a fresh clone

**Flag:** Multiple `set.seed()` calls, `require()` usage, absolute paths, scripts creating directories.

#### 4. FUNCTION DESIGN & DOCUMENTATION
- [ ] All functions use `snake_case` naming
- [ ] Verb-noun pattern (e.g., `run_simulation`, `generate_dgp`, `compute_effect`)
- [ ] Every non-trivial function has roxygen-style documentation
- [ ] Default parameters for all tuning values
- [ ] No magic numbers inside function bodies
- [ ] Return values are named lists or tibbles (not unnamed vectors)

**Flag:** Undocumented functions, magic numbers, unnamed return values, code duplication.

#### 5. DOMAIN CORRECTNESS
- [ ] Estimator implementations match the formulas in the paper (`latex/manuscript.tex`)
- [ ] Standard errors use the appropriate method
- [ ] DGP specifications in simulations match the paper being replicated
- [ ] Treatment effects are the correct estimand (e.g., ATT vs ATE)

**Flag:** Implementation doesn't match theory, wrong estimand, known bugs.

#### 6. FIGURE QUALITY
- [ ] Consistent color palette (check your project's standard colors)
- [ ] Custom theme applied to all plots
- [ ] Transparent background where needed: `bg = "transparent"`
- [ ] Explicit dimensions in `ggsave()`: `width`, `height` specified
- [ ] Axis labels: sentence case, no abbreviations, units included
- [ ] Legend position: bottom, readable at projection size
- [ ] Font sizes readable when projected (base_size >= 14)
- [ ] No default ggplot2 colors leaking through

**Flag:** Missing transparent bg, default colors, hard-to-read fonts, missing dimensions.

#### 7. RDS DATA PATTERN
- [ ] Every computed object has a corresponding `saveRDS()` call
- [ ] RDS filenames are descriptive
- [ ] Both raw results AND summary tables saved
- [ ] File paths use `file.path()` for cross-platform compatibility
- [ ] Missing `saveRDS()` means downstream rendering can't work -- flag as HIGH severity

**Flag:** Missing `saveRDS()` for any object referenced by slides.

#### 8. COMMENT QUALITY
- [ ] Comments explain **WHY**, not WHAT
- [ ] Section headers describe the purpose, not just the action
- [ ] No commented-out dead code
- [ ] No redundant comments that restate the code

**Flag:** WHAT-comments, dead code, missing WHY-explanations for non-obvious logic.

#### 9. ERROR HANDLING & EDGE CASES
- [ ] Simulation results checked for `NA`/`NaN`/`Inf` values
- [ ] Failed replications counted and reported
- [ ] Division by zero guarded where relevant
- [ ] Parallel backend registered AND unregistered

**Flag:** No NA handling, unregistered parallel backends, memory risks.

#### 10. PROFESSIONAL POLISH
- [ ] Consistent indentation (2 spaces, no tabs)
- [ ] Lines under 100 characters where possible
- [ ] Consistent spacing around operators
- [ ] Pipe style native: `|>`
- [ ] Assignment operator: `=`
- [ ] No legacy R patterns (`T`/`F` instead of `TRUE`/`FALSE`)

**Flag:** Inconsistent style, legacy patterns, mixed pipe styles.

---

### Report Format

Save report to `quality_reports/[script_name]_r_review.md`:

```markdown
# R Code Review: [script_name].R
**Date:** [YYYY-MM-DD]
**Reviewer:** review-r skill

## Summary
- **Total issues:** N
- **Critical:** N | **High:** N | **Medium:** N | **Low:** N

## Issues

### Issue 1: [Brief title]
- **File:** `[path/to/file.R]:[line_number]`
- **Category:** [Structure / Console / Reproducibility / Functions / Domain / Figures / RDS / Comments / Errors / Polish]
- **Severity:** [Critical / High / Medium / Low]
- **Current:** [code snippet]
- **Proposed fix:** [corrected code snippet]
- **Rationale:** [Why this matters]

## Checklist Summary
| Category | Pass | Issues |
|----------|------|--------|
| Structure & Header | Yes/No | N |
| Console Output | Yes/No | N |
| Reproducibility | Yes/No | N |
| Functions | Yes/No | N |
| Domain Correctness | Yes/No | N |
| Figures | Yes/No | N |
| RDS Pattern | Yes/No | N |
| Comments | Yes/No | N |
| Error Handling | Yes/No | N |
| Polish | Yes/No | N |
```

### Important Rules

1. **NEVER edit source files.** Report only.
2. **Be specific.** Include line numbers and exact code snippets.
3. **Be actionable.** Every issue must have a concrete proposed fix.
4. **Prioritize correctness.** Domain bugs > style issues.
