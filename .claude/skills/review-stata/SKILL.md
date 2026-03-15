---
name: review-stata
description: Run the Stata code review protocol on Stata scripts. Checks code quality, reproducibility, data-state safety, and professional standards. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review Stata Scripts

Run the comprehensive Stata code review protocol.

## Steps

1. **Identify scripts to review:**
   - If `$ARGUMENTS` is a specific `.do` or `.ado` filename: review that file only
   - If `$ARGUMENTS` is `all`: review all Stata scripts in `code/`

2. **For each script, launch the `stata-reviewer` agent** with instructions to:
   - Follow the full protocol in the agent instructions
   - Read `.claude/rules/stata-code-conventions.md` for current standards
   - Save report to `quality_reports/[script_name]_stata_review.md`

3. **After all reviews complete**, present a summary:
   - Total issues found per script
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues

4. **IMPORTANT: Do NOT edit any Stata source files.**
   Only produce reports. Fixes are applied after user review.
