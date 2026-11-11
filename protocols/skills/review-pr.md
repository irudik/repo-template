# Address PR Review Comments

Use only when the user asks for it. This workflow implements supported fixes,
commits and pushes them, replies with commit hashes, and resolves addressed
threads; a review-only request limits it to findings.

Run each command separately. Replace bracketed values with actual values from
preceding results; do not rely on shell variables or command substitution.

```bash
gh repo view --json name,owner
gh pr view <pr-number> --json number,headRefName,baseRefName,url
git status
gh pr checkout <pr-number>
```

Preserve pre-existing changes when checking out. Use the PR's working branch
rather than `main` so fixes stay on the reviewed change; if it points to `main`,
leave it unchanged and report the branch problem.

Fetch threads with literal owner, repository, and PR values:

```bash
gh api graphql -f query='query { repository(owner: "<owner>", name: "<repo>") { pullRequest(number: <pr-number>) { reviewThreads(first: 100) { pageInfo { hasNextPage endCursor } nodes { id isResolved isOutdated path line comments(first: 100) { pageInfo { hasNextPage endCursor } nodes { id databaseId body author { login } } } } } } } }'
```

Follow pagination for both threads and comments using returned cursors. Skip
resolved threads; leave outdated threads untouched unless the user requests
otherwise. Assess each remaining claim against code and specification. Implement
clear corrections in related groups; leave ambiguous research or design choices
unchanged and explain the uncertainty. Apply relevant checks and resolve blocking
defects under root `AGENTS.md` before committing; treat style items as advisory.

```bash
git add <specific-files>
git commit -m "<message explaining the correction>"
git rev-parse --short HEAD
git push
```

Exclude secrets and unrelated changes. After a fix is committed and pushed,
reply to the specific comment addressed, using its `databaseId` and the actual
commit hash, then resolve that thread by its GraphQL `id`:

```bash
gh api repos/<owner>/<repo>/pulls/<pr-number>/comments/<comment-database-id>/replies -X POST -f body='Addressed in <commit-hash>.'
gh api graphql -f query='mutation { resolveReviewThread(input: { threadId: "<thread-id>" }) { thread { isResolved } } }'
```

Resolve a thread only when its concern has been addressed with a committed fix;
leave questions or disputed requests open unless the user directs otherwise.
Follow `Reports and Updates` in `protocols/writing.md`: explain addressed concerns
with commit links, verification, and items left open with reasons.
