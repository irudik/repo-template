# Compare Branch Outputs Protocol

Compare script outputs between two branches to verify identical results.

## Arguments

- `base-branch`: reference branch such as `main`
- `target-branch`: branch with changes
- `dir-or-script`: directory or script to compare

## Steps

### 1. Set up a worktree for the base branch

```bash
git worktree add /tmp/branch-compare-base <base-branch>
```

### 2. Run scripts on the base branch

In the worktree, run via `make` when available or directly otherwise. Record
checksums for stable-format outputs such as CSV, TSV, and generated `.tex`
files.

### 3. Run scripts on the target branch

Repeat the same execution and record checksums.

### 4. Compare outputs

```text
## Branch Comparison: [base] vs [target]
| File | Base MD5 | Target MD5 | Status |
|------|----------|------------|--------|
```

For small CSVs smaller than 1 MB that differ, show a content diff.

### 5. Clean up

```bash
git worktree remove /tmp/branch-compare-base
```

## Important

- Follow the verification-format rules for which formats are checksum-stable.
- Always clean up the worktree.
- Do not modify files on either branch.
