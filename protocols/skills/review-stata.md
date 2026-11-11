# Review Stata Scripts

Review the supplied files; `all` means all Stata Scripts in `code/`.
Read `protocols/conventions/shared.md` and
`protocols/conventions/stata.md`. This review returns findings without source
edits so the requesting agent can assess and apply corrections.

- Match estimators, fixed effects, clustering, weights, and sample restrictions
  to the intended estimand. Check `merge`, `joinby`, `append`, `collapse`, and
  `reshape` invariants: key uniqueness, unmatched observations, counts, totals,
  and explicit `xtset` or `tsset` when needed.
- Check `version`, batch `set more off`, stochastic `set seed`, relative paths,
  and local or temporary macros rather than unnecessary globals.
- Check `program define` input validation with `syntax`, macro quoting, and
  `sort` or `bysort` before order-dependent operations.
- Examine `_rc` after `capture`, balanced `preserve`/`restore`, assertions after
  critical transformations, and scoped `tempfile`, `tempname`, and `tempvar`.
- Check required outputs from `save`, `export delimited`, `putexcel`, `esttab`,
  or `file write`, including dynamic-number exports under `output/numbers/`.
- Apply Stata conventions for readable commands and `///` continuations,
  descriptive names, and comments explaining non-obvious economic choices;
  flag production `pause`, `set trace on`, and excessive loop output.

Return findings to the agent that started the review, distinguishing claims
based on reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: give actionable findings with file and line references,
evidence, proposed corrections, and verification limits, separating blocking
defects under `Defects That Block a Commit or Merge` in root `AGENTS.md` from
advisory items.
