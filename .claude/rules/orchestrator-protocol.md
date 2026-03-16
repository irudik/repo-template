# Orchestrator Protocol: Contractor Mode

> **Routing:** Use this full loop for multi-file or cross-cutting changes. For single-file R/Julia/Stata/MATLAB script tasks, use `orchestrator-research.md` instead.

**After a plan is approved, the orchestrator takes over autonomously.**

## The Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Run `make -n` to check staleness; build stale targets
  │         If Makefile exists: `make -C code/[dir] [target]` or `make -C latex`
  │         Otherwise: compile/render/run directly
  │         If verification fails → fix → re-verify
  │
  Step 3: REVIEW — Run review agents (by file type)
  │
  Step 4: FIX — Apply fixes (critical → major → minor)
  │
  Step 5: RE-VERIFY — Confirm fixes are clean
  │
  Step 6: SCORE — Apply quality-gates rubric
  │
  └── Score >= threshold?
        YES → Continue to Step 7
        NO  → Loop back to Step 3 (max 5 rounds)
              After max rounds → continue to Step 7 with remaining issues
  │
  Step 7: OPTIONAL REVIEWS — If the approved plan requests them:
  │         • Domain substance review → run `domain-reviewer` agent
  │         • Proofreading → run `proofreader` agent
  │         These run once on the final state, after the review-fix loop.
  │         They produce reports only — fixes require user review.
  │         Skip this step if the plan does not request optional reviews.
  │
  Step 8: Present summary to user (including optional review reports)
```

## Limits

- **Main loop:** max 5 review-fix rounds
- **Critic-fixer sub-loop:** max 5 rounds
- **Verification retries:** max 2 attempts
- Never loop indefinitely

## "Just Do It" Mode

When user says "just do it" / "handle it":
- Skip final approval pause
- Auto-commit if score >= 80
- Still run the full verify-review-fix loop
- Still present the summary
