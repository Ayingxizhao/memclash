# Task: find clashing git rules

You are reviewing rules that coding agents keep in their memory folders. Read the file
`data/runs/git/large_filter/git_rules_for_review.md`. It has 4 sections, one per project folder.
Each line is one rule with its number (for example **R12**).

Find every pair of rules **in the same folder** that clash. Do not compare rules across folders.
Do not run any other script, do not call any API, and do not open other files in this repository.
Work only from the rules file.

## What counts as a clash

Two rules clash if there is a concrete, realistic situation where an agent that follows one
rule must break the other. Examples (made up):
- "Always push straight to main" vs "Never push to main without a PR": clash. Situation: the agent
  has a finished change and wants to push.
- "During a hotfix, skip review" vs "During a hotfix, get two reviews before merging": clash.
  Both rules apply in the same special situation (a hotfix).

These are NOT clashes:
- Two rules that say the same thing, or one is a stricter version of the other
  ("never force push" and "never force push to main").
- One rule states an explicit exception to the other ("require review, except in backlog sweeps").
- The rules apply to clearly different situations (one for the local clone, one for the remote).
- One rule is vague and you would have to stretch it to make it clash.

If you are unsure whether two situations are the same, still list the pair, but mark it
`unsure`.

## Steps

1. For each folder, read all its rules once before judging any pair.
2. Group the rules by topic (pushing, merging, PRs and reviews, branches, commits and what may be
   committed, worktrees, others).
3. Inside each topic, and between related topics (for example "merge" and "PR review"), check
   every pair. Also note which rules apply only in a special situation ("during a sweep",
   "for UI changes"), and compare rules that name the same situation with special care.
4. For each clash, write the situation in one sentence and say which rule is broken.
5. Review your list once more and remove pairs that fall under "NOT clashes".

## Output

Write the file `data/runs/git/large_filter/codex_clashes.json` with this content:

```json
{
  "clashes": [
    {"folder": "owner/name", "a": "R12", "b": "R40",
     "quote_a": "<rule text>", "quote_b": "<rule text>",
     "situation": "<one sentence: when this happens, following A breaks B>",
     "confidence": "sure" | "unsure"}
  ],
  "same_situation_pairs": [
    {"folder": "owner/name", "a": "R5", "b": "R9", "situation": "<the special situation both name>",
     "clash": true | false}
  ],
  "notes": "<anything about the rules or the task you found hard>"
}
```

Use exact rule numbers and copy the rule text exactly. An empty `clashes` list is a valid answer
if you find none.
