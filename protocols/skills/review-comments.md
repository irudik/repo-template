# Comment and Documentation Cleanup

Review the requested files or directory, defaulting to the current directory.
Follow `protocols/writing.md` and any supplied style reference.

Find misleading or stale comments, incorrect docstrings, broken documentation
paths, commented-out code, and prose that merely repeats obvious mechanics.
Add comments where reasoning is not obvious, especially economic assumptions,
sample choices, and numerical decisions. Explain inputs and returns in
function documentation and keep file headers self-contained.

Use concise, plain language. Remove references to issue numbers, commits, or
AI conversations that require unseen context. Prefer purpose-based section
headings and mathematical notation when it helps; avoid a fixed comment quota.

When cleanup is requested, edit and check documentation against actual behavior
and referenced paths. Remove commented-out code within that scope; leave live
unused code unchanged unless its removal was requested, because removing it
could change behavior. For review-only requests, return findings without edits.

Return review findings to the agent that started the review, distinguishing
reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: summarize changes or findings with relevant locations,
proposed corrections, and anything left unchanged because its meaning is unclear.
