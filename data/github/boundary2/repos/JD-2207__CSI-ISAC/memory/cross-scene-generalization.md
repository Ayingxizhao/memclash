---
name: cross-scene-generalization
description: "Cross-scene #6: Munich-trained ISAC model -> Paris(etoile) zero-shot + few-shot fine-tune curve. Loc fingerprint COLLAPSES to random zero-shot; recon transfers PARTIALLY; both re-instantiate with target data. Closes the single-scene audit caveat. 2026-06-19."
metadata:
  node_type: memory
  type: project
  originSessionId: thesis-writing-prep
---

Cross-scene generalization study (roadmap #6) — quantifies the BOUNDARY of the Munich-trained
multi-task ISAC model on a second urban scene, and the cheap RT-digital-twin re-instantiation
cost. Closes the single-scene caveat in [[simulation-audit-caveats]] (#5). Directly confirms
[[identifiability-diagnostic]] (loc = scene-specific fingerprint) at the strongest test: a whole
new city. See [[thesis-roadmap]], [[localization-analysis]], [[los-coverage-orientation]].

### Setup
- **Target scene = `etoile` (Paris)** (user-chosen over san_francisco/florence; canonical Munich-
  twin, European mid-rise dense urban). Sionna 2.0.1 ships real-city scenes etoile/florence/
  san_francisco/munich (load by name).
- **gNB site (196, 4, 12)**: open Haussmann avenue, ~65% surrounding building density, ~31 m
  rooftops (found by a downward-ray surface-height probe). z=12 (NOT Munich's 27) deliberately —
  see LOS below. Cross-block **azimuth 255°** (down-avenue az points straight at the Etoile
  centre = max LOS).
- **etoile is intrinsically LOS-RICH**: even at this low cross-block placement, real depth-10 LOS
  = 53.5% (Munich los15 = 17%). The path-only az-scan UNDER-counts massively here (predicted ~5%)
  because etoile's thin walls + wide boulevards give lots of straight-through-refraction false-LOS.
  Matching Munich's 17% would need cutting max_depth/refraction = DISTORTS the channels, so instead
  the LOS-ratio difference is CONTROLLED by conditioning every metric on LOS/NLOS.
- **Data**: `data/rt_etoile_64ant_10000ue` (10005 UEs, 53.5% LOS, 2757 indoor; gen ~13 min @
  12.7 UE/s; batch=12 cfr_chunk=16 to bound the Dr.Jit 2^32 tensor — etoile depth-10 explodes path
  count vs Munich). Generated with `rt_gen_run.py` (now has `--gnb_x/y/z` + `--cfr_chunk`, defaults
  = Munich so legacy runs byte-identical; `diag_los_coverage.py` also gained `--gnb_x/y/z`).
- **Source model**: `results/geo_split/100k/geo_geographic.pt` (Munich los15 100k joint, GEO-split-
  trained = honest). IMPORTANT: do NOT use `joint_los15_az170.pt` for cross-scene — it was
  RANDOM-split-trained, so a geo-split Munich test leaks its train UEs (gave a false 3.9 m / −11.4 dB
  "source ceiling"); the honest geo source is 20 m / −8.96 dB.
- Code: `exp/cross_scene_eval.py` (zero-shot + warm-start few-shot fine-tune curve; recon NMSE is
  per-sample-normalized => scene-agnostic/comparable; loc reported in target-frame meters [best-case
  affine via each scene's own min-max] AND normalized [0,1] space). `results/cross_scene/etoile_xscene.json`.

### RESULT (2026-06-19) — the quantified boundary
recon NMSE dB | loc MAE m | loc norm-p50  (geo test, n=512 etoile / 3843 Munich):
- **Munich native (honest):** −8.96 | 20.0 | 0.034
- **etoile ZERO-SHOT:**       −2.49 | 186  | **0.505**  (LOS −2.47/182, NLOS −2.50/189 — uniform)
- etoile +100 shots:          −2.75 | 94   | 0.215
- etoile +500:                −2.96 | 64   | 0.141
- etoile +2000:               −3.74 | 46   | 0.095
- etoile +5000:               −4.14 | 38   | 0.081
- **etoile-NATIVE CEILING (geo, from-scratch 120ep, full ~8k train):** −4.63 | 26.2 | (p50 16.9, p90 56.1)

### ETOILE-NATIVE CEILING (added 2026-06-19, resolves finding #3's open caveat)
Computed with `exp/exp_geographic_split.py --data_dir data/rt_etoile_64ant_10000ue --epochs 120
--batch_size 32 --out_dir results/cross_scene/etoile_native` (~14 min, both arms; geo_split.json +
etoile_native_run.log). VERIFIED apples-to-apples: `multitask_train.loc_mae_m` and
`cross_scene_eval` BOTH use `denorm_xy(.., feed.xy_min, feed.xy_max, feed.pos_norm)` with etoile's
OWN min-max → identical footing; recon NMSE per-sample-normalized in both. The docstring's "best-
case affine" = this same min-max linear map, NOT a fitted rotation.
- **etoile-native geographic floor: recon −4.63 dB | loc 26.2 m (p50 16.9, p90 56.1).** Random-split
  (leaky) arm: −5.86 dB | 13.8 m (p50 9.3, p90 25.4) → second-city spatial-leakage gap loc +12.4 m /
  recon +1.23 dB reproduces the Munich §3 audit on a new city (re-justifies geo-split as honest).
- **ETOILE IS INTRINSICALLY HARDER THAN MUNICH** (native floors: loc 26.2 vs 20.0 m = +31%; recon
  −4.63 vs −8.96 dB = 4.3 dB worse). So the old "5000-shot doesn't reach Munich-native (20m/−8.96dB)"
  comparison was UNFAIR — etoile can't reach Munich's numbers with unlimited data (denser depth-10
  refraction-rich multipath = worse compressibility + fingerprint floor). Correct yardstick = etoile
  ceiling, not Munich's.
- **AGAINST THE CORRECT CEILING, 5000-shot has largely re-instantiated the scene:** recon 5000-shot
  −4.14 is within **0.49 dB** of the −4.63 floor (77% of achievable gap closed = ~SATURATED); loc
  5000-shot 38 m has closed **~93%** of the 186→26.2 m gap (residual 11.8 m, still climbing). Recon
  plateaus, loc does NOT (loc = harder-to-relearn fingerprint, but much closer to done than the bare
  38-vs-20 number implied). REVISED finding #3 framing below.

### Findings (thesis framing)
1. **LOC FINGERPRINT DOES NOT TRANSFER — full collapse.** Zero-shot normalized loc error = 0.505,
   i.e. the prediction is ~uncorrelated with truth (a centroid/random guess in [0,1]^2); 186 m.
   IDENTICAL for LOS and NLOS => genuine scene-transfer failure, NOT the LOS-ratio difference.
   This is the strongest possible confirmation of [[identifiability-diagnostic]]: the loc head is
   a scene-specific fingerprint (coordinate frame + reflector geometry differ -> nothing transfers).
2. **RECON TRANSFERS PARTIALLY.** Zero-shot −2.49 dB (vs −8.96 native): degraded ~6.5 dB but NOT
   collapsed — still captures ~44% of channel energy (a trivial predictor = ~0 dB), because the
   angular-delay sparsity it exploits is partly scene-agnostic. More transferable than loc (which
   is at random). Matches the prediction's DIRECTION (recon > loc transfer), though recon also
   degrades substantially in absolute dB.
3. **CHEAP RE-INSTANTIATION via the RT digital twin — both heads recover monotonically with target
   data.** With 5000 etoile samples (half a ~13-min RT-twin gen): loc 186->38 m (norm 0.505->0.081),
   recon −2.49->−4.14 dB. Loc recovers more relative ground; recon recovers slower in absolute dB
   (the decoder must re-learn the scene's specific multipath). NEITHER reaches Munich-native at 5000
   shots and the curve has NOT plateaued (recon −3.74->−4.14, loc 46->38 from 2k->5k) => full
   re-instantiation needs more target data/epochs (warm-start full fine-tune, 30 ep). [CAVEAT NOW
   RESOLVED 2026-06-19 — see ETOILE-NATIVE CEILING section above: the etoile-native geo floor is
   −4.63 dB / 26.2 m, and etoile IS intrinsically harder than Munich (+31% loc, +4.3 dB recon).
   Measured against the CORRECT (etoile) ceiling, 5000-shot recon is ~saturated (within 0.49 dB) and
   loc has closed ~93% of the gap (11.8 m residual, still climbing). The earlier "doesn't reach
   Munich-native" was the wrong yardstick.]
4. **Conditioning on LOS/NLOS** (the controlled comparison) shows the collapse + partial-recon-
   transfer hold in both regimes => results are scene-geometry transfer, not a LOS-distribution artifact.

THESIS USE: this is a quantified GENERALIZATION-BOUNDARY result (not a hoped-for positive) — exactly
the framing the user set. Loc is fundamentally a per-scene fingerprint (collapses, must be re-learned);
recon partially transfers; a cheap RT digital-twin few-shot adaptation re-instantiates both. Closes
the single-scene audit caveat with a concrete, defensible boundary.
