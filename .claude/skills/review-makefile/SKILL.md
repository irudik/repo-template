---
name: review-makefile
description: Run the Makefile review protocol. Checks conventions, dependency correctness, script coverage, and build system quality. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[path/to/Makefile or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Makefiles

Run the comprehensive Makefile review protocol.

## Steps

1. **Identify Makefiles to review:**
   - If `$ARGUMENTS` is a specific Makefile path: review that file only
   - If `$ARGUMENTS` is `all`: review all Makefiles in the project (root, `code/`, `code/*/`, `latex/`)

2. **For each Makefile, launch the `makefile-reviewer` agent** with instructions to:
   - Follow the full protocol below
   - Read `.claude/rules/makefile-conventions.md` (or `code/AGENTS.md`) for current standards
   - Scan all scripts in the same directory for coverage checking
   - Save report to `quality_reports/[dir_name]_makefile_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per Makefile
   - Breakdown by severity (Critical / High / Medium / Low)
   - Orphaned scripts (scripts with no Makefile target)

4. **IMPORTANT: Do NOT edit any Makefiles.**
   Only produce reports. Fixes are applied after user review.

---

## Review Protocol

You are a **Senior Build Engineer** with deep expertise in GNU Make for academic research pipelines.

### Review Categories

#### 1. STRUCTURE
- [ ] `all` is the default (first) target
- [ ] `clean` target exists
- [ ] `.PHONY` declared for all non-file targets
- [ ] Logical ordering: variables, targets, pattern rules, clean

#### 2. DIRECTORY CREATION
- [ ] Output directories use order-only prerequisites (`| output/dir`)
- [ ] Directory creation uses `mkdir -p $@`
- [ ] Scripts do NOT create directories

#### 3. DEPENDENCY CORRECTNESS
- [ ] No circular dependencies
- [ ] All prerequisites exist or have rules
- [ ] Cross-directory dependencies use `$(MAKE) -C`
- [ ] Input data files listed as prerequisites

#### 4. SCRIPT COVERAGE
- [ ] Every `.R`, `.jl`, `.do`, `.ado`, `.m` file has a corresponding target
- [ ] No orphaned scripts
- [ ] Excluded scripts (utilities, shared libraries) documented

#### 5. JOINT PRODUCTION
- [ ] Multi-output scripts: one target with recipe, secondary with empty recipe (`;`)
- [ ] No duplicate recipes for the same script

#### 6. RECIPE CONVENTIONS
- [ ] R: `Rscript $<`, Julia: `julia $<`, Stata: `stata -b do $<`, MATLAB: `matlab -batch "run('$<')"`
- [ ] Automatic variables used (`$<`, `$@`)
- [ ] No absolute paths

#### 7. EXPENSIVE INTERMEDIATES
- [ ] `.PRECIOUS` on files that take minutes+ to regenerate

#### 8. DELEGATION (parent Makefiles)
- [ ] `$(MAKE) -C` for subdirectories
- [ ] Subdirectories in a variable for maintainability

#### 9. PROFESSIONAL POLISH
- [ ] Tabs for recipes (not spaces)
- [ ] Comments on non-obvious targets
- [ ] Variables at top

---

### Report Format

Save report to `quality_reports/[dir_name]_makefile_review.md`:

```markdown
# Makefile Review: [path/to/Makefile]
**Date:** [YYYY-MM-DD]
**Reviewer:** review-makefile skill

## Summary
- **Total issues:** N
- **Critical:** N | **High:** N | **Medium:** N | **Low:** N

## Issues

### Issue 1: [Brief title]
- **File:** `[path/to/Makefile]:[line_number]`
- **Category:** [Structure / Directories / Dependencies / Coverage / JointProd / Recipes / Precious / Delegation / Polish]
- **Severity:** [Critical / High / Medium / Low]
- **Current:** [code snippet]
- **Proposed fix:** [corrected code snippet]
- **Rationale:** [Why this matters]

## Checklist Summary
| Category | Pass | Issues |
|----------|------|--------|
| Structure | Yes/No | N |
| Directory Creation | Yes/No | N |
| Dependency Correctness | Yes/No | N |
| Script Coverage | Yes/No | N |
| Joint Production | Yes/No | N |
| Recipe Conventions | Yes/No | N |
| Expensive Intermediates | Yes/No | N |
| Delegation | Yes/No | N |
| Polish | Yes/No | N |
```

### Important Rules

1. **NEVER edit Makefiles.** Report only.
2. **Be specific.** Include line numbers.
3. **Be actionable.** Every issue needs a concrete proposed fix.
4. **Prioritize correctness.** Circular deps > missing prereqs > style.
