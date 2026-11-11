# Review Numerical Results in LaTeX

Run when results or the prose around them changed. Review supplied documents;
`all` means all `.tex` files under `latex/`. Include affected prose uses across
documents unless the user explicitly limits scope.

## Changed Values

1. Read `output/numbers/*.txt` and relevant `\input{...}` lines to map generated
   `\newcommand` definitions to sources and rendered values. Record definitions
   before a producing script runs and compare afterward; a reliable version
   control baseline can substitute if review begins after rebuilding.
2. Compare macro contents, not file modification times. Include added, removed,
   and changed definitions; identical regenerations need no context review.
   Without reliable earlier definitions, state the limitation and review all
   prose uses of macros in regenerated files.
3. Review every prose occurrence of each changed macro in manuscripts, slides,
   captions, and notes, following aliases and prose wrappers. Read the complete
   sentence and nearby context needed to assess its claim.
4. Check articles based on the spoken phrase, singular/plural agreement, sign
   and direction, units and scales, currency, percent versus percentage points,
   comparisons, ranges, thresholds, and qualitative magnitudes or rankings.
   Intervening prose matters: `a roughly 8\% change` differs from
   `an approximately 8\% change`.
5. Keep generated macros value-only. Do not replace contextual reading with
   generated sentence fragments or a general article-selection function.

## Hardcoded Results

Inspect empirical values in running prose, especially currency amounts,
percentages, standard-error-like parentheses, and decimals near result claims.
Exclude math/table environments, preambles, comments, citations, reference and
layout commands, years, ordinals, and structural descriptors. In slides,
distinguish substantive estimates and policy quantities from agenda counts,
dates, and orientation numbers.

Match suspicious values to generated macros by meaning and source, not numerical
coincidence. Trace unmatched results through `code/` and Makefile producers.
When one computation unambiguously supplies the value, add its value-only macro,
Makefile dependencies, and TeX use; rebuild the producer and confirm agreement.
Fix changed-value wording only when the generated value and context determine
the correction. Leave ambiguous claims or source choices unchanged and report
them. A review-only request excludes these edits. After edits, compile affected
documents through `make -C latex` and inspect the changed passages.

If both generated numbers and producing code are absent, hardcoded-number
findings are informational rather than demonstrated pipeline defects.

Return findings to the agent that started the review, distinguishing reading
from checks actually run and blocking defects from advisory items under root
`AGENTS.md`. Follow `Reports and Updates` in `protocols/writing.md`: summarize
the baseline, old and new values, fixes and verification limits; name only
locations where wording changed or a question remains, not every reviewed use.
