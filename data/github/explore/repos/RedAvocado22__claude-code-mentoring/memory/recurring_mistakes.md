---
name: recurring-mistakes
description: "Mistakes that happened more than once — tracked by name so Claude can call them out on the second occurrence"
metadata:
  type: feedback
---

Each entry: pattern name, description, count.

When Claude sees a mistake for the second time, it names the pattern directly:
"This is the 2nd time — [PATTERN_NAME]. Fix this into a habit."

---

## Carry-over Mistakes (from past projects — likely to recur)

**ONE_GIANT_COMMIT** [0 occurrences]
Bundling all changes into one commit at the end of a feature. Kills `git bisect` and targeted reverts.
Fix: commit after each coherent change — method done, bug fixed, new file wired up.

**POST_PAGINATION_FILTER** [0 occurrences]
Filtering a result set after fetching the page instead of at query level. Breaks page sizes and total counts.
Fix: push filters into the WHERE clause, not Java streams after fetch.

<!-- Add your own carry-over mistakes here based on your past projects -->

---

## Project-Specific Mistakes (track as they appear)

<!-- 
Format:
**PATTERN_NAME_IN_CAPS** [0 occurrences]
What happened / what the mistake looks like.
Fix: the correct approach.
-->

**EXAMPLE_PATTERN** [0 occurrences]
[Describe the mistake concisely — what did you do wrong and what went wrong as a result]
Fix: [the correct behavior]

---

## Claude's Own Mistakes (things Claude got wrong)

<!-- 
Track mistakes Claude makes during this project — wrong assumptions, stale memory used without verification, etc.
This keeps Claude accountable to the same standard.
-->

**ASSUME_WITHOUT_READING** [0 occurrences]
Raising an issue about two files being inconsistent without reading both first.
Rule: before claiming "file A uses X but file B uses Y", read both — no assumptions.
