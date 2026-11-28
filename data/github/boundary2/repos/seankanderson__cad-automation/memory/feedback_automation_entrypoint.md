---
name: feedback-automation-entrypoint
description: automation.py is the sole FreeCAD entry point — never tell the user to run other scripts directly
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0915fc8d-24ef-4720-8196-bf8a16aec8a1
  modified: 2026-08-07T03:23:03.045Z
---

`automation.py` is the only script the user runs from FreeCAD (via the `run_automation` macro). Other modules (`stud_framing.py`, `enclosure.py`, etc.) expose a `build(doc)` function that must be imported and called from `automation.py`.

**Why:** The FreeCAD macro is wired to automation.py only. Telling the user to "run stud_framing.py" or "re-run enclosure.py" separately is meaningless.

**How to apply:** When a task requires rebuilding walls, subfloor, roof, etc., write automation.py to import and call the relevant `build(doc)` functions in the right order. Never end a response by saying "re-run X.py" — instead, either include those calls in the current automation.py or offer to write the next automation.py that does so.
