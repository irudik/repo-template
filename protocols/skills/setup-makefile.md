# Generate Makefile from Directory Contents Protocol

Scan a directory for scripts and generate a Makefile following project
conventions.

## Steps

### 1. Scan the Directory

Glob for `.R`, `.jl`, `.do`, `.ado`, and `.m` files.

### 2. Parse Output Paths

For each script, scan for write calls:

- R: `write.csv`, `write_csv`, `saveRDS`, `ggsave`, `writeLines`
- Julia: `CSV.write`, `jldsave`, `savefig`, `open(..., "w")`
- Stata: `save`, `export delimited`, `putexcel`, `esttab`, `file write`
- MATLAB: `writetable`, `writematrix`, `save`, `saveas`

Concrete patterns to match include:

- R: `write.csv(df, file.path("output", "tables", "results.csv"))`
- Julia: `CSV.write(joinpath("output", "tables", "results.csv"), df)`
- Stata: `save "output/tables/results.dta", replace`
- Stata: `export delimited using "output/tables/results.csv", replace`
- Stata: `file open fh using "output/numbers/estimate.txt", write text replace`
- MATLAB: `writetable(tbl, fullfile("output", "tables", "results.csv"))`

Also scan for input paths to determine dependencies.

### 3. Generate the Makefile

Follow the relevant Makefile conventions:

- `all` as the default target with `.PHONY`
- Order-only prerequisites for directories
- Automatic variables such as `$<` and `$@`
- Joint production for multi-output scripts
- `.PRECIOUS` for expensive intermediates
- A `clean` target

### 4. Present for Review

Do not write directly. Present the generated content and ask for approval.

### 5. Write After Approval

Write the Makefile and update the parent `code/Makefile` delegation if needed.

## Important

- Always present for review before writing.
- Follow Makefile conventions exactly.
- Use the existing Stata recipe convention `$(STATA) -b do $<` when a generated
  Makefile includes Stata targets.
- Flag scripts whose outputs cannot be parsed reliably.
