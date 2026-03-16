# Commit, PR, and Merge Protocol

Stage changes, commit with a descriptive message, create a PR, and merge to `main`.

## Steps

1. **Check current state:**

```bash
git status
git diff --stat
git log --oneline -5
```

If a root `Makefile` exists, run `make -n` to check for stale targets. If stale
targets exist, warn the user before proceeding. This is a soft gate.

2. **Create a branch** from the current state:

```bash
git checkout -b <short-descriptive-branch-name>
```

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

```bash
git push -u origin <branch-name>
gh pr create --title "<short title>" --body "<summary and test plan>"
```

6. **Merge and clean up:**

```bash
gh pr merge <pr-number> --merge --delete-branch
git checkout main
git pull
```

7. **Report** the PR URL and what was merged.

## Important

- Always create a new branch. Never commit directly to `main`.
- Exclude sensitive files from staging.
- Use `--merge` unless the user explicitly asks for `--squash` or `--rebase`.
- If a commit-message argument is provided, use it exactly.
