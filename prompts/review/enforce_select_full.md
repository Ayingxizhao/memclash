You classify rules for a research experiment. Work read-only; your final message is saved.
Open ONLY `data/runs/natural/full_blind.json` (1,287 real rules from coding-agent memory folders,
by folder) and `pipeline/rules/vocab.py` (the fixed vocabulary). Do NOT open any other file
under `data/` (no translations, labels, gold, frozen or held-out files). No paid API calls.

For EACH rule decide whether it is ELIGIBLE, using this fixed test and nothing else:

ELIGIBLE if both hold:
1. The rule forbids, permits, or sets a precondition on ONE agent action that the vocabulary
   can name: a git command (commit, push, force push, merge, PR create/merge, branch
   create/delete, checkout, pull, rebase, reset --hard, cherry-pick, fetch, worktree), a file
   action (read, create, edit, move, delete) on a path or path pattern, or running a task
   (test, build, lint, format, deploy, migrate, publish, restart, or a named task), possibly
   with branch, path, yes/no conditions such as user confirmation or tests passed, or one
   earlier step.
2. Looking at one proposed action (plus the earlier step it depends on) is enough to tell
   whether the rule is broken.

NOT ELIGIBLE: rules about writing style or the content of text/code; which tool, library,
shell or command style to use when the vocabulary has no name for it; obligations to do
something at some point ("always run tests before finishing"); numeric or time values the
vocabulary lacks; vague rules with no concrete action.

Judge from the English text only. Do not consider whether a rule would be easy for any
method. Output only a JSON object in a ```json block:
{"rules": [{"folder": "...", "id": "R..", "eligible": true|false, "reason": "<= 12 words"}]}
covering all 1,287 rules.
