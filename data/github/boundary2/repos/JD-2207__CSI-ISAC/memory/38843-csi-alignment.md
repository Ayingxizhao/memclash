---
name: 38843-csi-alignment
description: "Workstream aligning the CSI-feedback code (clause 6.2) with TR 38.843 V19 reporting/representation — what's done, the Option-2b finding, and the tier plan"
metadata: 
  node_type: memory
  type: project
  originSessionId: 36d92029-a760-4cd0-9db5-b64ee35b1ed0
---

Active workstream (started 2026-06-25): make the thesis CSI-feedback code spec-faithful to
**TR 38.843 V19 §6.2** so we study performance the way §6.2.2 does. Reporting/representation/docs
alignment, NOT a numeric-results task. Grounded in `literature/explainers/38843-j00-walkthrough.md`
+ [[3gpp-kpi-targets]]. Doing it "bit by bit" with the user reviewing each. See
[[matched-overhead-classical-vs-dl]] (the sec4c story this reframes), [[thesis-roadmap]].

## KEY FINDING (verified firsthand against code)
Our CSI output = **Option 2b (EXPLICIT channel matrix in angular-delay), MSE-trained** — NOT
Option 1b (precoding matrix). `multitask_ae.py decoder(z)` reconstructs normalized H (the object
`data_feed.py` provides); `nmse_per_sample` in `multitask_train.py:56`. Corrected the wrong
"Option 1b = ours" note in [[3gpp-kpi-targets]]. This IS the sec4c mechanism: explicit-H MSE-DL vs
eType-II's precoding-subspace PMI (Option 1b-style) → eType-II ≥ MSE-DL on matched-overhead sum-rate.
**Rank-1 nuance:** at n_rx=1 the precoder = h*/||h||, so Option 1b/2b carry near-identical info; the
"precoding > explicit" gap (§6.2.2.19) is mainly a **rank>1 effect** → Option 1b migration is best
paired with rank 2/4.

## TIER PLAN (effort vs rigor, agreed with user)
- **Tier 1** — intermediate-KPI + labels (cheap, no numerics change). § what §6.2.2 reports.
- **Tier 2** — switch representation to **Option 1b** (precoding matrix) + SGCS/precoding-aware loss.
- **Tier 3** — eventual KPI: wire `phy_abstraction.py` (EESM link-to-system, BUILT but UNWIRED) into
  an FTP-1 + scheduler + queue harness → real **UPT** (avg + 5% + CDF) at RU points. No ns-3.
- **Tier 4** — regen **rank 2/4** (n_rx=2/4) + per-layer feedback (and optional 32-port dual-pol) =
  the regime where AI actually beats eType-II on 3GPP's terms; the change that can move the headline.
Honest ceiling: Tiers 1-3 at rank-1 = a rigorous §6.2.2-faithful study, but rank-1 is §6.2.2.19's
low end (AI gain 0.2-2%, sometimes negative). Full "same as §6.2.2" (rank sweep + UPT) needs Tier 4.

## LANDED
- **Bit 1 (DONE 2026-06-25):** `mu_mimo_eval.py` now reports the §6.2.1 KPI stack (additive, no model
  numerics changed; byte-compiles; helper math CPU-validated). New `sgcs_nmse()` (SGCS primary +
  scale-invariant NMSE) + `peruser_se_stats()` (per-user SE mean + cell-edge 5% + CDF) + overhead-
  reduction% vs Rel-16 eType-II + per-method `bits` map. HONEST LABEL: the SE is a **full-buffer SE
  PROXY, NOT UPT** (docstring + print header + footer flag the Tier-3 phy_abstraction UPT upgrade).
  Not yet run on a real ckpt (needs GPU).
- **Bit 2 (DONE 2026-06-25):** representation labeling — `multitask_ae.py` module docstring now states
  Type-1 two-sided / Level-y, **Option 2b** explicit-channel (not 1b), **Case 2-1** quant, rank-1 nuance,
  Option 1b migration plan. Corrected [[3gpp-kpi-targets]] §7.1.2 note (1b→2b retraction).
- **Bit 3 (DONE 2026-06-25):** Tier-2 step 1 — built `data_feed.precoding_matrix_repr(H_delay)` = the
  Option-1b target transform (per-subcarrier unit-normalize the antenna vector → keeps direction+phase,
  drops freq-selective magnitude; stays delay-compact; drop-in before angular_dft+normalize). CPU-validated
  (scratchpad/prec_test.py): per-sc SGCS(V,H)=1.000, unit per-sc norm, 99.9% delay energy top-3 taps, RZF
  sum-rate from V-directions = **100.1% of from-H** (comms-SUFFICIENT). **KEY QUANT of the rank-1 caveat:**
  V differs from the Option-2b target by only **4.5%** (‖Vn−Hn‖/‖Hn‖) → the precoding rep IS different but
  modestly at rank-1, confirming the big precoding>explicit gap is a rank>1 effect. NOT a re-run of the
  §4c precoding-aware LOSS (that was negative/architectural); this changes the TARGET. NOT yet wired/trained.
  NEXT: bit 4 = wire into build_multitask_feeds behind `csi_repr` flag (explicit byte-identical; keep loc
  log_mag from ORIGINAL H so loc path unaffected); bit 5 = SGCS recon loss + recon-only Option-1b vs 2b train.
- **Bit 4 (DONE 2026-06-25):** wired `csi_repr="explicit"|"precoding"` into `data_feed.build_multitask_feeds`
  (precoding conversion before the unitary angular DFT; log_mag from ORIGINAL channel energy). CPU-validated
  (scratchpad/bit4_test.py, synthetic shards): default==explicit BYTE-IDENTICAL; explicit==manual pipeline;
  precoding==manual precoding pipeline; **log_mag IDENTICAL across modes (loc cue preserved, std 1.0 not const)**;
  precoding vs explicit target differs 15.5% L2 (= discarded freq-selective magnitude + phase-ref; comms
  direction still identical, SGCS=1.0 from bit3) → real, non-trivial target. Explicit path untouched.
  NOTE: flag added to single-gNB build_multitask_feeds only (multi-gNB build_multignb_feeds NOT yet; add if a
  precoding multi-gNB run is wanted).
- **Bit 5 WRITTEN + pipeline-validated (2026-06-26), HOLD for user go-ahead to launch the REAL run.** Added:
  (a) `multitask_train.sgcs_loss(recon,target,n_rows,n_cols)` = differentiable 1−mean-per-subcarrier-SGCS
  (antenna-freq, real/imag explicit for stable autograd) — CPU-validated: perfect/scaled→0, random→0.98,
  grad-descent 0.98→0.007. (b) `train_multitask(..., csi_repr=, recon_loss=)` kwargs (+ CLI args + cfg
  persistence + meta-grid load mirroring beam_loss); recon loss picks nmse|sgcs at the loop. (c) NEW runner
  `exp/exp_csi_repr.py`: trains a list of `csi_repr:recon_loss` ARMS (default explicit:nmse [2b baseline],
  precoding:sgcs [Option-1b move], precoding:nmse [target-vs-loss control]) at MATCHED bits, scores each
  vs the TRUE EXPLICIT channel with §6.2.1 KPIs (SGCS precoder-direction + scale-inv NMSE + per-user SE
  mean/edge), + faithful Rel-16 eType-II benchmark + Perfect CSI. Args --data_dir/--code_bits/--K/--split_mode/
  --smoke. END-TO-END smoke on synthetic shards PASSED (all 3 arms train incl SGCS-loss arm, eval+eType-II+JSON
  all wire). NOT a real result. LAUNCH: `mamba run -n venv python exp/exp_csi_repr.py --data_dir
  data/rt_munich_64ant_10000ue --epochs 80 --code_bits 4` (10k proxy first; CONFIRM on 100k). Honest prior:
  rank-1 A/B expected SMALL (precoding vs explicit target differ only ~4-15%, SGCS=1 comms-equivalent) — the
  real payoff is the rank>1 Tier-4 follow-up. All edits additive; explicit:nmse path = the existing baseline.
  CHEAP-AXIS COMPLETION (2026-06-26): exp_csi_repr now also reports SE CDF (p50 col + {5,50,95} JSON),
  overhead-reduction% vs eType-II, enc/dec real-value params + **FLOPs** (§6.1), and the generalization Case
  label (random=Case 1 / geographic=Case 2). FLOPs via NEW `multitask_ae.count_macs` (Conv2d/Linear hooks,
  FLOPs=2*MACs, no new dep; CPU-validated). All cheap CSI-axes now DONE.
- **Bit 5 RESULT — 10k los15, rank-1, 1024b, K=8, random split (2026-06-26, results/csi_repr/):**
  | arm | SGCS | NMSE dB | SE mean% | edge% |
  explicit:nmse(2b base) 0.754/−6.85/75.3/30 ; precoding:sgcs(1b move) 0.680/−5.43/**66.2**/20 ;
  precoding:nmse(control) 0.766/−6.88/74.9/**42** ; eType-II 236b 0.706/−5.89/74.6/13. enc 2.10M/7.4MFLOP,
  dec 2.13M/180.8MFLOP. **CONCLUSIONS:** (1) **SGCS-LOSS arm NEGATIVE** — worse on EVERY axis incl SGCS
  itself (0.680<0.766) ⇒ the precoding-aware LOSS optimizes worse (echoes §4c "centroid is architectural";
  here actively worse, likely flatter/degenerate landscape from scale+phase invariance). (2) **precoding
  TARGET + NMSE loss ≈ neutral on MEAN (74.9 vs 75.3) but lifts CELL-EDGE 30→42%** = small real worst-user
  gain (precoding direction helps RZF nulling for weak users) — the only positive signal, exactly as the
  rank-1 prior predicted (target differs only ~4-15%, mean ≈, edge moves). (3) DL ≈ eType-II on SE mean but
  4.3× more bits (ovh −334%); precoding edge 42% ≫ eType-II 13%. OPEN: is SGCS-loss underperf the loss or
  under-optimization (LR/epochs)? 100k confirm of the cell-edge signal pending user call. Honest: Option-1b
  at rank-1 = mostly neutral + a cell-edge nudge; the SGCS loss is the wrong lever. Motivates rank>1 (Tier 4).
- **Bit 5 RESULT @100k — CELL-EDGE SIGNAL CONFIRMED + STRENGTHENED at scale (2026-06-26, results/csi_repr/run_100k_los15.log,
  100k los15, 1024b, K=8, random split=Case 1, 80ep).** | arm | SGCS | NMSE dB | SE mean% | edge% |
  explicit:nmse(2b base) 0.873/−10.05/87.8/**59.0** ; precoding:sgcs(1b move) 0.719/−6.11/70.6/26.4 ;
  precoding:nmse(target control) 0.878/−9.76/86.0/**79.3** ; eType-II 236b 0.693/−5.71/73.0/12.3. CONCLUSIONS:
  (1) **The precoding-TARGET+NMSE cell-edge lift HOLDS AND GROWS at scale: 5%-ile SE 59→79% = +20.3pp** (vs +12pp
  at 10k) over the explicit baseline = the §6.2.1 "5% UPT" cell-edge KPI, the ONE positive Option-1b result, now
  robust at 100k. Cost: mean SE −1.8pp (86.0 vs 87.8) and SGCS ~tied (0.878 vs 0.873). Mechanism: the unit-norm
  precoding direction helps RZF null interference for the WEAKEST users (cell-edge), trading a touch of mean
  for a big worst-user gain — exactly the rank-1 prior. (2) **SGCS-LOSS arm STILL NEGATIVE everywhere** (0.719
  SGCS < 0.878, 70.6% mean, 26.4% edge) → SGCS-as-loss is the wrong lever at 10k AND 100k; the precoding TARGET
  (not the loss) is what helps. (3) At 100k DL recon jumps to −10 dB so explicit:nmse mean 87.8% ≫ eType-II 73.0%
  here — but UNMATCHED (1024 vs 236b); the matched §4c story (684b eType-II) is unchanged, see [[matched-overhead-classical-vs-dl]].
  THESIS TAKEAWAY: migrating the CSI target to Option-1b precoding-matrix form buys a large, scale-robust
  cell-edge/5%-UPT improvement at rank-1 (mean ~neutral) — a clean §6.2.1-aligned positive; the SGCS loss does not.
- **Bit 6a+6b (DONE 2026-06-26) — dedicated-TRP loc upper-bound scaffolding.** 6a: `multitask_train.evaluate`
  loc CDF now p50/**67/80**/90 (§6.4.1 set) + test print. 6b: NEW `loc_source="channel"` in MultiTaskAE = loc
  head reads the FULL uncompressed angular-delay channel (2*Nc*Nt) instead of the codeword z → the dedicated
  full-CIR direct-AI-positioning UPPER BOUND vs codeword loc (= price of free positioning / ISAC Pareto). CPU-
  validated: xy (B,2), loc-in 8193, grad to loc_head NOT encoder (loc reads channel), bottleneck arm unchanged.
  6d later: multi-TRP full-channel (mirror multignb_ae, the spec 18-BS setup). Resource framing:
  full-channel loc needs dedicated UL-SRS / prohibitive feedback; codeword loc = zero incremental RS.
- **Bit 6c (WRITTEN + smoke-validated 2026-06-26, NOT yet run for real).** NEW `exp/exp_loc_dedicated.py`:
  2 loc-only arms, same data/split/loc-head, differ ONLY in loc input — A `codeword` (loc_source=bottleneck,
  code_bits=4 = 1024b, zero incremental RS) vs B `full_channel` (loc_source=channel = dedicated full-CIR upper
  bound, needs UL-SRS). Reports horizontal CDF p50/67/80/90 + the "price of free positioning" gap. Defaults
  split_mode=geographic (honest loc). CAVEAT in docstring: arm B is a raw-MLP on 8192-dim CSI → if it underperforms
  A that's MLP weakness not less info; pass --loc_fourier_features or build a conv-front-end variant (future) for a
  fair upper bound. Smoke (synth random-xy) PASSED (both arms train, table+JSON render). LAUNCH for real:
  `mamba run -n venv python exp/exp_loc_dedicated.py --data_dir data/rt_munich_64ant_10000ue_los15 --epochs 120`.
  **RAN 10k los15 geo 120ep (results/loc_dedicated/): codeword p50 16.5/p90 47.8 BEATS full_channel p50 30.1/
  p90 83.9 (price −13.6/−36.1). ⚠ INVALID upper bound = the raw-MLP caveat REALIZED:** codeword arm's encoder
  is a learned conv feature-extractor; arm B = raw MLP on 8192-dim CSI (no conv prior) = WEAK baseline, NOT
  dedicated upper bound. Do NOT read as "codeword beats dedicated". NEXT-SESSION FIX before using 6c: rerun
  with --loc_fourier_features 256 on both arms AND/OR build a conv-front-end arm-B (full channel through encoder
  conv, skip bottleneck) = fair full-CIR upper bound, then re-interpret.
- **Bit 6c FIXED + RE-RUN (2026-06-26, results/loc_dedicated/, the invalid upper bound now repaired).** Chose
  the conv-front-end over the Fourier-MLP because it's the SPEC-FAITHFUL fix (TR 38.843 §6.4.1 model input = CIR
  `N_TRP×N_port×N_t`; §6.4.2.4 model-input-size = HOLD the model, VARY the input; source companies use CNNs on the
  CIR, never a raw MLP). Added `loc_source="channel_conv"` (multitask_ae.py): full channel through a 2-block conv
  front-end MIRRORING the CsiNet+ encoder conv stack but SKIPPING the fc bottleneck + quantization → same conv
  inductive bias as the codeword arm, isolating INFORMATION as the only variable. exp_loc_dedicated.py now runs
  3 arms (codeword / full_channel raw-MLP [kept as contrast] / full_channel_conv [valid upper bound]); price gap
  = codeword − full_channel_conv. 10k los15 geo 120ep: **codeword MAE 24.8 / p50 16.4 / p67 24.2 / p80 34.2 /
  p90 49.2 ; full_channel_conv (upper bound) MAE 24.0 / p50 16.6 / p67 24.6 / p80 36.3 / p90 51.4 ; full_channel
  raw-MLP (invalid) MAE 40.6 / p50 30.1 / p90 83.9.** PRICE OF FREE POSITIONING (codeword − upper bound) = **p50
  −0.2 m / p90 −2.2 m ≈ ZERO.** CONCLUSIONS: (1) the conv prior WAS the missing piece — full_channel_conv (24.0)
  crushes the raw-MLP full_channel (40.6), confirming the earlier "codeword beats full channel" was a model-
  capacity artifact, NOT information. (2) **The compressed 1024b codeword MATCHES the full-CIR upper bound for
  positioning (within seed noise, even nominally ≤ on p50/p90)** → compression costs ~nothing for loc; "free ISAC
  ≈ free lunch" now rests on a VALID upper bound. (3) the 256-d bottleneck may even mildly regularize under geo
  split (codeword p90 49.2 < upper bound 51.4) but treat as a tie. Honest framing for the thesis §6.4.1: the
  zero-RS feedback codeword is positioning-information-sufficient vs the dedicated full-CIR direct-AI input.

## TIER-3 COMPLETE — UPT eventual KPI WIRED IN (2026-06-27)
Tier-3 was ~90% (latency module `latency_pareto.py` built+wired into `exp/isac_frontier.py`; UPT
harness `phy_upt.py` built+selftested but **nothing called it** — `exp_csi_repr`/`mu_mimo_eval`
still used the full-buffer SE proxy `peruser_se_stats`). NOW genuinely closed: `phy_upt.upt_stats`
(reconstructed CSI → RZF SINR → EESM/CQI/BLER `phy_abstraction` → goodput → FTP-1 0.5MB Poisson +
PF MU-MIMO scheduler + queue → UPT avg/5%/CDF) wired into `exp/exp_csi_repr.py` ALONGSIDE the SE
proxy (per method: Perfect/DL arms/Rel-16), cached to `csi_repr_results.json`, surfaced by
`exp/csi_matrix.py` (new upt_* cols + printed block). Flags `--upt_load`(0.5)/`--upt_bw_hz`(100e6)/
`--no_upt`. CPU smoke (200ue, K=4): Perfect 100% / eType-II 44% avg·20% edge / near-random-2ep-recon
0% — physical ordering correct. **BUG FOUND+FIXED (was a SEGFAULT/near-hang): degenerate recon →
goodput≈outage → `lam_user`→0 → `n_slots` exploded to 1e8–1e12 → crash.** Fixes in `phy_upt.py`:
(a) offered-load arrivals now from a method-INDEPENDENT reference rate (`ref_goodput_bps_hz` = the
Perfect-CSI mean goodput, passed by exp_csi_repr) so a worse recon shows lower UPT via QUEUE BUILDUP
not a collapsed arrival rate — the physically-correct mechanism; (b) hard horizon cap
`FTP1Config.max_slots=400k`; (c) nan/inf-guard SINR+rate. Selftest extended with a degenerate-input
bound check. Tier-4 (rank>1 regen, n_rx=2/4 + per-layer feedback/SGCS) remains the only un-started
tier — needs a Sionna-RT GPU regen (new data axis), explicitly deferred.

## MULTI-gNB channel_conv ceiling arm + genie-LOS oracle relabel (2026-06-27)
Two positioning-matrix fairness fixes (see [[classical-loc-baseline]]). (1) `multignb_ae.MultiAnchorAE`
gained `loc_source={"codeword","channel_conv"}` — channel_conv = per-anchor FULL CIR through a shared
conv front-end (mirrors single-gNB `MultiTaskAE.loc_conv`), fc bottleneck skipped → the multi-gNB
full-CIR DL UPPER BOUND (encoder/decoder still run, ISAC recon unchanged). Threaded through
`exp/exp_multignb.py --loc_source` (export stamped with loc_source); `exp/positioning_matrix.py`
`--dl_pred_npz` now takes MULTIPLE exports → codeword arm beside `channel_conv (DL, full-CIR ceiling)`.
Full 10k-triangle channel_conv run launched 2026-06-27 (results/multignb/10k/multignb_ab_chanconv_tri).
(2) `positioning_matrix.py` flags `dltdoa_genie` as an IDEALIZED UPPER BOUND (`*` suffix + `n` column +
footnote/oracle_note): perfect ground-truth LOS oracle (real systems estimate it) AND scored only on the
≥3-LOS-anchor subset (tiny n) → not a deployable peer; DL codeword on the same subset is ~tied at zero RS.

## TIER-4 STARTED — data+repr BUILT, but rank-2 is MARGINAL in Munich (2026-06-27)
Plan: `.claude/plans/tier4-rank2-csi.md`. DONE + CPU/smoke-validated: (1) data-gen rank-2 support —
`RTSceneConfig.rx_polarization` ("cross"=dual-pol→2 ports), `sionna_rt_gen.generate_batch` preserves
the rx-port axis when >1 (legacy n_rx_ant==1 path BYTE-IDENTICAL, verified: single-pol still (M,64,64));
`munich_dualpol_config()` + `rt_dualpol_data_gen.py` runner; smoke 300-UE → channel (M,2,64,64), meta
n_rx_ant=2. (2) per-layer feedback target `data_feed.precoding_layers_repr` (per-sc SVD → top-R right
singular vectors, delay-mapped, (...,R,n_ant,n_taps)) + `mu_mimo_eval.per_layer_sgcs`; CPU-validated:
layers orthonormal, self-SGCS=1, delay-compact. 10k dual-pol regen ran (`rt_munich_64ant_10000ue_dualpol`).
**KEY HONEST FINDING — rank-2 is MARGINAL (CORRECTS an earlier overstated number).** The feasibility
probe's "layer-2 capacity-share 0.21" was an ARTIFACT (it renormalized both eigenmodes to equal AVERAGE
gain, inflating the weak layer). Correct fixed-power metric on real dual-pol data: σ2/σ1 median 0.12,
energy share σ2²/Σ = **1.5%**; honest layer-2 capacity share (equal P/2 per mode) = **2.5% @10dB / 5%
@20dB / 14% @30dB**. ⇒ at realistic SNR the 2nd UE-pol layer is ~rank-1-in-disguise. **POLARIZED-VARIANT QUESTION RESOLVED
(2026-06-27, user asked to verify first): the marginal rank-2 is PHYSICAL, not a modeling artifact.**
(1) NAME MISREAD CORRECTED: `cuda_ad_mono_polarized` = MONOCHROMATIC + **POLARIZED** (not "mono-
polarization") — Sionna RT 2.0.1 ALREADY runs on a polarized Mitsuba variant. (2) `sionna/rt/path_solvers/
field_calculator.py` propagates the field as JONES VECTORS + applies a per-interaction JONES MATRIX
(`jones_mat@e_field`) from each material's Fresnel eval → full polarimetric depolarization, in Sionna's
path solver, independent of the render variant. (3) `cuda_ad_polarized` doesn't exist in the build
(only `*_mono_polarized` + `*_spectral_polarized`; spectral=multi-wavelength, irrelevant narrowband). (4)
EMPIRICAL: NLOS σ2/σ1 0.12 > LOS 0.07 proves reflection depolarization IS active. ⇒ NO higher-fidelity
lever; rank-2 is genuinely weak because a 2-port UE vs 64-ant gNB in Munich macro-NLOS has a small 2nd
eigenmode. UE spatial rank ≤ #UE ports (2). Real rank>1 study needs: 30 dB operating point (layer-2→14%),
or richer-scatter/smaller-cell scene (canyon/indoor), or accept "Munich macro is effectively rank-1" as
the honest §6.2.2.19 finding. Per-layer model retrain HELD pending the user's pick among those levers.

**RANK-2 CEILING quantified on 10k dualpol (2026-06-27, single-user analytical, equal-power P/2):**
rank-2-vs-rank-1 capacity GAIN — NLOS (n=9965, σ2/σ1 0.137): **10dB −22% / 20dB −2% / 30dB +22%**;
LOS (n=40, σ2/σ1 0.078): 10dB −24% / 20dB −9% / 30dB +10%. ⇒ (1) rank-2 only pays at HIGH SNR; at
≤20 dB forced 2-layer split is NEGATIVE (weak 2nd mode wastes power rank-1 would use) — with rank
ADAPTATION this floors at 0 (pick rank-1), so rank-2 is NEUTRAL ≤20 dB, +22% (NLOS) only @30 dB.
(2) NLOS>LOS confirmed (answers "does %NLOS matter": YES, NLOS depolarizes → stronger rank-2; our
az-235 data is 99.6% NLOS = the FAVORABLE regime). ⇒ user picked (a): run the rank-2 AI-vs-eType-II
study at **30 dB** (the only regime where rank-2 is beneficial). Building `exp/exp_csi_rank2.py`
(per-layer precoding AE + per-layer SGCS + rank-2 sum-rate vs Rel-16 Type-II rank-2) on the dualpol
data — self-contained (build_multitask_feeds assumes rank-1 (M,n_ant,n_taps), don't retrofit shared feed).

**TIER-4 RESULT — NEGATIVE (2026-06-27, `exp/exp_csi_rank2.py`, results/csi_rank2/csi_rank2_10k.json).**
10k dualpol (az-235, 99.6% NLOS), per-layer SVD precoding AE vs Rel-16 Type-II per layer, geo split,
test n=418, feedback 10 dB, **MU-MIMO K=8 @ 30 dB DL**. Per-layer SGCS: AI L1 0.597/L2 0.445 (mean
0.521, 2048b) vs eType-II L1 0.561/L2 0.431 (mean 0.496, 472b) — AI edges SGCS but at 4.3× bits, and
**the weak L2 is harder for both** (L2<L1). MU-MIMO sum-rate (b/s/Hz/group): Perfect-V r2 22.95/r1
35.08; AI r2 6.23/r1 10.71; eType-II r2 6.37/r1 10.58. **TWO NEGATIVES:** (1) **rank-2 HURTS at MU
load** — rank-2-vs-rank-1 gain Perfect −34.6% / AI −41.8% / eType −39.8% @K=8 (8 users×2 weak layers
=16 streams floods interference; single-user ceiling is +20.4%, so the multiplexing gain exists in
ISOLATION but is killed by inter-user interference at MU-MIMO load — this is why MU≠single-user, user
caught it). (2) **AI ≈ eType-II at rank-2** (MU r2 6.23 vs 6.37, eType nominally AHEAD at 4.3× fewer
bits) — the §6.2.2.19 "AI gains materialize at rank>1" does NOT reproduce here. ⇒ HONEST CONCLUSION:
Munich macro + dual-pol UE is EFFECTIVELY RANK-1 (marginal 2nd layer + MU interference make rank-2
counterproductive); AI-CSI is neutral vs faithful eType-II at rank-2 just as at rank-1. Infra (dualpol
data-gen, precoding_layers_repr, per_layer_sgcs, rank2_mu_sumrate) built+validated, transfers to a
richer-scatter scene (canyon/indoor) if a positive rank>1 is later chased. NOTE: AI here uses csi_repr
that autoencodes the PRECODER directly (explicit recon of V), code_bits=4 → 1024b/layer (UNMATCHED vs
eType 236b/layer); a matched-overhead (code_bits=1, ~512b) arm + a los15 dualpol regen (identical-
geometry rank-1↔rank-2) are the obvious follow-ups but won't change the rank-1 conclusion.

## RECON-PIPELINE SANITY — "is Munich RT data anomalous?" = NO (2026-06-26, synthetic control)
User worry: maybe our Sionna-RT Munich data has a hidden problem making recon NMSE modest
(−6.85 dB @10k 4-bit / −9 dB @100k). Validated CHEAPLY with controlled synthetic channels
(no DeepMIMO download needed; scratchpad gen scripts). Results (recon-only, encoded_dim 256,
eta=1/32, K-irrelevant): on-grid angular-delay-SPARSE 3-path synthetic — CONTINUOUS @40dB:
TRAIN −14.0 dB / TEST −6.84 dB ; 4-bit @40dB: TEST −3.87 dB. **CONCLUSIONS:** (1) NO pipeline
bug — model fits TRAIN to −14 dB (architecture CAN represent sparse CSI). (2) the ~−7 dB test
ceiling is GENERIC finite-data generalization at eta=1/32, NOT a Munich defect — unstructured
synthetic lands at the SAME −6.84 dB. (3) **Munich OUTPERFORMS the controlled synthetic**:
Munich −6.85 dB at 4-bit + 10 dB feedback vs synthetic needing continuous + 40 dB for −6.84
(only −3.87 at 4-bit) — Munich's spatial manifold HELPS generalization. (4) train→test gap
(−14→−7) explains why MORE DATA helps (100k −9 > 10k −6.85). ⇒ Munich NOT anomalous; pipeline
healthy; modest NMSE = high-compression + 4-bit-quant ceiling, consistent across datasets.
DeepMIMO external-validation plan (.claude/plans/magical-gathering-leaf.md) now OPTIONAL =
belt-and-suspenders real-RT confirmation for the thesis, not needed to answer the question.
ENV NOTE: installing DeepMIMO 4.0.3 bumped numpy 2.x→2.2.6 in `venv`; torch+CUDA/sionna 2.0.1/
the project pipeline ALL still run clean under it. DeepMIMO needs `dm.download(scenario)` (not local).

## REALISTIC CHANNEL ESTIMATION — Tier-1 EVM piece IMPLEMENTED (2026-07-02, eval-only, NOT yet run)
38.843 CSI EVM Table 6.2.1-1 mandates "realistic channel estimation" (+MMSE-IRC) as baseline; our
headline results feed ideal (true RT) CSI. Built the quantified robustness gap. `data_feed.add_estimation_noise
(H, snr_db, seed)` = per-UE effective-CSI-RS-SNR complex-Gaussian noise on the RAW channel BEFORE
normalize/DFT (CPU-verified: measured per-UE SNR = target exactly across 4-decade energy spread; seed-repro).
**DISTINCT from `multitask_train.add_awgn`:** add_awgn = FEEDBACK-link noise on the *normalized encoder input*
(loc log-mag cue stays clean); add_estimation_noise = ACQUISITION pilot error pre-normalize → corrupts BOTH
recon target AND loc path-loss cue (honest for the joint ISAC claim). Wired as
`build_multitask_feeds(..., est_snr_db=γ, est_seed=0)` (gated; None=ideal=byte-identical). NEW
`exp/exp_realistic_ce.py` (eval-only, no retrain): loads locked ideal ckpt, replays exact test split, sweeps
γ∈{ideal,30,20,15,10,5 dB}, reports per-cond (all/LOS/NLOS) recon NMSE + **SGCS** (also added `sgcs()` helper
= the other cheap 38.843 KPI) + loc p50/p90 + Δ-vs-ideal; headline op-point 20 dB; `--smoke`; →
results/realistic_ce_sweep.json. Both files py_compile-OK. Answers the
dense-full-band question: the 1024-pt grid is a faithful OVERSAMPLE of the delay-bandlimited channel (not an
illegitimate advantage); the real idealization is error-free acquisition, now sweepable. QA-doc Topic 6c.
**RAN 2026-07-02 (results/realistic_ce_sweep.json + realistic_ce_run.log), 100k los15, joint_los15_az170.pt,
feedback SNR 10 dB, eval-only, n=9968 test.** γ=ideal: NMSE −9.05 dB / SGCS 0.883 / loc p50 4.2 / p90 9.8.
Δ-vs-ideal: 30 dB +0.03 dB (≈ideal, sanity OK); **20 dB (nominal) +0.32 dB / SGCS −0.009 / loc FLAT (p50 4.2)**;
15 dB +0.92; 10 dB +2.36 / SGCS 0.801; 5 dB (knee) +4.79 dB / SGCS 0.663 / loc p50 +1.3 p90 +3.2. **TWO
POSITIVE FINDINGS:** (1) ideal-CSI headline is optimistic by a SMALL BOUNDED margin — recon barely dents at the
realistic 20 dB op-point (<0.35 dB), only degrades seriously <15 dB. (2) **LOCALIZATION strikingly ROBUST to
CE noise** — p50 flat 4.2 m until 5 dB (+1.3 m only) → codeword positioning tolerates noisy acquisition,
strengthens ISAC claim. CAVEAT: eval-only on IDEAL-trained ckpt = pessimistic "deployed naive" case; CE-noise-
trained would be ≥ this robust. This is the disclosable, quantified realistic-CE result for the thesis.

## STOCHASTIC 38.901 CDL GENERALIZATION — DONE + VERIFIED (2026-07-02) — comms generalizes to the spec channel
Proved CSI COMPRESSION generalizes to the SPEC (stochastic 38.901) channel = the EVM's baseline channel,
closing "only tested on ray tracing" for the COMMS half (as DeepMIMO did cross-simulator). Recon-ONLY (loc
UNDEFINED on CDL — clusters re-randomize per realization, no position→channel map) → SHARPENS the thesis:
comms half channel-agnostic, sensing half RT-contingent (the ISAC trade). BUILT (Path A, chosen over numpy):
- **Separate offline env `chgen`** = Sionna 0.19.1 + TF 2.15.1 (CPU), the original stochastic stack
  (`original/env1_sionna.txt`). venv is Sionna-2.0 RT (no `sionna.channel`, no TF) so CDL can't run there.
- **`cdl_data_gen.py`** (top-level src/, runs in chgen): Sionna's VALIDATED `tr38901.CDL` (max compliance),
  8×8 single-pol-V UPA gNB / 1-ant UE / 3.5 GHz / 100 MHz-1024sc / DS=100 ns / first-path-normalized delay /
  n_taps=64 — mirrors RT geometry. Each batch elem = independent CDL realization. Writes the project shard
  contract with xy=0 (loc undefined), los/indoor=False. **Gotcha fixed:** Sionna 0.19 `__init__` does
  `from . import rt` (mitsuba) → fatal LLVM-C.dll crash on Windows; stub `sys.modules["sionna.rt"]` before
  `import sionna` (channel loads before rt; CDL path never touches RT). Generated `data/cdl_B_10000`,
  `data/cdl_C_10000`.
- **RECON RESULT (train-on-CDL/test-on-CDL, 10k, 1024b, eta=1/32, recon-only):** CDL-B NMSE **−8.2 dB**,
  CDL-C **−11.1 dB** (vs Munich-10k −6.85, DeepMIMO-10k −9.9) → AI compresses the stochastic 38.901 channel
  comparable-to-BETTER than RT at matched 10k size. Core generalization claim SOLID.
- **HEAD-TO-HEAD vs faithful Rel-16 eType-II (exp_csi_repr --arms explicit:nmse, @30 dB K=8, results/cdl/{B,C}):**
  CDL-B AI 0.851 SGCS / −8.54 dB / 83.5% SE vs eType-II **0.425 / −2.53 / 39.2%**; CDL-C AI 0.914 / −11.22 /
  88.4% vs eType-II **0.594 / −4.14 / 49.3%**. AI decisively beats eType-II on BOTH — **BUT at 1024 vs 236 bits
  (4.3×, UNMATCHED overhead; +334% ovh)** = the §4c caveat → RESOLVED by the matched run below.
- **MATCHED-OVERHEAD RESULT (2026-07-02, code_bits=1 ~256b vs eType-II 236b, results/cdl/{B,C}_matched):**
  CDL-B AI **0.724 SGCS / −5.82 dB / 69.4% SE / 55% edge** vs eType-II 0.425 / −2.53 / 39.2 / 13; CDL-C AI
  **0.852 / −8.65 / 79.9% / 70%** vs eType-II 0.594 / −4.14 / 49.3 / 22. **AI BEATS eType-II DECISIVELY EVEN
  AT MATCHED OVERHEAD** — the 1024b lead was NOT an overhead artifact. **This is the OPPOSITE of Munich §4c**
  (matched eType-II ≥ MSE-DL there). Mechanism (verified): eType-II is a beam-SELECTION codebook, efficient
  only on spatially-SPARSE channels (Munich eff-rank 2.2 → competitive); CDL-B is spatially RICH (eff-rank
  5.4, 23 dense clusters) → eType-II's few beams structurally cap out even at equal bits → AI's delay-domain
  compression wins. ⇒ **the classical-vs-DL verdict is CHANNEL-DEPENDENT**, not universal. Caveat: eType-II
  param_comb=6 not swept (but a 0.43-vs-0.72 gap is too large for a config tweak). See [[matched-overhead-classical-vs-dl]].
- **FAIRNESS VERIFIED (this was the crux — nearly reported an inflated result):** eType-II's low SGCS is NOT a
  geometry/ordering artifact. Chain: (1) transpose-invariant beam-sparsity; (2) Munich LOS dominant-eigvec
  2D-DFT top-1 = 0.058 == CDL LOS 0.06 (IDENTICAL) → the "LOS not DFT-bin-sparse" alarm is a misleading metric
  (8-pt oversampled DFT spreads a tone), same for validated Munich; (3) eType-II code gives correct 0.706 on
  Munich → fair on CDL. **Real mechanism:** CDL-B spatial eff-rank **5.4** vs Munich **2.2** — CDL is spatially
  RICHER (23 dense clusters) → beam-selection codebooks capture less, while the AI exploits DELAY-domain
  compactness (70% energy in 8 taps). CDL-D LOS control = top eigenvalue 0.95 / eff-rank 1.1 → pipeline
  produces physically correct rank-1 LOS. **Lesson:** single-bin DFT-beam-peak is NOT an eType-II sparsity proxy.
- DELIVERABLE FRAMING: comms compression generalizes to the spec channel; the AI's advantage over eType-II
  GROWS on spatially-rich stochastic channels (delay-domain vs spatial-beam), modulo the unmatched-overhead
  caveat. DS=100 ns + rank-1 are the stated operating points. QA-doc Topic 6c. Artifacts: cdl_data_gen.py,
  data/cdl_{B,C}_10000, checkpoint/cdl/, results/cdl/{B,C}/csi_repr_results.json.

## DEVIATIONS to state in the thesis (scope, §6.1 allows "other datasets")
Sionna-RT Munich vs 38.901 statistical Dense-Urban-Macro; 64-elem single-pol-V vs 32-port dual-pol;
n_rx=1 = rank-1 (low end of §6.2.2.19); outdoor vs the §6.4 InF-DH positioning baseline; beam-mgmt FR2
out of scope. Benchmark = faithful Rel-16 eType-II (already in `beamforming_baselines.py`) = aligned.

## POSITIONING-SIDE SPEC GROUNDING (2026-06-26) — mirrors the CSI-side §6.2 work
Did for §6.4 positioning what bits 1-5 did for §6.2 CSI. Read 38.843 positioning clauses firsthand
(§5.3 / §6.4.1 / §6.4.2.1-.6 / §7.1.4 / §7.2.4 / §7.3.5 / §8) → `literature/explainers/38843-positioning-
deepdive.md` (verbatim Table 6.4.1-1 InF + 6.4.1-2, model input N_TRP×N_port×N_t @8.14ns CIR/PDP/DP,
truncated-Gaussian labels, fine-tune/timing/TRP multipliers, §8 "RECOMMENDED for normative work"). KPI
ALIGNED: our evaluate() p50/67/80/90 + #params+FLOPs = §6.4.1 exactly; 38.843 sets NO AI positioning target.
Our method = network-side DIRECT loc between Case 3a/3b, novelty = comms-codeword input (not dedicated
CIR/PRS); the `loc_source="channel_conv"` full-CIR arm (bit 6c) ≈ the §7.1.4 Case-3b "timing+power+phase of
channel response" dedicated input. Per-item spec-faithful config decisions + diffraction-OFF finding live in
[[spec-scenario-grounding]]. P1 gap = classical baseline DL-TDOA/Multi-RTT + 38.855 timing error (not yet coded).

## DRIFT NOTE
CLAUDE.md Tier-1 list names a top-level `model_config.py` — it does NOT exist (only
`src/original/model_config.py`); config is argparse in `multitask_train.py`, persisted as `ck["cfg"]`.
