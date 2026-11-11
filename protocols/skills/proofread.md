# Proofread Academic Documents

Use only when the user asks for it. Review the supplied text files; `all` means
`.tex` files in `latex/` except `latex/latex_extras/`, plus project `.qmd` files.
Return findings without source edits.

- Check agreement, tense, articles, modifiers, sentence boundaries, spelling,
  doubled or missing words, and technical terminology.
- Check notation, capitalization, number formats, abbreviations, citation style,
  and citation keys against the bibliography.
- Inspect likely equation and table overflow, figure placement, orphaned
  headings, and widow/orphan lines; distinguish suspected layout problems from
  those visible in rendered output.
- Check claim strength, paragraph structure, transitions, and whether the
  abstract describes the actual document. Keep substantive identification or
  model review within a separately requested domain review.

Return findings to the agent that started the review, distinguishing claims
based on reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: give actionable findings with file and line references,
evidence, proposed corrections, and verification limits, separating blocking
defects under `Defects That Block a Commit or Merge` in root `AGENTS.md` from
advisory items.
