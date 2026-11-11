# Generate a Makefile

Read `protocols/conventions/makefile.md`. Scan the requested directory for
`.R`, `.jl`, `.do`, `.ado`, and `.m` scripts, their input paths, and write calls:

- R: `write.csv`, `write_csv`, `saveRDS`, `ggsave`, `writeLines`.
- Julia: `CSV.write`, `jldsave`, `savefig`, `open(..., "w")`.
- Stata: `save`, `export delimited`, `putexcel`, `esttab`, `file write`.
- MATLAB: `writetable`, `writematrix`, `save`, `saveas`.

Resolve constructed output paths: in `code/<task_group>/`, typical roots are
`file.path("..", "..", "output")` in R,
`joinpath("..", "..", "output")` in Julia, `../../output` in Stata, and
`fullfile("..", "..", "output")` in MATLAB. Use local script prerequisites
and `OUTPUT_ROOT ?= ../../output` for generated targets.

Generate `all` as the default target, `.PHONY` for non-file targets, order-only
directory prerequisites, one production rule for a script's joint outputs,
`.PRECIOUS` for costly intermediates, and a scoped `clean` target. List input
data and helper scripts as prerequisites. Use automatic variables and the
Stata recipe `$(STATA) -b do $<`; delegate subdirectories through `$(MAKE) -C`.
For LaTeX builds use `make -C latex` rather than shell directory or environment
changes.

When generation or changes are requested, write the Makefile and update parent
delegation as needed, then check target selection with a scoped dry run and
build the affected target. For review-only requests, report without editing.
Leave uncertain dependencies unchanged rather than inventing output paths.

Follow `Reports and Updates` in `protocols/writing.md`: describe the resulting
build rules, checks, and scripts whose inputs or outputs could not be resolved.
