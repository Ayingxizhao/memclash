---
name: describe-runs-not-ids
description: Refer to runs by what they are (their setup), not by wandb run names or ids
metadata:
  type: feedback
---

When talking to the user about runs, name each run by its setup (e.g. "旧版多样的那次", "当前配置（DINO）", "当前配置只换回旧 prompt"), not by wandb run names like northern-paper-439 or ids like y150poff. A run name can be given once in parentheses at most.

**Why:** the user said (2026-10-24) they cannot tell which run is which from the names/ids.

**How to apply:** in every report, comparison table and column header, use descriptive labels; keep run names/ids only in files (ablation_log.md, logs) where they are needed for lookup. Related: [[monitor-report-homogenization]].
