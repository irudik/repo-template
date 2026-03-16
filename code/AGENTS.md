# Code Pipeline Conventions

These conventions apply to all scripts in `code/` and its subdirectories.

---

## R Code Standards

**Standard:** Senior Principal Data Engineer + PhD researcher quality

### 1. Reproducibility

- `set.seed()` called ONCE at top (YYYYMMDD format)
- All packages loaded at top via `library()` (not `require()`)
- All paths relative to repository root
- Rely on the Makefile to make directories

### 2. Function Design

- `snake_case` naming, verb-noun pattern
- Roxygen-style documentation
- Default parameters, no magic numbers
- Named return values (lists or tibbles)

### 3. Domain Correctness

<!-- Customize for your field's known pitfalls -->
- Verify estimator implementations match paper formulas (`latex/manuscript.tex`)
- Check known package bugs (document below in Common Pitfalls)

### 4. Visual Identity

```r
# --- Your institutional palette ---
plot_blue = "#4575b4"
plot_mid = "#ffffdf"
plot_red = "#d73027"
plot_purple = "#c51b7d"
plot_green = "#3a7813"
```

#### Fonts
```
sysfonts::font_add_google("Lato")
sysfonts::font_add_google("Fira Sans")
```

#### Custom Themes
```r
# Regular plots
main_theme <-
  theme_classic() +
  theme(
    legend.position = "none",
    title = element_text(size = 24),
    text = element_text(family = font_choice),
    axis.text.x = element_text(size = 30), axis.text.y = element_text(size = 30),
    axis.title.x = element_text(size = 30), axis.title.y = element_text(size = 30),
    panel.grid.minor.x = element_blank(), panel.grid.major.y = element_blank(),
    panel.grid.minor.y = element_blank(), panel.grid.major.x = element_blank(),
    axis.line = element_line(colour = "black"), axis.ticks = element_line(colour = "black"),
    plot.background = element_rect(fill = "#ffffff")
  )

# Maps
map_theme <-
  theme_void() +
  theme(
    legend.position = "bottom",
    legend.key.height = unit(.35, "cm"),
    legend.key.width = unit(.6, "cm"),
    legend.text = element_text(size = 8),
    text = element_text(family = "Lato"),
  )
```

#### Figure Dimensions (for slides template)
```r
# Maps
ggsave(filepath, width = 8, height = 4, bg = "transparent")
# Figures
ggsave(filepath, width = 8, height = 8, bg = "transparent")
```

### 5. Output Paths

All code outputs go to canonical subdirectories under `output/`:

```r
# Figures
ggsave(file.path("output", "figures", "my_plot.pdf"), width = 8, height = 8, bg = "transparent")

# Tables / RDS
saveRDS(result, file.path("output", "tables", "my_results.rds"))

# Inline numbers for manuscript (\newcommand .txt files)
writeLines("\\newcommand{\\myEstimate}{2.31}",
           file.path("output", "numbers", "my_estimate.txt"))
```

**Heavy computations saved as RDS; slide rendering loads pre-computed data.**

### 6. Common Pitfalls

<!-- Add your field-specific pitfalls here -->
| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Missing `bg = "transparent"` | White boxes on slides | Always include in ggsave() |
| Hardcoded paths | Breaks on other machines | Use relative paths |

### 7. Line Length & Mathematical Exceptions

**Standard:** Keep lines <= 120 characters.

**Exception:** Mathematical formulas may exceed 120 chars if breaking the line would harm readability, an inline comment explains the operation, and the line is in a numerically intensive section.

### 8. Code Quality Checklist

```
[ ] Packages at top via library()
[ ] set.seed() once at top
[ ] All paths relative
[ ] Functions documented (Roxygen)
[ ] Figures: transparent bg, explicit dimensions
[ ] RDS: every computed object saved
[ ] Comments explain WHY not WHAT
```

---

## Julia Code Standards

**Standard:** Senior Principal Computational Scientist + PhD researcher quality

### 1. Reproducibility

- `Random.seed!(YYYYMMDD)` called ONCE at top (YYYYMMDD format) **ONCE CHOOSING A SEED DO NOT CHANGE IT AGAIN**
- All dependencies loaded at top via `using` or `import`
- All paths relative to repository root using `joinpath()`
- Rely on the Makefile to make directories

### 2. Function Design

- `snake_case` for functions and variables, `CamelCase` for types and modules
- Verb-noun pattern (e.g., `run_simulation`, `generate_dgp`, `compute_effect`)
- Triple-quoted docstrings with signature, arguments, and return type
- Default parameters for all tuning values, no magic numbers
- Return `NamedTuple` or custom `struct` (not bare tuples)

### 3. Domain Correctness

<!-- Customize for your field's known pitfalls -->
- Verify estimator/simulation implementations match paper formulas (`latex/manuscript.tex`)
- Check known package bugs
- Be aware of Float64 precision differences vs R

### 4. Output Paths & Data Persistence

```julia
# Figures
savefig(joinpath("output", "figures", "my_plot.pdf"))

# Tables / data
CSV.write(joinpath("output", "tables", "my_results.csv"), df)

# Inline numbers for manuscript
open(joinpath("output", "numbers", "my_estimate.txt"), "w") do io
    println(io, "\\newcommand{\\myEstimate}{2.31}")
end
```

**Heavy computations saved to disk; downstream scripts load pre-computed data.**

Prefer JLD2 for Julia-native objects. Use CSV for model output. When saving parameterized results, include parameter values in filenames (ASCII only, strip hats).

### 5. Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Global variables in hot loops | Severe performance regression | Pass as arguments or use `const` |
| Abstract-typed struct fields | Type instability, slow dispatch | Always annotate fields with concrete types |
| `1:length(x)` instead of `eachindex(x)` | Off-by-one risk with OffsetArrays | Use `eachindex(x)` or `axes(x, dim)` |
| Unfused broadcasts | Allocates intermediates | Use `@.` macro |
| Missing `@views` on slices | Allocates copies | Wrap in `@views` |
| Hardcoded paths | Breaks on other machines | Use `joinpath()` with relative paths |

### 6. Line Length

**Standard:** Keep lines <= 92 characters (Julia community convention). Mathematical formulas may exceed 92 chars under the same conditions as R.

### 7. Type Stability & Performance

- Run `@code_warntype` on hot functions during development
- Struct fields must have concrete types (no `Any`, no abstract types)
- Use `const` for module-level constants
- Use `@views` to avoid allocating array slices in loops
- Pre-allocate output arrays when size is known

### 8. Broadcasting & Fusion

- Prefer `@.` macro for multi-operation broadcast expressions
- Use `map` / `reduce` / comprehensions for non-broadcastable transforms
- Avoid allocating intermediate arrays where fused broadcasts suffice

### 9. Code Quality Checklist

```
[ ] Dependencies loaded at top via using/import
[ ] Random.seed!() once at top
[ ] All paths relative via joinpath()
[ ] Functions documented (triple-quoted docstrings)
[ ] JLD2: every computed object saved
[ ] Comments explain WHY not WHAT
[ ] Struct fields have concrete types
[ ] Hot loops use @views and pre-allocation
[ ] Broadcasts fused with @. where applicable
```

---

## Stata Code Standards

**Standard:** Senior Principal Econometrician + PhD researcher quality

### 1. Reproducibility

- `version` pinned near the top of each script or program
- `set more off` in batch scripts
- `set seed` called ONCE at top if stochastic operations are present
- All paths relative to repository root
- No hardcoded absolute paths and no `cd`
- Prefer local macros and program arguments over global macros
- Rely on the Makefile to make directories

### 2. Program Design

- Wrap reusable logic in `program define`
- Use `syntax` to validate arguments and options for non-trivial programs
- Use `tempfile`, `tempname`, and `tempvar` for temporary state
- Keep locals descriptive and scoped tightly
- Avoid magic numbers; lift them into named locals or documented parameters

### 3. Data Integrity & Domain Correctness

- Verify estimators and transformations match paper formulas (`latex/manuscript.tex`)
- Check merge keys with `isid`, `duplicates report`, or `assert`
- After `merge`, inspect `_merge` and assert the expected match pattern
- After `reshape`, assert the expected observation count and key uniqueness
- Set `xtset` / `tsset` explicitly for panel or time-series work
- Match cluster, FE, and weight choices to the intended estimand

### 4. Output Paths

All code outputs go to canonical subdirectories under `output/`:

```stata
save "output/tables/my_results.dta", replace
export delimited using "output/tables/my_results.csv", replace

file open fh using "output/numbers/my_estimate.txt", write text replace
file write fh "\newcommand{\myEstimate}{2.31}" _n
file close fh
```

**Heavy computations should be saved to disk; downstream scripts should load pre-computed data where possible.**

### 5. Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Missing `version` | Results may change across Stata releases | Pin `version` at top |
| Hardcoded paths or `cd` | Breaks on other machines | Use repo-relative paths only |
| Unchecked `_merge` after `merge` | Silent sample corruption | Assert expected `_merge` values |
| Globals for routine state | Hidden dependencies across scripts | Prefer locals and `syntax` |
| `capture` without `_rc` check | Real failures get silenced | Check `_rc` immediately |
| Unbalanced `preserve` / `restore` | Wrong dataset state later in script | Keep blocks tight and paired |
| Hidden sort dependence | Wrong grouped calculations | Use `sort` / `bysort` explicitly |

### 6. Line Length & Continuations

**Standard:** Keep lines <= 100 characters where practical. Use `///` continuations consistently, and align long option lists when that improves readability.

### 7. Code Quality Checklist

```
[ ] version pinned at top
[ ] set more off in batch scripts
[ ] set seed once at top if stochastic
[ ] All paths relative and no cd
[ ] Programs documented and arguments validated with syntax
[ ] merge/reshape steps checked with assert/isid/duplicates logic
[ ] Outputs saved to output/
[ ] Comments explain WHY not WHAT
[ ] capture followed by _rc checks
[ ] preserve/restore blocks are balanced
```

---

## MATLAB Code Standards

**Standard:** Senior Principal Computational Scientist + PhD researcher quality

### 1. Reproducibility

- `rng()` called ONCE at top if stochastic operations are present (never inside loops/functions)
- All paths relative to repository root
- Path construction uses `filesep` or `fullfile()` for cross-platform compatibility
- No hardcoded absolute paths (e.g., `/Users/...`, `C:\Users\...`)
- Rely on the Makefile to make directories (when Makefiles exist)

### 2. Function Design

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
- Input validation via `assert()` for critical dimensions

### 3. Domain Correctness

- Verify objective function implementations match paper formulas (`latex/manuscript.tex`)
- Check known package/solver bugs (document below in Common Pitfalls)

### 4. Solver Configuration

Projects using optimization should follow a dual-solver pattern (e.g., KNITRO + fmincon) controlled by a configuration flag. Key requirements:
- Option file paths constructed with `filesep` or `fullfile()`
- Hessian callback matches the wrapper signature
- Both solver paths should produce consistent results
- Always check `exitflag` after solver call

### 5. Output Paths

All code outputs go to canonical subdirectories under `output/`:

```matlab
writetable(results, fullfile("output", "tables", "results.csv"));
writematrix(data, fullfile("output", "tables", "output.csv"));
save(fullfile("output", "tables", "results.mat"), "results", "params");
```

Projects with a `Params` struct may wrap these paths (e.g., `Params.outputdir` instead of `"output"`), but the canonical subdirectories (`tables/`, `figures/`, `numbers/`) remain the same.

### 6. Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Hardcoded absolute paths | Breaks on other machines | Use relative paths with `filesep` |
| Unchecked solver `exitflag` | **Silent convergence failure (Critical, -20)** | Always check `exitflag > 0` |
| Missing NaN/Inf guards | Solver crashes or wrong results | Check before and after optimization |
| Inconsistent index trimming | Wrong data alignment | Trim all parallel arrays identically |
| `i`/`j` as loop variables | Shadows complex unit | Use `ii`, `jj`, `kk` or descriptive names |
| Asymmetric Hessian | **Silently wrong results (Critical, -25)** | Symmetrize: `H = (H + H') / 2` |
| Missing semicolons | Unwanted console output | End assignment lines with `;` |

### 7. Line Length

**Standard:** Keep lines <= 120 characters. Mathematical formulas may exceed 120 chars if breaking the line would harm readability, an inline comment explains the operation, and the line is in a numerically intensive section.

### 8. Code Quality Checklist

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

---

## Makefile Conventions

### Structure

- Every Makefile has `all` and `clean` as `.PHONY` targets
- `all` is the default (first) target and builds everything in that directory
- `clean` removes all generated outputs
- Root Makefile delegates to sub-Makefiles with a `$(MAKE) -C` loop

### Directory Creation

Use order-only prerequisites for output subdirectories:

```make
output/tables/results.csv: code/analysis.R | output/tables
output/figures/plot.pdf: code/figures.R | output/figures
output/numbers/estimate.txt: code/analysis.R | output/numbers

output/tables output/figures output/numbers:
	mkdir -p $@
```

Scripts must NOT create directories themselves. The Makefile owns all directory creation.

### Cross-Makefile Dependencies

```make
../sibling_dir/output.csv:
	$(MAKE) -C ../sibling_dir output.csv
```

### Expensive Intermediates

Mark expensive-to-produce files as `.PRECIOUS` so Make does not delete them on interruption.

### Pattern Rules

```make
STATA ?= stata-mp

output/tables/%.rds: code/%.R | output/tables
	Rscript $<

output/tables/%.csv: code/%.jl | output/tables
	julia $<

output/tables/%.dta: code/%.do | output/tables
	$(STATA) -b do $<
```

### Joint Production

When a single script produces multiple outputs, declare one primary target with the recipe and secondary targets with an empty recipe (`;`).

### Recipe Conventions

- R scripts: `Rscript $<`
- Julia scripts: `julia $<`
- Stata scripts: `$(STATA) -b do $<` with `STATA ?= stata-mp` (or your local Stata binary)
- MATLAB scripts: `matlab -batch "run('$<')"`
- Always use `$<` (first prerequisite) and `$@` (target) automatic variables
- Never use absolute paths

### Root Makefile Pattern

The project root Makefile delegates to `code/` and `latex/`:

```make
SUBDIRS = code latex

.PHONY: all clean $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
```

The `code/Makefile` in turn delegates to sub-Makefiles in each task-group directory.

### Validation

- `make -n` (dry-run) must produce a valid plan
- Every `.R`, `.jl`, `.do`, `.ado`, and `.m` file under `code/` should appear as a prerequisite in some Makefile target -- orphaned scripts are a warning sign
