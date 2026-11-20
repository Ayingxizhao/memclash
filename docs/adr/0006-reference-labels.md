# 0006. Build the reference from two separate readers plus the author's decision

Date: 2026-11-19. Status: Accepted.

## Context
The large folders have no labels, and the checker reported 0 clashes there. One reader alone is
not a reliable reference, and paying for more LLM API calls was ruled out.

## Decision
Two readers look for clashes in the 212 kept git rules without API calls:
- Codex, with no access to the checker's output (`prompts/git/codex_find_clashes.md`);
- Claude, who had seen the checker's output (so not independent), in a pass that assigns every
  rule to a topic and records why each checked pair is not a clash.

Every pair either reader flags is shown to the author on a review page
(`.lavish/clash_review.html`) in plain words, and the author's labels under ADR 0003 are the
reference (`data/runs/git/large_filter/reference_labels.json`).

## Consequences
- Pairs neither reader flags are not reviewed, so the reference can miss clashes.
- Result: 16 pairs reviewed; under ADR 0003, 11 are clashes, 2 are clashes only if "firmware"
  counts as "not hardware code", and 3 are not clashes. The checker found none of them: 9 are
  about tool choice, 1 about dev-bot testing, and 1 depends on "backlog sweep", none of which the
  model can express.
- The readers disagreed on several pairs, and each missed pairs the other found, which supports
  using two readers.
