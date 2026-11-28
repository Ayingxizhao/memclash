---
name: project-cabin-layout
description: Design intent, group names, and builder constants for the 32x24 cabin — NOT a geometry record; cabin.FCStd is source of truth
metadata:
  node_type: memory
  type: project
  originSessionId: 0915fc8d-24ef-4720-8196-bf8a16aec8a1
  modified: 2026-08-07T00:00:00.000Z
---

**Source of truth: `cabin.FCStd`.** Do not treat coordinates here as authoritative — read the model or the builder scripts instead.

## Design intent (non-derivable)

- Cabin is 32'×24' elevated floor, tornado shelter CMU core
- FLOOR_HT = 36" above grade (standard; builders can adjust per site)
- CMU door sill = FLOOR_HT + 1.5" — must be ≥ 7 ft above pad bottom (−48"); currently 85.5" = 7'1.5" ✓
- Center LVL beam pocketed 6" into CMU north wall (tornado shelter design)
- Kitchen zone is **open plan** — no north partition wall on the kitchen side
- Interior partitions: 2×4 (3.5"); perimeter: 2×6 (5.5")

## Canonical group hierarchy

| Group | Sub-group | What belongs there |
|---|---|---|
| `Floor Structure` | `Grade` | GradePlane |
| `Floor Structure` | `Piers` | Pier_*, Sonotube_* |
| `Floor Structure` | `Posts` | Post_* |
| `Floor Structure` | `Beams` | Beam_* |
| `Floor Structure` | `Joists` | Joist_*, BandBoard_* |
| `Floor Structure` | `CMU Ledgers` | CMULedger_*, CoreLedger_* |
| `Floor Structure` | `Subfloor` | SubfloorDeck, SubfloorSheet_* |
| `Exterior Walls` | `Wall West/East/South/North` | Stud framing per wall |
| `Wall Sheathing` | *(flat)* | ZIPSheet_* |
| `Roof` | `Trusses / Furring / Sheathing` | Truss_*, FurringS/N_*, SheathSouth/North |
| `Structure` | *(flat)* | PerimeterWalls, CoreBlockRoom |
| `Foundation` | *(flat)* | CMUFooting |
| `Walls` | *(flat)* | All interior partition walls (Wall_*) |
| `Ceiling` | *(flat)* | CeilingFurring_*, CeilingPlanks |
| `Bath` | *(flat)* | Bath_* fixtures |
| `Kitchen` | *(flat)* | Kitchen cabinets, counters, appliances |
| `Fixtures` | *(flat)* | Catch-all for unmatched Part::Feature objects |
| *(root)* | — | TechDraw FloorPlan objects — do NOT group |

**Why grouping:** User requested clean tree on 2026-08-02 after model grew to 66 flat objects. See [[feedback-grouping]].
