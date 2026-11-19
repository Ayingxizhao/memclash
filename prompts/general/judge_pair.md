You compare TWO rules from the same coding agent's memory folder. Both are loaded in the same
session. Decide which relation holds between them. Apply the labels in this order and take
the first that fits:

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
6. none: unrelated, compatible, merely the same topic, or one states an explicit exception
   to the other.

Most pairs are `none`. Do not invent a relation.

Return JSON: {"label": "duplicate|contradiction|override|stale|tension|none",
              "explanation": "one sentence"}
