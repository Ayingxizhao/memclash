---
name: deepmimo-cross-simulator
description: "Cross-simulator validation — multitask CSI+loc pipeline run from scratch on a DeepMIMO (Remcom) scene, all three deliverables work; closes single-ray-tracer caveat"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0c7217bd-688e-4a9b-b67b-f2e6adf6a317
---

Ran the full multitask CSI-feedback + localization pipeline **from scratch on DeepMIMO**
(Remcom Wireless InSite ray tracing — a public benchmark), independent of Sionna RT. This
is a cross-SIMULATOR result complementing the cross-SCENE [[cross-scene-generalization]]
Munich→Paris finding, and closes the single-ray-tracer scope caveat in
[[simulation-audit-caveats]].

**TWO scenes done at 10k** (same 8×8 UPA / 64-port / 64-tap / 1024-sub contract as the Sionna
shards — consumed by the UNCHANGED training/eval pipeline). All: joint, encoded_dim=256, 120 ep
(~7.5 min ea), csinet, uniform SNR, feedback 10 dB.

| scene | size | LOS | recon NMSE | loc MAE / p50 / p90 | beam SE retained |
|-------|------|-----|-----------|---------------------|------------------|
| `asu_campus_3p5` | 410×320 m | 30.3% | **−9.93 dB** | 18.7 / **10.7** / 41.2 m | **96.2%** (+2.71 dB @0dB fb) |
| `city_0_newyork_3p5` | 290×108 m | 26.6% | **−9.92 dB** | 8.5 / **5.4** / 15.7 m | **96.0%** |

Datasets `data/dm_{asu_campus_3p5,city_0_newyork_3p5}_64ant_10000ue`. Ckpts
`checkpoint/dm_{asu_campus,nyc}_joint.pt`. Logs `src/data/dm_*{,_nyc}.log`.

**Reading:** recon is rock-steady ~−9.9 dB across both DeepMIMO scenes (BETTER than Munich
joint-100k's −7.79 — asu/NYC channels are sparser/more-LOS). Loc tracks SCENE SIZE/density,
not just LOS: NYC's small dense canyon (290×108 m) → p50 5.4 m vs campus's larger 410×320 m →
10.7 m. Both pipelines reproduce Munich's gain-vs-feedback-SNR SHAPE (DL helps most at low fb
SNR, crosses ~0 by ~12 dB).

**Scale caveat (important for fair comparison):** these are 10k. Munich's loc curve
[[localization-analysis]] is 2k=45/28, **10k=18.8/10.6**, 40k=6.3/4.1, 100k=4.6/3.1 (MAE/p50,
loc-only). So DeepMIMO-10k ≈ **Munich-10k**, NOT Munich-100k — the campus 10.7 m matches
Munich-10k's 10.6 m almost exactly (and NYC beats it on the smaller scene). Headline-matched
(80k, asu has only ~85k active) NOT yet run — user chose breadth (2nd scene) over depth.

**Code (new, all Sionna-free / CPU for data-gen → no OptiX/driver constraint):**
`src/deepmimo_data_gen.py` (DeepMIMOConfig + generate_dataset, scene-parametrized — change
`scenario` to add scenes), `src/deepmimo_localization_data_gen.py` (runner), `src/exp/dm_smoke_test.py`.
deepmimo **4.0.3** installed in `venv`.

**Two non-obvious gotchas solved (reusable):**
1. DeepMIMO's `dm.download` prints a "✓" that crashes on Windows cp1252 stdout — run any
   deepmimo entrypoint with `PYTHONUTF8=1`.
2. DeepMIMO synthesizes the CFR from **ABSOLUTE** path delays; in a macro scene the bulk
   propagation delay (~1.55 µs at ~465 m) exceeds the OFDM symbol duration → **every path
   clips to ZERO** (`||H||_F=0`). Fix = subtract each UE's first-path delay from the `delay`
   ray matrix IN PLACE before `compute_channels` (`_anchor_delays_inplace`), the DeepMIMO
   analogue of Sionna's `normalize_delays=True`. A post-hoc CFR phase ramp is too late.
3. v4.0.3 API: `subset`/`get_active_idxs`/`get_uniform_idxs` are gone → use
   `ds.get_idxs("active"|"uniform",...)` + `ds.trim(idxs=...)`.
4. Multi-BS scenarios (e.g. `city_0_newyork_3p5` has 3 BS) load as a `MacroDataset`
   (indexable, `n_ue` is a per-BS array not a scalar) — `isinstance(...,list)` misses it;
   `load_scenario` indexes down to BS 0 via `while not np.isscalar(ds.n_ue): ds = ds[0]`.
   Runner takes an optional CLI arg: `python deepmimo_localization_data_gen.py <scenario> [n_ue]`.

**MULTI-gNB CROSS-SIMULATOR (2026-06-27, NEGATIVE-with-explanation — genuinely informative):**
NYC `city_0_newyork_3p5` ships **3 BS** in one scene, so a cooperative-loc A/B needs NO new ray
tracing. Built multi-gNB DeepMIMO support: `deepmimo_data_gen.generate_multignb_dataset` /
`meta_dict_multignb` (emit H (M,G,64,64) + los (M,G), per-BS delay-anchored independently) +
runner `deepmimo_multignb_data_gen.py`. Dataset `data/dm_city_0_newyork_3p5_64ant_10000ue_3gnb`
(reach gNB0=100%/gNB1=71%/gNB2=93%). Ran `exp/exp_multignb.py --max_gnb 3` (joint, geographic
split, identical protocol to Munich) → `results/multignb/dm_nyc/multignb_ab_123.json`:

| arm | MAE | p50 | p90 | NMSE |
|-----|-----|-----|-----|------|
| 1gNB | 18.0 | 14.1 | 33.3 | −12.2 dB |
| 2gNB | 21.7 | 20.5 | 34.7 | −12.3 dB |
| 3gNB | 18.3 | 16.8 | 34.0 | −13.2 dB |

**Loc is FLAT/worse with more anchors — opposite of Munich** (1→3 gNB p90 64.9→25.2 @10k). Recon
NMSE DOES improve monotonically (−12.2→−13.2 dB: more CSI = better denoising, geometry-free).
**Cause = anchor GEOMETRY:** the 3 NYC BS are CLUSTERED near scene centre (triangle area only
**1030 m²**, separations 34–87 m, all low 6 m street-level) inside a 290×108 m (~31000 m²) scene →
for far UEs all 3 anchors share nearly one bearing → poor GDOP / no triangulation diversity.
Munich's POSITIVE result used anchors deliberately spread to SPAN the area (the "triangle regen"
lifting anchor-triangle area ~0→35366 m², [[classical-loc-baseline]]). **Finding: the multi-gNB loc
lever is GEOMETRY-CONTINGENT and does NOT transfer automatically — it needs anchors spanning the
scene, not as-shipped clustered small cells.** Reinforces (not contradicts) the Munich triangle
finding. (Geographic-split single-gNB NYC = p50 14.1 vs random-split 5.4 = the honest-split gap,
[[identifiability-diagnostic]].)

**BS-GEOMETRY SCOUT (2026-06-27, `exp/dm_scout_bs.py` → `results/dm_bs_scout.json`):** downloaded
all 20 `city_*_3p5` (each has exactly 3 BS) + measured anchor-triangle area vs scene area
(span_ratio) + centroid-offset. Ranked best→worst multi-gNB GDOP. **NYC city_0 sits near the
BOTTOM** (span 0.033, cent_off 0.50 = clustered centre) → confirms the negative result was a
geometry artifact. **Best spanning-anchor candidates:** city_16_sanfrancisco (tri 7047 m², span
0.170, cent_off 0.95 = anchors ~1 scene-radius out), city_12_fortworth (5875, 0.155),
city_3_houston (4359, span 0.142, diag_frac 0.68 = biggest BS-sep/scene). Worst: city_8_dallas
(202 m², span 0.005), city_18_denver (478). **Next test:** run the 1/2/3-gNB A/B on
city_16_sanfrancisco_3p5 — if loc gain reappears, confirms multi-gNB lever returns with good GDOP.
(Even 0.170 is modest vs an engineered spanning triangle, so expect a moderate, not Munich-scale, gain.)

**GDOP TEST → HYPOTHESIS REFUTED (2026-06-27).** Ran the same 1/2/3-gNB A/B on
`city_16_sanfrancisco_3p5` — the BEST-spread DeepMIMO scene (span 0.170, 5× NYC; per-anchor LOS
15/58/61%), dataset `data/dm_city_16_sanfrancisco_3p5_64ant_10000ue_3gnb`,
`results/multignb/dm_sf/multignb_ab_123.json`. **Multi-gNB STILL gives no loc gain** — best-VAL
loc MAE 1/2/3gNB = 11.9 / 12.5 / 11.7 m (p90 22.3 / 27.3 / 21.5) = FLAT. (Test deltas noisier:
small geographic held-out set ~300–500 UEs; a 1gNB test-recon −2.9 dB outlier is held-out-cell
variance, val NMSE was −10.0 dB — does not affect the loc read.) So better anchor GEOMETRY did
NOT recover the gain → **anchor spread/GDOP is NOT the explanation.**

**Revised synthesis (the real reason Munich's multi-gNB gain doesn't transfer):** Munich's large
1→3gNB gain came from disambiguating a PATHOLOGICALLY ambiguous single-gNB channel (0.5% LOS, deep
NLOS, 54% indoor → single-gNB 3gnb-dataset p50 ~23 m). DeepMIMO urban scenes have far MORE LOS
(15–61%/anchor) so the PRIMARY gNB alone already resolves position (val p50 ~9 m) — little
ambiguity left for extra anchors to remove → diminishing returns ≈ 0. Multi-gNB helps most exactly
where single-gNB is WORST (high channel ambiguity, [[identifiability-diagnostic]]); DeepMIMO's
single-gNB isn't ambiguous enough to benefit. Cross-simulator lesson: the multi-gNB localization
lever is CONTINGENT ON SINGLE-ANCHOR AMBIGUITY, not on anchor count or GDOP per se. Recon NMSE
still improves with anchors in all cases (more CSI = better denoising, ambiguity-independent).
Tool `exp/dm_scout_bs.py` + `results/dm_bs_scout.json` rank all 20 cities by anchor spread.

**CLASSICAL BASELINE ON DEEPMIMO (2026-06-27).** Made `exp/classical_loc_baseline.py` run on
DeepMIMO via 3 additions: (1) multi-gNB adapter now emits a `toa` shard key (per-anchor abs
first-path delay = the τ_min already computed in `_anchor_delays_inplace`); verified c·toa = true
gNB→UE dist to 0.1 m on LOS. (2) `meta_dict_multignb` fills gNB orientation from DeepMIMO `tx_ori`
(=[0,0,0] → az 0 / downtilt 0). (3) **AoA manifold convention fix** — DeepMIMO's [8,8] UPA maps
its dims to SWAPPED axes vs Sionna (row→vertical z, col→horizontal y, y-handedness flip); brute-
forced against LOS geometry → LOS AoA p50 0.7° (matches Sionna manifold). Added `convention=
"deepmimo"` to `upa_elem_positions`, auto-selected via `meta["source"]`. Regenerated NYC+SF 3-BS
datasets with toa. Results `results/multignb/{10k,dm_sf}/classical_baseline.json`.

**Findings (3gNB, geographic split = same test as the learned A/B):**
- **ToA/Multi-RTT classical WORKS** (angle-free, uses exact toa): NYC perfect-timing 3gNB ToA-trilat
  LOS p50 **4.4 m** / Multi-RTT LOS p50 2.3 m; all-UE p50 17 m. Degrades in NLOS (first path =
  reflection → range biased long) and under realistic 38.855 t50=50 ns timing (15 m range noise →
  all-UE p50 ~42 m). SF noisier + a LOS>NLOS GDOP inversion (LOS-to-BS0 UEs cluster near BS0 = poor
  trilateration conditioning despite well-spread anchors) — point-estimate trilateration is
  GDOP-sensitive even with near-exact ranges.
- **AoA classical BREAKS** on these scenes (LOS p50 30–95 m) — NOT a bug, GEOMETRY: DeepMIMO city BS
  are LOW (6 m) CENTRAL small cells with planar arrays facing +x, so (a) ~0 elevation → no AoA range
  cue, (b) planar front/back ambiguity with UEs at 360° around the BS → half the bearings
  unresolvable. Contrast Munich's 27 m DOWNTILTED SECTORIZED macro where AoA worked (1gNB AoA+ToA
  p50 3.5 m, [[classical-loc-baseline]]). Cross-sim lesson: classical AoA needs elevated sectorized
  anchors; ToA needs only sync + bandwidth.
- **Classical vs LEARNED (NYC, same geo test n≈310):** learned net 1-gNB joint p50 **14.1 m** ≈
  classical ToA-trilat 3-gNB PERFECT-timing (17 m), and BEATS classical 3-gNB under REALISTIC 50 ns
  timing (42 m). Headline: one learned CSI codeword from a SINGLE gNB matches/beats classical
  multilateration from THREE synchronized anchors, and degrades far less in NLOS. Reinforces the
  §4.2 "learned > classical fingerprinting" thesis on an independent simulator.

**Open:** matched-overhead eType-II arm on DeepMIMO; Munich→DeepMIMO zero-shot transfer;
headline-matched ~80k asu run.
