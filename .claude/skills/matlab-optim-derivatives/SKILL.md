---
name: matlab-optim-derivatives
description: Audit MATLAB optimization derivatives and KNITRO integration with finite-difference validation
disable-model-invocation: true
argument-hint: "[path to MATLAB objective/constraint files]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
workflow_stage: solver-debug
compatibility:
  - codex
  - claude-code
  - cursor
  - gemini-cli
version: 1.0.0
tags:
  - matlab
  - optimization
  - knitro
  - gradient
  - hessian
---

# MATLAB Optimizer Derivative Audit

## Purpose

Validate analytic gradients, Hessians, and constraint Jacobians against numerical derivatives and confirm optimizer callback wiring is correct.

## When to Use

- Debugging matlab optimization functions and functions that call the solvers
- KNITRO convergence failures or suspicious solutions
- Suspected sign/index/scaling errors in derivative code
- Pre-port validation before translating MATLAB solver logic

## Workflow

1. Locate optimization stack.
- Find objective and constraint definitions.
- Find KNITRO call sites and callback registration.

2. Verify parameter plumbing.
- Confirm variable ordering and shape assumptions.
- Confirm scaling and bounds mapping.
- Confirm any transformed parameterization is inverted correctly.

3. Validate derivatives numerically.
- Compute finite-difference gradient checks.
- Compute Hessian checks (or Hessian-vector checks where appropriate).
- Validate constraint Jacobian entries.

4. Isolate mismatch sources.
- Classify by sign errors, missing terms, index offsets, scaling issues.
- Reproduce on minimal parameter vectors and test cases.

5. Report and patch.
- Provide mismatch table with absolute and relative errors.
- Provide concrete patch suggestions tied to line-level logic.
- Re-run checks after edits.

## Required Checks

- Objective gradient vs finite differences
- Hessian symmetry and finite-difference consistency
- Constraint Jacobian vs finite differences
- Callback dimensions/order expected by KNITRO
- Bounds and scaling consistency

## Output Template

- `Functions audited`: objective, constraints, callbacks
- `Check points`: parameter vectors used
- `Derivative errors`: max abs/rel by block
- `Likely causes`: ranked root causes
- `Patch plan`: file-level actions
- `Recheck`: pass/fail after changes

## Guardrails

- Keep algorithm choice unchanged unless requested.
- Treat "numerically close enough" with explicit tolerances.
- Separate optional Julia-port notes from core derivative audit.

## Test Guidance

- Use multiple points, not just one nominal calibration.
- Include edge-case points near bounds.
- Persist a small reproducer test to prevent regression.
