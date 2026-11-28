---
name: baselines-requirement-and-theory
description: User requires industry+classical baselines; plus the analytical bounds that prove the eType-II & CS-OMP results
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a1f3e29e-2309-4a08-ae16-1784ce6b7621
---

**The user wants every DL method benchmarked against established references, not just ablation-style.** Include the **industry standard** (3GPP Rel-16 enhanced Type-II codebook, spatial+delay) and the **classical baselines** from foundational DL-CSI papers (compressive sensing: LASSO/TVAL3/BM3D-AMP/OMP, as in CsiNet), on the **same held-out test split**, with rate–distortion curves (NMSE vs feedback bits).

**Why:** A thesis-grade evaluation needs credible reference points — reviewers expect comparison to what industry deploys and to the pre-DL state of the art, not just the model's own variants.

**How to apply:** When proposing/evaluating any DL method here, proactively include an industry-standard + classical baseline on the shared split; don't wait to be reminded. Related: [[thesis-project]], [[beamforming-eval-deliverable]].

## Analytical bounds (the rigorous "DL > classical" argument for §4)
Closed-form bounds that the measured ρ (squared cosine similarity, [[beamforming-eval-deliverable]]) matches. Scripts: `src/exp/validate_etype2_capture.py`, `src/exp/validate_cs_sparsity.py` (CPU-only).

- **eType-II ceiling = L-beam capture ratio** η_L = tr(P_L R)/tr(R), P_L = orthogonal projection onto the L strongest oversampled-DFT beams (NOT Σ|bᴴh|² — that double-counts the overcomplete frame, gives η>1). Measured (40k): η_4=0.80, η_8=0.88, η_24=0.99 (rises slowly → channel NOT low-rank in DFT-beam basis). Measured Type-II ρ=0.64 at L=4 = η_4 minus quant+noise penalty (~0.16). ρ ≈ η_L(1−ε_q), ε_q ≈ π²/(3·4^bphase). ρ flat in L while η climbs → codebook recon is quantization-limited, not subspace-limited (could strengthen with LS coeffs).
**CODE-vs-THEORY AUDIT 2026-06-19 — both validators VERIFIED CORRECT.** eType-II: η_L correctly uses
the ORTHOGONAL-PROJECTION capture `tr(P_L R)=tr((B_LᴴB_L)⁻¹ B_LᴴR B_L)` (frame-Gram inverse), NOT the
double-counting Σ|bᴴh|² — the subtle-correct thing; valid upper bound on L-beam MRT gain. CS: best-K-term
error `√(1−topK energy)`, mutual coherence `μ=max off-diag |Gram|` of unit-col Φ, OMP bound `K<(1+1/μ)/2`,
RIP law `M≥CK log(N/K)` — all standard + correctly coded. FRAMING NOTE: the coherence bound is WORST-CASE
(μ=0.25→K≈2, famously pessimistic for random Φ); the OPERATIVE recoverable-K is the RIP one (~60 at M=256).
Thesis must use RIP-60 as operative and label coherence-2 as worst-case (memory already does). No bugs.

- **CS-OMP limit = weak compressibility vs recoverability.** Angle-delay channel needs K90=73, K99=547 coeffs (of N=4096); sorted-decay exponent −0.80 = only weakly compressible. Gaussian Φ mutual coherence μ=0.25 → OMP exact-recovery bound K<(1+1/μ)/2≈2; RIP law M≥CK·log(N/K) → K≈60 recoverable at M=256. Needs 547, recovers ~60 → measured CS ρ=0.52 == best-4-term quality. Equations (MRT/Cauchy-Schwarz, Type-II quant, RIP/coherence/stable-recovery) written up in-session.
