---
name: review-tex
description: Run the LaTeX review protocol on manuscript and slides. Checks for hardcoded numbers, citation consistency, and compilation issues. Auto-fixes unambiguous hardcoded values; produces a report for ambiguous cases.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review LaTeX Files

Run the comprehensive LaTeX review protocol focused on hardcoded numeric results.

## Steps

1. **Identify files to review:**
   - If `$ARGUMENTS` is a specific `.tex` filename: review that file only
   - If `$ARGUMENTS` is `all`: review all `.tex` files in `latex/`

2. **For each file, launch the `tex-reviewer` agent** with instructions to:
   - Follow the full protocol below
   - Check for hardcoded numbers that should use `\input` from `output/numbers/`
   - Check citation consistency against `latex/references/references.bib`
   - Save report to `quality_reports/[FILENAME_WITHOUT_EXT]_tex_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per file
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues

4. **IMPORTANT: Do NOT edit any LaTeX source files** unless auto-fixing (see Phase 2).

---

## Review Protocol

Detect hardcoded numeric results in LaTeX manuscript prose and, when possible, automatically replace them with dynamically generated macros from the code pipeline.

### Background

The project's code pipeline (R/Julia/Stata/MATLAB) generates `.txt` files containing `\newcommand` definitions in `output/numbers/`. The `latex/Makefile` sets `TEXINPUTS` to include `../output/numbers/`, so the manuscript uses plain filenames:

```latex
\input{revenue_estimate.txt}
% Then in prose:
% a U.S. carbon tariff raises \$\revenueEstimate\ billion
```

### Phase 1: Detection (Read-Only Scan)

**Step 1: Build the Dynamic Value Registry**
1. Glob for `output/numbers/*.txt` and all `\input{...}` lines in `.tex` files
2. Read each `.txt` file and extract `\newcommand` definitions
3. Build a registry: `{macro_name: value, ...}`

**Step 2: Scan Prose Sections**
Read the `.tex` files. For each line, skip if inside:
- Math environments: `equation`, `align`, `gather`, `multline`, inline `$...$`
- Table environments: `tabular`, `table`, `longtable`
- Preamble (before `\begin{document}`)
- Comment lines, `\ref`, `\eqref`, `\label`, `\cite` commands
- LaTeX layout commands: `\vspace`, `\hspace`, `\setcounter`, `\setlength`

**Step 3: Classify Numbers**

**Always OK (never flag):**
- Section/equation/figure/table references
- Years (1900--2100)
- Structural descriptors: "12-sector", "N-country", "3-digit"
- Numbers inside math or table environments
- Page numbers, ordinals in prose

**Suspicious (flag for review):**
- Dollar amounts: `\$N.NN` followed by "billion"/"million"/"trillion"
- Percentages: `N\%`, `N percent`, `N percentage points`
- Parenthetical numbers resembling standard errors: `(0.042)`
- Numbers preceded by result verbs: "raises", "increases", "lowers", "reduces"
- Decimal numbers in prose context

**Step 4: Cross-Reference Against Registry**
- If an existing macro holds approximately this value: **Critical** -- macro exists but prose uses hardcoded number
- If no matching macro: proceed to Phase 2

### Phase 2: Source Tracing and Auto-Fix

**Step 1: Trace the Source**
1. Grep `code/` for the numeric value, nearby variable names, or contextual keywords
2. Examine Makefiles to find which scripts produce output files
3. Identify the specific script and line that computes the value

**Step 2: Decide**
- **Auto-fix** if exactly one script clearly produces the value
- **Escalate to user** if multiple candidates, no match, or external source

**Step 3: Auto-Fix (When Source Is Clear)**
1. Add stats generation code to the source script
2. Update `latex/Makefile` SOURCES
3. Replace hardcoded number with macro in manuscript
4. Rebuild and verify the generated number matches

### Template State

If `output/numbers/` does not exist AND `code/` has no scripts, report:
> No code pipeline found. Hardcoded number detection is informational only.

---

### Report Format

```markdown
# Hardcoded Number Review: [FILENAME_WITHOUT_EXT].tex
**Date:** [YYYY-MM-DD]
**Reviewer:** review-tex skill

## Summary
- **Auto-fixed:** N
- **Escalated:** N
- **Clean:** No hardcoded results detected

## Auto-Fixed
[List: line, old value, new macro, generated value]

## Escalated Issues

### Issue N: [Brief description]
- **File:** `latex/[file]:[line_number]`
- **Severity:** [Critical / High / Medium]
- **Hardcoded value:** [the number]
- **Context:** [surrounding sentence]
- **Candidate sources:** [script paths, if any]
- **Action needed:** [What the user should decide]
```

### Severity Levels

| Severity | Condition | Quality Deduction |
|----------|-----------|-------------------|
| Critical | Macro exists but prose uses hardcoded number | -15 |
| High | Number is clearly a computed result but source not traced | -5 |
| Medium | Numbers do not match between hardcoded and dynamic | -5 |
