You are given ALL rules of one coding agent's memory folder. All of them are loaded in the
same session. Find every pair of rules that stands in one of the relations below. Consider
every pair, including rules far apart in the list and rules from different files. Apply the
labels in this order and take the first that fits:

1. duplicate: both rules require the same behavior; the scope is the same, or one rule's
   scope is contained in the other's with the same behavior. Includes an index line that
   restates a file.
2. contradiction: there is a realistic situation in which both rules apply and the agent
   cannot comply with both. Counts: obligation vs prohibition of the same action; an explicit
   permission vs a prohibition. Does not count: an implied permission; rules that can both be
   satisfied by doing more (e.g. confirm AND proceed).
3. override: both rules are still meant to hold, but one (more specific, or newer) changes
   the behavior the other requires for part of its scope, without an explicit exception
   linking them.
4. stale: one rule is outdated relative to the other: it reflects an earlier state or
   decision that has been replaced (e.g. an index entry that no longer matches its file).
5. tension: both can be followed, but they pull in different directions, or it is unclear
   whether one rule's trigger covers the other's action.

Pairs that are unrelated, compatible, or merely on the same topic are not reported. Do not
invent relations.

Return JSON: {"relations": [{"a": "<rule id>", "b": "<rule id>",
  "label": "duplicate|contradiction|override|stale|tension", "explanation": "one sentence"}]}
