---
name: code-vs-literature-audit
description: "Code components verified against literature/standards (precoder, angular-delay basis, link budget, denoising-AE, flow-decoder faithfulness) — thesis validation/methods material"
metadata:
  node_type: memory
  type: reference
  originSessionId: f0239455-53ee-4944-9e40-57c637969c4f
---

Consolidated code-vs-literature verifications (the user will cite these in the thesis
methods/validation). EARLIER audits live in [[beamforming-eval-deliverable]] (CsiNet+-based
qualifier; faithful Rel-16 eType-II vs TS 38.214 §5.2.2.2.5; CS-OMP = textbook Tropp-Gilbert
2007; UncertaintyWeighting = exact Kendall-2018; gaussian_nll = std diag-Gaussian) and
[[classical-loc-baseline]] (CRLB Jacobian fix vs 2502.19354). NEW this session below.
See [[matched-overhead-classical-vs-dl]].

## MU-MIMO precoder + sum-rate (mu_mimo_eval.rzf_sumrate) — VERIFIED
Underpins ALL §4 numbers. `W = Ĥ(ĤᴴĤ + (K/SNR)I)⁻¹`, power-normalized, noise=1;
`SINR_k=|h_kᴴw_k|²/(Σ_{j≠k}|h_kᴴw_j|²+1)`, `R=Σ log2(1+SINR_k)`.
- = standard MMSE / regularized zero-forcing precoder (regularized channel inversion,
  Peel-Hochwald-Swindlehurst, IEEE TComm 2005; = transmit-Wiener, Joham-Utschick-Nossek
  2005). reg α=K/SNR is the canonical RZF factor (SINR-optimal in large-system limit).
- SINR/rate matches 2605.08628 eq.(1) exactly (their σ²=1, power in W). ✓
- DESIGN CHOICE (document, not a bug): we use RZF + SUM-power constraint; 2605.08628 uses
  pure ZF + per-user equal power. RZF is the RIGHT choice for our IMPERFECT-Ĥ study (K/SNR
  regularization stabilizes inversion under CSI error; pure ZF amplifies it).
- ASSUMPTION (document): users co-scheduled as RANDOM K-tuples (consecutive test UEs, random
  split) — scheduler-agnostic; a real PF/orthogonal scheduler shifts absolute sum-rates but
  not the DL-vs-eType-II ordering.

## #1 Angular/delay basis — VERIFIED (standard CsiNet/AiANet representation)
- ANGULAR: `angular_dft_upa` (data_feed.py:130) = unitary 2D-DFT (fft2 norm="ortho") over the
  8×8 UPA grid = the Kronecker (az⊗el) beamspace transform; same basis family as the 3GPP
  Type-II OVERSAMPLED 2D-DFT codebook (ours un-oversampled/unitary; our faithful eType-II uses
  the O1=O2=4 oversampled version of the SAME basis). ✓
- DELAY: `cfr_to_delay` (sionna_rt_gen.py:416) = IFFT over 1024 subcarriers, keep n_taps=64,
  `normalize_delays=True` (first path at tap 0) = canonical CsiNet angular-delay truncation;
  validated ~93% energy in 64 taps (config:42 + didactic dump prints retention). Delay res
  1/BW=10ns ×64=640ns≈192m excess delay — right for a ~300m cell. FLnet config (100MHz/1024sc)
  matched. ✓
- NORM: `normalize_csi` (data_feed.py:144) unit-Frobenius + global-phase removal (ref=strongest
  elem) — correct, ρ/sum-rate are phase-invariant. ✓
- CAVEAT (label only, not correctness): antenna→(row,col) reshape assumes Sionna row-major
  PlanarArray order; if transposed it's still unitary+invertible and to_antenna_freq + eType-II
  use the SAME reshape → all mutually consistent; only az↔el axis labeling would swap.
- NOTE: 64-tap truncation keeps ~93% DELAY energy, but WITHIN the taps the angular-delay map is
  NOT sparse (K99≈547/4096, dense urban) — exactly why CS-OMP struggles & eType-II's structured
  projection is efficient.

## #2 Link-budget SNR model — VERIFIED (formula standard; RT gains physically consistent)
`linkbudget_snr_db` (multitask_train.py:164): `SNR_i = (P_tx−Nfloor) + 20log10‖H_i‖`,
`Nfloor=−174+10log10(BW)+NF` (multitask_train.py:351). Standard thermal-noise link budget
(kT₀=−174 dBm/Hz, NF=7 dB). Default = median-anchor (median UE→10 dB, uses only RELATIVE RT
gains); physical-anchor option via tx_power_dbm.
- SANITY CHECK (exp/_verify_linkbudget.py, rt_munich_64ant_10000ue_los15, N=10024, 18% LOS):
  median channel gain −95.4 dB, LOS−NLOS gap **11.9 dB** (UMa typical 10–25 ✓), cell 100–285 m.
  MAGNITUDE MATCHES UMa: UMa-NLOS PL@211m≈115 dB minus ~18–20 dB 64-elem array gain ≈ −97 dB ≈
  our −95.4 dB. ✓
- Gain-vs-distance SLOPE does NOT match clean UMa exponents (LOS −47.7 vs −22; NLOS −22.1 vs
  −39 dB/decade) — EXPECTED for site-specific Munich RT (building geometry + shadowing +
  NLOS-survivor selection), NOT a statistical channel → a FEATURE of using RT, not a bug.
- The fixed 10 dB feedback operating point is CONSERVATIVE: a real macro EIRP (~53 dBm) implies
  median SNR ~45 dB; we test in a HARDER feedback regime (stress-tests DL denoising). ~12% of
  UEs hit the −10 dB clip (deep-blocked) — clip working as intended. (Headline models use
  snr_model="uniform" snr_val=10; linkbudget is the optional-realism mode.)

## #3 Denoising-AE / feedback-noise model — VERIFIED
`add_awgn` (multitask_train.py:142): complex AWGN on the unit-Frobenius CSI BEFORE the encoder,
noise_var=sig_p/snr_lin/2 per real comp; CLEAN CSI = recon target; quantization modeled
SEPARATELY (code_bits, STE). Cleanly separates the two CSI-feedback impairments (estimation
error vs quantization) instead of conflating them = textbook denoising AE (Vincent 2008) +
standard sweepable feedback/estimation SNR. NICE PROPERTY (state in thesis): noise injected in
angular-delay but the DFT/FFT are UNITARY ⇒ AWGN there ≡ AWGN in antenna-freq (rotational
invariance) ⇒ "feedback SNR" is DOMAIN-INVARIANT, which is why ρ/sum-rate comparisons across
DL/eType-II/raw are consistent and computable in either domain. ✓

## Ad-hoc DATA choices (no literature) — now EMPIRICALLY/PROVABLY justified
(exp/_verify_data_choices.py, rt_munich_64ant_10000ue_los15, dl_mse.pt)
- **Phase reference = strongest |element| (normalize_csi, data_feed.py:160) — PROVABLY
  IMMATERIAL.** Strongest-elem vs fixed-[0,0]-tap reference: max ||H_s|−|H_f|| = 6e-8
  (magnitude IDENTICAL); ρ(H_s,H_f)=1.000 (differ ONLY by a per-sample global phase);
  ρ(H, H·e^{jφ})=1.000 (beamforming metric global-phase invariant). ⇒ §4 beamforming
  (ρ, MU-MIMO sum-rate) is reference-INDEPENDENT by construction; recon/loc see the same
  problem up to a fixed per-sample unitary. Strongest single verification — no retrain needed.
- **min_norm_frac=1e-3 degenerate-drop threshold (data_feed.py:237) — threshold IMMATERIAL,
  drop NECESSARY.** Leakage-free probe (model's REAL split fixed, only SUBSET the test set by
  a norm floor): NMSE FLAT across floors [0,1e-3,2e-3,5e-3,1e-2]×med — mean −6.0 / median −7.3
  / p90 −2.8 dB throughout (retained borderline UEs reconstruct as well as the rest). The drop
  itself is necessary (zero-norm channels diverge NMSE, see [[recon-nmse-zero-norm-bug]]); drop
  count grows slowly (17→26→37 over [1e-4,1e-3]×med) so the threshold sits in a low-density gap.
  METHODOLOGICAL CATCH (thesis-worthy): the NAIVE cross-threshold sweep is CONFOUNDED — changing
  min_norm_frac reshuffles the train/test split, leaking trained-on UEs into "test" (spurious
  −10 dB at non-default thresholds). Always hold the split fixed; and mean NMSE is heavy-tailed
  (mean −6 vs median −7.3) → report MEDIAN / norm-floored NMSE.

## Localization baselines (the loc-side analog of the feedback baselines) — VERIFIED
- **KNN fingerprinting (exp/knn_localization.py)** = standard distance-weighted KNN regression
  (w=1/dist) on standardized angle-delay CSI (real|imag|mag) via cKDTree, + an "oracle
  nearest-in-space" floor (best a perfect CSI-fingerprint could reach). = the FLnet loc
  baseline. ✓
- **Classical AoA/ToA (exp/classical_loc_baseline.py) — all textbook:**
  · DoA = **Bartlett/conventional beamformer** argmax over a world-direction grid (P=|XᴴS|²).
    CORRECT choice (single snapshot = strongest delay tap → rank-1 cov → MUSIC inapplicable;
    Bartlett is the right single-snapshot DoA estimator, Van Trees Optimum Array Processing).
  · **Exact Sionna UPA array manifold** (element positions Rz(az)Ry(el), λ/2; verified vs
    scene.tx_array.positions; LOS median ~0.7°), front-hemisphere restriction resolves the
    planar-array front/back ambiguity. ✓
  · single-gNB: bearing ray ∩ UE-height plane; multi-gNB: **LS ray-intersection triangulation**
    (Σ(I−ddᵀ) closest-point) — textbook. ✓
  · ToA: range=c·τ with finite-BW quantization (bin c/BW) + timing noise; **linear-LS
    trilateration**; correctly flags the COLLINEAR-anchor GDOP degeneracy. ✓
  · **CRLB** = sqrt(trace(inv FIM)), Jacobians az=(1/d)[−sφ,cφ], el=(−dz/r²)[cφ,sφ],
    range=(d/r)[cφ,sφ] (the d/r fix already applied, [[classical-loc-baseline]]); LOS-only
    (NLOS violates unbiasedness → CRLB doesn't bound it = formal NLOS-break reason, 2502.19354);
    robust-MAD sensor σ. ✓
- Lower-priority STANDARD items (underpin negative/secondary results, spot-verify on request):
  LocHead random Fourier features = Tancik 2020 / Rahimi-Recht 2007 (already in docstring);
  temporal_tracking = CV Kalman + RTS smoother + Cressie variogram.
- ⚠️ charting_loss / triplet_charting_loss = NOT channel charting — see dedicated section below.

## Channel charting faithfulness (multitask_train.py vs Studer 1807.05247 + Ferrand 2005.12242) — UNFAITHFUL, found 2026-06-20
Read BOTH founding papers in full (+ UNILocPro 2510.27394 secondary). VERDICT: the "channel charting"
in the code is SUPERVISED METRIC LEARNING, not CC — the loss ALGEBRA is faithful but the SUPERVISION
SIGNAL is inverted. CC's DEFINING property is label-free: Studer §II-B "learn the chart solely from
channel features WITHOUT using the true spatial locations"; Ferrand abstract "self-supervised … without
any knowledge of the user location", triplets ordered by TIMESTAMP proximity ("weak supervision").
- `charting_loss(emb, xy_norm)` = `(‖f(x_i)−f(x_j)‖ − d_ij)²` — matches Sammon/Siamese form (Studer eq.5,
  Ferrand C_s eq.7) EXACTLY, but d_ij must be a CSI-FEATURE distance; code uses `pdist(xy)` = TRUE spatial.
- `triplet_charting_loss(emb, xy_norm)` = `(d(a,p)−d(a,n)+M)⁺` — matches Ferrand margin cost (eq.12)
  EXACTLY, but pos/neg must be mined by TIMESTAMP; code mines by true `d_xy`.
- Also SKIPS CC's feature-extraction stage (Studer §IV: scaled angular |R2M|, "most critical step"); runs
  on the supervised loc-head embedding. Evaluated by absolute MAE (m); CC is valid only up to isometry → TW/CT.
- ⇒ What was built and "DROPPED" ([[thesis-roadmap]], [[identifiability-diagnostic]]) is the fully-supervised
  fingerprinting CC is positioned AGAINST (Studer §I-B). The "charting → NEGATIVE" verdict does NOT bear on CC:
  (1) at 84k labels a label-distance aux is redundant with the MSE loss → expected null; (2) a label-based loss
  CANNOT help the held-out geographic block (no labels there) — the real mechanism is TRANSDUCTIVE CSI-dissimilarity
  CC over UNLABELED target channels; (3) CC's actual value, LABEL-EFFICIENCY, was never tested.
- FAITHFUL re-test (cheap, repo already has the primitive): diag_identifiability already computes ρ=|⟨h_i,h_j⟩|
  (Studer's correlation dissimilarity); build D_ij from CSI (1−ρ or angular-|R2M| Frobenius), train label-free
  + transductive over unlabeled target region, anchor with few labels (semi-sup, à la Ferrand/UNILocPro), sweep
  LABEL BUDGET, report TW/CT. CAVEAT: our data is static snapshots (no timestamps) → Ferrand timestamp-triplets
  N/A; Studer CSI-dissimilarity path is the feasible one. HONEST: pure CC is "highly distorted" on absolute MAE
  (UNILocPro) and reaches fingerprinting parity only WITH anchors+map+OT → faithful CC likely won't beat supervised
  loc at 84k labels on MAE, but SHOULD win in the LABEL-SCARCE regime + on TW/CT = a different, legitimate contribution.
  Multi-gNB already won the loc lever, so this matters only if the thesis wants a label-efficiency story.

## Other dropped-negative audits (2026-06-20) — CALIBRATED (not all premature)
Applied the same "was it a faithful test of the method?" lens to the 3 remaining NEGATIVE/DROPPED items
([[thesis-roadmap]]). Verdicts differ — important for honesty:
- **Swin/Transformer "failed to train" = PREMATURE (recipe artifact) — NOW PAPER-GROUNDED (read SwinCFNet 2401.06435
  + AiANet 2504.12440 IN FULL, 2026-06-20).** [[swin-backbone]]: our attempt failed at lr=1e-3 → NMSE flat 2.87 dB;
  + 280 s/ep from eager manual windowed attention. TWO independent primary sources confirm the LR artifact: SwinCFNet
  trains at CONSTANT lr=1e-4; AiANet at AdamW COSINE 1e-4→1e-6, 1000 ep, batch 200 — i.e. 10× lower than our 1e-3.
  BOTH beat CNNs on OUTDOOR CSI (= our Munich regime) at CR=1/4: SwinCFNet NMSE −21.29 dB & AiANet −17.53 vs CsiNet
  −8.75 (AiANet Table V: +3.42 dB over ACRNet indoor, +1.24 dB outdoor). SwinCFNet also uses 32×32 input/window=4 vs our
  64×64 first-stage (the 280s/ep). ⇒ "Swin failed" = our wrong LR + expensive input resolution, NOT Swin-for-CSI.
  Revivable (lr~1e-4 cosine, SDPA, 32×32 stem). Caveat: recon already strong (88% MU-MIMO) → enhancement, not a gap.
- **Staged training (FLnet) = FAITHFUL impl, verify-gap CLOSED (read Guo TWC2024 FLnet firsthand 2026-06-20).**
  FLnet = "Learning-Based Integrated CSI Feedback and Localization" (ON DISK, = the integrated paper). multitask_train.py:464-559
  P1 recon MSE → P2 freeze enc+dec, train loc head on FROZEN codeword (high/same LR) → P3 unfreeze, 0.1×LR joint FT
  (splits 0.4/0.2/0.4) MATCHES FLnet §III-A-3-b EXACTLY, incl. the LR schedule (FLnet: P1 lr1e-3, P2 lr1e-3 "high", P3 lr1e-4=0.1×).
  Faithful. NUANCE (important for framing): FLnet's actual HEADLINE is NOT negative-transfer-recovery — it's joint CODEWORD-based
  loc (f'_Loc: s_i→p_i, eq.12) BEATS sequential RECON-based loc (S-FLnet) at ~no feedback cost (Table III: 0.56 vs 0.82 m MAE @64b).
  We ALREADY adopted FLnet's contribution (loc_source="bottleneck" = codeword loc). Our staged A/B tests a DIFFERENT question
  (does the 3-step recipe rescue our joint-vs-loc-only negative transfer at scale — mostly no): sound for that, faithful to the recipe.
- **Self-aided ISAC = SOUND negative, NOT premature — now PAPER-GROUNDED (read PCEnet 2507.17950 in full firsthand
  2026-06-20).** +0.0% loc / +0.17 dB (multitask_ae.py:228-288: round-1 gated estimate → round-2 of the SAME forward pass).
  PCEnet's PREMISE makes our null EXPECTED: main & side channels are UNCORRELATED (distinct environments); the UE position
  is a BRIDGE that lets a position estimated from the main channel help acquire the UNOBSERVED SIDE channels (Fig.4, Alg.1).
  PCEnet NEVER feeds position back to the SAME channel — "the complete channel cannot be fully inferred from position alone."
  So our self_aided (self-position → SAME channel it was estimated from) is a DEGENERATE same-channel special case that PCEnet's
  own logic predicts is redundant (the codeword already determines that channel) → ZERO new info → correct null. The FAITHFUL
  PCEnet mechanism (position → OTHER anchors' channels) = our MULTI-GNB axis, which WON (−40% p90). Nothing missed; correctly
  scoped. Thesis framing: present self-aided-null + multi-gNB-win together as PCEnet's thesis — position aids CROSS-observation,
  is redundant INTRA-observation. (PCEnet label-free variant §IV-C uses CC relative position = ties to the faithful-CC track.)
  NOW DOUBLY CONFIRMED — read FLnet firsthand 2026-06-20 (§III-B, Tables VIII-IX): FLnet's coarse-position feedback gain comes
  from an EXTERNAL/INDEPENDENT GPS prior (NMSE −10.55→−11.69 dB at p_e=3m; gain LARGER at low bits, +1.39 dB@128 vs +1.14@256;
  fed via HYBRID fusion at enc+dec to avoid the prior being drowned among CSI features — our prior_residual hits the same concern).
  Our self_aided removes exactly the independence (prior self-derived from the same codeword) → zero new info → null is correct.
  The thesis's external_prior mode = the faithful FLnet reproduction. Both PCEnet (cross-channel) + FLnet (external coarse position)
  agree: position aids FEEDBACK only via NEW/independent info.
- META-PATTERN across the buried negatives: declaring a method dead from ONE instantiation, tested at the dense/well-sampled
  operating point where the baseline is already near-ceiling, scored on the MEDIAN not the tail/regime where the method lives.
  Hit charting (wrong method entirely) + Swin (wrong recipe). Did NOT hit self-aided (sound) — calibrated, not blanket.

## Faithful CC re-test (exp/exp_charting_faithful.py, NEW 2026-06-20)
Implements CC faithfully: label-free CSI-correlation dissimilarity d=1−|⟨h_i,h_j⟩| (Studer metric, = diag_identifiability's
ρ primitive), Siamese distance-preservation (Studer SM eq.5 / Ferrand C_s eq.7), TRANSDUCTIVE over train∪held-out-target
channels (no labels), semi-sup anchor alignment (k labels via lstsq), label-budget sweep, TW/CT (Studer §III) + MAE on geo
split. CPU smoke (10k, 2 ep, k=50/100, `--smoke --cpu`) VALIDATES the pipeline + the qualitative structure: charting BEATS
supervised at low k (label-efficiency, as predicted). Smoke ABSOLUTE numbers meaningless (undertrained); real GPU run (80 CC
ep / 120 sup ep) PENDING behind the 512b flow job = the actual answer. Expected: charting > supervised at small k, gap shrinks
as k→all; supervised(all) strong. If confirmed → the label-efficiency contribution charting always should have been tested for.
FIRSTHAND CALIBRATION (read Studer §VI + UNILocPro §VII in FULL 2026-06-20): unsupervised CC achieves TW/CT ≈ 0.84–0.94
(neighborhood preservation), and for NLoS-heavy scenes distance-preservation SM/SM+ BEATS autoencoder charting (Studer Fig 7,
AE struggles on Quadriga-NLoS) → our Siamese distance-preservation faithful-CC is the RIGHT variant for Munich (58% indoor/NLoS).
BUT pure CC gives DISTORTED absolute position (UNILocPro Table II/Fig 8: CC-only 12–15 m vs fingerprinting ~4.5 m) UNLESS anchored
(model-based LoS anchors + OT alignment → 4.17 m = fingerprinting parity, label-free). ⇒ SET THE RE-TEST SUCCESS METRIC RIGHT:
expect faithful CC to win on LABEL-EFFICIENCY + local geometry (TW/CT, low-label MAE-WITH-ANCHORS), NOT to beat full supervision
on raw absolute MAE. exp_charting_faithful.py already does anchor-alignment (lstsq on k labels) + TW/CT, so it's aligned.
RESULT (results/charting_faithful/100k/, geo split, 2026-06-20) — HYPOTHESIS CONFIRMED (direction): faithful label-free CC
BEATS supervised at matched LOW label budgets, gap shrinks with labels: charting vs supervised MAE 103.8 vs 132.1 m (k=50, Δ−28.3),
93.9 vs 123.4 (k=100), ~95-96 vs ~124 (k=200/500), 95.9 vs 110.0 (k=1000, Δ−14); TW/CT 0.77/0.81. ⇒ the "charting NEGATIVE"
WAS mis-scoped — done faithfully it shows the label-efficiency win the supervised-metric-learning version couldn't. CAVEATS (don't
oversell): (1) PROOF-OF-CONCEPT — tiny ChartEncoder on 8k/2k subset → absolute MAE 53-132 m FAR worse than the real CsiNet+ loc
(~16-20 m geo, [[identifiability-diagnostic]]); (2) supervised(all)=53.3 m beats charting(any k) → CC value = label-EFFICIENCY, not
beating full supervision (matches UNILocPro); (3) multi-gNB already won the loc lever → this is a DIFFERENT deployment-cost contribution.
Thesis-grade needs: CsiNet+-backbone encoder, Studer angular-|R2M| feature, OT alignment, vs the REAL supervised loc at matched labels.

## RZF MU-MIMO sum-rate metric (mu_mimo_eval.rzf_sumrate) — FAITHFUL by inspection, but UNTESTED (2026-06-20)
The metric underpinning ALL §4c results (flow, charting-vs-eType, beam_loss). Verified vs textbook RZF: W = Hhat(Hhatᴴ Hhat + αI)⁻¹
= Hᴴ(HHᴴ+αI)⁻¹ (standard regularized-ZF; Hhat = Nt×K user channels); α=K/SNR (standard convention — α=Nt/SNR or exact-MMSE α are
alternatives, not wrong); power-norm ‖W‖_F²=P (total power, noise=1); SINR_k=|h_kᴴ w_k|²/(Σ_{j≠k}|h_kᴴ w_j|²+1) on the TRUE channel
with precoder from RECONSTRUCTED Hhat → rate=Σlog2(1+SINR). All textbook ✓. GAP: test_beamforming_math.py only unit-tests the
SINGLE-USER path (cosine_sim/SE/Parseval), NOT the MU-MIMO RZF → correctness rests on inspection, no test. CHEAP FIX: add a
perfect-CSI→interference-nulls (off-diag Geff→0, sum-rate→interference-free bound) + monotonicity (better recon→higher sum-rate) test.
DONE 2026-06-20: exp/test_mu_mimo_rzf.py ADDED + PASSES — perfect-CSI interf/signal 6e-10 vs random 49; perfect sum-rate scales
+53 over 30→50 dB while imperfect saturates +0.0 (interference-limited signature); monotone in recon quality; perfect ≥ imperfect.

## eType-II Rel-16 (etype2_r16_reconstruct) vs TS 38.214 — FAITHFUL, read §5.2.2.2.1+.3+.5 FIRSTHAND (2026-06-20)
Audit needed THREE sections, not just §5.2.2.2.5 (which delegates): §5.2.2.2.5 (enhanced TII: FD basis, amp/phase tables,
bitmap, precoder), §5.2.2.2.3 (TII: SD beam basis v_{l,m}, orthogonal grouping, n1/n2), §5.2.2.2.1 Table 5.2.2.2.1-2 ((N1,N2)→(O1,O2)).
VERIFIED EXACT vs spec: (a) paramComb Table 5.2.2.2.5-1 (L,pv,β) = _PARAMCOMB ✓; (b) amplitude Table 5.2.2.2.5-2 (k1, 16-level incl
Reserved@0) = _AMP1 ✓ and 5.2.2.2.5-3 (k2, 8-level) = _AMP2 ✓; (c) PHASE = 16-PSK φ=e^{j2πc/16}, c∈{0..15} → code n_phase=16 is
CORRECT (I'd wrongly suspected 8PSK; Rel-15 TII §5.2.2.2.3 is N_PSK∈{4,8}, but the ENHANCED codebook is 16 — code uses the right one);
(d) SD beam v_{l,m} = oversampled-DFT Kron = dft_beam_grid ✓; (e) orthogonal grouping m1=O1·n1+q1, m2=O2·n2+q2 = _ortho_groups EXACT ✓;
(f) O1=O2=4 for all 2D configs (Table 5.2.2.2.1-2) ✓; (g) FD basis y=e^{j2πtn3/N3} + combinatorial C(x,y) ✓; (h) precoder W=Σ v·p1·p2·φ·y ✓.
TWO DOCUMENTED DEVIATIONS (both correct, not bugs): (1) SINGLE-POL adaptation — K0=⌈βLMv⌉ not spec ⌈β·2L·Mv⌉, no 2L pol stacking
(our gNB is single-pol-V); (2) (N1,N2)=(8,8) is BEYOND the standardized configs — spec max is 32 ports = 2N1N2 ⇒ N1N2≤16 (largest 2D
(4,4)/(8,2)/(16,1)); our 64 single-pol elements EXTRAPOLATE the eType-II structure to a larger array (structure generalizes cleanly,
but it's non-standard array size). MINOR SIMPLIFICATIONS (authors flag "faithful-ish overhead"): FD selection is greedy-strongest vs the
exact Minitial-window/i_{1,6,l} signaling; overhead is reported, not exact UCI layout. ⇒ §4c "faithful Rel-16 eType-II" claim JUSTIFIED,
state the single-pol + (8,8)-extrapolation caveats. The codebook math itself is spec-exact.

## Data-gen RT physics (sionna_rt_gen.py) — AUDITED 2026-06-22 (the foundational "never done" audit)
First full physics review of the Sionna RT generator (the basis audit above covered only the angular/delay
TRANSFORM; this covers the RT-SOLVER layer). VERDICT: physically sound; no correctness bugs; a few
modeling caveats to STATE in the thesis. All checks vs first principles + Sionna 2.0.1 RT API.
- **Far-field array (`synthetic_array=True`) VALID — verified.** 8×8 UPA @3.5 GHz: λ=8.57 cm, 0.5λ spacing
  → aperture D≈0.30 m → Fraunhofer 2D²/λ ≈ **2.1 m ≪ r_min=30 m**. Every UE is in the array far field, so
  the synthetic (per-element steering-vector) array response is exact for our geometry. The code comment
  "ok for our aperture" is CORRECT. (Would break only for UEs <~2 m, which the wedge excludes.)
- **CFR→delay IFFT convention = BENIGN.** `np.fft.ifft(h, axis=-1)` is applied to the CFR over
  `subcarrier_frequencies` (Sionna returns BASEBAND-CENTERED freqs, DC at index N/2). Direct ifft of an
  fftshifted spectrum gives `h_delay[n] = g_true[n]·(−1)ⁿ` (circshift-by-N/2 phase) → **per-tap MAGNITUDE
  unchanged** ⇒ energy compaction (93%, self-measured by the didactic dump) and the 64-tap truncation are
  UNAFFECTED, and train/test see the same consistent representation. NOT a bug; cosmetic phase convention.
  (If ever citing absolute tap-delays, ifftshift first; for ρ/sum-rate/loc it is immaterial.)
- **`scattering_coefficient=0.5` is on the HIGH side — acknowledge.** Sionna S∈[0,1]: scattered-field
  amplitude ∝ S, specular ∝ √(1−S²) ⇒ S=0.5 sends **~25% of power to diffuse**, 75% specular. Typical
  urban-building measurements put S≈0.2–0.4, so 0.5 makes the NLOS channel RICHER than average (more diffuse
  multipath). Defensible (Sionna's own default Lambertian; richer NLOS stresses the model harder) but state
  it; a sensitivity sweep on S would be the rigorous follow-up if a reviewer pushes.
- **Subcarrier spacing 97.66 kHz is NON-standard NR (labeling caveat).** 1024 sc over 100 MHz ⇒ SCS=97.66
  kHz, NOT an NR numerology (real 100 MHz @30 kHz = 273 PRB = 3276 sc). It's a FLnet-aligned WIDEBAND CHANNEL
  SAMPLING, not the literal NR resource grid; the CFR is a correctly sampled H(f), delay window
  (1024/100 MHz=10.24 µs) heavily oversamples the 640 ns kept → physics fine, only the word "subcarrier" is
  synthetic. Call them "frequency samples / virtual subcarriers" in the thesis.
- **LOS label (`_los_flags`) = first-path-delay vs geometric delay, tol 2 ns.** 2 ns ⇒ 0.6 m path-length
  tolerance; sound single-snapshot geometric LOS test (first finite +delay ≈ ‖gNB−UE‖/c). Per-(UE,gNB),
  squeezed for single-gNB (legacy-safe). ✓
- **Indoor label (`indoor_flags`) = vertical ray-cast, roof hit within zmax.** Geometric proxy (Mitsuba
  ray_intersect straight up), fine as a coarse indoor/outdoor flag. ✓
- **`normalize_cfr=False` retains absolute path loss = CORRECT** (the localization distance cue; consistent
  with link-budget audit #2 above and the loc-magnitude caveat). ToA saved separately (`save_toa`) without
  touching the delay-normalized CSI. ✓
- **CFR frequency-chunking (`_cfr_chunked`) is EXACT** — each chunk evaluates `paths.cfr` at an independent
  frequency subset, concatenated along the freq axis ⇒ bit-identical to a single call; only bounds the
  Dr.Jit 2³² tensor. The multi-gNB batch/chunk downscaling (output-identical claim) is therefore sound. ✓
- **MINOR: solver `seed` is FIXED per batch** (`seed=cfg.seed` on every `solver()` call). The diffuse-ray
  sampling uses the same PRNG seed each batch, but UE geometry differs per batch (rng advances positions) ⇒
  no path duplication, just reproducible scattering. Not a correctness issue; if a reviewer wants i.i.d.
  diffuse realizations across batches, vary the seed. Low priority.
- **`max_depth=10`** captures multi-bounce + indoor penetration (expensive but intended). Consistent with
  the indoor-UE inclusion goal.
⇒ The data pipeline's RT physics is trustworthy; the only thesis-worthy disclosures are the S=0.5 (rich
NLOS) and the virtual-subcarrier (97.66 kHz) modeling choices, both benign and defensible.

## Flow decoder faithfulness (flow_decoder.py vs 2605.08628) — math VERIFIED, conditioning FIXED 2026-06-20
Straight-line OT path (1−t)src+t·h_clean ✓; target w=h_clean−src ✓; source N(h̄,σ0²I) refiner /
N(0,prior_std²I) direct ✓; CFM loss E‖φθ(h(t),z,t)−w‖² ✓ (eq.4); midpoint ODE (Alg.1) ✓;
Gaussian-Fourier time emb ✓ (eq.5); EMA ✓ (eq.6). Adaptation: 2D-image U-Net (angle×delay) vs their
1D-over-antenna (unitary-equiv).
- **CORRECTION (was UNFAITHFUL, now fixed):** the FEEDBACK conditioning was originally injected ONLY as
  a global FiLM scale/shift (once) — but paper §III-D / Fig 2b requires it CONCATENATED at the input AND
  reintroduced at multiple resolutions in the down path. The global-only version is IGNORED in the
  wideband image (z-shuffle test: identical output, rho 0.016) → recon collapses to a z-independent
  sample (+3 dB). FIXED via `cond_on_hbar` (FlowVectorField cond_img_ch=2): h_bar=D0(z) concatenated at
  input + area-pooled reintroduction at every down-scale → on-manifold (−4.4 dB). See
  [[matched-overhead-classical-vs-dl]] "WIDEBAND ROOT CAUSE / THE FIX".
- **Direct-mode prior scale:** must match the data's per-element std (unit-FROBENIUS CSI → ~0.011 over
  8192 elems), NOT N(0,1) (90× too large → noise swamps signal). exp arg --prior_std 0=auto(per-elem RMS).
