You are an independent, critical reviewer for a class project (CS2520, presented Dec 1). You
did not help write it. Work read-only: do not edit or create files; your final message is saved
as your report. Do not open `data/gold/` or any file named `labels_*`. Do not call any paid API.

## The project in brief

Coding agents keep memory folders of markdown rules. An LLM translates each rule alone into a
fixed vocabulary; Z3 then checks every pair of translated rules for a clash ("in some situation
both rules name, no single action satisfies both"; an explicit "may" must stay possible). The
scope is now git rules plus file rules. Each rule will be translated 3 times to measure
agreement, a hand-checked sample checks correctness, and 10 held-out folders with clash labels
are the final test.

Read: `README.md`, `docs/adr/` (all), `docs/review/vocab_draft.md` (the vocabulary, agreed by
two authors), `pipeline/git/git_check.py`, `prompts/git/git_translate.md`.

One fact to consider: a rough keyword count over the 60 survey folders (`data/github/explore/`)
found rule-like lines about running tests in 8 folders, builds 3, deploy 5, migrations 6,
lint/format 8, publish/release 7, restarting servers 3. The draft models only tests and builds.

## Questions

1. **Attack surface.** What will a grader or audience most likely attack: in the vocabulary,
   the clash definition, the evaluation plan, and the claims? Rank the top 8 by how damaging
   they are. For each: the attack in one sentence, and the smallest change that removes it or
   shrinks it (narrow a claim, cut a feature, add a measurement, add one sentence of
   justification). Prefer cutting or narrowing over adding work. Today is 2026-11-22.
2. **Unjustified parts.** Which items in the vocabulary (actions, fields, translation rows,
   multiple-meaning words) cannot be justified from the words' meaning, git's own definitions,
   or prior art? Should they be cut?
3. **One prompt or two?** Should git rules and file rules be translated with one prompt and one
   vocabulary, or two separate prompts? Consider rules that mix both ("never commit .env"),
   the routing step a split needs, cross-family clashes, prompt length, and agreement
   measurement. Recommend one.
4. **Running commands.** Given the counts above, keep only tests and builds, or replace them
   with one action `run` plus an opaque task name (exact-match only, like process names)?

Output: Markdown, under about 1500 words, sections 1–4, then a 5-bullet summary. Say plainly
when you are unsure. Write in plain language a person with no context can follow.
