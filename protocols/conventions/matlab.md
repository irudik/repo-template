# MATLAB Conventions

Read alongside `protocols/conventions/shared.md`.

## Setup and Function Design

- In stochastic scripts, call `rng(YYYYMMDD)` once at the top. Never call `rng()` inside loops or objective and constraint functions, because resetting the generator mid-run repeats identical draws across replications or introduces discontinuities across solver steps; if a simulated objective needs fixed draws across evaluations, draw the shocks once beforehand and pass them in through `data` or `Params` (resetting inside a standalone test script is fine).
- Pass configuration and tuning values in a `Params` struct rather than unnamed constants, and check critical matrix dimensions with `assert()`.
- Match objective functions, moments, and constraints to `latex/manuscript.tex`.

## Solvers and Numerical Checks

- When a project keeps two solver paths (such as KNITRO and `fmincon`) under a configuration flag for cross-checking, build solver option paths with `fullfile()` and match the Hessian callback to the active solver's wrapper signature.
- Check `exitflag > 0` (or the solver's documented convergence code) after every optimization call, check inputs and outputs for `NaN` and `Inf`, and symmetrize Hessians (`H = (H + H') / 2`) when numerical noise introduces slight asymmetry.
- When dropping or trimming observations, apply the same logical mask across all parallel vectors and matrices.

## Output Paths

Task-group scripts run from the script working directory (usually `code/[task_group]/`). Define `output_root` once (or wrap it in `Params.outputdir`) and write into the repository-root `output/` subdirectories:

```matlab
output_root = fullfile("..", "..", "output");

writetable(results, fullfile(output_root, "tables", "results.csv"));
writematrix(data, fullfile(output_root, "tables", "output.csv"));
save(fullfile(output_root, "tables", "results.mat"), "results", "params");
```

Save tables, `.mat` files, and number macros that later steps or reproduction need, rather than every intermediate workspace variable. Let the Makefile create output directories.
