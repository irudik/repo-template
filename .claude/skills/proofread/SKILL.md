---
name: proofread
description: Run expert proofreading on academic documents. Checks grammar, typos, overflow risks, citation consistency, and academic quality. Supports LaTeX, Quarto, PDF, and Markdown. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Proofread Academic Documents

Run the expert proofreading protocol on academic writing.

## Steps

1. **Identify files to proofread:**
   - If `$ARGUMENTS` is a specific filename: proofread that file only
   - If `$ARGUMENTS` is `all`: proofread all `.tex` files in `latex/` (excluding `latex/latex_extras/`) plus any `.qmd` files

2. **For each file, launch the `proofreader` agent** with instructions to:
   - Follow the full protocol in the agent instructions
   - Check all 5 categories: Grammar, Typos, Overflow/Formatting, Consistency, Academic Quality
   - Cross-reference citation keys against the bibliography file
   - Save report to `quality_reports/[FILENAME_WITHOUT_EXT]_proofread_report.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per file
   - Breakdown by category (Grammar / Typo / Overflow / Consistency / Academic Quality)
   - Breakdown by severity (High / Medium / Low)
   - Top 3 most critical issues

4. **IMPORTANT: Do NOT edit any source files.**
   Only produce reports. Fixes are applied after user review.
