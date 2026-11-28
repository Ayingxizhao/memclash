---
name: project-bom-attributes
description: Every Part::Feature must have BOM properties set via set_bom_props(); bom.py reads properties first then falls back to label parsing
metadata: 
  node_type: memory
  type: project
  originSessionId: 0915fc8d-24ef-4720-8196-bf8a16aec8a1
  modified: 2026-08-05T13:27:08.677Z
---

## BOM Property Convention

Every `Part::Feature` created in any builder **must** have three custom properties set immediately after creation using `builders/bom_props.py`:

```python
from builders.bom_props import set_bom_props
obj = _box(doc, grp, label, ...)
set_bom_props(obj, "Lumber - KD", "2×6 KD", "LF")
```

**Why:** `bom.py` (the BOM extractor macro) reads `BomCategory`, `BomDescription`, `BomUnit` from the object directly. Without these, it falls back to label-pattern matching which is fragile. Builders that set properties produce accurate, self-describing objects.

**How to apply:** Call `set_bom_props` for every object a builder creates. If an object should be excluded from BOM (composite solid used for SVG floor plan), set `BomCategory = "EXCL"`.

## Valid BomCategory values

| BomCategory   | BomUnit  | What it covers                              |
|--------------|----------|---------------------------------------------|
| `LVL Beam`   | `LF`     | Engineered lumber (LVL, PSL)                |
| `Lumber - PT`| `LF`     | Pressure-treated dimensional lumber         |
| `Lumber - KD`| `LF`     | Kiln-dried dimensional lumber               |
| `Concrete`   | `EA`     | Sonotubes, cast-in-place                    |
| `Sheet Goods`| `SQFT`   | Plywood, OSB, ZIP sheathing, T&G panels     |
| `Roof`       | `LF`/`EA`| Trusses (EA), purlins/furring (LF)          |
| `Ceiling`    | `LF`/`SQFT`| Furring strips (LF), T&G planks (SQFT)   |
| `Fixture`    | `EA`     | Bath/kitchen appliances and fixtures        |
| `EXCL`       | n/a      | Composite solids for floor plan SVG only    |

## BomUnit measurement rules in bom.py

- `LF` → longest BoundBox dimension / 12 → sum linear feet
- `SQFT` → mid × long BoundBox dims → sum sq in → convert to sheet equivalents
- `EA` → count pieces, no dimension aggregation

## Builders already updated (as of 2026-08-05)

- `builders/stud_wall_builder.py` — all stud wall members tagged
- `enclosure.py` — SubfloorSheet_* and ZIPSheet_* tagged

## Builders still using label-fallback only

- `automation.py` (floor structure, sonotubes, posts, beams) — still works via label, should add props eventually
- `builders/roof_builder.py` (Truss_*, Furring*, CeilingFurring_*, CeilingPlanks) — label rules in bom.py cover these

## Running the BOM

```
freecadcmd.exe run_bom.py   # headless
# or: open bom.py as a macro inside FreeCAD
```

Output: `cabin_bom_YYYY-MM-DD.xlsx` in project root.
Tabs: BOM Summary | Detail | Unclassified

## Current BOM output (baseline 2026-08-05)

| Category      | Description                        | Pcs | LF    | Sheets |
|---------------|------------------------------------|-----|-------|--------|
| LVL Beam      | 3-ply 1.75"×14" LVL Side Beam     | 2   | 48.0  |        |
| LVL Beam      | 2-ply 1.75"×11-7/8" LVL Ctr Beam  | 1   | 16.0  |        |
| Lumber - PT   | 2×12 PT                            | 31  | 678.5 |        |
| Lumber - PT   | 6×6 PT Post                        | 7   | 6.4   |        |
| Lumber - KD   | 2×10 Header                        | 5   | 17.7  |        |
| Lumber - KD   | 2×6 KD Plate/Sill                  | 15  | 339.2 |        |
| Lumber - KD   | 2×6 KD Stud/King/Jack/Cripple      | 108 | 737.2 |        |
| Concrete      | 12" dia sonotube                   | 7   |       |        |
| Sheet Goods   | 5/8" T&G Plywood (Subfloor)        | 25  |       | 24.00  |
| Sheet Goods   | 7/16" ZIP Sheathing                | 28  |       | 26.75  |
| Roof          | Engineered Roof Truss              | 5   |       |        |
| Roof          | 1×4 Roof Purlin / Furring          | 16  | 576.0 |        |
| Ceiling       | 3"×1.5" Ceiling Furring            | 13  | 404.1 |        |
| Ceiling       | 3/4" T&G Pine Ceiling              | 1   |       | 22.42  |
| Fixture       | Bath fixtures (7 items)            | 7   |       |        |
| Fixture       | Kitchen (13 items)                 | 13  |       |        |

See [[feedback-grouping]] — every object must also be in its canonical group.
