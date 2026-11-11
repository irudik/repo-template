# LaTeX Conventions

These conventions apply to all files in `latex/` and its subdirectories.

---

## Building and Checking

Compile with `make -C latex` from the repository root. The Makefile sets
`TEXINPUTS`, `BIBINPUTS`, and `BSTINPUTS`, so `\input` and
`\includegraphics` find files in `output/numbers/`, `output/tables/`, and
`output/figures/` without a path prefix. Do not run `pdflatex` by hand with
exported variables; shell state does not carry from one command to the next.

After a build, confirm there are no undefined citations, no missing inputs,
and no badly overfull lines. Run `/review-tex` when results or the prose
around them changed, not after every edit.

`latex/Makefile` lists every dependency in `MAIN_SOURCES` and
`SLIDES_SOURCES` so Make can tell when a PDF is out of date. Add new source
files and generated inputs there. Make does not use `TEXINPUTS`, so a
generated input needs its path in the Makefile
(`../output/numbers/revenue_estimate.txt`) even though the `.tex` source
omits it. Add citations to `references/references.bib` directly.

---

## Dynamic Numbers

The pipeline keeps computed results out of `.tex` source by writing `\newcommand` definitions to `output/numbers/` and resolving them at compile time via `TEXINPUTS`.

### How It Works

1. **Code generates a `.txt` file** with a `\newcommand` (R, Julia, Stata, or MATLAB)
2. **The manuscript inputs the file**: `\input{revenue_estimate.txt}`
3. **`TEXINPUTS` resolves the path** -- pdflatex finds the file in `../output/numbers/`

### Adding a New Dynamic Number

1. Add the write call to your R, Julia, Stata, or MATLAB script
2. In the relevant `code/` Makefile, declare the `.txt` file as a target built by that script, and add `../output/numbers/filename.txt` to `MAIN_SOURCES` or `SLIDES_SOURCES` in `latex/Makefile`
3. Add `\input{filename.txt}` in the manuscript preamble
4. Use the macro in prose
5. Run `make` -- the code pipeline writes the file, then pdflatex picks it up

### Reviewing Updated Values

Before a task rebuilds `output/numbers/`, record the current macro definitions.
Compare their contents after the rebuild. Whenever a generated numeric macro
changes value, review every prose occurrence in all affected TeX documents,
including captions, notes, and slides. Inspect the containing sentence and
enough nearby context to check articles, singular and plural agreement,
direction, units, comparisons, thresholds, and descriptions of magnitude.
Fix unambiguous wording, flag substantive ambiguity, and recompile affected
documents. Identical regenerated definitions do not require this review.

Keep generated macros value-only. Do not replace contextual prose review with
a general article-selection function.

The same `TEXINPUTS` mechanism resolves figures (`output/figures/`) and tables (`output/tables/`).

---

## TeX Prose Conventions

- Reference labels as "equation \eqref{...}" or "equations \eqref{...}--\eqref{...}" when grammatically appropriate
- Avoid bare "\eqref{...}" in running text
- Follow the plain-language rules in `protocols/writing.md`: no programmer
  jargon, no AI-inflated vocabulary, and no references to code, file paths,
  or pipeline stages in manuscript or slide prose -- describe the economics
  and the mathematics
- Write in first person active voice ("we estimate", "we find") with no
  contractions; state the claim first and qualify second
- Report magnitudes with units and, where possible, a benchmark a reader can
  anchor on (dollar values with a base year, effect sizes against familiar
  interventions)
