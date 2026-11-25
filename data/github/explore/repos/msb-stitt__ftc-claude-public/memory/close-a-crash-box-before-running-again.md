---
name: close-a-crash-box-before-running-again
description:
  "Close a program's \"quit unexpectedly\" box before starting that program again; Claude may close
  it whenever it likes."
metadata:
  type: feedback
---

When a program crashes and macOS shows its "quit unexpectedly" box, close it, with **Ignore**,
before running the program again. Closing it is Claude's to do at any time.

**Why:** on 2026-10-16 three `melt` runs crashed with exit 139, and the box stayed on the screen
until Mike asked about it. His words: "it's yours to close when you want, but definitely close it
before you start a new melt run."

**How to apply:** after a crash, look at the screen, as [[this-mac-is-claudes]] allows, and close
the box before the next run. The crash report stays in `~/Library/Logs/DiagnosticReports/`.
