# Commit, PR, and Merge

Use only when the user asks for it. Invoking `/commit` authorizes the standard
commit, push, PR, and merge cycle; a narrower request limits the work to that
step. A requested commit or merge needs no second confirmation.

1. Inspect the branch, working tree, diff, and recent commits. Identify the
   requested changes and exclude unrelated work and secrets from staging.
2. If the current branch is a non-`main` branch, keep using it.
   If the current branch is `main`, detached, or the user explicitly asks for a
   new branch, create one with `git switch -c <branch-name>`.
   Keep branch naming tool-neutral. Use a working branch for commits so the
   changes can be reviewed before merging, unless the user requests otherwise.
3. Choose Make verification in proportion to the files being committed:
   - Changed Makefiles or dependencies: scoped dry run, then affected target.
   - Source under an unchanged Makefile: relevant target, using existing
     successful results unless further changes invalidate them.
   - Cross-cutting work: root `make -n` when the full dependency plan helps.
   - Documentation and instruction-only changes require no Make dry run.
4. Resolve blocking defects under `Defects That Block a Commit or Merge` in
   root `AGENTS.md`; distinguish advisory items from those defects.
5. For a template-maintenance merge, first remove this branch's ad hoc plans,
   handoffs, logs, reports, and scratch files; keep intentional template
   assets and `.gitkeep` files. Include tracked removals in the commit.
   Stage explicit paths with `git add <paths>` to avoid unrelated changes.
   Exclude secrets and local tool state such as `.claude/settings.local.json`.
   Use the supplied commit message exactly, or write one explaining the change,
   then create the commit with `git commit -m "<message>"`.
6. Push the working branch, setting its upstream on first push with
   `git push -u origin <branch-name>`. Create or update its PR with the final
   scope and relevant validation; use `--body-file` for multiline descriptions.
7. Merge with
   `gh pr merge <pr-number> --merge --delete-branch`, unless the user requested
   another merge method, then switch to `main` and pull.

Follow `Reports and Updates` in `protocols/writing.md`: report the commit or
PR link, what was included, and unresolved advisory items or verification limits.
