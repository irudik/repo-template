# Shared Code Pipeline Conventions

These conventions apply to all scripts in `code/` and its subdirectories.

## Path Style

- Invoke builds from the repository root with `make -C code/[task_group]`.
  Because `make -C` changes Make's working directory, paths in task-group Makefiles
  and the scripts they run are relative to the task-group directory.
- In the standard `code/[task_group]/` layout, use `../../output` to reach the
  repository-root output directory. Do not add a `PROJECT_ROOT` variable merely
  to implement this standard two-level layout.
- Use forward slashes in any literal filepath on every platform, including
  Windows (for example `../../output/tables/results.csv`)
- Never write Windows-style backslashes in path literals
- Path helpers such as `file.path()`, `joinpath()`, and `fullfile()` remain
  preferred for programmatic path construction

## Running and Checking

- Run a script through its Make target. When no Makefile governs it, use
  `code/[task_group]/` as the command's working directory and run the script
  there: `Rscript script.R`, `julia script.jl`, `stata -b do script.do`, or
  `matlab -batch "run('script.m')"`. If your shell tool cannot set a working
  directory, add a Make target for the script and run it with `make -C`.
- After a run, confirm the expected output files exist and hold plausible
  content. Read the Stata batch log or the solver output for errors and
  failed convergence.
- In stochastic code, set the seed once at the top, and confirm that two runs
  with the same seed give the same output.
- When scripts are added, renamed, or moved, check that every `.R`, `.jl`,
  `.do`, `.ado`, and `.m` file is a prerequisite of some Make target. A script
  outside the build is either unused or missing from it.

## Shared Research Code Style

These standards apply across R, Julia, Stata, MATLAB, and Makefiles unless a
language-specific convention gives a narrower rule.

- Prefer clarity over cleverness. Slightly longer code is better than a dense
  expression that hides data construction, identification logic, or output
  provenance.
- Reproducibility is the deliverable. Code must run from the Makefile-driven
  pipeline on a clean checkout without hidden state, manual steps, absolute
  paths, or hand-edited outputs.
- Use one operation per line. Do not combine loading, filtering, mutating,
  summarizing, estimating, and exporting into compact one-liners.
- For long calls or commands, put one substantive argument or option per line
  when it improves scanability and version-control diffs.
- Use names that read like prose. Prefer descriptive `snake_case` names for
  files, data objects, variables, locals, and functions unless the applicable
  language convention explicitly differs, such as Julia `CamelCase` types.
- Every analysis file should start with a clean header block that states the
  title or purpose, inputs, outputs, and any key assumptions or runtime notes.
  Do not include user-specific absolute paths in headers.
- Use section headers to mark workflow stages such as setup, data construction,
  estimation, diagnostics, and export.
- Comments should explain economic intuition, data logic, identifying
  assumptions, and non-obvious transformations rather than restating syntax.
- Comments, docstrings, and new identifiers follow the plain-language rule in
  `protocols/writing.md`: a term fails if an economics PhD would not
  understand it immediately from ordinary research practice. That file holds
  the banned-term table and its replacements. Name the object or task
  directly; if a precise software term must appear, explain it in plain
  language in the same comment or docstring.
- Comments and docstrings must be self-contained. Never reference issue or
  ticket numbers, commit hashes, pull requests, or conversations with Claude or
  Codex. The reader is a coauthor, referee, or future self without access to the
  repository history or an AI transcript.
