You write test material for a research experiment. Work read-only (your final message is
saved). Do not open `data/gold/`, `labels_*`, `frozen_*`. No paid API calls.

Background: coding agents keep memory folders of short rules ("Never force-push main.",
"Run the test suite before every commit."). Read `data/runs/natural/rules_blind.json` to see the
style of real rules (wording, length, file names). A clash means: in some situation the rules
talk about, no single action follows all of them; an explicit "you may X" counts as a
permission that must stay usable.

Write 16 groups of exactly three rules about git actions (commit, push, branch, merge, rebase,
tag, PRs), creating/editing/moving/deleting files, or running tasks (tests, build, lint,
deploy):

- 8 CLASH groups: the three rules together clash in a concrete situation, but EVERY PAIR of
  them can be followed together. Typical shapes: a required action needs a prerequisite that
  another rule forbids or limits ("push only after tests pass" + "run tests only when the user
  asks" + "push at the end of every task"); an action split so that two rules forbid all ways
  while a third demands it; a permission ("you may ...") blocked only by two rules together.
  Vary the shapes and topics; do not reuse one template.
- 8 CONTROL groups: look-alikes on the same topics that are compatible as a group (a way out
  exists: a scope that differs, an exception, an allowed alternative), and no pair clashes.

Each rule: one sentence in the style of a real memory rule, with a plausible memory file name
(e.g. `feedback_push_policy.md`, `CLAUDE.md`). Avoid the words "clash", "conflict",
"contradict". Do not make the trick obvious from wording alone.

Output only a JSON object in a ```json block:
{"groups": [{"group": "G1", "kind": "clash"|"control", "rules": [{"file": "...", "rule": "..."},
x3], "situation": "<for clash: the situation where no action follows all three; for control:
the way out>"}]}
Mix clash and control groups in a random order.
