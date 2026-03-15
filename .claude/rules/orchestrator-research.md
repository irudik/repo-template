---
paths:
  - "**/*.do"
  - "**/*.ado"
  - "**/*.m"
  - "**/*.jl"
  - "code/**/*.R"
  - "code/**/*.do"
  - "code/**/*.jl"
  - "code/**/Makefile"
  - "latex/**/*.tex"
---

# Research Project Orchestrator (Simplified)

> **Routing:** Use this simplified loop for single-file R/Julia/Stata/MATLAB script tasks. For multi-file or cross-cutting changes, use `orchestrator-protocol.md` instead.

**For R/Julia/Stata/MATLAB scripts, simulations, and data analysis** -- use this simplified loop instead of the full multi-agent orchestrator.

## The Simple Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Run `make -n` to check staleness; build stale targets
  │         If Makefile exists: `make -C code/[dir] [target]` or `make -C latex`
  │         Otherwise: `Rscript` / `julia` / `stata -b do` / `matlab -batch` / `pdflatex` directly
  │         R scripts: runs without error, outputs created
  │         Julia scripts: runs without error, CSV/JLD2 created
  │         Stata scripts: runs without error, .dta/.csv/.tex outputs created
  │         MATLAB scripts: runs without error, .mat/.csv outputs created
  │         Simulations: set.seed / Random.seed! / set seed / rng reproducibility
  │         Plots: PDF/PNG created, correct format
  │         If verification fails → fix → re-verify
  │
  Step 3: SCORE — Apply quality-gates rubric
  │
  └── Score >= 80?
        YES → Done (commit when user signals)
        NO  → Fix blocking issues, re-verify, re-score
```

**No 5-round loops. No multi-agent reviews. Just: write, test, done.**

## Verification Checklist

- [ ] `make -n` shows no stale targets (or targets rebuilt successfully)
- [ ] Script runs without errors (R, Julia, Stata, and/or MATLAB)
- [ ] Language setup is explicit at top (`library()`, `using`, `version`, `rng`)
- [ ] No hardcoded absolute paths
- [ ] `set.seed()` / `Random.seed!()` / `set seed` / `rng()` once at top if stochastic
- [ ] Output files created at expected paths
- [ ] Tolerance checks pass (if applicable)
- [ ] No hardcoded computed results in manuscript prose (tex-reviewer)
- [ ] Quality score >= 80
