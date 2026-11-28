---
name: feedback-task-scoped-automation
description: automation.py must only touch objects relevant to the current task; never rebuild unrelated systems on every run
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0915fc8d-24ef-4720-8196-bf8a16aec8a1
  modified: 2026-08-07T20:41:53.849Z
---

automation.py is task-scoped. Each run should ONLY create/update the specific objects needed for the stated task. Never add calls like `stud_framing.build(doc)` or `enclosure.build(doc)` unless stud framing or enclosure is the actual task being done.

**Why:** Re-running automation.py was overwriting Wall_Bath_N (removing its bathroom entry door), demolishing and re-building all exterior stud walls, and rebuilding all subfloor/sheathing sheets — all side effects of including builders that weren't needed for the current task. User explicitly stated: "we should not be building this model from scratch each time — make sure we are only altering objects within context of each prompt."

**How to apply:** Before adding any `build()` call or `_upsert_box` to automation.py, ask: "is this object explicitly part of the stated task?" If no, leave it out entirely — do NOT touch it without direct user confirmation first. The _upsert pattern makes individual object updates idempotent; a full rebuild call (like `remove_group` + rebuild) is destructive and must only appear when that system is the explicit subject of the task. This is a prime directive: no object is altered unless it is named in the prompt or the user has confirmed it should be included.
