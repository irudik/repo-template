# Review Makefiles Protocol

Run the comprehensive Makefile review protocol.

## Steps

1. **Identify Makefiles to review:**
   - If an argument is a specific Makefile path, review that file only.
   - If the argument is `all`, review all Makefiles in the project.

2. **For each Makefile, follow the review protocol below:**
   - Read `.claude/rules/makefile-conventions.md` or the Makefile section of
     `code/AGENTS.md`.
   - Scan scripts in the same directory for coverage checking.
   - Save the report to `quality_reports/[dir_name]_makefile_review.md`.

3. **After all reviews complete, present a summary:**
   - Total issues found per Makefile
   - Breakdown by severity
   - Orphaned scripts

4. **Do not edit Makefiles.** Produce reports only.

## Review Protocol

You are a Senior Build Engineer with deep expertise in GNU Make for academic
research pipelines.

### Review Categories

#### 1. Structure

- `all` is the default first target
- `clean` target exists
- `.PHONY` declared for non-file targets
- Logical ordering of variables, targets, rules, and clean

#### 2. Directory Creation

- Output directories use order-only prerequisites
- Directories created with `mkdir -p $@`
- Scripts do not create directories

#### 3. Dependency Correctness

- No circular dependencies
- All prerequisites exist or have rules
- Cross-directory dependencies use `$(MAKE) -C`
- Input data files listed as prerequisites

#### 4. Script Coverage

- Every `.R`, `.jl`, and `.m` file has a corresponding target
- No orphaned scripts
- Excluded helper scripts are documented

#### 5. Joint Production

- Multi-output scripts use one real recipe and secondary targets
- No duplicate recipes for the same script

#### 6. Recipe Conventions

- `Rscript $<`, `julia $<`, `matlab -batch "run('$<')"` as appropriate
- Automatic variables such as `$<` and `$@`
- No absolute paths

#### 7. Expensive Intermediates

- `.PRECIOUS` used on files that are expensive to rebuild

#### 8. Delegation

- `$(MAKE) -C` used for subdirectories
- Subdirectories stored in a variable

#### 9. Professional Polish

- Tabs, not spaces, in recipes
- Comments on non-obvious targets
- Variables declared near the top

## Report Format

Save the report to `quality_reports/[dir_name]_makefile_review.md`.

Include:

- Issue counts by severity
- File and line references
- Concrete proposed fixes
- A checklist summary by review category

## Important Rules

- Never edit Makefiles.
- Include line numbers.
- Every issue needs a concrete proposed fix.
- Prioritize correctness over style.
