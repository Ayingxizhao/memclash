# 0004. Conditions the model cannot express become unknown facts

Date: 2026-11-19. Status: Accepted.

## Context
On the large folders, the first translations reported 20 clashes, all false. One cause: the
translator dropped conditions it could not express, so "never commit to the local clones" became
"never commit", which then clashed with every rule that requires a commit.

## Decision
A condition the model cannot express ("in the local clones", "during a backlog sweep") is kept
as `when_unmodeled`. The checker turns it into a fresh unknown yes/no fact for that clause, so
the clause applies only when that fact holds. An `only_if` whose requirement cannot be expressed
becomes an unknown requirement the agent can meet.

Rule of thumb: dropping a requirement can only cause missed clashes; dropping a condition causes
false clashes. So conditions are never dropped.

## Consequences
- False clashes on the large folders went from 20 to 0.
- Known blind spot: two rules naming the same unexpressible condition get two different unknown
  facts, so their clash is missed (for example "during a sweep, review" vs "during a sweep, never
  review"). A fix is to let rules that name the same condition share one fact.
