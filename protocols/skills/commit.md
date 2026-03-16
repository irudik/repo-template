# Commit, PR, and Merge Protocol

Stage changes, commit with a descriptive message, create a PR, and merge to `main`.

## Steps

1. **Check current state:**

```bash
git branch --show-current
git status
git diff --stat
git log --oneline -5
```

If a root `Makefile` exists, run `make -n` to check for stale targets. If stale
targets exist, warn the user before proceeding. This is a soft gate.

2. **Choose the working branch:**

- If the current branch is a non-`main` branch, keep using it.
- If the current branch is `main`, detached, or the user explicitly asks for a
  new branch, create one first:

  ```bash
  git switch -c <short-descriptive-branch-name>
  ```

- Never commit directly to `main`.

3. **Stage files** with specific `git add` targets. Never use `git add -A`.

Do not stage `.claude/settings.local.json`, `.codex/` local state, or any files
containing secrets.

4. **Commit** with a descriptive message.

If a commit-message argument is provided, use it exactly. Otherwise, analyze the
staged changes and write a message that explains why the change exists, not just
what changed.

```bash
git commit -m "<commit message>"
```

5. **Push and create the PR:**

- Push the branch you committed on. If it does not already track a remote branch,
  set the upstream on first push:

  ```bash
  git push -u origin <branch-name>
  gh pr create --title "<short title>" --body "<summary and test plan>"
  ```

6. **Merge and clean up:**

- For template-maintenance branches in this repository, remove branch-specific
  working artifacts before merging to `main`. In particular, clear ad hoc files
  under `quality_reports/plans/`, `quality_reports/session_logs/`,
  `quality_reports/merges/`, and scratch directories such as
  `quality_reports/thorny_loop/` unless they are intentional template assets.
  Keep placeholder `.gitkeep` files and durable templates.

```bash
gh pr merge <pr-number> --merge --delete-branch
git switch main
git pull
```

7. **Report** the PR URL and what was merged.

## Important

- Reuse the current non-`main` branch by default.
- Create a new branch only when on `main`, in detached HEAD, or when the user
  explicitly asks for one.
- Keep branch naming tool-neutral. Any Codex or Claude client naming
  preferences are local constraints, not shared protocol rules.
- For template-maintenance work in this repo, merge back to `main` with a fresh
  tree: branch-local `quality_reports` artifacts should not land on `main`
  unless they are intentional template files.
- Exclude sensitive files from staging.
- Use `--merge` unless the user explicitly asks for `--squash` or `--rebase`.
- If a commit-message argument is provided, use it exactly.
