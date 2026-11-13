---
name: Bouncy particles scene status
description: Current state of the basics.usda bouncy liquid glass particles scene and generator script
type: project
---

The main scene file `assets/basics.usda` is a physics simulation of 50 bouncy liquid glass particles dropping into a walled container.

**Key architecture:**
- `scripts/generate_bouncy_cubes.py` is the single source of truth — generates the USDA
- Run: `python scripts/generate_bouncy_cubes.py --count 50 --output assets/basics.usda`
- A single `variantSet "Shape"` on the `Particles` Xform switches ALL particles between Cube, Sphere, and Ellipsoid
- Particle transforms are defined outside the variant; only the shape child prim varies (via `over`)
- Sizes follow Maxwell-Boltzmann distribution (thermal dynamics), mass scales with volume

**Scene structure:**
- `World/PhysicsScene` — gravity 9.81 m/s² down Z
- `World/Particles` — parent Xform with variantSet "Shape", contains 50 Particle_NNN children
- `World/Backdrop` — Floor (visible), FrontWall/LeftWall (visible), BackWall/RightWall/Ceiling (invisible colliders), FloorCollider (thick safety net cube under floor)
- `World/Materials` — 8 liquid glass colors, WhiteMatte, BouncyPhysicsMat (restitution=0.85), BouncyWallMat (restitution=0.7)
- Camera and DomeLight/DistantLight for fallback lighting

**Known issues addressed:**
- Thin mesh walls can let fast particles tunnel through — FloorCollider safety net added
- Particles must not overlap at spawn — stacked vertically with spacing > size
- Time-sampled visibility causes reappearing on timeline loop — use height staggering instead

**Why:** User is building USD physics demos, likely for Omniverse on an L4 GPU. Keep particle counts reasonable (50 is good, 256 was too much).

**How to apply:** When modifying the scene, edit the generator script and re-run rather than hand-editing the USDA. Respect the variant set architecture — shared data outside variants, shape-specific data inside.
