---
name: beamforming-eval-deliverable
description: Planned headline thesis result — downlink beamforming gain from DL-reconstructed CSI vs baselines
metadata: 
  node_type: memory
  type: project
  originSessionId: f4bbcb42-a71c-4faa-ae17-bc15b8ffc247
---

A required **final result** for the thesis: visualize how downlink beamforming at the gNB benefits from more accurate DL CSI reconstruction (vs 3GPP Type-II + classical CS baselines). See [[thesis-project]], [[flnet-reference-config]].

**Evaluation design (gNB 64-ant 8×8 UPA, single-antenna UE → 64-dim DL beamformer):**
- From each reconstruction Ĥ derive MRT/conjugate beamformer ŵ = ĥ*/‖ĥ‖.
- Score it on the TRUE channel: beamforming gain g = |h_trueᴴ ŵ|² / ‖h_true‖² (1.0 = perfect alignment). Equivalent: achievable rate log2(1 + SNR·‖h‖²·g).
- Compare g (and resulting spectral efficiency) for DL recon vs Type-II vs CS, across compression ratios η and SNR. Plot gain/rate vs η (and vs SNR).
- This is the practical payoff narrative: lower NMSE → higher beamforming gain → higher rate, not just abstract reconstruction error.

**Status (2026-06-07):** dataset done (pure-NLOS); to be implemented in the evaluation stage after the multi-task model trains. User also wants a LOS/NLOS comparison eventually, but testing pure-NLOS first.

**DELIVERED (2026-06-08): `src/beamforming_eval.py` + `beamforming_baselines.py`.** Metric = per-subcarrier squared cosine similarity rho = |hᴴĥ|²/(‖h‖²‖ĥ‖²) (= MRT beamforming-gain retention; rho=1 perfect). SE = log2(1+gamma·rho). All transforms unitary so rho computed in angle-delay = antenna-freq. Math validated in `test_beamforming_math.py`.

**HEADLINE RESULT (100k recon-only CsiNet+, eta=1/32, test@10dB feedback, per-subcarrier MRT):**
| method | mean rho | rho dB | SE@10dB | %perfect | overhead |
|---|---|---|---|---|---|
| Perfect CSI | 1.000 | 0.00 | 3.459 | 100% | inf |
| Raw noisy (uncompressed) | 0.889 | -0.51 | 3.305 | 95.5% | full |
| **DL recon** | **0.859** | **-0.66** | **3.251** | **94.0%** | **1/32** |
| eType-II L=4 | 0.637 | -1.96 | 2.808 | 81.2% | 232 b |
| CS-OMP M=256 | 0.517 | -2.86 | 2.522 | 72.9% | 256 |
DL beats classical compressed feedback by ~1.3 dB (eType-II) / ~2.2 dB (CS) and nearly matches uncompressed at 32x compression.

**MU-MIMO sum-rate (`mu_mimo_eval.py`, K=4, RZF, feedback 10dB, @30dB tx SNR, % of perfect):** Perfect 7.81 (100%) | raw 7.15 (92%) | DL 6.87 (88%) | DL 4-bit/1024b 6.82 (87%) | DL 2-bit/512b 6.00 (77%) | eType-II 4.69 (60%) | CS 4.77 (61%). **MU-MIMO AMPLIFIES DL's edge over classical: 94%-vs-81% (single-user SE) -> 88%-vs-60% (MU sum-rate)** because inter-user interference leakage ~ (1-rho). DL codeword quantizes cheaply (4-bit ~= continuous). See [[realistic-impairments-scope]].

**FINAL bs32-keeper re-run (2026-06-15) — THESIS NUMBERS (supersede the older tables above for the writeup).**
On the #5 keeper `checkpoint/auto/joint_nll_decoupled_100k_los15_bs32.pt` (csinet enc256 eta=1/32,
los15 100k, feedback 10dB). Written up as section 4 of `src/results/isac_findings.md`.
- Single-UE MRT (`beamforming_baselines.py`, `results/beamforming/mrt_bs32/`): rho — Perfect 1.00 |
  raw(uncompressed) 0.887(−0.52dB,94→95.5% SE) | **DL 0.867(−0.62dB, 94.3% SE)** | eType-II L=4
  0.711(−1.48dB, 86.1%) | CS-OMP M=256 0.584(−2.33dB, 78.2%). DL p10 rho 0.70 vs Type-II 0.45 / CS
  0.30 — DL's worst-decile (NLOS/indoor) lead is the cleanest tail result.
- MU-MIMO RZF K=4 (`mu_mimo_eval.py`, `results/beamforming/mu_mimo_bs32/`), @30dB tx, %perfect:
  Perfect 7.45(100%) | raw 6.75(90.7%) | **DL 6.56(88.1%)** | DL 4-bit/1024b 6.41(86.1%) | DL
  2-bit/512b 4.75(63.8%) | eType-II 4.71(63.2%) | CS-OMP 4.83(64.8%). DL beats classical compressed
  by ~25pp; DL@4-bit still beats them (overhead-fair); raw is an uncompressed REFERENCE not a baseline
  (at 10dB its noise is mild so it edges DL — flips at low feedback SNR). HEADLINE DELIVERABLE COMPLETE.

**OVERHEAD-MATCHED Pareto (2026-06-15) — #1 audit fix, the RIGOROUS baseline claim.**
`exp/overhead_matched_pareto.py` (10k proxy, K=4, feedback 10dB, RZF; `results/overhead_pareto/matched_10k_snr30/`
@30dB + `matched_10k/` @20dB; written as §4c of isac_findings.md). All methods on ONE bits axis, same test
set + single noisy realization. DL=the 5 QAT models of §5 (trained forward, own STE quantizer); eType-II swept
over beams/subbands/amp-phase; CS quantized 4-bit (real bits) + unquant reference. @30dB matched table (%perfect):
~512b DL 75.0 / eType-II 60.5 / CS-4b 36.1; ~1024b 75.5 / 56.8 / 48.2; ~1536b 76.5 / 54.0 / 57.7. KEY: (1) DL
beats eType-II +15–22pp at matched bits — the honest gap, NOT the unmatched +25pp of §4a (which was 8192-bit
continuous DL vs 232-bit eType-II). (2) DL's WORST point (75.0%@512b) > eType-II's BEST (70.9%@68b). (3)
eType-II gets WORSE with more bits (70.9→54.0%) — no denoising, extra beams fit the 10dB noise; CS needs 4096b
to reach 79.7% and only rivals DL unquantized (non-physical). 10k-proxy validity: eType-II@232b=64.8% here vs
63.2% on 100k. So the matched comparison both CONFIRMS and tempers the headline.

**CODE-vs-THEORY AUDIT of the ACTUAL baseline implementations (2026-06-19, `beamforming_baselines.py`
— NOTE: the `validate_*.py` scripts only prove the BOUNDS; the algorithms that produce the headline
rho live here).** CS-OMP (`omp_complex`/`cs_reconstruct`): textbook OMP (argmax|Φᴴr| selection, full
active-set LS, residual update) — CORRECT; fairness caveat = M=256 COMPLEX (512 real DOF) UNQUANTIZED →
generous to CS (still loses to DL; honest bit-matched comparison is §4c). eType-II (`etype2_reconstruct`):
**CHECKED vs TS 38.214 §5.2.2.2.5 (read 2026-06-19) — the "Rel-16 enhanced Type-II" LABEL IS WRONG.** The
code is a SIMPLIFIED Rel-15-Type-II-FLAVORED DFT-codebook baseline (oversampled O1=O2=4 grid + top-L beams
by power + per-subband INDEPENDENT amp/phase quant). It implements NONE of the four DEFINING Rel-16 eType-II
mechanisms: (1) FREQUENCY-DOMAIN COMPRESSION (`W=Σᵢvₘ·Σ_f y^(f)·p⁽¹⁾p⁽²⁾φ` over L spatial × Mᵥ FD-DFT basis
vectors — THE defining feature; code does per-subband independent quant, no FD basis); (2) L beams from an
ORTHOGONAL beam GROUP (code: top-L from full grid); (3) NON-UNIFORM dB-spaced amplitude tables 5.2.2.2.5-2/-3
(code: uniform); (4) nonzero-coefficient BITMAP K₀=⌈β·2LMᵥ⌉ (absent). → RELABEL as "simplified Type-II-style
DFT-codebook baseline," NOT eType-II/Rel-16. FAITHFUL Rel-16 eType-II
NOW IMPLEMENTED + TESTED (2026-06-19, `etype2_r16_reconstruct` in beamforming_baselines.py: orthogonal-group
L-beam select, FD-DFT-basis compression to Mv=⌈pv·N3⌉, amplitude Tables 5.2.2.2.5-2/-3, 16-PSK, K0=⌈β·L·Mv⌉
bitmap, paramComb table; single-pol adaptation = drop the 2L pol factor). Smoke-verified (structured 4-beam
channel ρ=0.965, white noise 0.046, orthonormal groups). **RESULT — the effect is METRIC-DEPENDENT (caveat was single-UE-only; my
earlier "refuted/equal" take was PREMATURE for MU-MIMO).** Wired faithful + simplified into both deliverable
scripts; re-ran on the headline 100k los15 single-gNB set w/ bs32 keeper (results/beamforming/{mrt,mu_mimo}_bs32_r16/):
- **Single-UE MRT (ρ, own-channel alignment):** faithful pc6 ρ=**0.690** (−1.61 dB, 236 b) ≈ slightly BELOW
  simplified 0.711 (−1.48 dB, 232 b); DL 0.867 (−0.62). Here faithful ~ simplified.
- **MU-MIMO RZF (% of perfect @30 dB, interference nulling):** faithful pc6 = **74.3%** vs simplified **63.2%**
  (+11 pp!) vs DL **88.1%** vs CS-OMP 64.8%. Faithful is MUCH better — MU-MIMO rewards its clean ORTHOGONAL-beam
  + FD-compressed directional/subspace structure (nulling), which single-UE ρ doesn't see.
**THESIS IMPACT:** the faithful Rel-16 eType-II is the RIGHT baseline; in the MU-MIMO headline it CUTS the
DL-vs-eType-II gap from +25 pp (vs simplified) to **+13.8 pp** (vs faithful) — DL still wins but by less, now
vs a legitimate Rel-16 codebook. So the user's push to make the baseline faithful MATERIALLY changed the number
(MU-MIMO eType-II 63→74%). Report BOTH variants (faithful primary). Still TRUE that single-UE ρ is channel/
sparsity-limited (K99=547/4096; FD compression buys little for alignment) — the metric split IS the finding.

**§4c OVERHEAD-MATCHED upgraded to faithful eType-II (2026-06-20) — REVEALS A CONFOUND, §4c claim now UNSETTLED.**
overhead_matched_pareto.py now sweeps `etype2_r16_reconstruct` (ETYPE2_R16_CFGS, ~90–684 b) alongside the
simplified one + DL QAT. results/overhead_pareto/{matched_10k_r16 @20, matched_10k_snr30_r16 @30}. RESULT
(@30, 10k proxy): faithful eType-II SCALES UP with bits (72%→90.2% @684 b) while simplified DEGRADES
(71%→54%, noise-fitting); at matched ~512–1024 b faithful eType-II **89–90%** BEATS DL QAT **75–76%** and even
DL-cont **80%**. NOT A BUG: single-UE ρ consistent (pc8/N3=64 ρ=**0.889** > raw 0.887 > DL 0.867) — the
faithful eType-II is a strong MODEL-BASED denoiser (projects onto 6 beams×16 delay-taps = 72 coeffs, ~10×
more bit-efficient than DL's continuous codeword, exploits KNOWN DFT array+delay geometry). **CONFOUND:** the
§4c DL QAT models are **10k-TRAINED (weak; DL needs data — 100k keeper ρ=0.867 vs 10k QAT cont ~80% MU-MIMO);
eType-II is data-independent → handicaps DL.** No 100k DL-QAT models exist. ⇒ the old "DL beats eType-II at
matched bits (+15–22 pp)" is NO LONGER SUPPORTED, and the 10k proxy REVERSES it — but the reverse isn't clean
either (10k DL handicap). FAIR resolution needs 100k-trained DL QAT models (multi-hour) OR honest reframe.
Do NOT write either direction in §4c until resolved. DL's defensible wins remain: full-codeword §4a/§4b (88%
MU-MIMO, 100k) + the localization side. The user's push to faithful-ize the baseline materially changed §4c. CS-OMP verified
from KNOWLEDGE only (no OMP paper in literature/; code = correct textbook OMP, cite Tropp-Gilbert 2007). Also verified
CORRECT this audit: UncertaintyWeighting = exact Kendall-2018 (`0.5 e^{-s}L+0.5 s`, s=logσ²), gaussian_nll
= standard diag-Gaussian, RZF `W=Ĥ(ĤᴴĤ+(K/SNR)I)⁻¹` power-normalized = standard MMSE-RZF. See
[[baselines-requirement-and-theory]], [[classical-loc-baseline]] (CRLB Jacobian fix), [[thesis-project]]
(CsiNet+-based qualifier).

**UNIFIED JOINT MODEL capstone (2026-06-09, `joint_best_100k.pt` -> beamforming_eval + mu_mimo_eval, results in `results/beamforming_joint/`):** ONE model + ONE eta=1/32 codeword -> denoised CSI + position. Single-user rho 0.841 (93.1% SE) vs recon-only 0.859 (94.0%); MU-MIMO sum-rate 86.5% of perfect (4-bit 85.3%) vs recon-only 88.0%; loc 6.3m/p50 4.4m. Unified model costs only ~1.5pp MU-MIMO / ~0.9pp single-user vs dedicated recon model, still beats eType-II(60%)/CS(61%) by ~26pp. COMPLETE thesis deliverable: joint ISAC, single codeword, beamforming + localization. See [[localization-analysis]] (joint negative transfer). **DL rho is COMPRESSION/capacity-limited: saturates ~0.86 across feedback SNR 10->20dB** (raw climbs 0.89->0.99) — at LOW SNR DL denoises strongly (0dB: rho 0.48->0.82, +2.3dB). Recon checkpoint `checkpoint/recon_best_100k.pt` (TEST NMSE -8.45 dB). Baselines provably bounded — see [[classical-baseline-theory]] / validate_etype2_capture.py (eta_L beam-capture) + validate_cs_sparsity.py (K99=547 vs ~60 recoverable). Swin upgrade = GO (capacity-limited) — see [[swin-backbone]].
