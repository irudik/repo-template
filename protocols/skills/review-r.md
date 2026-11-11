# Review R Scripts

Review the supplied files; `all` means all R Scripts in `code/`.
Read `protocols/conventions/shared.md` and
`protocols/conventions/r.md`. This review returns findings without source
edits so the requesting agent can assess and apply corrections.

- Match estimators, treatment effects, simulations, standard errors, weights,
  and sample restrictions to the paper's specification. Check join keys,
  unmatched rows, aggregation totals, and missing-data treatment.
- Check package setup, stochastic seed placement, relative `file.path()` paths,
  and whether the script can run through `Rscript` with declared inputs.
- Examine `NA`, `NaN`, `Inf`, division by zero, failed simulation replications,
  and parallel-worker cleanup; failures should remain visible.
- Check that objects needed downstream or for reproduction are saved with
  descriptive names, using `saveRDS()` and stable tables where appropriate.
- Inspect figures for units, readable labels and legends, consistent project
  styling, explicit `ggsave()` dimensions, and transparency when needed.
- Apply R conventions for documented functions, named returns, `snake_case`,
  native `|>`, `=` assignment, explicit logical values, and readable operations.
  Comments should explain non-obvious economic choices, not repeat mechanics.

Return findings to the agent that started the review, distinguishing claims
based on reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: give actionable findings with file and line references,
evidence, proposed corrections, and verification limits, separating blocking
defects under `Defects That Block a Commit or Merge` in root `AGENTS.md` from
advisory items.
