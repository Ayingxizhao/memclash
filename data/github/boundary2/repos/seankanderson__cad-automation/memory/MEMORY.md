# Memory Index

- [BOM attribute pattern](project_bom_attributes.md) — every Part::Feature needs BomCategory/BomDescription/BomUnit via set_bom_props(); bom.py reads props first then label fallback
- [Web search permission](feedback_web_search.md) — don't run WebSearch without explicit user request
- [Blender rendering deferred](project_blender_rendering.md) — photorealistic renders via Blender addon, revisit later
- [FreeCAD version](user_freecad.md) — user runs FreeCAD 1.1.3 on Windows 11
- [Grouping is mandatory](feedback_grouping.md) — every new Part::Feature must go into its canonical group immediately; never leave objects at document root
- [Cabin design intent & group names](project_cabin_layout.md) — design intent, canonical group hierarchy; cabin.FCStd is source of truth for geometry
- [Door openings are mandatory](feedback_door_openings.md) — every build_partition_wall/build_wall_envelope call with a door MUST include doors=[...]; omitting it silently removes the door from the SVG floor plan
- [Sub-group standard](feedback_subgroups.md) — nested sub-groups required for multi-type systems; use builders/group_utils.py
- [automation.py is the sole entry point](feedback_automation_entrypoint.md) — never tell user to run other .py files; call their build(doc) from automation.py instead
- [Task-scoped automation — prime directive](feedback_task_scoped_automation.md) — no object is altered unless explicitly named in the prompt; never add unrelated build() calls to automation.py without user confirmation
