# Feedback: Claude used jargon instead of plain language

Recorded 2026-11-19 (CS2520 project sessions, Nov 16–19), for a later memory entry.

## What happened

Claude kept using its own internal labels when explaining results. The user had to stop and ask
what they meant, sometimes twice for the same topic.

| Term Claude used | What it meant | What the user said |
|---|---|---|
| "demand" (of a rule) | what the rule requires | "Wait what does "demand" even mean?" then "use plain language throughout please" |
| "fact linking", "linked / unlinked" | telling the solver how two actions relate | "i understand about the numbers problem, but for the fact linking? i am not sure what that means" |
| "host", "exact pair", "rule that repeats the host" | the original rule a fake rule was written to clash with; that rule + the fake rule; another original rule that says the same thing | "whats exact pairs and whats rule that repeats the host?" |
| (second answer still used "host" and "exact pair" in the table) | | "plain language please" |

## The pattern

- Claude invents short labels while working (host, demand, link, side conflict, witness,
  clause, exact pair) and then uses them in answers as if the user knew them.
- When asked what a label means, Claude defined it but kept using it in the same answer,
  so the answer still read as jargon.

## What to do instead

1. Use everyday words in answers: "the rule I picked for it to clash with", not "host";
   "what the rule requires", not "demand"; "when the rule applies", not "scope".
2. Start with a concrete example (the actual two rules, quoted), then the general point.
3. If a technical term is needed, explain it in one plain sentence the first time, or leave
   it out.
4. When the user asks what a term means, rewrite the whole answer without that term; do not
   only add a definition.
5. Code names (`must_do`, `only_if`, `link`) stay in code blocks; do not use them in prose.
6. Tables: plain column names and an explicit target column (e.g. Kind / Injected / Target /
   Result), as the user asked earlier ("this way of naming table is cleareer").

## Before / after example

Before: "Found on the exact pair 2 of 6; via a rule that repeats the host 5 of 6."

After: "For each fake rule I picked one original rule for it to clash with. The check caught
2 of those 6 clashes. Some original rules say the same thing twice, and counting those
copies, 5 of the 6 fake rules were caught."
