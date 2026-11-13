---
name: Edit generator script, not USDA directly
description: User wants changes made in the Python generator script for version control, not hand-editing the USDA
type: feedback
---

When making changes to the particle scene, modify `scripts/generate_bouncy_cubes.py` and re-run it, rather than hand-editing `assets/basics.usda`.

**Why:** User explicitly asked to "write down the python script so we can version control it." The script is the source of truth.

**How to apply:** For any scene changes (count, sizes, materials, physics, container, etc.), update the script constants or functions, then run `python scripts/generate_bouncy_cubes.py --count N --output assets/basics.usda`.
