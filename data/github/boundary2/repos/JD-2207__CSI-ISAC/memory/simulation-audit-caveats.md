---
name: simulation-audit-caveats
description: "Methodological caveats found auditing the CSI-ISAC sim pipeline — what's optimistic / not yet controlled, ranked"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1d301dd3-0c88-4492-abe4-4c73b589ce04
---

2026-06-15 critical audit of the sim pipeline (verified against current code, not memory). What checks
out and what a thesis committee will press on. See [[beamforming-eval-deliverable]], [[localization-analysis]].

**Sound / verified:** noise model correct (add_awgn in angular-delay = AWGN on raw channel, transforms
unitary); recon↔beamforming consistent (NMSE −8.56 dB ⇒ predicted cos² 0.861 ≈ measured rho 0.867);
real 100 MHz / 1024-sub / 64-tap band (freq selectivity captured); loc IS fed path-loss (Frobenius
scalar via `log_mag`/use_magnitude) + intact angular/delay signature.

**Caveats, ranked (most → least important):**
1. **Overhead-matching — FIXED for the headline (2026-06-15).** Original §4a "DL 88% vs eType-II 63%"
   compared *continuous* 8192-bit DL vs 232-bit eType-II (35× gap). Now controlled in §4c
   (`overhead_matched_pareto.py`): matched gap is +15–22 pp (still a clean DL win; DL's worst > eType-II's
   best). DONE.
2. **Spatial leakage — FULLY ADDRESSED 2026-06-16 (geographic split at 10k + 100k).** Random
   `_split_indices` + ~1 m UE spacing let the model interpolate a dense field. Added
   `split_mode="geographic"` to `build_multitask_feeds`/`train_multitask` (`_split_indices_geo`: whole
   25 m grid cells held out + 5 m guard band). `exp/exp_geographic_split.py` run at both scales:
   - **10k** (`results/geo_split/10k/`): recon −5.91→−5.64 dB (+0.28), loc 18.1→28.6 m (+58%)
   - **100k** (`results/geo_split/100k/`): recon −9.07→−8.96 dB (**+0.11, extremely robust**), loc
     5.3→**19.9 m** (+275%; p50 4.2→12.5; p90 9.6→39.1). Geo test = 3843 UEs (4694 guard-band drops).
   **Headline numbers to report:** recon/beamforming is leakage-ROBUST (holds under geographic split);
   honest loc generalization = **~20 m MAE / 12.5 m p50 at 100k**. The 4.7 m keeper / 5.3 m this run
   are random-split upper bounds (flag explicitly). More data helps under geo split (28.6→19.9 m, −30%)
   but far less than under random split (18.1→5.3 m, −71%) — the apparent data-scaling win is mostly
   interpolation. DONE. Written as §3 of isac_findings.md.
3. **Sum-rate is on UNIT-normalized channels (`normalize_csi` per-sample Frobenius=1) + random equal-power
   user groups.** ⇒ absolute bits/s/Hz are NOT real capacity (per-subcarrier energy ~1/64, "tx SNR" axis
   nominal); report % of perfect / relative only. No near-far; benign interference. Frame sum-rate as
   CSI-error SENSITIVITY, not system capacity.
4. **Denoising confound — ADDRESSED 2026-06-16 (MU-MIMO eval at 30 dB feedback).** DL trained
   noisy→clean (it denoises); eType-II/CS compress the *noisy* estimate. Re-ran identical MU-MIMO RZF
   eval at 30 dB feedback (near-clean input) vs the 10 dB §4a run (`results/beamforming/mu_mimo_bs32_snr30/`):
   - **DL vs eType-II gap IDENTICAL (+24.9 pp) at both 10 and 30 dB** ⇒ none of DL's edge over eType-II
     is denoising; it's pure compression. DL recon itself is feedback-SNR-invariant (88.1→88.2%).
   - **DL vs CS-OMP gap shrinks +23.3→+14.5 pp** (CS-OMP 64.8→73.7% with clean feedback) ⇒ ~9 pp of
     DL's edge over CS *was* denoising, +14.5 pp is genuine compression. CS is the only baseline
     materially flattered by clean feedback; DL still wins clearly.
   Honest claim: DL's win is overwhelmingly better CSI-subspace compression, small denoising bonus only
   vs CS at low SNR. DONE. Written as §4d of isac_findings.md.
5. **Single-scene — ADDRESSED 2026-06-19 (cross-scene study, [[cross-scene-generalization]]).** Train
   Munich → eval Paris(etoile, a real urban Munich-twin, NOT the canyon toy). Quantified boundary:
   loc fingerprint COLLAPSES zero-shot (normalized err 0.5 = random; 186 m, uniform LOS/NLOS), recon
   transfers PARTIALLY (−2.49 vs −8.96 dB native), and both re-instantiate monotonically with few-shot
   target data (5000 etoile samples → loc 38 m, recon −4.14 dB). So DL's loc edge IS scene-specific
   fingerprinting (expected, confirms [[identifiability-diagnostic]]); recon's angular-delay sparsity
   is partly scene-agnostic; cheap RT-digital-twin adaptation recovers both. Caveat largely closed.

**TR 38.901 §8.4 map-based HYBRID channel model — DECISION: DO NOT IMPLEMENT, cite instead (2026-06-22, read §8.4 firsthand doc pp.149-157).** User asked if implementing §8.4 (RT + stochastic random clusters) would be "too harmful." VERDICT: net harmful + largely redundant; analogous to the ns-3 "real but wrong layer, don't build" call ([[thesis-roadmap]]).
- WHAT §8.4 IS: deterministic ray-trace (Step 3, Table 8.4-1: Friis/Snell+Fresnel/UTD/slab-penetration/RCS-scatter, paths within 25 dB of strongest) PLUS a §7.5-GSCM stochastic OVERLAY (Steps 4-13: Cholesky-correlated LSPs, exponential delays 8.4-1 with Xₙ~uniform, wrapped-Gaussian/Laplacian angles+random signs 8.4-10…-21, UNIFORM random phases). Spec says verbatim "NOT calibrated, can be used per company basis" + "not all parameters are used" ⇒ uncalibrated vendor option, NO standards-rigor gain.
- HARMFUL TO LOCALIZATION (the decisive reason): random clusters are POSITION-INDEPENDENT stochastic draws (conditioned only on local large-scale stats, not geometry). Fingerprinting needs a position-DETERMINISTIC channel. Uncorrelated draw → dilutes the geometric fingerprint (zero position info); spatially-consistent draw (§7.6.3) → a single seeded realization the net would fit non-physically (re-seed = different "world") → breaks the geo-split/cross-scene generalization story.
- REDUNDANT ON COMMS SIDE: the dense diffuse tail §8.4 adds stochastically, Sionna ALREADY adds DETERMINISTICALLY + position-tied via enabled diffuse scattering (scattering_coefficient=0.5, already on the HIGH side per the data-gen audit [[code-vs-literature-audit]]). Only edge-diffraction richness is under-represented by pure RT, and generic random clusters aren't a faithful substitute for diffracted paths.
- COST: faithful §8.4 = re-implement a big slice of §7.5 GSCM + fuse onto Sionna (weeks, Windows/OptiX) AND would INVALIDATE the entire result corpus (§4c/multi-gNB/frontier) by changing the channel model under them.
- DO INSTEAD: cite §8/Table 8.4-1 to legitimize the RT EM-interaction principles Sionna uses; frame pure-deterministic Sionna RT as a CLEANER instance of the 3GPP map-based methodology, stochastic overlay deliberately OMITTED because loc requires a position-deterministic channel (a principled choice, not a gap). Realism defense already covered by high diffuse-scatter + cross-scene + real-measurement pointer (2211.05527). OPTIONAL only if a committee demands a diffuse-mismatch test: eval-time-ONLY stochastic-cluster perturbation as a robustness probe (never in training) — but marginal vs existing AWGN/cross-scene probes.

**Fine / acknowledge as scope:** CS loses legitimately (channel not sparse, K99≈547 ≫ recoverable — not a
strawman); 59% indoor / 17% LOS is deliberately HARD (cuts against caveats 2–3); no CIs (gaps far exceed
noise); single-cell, no inter-cell interference / pilot contamination / hardware impairments / channel
aging (standard static-snapshot scope, list explicitly).
