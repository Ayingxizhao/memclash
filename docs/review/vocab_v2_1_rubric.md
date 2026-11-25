# Vocabulary v2.1 and label conversion rubric (written before any v2.1 translation run)

Date: 2026-11-22. Agreed with Codex (`docs/review/autonomy_consult_3_codex.md`). v2 labels and
all v2 scores are kept unchanged; v2.1 labels are new files.

## What changes in v2.1

1. **Details of an earlier step.** Three new situation fields, each describing the same
   earlier action that `after` names:
   - `after_task`: the task of an earlier `run` (same names as `task`); needs `run` in `after`.
   - `after_path`: the path of an earlier file action (`read`, `create`, `edit`, `move`,
     `delete`, `stage`, `commit`); needs such an action in `after`.
   - `after_ok`: the earlier `run` succeeded (true) or failed (false); needs `run` in `after`.
   In Z3 each action kind has its own earlier-step details (one earlier step per action kind),
   so `after: [edit]` + `after_path: X` means "an earlier edit, of X". `after_branch` moves to
   the same per-action form.
2. **Conjunctions are separate clauses.** A list of paths in one clause still means "any of
   them" (unchanged). "Update A, B and C" or "create X.c and X.h" means each file, so it is
   written as one clause per file. The prompt states this as a definition of the format.

## Converting a v2 label to v2.1 (mechanical; uses only the label and the rule text)

- A `when_unmodeled` condition or a left-out requirement that names an earlier task, an
  earlier file action on a stated path, or success of an earlier task becomes the matching
  `after` / `after_task` / `after_path` / `after_ok` fields. Any remaining part of the
  condition stays in `when_unmodeled`.
- A clause whose path list joins files with "and" (each is required) becomes one clause per
  path; "or" lists stay one clause.
- Nothing else changes. Rules without such conditions or lists keep their v2 label.
- The frozen set gets a separate file `frozen_v2.1_2026-11-22.json`; results on it are
  retrospective (it influenced this change). The original frozen file is not modified.
