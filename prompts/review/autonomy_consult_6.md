You are Codex, consulting as an equal partner. Read-only (no edits; final message saved). Do not
open `data/gold/`, files named `labels_*`, or any `frozen_*` label file. No paid APIs.

Read `docs/review/experiment_log.md` E8 and `prompts/rules/requirements.md` (step 1).

Proposed correction of our own step-1 category definitions (general, not about one rule):
- `translate`: "about git, files, or running a task, including a rule that limits when such an
  action may happen (e.g. only with the user's approval, only after tests pass)".
- `outside_vocabulary`: "concrete, but neither an action on git, files or tasks nor a limit
  on one (code style, which tool to use, what to say to the user)".
Reason: step 1 does not see the vocabulary, and the old wording ("what to tell the user")
made approval-before-push rules look outside, although `user_confirmed` is a field.

Questions (under 300 words): is this general and correct? Anything else in requirements.md
that conflicts with the vocabulary the same way? After this, do we refresh the
preregistration fingerprint and run the frozen evaluation once (no more dev iterations), or
first re-check the pilot once (~$0.07)? AGREE / CHANGE.
