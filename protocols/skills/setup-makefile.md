# Generate Makefile from Directory Contents Protocol

Scan a directory for scripts and generate a Makefile following project
conventions.

## Steps

### 1. Scan the Directory

Glob for `.R`, `.jl`, and `.m` files.

### 2. Parse Output Paths

For each script, scan for write calls:

- R: `write.csv`, `write_csv`, `saveRDS`, `ggsave`, `writeLines`
- Julia: `CSV.write`, `jldsave`, `savefig`, `open(..., "w")`
- MATLAB: `writetable`, `writematrix`, `save`, `saveas`

Also scan for input paths to determine dependencies.

### 3. Generate the Makefile

Follow the relevant Makefile conventions:

- `all` as the default target with `.PHONY`
- Order-only prerequisites for directories
- Automatic variables such as `$<` and `$@`
- Joint production for multi-output scripts
- `.PRECIOUS` for expensive intermediates
- A `clean` target

### 4. Present for Review

Do not write directly. Present the generated content and ask for approval.

### 5. Write After Approval

Write the Makefile and update the parent `code/Makefile` delegation if needed.

## Important

- Always present for review before writing.
- Follow Makefile conventions exactly.
- Flag scripts whose outputs cannot be parsed reliably.
