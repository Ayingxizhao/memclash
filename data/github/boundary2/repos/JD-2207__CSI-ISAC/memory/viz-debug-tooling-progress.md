---
name: viz-debug-tooling-progress
description: "2026-06-12 session — didactic/debug instrumentation, scene figures, Jupyter interactive, tri-sector plan"
metadata: 
  node_type: memory
  type: project
  originSessionId: a1f3e29e-2309-4a08-ae16-1784ce6b7621
---

Session of **2026-06-12** added data-gen debug/teaching instrumentation, scene figures, and an interactive Jupyter path; plus a designed-but-unbuilt tri-sector plan. See [[rt-datagen-progress]], [[scene-viz-workflow]], [[canyon-toy-scene]].

## Didactic / debugging (data-gen)
- `sionna_rt_gen.py`: new `RTSceneConfig.didactic` flag + `_didactic_dump()` — prints ONE fully worked UE (geometry, RT path count, first-path vs geometric delay, [1] freq CFR, [2] delay-domain H with n_taps energy-truncation %, [3] 8x8 UPA array response, total power). One-shot guard; wired into `generate_batch`; enabled in the runner.
- `inspect_dataset.py`: NEW offline counterpart (numpy only, no Sionna/GPU) — loads stored shards + meta, prints dataset summary and the [2]/[3]/geometry sections for a chosen UE (`--ue first|random|N`). Also renders `inspect_ue{i}_fft.png` (`fft_images()`, lazy matplotlib): [A] angular-delay domain `|DFT_ant(H)|` = the sparse CsiNet+ compression image (stored H is already delay-domain, so this applies only the remaining spatial DFT over the 64 ports — the "2D FFT" framing covers gen-time IFFT + this), prints sparsity (e.g. ~1% of coeffs hold 90% energy); [B] az-el beamspace = true 2D FFT of the 8x8 UPA at the peak tap → dominant DoD (directional-cosine axes, lambda/2 assumed). Flags `--no_fig/--show/--fig_dir`.
- Bug fixed (both): `suppress=True` was rounding the ~1e-6 absolute gains to "0.000" (they're tiny because `normalize_cfr=False` keeps path loss). Now `suppress=False` (sci notation) + a `peak |H|` line + total power shown in dB, e.g. `2.5e-10 (linear) = -96.0 dB [absolute path gain]`. Also made all printed strings ASCII (Windows cp1252 console).
- Note for thesis: per-tap energy peaks at tap ~3, not 0, despite `normalize_delays=True` (leading taps = IFFT sidelobes/near multipath) — revisit if strict first-tap alignment wanted.

## Scene figures (`scene_render.py`)
- `preview_scene()` (bare scene + gNB + candidate UEs, no dataset needed) and `fig_overview` wrapper.
- `fig_los_closeup()`: searches a near-gNB ring for a TRUE specular LOS UE at `target_dist` (~70 m good), shrinks device markers via `display_radius`, `closeup_camera` side-3/4 framing. Falls back to diffuse multipath if no LOS.
- `sector_map()`/`fig_sector_map()`: top-down building-occupancy raster (cheap roof-above test) + gNB + oriented sector wedge + boresight + dashed full-360 ring + indoor/outdoor candidate sample. Takes a `cfg` directly so hypothetical configs (e.g. 360 deg) can be previewed pre-generation.
- Hardened `fig_ray_paths` with specular->diffuse fallback + empty-paths guard.
- `main` figures: `sector,overview,los,aerial,paths,coverage`. Runner `rt_localization_data_gen.py` got a `MAKE_PREVIEW` cell + `didactic=True`.
- KEY findings: Munich is ~98.6% NLOS; true specular LOS exists only in the open plaza near the gNB base (distant LOS-flagged UEs only get a near-geometric diffuse path). The `tr38901` panel is directional (~25-30 dB front/back) so a single panel can't cover 360 deg.

## Interactive Jupyter
- `scene_explore.ipynb`: place a UE (manual or `find_los(target_dist)`), trace, view with `scene.preview(paths=..., show_devices=True)` (rotate/zoom/pan).
- Blank-preview cause = running in VS Code (doesn't load pythreejs widget JS). Fix: installed `jupyterlab==4.5.8` into `venv` (added to `venv.txt`), registered the `venv` kernel; verified `jupyter-threejs`/ipywidgets labextensions enabled. Run `jupyter lab` from `src/` in the browser. See [[scene-viz-workflow]].

## Tri-sector (3-sector) coverage — DESIGNED, NOT BUILT
User is considering 360 deg coverage via **3 co-located panels 120 deg apart** (validated: one PathSolver call -> CFR `(B,1,3,64,1,n_sub)`; per-UE serving sector = argmax power; best-vs-worst sector ~25-30 dB). Model/beamforming eval UNCHANGED — each UE still served by one 64-port panel, stored H stays `(N,64,n_taps)`; only data-gen + a new `sector_id` label change.
- Plan: add `n_sectors=1` config (default = current behavior); `build_scene` loops `n_sectors` Transmitters co-located, each `look_at` its azimuth; `generate_batch` picks serving sector + stores `sector_id`; full-360 ring UE sampling; multi-wedge `sector_map`.
- Issues: (1) ~3x RT time + 3x CFR tensor -> must cut `batch_size`/`cfr_chunk` under Dr.Jit 2^32 (a 100k regen is much longer); (2) `sector_id` ~ coarse 120 deg bearing -> keep as METADATA not model input (localization-leakage); (3) sector-boundary power cusps (+/-60 deg); (4) per-sector LOS/NLOS imbalance (plaza in one sector); (5) dataset versioning (old shards single-panel, no sector_id); (6) co-located vs ~1-2 m offset panels (minor). Offered to implement behind `n_sectors`, validate on 200-UE first.
