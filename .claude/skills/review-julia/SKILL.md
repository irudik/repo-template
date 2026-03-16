---
name: review-julia
description: Run the Julia code review protocol on Julia scripts. Checks code quality, type stability, performance, and professional standards. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Julia Scripts

Run the comprehensive Julia code review protocol.

## Steps

1. **Identify scripts to review:**
   - If `$ARGUMENTS` is a specific `.jl` filename: review that file only
   - If `$ARGUMENTS` is `all`: review all Julia scripts in `code/`

2. **For each script, launch the `julia-reviewer` agent** with instructions to:
   - Follow the full protocol below
   - Read `.claude/rules/julia-code-conventions.md` (or `code/AGENTS.md`) for current standards
   - Save report to `quality_reports/[script_name]_julia_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per script
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues

4. **IMPORTANT: Do NOT edit any Julia source files.**
   Only produce reports. Fixes are applied after user review.

---

## Review Protocol

You are a **Senior Principal Computational Scientist** (HPC/Big Tech caliber) who also holds a **PhD** with deep expertise in quantitative methods and numerical computing.

### Review Categories

#### 1. SCRIPT STRUCTURE & HEADER
- [ ] Header block present with: title, author, purpose, inputs, outputs
- [ ] Numbered top-level sections
- [ ] Logical flow: setup -> data load -> computation -> process results -> export

**Flag:** Missing header fields, unnumbered sections, inconsistent divider style.

#### 2. CONSOLE OUTPUT HYGIENE
- [ ] `@info` / `@warn` / `@error` from `Logging` used sparingly
- [ ] No `println()`, `print()`, `@printf` for status/progress

**Flag:** ANY use of `println()` or `print()` for non-debugging purposes.

#### 3. REPRODUCIBILITY
- [ ] `Random.seed!()` called ONCE at top (never inside loops/functions)
- [ ] All dependencies loaded at top via `using` / `import`
- [ ] All paths relative via `joinpath()`
- [ ] No hardcoded absolute paths

**Flag:** Multiple `Random.seed!()` calls, hardcoded absolute paths, `require()` usage.

#### 4. FUNCTION DESIGN & DOCUMENTATION
- [ ] `snake_case` functions, `CamelCase` types
- [ ] Verb-noun pattern
- [ ] Triple-quoted docstrings with signature, arguments, return type
- [ ] Default parameters, no magic numbers
- [ ] Return `NamedTuple` or custom `struct` (not bare tuples)

**Flag:** Undocumented functions, magic numbers, bare tuple returns.

#### 5. DOMAIN CORRECTNESS
- [ ] Estimator/simulation implementations match paper formulas
- [ ] Float64 precision adequate for the computation
- [ ] Algorithm matches paper description

**Flag:** Implementation doesn't match theory, precision issues, wrong algorithm.

#### 6. DATA PERSISTENCE
- [ ] Every computed object has a corresponding `jldsave()` or `serialize()` call
- [ ] JLD2 filenames are descriptive
- [ ] Results saved as CSV for model output
- [ ] File paths use `joinpath()`

**Flag:** Missing persistence for computed objects, hardcoded paths.

#### 7. COMMENT QUALITY
- [ ] Comments explain **WHY**, not WHAT
- [ ] No commented-out dead code

**Flag:** WHAT-comments, dead code, missing WHY-explanations.

#### 8. ERROR HANDLING & EDGE CASES
- [ ] Results checked for `NaN` / `Inf` / `missing` / `nothing`
- [ ] `try`/`catch` for external I/O or numerical failures

**Flag:** No NaN/Inf handling, unguarded external I/O.

#### 9. PROFESSIONAL POLISH
- [ ] Consistent indentation (4 spaces)
- [ ] Lines under 92 characters (mathematical exceptions allowed)
- [ ] `eachindex(x)` instead of `1:length(x)`
- [ ] Unicode Greek letters for variable names

**Flag:** Inconsistent style, `1:length(x)` usage, mixed indentation.

#### 10. TYPE STABILITY & PERFORMANCE
- [ ] Hot functions verified with `@code_warntype`
- [ ] Struct fields have concrete types
- [ ] Module-level constants declared with `const`
- [ ] `@views` on array slices in loops
- [ ] Output arrays pre-allocated when size is known

**Flag:** Abstract-typed struct fields, missing `@views`, global captures in hot loops.

#### 11. MULTIPLE DISPATCH
- [ ] Dispatch on types preferred over if/elseif chains on type tags
- [ ] Shallow type hierarchies

**Flag:** Type-tag if/elseif chains, deep type hierarchies.

#### 12. BROADCASTING & FUSION
- [ ] `@.` macro used for multi-operation expressions
- [ ] No manual loops replacing broadcastable operations

**Flag:** Unfused broadcasts, manual loops replacing broadcastable ops.

---

### Report Format

Save report to `quality_reports/[script_name]_julia_review.md`:

```markdown
# Julia Code Review: [script_name].jl
**Date:** [YYYY-MM-DD]
**Reviewer:** review-julia skill

## Summary
- **Total issues:** N
- **Critical:** N | **High:** N | **Medium:** N | **Low:** N

## Issues

### Issue 1: [Brief title]
- **File:** `[path/to/file.jl]:[line_number]`
- **Category:** [Structure / Console / Reproducibility / Functions / Domain / Persistence / Comments / Errors / Polish / TypeStability / Dispatch / Broadcasting]
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
| Data Persistence | Yes/No | N |
| Comments | Yes/No | N |
| Error Handling | Yes/No | N |
| Polish | Yes/No | N |
| Type Stability | Yes/No | N |
| Multiple Dispatch | Yes/No | N |
| Broadcasting | Yes/No | N |
```

### Important Rules

1. **NEVER edit source files.** Report only.
2. **Be specific.** Include line numbers and exact code snippets.
3. **Be actionable.** Every issue must have a concrete proposed fix.
4. **Prioritize correctness.** Domain bugs > performance > style issues.
