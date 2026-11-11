# Stata Conventions

Read alongside `protocols/conventions/shared.md`.

## Setup and Program Design

- Pin `version` and `set more off` near the top of batch scripts, and call `set seed YYYYMMDD` once at the top when stochastic commands run.
- Never use `cd` inside project `.do` files, because changing Stata's working directory breaks relative paths later in the batch run; the only exception is wrapping a third-party command that requires its own directory and restoring the original directory immediately afterward.
- Prefer `local` macros and `syntax` arguments over `global` macros in analysis scripts, because globals persist across `.do` files and create hidden dependencies; reserve globals for session-wide configuration when unavoidable.
- Wrap reusable logic in `program define` validated with `syntax`, use `tempfile`, `tempname`, and `tempvar` for temporary files, scalars, and variables, and keep `preserve` / `restore` blocks short and balanced.

## Data Integrity and Estimation

- Match estimators, fixed effects, clustering, and weights to `latex/manuscript.tex`.
- Check key uniqueness before `merge` (`isid` or `duplicates report`), `assert` the expected `_merge` pattern afterward, and verify observation counts and keys after `reshape`.
- Declare panel or time-series structure with `xtset` or `tsset`, and sort explicitly (`sort` or `bysort`) before order-dependent grouped calculations.
- Never leave `capture` without an immediate `_rc` check in data construction or estimation steps, because unchecked `capture` silences real failures; omit the `_rc` check only on benign cleanup lines such as `capture log close` or `capture drop` before creating a variable.

## Output Paths

Task-group scripts run from the script working directory (usually `code/[task_group]/`). Define `output_root` once and write into the repository-root `output/` subdirectories:

```stata
local output_root "../../output"

save "`output_root'/tables/my_results.dta", replace
export delimited using "`output_root'/tables/my_results.csv", replace

file open fh using "`output_root'/numbers/my_estimate.txt", write text replace
file write fh "\newcommand{\myEstimate}{2.31}" _n
file close fh
```

Save datasets and estimates that later steps or reproduction need, rather than every intermediate dataset. Let the Makefile create output directories.
