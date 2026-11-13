---
name: dta-chains-need-pipefail
description: A shell chain of dta verbs joined with && and piped through grep/tail keeps going after a failed build unless `set -o pipefail` is on; a failed step also holds the build slot until its shell is stopped.
metadata:
  type: feedback
---

`node bin/dta.mjs product build 2>&1 | grep ... | tail -6 && node bin/dta.mjs gate run ...` runs the
gates and the selftest against the OLD binaries when the build fails: the pipeline's status is
`tail`'s, not the build's. Start every chained verification with `set -o pipefail`.

**Why:** on 2026-09-18 a chain whose product build failed (a private setter) went on to build the
gates and run the selftest on stale exes, reported "40 passed, 2 failed" for verbs the exe did not
have, and its shell then sat on the resource-governed build slot for four hours, so the corrected
chain launched after it could not start compiling until the first shell was stopped.

**How to apply:** `set -o pipefail;` first in any background chain; when a chain's output stays
empty while `tasklist` shows no `cl.exe`, look for an earlier chain still running and stop it
before waiting further. See [[dta-resource-governor]].
