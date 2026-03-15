---
paths:
  - "**/Makefile"
  - "**/*.make"
---

# Makefile Conventions

## Structure

- Every Makefile has `all` and `clean` as `.PHONY` targets
- `all` is the default (first) target and builds everything in that directory
- `clean` removes all generated outputs
- Root Makefile delegates to sub-Makefiles with a `$(MAKE) -C` loop

## Directory Creation

Use order-only prerequisites for output subdirectories:

```make
output/tables/results.csv: code/analysis.R | output/tables
output/figures/plot.pdf: code/figures.R | output/figures
output/numbers/estimate.txt: code/analysis.R | output/numbers

output/tables output/figures output/numbers:
	mkdir -p $@
```

Scripts must NOT create directories themselves. The Makefile owns all directory creation via `mkdir -p $@`.

## Cross-Makefile Dependencies

When a target in one sub-Makefile depends on output from another:

```make
../sibling_dir/output.csv:
	$(MAKE) -C ../sibling_dir output.csv
```

## Expensive Intermediates

Mark expensive-to-produce files as `.PRECIOUS` so Make does not delete them on interruption:

```make
.PRECIOUS: output/tables/model_fit.rds
```

## Pattern Rules

Use pattern rules for parametric outputs:

```make
# R pattern rule
output/tables/%.rds: code/%.R | output/tables
	Rscript $<

# Julia pattern rule
output/tables/%.csv: code/%.jl | output/tables
	julia $<

# Stata pattern rule
STATA ?= stata-mp
output/tables/%.dta: code/%.do | output/tables
	$(STATA) -b do $<
```

## Joint Production

When a single script produces multiple outputs, declare one primary target with the recipe and secondary targets with an empty recipe (`;`):

```make
output/tables/results.csv output/figures/diagnostics.pdf: code/analysis.R | output/tables output/figures
	Rscript $<
output/figures/diagnostics.pdf: output/tables/results.csv ;
```

## Recipe Conventions

- R scripts: `Rscript $<`
- Julia scripts: `julia $<` (or `julia +release -t auto $<` for threaded workloads)
- Stata scripts: `$(STATA) -b do $<` with `STATA ?= stata-mp` (or your local Stata binary)
- Always use `$<` (first prerequisite) and `$@` (target) automatic variables
- Never use absolute paths — all paths are relative to the Makefile's directory

## Root Makefile Pattern

The project root Makefile delegates to `code/` and `latex/`:

```make
SUBDIRS = code latex

.PHONY: all clean $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

clean:
	for dir in $(SUBDIRS); do $(MAKE) -C $$dir clean; done
```

The `code/Makefile` in turn delegates to its own sub-Makefiles for each task group.

## LaTeX Makefile Pattern

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

List all `.tex` and `.bib` dependencies in `MAIN_SOURCES` and `SLIDES_SOURCES` so Make can detect staleness. The conditional bibtex pattern (`@if grep -q '\\citation'`) avoids bibtex errors when there are no citations yet.

## Validation

- `make -n` (dry-run) must produce a valid, readable plan with no errors
- Every `.R`, `.jl`, `.do`, `.ado`, and `.m` file under `code/` should appear as a prerequisite in some Makefile target — orphaned scripts are a warning sign
