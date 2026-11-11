# Trace an Ambiguous Result

Use for unexpected estimates, dropped rows, stale builds, solver failures,
or disagreement between code, tables, and manuscript numbers.

1. Establish what was observed and expected using concrete files, commands,
   outputs, or errors. Keep observation separate from interpretation.
2. Read the smallest relevant set of source files, inputs, Makefiles, logs,
   outputs, and changes. Prefer direct evidence over timing or resemblance.
3. Consider competing explanations unless the evidence already isolates the
   cause: logic, sample or merge keys, dependencies, interpretation, or
   numerical instability. Identify predictions that distinguish them.
4. Test the plausible explanations against the available evidence. Rank them
   by support, accounting for contradictions and assumptions still unverified.
5. Identify the missing fact that most limits confidence and the next check
   most likely to resolve it. Run that check when available and within scope;
   stop expanding diagnosis once the cause is demonstrated.
6. For solver failures, use `protocols/solver-debugging.md`.
   For a diagnosis-only request, leave source unchanged. When the user asked
   for a fix, continue through the supported correction and its verification;
   a delegated read-only reviewer returns the evidence for the parent to act on.

Return findings to the agent that started the review. Distinguish conclusions
from reading code and conclusions supported by something actually run.

Follow `Reports and Updates` in `protocols/writing.md`. In plain prose, explain
what was observed, the best-supported explanation and its evidence, what is
still uncertain, and the next check or the result of that check; include any
requested fix and its verification.
