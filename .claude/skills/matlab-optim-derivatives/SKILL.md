---
name: matlab-optim-derivatives
description: Audit MATLAB gradients, Hessians, constraint Jacobians, and KNITRO callbacks. Use for suspected derivative errors, solver failures, or validation before translating numerical code.
disable-model-invocation: true
argument-hint: "[path to MATLAB objective/constraint files]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
workflow_stage: solver-debug
compatibility:
  - codex
  - claude-code
  - cursor
  - antigravity
version: 1.0.0
tags:
  - matlab
  - optimization
  - knitro
  - gradient
  - hessian
---

Read `protocols/skills/matlab-optim-derivatives.md` and apply it to `$ARGUMENTS`.
