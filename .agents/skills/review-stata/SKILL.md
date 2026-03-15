---
name: review-stata
description: Run the Stata code review protocol on Stata scripts. Checks code quality, reproducibility, data-state safety, and professional standards. Produces a report without editing files.
workflow_stage: review
compatibility:
  - codex
  - claude-code
version: 1.0.0
tags:
  - stata
  - code-review
  - reproducibility
  - data-management
---

# Review Stata Scripts

Run the comprehensive Stata code review protocol.

## Steps

1. **Identify scripts to review:**
   - If an argument is a specific `.do` or `.ado` filename: review that file only
   - If the argument is `all`: review all Stata scripts in `code/`

2. **For each script, follow the review protocol below.**
   - Read `code/AGENTS.md` (or `.claude/rules/stata-code-conventions.md`) for current standards
   - Save report to `quality_reports/[script_name]_stata_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per script
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues

4. **IMPORTANT: Do NOT edit any Stata source files.**
   Only produce reports. Fixes are applied after user review.

---

## Review Protocol

You are a **Senior Principal Econometrician** with deep expertise in empirical microeconomics, panel data workflows, and research replication in Stata.

### Review Categories

#### 1. SCRIPT STRUCTURE & HEADER
- [ ] Header block present with: title, author, purpose, inputs, outputs
- [ ] Numbered top-level sections
- [ ] Logical flow: setup -> data load -> cleaning -> estimation -> export

**Flag:** Missing header fields, unnumbered sections, inconsistent divider style.

#### 2. CONSOLE OUTPUT HYGIENE
- [ ] `display` / `di` used sparingly
- [ ] No verbose printing inside loops or bootstrap/simulation blocks
- [ ] No `pause` or `set trace on` left in production code

**Flag:** Any noisy console output that obscures real warnings or errors.

#### 3. REPRODUCIBILITY
- [ ] `version` pinned near the top of each script/program
- [ ] `set more off` at the top of non-interactive scripts
- [ ] `set seed` called ONCE if stochastic
- [ ] All paths relative to repository root
- [ ] No hardcoded absolute paths or `cd`
- [ ] Local/temp macros preferred over globals

**Flag:** Missing `version`, multiple seeds, globals, hardcoded paths, `cd`.

#### 4. PROGRAM DESIGN & DOCUMENTATION
- [ ] Reusable logic wrapped in `program define` for non-trivial workflows
- [ ] Programs use `syntax` to validate inputs
- [ ] `tempfile`, `tempname`, and `tempvar` used instead of scratch filenames
- [ ] No magic numbers without explanation

**Flag:** Undocumented programs, brittle argument handling, duplicated logic, magic numbers.

#### 5. DATA INTEGRITY & DOMAIN CORRECTNESS
- [ ] Estimators match paper formulas (`latex/manuscript.tex`) when relevant
- [ ] `merge`, `joinby`, `append`, `collapse`, and `reshape` steps are validated
- [ ] Key uniqueness checked with `isid`, `duplicates report`, or assertions where needed
- [ ] Panel/time-series settings (`xtset` / `tsset`) are explicit when required
- [ ] Cluster, FE, and weight choices match the intended estimand

**Flag:** Unchecked merge state, wrong estimand, incorrect panel declaration, broken keys.

#### 6. OUTPUT PERSISTENCE
- [ ] Outputs saved via `save`, `export delimited`, `putexcel`, `esttab`, or `file write`
- [ ] Output paths point to canonical `output/` subdirectories
- [ ] Filenames are descriptive and scenario-specific where needed
- [ ] Dynamic-number exports for LaTeX use `file write`

**Flag:** Missing output saves, ad hoc filenames, outputs written outside `output/`.

#### 7. COMMENT QUALITY
- [ ] Comments explain **WHY**, not WHAT
- [ ] Section headers describe purpose
- [ ] No commented-out dead code
- [ ] Economic intuition is documented where non-obvious

**Flag:** WHAT-comments, dead code, missing intuition around transformations or estimands.

#### 8. ERROR HANDLING & STATE MANAGEMENT
- [ ] `capture` only used when followed by an `_rc` check
- [ ] `preserve` / `restore` are balanced
- [ ] `assert` or equivalent checks follow critical transformations
- [ ] Temporary files and frames are cleaned up or clearly scoped

**Flag:** Silenced failures, unmatched `preserve`, unchecked `_rc`, fragile state handling.

#### 9. PROFESSIONAL POLISH
- [ ] Consistent indentation and continuation style
- [ ] Lower-case command style is consistent
- [ ] Macro expansion uses correct quoting
- [ ] No hidden sort dependence; `sort` / `bysort` used explicitly before grouped work

**Flag:** Inconsistent style, quote bugs, order-dependent logic, uncontrolled globals.

---

### Report Format

Save report to `quality_reports/[script_name]_stata_review.md`:

```markdown
# Stata Code Review: [script_name].do
**Date:** [YYYY-MM-DD]
**Reviewer:** review-stata skill

## Summary
- **Total issues:** N
- **Critical:** N | **High:** N | **Medium:** N | **Low:** N

## Issues

### Issue 1: [Brief title]
- **File:** `[path/to/file.do]:[line_number]`
- **Category:** [Structure / Console / Reproducibility / Programs / Domain / Output / Comments / Errors / Polish]
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
| Program Design | Yes/No | N |
| Data Integrity & Domain Correctness | Yes/No | N |
| Output Persistence | Yes/No | N |
| Comments | Yes/No | N |
| Error Handling & State | Yes/No | N |
| Polish | Yes/No | N |
```

### Important Rules

1. **NEVER edit source files.** Report only.
2. **Be specific.** Include line numbers and exact code snippets.
3. **Be actionable.** Every issue must have a concrete proposed fix.
4. **Prioritize correctness.** Data integrity and estimand bugs outrank style issues.
