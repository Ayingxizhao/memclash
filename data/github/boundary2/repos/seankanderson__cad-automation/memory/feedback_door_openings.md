---
name: feedback-door-openings
description: Every build_partition_wall() or build_wall_envelope() call for a walled door MUST include doors= parameter; omitting it silently produces a solid wall with no door gap in the floor plan
metadata: 
  node_type: memory
  type: feedback
  modified: 2026-08-02T20:22:52.602Z
  originSessionId: 0915fc8d-24ef-4720-8196-bf8a16aec8a1
---

Always pass `doors=[{...}]` when building any wall that has a door opening. Omitting the parameter creates a fully solid wall — the door will never appear in the floor plan or in the model.

**Why:** `floorplan_svg.py` reads door openings deterministically via `Shape.section()` at floor height. If no boolean cut exists in the wall solid, the section returns a single closed rectangle (solid wall) with no gap. Multiple sessions discovered bathroom and CMU-room doors were missing from the SVG because the original `build_partition_wall()` calls omitted `doors=`.

**How to apply:**
- Before writing any `build_partition_wall()` or `build_wall_envelope()` call, ask: does this wall have a door in the cabin plan? If yes, always include `doors=[...]`.
- `build_partition_wall` door format: `{"center_in": <coord>, "width_in": <w>, "height_in": 80.0}`
  - `center_in` is the **Y** coordinate for N-S walls; the **X** coordinate for E-W walls
- `build_wall_envelope` door format: `{"wall": "south"|"north"|"east"|"west", "center_in": <coord>, "width_in": <w>, "height_in": <h>, "sill_in": 0.0}`
  - `center_in` for west/east perimeter walls is **Y**; for south/north walls is **X**
- Windows also go in `doors=` with `"sill_in"` > 0 (e.g. 36") if they need to appear in geometry. Currently windows are hardcoded in `WINDOW_GAPS` in `floorplan_svg.py` — don't use `doors=` for windows unless changing that approach.
- The full parameter table is in CLAUDE.md under "Door openings — MANDATORY".

See [[project-cabin-layout]] for known door positions in the cabin.
