# Review Research Substance

Use only when the user asks for it. Review supplied manuscripts, slides, or
lecture materials; `all` means `.tex` files in `latex/` except
`latex/latex_extras/`, plus project `.qmd` files. Return findings without edits.
Read relevant code, bibliography entries, and original sources in `literature/`
when present; distinguish source verification from unverified citation claims.

- Identification: do causal claims follow from the design, stated assumptions,
  and evidence? Are important threats addressed?
- Mathematics: do derivations follow from assumptions, including boundaries
  and edge cases? Are approximations acknowledged and their limits justified?
- Citations: do attributed claims match original sources, with appropriate
  methodological references and no misattribution?
- Code and theory: do transformations, estimation commands, parameter choices,
  and numerical implementation match the paper's specification?
- Internal logic: do conclusions follow from reported results, and do claims
  remain consistent across the introduction, analysis, and conclusion?

Return findings to the agent that started the review, distinguishing claims
based on reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: give actionable findings with file and line references,
evidence, proposed corrections, and verification limits, separating blocking
defects under `Defects That Block a Commit or Merge` in root `AGENTS.md` from
advisory items.
