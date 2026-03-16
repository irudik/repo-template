---
name: review-domain
description: Run the substantive domain review on manuscripts, slides, or lecture materials. Checks identification, derivations, citations, code-theory alignment, and logical consistency. Produces a report without editing files.
workflow_stage: review
compatibility:
  - codex
  - claude-code
version: 1.0.0
tags:
  - empirical-micro
  - identification
  - citations
  - domain-review
---

# Review Domain Substance

Run the substantive domain review protocol (empirical microeconomics referee review).

## Steps

1. **Identify files to review:**
   - If an argument is a specific filename (`.tex`, `.qmd`, `.md`): review that file only
   - If the argument is `all`: review all `.tex` files in `latex/` (excluding `latex/latex_extras/`) plus any `.qmd` files

2. **For each file, follow the domain review protocol:**
   - Apply all 5 lenses: Identification, Derivations, Citation Fidelity, Code-Theory Alignment, Backward Logic
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
