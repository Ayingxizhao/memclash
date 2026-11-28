---
name: localization-analysis
description: "Why codeword localization is ~44m in pure NLOS, and what actually moves it (diagnostics)"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4bbcb42-a71c-4faa-ae17-bc15b8ffc247
---

Root-cause analysis of localization accuracy on `data/rt_munich_64ant_2000ue` (pure NLOS, 2019 UEs, 422x323 m scene). Scripts: `src/diag_localization.py`, `src/knn_localization.py`. See [[rt-datagen-progress]], [[thesis-project]], [[beamforming-eval-deliverable]].

**Diagnosis (loc-only CsiNet+ encoder, eta=1/32, seed 42, 2026-06-08):**
- TRAIN MAE **3.0 m** clean vs TEST MAE **44.6 m** clean → **15x generalization gap**. Capacity is NOT the limit (it memorizes train); noise is NOT the limit (test 44.6 clean → 47.7 @0dB, basically flat).
- Centroid-guess floor = 121.7 m. Spatial nearest-train-neighbor for test UEs = **3.6 m median** (grid is dense enough).
- **KNN on raw angle-delay CSI = 128 m** (≈ centroid floor!) vs **oracle nearest-in-space = 3.8 m**. → In pure NLOS, **Euclidean distance in CSI space is uncorrelated with physical distance** (multipath ≈ random hash of position at raw-feature level). KNN fingerprinting fails completely here.

**Key implications:**
1. The deep net (44 m) beats classical KNN (128 m) **~3x** — this IS the Section 4.2 "learned > classical fingerprinting" result. Strong thesis point.
2. NOT fixable by regularization alone (KNN, the smoothest interpolator, is worst). The CSI→position map is genuinely high-frequency/complex.
3. Gap from 44 m → 3.8 m oracle = **learnability gap**: complex map + only 1615 train samples. The two real levers: **(a) much more data** (denser sampling), **(b) stronger model / better inductive bias = TransformerAE** (global attention over angle-delay map, per guide's SwinCFNet/AiANet rationale).
4. SNR-robustness already good → don't spend effort on denoising for the loc task.

**User goal (2026-06-08):** 50 m is unacceptable; prioritize driving localization error down (model + data optimization) over baselines/mutual-benefit work.

**FIX CONFIRMED — data lever works (2026-06-08, `src/exp_backbone_data.py`, loc-only eta=1/32 test@10dB):**
- CsiNet+ 2k→10k UEs: TEST MAE **45.2 → 18.8 m**, p50 28.1 → **10.6 m**, gap 12.7x → 6.1x. Broke the 50 m wall via DATA, as diagnosed. Gap still 6x → more data likely helps further.
- **TransformerAE FAILED to train** (train MAE ~113 m ≈ centroid at both scales = optimization collapse, NOT capacity). Cause: PyTorch TransformerEncoderLayer defaults to POST-LayerNorm (unstable at lr 1e-3, no warmup) + saturating sigmoid bottleneck. FIX applied: `norm_first=True` (pre-LN) in both transformer enc/dec layers + lower LR (3e-4); retest running (bbps4l02g).
- Current best localizer: **CsiNet+ @ 10k, loc-only, 18.8 m MAE / 10.6 m p50.**

**TransformerAE verdict (2026-06-08): CNN wins, plain transformer abandoned for now.** Three bugs found+fixed to make it train: (1) post-LayerNorm → `norm_first=True`; (2) saturating sigmoid bottleneck → linear code + post-transformer LayerNorm; (3) **no positional encoding → permutation-invariant over angle tokens (the key bug)** → added learnable pos_emb to enc+dec. After all fixes: loc-only 10k test **46 m** (p50 34) vs CsiNet+ **18.8 m** — still 2.4x worse at 8x params (35.8M), still crawling at epoch 119. Conclusion: CNN's locality/translation-equivariance suits the grid angle-delay map; plain ViT needs more data/tuning. Guide's SOTA evidence (SwinCFNet/AiANet) is conv-hybrid/windowed-attention (reconstruction-focused), NOT plain transformer — that's the proper upgrade path if revisited. **Decision: lock CsiNet+ as working backbone.** All transformer fixes retained in `multitask_ae.py` (code_activation default 'none', pos_emb, pre-LN) for future Swin-style work.

**ETA SWEEP — FLAT (2026-06-08, `src/exp_eta_sweep.py`, loc-only CsiNet+ 10k):** encoded_dim 128→2048 (eta 1/64→1/4) all give TEST MAE ~18-19 m, p50 ~10-11 m, gap ~6x throughout. **Codeword size is NOT the bottleneck** — position info fits in a tiny 1/64 code. POSITIVE thesis result: feedback overhead and localization accuracy are DECOUPLED (run aggressive 1/64 compression with zero loc penalty). Lever to push lower = data + regularization, NOT eta.

**Datasets now: `data/rt_munich_64ant_{200,2000,10000,20000}ue/`.** 20k = 20007 UEs (90 LOS/19917 NLOS, 10837 indoor/9170 outdoor). `multitask_train.py` now also has tunable `weight_decay` param. `src/exp_regularization.py` = dropout x wd sweep.

**REGULARIZATION HURTS (2026-06-08):** dropout 0→0.2→0.4 makes test MAE WORSE 18.6→20.9→22.4 (gap shrinks 6.1x→2.9x only because train rises faster). wd negligible. Confirms non-smooth map (like KNN): smoothing removes usable signal. No-dropout stays best. Regularization NOT a lever.

**DATA SCALING — the winning lever, not saturating:** loc-only CsiNet+ eta=1/32 test@10dB: 2k=45.2m(p50 28), 10k=18.8m(p50 10.6), **20k=10.2m (p50 6.2)**. Doubling data ~halved error. 20k run still descending at epoch 119 (longer training would help). **Current best: 6.2 m median localization, pure-NLOS macro, from compressed CSI** — strong result. Next data step (40k) + longer epochs likely → ~6-7 m MAE.

**40k dataset created: `data/rt_munich_64ant_40000ue/`** = 40007 UEs (192 LOS/39815 NLOS, 21590 indoor/18417 outdoor). `src/exp_final_loc.py` trains 20k+40k loc-only @250ep, batch 128, saves best ckpt to `checkpoint/loc_best_{20k,40k}.pt`. Datasets now {200,2k,10k,20k,40k}ue.

**FINAL LOC RESULT (2026-06-08): 40k → TEST MAE 6.3 m, p50 4.1 m, p90 11.8 m** (loc-only, CsiNet+, eta=1/32, test@10dB). Full scaling: 2k=45.2/28.1, 10k=18.8/10.6, 20k=10.7/6.3, 40k=6.3/4.1 (MAE/p50). ~8x better than starting 50m. Each data doubling ~halves error, not saturated (80k→~4m possible but diminishing). **Longer training (250 vs 120 ep) added NOTHING — lever is purely DATA.** Strong thesis result: pure-NLOS macro, indoor UEs included, harder than FLnet's scenes. Checkpoints: `checkpoint/loc_best_{20k,40k}.pt`. **100k → MAE 4.6 m / p50 3.1 m** (loc_best_100k.pt).

**BANDWIDTH HYPOTHESIS WAS WRONG (2026-06-09).** Predicted higher BW (n78 CA, 200/400 MHz) -> sub-meter via finer delay resolution (p50~=c/B). FALSE. With n_taps=64 FIXED, loc got WORSE: 100MHz 6.3m/4.1 -> 200MHz 9.2/5.8 -> 400MHz 12.2/7.6. Cause (confirmed `diag_delay_coverage.py`): fixed 64 taps = delay WINDOW n_taps/B shrinks 192m->96m->48m; at 400MHz 14.4% of energy is in the last 16 taps (vs 5.9% at 100MHz) = far-multipath fingerprint TRUNCATED. **In NLOS, position is in the multipath signature spread over the delay profile (COVERAGE), not first-path ranging (resolution).** The 100MHz p50~=3m matching c/B was coincidental. Corrected test = constant delay window (scale n_taps with B: 200/128, 400/256) but needs REGEN (data stored at 64 taps) + scaled model/eta. Revised view: loc is COVERAGE + DATA + learnability limited; sub-meter via single-gNB NLOS bandwidth alone unlikely. Real levers: more data, multi-gNB. Datasets `data/rt_munich_64ant_40000ue_{200,400}mhz` (n_taps=64).

**JOINT ISAC NEGATIVE TRANSFER SHRINKS AT SCALE (2026-06-09, `exp_joint_100k.py`, joint CsiNet+ 100k, uncertainty weighting + 15ep recon warmup).** Joint vs single-task: loc 6.26m/p50 4.44m (single 4.60/3.10, +1.66/+1.34) | recon -7.79 dB (single -8.45, +0.66). Early ablation found joint cost ~6m loc; at 100k it's only +1.66m -> **data eases task competition**. Unified ISAC model = one eta=1/32 codeword -> denoised CSI (-7.79 dB) + position (6.3m/4.4m), modest well-quantified cost. Checkpoint `checkpoint/joint_best_100k.pt`. Final backbone = CsiNet+ (Swin/transformer benched). See [[beamforming-eval-deliverable]], [[swin-backbone]].

**PER-CONDITION ERROR BREAKDOWN (2026-06-13, `exp/diag_error_breakdown.py` on `joint_los15_az170.pt`, 100k los15, test@10dB).** Tool replays the exact test split (seed 42, return_flags) + groups loc MAE & recon NMSE by LOS/NLOS, indoor/outdoor, distance, path-gain. **Key finding: error is REMARKABLY UNIFORM across conditions — no pathological tail.** LOS 4.2m/-11.66dB vs NLOS 5.6m/-8.67dB (only +1.4m loc); near→far +0.6m; weak→strong gain -0.7m; **indoor≈outdoor for loc (5.3 vs 5.4m)**. So the ~5m is a SYSTEMIC RESOLUTION FLOOR of the huge (290×500m) fingerprint-ambiguous scene, NOT a few bad UEs → lever is overall representation/capacity (staged training, encoded_dim, contrastive), NOT tail-fixing. Sub-findings: indoor recon BETTER than outdoor (-10.0 vs -7.9 dB, sparser structured multipath); recon improves with distance/weak gain. Run on staged checkpoints when they land to compare. See [[references-and-prior-art]] (staged experiment + FLnet).

**WHY THE BANDWIDTH RESULT LOOKS BACKWARDS — the mechanism, verified at source (2026-08-09).**
`sionna_rt_gen._cfr_chunked` calls `paths.cfr(..., normalize_delays=True)` (explicit, and `cfr_to_delay`
documents why: first path at tap 0 so a 64-tap truncation holds most of the energy). Verified against the
installed Sionna 2.0.1 source that `paths.cfr` computes ĥ(f)=Σ_i a_i e^{−j2πfτ_i}. ⇒ **absolute
time-of-flight is REMOVED from the stored CSI; only relative delays survive.** So the learned localization
CANNOT be doing ranging — it is necessarily reading the multipath signature, which is exactly why bandwidth
behaves as delay-profile COVERAGE not ranging RESOLUTION (the 100→200→400 MHz got-worse result), and why
38.857's timing-based bandwidth scaling should NOT be assumed to apply to our method. Also why the classical
baselines need the separate `toa` shard (`cir(normalize_delays=False)`) — the CSI itself cannot supply it.
The walkthrough documents this (7 mentions); the frame-waterfall Part II §13.2 did NOT and has been fixed
(+ a row in its idealization table). See [[5g-system-primer]], [[spec-scenario-grounding]].
