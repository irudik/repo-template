# Handing Work from Claude to Codex

Use this procedure only when the user asked for it during the task or while
planning, with wording such as "hand this to Codex", "delegate execution to
Codex", or "Codex executes", or with a `[codex]` marker on plan steps.
Otherwise Claude does the work itself.

## Plan

Record a `Codex Handoff` section in the saved plan with: the steps Codex
carries out, the path of the plan, the acceptance criteria, the commands
expected to verify the result, that Codex does not commit unless told to, and
a note to handle the `data/` and `output/` links with care. Then send the plan
to the `codex:codex-rescue` subagent with write access. Wait for plan approval
first only when the user asked for that step.

## Roles

Codex implements the change and its verification. It adds or updates whatever
is needed to make the acceptance criteria checkable, such as unit tests,
example inputs, Make targets, data-property checks, or checksum scripts.
Before handing back, Codex reviews its own diff and results, fixes obvious
gaps, and reports the exact evidence.

Claude plans and reviews. It reviews Codex's changes, verification design,
and reported results against the acceptance criteria, confirms that the
relevant tests pass, and names gaps for Codex to fix. Allow one Codex fix and
one Claude re-review by default. Use more rounds only when the user asks, or
when a failure is still unexplained after normal diagnosis; state the open
hypotheses and when to stop before adding rounds. Claude does not write the
verification code or rerun the full verification unless the user asks.

## Background Jobs

A handoff that runs in the background returns only a job ID within seconds,
and Claude does not run again until something wakes it, so a finished job can
sit unreported. Immediately after starting such a job, start a background
watcher that waits on the plugin's own status command
(`codex-companion status <jobId> --wait`) with a time limit. When the watcher
exits, Claude is invoked again and reports the result without being asked. If
the time limit is reached first, say in one line that the job is still
running, start the watcher again, and keep going until the job finishes or
fails. A handoff run in the foreground, or with `--wait`, needs no watcher.
Drop the watcher if the Codex plugin gains its own completion signal.
