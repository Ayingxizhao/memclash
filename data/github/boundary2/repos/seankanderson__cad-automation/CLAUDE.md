# CAD Automation — Project Instructions

## Memory
Project memory lives in `memory/` (project root). `MEMORY.md` is the index; individual files hold the content. Always write new memories to this folder.

## Workflow

**Every task follows this sequence — no exceptions:**
1. **Observe** — read `cabin.FCStd` to understand current model state before writing any code
2. **Identify** — state specifically what needs to change and why
3. **Propose** — write the scoped script and describe what it will do in plain language
4. **Confirm** — wait for user approval before running
5. **Execute** — run, then report what changed

- User runs the `run_automation` macro in FreeCAD; it executes `automation.py` inside FreeCAD's Python environment.
- `automation.py` is **task-scoped**: only objects explicitly named in the task are touched. Never add unrelated `build()` calls without confirmation.
- `cabin.FCStd` is the **source of truth**. Builders create objects that are missing; they skip objects that already exist. Never delete-then-recreate on a routine run.
- All public builder APIs take **inches**; builders convert internally using `MM = 25.4`.
- **Skip if exists:** check for the label before building. If found, use `_place_if_homeless()` to ensure correct grouping and move on.
- **Place if homeless:** new objects go into their default group only if not already grouped. Never use `_reparent()`.
- Never call `remove_group()` on any group the user may have organized.

## Document Tree — Groups and sub-groups are mandatory

Every Part::Feature object added to the document **must be placed in the correct group or sub-group**.

Use `builders/group_utils.py` for all grouping — never copy-paste a helper inline:

```python
from builders.group_utils import get_group, get_subgroup

parent = get_group(doc, "2 Floor Structure")
sub    = get_subgroup(doc, parent, "Piers")
sub.addObject(obj)
```

**Rule**: any system with more than one component type gets sub-groups. Flat groups are only acceptable when all members are the same kind of thing (e.g., `Wall_*` interior partitions are all partition walls).

### Numbered build-order groups — USER-DEFINED, AUTHORITATIVE

The user prefixes top-level group labels with a number reflecting construction sequence. **These labels are authoritative. Always read `cabin.FCStd` to confirm current names before hardcoding any group string.**

If `get_group(doc, "some name")` doesn't find an existing group it creates a new orphan — this is how duplicate groups appear. **Never invent a group name; read the model first.**

#### Canonical hierarchy (read from cabin.FCStd 2026-08-08 — update this when user reorganizes)

```
1 Core/               CMU masonry tornado shelter
  CMU Tower           the hollow CMU room solid (SVG/BOM EXCL)
  CMU Footing         spread footing below grade

2 Floor Structure/
  Foundation/           Beams, Piers, Posts live here (sub-group)
    Beams/              Beam_West, Beam_Center, Beam_East
    Piers/              Sonotube_*
    Posts/              Post_*
  Joists/               Joist_*, BandBoard_*
  CMU Ledgers/          CMULedger_*
  Floor Sheathing/      SubfloorSheet_*   ← label is "Floor Sheathing", NOT "Subfloor"

3 Exterior Walls/
  Wall West/            StudWall_W_*
  Wall East/            StudWall_E_*
  Wall South/           StudWall_S_*
  Wall_North/           StudWall_N_*      ← label has underscore (unlike the others)
  Zip Sheathing/        ZIPSheet_*        ← wall ZIP sheathing lives HERE, inside Exterior Walls

4 Roof/
  Trusses/              Truss_*
  Furring/              FurringS_*, FurringN_*
  Sheathing/            SheathNorth, SheathSouth
  Ceiling/              CeilingFurring_*, CeilingPlanks

5 Interior/             top-level parent for all interior fit-out
  Walls/                Wall_*  (all interior partition walls)
  Bath fixtures/        Bath_*
  Kitchen fixtures/     Kitchen_*
```

Not yet in a numbered group: TechDraw FloorPlan objects (leave at root), CoreBlockRoom, CMUFooting, GradePlane.

**When the user renames or renumbers a group:** grep every Python file for the old string and update all `get_group()` / `get_subgroup()` calls. Ask the user for the new name rather than guessing.

New groups or sub-groups — **ask the user what name/number to use** rather than inventing one.

## Wall conventions
- Interior partitions: 2×4 nominal (3.5" thick) via `build_partition_wall`
- Perimeter: 2×6 (5.5" thick) via `build_wall_envelope`
- Corner framing: one wall laps through the other's thickness
- For N-S walls: door `center_in` is Y coordinate; for E-W walls: X coordinate

### Door openings — MANDATORY
**Every `build_partition_wall()` or `build_wall_envelope()` call for a wall with a door MUST include a `doors=` parameter.** `floorplan_svg.py` reads door openings directly from the model via `Shape.section()`. A wall built without `doors=` will appear as a solid bar in the floor plan — no gap, no arc.

**`build_partition_wall` doors:**
```python
build_partition_wall(doc, "Wall_Bath_W",
    x1, y1, x2, y2, height_in=96, z_base_in=36.0,
    doors=[{"center_in": 72.0,   # Y coord for N-S wall; X coord for E-W wall
             "width_in":  32.0,
             "height_in": 80.0,   # height_in optional (default 80"), sill_in optional (default 0)
             "sill_in":   0.0}])
```

**`build_wall_envelope` doors:**
```python
build_wall_envelope(doc, "PerimeterWalls", ...,
    doors=[{"wall":       "south",   # 'west'|'east'|'south'|'north'
             "center_in": 192.0,     # X coord for south/north; Y coord for west/east
             "width_in":  36.0,
             "height_in": 80.0,
             "sill_in":   0.0}])     # 0 = door (at floor); >0 = window
```

**`center_in` axis rule** — measured along the wall *face*, not its thickness:
| Wall orientation | Long axis | `center_in` is… |
|---|---|---|
| N-S partition wall | Y | Y coordinate of door centre |
| E-W partition wall | X | X coordinate of door centre |
| Perimeter west / east | Y | Y coordinate |
| Perimeter south / north | X | X coordinate |

## Cabin reference dimensions
- Footprint: 384" E-W × 288" N-S (32' × 24')
- Floor height (FLOOR_HT): **36"** above grade (standard; site-adjustable by builders)
  - Joist top / subfloor bottom
  - Joist bottom / beam top: 24.75"  (= FLOOR_HT − JOIST_D 11.25")
  - Plate / truss bearing (z_plate_in): 132"  (= FLOOR_HT + WALL_H)
- Wall height (WALL_H): 96" above floor
- CMU core: x = 162"–222", y = 0"–96", z = −42"–+132"
  - CMU door sill: FLOOR_HT + 1.5" = 37.5" above grade = 79.5" above CMU base
  - Door 7 ft (84") tall; top at z = 121.5"; sill is 85.5" above pad bottom (≥ 7 ft ✓)
  - Center LVL beam pocketed 6" into CMU north wall (y_start = 90")
  - CMU is tornado shelter with bonding beams; beam pocket in north wall
- North perimeter interior: y = 282.5"
- East perimeter interior: x = 378.5"
- West perimeter interior: x = 5.5"
- South perimeter interior: y = 5.5"
