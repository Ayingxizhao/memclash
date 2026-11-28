---
name: references-and-prior-art
description: Key prior art (FLnet benchmark config) + recent SOTA refs (post-Swin) for CSI feedback & ISAC localization
metadata: 
  node_type: memory
  type: reference
  originSessionId: a1f3e29e-2309-4a08-ae16-1784ce6b7621
---

Reference hub for related-work and the benchmark our RT data-gen targets. See [[thesis-project]], [[rt-datagen-progress]], [[swin-backbone]].

## Primary prior art — FLnet (the design we follow)
**Guo, Lv, Wen, Li, Jin, "Learning-Based Integrated CSI Feedback and Localization in Massive MIMO," IEEE TWC vol.23 no.10, Oct 2024.** Codeword-direct localization. Local PDF: `C:\Users\javid\Documents\Javier\CSI\literature\Learning-Based_Integrated_CSI_Feedback_and_Localization_in_Massive_MIMO.pdf`.

Their dataset config (the benchmark to match/beat):
- Tool: DeepMIMO / Wireless InSite. Scenarios O1 (all-LOS 200×40 m street), O1_Blockage (550×35 m, mostly NLOS), O2_Dynamic.
- Carrier 3.5 GHz DL; **bandwidth 100 MHz; 1024 OFDM subcarriers**; #paths capped at 5.
- BS: **6 m** height, **32-antenna ULA**, λ/2 spacing. UE: 1 antenna. Label = 2D [X,Y], fixed height.
- ~181k samples (static), 70/20/10 split. Quantization B=4 bits. Compression γ = 1/128, 1/64, 1/32 (Nbit 64/128/256).
- Localization from the **feedback codeword directly**; loss = ρ·L_CSI + L_Loc (manual ρ). Metric MAE + error CDF.
- Baselines: OMP (CS feedback), KNN fingerprinting (loc). Perfect-CSI loc MAE: 0.15 m (O1 LOS), 2.3 m (dynamic).

**VERIFIED 2026-06-13 (read full PDF) — directly bears on our negative-transfer Finding 2:**
- **Two variants = our `loc_source` switch:** FLnet = loc from codeword (`loc_source="bottleneck"`); S-FLnet = loc from reconstructed CSI (`loc_source="decoder"`), sequential. FLnet beats S-FLnet ~30% on loc AND needs a SMALLER loc head (2·N_cN_t vs 3·N_cN_t) → **confirms our bottleneck choice is correct, not just plausible.** Loc head = 6 FC+ReLU layers, QuanCsiNet (CsiNet-family) backbone.
- **Their negative-transfer fix is STAGED training, NOT gradient surgery:** they explicitly state single-step joint causes "conflicting parameter updates → unsuccessful training" (= our Finding 2). 3 steps: (1) train AE alone MSE LR 1e-3; (2) **freeze encoder**, train loc head on frozen codeword **high LR 1e-3**; (3) **joint fine-tune AE+loc low LR 1e-4**. Weighting = fixed manual ρ swept 200–700 (NOT uncertainty weighting like ours). → adopt this as the must-run baseline; PCGrad/CAGrad becomes the *novel* single-step alternative.
- **Their "joint helps loc 30%" = FLnet vs S-FLnet (codeword-loc vs recon-loc), NOT joint-vs-loc-only.** Different axis → does NOT contradict our Finding 2. They never run a loc-only single-task baseline.
- **Loc results:** LOS O1 N=64 ρ=600: NMSE −7.69 dB, MAE **0.56 m** (S-FLnet 0.82). NLOS-blockage 256b ρ=700: MAE **0.62 m** (KNN-on-perfect-CSI 3.81 m). Dynamic: 1.3–1.5 m. Coarse-GPS-aided (5 m prior fed into enc/dec/loc, hybrid fusion) refines to ~0.6–0.8 m — their headline sub-meter lever, but needs a GPS prior (changes "pure-CSI ISAC" story).
- **Why their 0.5–0.8 m vs our 4.58 m is MOSTLY SCENARIO, not model:** perfect-CSI bound 0.15 m (channel≈bijective w/ position); gridded UEs in 200×40 m; only 5 paths. Ours: random sampling over ~290×500 m, full RT scattering+refraction, 58% indoor, 64-UPA. Our error is reasonable for a much harder problem.

Gap vs our RT config (2026-06-05): we under-sampled bandwidth (~7.2 MHz/20 sc vs their 100 MHz/1024 — fix: n_prbs≈273 @30kHz, contiguous, FFT→delay truncate ~32 taps); 360° box sampling caused directional-antenna bias (~35% yield — fix: orient panel azimuth + ~10° downtilt, sample illuminated sector); Sionna scattering_coefficient defaults to 0 so the diffuse flag is inert (set ≈0.5 + pattern). Deliberate UPGRADES to keep: 64-ant **8×8 UPA** (vs 32 ULA), **27 m macro** BS (vs 6 m), Sionna RT + diffuse, indoor UEs → expect loc errors > their sub-meter. See [[rt-datagen-progress]] for the 5 config changes.

## Position-aided CSI feedback — full PDFs READ + verified 2026-06-19 (literature/)
Directly frame our #1b external-prior finding (see [[self-aided-probabilistic-pareto]]). THREE distinct
mechanisms by which position aids CSI feedback in the literature; NONE contradicts our recon-null result:
- **PCEnet — arXiv 2507.17950**, "DL-based Position-domain Channel Extrapolation for Cell-Free MIMO,"
  Guo, Wen, Li, Jin, 2025 (**SAME group as FLnet**). Cell-free: M BSs (ULA-N), single-ant UE, CPU.
  UE position is a **BRIDGE** between the "main channel" (BS1↔UE, fed back) and the UNCORRELATED
  "side channels" (other BSs). Estimate position from the main channel (NN localization, 3×FC-8N→FC-2),
  share via CPU, use it to design side-channel pilots + reconstruct the side channels. Overhead cut:
  primary two-sided **~50%**, one-sided real-time **~33%**, position-label-free (channel-charting
  RELATIVE position, no labels) **>1/3**. KEY QUOTE: "the complete channel cannot be fully inferred
  from the UE's position alone, [but] key channel characteristics can be derived from it" (angle/path-
  loss, strongest in LOS). **RECONCILES our finding #3 (position doesn't help recon) — NOT a
  contradiction:** PCEnet uses position to reconstruct channels with NO codeword (other BSs); we fed
  position alongside the codeword for the SAME channel → redundant (the codeword already determines it).
  Position's recon value is for UN-observed channels (other anchors/bands/times) = exactly our
  multi-gNB / temporal axes. Its label-free variant ties to our dropped channel-charting ([[thesis-roadmap]]).
- **Zone-Specific CSI Feedback — arXiv 2401.07451**, Zhang & Alkhateeb (ASU), Jan 2024 letter.
  Partition the site into spatial ZONES by UE position; train a per-zone feedback subnetwork; SELECT
  the right one via position (explicit) or CSI (implicit). Within-zone channel variation ≪ whole-site
  → higher CR / better recovery at same model complexity. DeepMIMO Boston5G downtown, 64-elem 16×4 UPA,
  3.5 GHz, 15 multipaths, ~106k channels (24k train), CR 1/64. **8-zone vs 1-zone: ~6 dB mean NMSE gain
  at equal complexity; 50% of UEs < −25 dB NMSE (8-zone) vs 8% (1-zone).** New overhead metrics MPTR/MPUR.
  Position helps recon by MODEL SELECTION (exploits spatial channel clustering), NOT per-sample position
  input → also consistent with our null (different mechanism, closer to spatial fingerprinting).
- **CORRECTION (earlier mis-cite):** arXiv 2402.19434 (Jiang & Alkhateeb, "Digital Twin Aided Massive
  MIMO: CSI Compression and Feedback," ICC 2024) does **NOT** use UE position as side-info — it uses a
  site-specific RT **digital twin** to generate synthetic training data + domain adaptation (orders-of-
  magnitude less real data). Relevant to **cross-scene #6** RT-twin re-instantiation ([[cross-scene-generalization]]),
  not to the position-prior point.
- **FLnet GPS numbers RE-VERIFIED 2026-06-19** (re-downloaded rasterizable PDF; original rendered blank).
  Coarse-position error is UNIFORM `‖p̃−p‖~U(0,pₑ)` (NOT Gaussian). Verified: O1-LOS perfect-CSI loc bound
  0.15 m; FLnet O1 N=64 ρ=600 loc 0.56 m (S-FLnet 0.82); NLOS-blockage 256b 0.62 m; dynamic 1.3–1.5 m.
  GPS-aided loc (Table IX, dynamic, 256b, pₑ=3m): w/o 1.33 m → w/ 0.63 m; CSI refines a 5 m prior to ~1.1 m.
  ***** CRITICAL — FLnet Table VIII CONTRADICTS our #1b finding #3 ("position doesn't help recon"):
  coarse position DOES improve CSI feedback NMSE by ~1.1–1.5 dB (dynamic scenario; No-aid→pₑ=3m:
  256b −10.55→−11.69, 128b −8.05→−9.38, 64b −6.16→−7.50), and the gain GROWS as the bit budget SHRINKS
  ("more significant when reconstruction operates with limited data"). Our recon-null is almost certainly
  an artifact of (1) our HIGH feedback rate (256-dim continuous, η=1/32, unquantized → position redundant
  with a rich codeword; FLnet's trend predicts ~0 gain at high rate), (2) dense-RT scattering+indoor scene
  (position weakly predicts channel; FLnet uses L=5 paths, position→AoD near-deterministic in LOS), and
  (3) our weaker single-step decoder-only zero-init fusion vs FLnet's hybrid enc+dec 3-step fusion.
  RESOLUTION = re-run the external-prior recon axis at LOW bit budget (code_bits 64/128); if position then
  helps recon, the null was a high-rate artifact matching FLnet. SOFTEN finding #3 accordingly (see
  [[self-aided-probabilistic-pareto]]). Companion ICC-2023 precursor PDF also in literature/
  (Integrated_CSI_Feedback_and_Localization_Using_Deep_Learning) — READ 2026-06-19: same FLnet/S-FLnet
  + config (32-ULA, DeepMIMO O1/O1B, L=5 paths, N=2048, LOS 0.56/0.82 m) but has NO coarse-GPS/position-
  aided variant (that is TWC-2024-ONLY -> cite TWC for any GPS-aided claim). Reinforces our #4 overhead-
  Pareto: "limited feedback bits may be used for sensing tasks EXCEPT CSI reconstruction" = loc needs
  fewer bits than recon (our loc-flat-across-budgets).

## Citations resolved from the 2026-06-19 PDF batch (literature/)
- **CsiNet+ (our LOCKED backbone) — STILL MISSING from literature/.** Need: Guo, Wen, Jin, Li, "CNN-Based
  Multiple-Rate Compressive Sensing for Massive MIMO CSI Feedback: Design, Simulation, and Analysis," IEEE
  TWC 19(4):2827-2840, 2020 = arXiv **1906.06007**. (The "Deep_Learning…Time-Varying" PDF is NOT CsiNet+ —
  it is **CsiNet-LSTM**: Wang, Wen, Jin, Li, IEEE WCL 2019; temporal CSI-feedback variant, bonus for Phase-3.)
- **SwinCFNet = arXiv 2401.06435** (Cheng et al., BJTU/ZTE, "Swin Transformer-Based CSI Feedback for Massive
  MIMO," 2024). **AiANet = arXiv 2504.12440** (Lou & Wu, "Attention-Infused Autoencoder for Massive MIMO CSI
  Compression," WCNC 2025; cross-scenario, +3.42 dB vs ACRNet; also cites LASSO/AMP/TVAL3/BM3D-AMP →
  pull CS-baseline refs from here). **TransNet** = Cui/Guo/Song, IEEE WCL 2022 (file present).
- **Classical CS baselines (cite directly, no PDF):** LASSO Tibshirani JRSS-B 1996; TVAL3 Li/Yin/Zhang
  Comput.Optim.Appl. 2013; BM3D-AMP Metzler/Maleki/Baraniuk IEEE TIT 2016. **Variogram** = Cressie,
  "Statistics for Spatial Data," Wiley 1993 (textbook, no PDF). **Positioning survey (optional)** =
  del Peral-Rosado et al., IEEE Comm Surveys & Tutorials 2018 (TS 38.305 + 2502.19354 already cover it).
- **2502.19354 VERIFIED** = "Two-Stage Weighted Projection…" (Dureppagari/Buehrer/Dhillon, ICC-W 2025);
  derives a GENERALIZED CRLB + NLOS-bias model, 3GPP 5G-NR TDOA/TOA cooperative loc → the exact cite for
  [[classical-loc-baseline]]'s "NLOS has no standard CRLB" formal argument.
- **3GPP cluster:** 2206.15132 (Guo, "AI for CSI Feedback Enhancement in 5G-Advanced," 2022 — CSI-specific
  standardization challenges; LIKELY source of the "gain vs two-sided-complexity" caveat — trace the exact
  sentence here before quoting). 2308.05315 (Lin/NVIDIA overview 2023). 2603.14317 VERIFIED = Gao et al.
  Rel-19 status review — does NOT state the complexity caveat in its abstract, so do NOT attribute it there;
  BUT it CORROBORATES cross-scene #6 (pretrain→finetune across datasets beats from-scratch, Transformer
  finetuning generalizes) → citable for [[cross-scene-generalization]]. TR 38.843 (Rel-18 study) present.

## Recent SOTA (post-Swin, lit search 2026-06-09) — the future-work menu
Post-Swin action is generative priors, SSM/Mamba, deep unfolding, channel charting — NOT another attention backbone (reinforces locking CsiNet+, [[swin-backbone]]).
- **Generative/diffusion** (can break deterministic-AE ρ≈0.86 ceiling but heavy gNB decoder): arxiv 2503.03753; 2505.21681 (residual diffusion JSCC); **2605.08628** (channel-geometry-preserving MU-MIMO, closest to ours — Park/Lee/Sohrabi/Andrews, UT Austin/Nokia); 2606.06846 (CsiCoGen, training-free codebook).
  ***** 2605.08628 READ+VERIFIED 2026-06-19 — IMPORTANT for our beamforming deliverable, and CORRECTS a
  prior mis-quote (it is NOT "~2× at half rate"). Actual: BS-side flow-matching generative decoders give
  **up to 2.4× sum-rate vs MSE-based reconstruction** (8-user, 48 b/user, SNR 20 dB, ~89% of full-CSI),
  QuaDRiGa 7 GHz 3GPP UMi. CORE THESIS = **lower NMSE does NOT imply higher MU-MIMO sum-rate**: MSE recon
  is "centroid-like" and fails to preserve the posterior channel GEOMETRY needed for inter-user
  interference suppression (gains largest in interference-limited/spatially-dense regimes). DIRECT
  LIMITATION of our MSE-trained decoder → acknowledge in [[beamforming-eval-deliverable]] (our mu_mimo_eval
  already reports SUM-RATE, the right metric, but the decoder is NMSE-trained → a generative decoder is the
  upside/future-work). [[thesis-roadmap]].
- **Deep unfolding** (learned ISTA/AMP = interpretable CS-OMP, bit-level quant): survey 2502.05952; overview 2206.14383; researchgate 366107580.
- **Efficiency backbones:** SwinLSTM AE 2505.04432; efficient quant net 2405.20068; Mamba-3.
- **Localization beyond supervised fingerprinting:** channel charting (channelcharting.github.io), CSI2Vec 2506.05237, distributed-MIMO 2406.13722, 3D 2512.15399, UNILocPro (geometry+charting hybrid) 2510.27394, CC-in-real-coords 2308.14498. Benchmarks: ISAC 400-AP median **2.17 m** (2504.17173); multi-task loc+blind chan-est p50 **1.62 m(3-tap)→0.89 m(10-tap)** (PMC12251876).
  ***** READ+VERIFIED 2026-06-19 (numbers confirmed, but BOTH are INDOOR WiFi fingerprinting → cite as
  SOTA-scale/directional CONTEXT, NOT quantitative comparisons to our outdoor MU-MIMO RT):
  · **2504.17173** "GLow" (Zhang et al., USTC): 2.17 m median over 436 APs / 5 floors / 25,600 m² real WiFi.
  Uses CONFIDENCE-AWARE loc + spatiotemporal contrastive pretraining → related to our #5 σ-head + temporal.
  · **PMC12251876** (Molina et al., CNAM, Sensors 2025): 1.62→0.89 m (50th pct) for 3→10 CIR taps, indoor
  WiFi/NYUSIM, 2 BS. Corroborates our delay-coverage finding DIRECTIONALLY (more taps→better loc) — not a
  number match. [[localization-analysis]].
  · **UNILocPro 2510.27394** (Zhang/Pan/Keskin/Valkama/Wymeersch, Chalmers/Tampere): frames our DROPPED
  channel-charting negative result — pure CC "yields highly distorted position estimates"; reaches
  fully-supervised-fingerprinting PARITY only by adding model-based geometry anchors + optimal-transport
  map alignment + (coarse) map + timestamps = i.e. NEW INFORMATION. Exactly why our naive in-model
  contrastive charting tested NULL at 100k ([[thesis-roadmap]], [[identifiability-diagnostic]]).
- **Negative-transfer methods (for our joint-ISAC Finding 2):** PCGrad gradient surgery (2001.06782); CAGrad/Nash-MTL; **ForkMerge** (fork branches at diff task-weights, merge best — 2301.12618). CAVEAT from recent MTL analysis: gradient conflict ≠ negative transfer (conflicting aux grads can act as regularization), so PCGrad treats a *symptom* — our transfer looks like a representation/capacity issue (bottleneck shaped for recon), so **staged freeze-fine-tune (FLnet) likely beats gradient surgery; test staging FIRST, reach for PCGrad/ForkMerge only on residual gap.** DL-ISAC survey 2509.06968; real-measurement loc dataset **2211.05527** (sim-to-real future-work target — READ+VERIFIED 2026-06-19: Colpaert et al., KU Leuven; real **64-antenna** MaMIMO testbed, location-labelled CSI via CNC-positioned antennas, ULA/URA/distributed, LTE-TDD, open on IEEE DataPort; 64-ant matches ours → legit sim-to-real target).

## Staged-training experiment (implemented 2026-06-13, queued)
Implemented FLnet 3-step as `train_multitask(training_schedule="staged", staged_splits=(0.4,0.2,0.4), staged_ft_lr_factor=0.1)`: P1 recon-only → P2 freeze encoder+decoder, train loc head on frozen codeword → P3 unfreeze, low-LR joint fine-tune (constant LR per phase, optimizer rebuilt per phase). CPU-verified (phase transitions + freeze + uncertainty in P3). Comparison runner `exp/exp_staged_compare.py` runs loc_only vs joint_single vs joint_staged on one dataset and prints negative-transfer / recovered / residual / %-recovered. Background watcher `exp/_launch_staged_when_free.py` (started bg) waits for the 100k recon job to free the GPU, then runs it on **rt_munich_64ant_100000ue_los15** → `results/staged_compare/` (launcher.log + results.json). 100k joint single-step refs (this session): joint az235 loc 6.28 m / NMSE −8.11 dB; joint los15 loc 5.36 m / NMSE −9.05 dB (Finding 1 holds at 100k; negative-transfer gap ~1.7 m vs loc_best_100k 4.58 m, down from ~7 m at 10k).

**STAGED RESULT (2026-06-14, los15 100k, ckpt `checkpoint/staged_compare/joint_staged.pt`) — FLnet recipe REJECTED for loc:** joint_staged NMSE **−9.52 dB / loc 9.2 m** (p50 7.2, p90 17.1) vs joint_single −9.05/**5.4 m** vs loc_only **3.9 m** vs recon_only −9.57 dB. Staging RECOVERED recon to ~recon-only level (erased the ~0.5 dB joint recon penalty) but **WRECKED loc (+3.8 m vs single-step, +5.3 vs loc-only), uniformly across all conditions** (per `diag_error_breakdown` on the staged ckpt: LOS 7.0/NLOS 9.5, recon uniformly better). **Mechanism:** P1 shapes the encoder purely for recon; P2 freezes it so the loc head can only read a recon-optimal code; P3's low-LR (1e-4) fine-tune can't re-shape the recon-basined encoder. In FLnet's near-bijective scenes (perfect-CSI loc 0.15 m) the recon-code already carries position so freezing is fine; in our dense-NLOS scene **loc-optimal ≠ recon-optimal representation diverge**, so locking recon starves loc. **TAKEAWAY: training schedule is a recon↔loc Pareto knob — staged=recon corner, single-step-uncertainty=balanced (the ISAC operating point), loc-only=loc corner. Single-step joint is the better ISAC point; to lift joint LOC, re-balance TOWARD loc (fixed-λ loc-weight sweep / CAGrad / ForkMerge), NOT staging.** Strong thesis result (FLnet recipe is scene-dependent). See [[localization-analysis]], [[thesis-roadmap]].

**FIXED-λ LOC-WEIGHT SWEEP CONFIRMS THE PARETO (2026-06-14, `exp/exp_loc_weight_sweep.py`, los15 100k, weighting="fixed", loss=λ_rec·l_rec+l_loc, uniform SNR10, seed42 → `results/loc_weight_sweep/`, ckpts `checkpoint/loc_weight_sweep/lrec_*.pt`):** λ_rec **0.1**→ −9.50dB/7.3m ; **0.01**→ −9.37/5.7 ; **0.001**→ −8.58/**4.8m** (p50 3.8, p90 8.8). Smooth dial-able recon↔loc Pareto. **Best joint loc = 4.8 m @ λ_rec=0.001** — beats uncertainty's 5.4 m, approaches loc-only ceiling 3.9 m, at ~1 dB recon cost (−8.58 vs recon-only −9.57). **Staged is Pareto-DOMINATED: fixed λ_rec=0.1 matches its recon (−9.50≈−9.52) with 1.9 m better loc (7.3 vs 9.2)** → staging is just an off-frontier point, not a useful technique here. Uncertainty (−9.05/5.4) sits ON the frontier (good auto default). Thesis framing: ISAC has a one-knob recon↔loc Pareto; pick the operating point (recon-priority λ=0.1, balanced=uncertainty/λ=0.01, loc-priority λ=0.001). Next loc levers to stack on the loc-priority point: B (Fourier head), #5 (probabilistic), CAGrad.
- **3GPP:** Rel-18 standardized AI/ML CSI feedback as a TWO-SIDED model (UE encoder + gNB decoder = our architecture), normative work item for Rel-20. Rel-19 caveat: gain "not sufficient to justify two-sided complexity" + inter-vendor training problem — cite as roadmap motivation AND honest limitation. ATTRIBUTION (fixed 2026-06-19): the pessimistic "gain insufficient" caveat is from researchgate 366043969 / 2603.14317 (still UNVERIFIED — read before quoting). **NOW VERIFIED FIRSTHAND 2026-06-21: TR 38.843 V19 §8 Conclusions state RAN1 reached NO CONSENSUS to recommend AI/ML CSI compression for normative work, reasons = "trade-off between performance and complexity/overhead" + "inter-vendor training collaboration" — cite 38.843 §8 directly. Contrast: §8 RECOMMENDS AI/ML positioning for normative work. See [[3gpp-kpi-targets]].** **2506.21796 is the OPPOSITE — a POSITIVE result, do NOT attribute the caveat to it:** READ+VERIFIED, it is the Qualcomm-Nokia real-life interoperability PoC (Korpi et al.) — first cross-vendor two-sided ML CSI feedback, BEATS a non-ML baseline, and SOLVES the inter-vendor training problem (confidential interoperable enc/dec; one decoder interoperates with multiple encoders). Cite it as evidence two-sided ML feedback is practically feasible. See [[beamforming-eval-deliverable]].
