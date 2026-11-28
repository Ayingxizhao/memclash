---
name: los-coverage-orientation
description: "gNB boresight currently points into Munich's LOS-dead half; az~60 deg gives ~50% LOS — cheap alternative to tri-sector for a LOS/NLOS mix"
metadata: 
  node_type: memory
  type: project
  originSessionId: a1f3e29e-2309-4a08-ae16-1784ce6b7621
---

The Munich datasets are ~1.4% LOS **because the gNB panel faces the wrong way**, not because the scene lacks LOS. `gnb_azimuth_deg=235` (default in `RTSceneConfig`) points SW into the dense interior — a LOS-dead direction. The UE sampling wedge is tied to the boresight (`sample_positions` draws azimuth in `[gnb_azimuth_deg +/- span/2]`) and the LOS flag is purely geometric (`_los_flags`: first-path delay ~= ||gnb-ue||/c, antenna-pattern-independent), so **rotating the boresight re-samples the UEs into a new city slice and changes LOS% directly.**

Scan finding (`exp/diag_los_coverage.py`, smoke test 6 az x 40 UEs, depth 3 — noisy but unambiguous): a single LOS lobe in the **NE quadrant (~30-90 deg)**. az=60 -> **53% LOS over reached UEs** (72% of outdoor); az=0 -> 32%; az=120 -> 17%; the back half (180/240/300) -> 0%. Second lever = radius: LOS concentrates near the gNB (30-80 m: 100%, 80-150 m: 83%, 150-300 m: 38%), so trimming `sector_r_max` raises LOS% further.

**Why this matters:** re-pointing is a far cheaper route to a LOS/NLOS *mix* than the tri-sector plan ([[viz-debug-tooling-progress]]) — one config number (`gnb_azimuth_deg`, optionally `sector_r_max`), no 3x compute, no Dr.Jit chunking, no localization sector-aliasing, model/eval untouched. 53% is likely too LOS-heavy (NLOS is the valuable regime per [[localization-analysis]]); az~0-30 or 60-with-trimmed-radius dials a balanced mix.

**Tool:** `exp/diag_los_coverage.py` sweeps boresight over an arc (`--az_min/--az_max/--n_az`), traces paths only (no CFR -> cheap), reports reached/indoor/LOS% per azimuth + radius breakdown + polar plot. `python exp/diag_los_coverage.py --az_min 90 --az_max 180 --n_az 10 --n_per 150`.

**CALIBRATION CAVEAT (important):** the path-only scan uses a low `--max_depth` (5) and **under-counts LOS** vs the real depth-10 generation, because deeper tracing + `refraction=True` gives more UEs a near-straight *through-building refracted* path whose delay ~= geometric -> `_los_flags` tags it LOS (the flag can't tell true unobstructed LOS from straight-through refraction; ~60% of these "LOS" are indoor). Same definition the baselines use, so comparisons stay fair, but **calibrate the azimuth with the actual pipeline** (quick 200-UE `rt_gen_run.py` gens), not the scan. Real depth-10 LOS%: az=145->32%, 160->22%, **170->15.2%**, 180->15.5% (scan had predicted ~15% already at 145).

**Generator:** `rt_gen_run.py` — CLI variant of the canonical `rt_localization_data_gen.py` runner (args: `--n_ue --azimuth --span --r_min/--r_max --suffix ...`), same pipeline/outputs; built so comparison sets don't require editing the runner. Output `data/rt_<scene>_<n_tx>ant_<n_ue>ue[_<suffix>]/`.

**DONE — comparison pair built (10k each, identical scene/config, only azimuth differs):**
- `rt_munich_64ant_10000ue` (baseline, az=235): **0.48% LOS** (48/10022)
- `rt_munich_64ant_10000ue_los15` (az=170): **17.8% LOS** (1783/10024), 58% indoor

(Dir named "los15" but realized 17.8% — within the 10-20% target; meta.json is authoritative.) Confirmed well-formed via `inspect_dataset.py --compare`: with abundant LOS now, the textbook contrast shows — LOS UE ~0.5% angular-delay coeffs / peak tap 0 / single clean DoD vs NLOS ~1.5% / peak tap 4 / spread.

**Confound for the A/B:** shoulder-pointing clusters LOS spatially (LOS correlates with a sub-region of XY), so the LOS set's localization gain is partly "LOS marks a place," not purely "LOS helps" — state this in the thesis comparison.

**A/B RESULT (csinet, eta=1/32, 120 ep, test SNR=10 dB; `exp/exp_los_compare.py`, single+joint -> `results/los_compare/results_tasks.json` + `los_compare.png`):**

Decomposed (recon-only / joint) NMSE dB, and (loc-only / joint) loc MAE m:
- baseline 0.5% LOS: NMSE -4.93 / -4.96 ; loc MAE 14.6 / 21.7
- los15 17.8% LOS:  NMSE -6.10 / -6.07 ; loc MAE 12.1 / 18.4

**Finding 1 (LOS helps, task-independent):** more LOS improves BOTH tasks whether trained alone or jointly — recon **-1.1 to -1.2 dB**, loc **-2.5 to -3.3 m**. Real, not a joint-setup artifact. (los15 region is ~7% LARGER in area yet MAE lower -> extent confound works against the result.)

**Finding 2 (NEGATIVE TRANSFER in the joint ISAC model):** joint training HURTS localization by ~7 m vs loc-only (14.6->21.7 baseline, 12.1->18.4 los15; p90 29->50), while recon is ~unchanged (-4.93 vs -4.96). Asymmetric: the shared bottleneck is tuned for recon (recon-only warmup + dominant structure) and loc pays for it. The joint ISAC model trades ~33% loc accuracy for one-codeword convenience. Levers to try: `loc_source="decoder"`, higher `encoded_dim`, detached/larger loc head, re-balanced weighting. See [[localization-analysis]], [[rt-datagen-progress]].

Confound still applies: shoulder-pointing clusters los15 LOS UEs spatially (LOS partly marks a sub-region).

**CPU analyses (stored shards, no GPU; `exp/diag_los_confound.py`, `exp/diag_sparsity_stats.py` -> `results/los_analysis/`):**
- *Confound bounded & defused:* on los15 the LOS flag alone localizes to only 111.8 m MAE (vs 121.4 m global-centroid -> 9.6 m / 7.9% info); the trained model gets ~12 m (loc-only)/~18 m (joint), i.e. ~6-9x better than the spatial prior. So the LOS-region prior explains only ~9% of the model's localization skill; ~91% is genuine channel info. Baseline has no confound (48 LOS). LOS UEs cluster (centroid 114 m from NLOS centroid, spread 89 vs 130 m).
- *Sparsity backs recon claim:* over 1783 LOS / 8241 NLOS UEs, LOS angular-delay k90 (coeffs for 90% energy) mean 42.1 vs NLOS 75.4 = **44% sparser** -> mechanism for the ~1 dB recon gain. Histogram saved.

**100k full-scale pair built** (same gen, `rt_gen_run.py --n_ue 100000`): `rt_munich_64ant_100000ue` (az235, **0.49% LOS** / 490) vs `rt_munich_64ant_100000ue_los15` (az170, **17.0% LOS** / 17033, 59% indoor). A/B runner is scale-switchable: `exp/exp_los_compare.py --scale {10k,100k}` -> `results/los_compare_{scale}/`.

**100k A/B DONE (2026-06-13, csinet eta=1/32 120ep SNR10, seed42 → `results/los_compare_100k/`):**
- recon-only NMSE: baseline -8.68 / los15 **-9.57** dB
- loc-only MAE: baseline 4.5 / los15 **3.9 m** (p50 3.1, p90 7.1) ← NEW BEST localizer
- joint NMSE/MAE: baseline -8.11/6.3 ; los15 -9.05/5.4
- **Finding 1 (LOS helps) HOLDS at 100k all tasks**: los15 wins recon -0.89 dB, loc -0.6 m (single-task).
- **Finding 2 negative transfer is BIDIRECTIONAL at 100k**: joint costs loc **+1.5-1.8 m** (4.5→6.3 base; 3.9→5.4 los15) AND recon **~+0.5 dB** (-8.68→-8.11; -9.57→-9.05) vs single-task. Loc gap ~1.7m (vs ~7m at 10k → data eases it). Staged-training fix being tested (see [[references-and-prior-art]] staged experiment + [[thesis-roadmap]]).
- NOTE: the auto-launch watcher's 800 MiB idle threshold was too low (this box idles ~1.24 GB GPU), so it never fired; launched `joint_staged` (only the missing arm — loc_only/joint_single already valid above at identical seed/config) manually, bg b2tpgnob5.
