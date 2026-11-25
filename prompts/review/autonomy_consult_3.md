You are Codex, consulting as an equal partner. Read-only (no edits; final message saved). Do not
open `data/gold/`, files named `labels_*`, or `data/runs/survey_rules/label_set/frozen_2026-11-22.json`.
You may read `data/runs/survey_rules/dev_set/dev_labels.json` (dev set) and
`data/runs/rules/dev/*.json`. No paid APIs.

Read `docs/review/experiment_log.md` (E3) and `docs/review/vocab_draft.md`. Also review my
adjudication of the dev-set disagreements (`dev_labels.json`, entries with `adjudication_note`):
AGREE or name the ones you would change.

Two proposed design changes, from systematic dev errors (decide with me, under 600 words):

1. **Earlier-step details.** Add two situation fields: `after_task` (the task of an earlier
   `run`, same names as `task`) and `after_path` (the path of an earlier file action), next to
   `after` / `after_branch`. Fixes "after a build, ..." / "after editing the Xcode project
   file, run plutil" / "verify the build succeeds before committing", which today become
   `when_unmodeled` text or misplaced fields. Z3: like `after_branch` (strings, regions).
   This changes vocabulary v2 (ADR 0008), so it is a new version (v2.1).

2. **Lists of paths in must_do / may_do.** In our format a list in one must_do means "some
   path in the list" (OR). Both labellers and the model read "update A, B, C and D" or
   "create X.c and .h" as each file. Proposal: in code, a must_do or may_do with several path
   patterns is split into one clause per pattern (each must happen / each stays allowed);
   never / only_if lists are already "each". Actions in `cmd` stay OR ("must do A or B").
   Applied identically to labels and translations, in `action_clauses`.

Questions: are both sound and general (not tuned to one rule)? For 1, labels that encode such
conditions as `when_unmodeled` text would then disagree with a better translation: how should
the dev and frozen labels be updated without peeking bias (the frozen set has been scored once,
for the A/B baseline)? For 2, any case where splitting is wrong (e.g. "create X or Y")?
Reply AGREE / CHANGE per item, plus your adjudication review.
