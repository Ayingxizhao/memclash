You are an external reviewer for a class project. Work read-only (do not edit or create files;
your final message is saved). Do not open `data/gold/` or any file named `labels_*`. Do not
call any paid API.

Read `docs/review/experiment_design.md`, then as needed `docs/adr/0003`, `0007`, `0008`,
`pipeline/rules/` (the checker), `prompts/rules/translate.md`, `data/inject/dev_pilot.json` and
`data/inject/dev_pilot_rules.json`.

Critique the design, focusing on run A (the pilot), which will be run next and costs money:
1. Will each measure actually answer its question? Is anything measured that answers nothing,
   or is any question left unanswered?
2. Are the planted pairs and the in-scope / out-of-scope split correct? Check the planted
   rules against the vocabulary yourself.
3. Are the stop rule and the "decided before running" choices sound? Anything that should be
   fixed in advance but is not (e.g. how a pair counts when one run is unclear)?
4. Anything that would make the results misleading or not reportable?
Give numbered, concrete changes (exact text where possible), most important first. Under about
700 words. Plain language. Say plainly when unsure.
