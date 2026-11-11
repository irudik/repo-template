# Compare Script Outputs

For a script or directory, discover outputs from Make targets and write calls:
R (`write.csv`, `write_csv`, `saveRDS`, `ggsave`, `writeLines`), Julia
(`CSV.write`, `jldsave`, `savefig`, `open`), Stata (`save`, `export delimited`,
`putexcel`, `esttab`, `file write`), and MATLAB (`writetable`, `writematrix`,
`save`, `saveas`). Resolve paths from the script's working directory.

In baseline mode, run the relevant Make target, or the script from its directory
if no Makefile governs it, and store stable-output MD5 checksums in a gitignored
`.checksums.json` beside the outputs. In comparison mode, run the same targets
with the same inputs and compare against that baseline, including missing and
new outputs. A comparison without a reliable baseline is not a pass.

## Formats

| Format | Comparison |
|---|---|
| CSV/TSV | MD5; CSV is the preferred stable format for style cleanup |
| Generated `.tex` | MD5 or text diff |
| RDS | Load with `all.equal()` or export values to CSV; bytes depend on R version |
| `.dta` | Read with `haven::read_dta()` or export to CSV |
| `.mat` | Load and compare named variables with explicit tolerances |
| JLD2 | MD5 in a compatible Julia environment, otherwise load and compare |
| PDF/PNG | Visual comparison; renderer differences make checksums unsuitable |

Skip binary files in checksum mode except JLD2 in a compatible environment;
perform needed value or visual comparisons separately and identify their
coverage. If nothing is
checksum-comparable, say that comparison was skipped and why.

## Research Tolerances

Use the project's documented tolerances and their rationale. Illustrative
values are `1e-6` for point estimates (numerical precision), `1e-4` for standard
errors (simulation variability), and `0.01` for coverage rates (Monte Carlo
uncertainty depending on replication count); these are not project defaults.
State absolute versus relative tolerance and justify it from the computation.
Style cleanup still requires identical output; tolerances do not relax that rule.

Follow `Reports and Updates` in `protocols/writing.md`: name the baseline,
comparison coverage, mismatches with brief content differences, tolerances, and
skipped outputs. Report discrepancies without changing analysis unless a fix
was requested.
