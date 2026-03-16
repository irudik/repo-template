---
paths:
  - "**/*.m"
  - "code/**/*.m"
---

# MATLAB Code Standards

**Standard:** Senior Principal Computational Scientist + PhD researcher quality

---

## 1. Reproducibility

- `rng()` called ONCE at top if stochastic operations are present (never inside loops/functions)
- All paths relative to repository root
- Path construction uses `filesep` or `fullfile()` for cross-platform compatibility
- No hardcoded absolute paths (e.g., `/Users/...`, `C:\Users\...`)
- Rely on the Makefile to make directories (when Makefiles exist)

## 2. Function Design

- Consistent naming convention (`snake_case` matching existing codebase)
- Comment-block docstring immediately after function signature:
  ```matlab
  function [obj, grad, H] = objective_fn(x, data, Params)
  % OBJECTIVE_FN  Compute objective, gradient, and Hessian.
  %
  %   [obj, grad, H] = objective_fn(x, data, Params)
  %
  %   Inputs:
  %     x      - Parameter vector (N x 1)
  %     data   - Structure with fields: ...
  %     Params - Configuration structure with fields: ...
  %
  %   Outputs:
  %     obj  - Scalar objective value
  %     grad - Gradient vector (N x 1)
  %     H    - Hessian matrix (N x N)
  ```
- Use `Params` struct for configuration and tuning values (no magic numbers)
- Input validation via `assert()` for critical dimensions:
  ```matlab
  assert(length(x) == Params.n_params, 'Parameter vector dimension mismatch');
  assert(size(W, 1) == size(W, 2), 'Weighting matrix must be square');
  ```

## 3. Domain Correctness

- Verify objective function implementations match paper formulas (`latex/manuscript.tex`)
- Check known package/solver bugs (document below in Common Pitfalls)

## 4. Solver Configuration

Projects using optimization should follow a dual-solver pattern (e.g., KNITRO + fmincon) controlled by a configuration flag:

```matlab
if Params.useknitro
    % KNITRO path with analytic Hessian
    extended_features.HessFcn = @(x, lambda) hessian_fn(x, data, Params);
    [x, fval, exitflag, output] = knitro_nlp(...);
else
    % fmincon path
    options = optimoptions('fmincon', 'Algorithm', 'interior-point', ...
        'SpecifyObjectiveGradient', true, ...
        'HessianFcn', @(x, lambda) hessian_fn(x, data, Params));
    [x, fval, exitflag, output] = fmincon(...);
end
```

Key requirements:
- `.opt` file path constructed with `filesep` or `fullfile()`
- `extended_features.HessFcn` callback matches the Hessian wrapper signature
- Both solver paths should produce consistent results
- Always check `exitflag` after solver call

## 5. Output Paths

All code outputs go to canonical subdirectories under `output/`:

```matlab
% Tables / CSV
writetable(results, fullfile("output", "tables", "results.csv"));

% Matrix data
writematrix(data, fullfile("output", "tables", "output.csv"));

% MATLAB binary
save(fullfile("output", "tables", "results.mat"), "results", "params");
```

Projects with a `Params` struct may wrap these paths (e.g., `Params.outputdir` instead of `"output"`), but the canonical subdirectories (`tables/`, `figures/`, `numbers/`) remain the same.

## 6. Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Hardcoded absolute paths | Breaks on other machines | Use relative paths with `filesep` |
| Unchecked solver `exitflag` | **Silent convergence failure (Critical, -20)** | Always check `exitflag > 0` after solve |
| Missing NaN/Inf guards | Solver crashes or wrong results | Check data before and output after optimization |
| Inconsistent index trimming | Wrong data alignment after NaN removal | Trim all parallel arrays identically |
| `disp()`/`fprintf()` in production | Noisy console output | Remove or guard with verbose flag |
| `i`/`j` as loop variables | Shadows complex unit | Use `ii`, `jj`, `kk` or descriptive names |
| Asymmetric Hessian | **Silently wrong results (Critical, -25)** | Verify `H == H'` or symmetrize: `H = (H + H') / 2` |
| Missing semicolons | Unwanted console output | End assignment lines with `;` |

## 7. Line Length & Mathematical Exceptions

**Standard:** Keep lines <= 120 characters.

**Exception: Mathematical Formulas** -- lines may exceed 120 chars **if and only if:**

1. Breaking the line would harm readability of the math (gradient computations, Hessian blocks, moment conditions)
2. An inline comment explains the mathematical operation
3. The line is in a numerically intensive section (objective functions, gradient/Hessian computation)

**Quality Gate Impact:**
- Long lines in non-mathematical code: minor penalty (-1 to -2 per line)
- Long lines in documented mathematical sections: no penalty

## 8. Code Quality Checklist

```
[ ] rng() once at top (if stochastic)
[ ] All paths relative with filesep/fullfile()
[ ] Functions documented (comment-block docstrings)
[ ] Solver exitflag checked after every optimization call
[ ] NaN/Inf guards on data input and solver output
[ ] Hessian symmetry verified
[ ] Output files saved (writetable/writematrix/save)
[ ] Comments explain WHY not WHAT
[ ] No magic numbers (use Params struct)
[ ] Semicolons on all assignment lines
```
