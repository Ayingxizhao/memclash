---
name: classical-loc-baseline
description: "Classical 5G positioning baseline vs DL net + FULL §6.4.1 method matrix (DL-AoD/Multi-RTT/DL-TDOA+NLOS-mitig/UL-TDOA/E-CID, timing model) + triangle regen that fixes the collinear GDOP trap; DL dominates, classical good in LOS, breaks in NLOS"
metadata: 
  node_type: memory
  type: project
  originSessionId: 51b9241a-484b-488c-921a-cc25e1a7a9f5
---

Classical (non-learned) localization baseline answering "what do textbook 5G positioning
primitives achieve vs the learned ISAC net?" — the deployment-relevant control reviewers
expect. Mirrors 3GPP NR positioning (UL-AoA, Multi-RTT/ToA). See [[thesis-roadmap]],
[[localization-analysis]], [[identifiability-diagnostic]].

**Are these methods used IRL?** YES (not just GPS): A-GNSS dominates open-sky handsets, but
3GPP standardizes cellular positioning (E-CID, OTDOA/DL-TDOA, UL-TDOA; 5G NR Rel-16/17:
Multi-RTT, UL-AoA, DL-AoD) for E911/E112 + indoor/IoT, targeting ~1 m (0.2 m industrial).
The thesis's multi-gNB massive-MIMO setup is the literal deployment scenario for UL-AoA +
Multi-RTT. The net = learned alternative reading the whole CSI codeword instead of
hand-crafted ToA/AoA scalars (which break in NLOS).

**Implementation:** `exp/classical_loc_baseline.py` (CPU/numpy, no GPU/Sionna at run time).
Reproduces the DL run's exact test population (primary gNB0 reach-mask) + geo split (seed 42).
- **Tier 1 UL-AoA:** vectorized Bartlett over a world-frame angle grid. Manifold is EXACT —
  pulled Sionna's element positions (`scene.tx_array.positions(lam)`) + orientation
  (`tx.orientation`, rotation = Rz(az)Ry(el), ZERO roll from look_at) on CPU with the GPU
  hidden (`CUDA_VISIBLE_DEVICES=""`, safe alongside a running GPU job). Two gotchas solved:
  (1) stored antenna index is TRANSPOSED — i=r*8+c maps slow→horizontal y=(r-3.5)·0.5λ,
  fast→vertical z=−(c-3.5)·0.5λ; (2) planar array (all elems local x=0) is FRONT/BACK
  ambiguous → constrain AoA search to d·boresight>0. Result: **pooled LOS angular err 0.7°**.
  Single-gNB pos = bearing ray ∩ UE-height plane (elevation+height→range); multi = ray LS.
- **Tier 2 ToA / Multi-RTT:** needs absolute first-path delay. Added opt-in `toa` shard key
  via `sionna_rt_gen.save_toa` + `rt_munich_3gnb_data_gen.py SAVE_TOA=1` (→ `_toa` dir;
  legacy paths byte-identical; saves ACTUAL first-arriving delay so NLOS bias is kept).
  Re-gen of 10k 3gnb (~25 min): xy/los/indoor IDENTICAL to original, H differs only ~0.4%
  (diffuse Monte-Carlo noise, dominant-tap spatial sig corr=1.000) → comparison stays fair.
  LOS range vs slant-dist diff = 0.0 m (toa correct). range=c·toa, 3 m BW-quant + timing noise.

**RESULT (10k geo test, n=406, `results/multignb/10k/classical_baseline.json`):**
MAE / p50 / p90 (m), arms 1/2/3 gNB:
- **UL-AoA:**   158/161/267 · 111/85/253 · 52/38/97
- **AoA+ToA:**   58/53/152 · 53/39/118 · **37/27/82**  (the usable Multi-RTT+AoA method)
- **DL net:**    31/23/65 · 18/15/37 · **14/12/25**

**Findings (thesis framing):**
1. **Classical is EXCELLENT in clean LOS:** 1-gNB AoA+ToA LOS p50 = **3.5 m** (0.7° AoA +
   3 m ranging from ONE anchor) — even beats the DL net there.
2. **Classical BREAKS in NLOS:** 1-gNB AoA+ToA NLOS p50 = **60 m** (first path is a
   reflection → biased bearing AND range). This is the motivation for the learned approach.
3. **DL is far more robust overall:** DL with 1 gNB (31 m) beats classical with 3 gNB
   (37 m); DL handles the NLOS tail classical geometry cannot. The learned model reading the
   full multipath CSI is the contribution.
4. **ToA-only multilateration is DEGENERATE here:** the 3 gNBs are EXACTLY COLLINEAR
   (gNB1/gNB2 mirror gNB0 — the AoA-triangulation baseline), so range-only trilateration is
   rank-deficient even with perfect ranges (~120 m on all-LOS). AoA bearings are required to
   resolve it. Clean GDOP point: the layout optimized for AoA is degenerate for pure ToA.
5. More anchors help classical too (cooperative: AoA 158→52, AoA+ToA 58→37) but never reach
   the net — consistent with [[thesis-roadmap]]'s multi-gNB story.

**CRLB FLOOR — DONE 2026-06-19 (`crlb_block` in classical_loc_baseline.py, prints + json `crlb`).**
Position FIM per LOS-to-anchor link, mirroring the estimator's info sources (azimuth + elevation
for AoA, azimuth + ToA-range for fusion, range-only for ToA); per-UE bound = sqrt(trace(inv FIM)).
Sensor noise grounded in the MEASURED LOS errors via ROBUST (MAD) scale, NOT std — a few gross
sidelobe/ambiguity AoA outliers corrupt plain std (gave σ_az 9.7° vs true ~0.85° → "eff>1" false
bound violations). Final σ_az 0.85°, σ_el 0.56°, σ_range 1.73 m (=hypot(quant bin/√12, timing 1.5 m)).
Compare achieved-LOS **p50** (not MAE — same outlier tail corrupts the LOS mean: AoA+ToA 1gNB LOS
mean 24 m vs median 3.5 m) to CRLB p50; ratio ~0.8-1.3 = efficient (CRLB is RMS-scale, efficient
median ≈0.83·RMS). RESULTS (10k geo test):
- **1gNB AoA+ToA LOS CRLB-EFFICIENT: achieved p50 3.5 m vs CRLB 3.88 m, ratio 0.89** → the headline
  classical method is near-optimal in LOS, NOT a strawman (the key committee defense).
- **1gNB UL-AoA LOS p50 24.4 vs CRLB 21.5, ratio 1.14** → efficient; single-panel az+el (range from
  elevation) is geometrically weak → CRLB quantifies WHY ToA is needed.
- **ToA-only FORMALLY UNOBSERVABLE: FIM singular for ALL UEs at 1gNB & 2gNB** (1 range=rank-1;
  2 collinear-anchor bearings=parallel gradients), only 24/155 observable at 3gNB → upgrades the
  earlier "rank-deficient linear-LS" to a Fisher-information GDOP statement (the AoA-optimized
  collinear layout is provably degenerate for trilateration; the 24 off-baseline UEs hit 2.8 m).
- **NLOS has NO standard CRLB** (biased first-path → unbiasedness violated) = the FORMAL reason
  classical breaks in NLOS, the clean motivation for learning (cite generalized-CRLB-with-NLOS-bias
  lit, e.g. arxiv 2502.19354).
- **BONUS: multi-gNB AoA+ToA is 17-31× OFF its CRLB for gNB0-LOS UEs** (geometry supports ~3 m,
  mean-of-points fusion delivers 50-90 m) → QUANTIFIES the fusion-refinement opportunity below.

**CODE-vs-THEORY AUDIT 2026-06-19 — ToA-range FIM Jacobian CORRECTED:** the ToA term used
`J_d=[cosφ,sinφ]` (horizontal-range gradient) but the measurement is the 3D range r=c·τ, whose
gradient is `(d/r)[cosφ,sinφ]` (`|∇r|=d/r`). Fixed in `crlb_block` (multiply by `d/np.sqrt(r2)`).
IMPACT NEGLIGIBLE: 1gNB AoA+ToA CRLB p50 3.884→3.888 m, ratio still 0.89 (azimuth FIM 1/d²
dominates + LOS UEs have d/r≈1); achieved numbers unchanged. So the "CRLB-efficient, not a
strawman" conclusion now rests on the CORRECT Jacobian. Verified-correct in same audit: Bartlett
AoA (=|aᴴx|², argmax; Bartlett not MUSIC is right for a single rank-1 snapshot/UE), azimuth FIM
`[-sinφ/d,cosφ/d]`, elevation FIM `(-dz/r²)[cosφ,sinφ]`. results/multignb/10k/classical_baseline.json
re-promoted with the fix.

Remaining refinements (low priority): smarter multi-gNB AoA+ToA fusion (LS/outlier-reject vs
mean-of-points — now quantified at ~10-30× off CRLB); MUSIC vs Bartlett. AoA+ToA fusion = the
headline classical method to report.

**FULL POSITIONING MATRIX + TRIANGLE REGEN — 2026-06-27 (38.843 spec-faithfulness workstream).**
Extended `exp/classical_loc_baseline.py` from {UL-AoA, AoA+ToA, ToA-trilat, CRLB} to the full
§6.4.1 menu, all scored with CDF **p50/67/80/90** over LOS/NLOS × **perfect/50-ns timing** × 1/2/3
gNB. New methods: **DL-AoD** (beam-codebook-quantized bearing, `beam_quantize`), **Multi-RTT**
(sync-invariant absolute-range multilateration, `range_solve_xy`), **DL-TDOA raw + 3 NLOS
mitigations** (rwls / genie-LOS+reref / triangle-ineq, `tdoa_mitigated_xy`), **UL-TDOA**, **E-CID**
(=AoA+ToA @1gNB). **38.855 truncated-Gaussian timing model** `apply_timing` (network-sync per-gNB
offset + per-link Rx/Tx, std T1∈{0,50ns}, trunc[-2T1,2T1]; Multi-RTT skips the sync term =
sync-invariant). Regression guard HELD: AoA+ToA p50 51.5/39.1/26.3 ≈ old 53/39/27. Run schema now
nested `timings[perfect|t50][NgNB][method_subset]`. Flags `--t50_ns --nlos_mitig {all,rwls}`.

**TRIANGLE REGEN FIXES THE GDOP TRAP (the key result).** The legacy 3gnb shard is EXACTLY
collinear (anchor-triangle area = **0 m²**; gNB1/gNB2 = opposite mirrors of gNB0) → on it ALL
range/TDOA methods are degenerate (Multi-RTT/ToA-trilat/DL-TDOA ~140-230 m p50, CRLB ToA-only
unobservable for every UE) = an UNFAIR classical baseline (the strawman §1/§8.4 warn against). New
preset **`munich_3gnb_tri_config`** (sionna_rt_gen.py): gNB0 stays the los15 primary; gNB1/gNB2 at
+120°/+240° around the UE-region centroid → **area 35366 m², non-collinear**. Runner toggle
`GEOM=tri` → `data/rt_munich_64ant_{N}ue_3gnb_tri_toa`. 300-UE GPU smoke VALIDATED the fix: 3gNB
Multi-RTT p50 23.6 (was ~230), DL-TDOA(raw) p50 20.8/LOS 16.1 (was ~227), ToA-trilat p50 25.1 (was
~137), CRLB ToA-trilat now observable (4 degen vs all); also 69% LOS-to-any (vs collinear 45%, since
anchors surround the cloud).

**AUTHORITATIVE 10k triangle results — 2026-06-27** (`data/rt_munich_64ant_10000ue_3gnb_tri_toa`,
10009 UEs, 66% LOS-to-any, 770 shards, ~46 min gen; `results/positioning_matrix/positioning_matrix_tri.{json,csv}`).
3gNB CDF p50/p90 (m), perfect | t50: **Multi-RTT 16.3/40.0 | 22.3/47.4** (≈ spec UMi Multi-RTT
16.6@p90, barely moves under 50ns = **sync-invariance confirmed**); **DL-TDOA(raw) 14.2/144.7 |
25.4/141.2** (huge NLOS tail = the §8.4 strawman, + degrades with sync); **DL-TDOA(genie-LOS)
2.7/8.2 | 33.6/95.2** (≈ spec UMi NLOS-mitig 3.1 / UMa 8.6@p90 — mitigation collapses the tail
144.7→8.2 = the §8.4 NLOS-mitigation story); ToA-trilat 15.4/49.6 | 26.3/63.1; AoA+ToA/E-CID
23.0/62.6. ALL these were 140-230m on the collinear shard → the triangle geometry makes classical
TDOA/RTT a FAIR baseline and the numbers match the literature. **DL HEAD-TO-HEAD DONE.**

**AUTHORITATIVE CLASSICAL-vs-DL (triangle 10k, geo test n=406, 2026-06-27)** — DL net retrained on
triangle data w/ decoupled-σ head (`multignb_ab_tri.json` + `tri_pos_export.npz`;
`positioning_matrix_tri.json`). **3gNB p90 head-to-head (the fair fight, perfect-timing/all):**
DL-TDOA-genie 8.2 < **codeword DL 23.7** < Multi-RTT 40.0 < ToA-trilat 49.6 < AoA+ToA 62.6 <<
UL-AoA 125.9 / DL-AoD 128.2 / raw-DL-TDOA 144.7. DL codeword (zero incremental RS): 1/2/3gNB p90
65.5/31.3/23.7, NMSE −5.2/−5.9/−5.8 dB; LOS p90 13.0 / NLOS p90 25.1. **Framing: DL beats every
SYNC-HONEST classical (Multi-RTT, AoA+ToA) and the realistic raw/timing-error DL-TDOA at ZERO PRS;
only the genie-LOS-oracle NLOS-mitigated DL-TDOA (8.2) edges it — and that uses a perfect LOS
oracle + dedicated DL-PRS, which the codeword spends nothing on.** σ-head Protection Level (38.857
§9): raw k=1.645 under-covers (0.43, geo-split test err > train σ) → **split-conformal k=4.25 gives
exactly 0.90 coverage** (PL_med 21.7 m, err/σ corr +0.36); integrity-availability 0.41@AL=20m,
0.95@AL=50m. The σ-head value = per-UE RELATIVE uncertainty (informative), conformal sets the
absolute scale = the spec-faithful impl-defined PL. σ-head bug found+fixed (see
[[self-aided-probabilistic-pareto]]).

**FULL-CIR CEILING ARM (channel_conv) — 2026-06-27** (`multignb_ab_chanconv_tri.json` +
`tri_pos_export_chanconv.npz`; folded into `positioning_matrix_tri.json` beside the codeword arm).
Built multi-gNB `loc_source="channel_conv"` in `MultiAnchorAE` (per-anchor FULL CIR through a shared
conv front-end, fc bottleneck skipped; encoder/decoder still run so ISAC recon unchanged) =
multi-gNB analog of the single-gNB bit-6c upper bound. **channel_conv (full-CIR) 1/2/3gNB p50
17.8/10.1/8.0, p90 49.0/29.4/20.1** vs **codeword (zero-RS) p50 21.9/12.7/10.0, p90 65.5/31.3/23.7**.
PRICE OF COMPRESSION = p90 ~3.6 m @3gNB (16/2/4 m @1/2/3gNB), small + monotonic → the compressed
feedback codeword is positioning-info-near-sufficient vs the full CIR, multi-gNB confirms single-gNB
bit-6c. Both still ride COMMS RS (codeword zero-incremental FDD; channel_conv free in TDD reciprocity
/ extra feedback FDD) — NEITHER needs dedicated PRS. genie-LOS row now flagged `*` idealized upper
bound (oracle + n=9 subset), not a peer. `positioning_matrix.py --dl_pred_npz` takes MULTIPLE exports.

**TIER-3 + LATENCY COMPLETE (2026-06-27):** `latency_pareto.py` — per-method L1+E2E from 38.857
§8.1.3.1-4 firsthand (DL-TDOA E2E 222.5-353, UL 149-322, Multi-RTT 288.5-486, E-CID 88-198 ms;
L1 from T8.1.2.11-1) + **codeword DL-ISAC reframe: no dedicated DL-PRS → E2E 45-109 ms cold / 2-30
ms incremental** (skips T_DL-Meas 88.5 + assist/meas-gap). `phy_upt.py` — FTP-1 + PF scheduler +
queue over EESM/CQI/BLER goodput → UPT avg/5%/CDF (replaces full-buffer SE proxy; selftest:
recon-quality ordering + load monotonicity). Latency row wired into `exp/isac_frontier.py`
(DL-ISAC 2-30 ms vs DL-TDOA 222-353 vs Multi-RTT 288-486).

**CONSOLIDATION DRIVERS (new):** `exp/positioning_matrix.py` = classical suite + DL loc_source arms
(codeword=multignb bottleneck zero-RS, channel_conv upper bound) head-to-head, σ-head as 38.857 §9
**Protection Level** (`protection_level_report`: coverage / integrity-avail / misleading-info per
AL), reference conventional CDFs printed beside (UMi DL-TDOA 3-10m@p90, UMa 9-63m). On legacy data
DL codeword 3gNB p50 12.0/p90 25.2 already beats realistic UMa DL-TDOA (53-65m@p90) at zero PRS.
Cached DL gives only p50/p90 (no p67/80/LOS-NLOS/σ) → `--dl_pred_npz` hook for full CDF+PL after the
triangle retrain. `exp/csi_matrix.py` (Task B) = one consolidated CSI matrix from cached
results/{csi_repr,sumrate_vs_k,baselines,mu_mimo} → `results/csi_matrix/csi_matrix.{json,csv}`;
matched-overhead CORE (csi_repr, 1024b): DL Option-1b precoding(nmse) 5%-edge SE 0.261/79% vs
Option-2b explicit 0.194/59% (**+20pp cell-edge, the one positive**); sum-rate-vs-K: eType-II 684b
≈ DL 87-88%@K8/16, CS-OMP worse. rank-1 = §6.2.2.19 low end (rank>1 = Tier-4).
