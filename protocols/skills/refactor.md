# Code Style Cleanup

The only acceptable outcome of a style cleanup is identical output. Read
`protocols/conventions/shared.md` and the applicable language conventions.

1. Record pre-existing changes so they can be preserved. Establish baseline
   outputs with `protocols/skills/verify-outputs.md` before editing.
2. Limit changes to comments, whitespace, indentation, missing documentation,
   and grouping or section organization that leaves execution unchanged.
   Apply language style conventions only where they preserve behavior.
3. Keep solver tolerances, options, and convergence criteria unchanged because
   identical output is required. Also preserve numerical-loop variable names,
   function signatures, parameters and returns, logic and control flow, data
   types and precision, error handling, and loop/vectorization choices: these
   can alter behavior or obscure numerical comparisons. Changes to these belong
   to an explicitly requested substantive task, not a style cleanup.
4. Flag unused code without removing it unless removal was explicitly requested.
   When a change's effect is uncertain, leave it unchanged and say so in the
   report.
5. Re-run and compare outputs with the baseline. On an output mismatch, find
   the edit that caused it, undo that edit, and compare again, so the rest of
   the cleanup is kept. If the cause cannot be isolated, undo all of this
   task's edits. Either way, preserve changes that were there before and
   report the mismatch; do not expand a style cleanup into a numerical repair.
6. Use a targeted independent review only when numerical code or substantial
   reorganization makes another reading useful. Give the final report after
   that review and any necessary corrections.

Follow `Reports and Updates` in `protocols/writing.md`: describe the cleanup,
outputs compared, review findings, and omissions; matching selected outputs
supports agreement for those outputs only.
