# Architecture decision records

One file per decision, in the format of Michael Nygard's ADRs: Context, Decision, Consequences.
Numbers are never reused. A decision that changes is not edited; a new ADR supersedes it.

| # | Decision | Status |
|---|---|---|
| [0001](0001-record-decisions.md) | Record decisions as ADRs | Accepted |
| [0002](0002-narrow-to-git-rules.md) | Narrow the exact method to git rules and a fixed git model | Accepted |
| [0003](0003-clash-definition.md) | A clash means no single action satisfies both rules; "may" is a strong permission | Accepted |
| [0004](0004-unexpressible-conditions.md) | Conditions the model cannot express become unknown facts | Accepted |
| [0005](0005-git-filter.md) | Find git rules with keywords OR an LLM question; estimate misses by sampling | Accepted |
| [0006](0006-reference-labels.md) | Build the reference from two separate readers plus the author's decision | Accepted |
| [0007](0007-tuning-vs-final-test.md) | Large folders are tuning data; the held-out folders are run once | Accepted |
