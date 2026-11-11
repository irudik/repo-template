# Compare Branch Outputs

Given a reference branch, target branch, and script or directory, compare their
outputs using `protocols/skills/verify-outputs.md` for formats and tolerances.

1. Create temporary worktrees at unused paths for the branches that need them;
   preserve the user's current working tree and any pre-existing changes.
2. Inspect input and output paths before running either branch. Worktrees may
   share linked data or output directories; isolate outputs or capture the
   reference results before the target run can overwrite them.
3. In each worktree, run `make -n` for the relevant targets; if stale,
   rebuild them with `make`. Without a governing Makefile, run the script from
   its containing directory using the same inputs and environment.
4. Compare the same discovered outputs on both branches. Show a short content
   diff for differing CSVs smaller than 1 MB; distinguish missing files from
   changed contents and formats that cannot be compared by checksum.
5. Remove only temporary worktrees created by this task. Preserve source files
   on both branches because this skill compares results rather than edits code;
   make source changes only under a separate requested fix.

Follow `Reports and Updates` in `protocols/writing.md`: name the branches,
comparison coverage, differences, and any limits caused by inputs or environment.
