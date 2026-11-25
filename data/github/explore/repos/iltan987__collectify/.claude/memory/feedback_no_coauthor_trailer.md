---
name: No Co-Authored-By trailer in commits
description: User forbids any Co-Authored-By or agent-attribution trailer in git commit messages for this repo
type: feedback
---

Never add a `Co-Authored-By:` line, agent-attribution footer, or any similar trailer
to git commit messages. This overrides the default Claude Code commit workflow that
would otherwise append `Co-Authored-By: Claude ...`.

**Why:** The user stated this explicitly and emphatically ("NEVER"). They want
commits to attribute only the human committing. Treat this as an absolute rule, not
a soft preference.

**How to apply:** When composing any `git commit -m` (or HEREDOC-style message) in
this project, omit the co-author trailer entirely — even when the default tooling
instructions say to include it. When proposing a commit message for user approval,
propose it *without* a co-author line. If existing scripts/templates would inject
one, disable that path and surface it to the user. Also codified in
`.specify/memory/constitution.md` as a NON-NEGOTIABLE workflow rule.
