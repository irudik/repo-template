# Review MATLAB Scripts

Review the supplied files; `all` means all MATLAB Scripts in `code/`.
Read `protocols/conventions/shared.md` and
`protocols/conventions/matlab.md`. This review returns findings without source
edits so the requesting agent can assess and apply corrections.

- Match objectives, constraints, boundary conditions, and algorithms to the
  mathematical specification. Check stochastic `rng()`, relative `fullfile()`
  paths, and saved results required downstream or for reproduction.
- Check solver option paths, consistency across alternative solver paths,
  callback registration, parameter ordering, bounds, scaling, and dimensions.
- Check objective/gradient/Hessian return consistency, Hessian wrappers and
  symmetry, derivative signs and dimensions, and finite-difference evidence.
  Use `protocols/skills/matlab-optim-derivatives.md` for a numerical audit.
- Examine `exitflag`, first-order optimality where relevant, and finite inputs
  and outputs. Unchecked convergence or failed derivatives are blocking defects.
- Check parameter-index arithmetic, equal trimming of parallel arrays,
  symmetric matrix row/column removal, and bounds matching parameter length.
- Apply MATLAB conventions for function documentation, dimension assertions,
  parameter structures, descriptive names, semicolons, and non-obvious economic
  comments; avoid `i` and `j` as loop names and unnecessary iteration output.

Return findings to the agent that started the review, distinguishing claims
based on reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: give actionable findings with file and line references,
evidence, proposed corrections, and verification limits, separating blocking
defects under `Defects That Block a Commit or Merge` in root `AGENTS.md` from
advisory items.
