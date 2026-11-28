---
name: record-experiments-always
description: "Standing user instruction: always record new experiments + conclusions to memory when they're done"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 25f850d3-7142-4fb9-948f-c500c3c3dafc
---

User instruction (2026-06-21, stated explicitly): **always record to memory when a new experiment
is run and a conclusion is drawn** — don't wait to be asked each time.

**Why:** this is a long-running thesis with many experiments across sessions; the memory dir is the
durable record the user relies on to keep the thesis narrative + results straight. Unrecorded results
get lost between context windows.

**How to apply:** after any experiment that lands a result/conclusion, update the relevant project
memory (e.g. [[matched-overhead-classical-vs-dl]], [[thesis-roadmap]], [[localization-analysis]]) with
the numbers + the conclusion + the artifact path (results/... + the exp script), and add/refresh the
MEMORY.md index line. Proactively, not only on request. Still verify file:line claims before relying
on point-in-time notes.
