# Review Makefiles

Review the supplied files; `all` means all Makefiles in the project.
Read `protocols/conventions/shared.md` and
`protocols/conventions/makefile.md`. This review returns findings without source
edits so the requesting agent can assess and apply corrections.

- Check that `all` is the first default target, non-file targets are `.PHONY`,
  `clean` is scoped, recipes use tabs, and expensive intermediates use
  `.PRECIOUS` where needed.
- Follow dependencies through input data and helper scripts; detect cycles,
  missing prerequisites, and prerequisites without producing rules.
- Check coverage of `.R`, `.jl`, `.do`, `.ado`, and `.m` scripts as prerequisites,
  including helpers; report unexplained exclusions and orphaned scripts.
- Check order-only directory prerequisites with `mkdir -p $@`, paths relative to
  each Makefile, and recursive delegation through `$(MAKE) -C`.
- For joint outputs, check that one script execution produces them consistently
  and that a missing secondary output will be rebuilt without duplicate runs.
- Check automatic variables and interpreter commands: `Rscript $<`, `julia $<`,
  `$(STATA) -b do $<`, and `matlab -batch "run('$<')"` as appropriate.
  Distinguish a dependency inferred from reading from behavior demonstrated by
  a scoped dry run or build.

Return findings to the agent that started the review, distinguishing claims
based on reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: give actionable findings with file and line references,
evidence, proposed corrections, and verification limits, separating blocking
defects under `Defects That Block a Commit or Merge` in root `AGENTS.md` from
advisory items.
