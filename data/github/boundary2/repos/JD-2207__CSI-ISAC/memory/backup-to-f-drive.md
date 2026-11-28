---
name: backup-to-f-drive
description: One-command full backup of workspace + Claude state + config to F:\Javier; run backup-to-F.ps1 manually
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f023fd1-28d8-4ac2-9aeb-f1bf02f9ecbc
  modified: 2026-08-12T11:37:22.962Z
---

Disaster-recovery copy lives on `F:\Javier`, refreshed on demand (no scheduled task) by
`CSI\backup-to-F.ps1` — or by double-clicking `F:\Javier\run-backup.cmd`. Restore runbook is
`CSI\RESTORE.md` (copied to `F:\Javier\RESTORE.md` on every run). Set up 2026-08-12; first full
run 22.7 min for 34.07 GB.

Layout: `F:\Javier\workspace\CSI` (whole workspace incl. `.git`, checkpoints, datasets),
`home\.claude` + loose dotfiles + `vscode\`, `env\` (conda specs only — the 5 GB env dir is
deliberately not copied), `_logs\`, `LAST-BACKUP.txt`. Switches: `-DryRun`, `-SkipBulk` (skips
the 31 GB `src\data` + `deepmimo_scenarios`), `-NoStats`.

Non-obvious points worth remembering:
- **Git is NOT a backup here.** `csi_isac` origin is the upstream `jmoraispk/StochasticRTcomparison`,
  HEAD is Nov 2025, and the whole current thesis codebase is uncommitted/untracked. The F: file
  mirror is the authoritative copy of the source. See [[csi-isac-github-repo]].
- `CSI\memory` is a **directory junction** into `.claude\projects\<key>\memory`. Robocopy `/XJ`
  skips it so the 39 notes are stored once (via the `.claude` mirror); `RESTORE.md` documents
  recreating the junction, and renaming the `projects\<key>` folder if the username/path changes.
- Robocopy exit codes 0–7 are success (1 = files copied). The script only treats `>= 8` as failure.
- `/MIR` deletes on the destination, so each section writes to its own dedicated subfolder and the
  script aborts if `-Dest` is a drive root.
- The old hand-made backup (12.6 GB, from the pre-reinstall "Fernando" machine, contained **no
  source files at all**) was moved to `F:\Javier_old\users-fernando` — safe to delete once trusted.

Related: [[machine-migration-2026-08]], [[thesis-project]].
