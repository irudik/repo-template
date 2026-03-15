# LaTeX Conventions

These conventions apply to all files in `latex/` and its subdirectories.

---

## Verification

After any LaTeX change:

1. Compile with `make -C latex` (preferred -- handles TEXINPUTS/BIBINPUTS/BSTINPUTS automatically)
2. For manual runs, first export environment variables from the `latex/` directory:
   ```bash
   export TEXINPUTS=.:./latex_extras/:../output/numbers/:../output/tables/:../output/figures/:
   export BIBINPUTS=./references/:
   export BSTINPUTS=./references/:
   ```
3. Verify PDF was generated with non-zero size
4. Check for overfull hbox warnings
5. Check for undefined citations
6. Run the `/review-tex` skill to check for hardcoded numbers in prose
7. Verify all dynamic number `\input{...}` files exist in `output/numbers/` and are listed in `latex/Makefile` SOURCES

---

## Makefile Pattern

```make
TEX      = pdflatex
BIBTEX   = bibtex
TEXFLAGS = -interaction=nonstopmode

# Resolve \input and \includegraphics from output/ subdirs without ../output/ prefixes
export TEXINPUTS := .:./latex_extras/:../output/numbers/:../output/tables/:../output/figures/:
export BIBINPUTS := ./references/:
export BSTINPUTS := ./references/:

MAIN     = manuscript
SLIDES   = slides

MAIN_SOURCES = $(MAIN).tex \
               latex_extras/packages.tex \
               latex_extras/custom_commands.tex \
               latex_extras/dynamic_tables.tex \
               references/references.bib

SLIDES_SOURCES = $(SLIDES).tex \
                 latex_extras/slides_setup.tex \
                 latex_extras/dynamic_tables.tex \
                 references/references.bib

.PHONY: all clean

all: $(MAIN).pdf $(SLIDES).pdf

$(MAIN).pdf: $(MAIN_SOURCES)
	$(TEX) $(TEXFLAGS) $(MAIN)
	@if grep -q '\\citation' $(MAIN).aux 2>/dev/null; then $(BIBTEX) $(MAIN); fi
	$(TEX) $(TEXFLAGS) $(MAIN)
	$(TEX) $(TEXFLAGS) $(MAIN)

$(SLIDES).pdf: $(SLIDES_SOURCES)
	$(TEX) $(TEXFLAGS) $(SLIDES)
	@if grep -q '\\citation' $(SLIDES).aux 2>/dev/null; then $(BIBTEX) $(SLIDES); fi
	$(TEX) $(TEXFLAGS) $(SLIDES)
	$(TEX) $(TEXFLAGS) $(SLIDES)

clean:
	rm -f $(MAIN).pdf $(SLIDES).pdf *.aux *.bbl *.blg *.log *.out *.toc \
	      *.fdb_latexmk *.fls *.nav *.snm *.vrb *.synctex.gz *.run.xml *-blx.bib
```

List all `.tex` and `.bib` dependencies in SOURCES variables so Make can detect staleness. The conditional bibtex pattern avoids errors when there are no citations yet.

---

## Dynamic Numbers

The pipeline keeps computed results out of `.tex` source by writing `\newcommand` definitions to `output/numbers/` and resolving them at compile time via `TEXINPUTS`.

### How It Works

1. **Code generates a `.txt` file** with a `\newcommand` (R, Julia, Stata, or MATLAB)
2. **The manuscript inputs the file**: `\input{revenue_estimate.txt}`
3. **`TEXINPUTS` resolves the path** -- pdflatex finds the file in `../output/numbers/`

### Adding a New Dynamic Number

1. Add the write call to your R, Julia, Stata, or MATLAB script
2. Add the `.txt` file as a prerequisite in the relevant `code/` Makefile
3. Add `\input{filename.txt}` in the manuscript preamble
4. Use the macro in prose
5. Run `make` -- the code pipeline writes the file, then pdflatex picks it up

The same `TEXINPUTS` mechanism resolves figures (`output/figures/`) and tables (`output/tables/`).

---

## TeX Prose Conventions

- Reference labels as "equation \eqref{...}" or "equations \eqref{...}--\eqref{...}" when grammatically appropriate
- Avoid bare "\eqref{...}" in running text
