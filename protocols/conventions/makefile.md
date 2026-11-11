# Makefile Conventions

Read alongside `protocols/conventions/shared.md`.

## Structure and Delegation

- Declare `all` and `clean` as `.PHONY` targets, with `all` first as the default target.
- The root Makefile delegates to `code` and `latex` via `$(MAKE) -C`, and `code/Makefile` delegates to each `code/[task_group]/` Makefile.

## Directory Creation and Output Paths

Use order-only prerequisites for output subdirectories. In task-group Makefiles under `code/[task_group]/`, keep script prerequisites local and route generated files to the repository-root `output/` directory:

```make
OUTPUT_ROOT = ../../output

$(OUTPUT_ROOT)/tables/results.csv: analysis.R | $(OUTPUT_ROOT)/tables
	Rscript $<
$(OUTPUT_ROOT)/figures/plot.pdf: figures.R | $(OUTPUT_ROOT)/figures
	Rscript $<
$(OUTPUT_ROOT)/numbers/estimate.txt: analysis.R | $(OUTPUT_ROOT)/numbers
	Rscript $<

$(OUTPUT_ROOT)/tables $(OUTPUT_ROOT)/figures $(OUTPUT_ROOT)/numbers:
	mkdir -p $@
```

Never create output directories inside analysis scripts governed by a Makefile, because the Makefile should declare every output location; the exception is a standalone exploratory script that has no Make target yet.

## Dependencies and Joint Outputs

Cross-directory prerequisites delegate to the sibling Makefile:

```make
$(OUTPUT_ROOT)/tables/sibling_output.csv:
	$(MAKE) -C ../sibling_dir $(OUTPUT_ROOT)/tables/sibling_output.csv
```

Mark expensive intermediate files `.PRECIOUS` so Make does not delete them if
a run is interrupted.

When one script writes several outputs, attach the recipe to one primary
target and give each secondary target an empty recipe (`;`) that depends on
the primary one, so a parallel Make runs the script once:

```make
$(OUTPUT_ROOT)/tables/results.csv: analysis.R | $(OUTPUT_ROOT)/tables $(OUTPUT_ROOT)/figures
	Rscript $<
$(OUTPUT_ROOT)/figures/diagnostics.pdf: $(OUTPUT_ROOT)/tables/results.csv ;
```

## Recipes and Validation

- Batch recipes: `Rscript $<`, `julia $<`, `$(STATA) -b do $<` (with `STATA ?= stata-mp`), and `matlab -batch "run('$<')"`.
- Never hardcode machine-specific absolute paths in project Makefiles, because they fail on coauthors' machines and in replication packages; when raw data live outside the repository, pass the location through an overridable variable (such as `DATA_DIR ?= ...`).
- When a Makefile or dependency declaration changes, run a scoped `make -n` and confirm that it selects the intended targets before running the build. Source-only edits under an unchanged Makefile do not need a separate dry run.
