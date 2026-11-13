---
name: dta-patching-crlf-files-from-bash
description: multi-line source patches must be Node scripts written to a file, never bash heredocs or sed — CRLF and backslash escapes both get mangled
metadata:
  type: feedback
---

The working tree is CRLF (autocrlf) and much of the C++/JS being patched contains `\\`, `\n`
and backticks. Scripted multi-line edits made through the Bash tool failed three separate ways
on 2026-09-17: an LF needle never matches a CRLF file; a bash heredoc collapses `\\n` into a real
newline (it produced broken C++ string literals inside a gate); and `sed`/`node -e` with nested
shell quoting silently matched only some of the intended lines, leaving a gate half-edited and
FAILING.

**Why:** each failure was silent until a build or a gate run caught it, and one left a gate
source in a mixed state.

**How to apply:** write a `.cjs` patch script with the Write tool (no shell quoting layer), use
`String.raw` for C++ text, normalise `\r\n` -> `\n` before matching and restore CRLF on write, and
make every replacement assert the needle occurs EXACTLY once (`s.split(a).length !== 2` -> throw).
One-line, escape-free substitutions (a mutant flipping a constant) are fine with `sed`, followed
by a `grep -c` proving the substitution landed, and a restore from a backup copy afterwards.
