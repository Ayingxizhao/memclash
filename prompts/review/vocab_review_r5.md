Round 5. You are co-authoring a fixed vocabulary with Claude. Work read-only (do not edit or
create files; your final message is saved). Do not open `data/gold/` or any file named
`labels_*`. Do not call any paid LLM API.

Since you signed off v1, two critical reviews were written (`docs/review/attack_review_claude.md`,
`docs/review/attack_review_codex.md`) and the user chose the scope: git plus basic file rules.
Claude rewrote the draft as v2: `docs/review/vocab_draft.md`. Main changes: `run` + fixed task
list; `in_repo` as a state with must_hold / never_hold; the "try every reading" feature
replaced by "words to watch" (translate from context, else flag `unclear` and exclude);
`may` always strong permission; cut `actor`, copy, "gitignored", file groups.

Read v2 in full. Reply in Markdown, under about 500 words:
1. Is any item in v2 still unjustified, contradictory, or inconsistent with the checker or ADR 0003?
2. Did v2 drop anything from v1 that is needed for the user's examples (force push vs never
   force push; may delete merged branches vs never delete branches; never push without ask vs
   final step pushes to main; delete map data vs never delete server-world.dat; object folder
   vs flat files; never commit vendor/ vs vendor/cmake stays committed; tests only when asked
   vs always run all tests)? For each example, say which it is: clash / unclear-excluded /
   unmodeled under v2.
3. Exact text changes, numbered. If none, write `SIGN OFF`. Do not repeat the draft back.
