# MATLAB Optimizer Derivative Audit

Audit objective gradients, Hessians, constraint Jacobians, and KNITRO callback
connections. For solver failures, also use
`protocols/solver-debugging.md`.

1. Locate objectives, constraints, solver calls, and callback registration.
   Check parameter ordering, dimensions, transformations and inverses, bounds,
   and scaling against the mathematical specification.
2. Compare analytic gradients and constraint Jacobians with finite differences
   at several parameter vectors, including feasible points near bounds. Choose
   feasible perturbations and check sensitivity to finite-difference step size.
3. Check Hessian symmetry and finite-difference or Hessian-vector agreement,
   including the constraint contributions expected by the solver callback.
4. Isolate sign errors, missing terms, index offsets, and scaling errors with
   small reproducible inputs. Record absolute and relative errors against
   explicit, justified tolerances; keep a small regression test for a fix.
5. For an audit-only request, return findings. When fixes are requested, correct
   demonstrated errors and compare derivatives again. Keep solver algorithms,
   options, and convergence criteria unchanged during an audit because changing
   them obscures the source of failure; change them only when requested.

Return findings to the agent that started the review, distinguishing code
reading from checks actually run. Follow `Reports and Updates` in
`protocols/writing.md`: name audited functions and test points, derivative
errors and tolerances, supported causes, fixes, and remaining uncertainty.
