---
paths:
  - "latex/**/*.tex"
  - "**/*.R"
  - "**/*.jl"
  - "**/*.do"
  - "**/*.ado"
  - "**/*.m"
  - "code/**"
  - "code/**/Makefile"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** -- good enough to save
- **90/100 = PR** -- ready for deployment
- **95/100 = Excellence** -- aspirational

## LaTeX Manuscript (.tex)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | pdflatex compilation failure | -100 |
| Critical | Typo in equation | -25 |
| Critical | Hardcoded result (macro exists but unused) | -15 |
| Critical | Undefined citation | -15 |
| Critical | Overfull hbox > 10pt | -10 |
| Major | Missing bibliography entries | -5 |
| Major | Likely computed result with no macro | -5 |
| Major | output/numbers/ file missing from Makefile dependencies | -5 |
| Minor | Long lines (>100 chars) | -1 (EXCEPT documented math formulas) |

## R Scripts (.R)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax errors | -100 |
| Critical | Domain-specific bugs (wrong estimand, incorrect formula) | -30 |
| Critical | Numerical errors (division by zero, unguarded NaN propagation) | -25 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing set.seed() | -10 |
| Major | Missing figure generation | -5 |

## Julia Scripts (.jl)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Runtime errors | -100 |
| Critical | Domain-specific bugs (wrong estimand, incorrect formula) | -30 |
| Critical | Numerical errors (NaN propagation, catastrophic cancellation, wrong precision) | -25 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Type instability in hot loops | -15 |
| Major | Missing `Random.seed!()` | -10 |
| Major | Abstract-typed struct fields | -5 |
| Major | Missing persistence (no CSV/JLD2 export) | -5 |
| Minor | Unfused broadcasts (`.+` instead of `@.`) | -2 |
| Minor | Globals captured in loops without `let` | -2 |

## Stata Scripts (.do / .ado)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Runtime errors | -100 |
| Critical | Domain-specific bugs (wrong estimand, incorrect formula) | -30 |
| Critical | Unchecked merge/reshape invariants (keys, `_merge`, panel state) | -25 |
| Critical | Hardcoded absolute paths or `cd` | -20 |
| Major | Missing `version` | -10 |
| Major | Missing `set seed` (if stochastic) | -10 |
| Major | `capture` without `_rc` checks or heavy global macro dependence | -5 |
| Major | Missing output persistence | -5 |
| Minor | Noisy `display` / `pause` / `set trace on` in production | -2 |

## MATLAB Scripts (.m)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Runtime errors | -100 |
| Critical | Domain-specific bugs (wrong objective, incorrect moment conditions) | -30 |
| Critical | Asymmetric Hessian | -25 |
| Critical | Gradient/Hessian sign errors | -25 |
| Critical | Gradient/Hessian dimension mismatch | -25 |
| Critical | Hardcoded absolute paths | -20 |
| Critical | Unchecked solver exitflag | -20 |
| Critical | Index consistency errors (off-by-one, bounds/parameter mismatch) | -20 |
| Major | Missing NaN/Inf guards | -10 |
| Major | Missing `rng()` (if stochastic) | -10 |
| Major | Missing output persistence | -5 |
| Minor | `i`/`j` as loop variables | -2 |
| Minor | Missing semicolons (unsuppressed output) | -1 |

## Makefile

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Circular dependencies | -100 |
| Critical | Missing prerequisites (stale builds) | -30 |
| Major | Missing `.PHONY` on non-file targets | -10 |
| Major | Absolute paths | -10 |
| Major | Directories not using order-only prerequisites | -5 |

## Enforcement

- **Score < 80:** Block commit. List blocking issues.
- **Score < 90:** Allow commit, warn. List recommendations.
- User can override with justification.

## Quality Reports

Generated **only at merge time**. Use `templates/quality-report.md` for format.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md`.

## Tolerance Thresholds (Research)

<!-- Customize for your domain -->

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Point estimates | [e.g., 1e-6] | [Numerical precision] |
| Standard errors | [e.g., 1e-4] | [MC variability] |
| Coverage rates | [e.g., +/- 0.01] | [MC with B reps] |
