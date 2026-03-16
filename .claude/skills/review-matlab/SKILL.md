---
name: review-matlab
description: Run the MATLAB code review protocol on MATLAB scripts. Checks code quality, solver configuration, derivative correctness, and optimization patterns. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review MATLAB Scripts

Run the comprehensive MATLAB code review protocol.

## Steps

1. **Identify scripts to review:**
   - If `$ARGUMENTS` is a specific `.m` filename: review that file only
   - If `$ARGUMENTS` is `all`: review all MATLAB scripts in `code/` (exclude `code/unit_tests/` and `code/hpc/`)

2. **For each script, launch the `matlab-reviewer` agent** with instructions to:
   - Follow the full protocol below
   - Read `.claude/rules/matlab-code-conventions.md` (or `code/AGENTS.md`) for current standards
   - Save report to `quality_reports/[script_name]_matlab_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per script
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues

4. **IMPORTANT: Do NOT edit any MATLAB source files.**
   Only produce reports. Fixes are applied after user review.

---

## Review Protocol

You are a **Senior Principal Computational Scientist** (HPC/Big Tech caliber) who also holds a **PhD** with deep expertise in numerical optimization and scientific computing.

### Review Categories

#### 1. SCRIPT STRUCTURE & HEADER
- [ ] Header comment block present with: title, author, purpose, inputs, outputs
- [ ] Numbered top-level sections
- [ ] Logical flow: setup -> data load -> configure -> solve -> process results -> export

**Flag:** Missing header fields, unnumbered sections, inconsistent divider style.

#### 2. CONSOLE OUTPUT HYGIENE
- [ ] `disp()` used sparingly -- one per major section maximum
- [ ] No `display()`, `fprintf()`, or `sprintf()` for routine status updates
- [ ] No per-iteration printing inside optimization or simulation loops

**Flag:** ANY use of `display()` for non-debugging purposes, verbose `disp()` in loops.

#### 3. REPRODUCIBILITY
- [ ] `rng()` called ONCE at top if stochastic
- [ ] All paths relative to repository root
- [ ] Path construction uses `filesep` or `fullfile()`
- [ ] No hardcoded absolute paths

**Flag:** Multiple `rng()` calls, hardcoded absolute paths, platform-specific path separators.

#### 4. FUNCTION DESIGN & DOCUMENTATION
- [ ] Comment-block docstring after function signature
- [ ] Consistent naming convention (`snake_case`)
- [ ] No magic numbers (use `Params` struct)
- [ ] Input validation via `assert()` for critical dimensions

**Flag:** Undocumented functions, magic numbers, missing dimension checks.

#### 5. DOMAIN CORRECTNESS
- [ ] Objective function / estimation criterion matches paper formulas (`latex/manuscript.tex`)
- [ ] Constraints and boundary conditions correct
- [ ] Algorithm matches paper description

**Flag:** Implementation doesn't match theory, wrong objective, incorrect constraints.

#### 6. SOLVER CONFIGURATION
- [ ] Dual-solver paths (if applicable) consistent
- [ ] Option file paths constructed correctly
- [ ] Hessian callback wired correctly
- [ ] Bounds match parameter vector dimension

**Flag:** Mismatched solver paths, wrong option file, incorrect callback wiring.

#### 7. DERIVATIVE CORRECTNESS (Critical -- any failure here is commit-blocking)
- [ ] Objective returns `[obj, grad, H]` triplet consistently
- [ ] Hessian wrappers call main objective with correct flags
- [ ] Hessian is symmetric -- **asymmetry is -25, automatic commit block**
- [ ] Gradient/Hessian dimensions match parameter vector -- **mismatch is -25**
- [ ] No sign errors in gradient components -- **sign error is -25**
- [ ] Finite-difference validation passes (or unit tests exist)

**Flag (all Critical):** Asymmetric Hessian, dimension mismatch, sign errors. Any derivative failure produces silently wrong results and must block the commit.

#### 8. OUTPUT PERSISTENCE
- [ ] Results saved via `writetable()`, `writematrix()`, or `save()`
- [ ] Output paths constructed with `filesep` or `fullfile()`
- [ ] Descriptive filenames with scenario/parameter identifiers

**Flag:** Missing output saves, hardcoded output paths.

#### 9. COMMENT QUALITY
- [ ] Comments explain **WHY**, not WHAT
- [ ] No commented-out dead code

**Flag:** WHAT-comments, dead code, missing WHY-explanations.

#### 10. ERROR HANDLING & CONVERGENCE
- [ ] Solver `exitflag` checked after every optimization call -- **unchecked is -20, Critical**
- [ ] First-order optimality verified
- [ ] Data checked for NaN/Inf before solver
- [ ] Solver output checked for NaN/Inf after optimization
- [ ] `assert()` for dimension validation

**Flag:** Unchecked exitflag (Critical, -20), missing NaN/Inf guards (Major, -10).

#### 11. INDEX CONSISTENCY
- [ ] Parallel arrays trimmed identically when dropping NaN/Inf indices
- [ ] Matrix row/column removal is symmetric
- [ ] Parameter index arithmetic is correct
- [ ] Bounds vectors match parameter vector length -- **mismatch is -20, Critical**

**Flag (Critical, -20):** Inconsistent trimming, off-by-one errors, bounds/parameter mismatch. These produce wrong solver inputs and silently incorrect results.

#### 12. PROFESSIONAL POLISH
- [ ] Consistent indentation (4 spaces or consistent tab width)
- [ ] Lines under 120 characters (mathematical exceptions allowed)
- [ ] Semicolons used consistently to suppress output
- [ ] No `i`/`j` as loop variables (shadows complex unit)

**Flag:** Inconsistent style, unsuppressed output, shadowed builtins.

---

### Report Format

Save report to `quality_reports/[script_name]_matlab_review.md`:

```markdown
# MATLAB Code Review: [script_name].m
**Date:** [YYYY-MM-DD]
**Reviewer:** review-matlab skill

## Summary
- **Total issues:** N
- **Critical:** N | **High:** N | **Medium:** N | **Low:** N

## Issues

### Issue 1: [Brief title]
- **File:** `[path/to/file.m]:[line_number]`
- **Category:** [Structure / Console / Reproducibility / Functions / Domain / Solver / Derivatives / Output / Comments / Errors / Indexing / Polish]
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
| Solver Configuration | Yes/No | N |
| Derivative Correctness | Yes/No | N |
| Output Persistence | Yes/No | N |
| Comments | Yes/No | N |
| Error Handling | Yes/No | N |
| Index Consistency | Yes/No | N |
| Polish | Yes/No | N |
```

### Important Rules

1. **NEVER edit source files.** Report only.
2. **Be specific.** Include line numbers and exact code snippets.
3. **Be actionable.** Every issue must have a concrete proposed fix.
4. **Prioritize correctness.** Domain bugs > solver bugs > derivative bugs > style issues.
