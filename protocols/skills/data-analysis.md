# R Data Analysis

Follow `protocols/conventions/shared.md` and `protocols/conventions/r.md`.
Put numbered scripts in `code/<task_group>/`, with outputs under `output/`.
Save objects and diagnostics that later steps or reproduction need.

1. State the research question, sample, estimand, and identifying assumptions
   from the request and project specification. Document inputs and outputs;
   load packages and, for stochastic work, set the seed once at the top.
2. Inspect variable types, missingness, distributions, panel trends, and
   relevant group comparisons. Check key uniqueness, join outcomes, sample
   counts, and aggregation totals before estimation.
3. Implement the specified design: `fixest` for suitable panel regressions,
   `lm()` or `glm()` where appropriate. Explain clustering, fixed effects,
   weights, and sample restrictions. Check outliers, collinearity, separation,
   and whether coefficients and uncertainty have the intended interpretation.
4. Produce tables with coefficients, standard errors, sample size, and useful
   fit statistics, preferably through `modelsummary`. Export LaTeX tables and
   an easily inspected format when useful.
5. Use `ggplot2` and the project theme, with readable labels, units, and explicit
   dimensions; use a transparent background where LaTeX requires it. Save
   figures in the formats downstream documents need and key objects with
   `saveRDS()`. Let Make create output directories.
6. Apply the risk-based review rule in `AGENTS.md` to substantive estimation,
   sample, or manuscript-result changes; address blocking defects before
   presenting the analysis as complete.

Follow `Reports and Updates` in `protocols/writing.md`: explain the main
estimates with units and uncertainty, sample and specification, and limitations.
