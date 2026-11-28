---
name: feedback-subgroups
description: Sub-groups within groups are mandatory when a system has multiple component types — flat groups only for single-type collections
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0915fc8d-24ef-4720-8196-bf8a16aec8a1
  modified: 2026-08-07T02:55:20.216Z
---

Every major system with multiple component types must use nested sub-groups, not a flat group. This lets the user show/hide component types independently in the FreeCAD model tree.

**Why:** User explicitly requested after finding past automation created duplicate and flat groups that were hard to manage.

**How to apply:** Use `builders/group_utils.py` for all grouping. Call `get_group()` for the top-level parent and `get_subgroup()` for each component type within it. Never place objects of different types directly in the same flat parent group. Flat groups are only acceptable when all members are the same kind of thing (e.g., Wall_* interior partitions are all partition walls, ZIPSheet_* are all sheathing panels).

```python
from builders.group_utils import get_group, get_subgroup, remove_group
parent = get_group(doc, "Floor Structure")
sub    = get_subgroup(doc, parent, "Piers")
sub.addObject(obj)
```

See [[feedback-grouping]] for the original grouping-is-mandatory rule. This extends it to require sub-groups.
