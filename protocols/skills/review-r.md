# Review R Scripts Protocol

Run the comprehensive R code review protocol.

## Steps

1. **Identify scripts to review:**
   - If an argument is a specific `.R` filename, review that file only.
   - If the argument is `all`, review all R scripts in `code/`.

2. **For each script, follow the review protocol below:**
   - Read `code/AGENTS.md` or `.claude/rules/r-code-conventions.md`.
   - Save the report to `quality_reports/[script_name]_r_review.md`.

3. **After all reviews complete, present a summary:**
   - Total issues found per script
   - Breakdown by severity
   - Top three most critical issues

4. **Do not edit R source files.** Produce reports only.

## Review Protocol

You are a Senior Principal Quantitative Research Engineer with deep expertise in quantitative
methods and reproducible research workflows.

### Review Categories

#### 1. Script Structure and Header

- Header block with title, author, purpose, inputs, outputs
- Numbered top-level sections
- Logical flow from setup through export

#### 2. Console Output Hygiene

- `message()` used sparingly
- No routine `cat()`, `print()`, or `sprintf()` status output
- No per-iteration printing inside simulation loops

#### 3. Reproducibility

- `set.seed()` called once at the top
- Packages loaded at the top via `library()`
- Paths relative to the repository root
- Scripts do not call `dir.create()`
- No hardcoded absolute paths
- Script can run cleanly via `Rscript`

#### 4. Function Design and Documentation

- `snake_case` naming
- Verb-noun naming pattern
- Roxygen-style documentation for non-trivial functions
- Default parameters and no magic numbers
- Named list or tibble returns instead of unnamed vectors

#### 5. Domain Correctness

- Estimators match the formulas in `latex/manuscript.tex`
- Standard errors use the correct method
- Simulations match the paper specification
- Treatment effects target the correct estimand

#### 6. Figure Quality

- Consistent palette
- Custom theme applied
- Transparent background where needed
- Explicit dimensions in `ggsave()`
- Clear labels and readable legends
- No default ggplot colors leaking through

#### 7. RDS Data Pattern

- Computed objects persisted with `saveRDS()`
- Descriptive filenames
- Raw results and summary tables both saved
- Paths use `file.path()`

#### 8. Comment Quality

- Comments explain why, not what
- Section headers describe purpose
- No commented-out dead code
- No redundant comments

#### 9. Error Handling and Edge Cases

- Results checked for `NA`, `NaN`, and `Inf`
- Failed replications counted and reported
- Division by zero guarded where relevant
- Parallel backends registered and unregistered cleanly

#### 10. Professional Polish

- Consistent indentation
- Reasonable line lengths
- Consistent operator spacing
- Native `|>` pipe style
- `=` assignment style when that is the project rule
- No legacy `T` and `F`

## Report Format

Save the report to `quality_reports/[script_name]_r_review.md`.

Include:

- Issue counts by severity
- File and line references
- Concrete proposed fixes
- A checklist summary by review category

## Important Rules

- Never edit source files.
- Include line numbers and code snippets.
- Every issue needs a concrete proposed fix.
- Prioritize domain correctness over style.
