---
name: dta-gate-authoring-lessons
description: s.mutant with an async function never catches (use mutantAsync and await it); String.raw templates cannot hold backticks; heredocs collapse double backslashes and choke on apostrophes
metadata:
  type: feedback
---

- `s.mutant(name, fn)` is synchronous: `fn` must return falsy for the mutant to count as caught. An
  `async` fn returns a Promise (truthy) and is NEVER caught. Use `await s.mutantAsync(...)`.
- Patch scripts written through a bash heredoc: `\\` collapses to `\`. Use `String.raw` templates
  with single backslashes - but a `String.raw` template cannot contain a backtick or `${`, and C++
  such as `L'\\'` cannot survive a heredoc at all. For those, use the Edit tool. Long prose with
  apostrophes belongs in the Write tool, not in a heredoc inside a larger command. See
  [[dta-patching-crlf-files-from-bash]].
- A regex over source text for "does this module start processes" needs `\bspawn\(`: `.exec(` on a
  RegExp matches a bare `exec\(`.
- Working-tree files are CRLF here; strip `\r` before `indexOf('...\n...')`.
- `dta gate run --all` does not build. After a configuration change every gate reads STALE until
  `dta gate build --all` has run.
