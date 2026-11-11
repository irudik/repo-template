# Julia Conventions

Read alongside `protocols/conventions/shared.md`.

## Setup and Estimation

- In stochastic scripts, call `Random.seed!(YYYYMMDD)` once at the top. Never change a script's chosen seed casually across edits, because changing the seed mixes Monte Carlo variation with code or model changes; change it only when testing seed sensitivity or assigning distinct seeds across parallel runs.
- Match estimator and simulation formulas to `latex/manuscript.tex`. When comparing numerical outputs against R or Stata, account for floating-point tolerances and solver defaults.
- Return a `NamedTuple` or `struct` when a function returns multiple model quantities.
- Let the Makefile create output directories.

## Output Paths and Data Persistence

Task-group scripts run from the script working directory (usually `code/[task_group]/`). Define `output_root` once and write into the repository-root `output/` subdirectories:

```julia
output_root = joinpath("..", "..", "output")

savefig(joinpath(output_root, "figures", "my_plot.pdf"))
CSV.write(joinpath(output_root, "tables", "my_results.csv"), df)

open(joinpath(output_root, "numbers", "my_estimate.txt"), "w") do io
    println(io, "\\newcommand{\\myEstimate}{2.31}")
end
```

Save objects that later steps or reproduction need (using `JLD2` for Julia objects and `CSV` for tables shared across tools), rather than every computed object. When filenames encode parameter values, use plain ASCII names without accents or hats.

## Numerical Performance

- Give `struct` fields concrete or parametric types in structures used inside repeated numerical evaluations; never leave those fields untyped or `Any`, because Julia cannot specialize arithmetic on unknown types (configuration structs read once outside inner loops may stay flexible).
- Pass parameters into inner loops as arguments or `const` bindings rather than non-constant globals.
- Use `@views` for array slices, pre-allocate output arrays when dimensions are known, and fuse elementwise expressions with `@.` in repeated evaluations.
- Index arrays with `eachindex(x)` or `axes(x, dim)` when array indexing may not start at 1.
