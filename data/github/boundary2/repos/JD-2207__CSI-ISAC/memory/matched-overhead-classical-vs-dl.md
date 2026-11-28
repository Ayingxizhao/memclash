---
name: matched-overhead-classical-vs-dl
description: "§4c thesis arc — faithful Rel-16 eType-II matches/beats MSE-DL on matched-overhead MU-MIMO sum-rate; why; what fixes it. Q&A for the thesis discussion."
metadata:
  node_type: memory
  type: project
  originSessionId: f0239455-53ee-4944-9e40-57c637969c4f
---

The full §4c story for the thesis discussion: the matched-overhead MU-MIMO comparison,
why a faithful codebook is so strong, and what (does/doesn't) let DL compete. The user
will EXPLAIN this in the thesis, so keep numbers + framing current as results land.
See [[beamforming-eval-deliverable]] (§4a/§4b/§4c numbers + faithful eType-II build),
[[references-and-prior-art]] (papers), [[self-aided-probabilistic-pareto]].

## THE DISCOVERY (the thing to explain)
At MATCHED feedback overhead and on MU-MIMO RZF **sum-rate** (not NMSE), a FAITHFUL
Rel-16 eType-II (`etype2_r16_reconstruct`, TS 38.214 §5.2.2.2.5) MATCHES/BEATS our
MSE-trained CsiNet+-based DL. 10k proxy, feedback 10 dB, rate @ 30 dB, K=4:
- faithful eType-II 684 b = **90.2%** of perfect; 526 b = 88–89%; 236 b = 75%.
- DL QAT matched (512–1536 b) = **73–76%** (FLAT in bits — learned code saturates,
  the §5 "2-bit≈6-bit" capacity limit); DL continuous 10k ≈ 80%.
- single-UE ρ: eType-II 0.889 > raw 0.887 > **DL 0.867** (even unquantized 8192-b DL trails).
- context: §4a 100k full-codeword MSE-DL = 88% MU-MIMO but at 8192 b (UNMATCHED).
The §4a/§4b "DL wins" was 8192-b continuous DL vs 236-b eType-II — an overhead gap, not a win.

## THE VERDICT IS CHANNEL-DEPENDENT — CDL reverses it (2026-07-02, NEW, important refinement)
The "eType-II ≥ MSE-DL at matched overhead" discovery is NOT universal — it is contingent on the channel
being spatially SPARSE (Munich-like). On the stochastic 38.901 **CDL** channel the result REVERSES: at
MATCHED overhead (AI 256b vs eType-II 236b) the AI beats eType-II decisively — CDL-B SGCS 0.724 vs 0.425,
SE 69.4% vs 39.2%; CDL-C 0.852 vs 0.594, 79.9% vs 49.3% (results/cdl/{B,C}_matched, K=8 @30dB). Mechanism
(verified, see [[38843-csi-alignment]] CDL section): eType-II is a beam-SELECTION codebook, efficient only
when the channel is spatially sparse (few dominant beams). Munich NLOS eff spatial rank 2.2 → eType-II's
low-rank beam basis parameterizes it near-losslessly → competitive/superior at matched bits. CDL-B eff rank
**5.4** (23 dense clusters, spatially RICH) → eType-II's few beams structurally cap out even at equal bits →
the AI's learned DELAY-domain compression wins. ⇒ thesis framing: the classical-vs-DL matched-overhead
verdict depends on the channel's spatial richness — eType-II wins on sparse (macro-NLOS Munich), DL wins on
rich (dense-cluster CDL). Caveat: eType-II param_comb=6 not swept (gap too large for a config tweak). NOTE:
CDL is recon-only (no loc); AI arm = explicit:nmse (Option-2b, MSE), so this is the SAME MSE-DL that loses
on Munich — the flip is purely the channel, not a better decoder.

## WHY (this is NOT "classical beats DL" — it is a boundary condition, 3 legs)
1. **Metric: NMSE ↛ sum-rate (Park, Lee, Sohrabi, Andrews, arXiv 2605.08628).** Verbatim:
   "lower normalized NMSE does not necessarily imply better sum-rate"; MMSE/MSE recon =
   "centroid-like compromises that fail to preserve the posterior geometry needed for
   inter-user interference suppression … fail to maintain user orthogonality"; gap
   "especially pronounced in interference-limited and spatially dense regimes." CsiNet+
   is EXPLICITLY MSE-trained (verified p9, 1906.06007). So our decoder is the exact
   "MSE-oriented deterministic baseline" the paper shows is suboptimal for precoding.
2. **eType-II ≠ CS, and it is PRECODER-oriented by design.** Type-II feeds back an
   implicit PMI = quantized dominant eigenvector(s) = the precoding subspace; CsiNet
   reconstructs the explicit full channel H. They are different 3GPP feedback TYPES.
   → CS (OMP/LASSO) is the apples-to-apples classical baseline for explicit-H (and DL
   DOES beat CS — we reproduce it). eType-II is strong on sum-rate BECAUSE it quantizes
   the eigenvector the beamformer uses, while explicit-H DL optimizes full-channel MSE
   (the wrong proxy). The comparison only becomes fair — and only then does the standard
   look strong — when you switch from NMSE-of-H to the downstream precoding metric.
3. **Representation efficiency.** eType-II 684 b (90.2%) ≈ uncompressed raw (90.7%): its
   ~72-coefficient DFT-beam+delay basis parameterizes THIS channel's precoding subspace
   almost losslessly; DL's learned 256-dim code loses ~10 pp to compression. The deficit
   is representation efficiency for the precoding subspace, NOT denoising and NOT the loss.

## WHAT WE RULED OUT / TESTED
- **Confound (the original reason §4c was flagged UNSETTLED):** §4c DL QAT was 10k-trained
  (handicap); eType-II is data-independent. RESOLVED WITHOUT a 100k retrain (Option B),
  because two signals show even un-handicapped DL loses: (a) unquantized 8192-b DL ρ 0.867
  < eType-II 0.889; (b) 100k full-codeword DL MU-MIMO ceiling 88% < eType-II 90% @684 b.
- **(b) Low-feedback-SNR sweep — NO CROSSOVER (refutes my earlier hypothesis).**
  `exp/overhead_matched_pareto.py --feedback_snr {0,3,5} --rate_snr 30`
  (results/overhead_pareto/matched_10k_fb{0,3,5}_r16/). eType-II 684 b stays
  86.8/88.7/89.4% vs DL ~78–80% cont / 73–76% matched across 0→5 dB. eType-II's
  structured low-rank projection is ITSELF a strong denoiser, so DL has no low-SNR refuge.
  ⇒ the deficit is not a high-SNR artifact; it points at the objective/architecture.
- **The loss-fix attempt — NEGATIVE, and it CONFIRMS the mechanism.** Added a
  differentiable precoding-aware loss `mu_mimo_rate_loss` (per-subcarrier RZF sum-rate
  GAP, `multitask_train.py`; flags `beam_loss_weight/beam_snr_db/beam_K/beam_sc_stride`,
  default 0 = baseline byte-identical; numpy-validated to 1e-6). `exp/exp_beam_loss.py`
  trains MSE-only vs NMSE+beam on 10k. RESULT (results/beam_loss/10k_los15/): DL-beam
  **80.2%** ≈ DL-MSE **80.3%** (Δ 0.1 pp at every budget) even though the train beam-gap
  fell 0.536→0.028 (20×, optimized fine). ⇒ a loss change on a DETERMINISTIC decoder
  can't fix geometry collapse: a sum-rate-WEIGHTED conditional mean is still a centroid.
  The collapse is ARCHITECTURAL (point estimate), not the loss → need a GENERATIVE
  posterior decoder (2605.08628's flow-matching = up to 2.4× over MSE).
- **The generative fix — IMPLEMENTED, results PENDING.** `flow_decoder.py` = the paper's
  BS-side **flow-matching refiner** (Section III-B): FlowVectorField (2D-image U-Net over
  angle-delay CSI, FiLM-conditioned on codeword z + Gaussian-Fourier time emb), FlowRefiner
  (conditional flow-matching loss eqs.2-4 + midpoint-ODE inference Alg.1), EMA. Freeze our
  MSE front end (encoder+decoder=D0); learn a flow that transports h_bar=D0(z) → p(h|z);
  deterministic at inference (ε=0) but posterior-GUIDED, not the mean. `exp/exp_flow_decoder.py`
  trains on 10k + evals MU-MIMO vs DL-MSE + eType-II. CAVEAT (sigma0 scale): unit-Frobenius
  CSI (per-elem std ~0.011 over 8192) → perturbation tube sigma0~0.005 (norm ~front-end
  error 0.3-0.5); sigma0=0.1 was wrong (noise-dominated source, train/inference mismatch).
  Run at the 4-bit (matched ~1024 b) operating point where the posterior is broadest (best
  shot for a generative gain; gain shrinks as feedback rate grows / posterior narrows).
  If the deterministic refiner shows no gain → try the DIRECT decoder (Gaussian prior +
  random ε = true posterior SAMPLING, paper Section III-C), which can pick sum-rate-better
  samples.
  - **REFINER RESULT (results/flow_decoder/10k_los15_4b/): NEGATIVE — IDENTITY COLLAPSE.**
    4-bit front end, DL-flow 79.8% ≈ DL-MSE 79.9% (Δ −0.1 pp) vs eType-II 684 b 90.2%. The
    flow-match loss pinned at the σ0² noise floor (~2.5e-5) from epoch ~11 → the deterministic
    refiner (ODE from h_bar, ε=0) just reproduces h_bar (the learned field ≈0 at the h_bar
    start). Confirms the refiner can't escape the centroid either.
  - **DIRECT DECODER (results/flow_decoder/10k_los15_4b_direct/): RUNNING.** Gaussian-prior
    init (mode="direct" in flow_decoder.FlowRefiner) → genuine generative task (loss NON-trivial
    0.20→0.037 in 2 ep, NOT pinned at 0) → samples p(h|z) from noise, no identity collapse.
    HONEST CAVEAT: at 4-bit/1024 b (HIGH feedback rate) the posterior p(h|z) may be NARROW
    (z nearly determines h) → a sample ≈ the mean → limited generative gain; the paper's 2.4×
    was at 48 b/user (low rate, broad posterior). If the direct decoder ALSO doesn't beat
    eType-II, the COMPLETE negative result (loss-fix + refiner + direct decoder) is itself the
    honest thesis conclusion: in our dense-urban HIGH-feedback-rate regime, a faithful codebook's
    structured precoding-subspace efficiency beats MSE-DL on matched-overhead MU-MIMO, and DL's
    value is elsewhere (joint ISAC, scale, low-rate regimes).
  - **DIRECT DECODER RESULT — ⚠️ INVALID TEST, NOT a refutation (corrected 2026-06-20 after
    re-reading 2605.08628 §V).** My direct decoder gave MU-MIMO 37.8% with recon NMSE **+1.8 dB**
    (error>signal = off-manifold garbage). BUT the paper's flow decoder reconstructs at NMSE
    **≈−4.7 dB** (Table II, 48 b) — GOOD, on-manifold. So my generative model is BROKEN/underpowered;
    it fails a step BEFORE the phenomenon they study applies → it is NOT a valid test of the
    generative hypothesis. ODE-step sweep 10→100 flat (not under-integration). DO NOT cite as
    "generative fix fails." RETRACTED.
  - **Why my reproduction was invalid (regime mismatch with the paper):** paper = NARROWBAND
    (h is a 64-dim spatial vector), 32-ant UPA, tiny latent L=8, **16–48 bits/user (BROAD
    posterior)**, 100k realizations, only **N_step=4** ODE steps; their MSE baseline is BAD at
    MU-MIMO (lots of room) and their gains are in SUM-RATE not NMSE (their generative NMSE ≈ MSE
    NMSE). MINE = WIDEBAND 8192-dim angle-delay image (~128× larger generative task), 1024-bit
    NARROW posterior (little room), 10k data, modest 5.9M U-Net. Any one breaks high-dim flow gen.
  - **WHAT STANDS (robust) vs WHAT'S RETRACTED:** STANDS — (1) faithful eType-II ≥ matched-overhead
    MSE-DL on MU-MIMO sum-rate; (2) precoding-aware LOSS on the deterministic decoder ≈ MSE
    (centroid is architectural); (3) flow REFINER ≈ identity = produces h_bar (NMSE −5.9, ON-manifold)
    — interpretable: our narrow high-rate posterior leaves no room to improve an already-good MSE
    estimate (consistent w/ the paper: their refiner helps BECAUSE their MSE baseline is bad +
    posterior broad). RETRACTED — the direct-decoder "negative". The generative route is therefore
    OPEN FUTURE WORK, not "tried and failed". Paper itself hedges: "flow-based decoding is NOT
    guaranteed to improve every feedback cell" (Fig 10b = a flow-failure cell).
  - **DIAGNOSTIC DONE (exp/exp_flow_narrowband.py) — flow_decoder.py is CORRECT; mechanism
    REPRODUCED.** Narrowband (1 subcarrier → 64-dim spatial vector on 8×8 UPA, tiny L=8 latent,
    same FlowRefiner mode="direct" code), 300 ep:
    · K=4, 32 b: MSE 60.2% (NMSE −6.47) | Flow 60.5% (−6.43) — TIE (on-manifold, code works).
    · **K=8, 32 b: MSE 44.9% (−6.47) | Flow 47.1% (−6.42) — FLOW WINS +2.2 pp with WORSE NMSE =
      the paper's exact NMSE↛sum-rate signature, REPRODUCED.**
    · K=8, 16 b (2-bit): MSE 34.4% | Flow 33.1% — flow worse (too coarse/undertrained at 16 b).
    ⇒ (1) my flow code is CORRECT (reconstructs on-manifold, NMSE ≈ MSE, not the wideband +1.8 dB);
    (2) the wideband +1.8 dB garbage was UNDERTRAINING/CAPACITY on a 128×-larger (8192-dim) generative
    task — NOT a bug, NOT a refutation; (3) the generative mechanism is REAL and reproduces in the
    paper's regime (gain grows with K = interference-limited, matching them). Gain is SMALL here
    (+2.2 pp, not their 2.4×) because of scale (10k/modest model vs their 100k).
  - **WIDEBAND ROOT CAUSE FOUND (2026-06-20) — it was NOT capacity/undertraining; it was a MISSING
    CONDITIONING MECHANISM (bug in FlowVectorField).** Scaling the failed wideband direct decoder
    (base 64→128 = 85M, deeper ch_mult, 200 ep, 10k) did NOT help: recon NMSE stayed pinned at EXACTLY
    +3.0 dB (= NMSE ratio 2.0 = recon UNCORRELATED with true h). Diagnostic (exp/_diag_flow_cond.py)
    on the trained ckpt: rho(h_flow,h_true)=0.016 AND **SHUFFLED z gave the SAME output (0.015) ⇒ the
    field was IGNORING z entirely.** Why: my FlowVectorField injected the codeword z ONLY as a global
    FiLM scale/shift (once) — but paper §III-D / Fig 2b says the feedback conditioning must be
    "concatenated with the intermediate state at the input AND reintroduced at multiple resolutions …
    rather than injecting it only once." A single global vector can specify the narrowband 64-px image
    (why narrowband worked, rho≈0.89) but is far too weak to paint the wideband 4096-px angle-delay map
    → the field minimizes the flow-match loss by reading h_clean out of the interpolant h_t (which leaks
    it at large t) and never learns to use z, so at inference from pure noise it produces a generic
    z-independent sample. The earlier faithfulness audit checked the FM math (path/target/loss/ODE/EMA)
    but MISSED that the conditioning injection was unfaithful. ALSO a second, smaller bug: the direct
    prior was N(0,**I**) (per-elem std 1) vs unit-FROBENIUS CSI (per-elem std ~0.011) — a 90× norm
    mismatch that swamps the signal; fixed via prior_std=per-elem data RMS (auto). [scale was a red herring.]
  - **THE FIX — spatial conditioning on h_bar=D0(z) (flow_decoder.py, validated 2026-06-20).** Added
    `cond_on_hbar`: feed the frozen front-end estimate h_bar (the natural "conditioning derived from b"
    in image form) as 2 extra input channels CONCATENATED to h_t at the input AND reintroduced (area-
    pooled) at every down-scale (FlowVectorField cond_img_ch; FlowRefiner cond_on_hbar). Plus auto
    prior_std. RESULT (exp/exp_flow_decoder.py --mode direct --cond_on_hbar, base 64, 60 ep, 10k,
    results/flow_decoder/10k_val_cond/): recon NMSE went +3.0 → **−4.40 dB = ON-MANIFOLD** (was garbage),
    z now used. The wideband generative decoder WORKS. New exp flags: --cond_on_hbar, --prior_std (0=auto),
    --ch_mult, --health_every (prints flow recon NMSE curve — the on-manifold gate). New helper
    exp/train_front_end.py (100k-los15 MSE D0). recon_best_100k.pt is NON-los15 (Jun-8, az 235°) → NOT
    reusable; must train fresh los15 D0.
  - **100k SCALE-UP RESULT @1024b — NEGATIVE (no sum-rate gain), but DIAGNOSTIC (2026-06-20).**
    base=128/ch_mult(1,2,4,8)=85M/30ep/100k, cond_on_hbar, direct, K=8, frozen D0=recon_mse_100k_los15.pt.
    Flow descended +2.91(ep1)→−8.20(ep28), settling ON-manifold but NOT to parity (DL-MSE −9.05).
    results/flow_decoder/100k_los15_4b_cond/: DL-flow **84.0%** < DL-MSE **87.7%** (Δ −3.7pp); recon NMSE
    DL-flow −7.85 < DL-MSE −9.05. WORSE on BOTH axes → NMSE↛sum-rate signature did NOT appear. eType-II
    684b 88.5% still best. Scaling 10k→100k closed most of the NMSE gap (10k −4.40 vs −5.92 → 100k −7.85
    vs −9.05) but the gain never materialized.
  - **KEY DIAGNOSTIC — why 1024b shows no gain: the operating point is NOISE-limited, not RECON-limited.**
    Raw-noisy feedback alone = 87.1% ≈ DL-MSE 87.7% (only 0.6pp apart); the 13pp gap to perfect CSI is the
    **10dB feedback-NOISE floor**, not a compression gap. 1024b quantization is ~lossless vs that noise →
    posterior p(h|z) NARROW → no spread for a generative model to exploit. A generative gain CANNOT appear
    where the MSE conditional-mean is already ~optimal (matches the narrowband finding: gain needs broad
    posterior / bad-MSE regime). So full NMSE parity wouldn't have helped at 1024b either.
  - **LEVER #3 DONE — code_bits=2 (512b) ALSO NEGATIVE → flow-decoder arc COMPLETE (2026-06-20).** Halving bits
    dropped frozen DL-MSE recon NMSE −9.30→−5.75 dB ⇒ quantization (not noise) the bottleneck, posterior genuinely
    broader. RESULT (results/flow_decoder/100k_los15_2b_cond/, K=8): DL-flow **75.1%** < DL-MSE **76.1%** (Δ −1.0pp);
    recon NMSE flow −5.14 < MSE −5.64. STILL worse on BOTH axes, NO signature — even though 512b DL-MSE (76.1%) fell
    BELOW raw-noisy (87.1%), i.e. compression is genuinely lossy here. ⇒ COMPLETE NEGATIVE across loss-fix + refiner +
    direct@1024b + direct@512b: the WIDEBAND generative flow decoder does NOT yield a matched-overhead MU-MIMO sum-rate
    gain in our dense-urban regime, at narrow OR broad posterior. eType-II 684b (88.5%) remains best at both budgets.
    Narrowband K=8 +2.2pp stands as the validated-mechanism proof-of-concept ONLY (real in the paper's regime; does NOT
    transfer to wideband 8192-dim at this scale/model). HONEST §4c CONCLUSION. [outage-resilient ckpt+resume added to exp_flow_decoder.py.]
  - **FINAL §4c POSITION (corrected & validated):** faithful eType-II ≥ matched-overhead MSE-DL on
    MU-MIMO sum-rate (robust); the deficit is the NMSE↛sum-rate geometry-collapse (precoding-aware
    LOSS can't fix it = architectural); the GENERATIVE decoder (2605.08628) is the principled fix, its
    mechanism is VALIDATED in-code (narrowband K=8) AND it now reconstructs on-manifold in WIDEBAND too
    (after the spatial-conditioning fix). Remaining: scale to NMSE parity for the wideband sum-rate gain.
    DL's demonstrated value: joint ISAC, scale, low-rate regimes.

## SUM-RATE vs K SWEEP — §4c result is ROBUST ACROSS THE REALISTIC MULTIPLEXING RANGE (2026-06-21)
NEW exp/sumrate_vs_k.py (wraps mu_mimo_eval, builds each method's recon ONCE, regroups into K-user
co-scheduling groups; pure-numpy RZF on one DL forward pass). recon_mse_100k_los15.pt + 100k los15,
n_eval=4096, feedback 10 dB, rate @ 30 dB. results/sumrate_vs_k/100k_los15/. Answers two things:
- **CAPACITY — how many simultaneous single-antenna UEs the Munich scene supports.** Perfect-CSI
  sum-rate vs K: 3.88(K1)→9.08(K8)→10.30(K16)→10.95(K32)→11.28(K64). Hard cap = 64 (= gNB ports), but
  **useful multiplexing SATURATES at K≈8–16** (K16 = 91% of the K64 ceiling at ¼ the users; per-user
  rate collapses 3.88→0.18 bits/s/Hz over K1→64 = dense-urban channel correlation, not antenna count).
  ⇒ realistic operating point K≈8–16 (matches real 5G-NR ~8–16 MU layers on 64 ports); our §4c K=4/8
  runs were the low-but-legitimate end, NOT unrealistically small. Settles the user's "how many users
  in Munich" question: ≤64 in principle, ~8–16 useful.
- **eType-II ≥ DL HOLDS AT EVERY K, lead slightly WIDENS** (refutes "DL catches up at many users").
  % of perfect @ 30 dB: eType-II 684b 95.5(K1)→88.4(K8)→88.7(K64); DL 1024b 94.9→87.3→87.2; DL 8192b
  95.1→88.0→87.8; DL 512b 89.5→75.4→75.7. Gap eType-II−DL1024b = +0.6→+1.1→+1.5 pp (K1→64) — does NOT
  narrow at high K, slightly widens. eType-II 684b ≥ DL even at 8192b at all K. ⇒ per-RE ordering
  EXTRAPOLATES to the full resource grid; interference-limited (high-K) does NOT rescue MSE-DL (geometry
  collapse holds across K). Settles "does the one-resource-element result extrapolate?" = YES.
- **USER'S INTUITION (DL's compression edge pays off at many users) = RIGHT TARGET, WRONG OPPONENT.**
  True vs CS-OMP (apples-to-apples explicit-H classical), FALSE vs eType-II. DL1024b − CS-OMP2048b =
  +15(K1)→+28(K8)→+34 pp(K64): CS COLLAPSES 79.5→53.0% as K grows while DL holds ~87% — and CS has MORE
  bits (2048>1024) yet loses badly = DL's compression efficiency, amplified in interference-limited K.
  So BOTH true at once: DL crushes the explicit-H classical (more so with K); eType-II (implicit PMI /
  precoding-subspace paradigm) beats DL at matched overhead (slightly more so with K). The cleanest §4c
  one-paragraph framing. Caveats: random K-tuple pairing (no greedy multiuser-diversity scheduler),
  single feedback SNR 10 dB, eType-II subband-granular vs DL per-SC; high-K rows fewer groups (64 @ K64)
  but trend monotone. NOTE config realism CONFIRMED: n_rx=1 single-pol single-antenna UE is the REALISTIC
  handset MU-MIMO case (massive-MIMO gain is at the 64-port gNB); the "many RX" of MU-MIMO = K co-scheduled
  single-antenna UEs, NOT multi-antenna UEs → eType-II's strength here is NOT a config artifact.

## WHY PAPERS BENCHMARK DL vs NON-STANDARD BASELINES (the user's question)
A mix of legitimate + incentive reasons (good thesis related-work point):
- LEGIT: paradigm mismatch (leg 2 above) — for an explicit-H compression paper, CS is the
  right classical counterpart; eType-II needs a downstream metric to compare fairly.
- LEGIT: faithful eType-II is a ~30-page TS 38.214 implementation lift — most "Type-II
  baselines" in the wild are simplified DFT-codebook strawmen (we caught exactly this
  mislabel; see [[beamforming-eval-deliverable]]).
- INERTIA: NMSE is convenient + differentiable + flatters DL (not the deployment metric).
- INCENTIVE: weak baselines inflate gains — 3GPP itself admits it (2206.15132: "most
  existing works … cannot be fairly compared with conventional feedback methods"; Rel-19:
  AI gain "not sufficient to justify two-sided complexity"). Our faithful+matched+sum-rate
  setup IS the fair comparison the field says is usually missing → doing it is a CONTRIBUTION.
- NOT undermining the thesis: DL's real edge is where there's NO codebook competitor —
  aggressive-compression NMSE, site-specific adaptation (Zone-Specific 2401.07451 ≈6 dB),
  scale, and JOINT ISAC/localization (the thesis core), plus the generative-decoder frontier.

## RESOLUTION FOR THE WRITEUP (§4c)
Do NOT claim a matched-overhead recon win over a faithful codebook. Frame §4c as: the
fair comparison shows a faithful Rel-16 eType-II matches/beats MSE-DL on matched-overhead
MU-MIMO sum-rate (the expected NMSE↛sum-rate boundary), robust across feedback SNR, and a
precoding-aware LOSS does not close it (confirming the collapse is architectural). DL's
defensible wins = full-codeword §4a/§4b + localization/joint-ISAC + scale; closing the
matched-overhead sum-rate gap needs a generative/geometry-preserving decoder whose MECHANISM
is validated in-code (narrowband K=8, see above) but whose WIDEBAND scale-up is future work.
