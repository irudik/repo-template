# Solver Debugging

Use this when a numerical solver fails or returns an implausible answer in
MATLAB, Julia, R, or Python.

## Checks

Work from the cheapest and most common causes toward the rarer ones. Stop as
soon as the evidence isolates the cause, and skip a check the symptom already
rules out.

1. Dimensions: matrices conform and vectors have the expected length.
2. First NaN or Inf: find the first operation that produces one and trace
   backward from it.
3. Input data: nothing passed to the solver is NaN, Inf, or missing.
4. Starting values: the initial guess satisfies the bounds and constraints.
5. Bounds: shares are non-negative and probabilities lie in [0, 1].
6. Derivatives: compare analytic gradients and Hessians with finite
   differences.
7. Conditioning: check the condition number of the Jacobian or Hessian.

## Limits

- Show evidence for the cause you report: the failing line, the offending
  value, or the comparison that isolates it. A guess presented as a diagnosis
  sends the next person in the wrong direction.
- Loosening a tolerance, changing solver options, or switching algorithm can
  hide a failure and changes the reported results, so none of these is a
  diagnostic step. Whether to make such a change is decided by
  `Ask the User When` in root `AGENTS.md`, including its exceptions.
- Do not wrap the solver in `try`/`catch` to silence an error. Catching an
  error in order to record it and stop is fine.

## After the Diagnosis

When the task was to fix the failure, make the fix and rerun the solver. When
the task was only to diagnose, report the cause and the fix you would make.
Either way the report says what failed, where the first error arose, the
cause with its evidence, and what was done or proposed.
