---
paths:
  - "latex/**/*.tex"
  - "code/**"
---

# Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** This is non-negotiable.

## Make-First Verification

If a Makefile governs the files being modified:
1. Run `make -n` from the relevant directory to check what is stale
2. Build stale targets: `make -C code/[subdir] [target]` or `make -C latex`
3. Check exit code — non-zero is a hard failure
4. Then proceed to file-specific checks below

## For LaTeX Manuscript:
1. Compile with `make -C latex` (preferred — handles TEXINPUTS/BIBINPUTS/BSTINPUTS automatically). For manual runs, first `export TEXINPUTS=.:./latex_extras/:../output/numbers/:../output/tables/:../output/figures/:`, `export BIBINPUTS=./references/:`, and `export BSTINPUTS=./references/:` from the `latex/` directory. Check for errors
2. Verify PDF was generated with non-zero size
3. Check for overfull hbox warnings
4. Check for undefined citations
5. Run tex-reviewer agent to check for hardcoded numbers in prose
6. Verify all dynamic number `\input{...}` files exist in `output/numbers/` and are listed in `latex/Makefile` SOURCES (or covered by TEXINPUTS)

## For R Scripts:
1. Prefer `make -C code/[subdir] [target]` if a Makefile governs the script; fall back to `Rscript path/to/script.R`
2. Verify output files (PDF, RDS, CSV) were created with non-zero size
3. Spot-check estimates for reasonable magnitude

## For Julia Scripts:
1. Prefer `make -C code/[subdir] [target]` if a Makefile governs the script; fall back to `julia path/to/script.jl`
2. Verify output files (CSV, JLD2) were created with non-zero size
3. Check file sizes are plausible (not suspiciously small or empty)
4. If stochastic, verify reproducibility: run twice with same seed, diff outputs

## For Stata Scripts:
1. Prefer `make -C code/[subdir] [target]` if a Makefile governs the script; fall back to `stata -b do path/to/script.do`
2. Verify output files (`.dta`, `.csv`, `.tex`, `.txt`, or logs used downstream) were created with non-zero size
3. Check the batch log for Stata error codes and unexpected warnings
4. Spot-check key counts, merge assertions, or exported estimates for reasonable magnitude

## For MATLAB Scripts:
1. Prefer `make -C code/[subdir] [target]` if a Makefile governs the script; fall back to `matlab -batch "run('path/to/script.m')"`
2. Verify output files (`.mat`, `.csv`, `.tex`, or figures) were created with non-zero size
3. Check file sizes are plausible and solver output/logs show successful convergence where relevant

## Common Pitfalls:
- **Relative paths**: Always use paths relative to the Makefile's directory
- **Assuming success**: Always verify output files exist AND contain correct content

## Verification Checklist:
```
[ ] Output file created successfully
[ ] No compilation/render errors
[ ] Images/figures display correctly
[ ] Reported results to user
```
