# Review and Address PR Comments Protocol

Fetch unresolved review threads from a pull request, categorize by confidence,
implement fixes, commit modularly, reply with commit hashes, resolve threads,
and report uncertain items back to the user.

## Steps

### Step 1: Parse the PR Reference

Extract the PR number from the argument. Error if it is missing.

Derive owner and repo:

```bash
OWNER_REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
OWNER=$(echo "$OWNER_REPO" | cut -d'/' -f1)
REPO=$(echo "$OWNER_REPO" | cut -d'/' -f2)
```

### Step 2: Check Out the PR Branch

```bash
gh pr checkout $PR_NUM
```

Abort if the checked-out branch is `main`.

### Step 3: Fetch Unresolved Threads via GraphQL

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          comments(first: 50) {
            nodes {
              body
              author { login }
              databaseId
              createdAt
            }
          }
        }
      }
    }
  }
}' -F owner="$OWNER" -F repo="$REPO" -F pr=$PR_NUM
```

### Step 4: Filter and Categorize

- Skip resolved threads.
- Flag outdated threads as informational only.
- Classify remaining threads:

| Confidence | Criteria | Action |
|------------|----------|--------|
| HIGH | Clear code fix | Implement, commit, resolve |
| MEDIUM | Ambiguous but likely | Implement, stage, ask user |
| LOW | Design question or unclear | Report only |

### Step 5: Group by File Path

Group actionable HIGH and MEDIUM threads by file path. Each group becomes one
atomic commit unit.

### Step 6: Implement, Verify, and Commit per Group

1. Implement the file-group changes.
2. Verify with `make -n` and a relevant build when applicable.
3. Run the appropriate review skill when applicable.
4. Apply quality gates.
5. For HIGH-confidence groups that pass, commit:

```bash
git add <files in group>
git commit -m "<message referencing the review comment>"
```

6. Reply and resolve HIGH-confidence threads:

```bash
gh api repos/$OWNER/$REPO/pulls/$PR_NUM/comments/$COMMENT_DB_ID/replies \
  -X POST -f body="Addressed in $(git rev-parse --short HEAD)."

gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { isResolved }
  }
}' -F threadId="$THREAD_ID"
```

### Step 7: Push

```bash
git push
```

### Step 8: Present a Summary Table

Report four sections:

- Addressed
- Needs approval
- Needs user input
- Outdated

## Important

- Never commit to `main`.
- Never resolve a thread without a committed fix.
- Keep one commit per file group.
- Do not stage sensitive files.
- Do not touch outdated threads.
