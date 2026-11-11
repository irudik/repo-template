# Review Julia Scripts

Review the supplied files; `all` means all Julia Scripts in `code/`.
Read `protocols/conventions/shared.md` and
`protocols/conventions/julia.md`. This review returns findings without source
edits so the requesting agent can assess and apply corrections.

- Match estimation, simulations, algorithms, and precision to the mathematical
  specification. Check join keys, sample construction, and aggregation totals
  where data transformations determine the estimand.
- Check dependencies, stochastic `Random.seed!()`, relative `joinpath()` paths,
  and saved objects needed downstream or for reproduction (`jldsave()` or
  `serialize()`, plus CSV results where appropriate).
- Examine `NaN`, `Inf`, `missing`, `nothing`, and numerical failures; exception
  handling should keep evidence of failure.
- Inspect frequently executed functions for type stability, concrete struct
  fields, captured globals, slice copies, and unnecessary allocations. Use
  `@code_warntype` or timing evidence if execution tools are available; otherwise
  describe performance concerns as code-reading findings, not measured results.
- Consider preallocation, `@views`, `const`, `eachindex()`, dispatch, and fused
  broadcasting where appropriate. Do not treat every loop as a defect.
- Apply Julia conventions for documented functions, named returns, descriptive
  names, shallow type hierarchies, and clear numerical operations.

Return findings to the agent that started the review, distinguishing claims
based on reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: give actionable findings with file and line references,
evidence, proposed corrections, and verification limits, separating blocking
defects under `Defects That Block a Commit or Merge` in root `AGENTS.md` from
advisory items.
