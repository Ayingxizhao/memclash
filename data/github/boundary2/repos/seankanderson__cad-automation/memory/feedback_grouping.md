---
name: feedback-grouping
description: Always place new FreeCAD objects into the correct document group immediately after creation; never leave Part::Feature objects at document root
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0915fc8d-24ef-4720-8196-bf8a16aec8a1
  modified: 2026-08-07T02:55:30.990Z
---

Every Part::Feature added to `cabin.FCStd` must be placed in its canonical `App::DocumentObjectGroup` immediately after creation — not in a separate cleanup pass later.

**Why:** The model tree grew to 66 flat objects that were difficult to navigate. The user explicitly asked that grouping be part of the standard workflow going forward, not an afterthought.

**How to apply:**
- Include `_get_or_create_group(doc, name)` helper in every `automation.py` that creates objects.
- Call `group.addObject(obj)` right after `build_*()` returns the feature.
- Use the canonical group names from CLAUDE.md: Foundation, Structure, Walls, Bath, Kitchen, Fixtures.
- If a new category is needed (e.g., Living, Bedroom), create a new group rather than dumping into Fixtures.
- TechDraw FloorPlan objects stay at document root — grouping them breaks TechDraw's internal relationships.

See [[project-cabin-layout]] for full group membership list.

See also [[feedback-subgroups]] — extends this rule to require typed sub-groups within each parent group.
