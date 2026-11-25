---
name: guard-rm-variables
description:
  "An rm whose path is built from a shell variable takes ${VAR:?}, so an empty variable stops the
  command rather than deleting at the root."
metadata:
  type: feedback
---

Write `rm -f "${SP:?}"/"${n:?}".mov`, never `rm -f $SP/$n.mov`. On 2026-10-15 Claude Code warned
"Dangerous rm operation on possibly-empty variable path" on a fault-run command, and Mike asked
for thoughts; Claude agreed and took the rule.

**Why:** with `SP` empty, `rm -f $SP/$n.mov` deletes `/f1.mov`; with both empty, `/.mov`. A
variable set a line earlier can still be empty when a line is copied into another command.

**How to apply:** every `rm`, `rm -rf` and `find … -delete` whose path holds a variable uses
`${VAR:?}` for each variable, or a literal path. Related: [[never-busy-wait-in-bash]].
