---
name: canyon-toy-scene
description: Toy simple_street_canyon_with_cars scene for clean RT ray-tracing visualization (complements Munich)
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fde92a1-881e-4167-87d9-a5dbd82553b3
---

Added a **toy** `simple_street_canyon_with_cars` dataset path alongside the 100k Munich set ([[rt-datagen-progress]]), purely to cleanly visualize ray-tracing/simulator features — NOT a replacement for the Munich experiment.

**Scene geometry (probed):** ~186 m (x) × 121 m (y); open E–W road corridor at y≈[−10,10] (cars on it) flanked by two building rows at y≈[±15,±35], heights 21/50/29 m; open cross-street gaps at x≈±25, ±75.

**Implementation (2026-06-09):**
- `sionna_rt_gen.py`: new `sampling="corridor"` mode in `sample_positions` (street strip x×y rect) + `canyon_with_cars_config()` preset. gNB at canyon mouth (−80,0,15), az=0 down the street, downtilt 5°, corridor_x=(−65,80), corridor_y=(−8,8). `meta_dict` now records sampling/corridor_x/corridor_y/specular_reflection.
- **Dr.Jit 2^32 gotcha:** cars + diffuse scattering at depth 8 → ~50k paths/UE, so CFR `(paths×ant×sc)` tensor overflows even at 20 UEs. Preset uses `batch_size=5, cfr_chunk=16` to bound it. ~0.5 s/UE.
- `rt_canyon_data_gen.py`: runner (default 2000 UE), same shard/meta layout as Munich → `scene_maps.py`/`scene_render.py`/`data_feed` work unchanged.
- `scene_render.py`: `cfg_for()` now rebuilds RTSceneConfig from the dataset `meta.json` (scene-agnostic) instead of hardcoding Munich. `scene_maps.py`: draws corridor rectangle (not sector wedge) when sampling=="corridor".

**Character:** corridor is ~all-LOS (open street, gNB sees straight down) — great for distinguishable LOS+reflection ray figures, poor as an NLOS demo. For NLOS, offset gNB behind a building or sample UEs in cross-streets.

**Render tuning (scene_render.py, learned the hard way):**
- Default runner uses **plain `simple_street_canyon`** (no cars) — cars are performance-neutral (path count driven by diffuse scattering on walls × max_depth, NOT cars) and only add visual clutter.
- For distinguishable rays the levers are: **down-canyon camera** (`canyon_axis_camera`, looks along +x from behind gNB; side-on views are occluded by tall facades) + **few UEs + low depth**. Final clean `fig_ray_paths` = `n_ue=2, max_depth=2` (direct + single wall/ground bounces). 3 UE / depth 3 was still a tangle.
- `cfg_for()` rebuilds RTSceneConfig from meta.json so renders are scene-agnostic; cameras derive from bbox.

**Status: DONE.** Dataset `data/rt_simple_street_canyon_64ant_2000ue/` (2000 UE, all LOS/outdoor). Figures in `results/figures/`: scene_aerial, scene_topdown, ray_paths (clean), coverage_map (shows canyon waveguiding). Logs: src/canyon_gen.log, canyon_render*.log.
