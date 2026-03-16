# Refactor Code Protocol

Safe refactoring with automatic output verification.

## Steps

### 1. Establish a Baseline

Run `/verify-outputs [target] baseline` to record output checksums before any
changes.

### 2. Read the Applicable Conventions

Read the relevant language conventions:

- R: `.claude/rules/r-code-conventions.md` or the R section of `code/AGENTS.md`
- Julia: `.claude/rules/julia-code-conventions.md` or the Julia section of
  `code/AGENTS.md`
- MATLAB: `.claude/rules/matlab-code-conventions.md` or the MATLAB section of
  `code/AGENTS.md`

Also read the refactoring protocol from `.claude/rules/refactoring-protocol.md`
or the Refactoring Protocol section of `AGENTS.md`.

### 3. Apply Only Approved Transformations

- Comment style
- Whitespace and indentation
- Variable grouping and section organization
- Missing documentation
- Language-specific style conventions

Do not change logic, tolerances, function signatures, or dead-code behavior.

### 4. Verify Outputs

Run `/verify-outputs [target]` to compare against the baseline checksums.

### 5. Present Results

- If outputs match, present the diff and report that the refactoring preserved
  outputs.
- If outputs mismatch, revert all changes and report what broke.

### 6. Review

Run the appropriate review skill after the refactor.

## Important

- The only acceptable outcome is identical output.
- Dead code may be flagged but not removed.
- Revert everything on any output mismatch.
