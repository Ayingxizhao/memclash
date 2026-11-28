---
name: project-drift-check-hook
description: Pre-commit hook depends on an external Python drift-check script outside the repo; per-machine paths and the cross-platform hook prototyped here
metadata:
  type: project
---

The repo's `.githooks/pre-commit` invokes a Python drift checker located
(on Windows) at `S:/Dev/dev-tools/project-check.py` (run inside the venv at
`S:/DevTools/venv-drift/`). The script lives **outside this repo** —
it's a shared dev-tool across David's Go projects, in the
`github.com/BeastHome/dev-tools` repo.

On the Mac the same script is at `~/dev/dev-tools/project-check.py`,
with its venv at `~/dev/dev-tools/.venv/` (Unix `bin/` layout, not
`Scripts/`). Since 2026-09-29 dice-roller's hook picks these per OS
(`uname -s` MINGW/MSYS/CYGWIN → Windows paths, anything else →
`~/dev/...`); `DRIFT_SCRIPT` and `DRIFT_VENV` (the venv root) env vars
override either default.

**Why:** keeping the drift checker outside the repo lets it evolve once
and apply to every project that installs the hook, instead of forking
the script per repo.

**Mac status (2026-09-29):** the hook originally didn't run on the Mac
clone, for three independent reasons (now fixed in dice-roller only):

1. `core.hooksPath` is unset. It's per-clone config that `new-app.sh`
   sets only when creating a repo; a clone doesn't inherit it.
2. The hook is committed as mode `100644`. macOS git skips
   non-executable hooks; Windows ignores the bit, so it never surfaced
   there.
3. Even if wired up, the `S:/` script path is missing, and the hook
   misreports that as "Drift detected — commit blocked."

dice-roller's fix: the hook resolves paths per OS, is committed
`100755`, reports a missing checker as such, and `.gitattributes` pins
`.githooks/*` to LF so Windows `core.autocrlf` can't break it.
`core.hooksPath` was set locally on the Mac clone — it isn't in the
repo, so set it on any new clone. The Windows branch was only simulated
on the Mac; verify with `git hook run pre-commit` on Windows before
porting.

`rampartmoon` and `scriptoire` still carry the old Windows-only hook.
David plans to port dice-roller's version to dev-tools later so every
app gets it.

**Where the hook's source lives:** the hook began as a copy of the
`app-base-go` template (dice-roller's now diverges until the port). On the Mac, `~/dev/templates/` is **not** a git
repo — `bootstrap-dev-tree.sh` generates it from `dev-manifest.json` in
dev-tools, and all four `app-base-*` hooks there carry the `S:/` paths.
A portable-hook fix belongs in `dev-manifest.json`, then gets copied
into each app's `.githooks/pre-commit`; editing `~/dev/templates/`
directly won't reach the Windows machine.

**What it checks here:** effectively nothing for dice-roller — both Go
checks skip (flags are parsed by hand in `internal/parse`, so there are
no `flag.X("name")` registrations; there's no `OUTPUT_CONTRACT.md`).
A missed run is low-risk for this repo.

**How to apply:**
- A commit can fail with "Drift detected — commit blocked." or with a
  Python error like `No such file or directory` if the path is missing
  — confirm the script path exists before assuming real drift.
- Don't try to fix drift by editing the hook or bypassing it
  (`--no-verify` is off-limits per [[feedback-commit-style]]); fix the
  source-of-truth that the script is comparing against.
- On a fresh clone or a different machine, both `S:/Dev/dev-tools/` and
  the venv at `S:/DevTools/venv-drift/` need to exist for the hook to
  succeed. If they don't, surface that to David rather than disabling
  the hook silently.
- To run it without committing (either OS): `git hook run pre-commit`.
- Last known successful run: 2026-05-31, commit `6a5fc3d` (the AGENTS/
  CLAUDE/memory bootstrap). Hook printed `No drift detected` then
  `No drift — commit allowed.`
- Last known Mac run: 2026-09-29, via the hook itself on the commit
  that made it cross-platform.
