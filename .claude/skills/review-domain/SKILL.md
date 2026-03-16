---
name: review-domain
description: Run the substantive domain review on manuscripts, slides, or lecture materials. Checks identification, derivations, citations, code-theory alignment, and logical consistency. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Domain Substance

Run the substantive domain review protocol (empirical microeconomics referee review).

## Steps

1. **Identify files to review:**
   - If `$ARGUMENTS` is a specific filename (`.tex`, `.qmd`, `.md`): review that file only
   - If `$ARGUMENTS` is `all`: review all `.tex` files in `latex/` (excluding `latex/latex_extras/`) plus any `.qmd` files

2. **For each file, launch the `domain-reviewer` agent** with instructions to:
   - Follow the full 5-lens protocol in the agent instructions
   - Check `literature/` for PDFs to verify citation fidelity (Lens 3)
   - Check `code/` for R scripts to verify code-theory alignment (Lens 4)
   - Check `latex/references/references.bib` for bibliography cross-referencing
   - Save report to `quality_reports/[FILENAME_WITHOUT_EXT]_substance_review.md`

3. **After all reviews complete**, present a summary:
   - Overall assessment (SOUND / MINOR ISSUES / MAJOR ISSUES / CRITICAL ERRORS)
   - Total issues found per file
   - Breakdown by severity (Critical / Major / Minor)
   - Top 3 most critical issues

4. **IMPORTANT: Do NOT edit any source files.**
   Only produce reports. Fixes are applied after user review.
