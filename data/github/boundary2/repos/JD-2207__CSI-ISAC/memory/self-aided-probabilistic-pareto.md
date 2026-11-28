---
name: self-aided-probabilistic-pareto
description: "Roadmap #5 probabilistic-sigma keeper (works), #1 self-aided ISAC (negative result), #4 overhead Pareto (done) — durable findings"
metadata: 
  node_type: memory
  type: project
  originSessionId: edfb6c15-36c8-4d37-9f25-d77a35f6a308
---

Consolidated findings for roadmap #5 (probabilistic localization), #1 (self-aided ISAC),
and #4 (overhead Pareto), implemented 2026-06-14/15. (Merged from the old
autonomous-overnight-run + probabilistic-loc-and-overhead-pareto notes; the unattended
GPU-orchestrator mechanics — `_auto_overnight.py`, `_run_chain.py`, PIDs, status sidecars —
are retired and intentionally dropped.) See [[localization-analysis]], [[thesis-roadmap]],
[[references-and-prior-art]], [[beamforming-eval-deliverable]], [[identifiability-diagnostic]].

## #5 probabilistic localization — KEEPER (the σ deliverable)
Opt-in `--loc_loss {mse|nll|nll_decoupled}` (default mse = byte-unchanged). `LocHead.loc_prob`
makes the final layer emit `2*out_dim` (means via out_act + raw log-vars); forward returns
`(mean, logvar)`; `evaluate` reports MAE on the mean + mean σ in meters. **`nll_decoupled`** is
the recommended variant: `l_loc = MSE(mean)` governs the recon↔loc balance while a SEPARATE
`logvar_head` reads the feature DETACHED, so σ is a passive calibrated error-estimator that
cannot reshape the representation (gradient-isolation verified: pure-σ loss → encoder/mean-mlp
grad 0, logvar-head ≠0). Avoids the raw-NLL scale collapse (coupled NLL @ λ_rec=0.001 dumped
recon to −2.5 dB because NLL's large magnitude swamped 0.001·l_rec).

**CONFIRMED keeper (bs32/120ep, ckpt `checkpoint/auto/joint_nll_decoupled_100k_los15_bs32.pt`,
csinet enc256 eta=1/32, los15 100k):** TEST NMSE **−8.56 dB / loc MAE 4.7 m** (p50 3.7, p90 8.6)
= matches the plain-MSE λ_rec=0.001 point → **the decoupled σ head is FREE.** σ-vs-error
Pearson +0.33 / Spearman +0.34, mean σ 6.3 m vs err 4.7 m (conservative), condition-aware the
right way (σ LOS 6.1<NLOS 6.3; outdoor 6.2<indoor 6.4). This is the bankable #5 result; it is
also the headline-deliverable checkpoint used in [[beamforming-eval-deliverable]] §4.

## #1 self-aided ISAC (GPS-free closed loop) — NEGATIVE RESULT (defensible)
> **CODE REMOVED 2026-07-11 (scope-limiting).** The `self_aided` branch was deleted from `multitask_ae.py`
> (`_forward_self_aided`, gate, params), `multitask_train.py`, `beamforming_eval.py`, `exp/isac_frontier.py`;
> `exp/diag_self_aided.py` + `exp/_run_chain.py` deleted. `external_prior` (#1b, POSITIVE) is UNTOUCHED and
> keeps the shared `prior_fuse`/`prior_dim` machinery. Rationale: the negative result below was predictable
> a priori (self-derived prior is information-theoretically redundant with the codeword) and added conceptual
> surface for no gain. The result is retained here + in the thesis narrative as the motivation for why
> `external_prior` must use INDEPENDENT info. Old `--self_aided` checkpoints can no longer be reconstructed by
> the loaders (they'd build a plain model → state_dict mismatch); they live only as the negative-run artifacts.

Opt-in `--self_aided` (forces nll_decoupled, task=joint, loc_source=bottleneck). Round-1 estimates
(μ1,σ1) with no prior → confidence gate g=exp(−(σ1/gate_scale)²) pulls the prior to scene-centre
when uncertain → prior=[g·μ1+(1−g)·0.5, g] fed into BOTH decoder (residual `prior_fuse`, zero-init
so round-2==round-1 at start) and loc head (`prior_dim=3`) → refined round-2. `diag_self_aided.py`
reports round-1→round-2 loc+recon CDFs and σ calibration.

**Verdict (budget-matched internal test): the closed loop does essentially nothing.**
round-1→round-2 LOC +0.0%, RECON +0.17 dB. **Mechanism:** the fed-back prior is DERIVED from the
codeword z and fed to heads that already read z → informationally REDUNDANT. FLnet's gain came
from an EXTERNAL (GPS) prior carrying independent info; self-deriving it adds nothing. Honest
negative result — self-aiding needs NEW information: a temporal prior (Phase-3 mobility) or a real
external fix. Don't pursue single-snapshot self-aiding further.

## #1b EXTERNAL prior (the counterpart that CLOSES the #1 story) — 2026-06-19
The honest follow-up to #1: if a SELF-derived prior was redundant, does a GENUINE EXTERNAL coarse
prior (noisy GPS) help? Same fusion architecture, only the prior's INDEPENDENCE changes. NEW code
(all gated behind `external_prior`, default off → baseline + self_aided byte-identical):
`MultiTaskAE(external_prior=True)` reuses the self_aided `prior_fuse` (decoder zero-init residual)
+ `LocHead(prior_dim=3)` but in a SINGLE pass with an externally-supplied prior `[x+ε,y+ε,conf=1]`,
ε~N(0,σ_gps²); `train_multitask(external_prior=, gps_sigma_m=)` builds the prior from the normalized
xy targets (σ meters→normalized via dataset span; eval noise fixed-seed). Runner
`exp/exp_external_prior.py` sweeps σ on a geo-split 10k joint model. `results/external_prior/10k/
external_prior.json` (rt_munich_64ant_10000ue_los15, geo split, 120ep). Smoke-tested forward/backward,
guards, baseline-unchanged.

**RESULT (geo split, loc MAE m | recon dB):**
- control (CSI-only, no prior): 29.4 (p50 21.1, p90 62.7) | −5.66
- σ=0 (oracle): **7.4** | −5.71 · σ=1: 7.3 | −5.69 · σ=5: 13.4 | −5.72 · σ=10: 16.7 | −5.78 ·
  σ=20: 20.5 | −5.66 · σ=50: **26.2** | −5.76   (GPS-only ref = 1.2533·σ: σ20→25.1, σ50→62.7)

**THREE findings (the #1↔#1b contrast is the thesis point):**
1. **EXTERNAL prior HELPS localization at EVERY σ** — even a coarse 50 m prior cuts loc 29.4→26.2 m;
   a perfect prior 29.4→7.4 m (−75%). DIRECT OPPOSITE of self-derived #1 (+0.0%). → the active
   ingredient is the prior's INDEPENDENCE/new information, NOT the fusion architecture (identical here).
   This is the clean close to #1: "GPS-aided ISAC's gain is the externality of the side-info."
2. **Genuine sensor FUSION (fused < BOTH CSI-only AND GPS-only) only when the prior is COARSE**
   (σ≥20 m, i.e. worse than the CSI-only ~29 m): σ=20 fused 20.5 < CSI 29.4 & GPS 25.1; σ=50 fused
   26.2 ≪ GPS 62.7. When the prior is FINE (σ≤10 m) the simple concat-fusion UNDER-uses it — loc
   floors ~7 m even with a PERFECT prior (σ=0→7.4, not ~0) and a sub-7 m prior is degraded. Likely
   mechanism: the prior is 3 of ~259 head-input features → diluted/regularized, not copied (FLnet's
   "hybrid fusion" injects it more aggressively → a residual/passthrough loc-fusion is the fix; future work).
3. **RECON is FLAT across all σ incl. the oracle** (−5.66→−5.78 dB ≈ control −5.66) at OUR operating
   point. ⚠️ DO NOT overclaim "position doesn't help recon" as universal — FLnet Table VIII (verified
   2026-06-19, [[references-and-prior-art]]) shows coarse position DOES improve CSI feedback NMSE by
   ~1.1–1.5 dB, growing as the bit budget shrinks. Our null is most likely a (1) HIGH feedback-rate
   artifact (256-dim continuous codeword → position redundant; FLnet's own trend → ~0 gain at high
   rate), (2) dense-RT-scattering+indoor scene (position weakly predicts channel; FLnet L=5 paths,
   LOS-ish), (3) weaker single-step decoder-only fusion. CORRECT framing: "at our high feedback rate
   and dense-scattering scene, an external position prior gives no measurable recon gain — consistent
   with FLnet's finding that the recon benefit shrinks with feedback budget and is largest in sparse/
   LOS channels." RESOLUTION = re-run the recon axis at LOW bit budget (code_bits 64/128); if position
   then helps recon, the null was a high-rate artifact.
   RESOLUTION RAN 2026-06-19 (exp/exp_prior_recon_budget.py, geo 10k, sigma=5 m, FLnet-Table-VIII mirror,
   results/external_prior/recon_budget/recon_budget.json). Delta-recon(prior-noP) by feedback bits:
   256b -0.34 | 512b -0.42 | 1024b -0.89 dB; continuous(earlier) ~0. OUTCOME = REFINED, not cleanly resolved:
   (a) CONFIRMED coarse claim: quantizing the codeword turns ON a nonzero prior->recon gain that is ~0 at the
   high continuous rate -> the original null WAS rate-dependent (FLnet-consistent in DIRECTION). (b) BUT my
   prediction (gain grows as bits drop, a la FLnet) was WRONG: within the quantized range the gain is LARGEST
   at 1024b, SMALLEST at 256b (opposite trend; the script's printed "more negative as bits drop" is a hardcoded
   string, NOT the data). (c) Gain small everywhere (<=0.9 dB) vs FLnet's 1.1-1.5 dB -> our dense-RT-scattering/
   indoor scene makes position a WEAK channel predictor (scene-sparsity leg, likely dominant). (d) CONFOUND:
   prior enters recon via the decoder zero-init residual on the QUANTIZED z; at 256b z is so crushed the
   residual may under-exploit it (same dilution proven on the loc side) -> the shrinking low-bit gain could be
   fusion-mechanism not physics; disentangle via a residual/stronger DECODER fusion. Clean side-results: loc
   gain large + BIT-BUDGET-INSENSITIVE (29->13 m at every budget, reinforces #4); prior@1024b recon -5.61 ~
   continuous -5.66 (position ~compensates for quantization distortion). DEFENSIBLE LINE: "an external position
   prior gives at most a MODEST recon benefit in our scene (<=0.9 dB, only once the codeword is quantized) --
   far below FLnet's sparse-channel gains -- consistent with position being a weak channel predictor in dense
   urban NLOS; whether even this modest gain is scene- or fusion-limited is left open."

PUNCHLINE: #1 (self-derived→null) + #1b (external→loc gain, recon null) ⇒ external positional info
helps LOCALIZATION (new info the codeword lacks) but NOT RECONSTRUCTION (codeword already suffices),
and the loc gain is fusion-style (rescues coarse priors) bounded by the concat-fusion's passthrough.
See [[references-and-prior-art]] (FLnet coarse-GPS variant = the prior art this reproduces/tests),
[[identifiability-diagnostic]], [[thesis-roadmap]].

## #5 σ-head ported to MULTI-gNB (triangle data) — 2026-06-27
Wired the decoupled-σ keeper into `MultiAnchorAE`/`exp/exp_multignb.py` (`--loc_prob`) so ONE
retrain yields the DL accuracy arms + a per-UE σ for the 38.857 §9 Protection Level
([[classical-loc-baseline]], [[spec-scenario-grounding]]). `predict_xy` exports per-UE positional
σ in METERS = sqrt(Σ_coord (exp(0.5·logvar)·span_coord)²), logvar clamped [−20,20] to guard exp()
overflow. **BUG + FIX (the lesson, restating the #5 rule):** first attempt folded the σ-NLL term
INTO `l_loc` before `uw([l_rec, l_loc])` → the detached logvar coupled into the recon↔loc
uncertainty-weighting and **diverged (3gNB σ→inf, PL coverage 0.41–1.0, useless)**. Fix = add it as
a SEPARATE term OUTSIDE uw: `loss = uw([l_rec, l_loc]); if loc_prob: loss += w·gaussian_nll(xy.detach(),
logvar, xy)` — byte-mirrors multitask_train `nll_decoupled` (l.575-608). σ now finite. The
detached-σ-must-stay-outside-the-task-weighting rule is the same gradient-isolation that makes #5
free; folding it in re-couples it. Point estimates were ~unaffected (MSE-trained mean) so the
accuracy arms from the buggy run were still valid, but a clean retrain was run for a calibrated PL.

## #4 feedback-overhead Pareto — DONE (10k proxy)
`exp/exp_overhead_pareto.py`, 5 quantization-aware points, bs32/120ep, `results/overhead_pareto/10k_los15/`
(written as §5 of isac_findings.md). (1) Bit-depth barely matters once quantized: 2-bit ≈ 6-bit
(−4.47 vs −4.87 dB; 77 vs 79% sum-rate); the cost is quantizing at all. **512 b/UE is the Pareto
knee** (3× overhead cut vs 6-bit for ~2 pp). (2) QAT 2-bit holds 77% where post-hoc 2-bit collapses
to 64% — training the codeword to survive its quantizer recovers the loss. (3) loc MAE FLAT 17–18 m
across all bit budgets → localization rides on the feedback at ~zero marginal overhead (loc is
representation-bounded, not bit-bounded — cf [[identifiability-diagnostic]]). (The separate
overhead-MATCHED baseline Pareto, §4c, lives in [[beamforming-eval-deliverable]].)

## Lessons (keep)
- **Match the training budget for any comparison.** My early 100k self-aided/#5 runs used bs512/80ep
  vs the λ-sweep's bs32/120ep (~24× fewer gradient updates) → undertrained (−5.8 dB/7.9 m) and not
  comparable; re-running at bs32/120ep gave the real −8.56/4.7. Don't pick bs512 "for speed" without
  LR scaling.
- σ-CALIBRATION TOOL (rebuilt 2026-07-11): `exp/diag_sigma_calibration.py` replaces the deleted
  `diag_self_aided.py` — panels B (predicted σ vs actual RMS error, binned, +Pearson/Spearman +calibration
  error), C (σ & error by LOS/NLOS + indoor/outdoor), D (σ & error vs path gain 20·log_mag); self-aided panel A
  dropped. Rejects non-probabilistic ckpts. Smoke-tested on `joint_nll_decoupled_100k_los15` (n=9968, SNR 10 dB):
  loc p50 6.1 m, mean σ 7.4 m, Pearson 0.32/Spearman 0.33, binned |σ−rms_err| 2.97 m, monotone B-curve, NLOS σ>LOS,
  σ↑ as path-gain↓ (calibrated). Outputs `results/sigma_calibration/diag_sigma_calibration.{png,json}`. Run on GPU.
- self_aided `gate_scale=0.15` (normalized units) was too large vs the trained σ (g≈1 always, no
  gating); ~0.02 if revisited.
