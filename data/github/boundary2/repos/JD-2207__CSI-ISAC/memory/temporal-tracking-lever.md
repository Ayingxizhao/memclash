---
name: temporal-tracking-lever
description: "Quantified the temporal/tracking loc lever WITHOUT generating trajectory data — Tier-0 error-field variogram + Tier-1 CV Kalman/RTS. Single-anchor tracking is a modest, bias-limited lever in the honest regime (+19% RMS); reinforces multi-gNB. 2026-06-19."
metadata:
  node_type: memory
  type: project
  originSessionId: thesis-writing-prep
---

Cheap proof of whether TEMPORAL information helps localization, done entirely on the EXISTING
static 100k dataset (no Sionna trajectory generation). Answers the Phase-3 mobility question's
*localization* half before committing to the sequential-CSI generator. See [[thesis-roadmap]]
(UE-mobility section), [[identifiability-diagnostic]], [[self-aided-probabilistic-pareto]] (#5
sigma-head), [[localization-analysis]], [[simulation-audit-caveats]] (geo-split = honest floor).

**Core idea:** "does temporal help loc?" reduces to one measurable property of the error field
e_i = pred_i - true_i: are nearby UEs' errors spatially UNCORRELATED (white jitter -> a motion
filter averages them down, temporal helps) or CORRELATED (a smooth bias field -> filtering
passes it through, temporal can't help)? Measurable on static data via the error-field VARIOGRAM.

### Tier-0 — error-field spatial autocorrelation (`exp/diag_error_autocorr.py`)
Replays the 100k GEOGRAPHIC-split held-out test set (honest floor, MAE 19.9 m / p50 12.7 m —
reproduces [[simulation-audit-caveats]] caveat #2 exactly), computes the variogram of the error
VECTOR field gamma(d)=0.5*E||e_i-e_j||^2. Result (`results/temporal/error_autocorr_100k.json`):
- nugget 242 m^2, sill 971 m^2 -> **only 25% of error variance is spatially UNCORRELATED**; the
  other **75% is a smooth bias field with ~37 m correlation length**. IDENTICAL 0.25 ratio in
  LOS and NLOS (structural property of the fingerprint, not multipath).
- Naive white-noise-only temporal ceiling: ~+13% RMS. This UNDERSTATES it (see Tier-1).

### Tier-1 — constant-velocity Kalman + RTS smoother (`exp/temporal_tracking.py`)
Synthesizes CV trajectories by a heading-constrained nearest-neighbour walk over the test point
cloud (a UE visiting sampled positions), runs CV-KF + RTS smoother on the per-snapshot position
estimates; measurement noise R = sigma-head's calibrated sigma when the ckpt is probabilistic
(loc_prob), else constant nugget-derived sigma (11 m). KEY RIGOR FIX: compare achieved reduction
to a population-matched, assumption-free CEILING = per-trajectory linear-in-time fit of the error
(constant + linear-in-k bias is indistinguishable from real position+velocity -> RETAINED by any
CV model; only jitter + nonlinear-along-path bias is removable).

**Two-regime contrast (the deliverable):**
- **Geographic / honest (`geo_geographic.pt`, constant R, `results/temporal/tracking_100k.json`):**
  RTS RMS 21.4 -> 17.3 m (**+19%**, p50 11.3 -> 8.5), EXACTLY the matched CV ceiling 19% (filter is
  optimal). Floor = the smooth along-path bias. Note trajectory subsample raw RMS 21.4 < full-set
  31.2 (the NN-walk favours densely-sampled easier UEs; isolated hard-tail UEs aren't trackable ->
  ~0 gain there). So single-anchor tracking is a MODEST, BIAS-LIMITED lever in the honest regime.
- **Random / optimistic (`auto/joint_nll_decoupled_100k_los15_bs32.pt` = the #5 sigma-head keeper,
  per-sample R, `results/temporal/tracking_sigmahead_random.json`):** RTS RMS 7.3 -> 3.6 m
  (**+51%**, p50 3.7 -> 2.3), matched ceiling 53%. sigma-head EXERCISED: mean sigma 6.3 m vs err
  4.7 m, Pearson(sigma,|err|) +0.33 (calibrated, conservative) -> feeds Kalman R directly. Errors
  here are jitter-dominated (interpolation regime) so tracking HALVES them.

**The contrast IS the insight:** the SAME filter removes +51% of jitter (random/dense-DB regime)
but only +19% in the honest regime — because the honest-floor error is a spatially-correlated
representation-generalization BIAS, not noise. This is independent confirmation of the
[[identifiability-diagnostic]] (loc floor = representation-generalization). Thesis framing:
single-anchor temporal tracking gives a bounded gain (~+19% RMS / p50 -2.8 m on trackable UEs)
but CANNOT remove the bias field; the bias needs NEW INDEPENDENT info -> reinforces multi-gNB
(spatial diversity = decorrelated bias) as THE loc lever, and bounds Phase-3 temporal-loc
expectations. The #5 sigma-head plugs straight into the tracker (the "temporal version of #1").

**SCOPE / honest caveats:** proxies position-estimate SMOOTHING only. Does NOT test (a) Doppler as
a new input feature (sequential CSI carries motion signature the static snapshot lacks — could
attack the bias, untested) or (b) CSI prediction vs FDD feedback-delay / channel aging — both need
the real sequential-CSI generator. Trajectories are synthetic straight CV paths snapped to the
static grid (no real temporal channel correlation/Doppler), standard CV-model-favourable. A
geo-split sigma-head doesn't exist (keeper is random-split); a cheap frozen-logvar finetune of
`geo_geographic.pt` would give sigma-fed tracking in the honest regime if wanted.
