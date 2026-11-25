You are co-authoring a fixed vocabulary with Claude for a class project. Work read-only (do not
edit or create files; your final message is saved). Do not open `data/gold/` or any file named
`labels_*`. Do not call any paid LLM API.

Read: `docs/review/vocab_draft.md` (Claude's merged draft), your own earlier report
`docs/review/schema_research_codex.md`, Claude's report `docs/review/schema_research_claude.md`,
`pipeline/git/git_check.py`, `prompts/git/git_translate.md`, `docs/adr/0003-clash-definition.md`.
You may look at survey results in `data/runs/survey/` and memory folders in `data/github/explore/`
to check that the vocabulary fits real rules.

Goal: one list both of you can sign. It must (a) let Z3 check pairs exactly, (b) make three
independent translations of the same rule agree as often as possible, (c) stay as small as
possible while covering the examples in the draft.

Output, in Markdown, under about 1200 words:

1. For each draft section 1–7: `AGREE`, or `CHANGE` with the exact replacement text
   (ready to paste) and one line of reason. Be concrete; no general advice.
2. Anything missing that real rules in the survey need (quote the rule and its folder).
3. Anything you think is wrong but cannot fix with a short replacement: say so as an open point.

Say plainly if you are unsure. Do not repeat the draft back.
