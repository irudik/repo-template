---
paths:
  - "**/*.R"
  - "**/*.jl"
  - "**/*.do"
  - "**/*.ado"
  - "**/*.m"
  - "code/**"
---

# Output Format Verification Guide

When comparing outputs before and after code changes (refactoring, style edits, etc.):

## Format Reference

| Format | Checksum-Stable? | How to Compare |
|--------|-----------------|----------------|
| CSV/TSV | Yes | MD5 checksum |
| RDS | No (R-version dependent) | Read and compare values, or convert to CSV |
| .dta | Partially | Read and compare values, or export to CSV first |
| .mat | Partially | Load and compare specific variables |
| JLD2 | Yes (Julia-version dependent) | MD5 or load-and-compare |
| PDF/PNG | No (renderer dependent) | Visual diff only |
| .tex (generated) | Yes | MD5 or text diff |

## Rules

- **Gold standard:** CSV checksums. Use these for refactoring verification.
- **Skip binary formats** (RDS, .mat, PDF, PNG) when checksumming -- they are not stable across software versions.
- **For .dta files:** compare via `haven::read_dta()`/`pandas.read_stata()` or export both versions to CSV first.
- **For .mat files:** load both versions and compare variable-by-variable with a tolerance (e.g., `max(abs(A - B)) < 1e-10`).
- **For RDS files:** read both into R and compare with `all.equal()` or convert to CSV first.
- **For figures:** visual inspection only. Do not checksum PDFs or PNGs.
