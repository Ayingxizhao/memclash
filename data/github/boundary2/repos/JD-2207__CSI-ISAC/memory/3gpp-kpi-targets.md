---
name: 3gpp-kpi-targets
description: "Firsthand 3GPP KPI targets (positioning 38.857, sensing 22.837, CSI 38.843) for the thesis ISAC frontier — what standards prioritize + the network-efficiency reframe"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 25f850d3-7142-4fb9-948f-c500c3c3dafc
---

3GPP KPI targets read FIRSTHAND from specs in literature/ (2026-06-21) to ground the joint-ISAC
experiment in what standards actually prioritize. See [[matched-overhead-classical-vs-dl]],
[[thesis-roadmap]], [[references-and-prior-art]], [[classical-loc-baseline]].

## Positioning — TR 38.857 V17.0.0 (38857-h00.pdf), §5 (the branch OUR thesis lives in)
- Metric = horizontal & vertical accuracy reported as a **CDF at percentiles 50/67/80/90%** (§5.2),
  headline = **90th percentile**. (Our p50/p90 reporting matches; add p67/p80 for spec-faithfulness.)
- **Rel-17 targets (§5.1):** commercial **H < 1 m @ 90%**, V < 3 m @ 90%; IIoT **H < 0.2 m @ 90%**
  (relaxable < 0.5 m), V < 1 m @ 90%. Latency E2E < 100 ms, PHY < 10 ms.
- **Rel-16 targets (§4, closest to OUTDOOR MACRO = our Munich):** commercial **< 3 m @ 80% indoor /
  < 10 m @ 80% outdoor**. ← the realistic comparator for our scene.
- **§5.2.3.2 NETWORK EFFICIENCY = PRS/SRS resource utilization is a NAMED KPI** (+ §5.2.3.3 device
  efficiency = UE power). THIS IS THE KEY REFRAME (below).
- Reality check (§8.4): even 3GPP's own evals reach sub-meter @ 90% only in high-LOS InF-SH; in
  NLOS-heavy InF-DH **sub-meter @ 90% is NOT achieved** → our dense-urban NLOS errors >1 m are
  CONSISTENT with the standard's own findings, not a method weakness. State this in the thesis.
- These targets ASSUME dedicated DL-PRS/UL-SRS, wide BW, multi-anchor (TDOA/multi-RTT/AoD/AoA),
  mostly LOS/indoor-factory. We position from the COMMS FEEDBACK CODEWORD → don't claim to beat
  <1 m@90%; claim the resource win (below).

## Sensing — TR 22.837 V19.4.0 (22837-j40.pdf) §7.2 Table 7.2-1 (a DIFFERENT ISAC branch)
SA1 ISAC KPI vocabulary: confidence level [%], positioning accuracy (H/V [m]), velocity accuracy
[m/s], sensing resolution (range [m] / velocity [m/s]), max sensing latency [ms], refresh rate [s],
**missed-detection [%]**, **false-alarm [%]**. Representative: object-detection H 0.5–10 m by scenario;
latency 100–60000 ms; refresh 0.1–60 s; missed/FA a few %. BUT every use case = **device-FREE sensing
of PASSIVE objects** (intruders, UAVs, vehicles, pedestrians; radar-like). Our thesis = **device-BASED
positioning** (connected UE located from its feedback) → cite 22.837 for VOCABULARY + to scope our work
in the POSITIONING branch (38.857 metrics), NOT the object-sensing branch (22.837 metrics).

## CSI feedback + AI/ML positioning — TR 38.843 V19.0.0 (38843-j00.pdf, Rel-19) — READ FIRSTHAND §6.1/§6.2.1/§6.4.1
NOTE file is now Rel-19 **j00** (not i00/Rel-18 — user upgraded; verify version!). TR 38.901 IS on disk
(tr_138901v190200p.pdf, Rel-19) — earlier "not on disk" was WRONG.
- **§6.2.1 CSI feedback intermediate KPI = "SGCS and/or NMSE" — BOTH listed (CORRECTION: I earlier said
  "NMSE de-emphasized in the standard's own choice" — WRONG; the spec lists both as co-equal. The NMSE↛sum-rate
  point is from the ACADEMIC paper 2605.08628, NOT a 3GPP de-emphasis. Don't attribute it to 38.843).** Our ρ
  ≈ SGCS (per-layer for rank>1). Intermediate CSI KPI uses target CSI from ideal channel and "equally applies
  to AI/ML AND the baseline codebook" ⇒ our SGCS DL-vs-eType-II is apples-to-apples PER SPEC. Post-proc output
  boundary = "precoding vectors per frequency unit" (spec frames CSI output as eigenvectors → underpins sum-rate).
- **§6.2.1 eventual KPI (verbatim): "Throughput including: average UPT, 5%-ile UE throughput, and CDF of UPT"**
  ⇒ mean + cell-edge + CDF confirmed firsthand. SLS is the baseline method (link-level optional).
- **§6.1 complexity (verbatim): "number of real-value model parameters" and "number of real-value operations"**
  (separately for CSI generation/encoder vs reconstruction/decoder), + FLOPs/TOPs/MACs, model size Mbyte,
  training + LCM complexity, OTA overhead (assistance/data-collection/model-transfer/signalling). First-class.
- **§6.4.1 AI/ML positioning = "Direct AI/ML positioning" (Fig 6.4.1-1): channel measurements TRP0..N-1 → AI/ML
  model → UE location = EXACTLY our architecture** (our codeword = compressed channel measurement; loc head
  outputs location directly). Also "Assisted AI/ML positioning" (model→intermediate measurement, multi/single-TRP).
  Main KPI = **CDF percentiles of HORIZONTAL accuracy: 90% baseline + {50,67,80}% optional**; vertical optional.
  Complexity = #model params + FLOPs. CRITICAL (verbatim): **"Target positioning requirements ... are NOT defined
  for AI/ML-based positioning evaluation"** ⇒ 38.843 sets NO target for AI/ML loc; the <1m@90%/<10m@80% targets are
  38.857 CONVENTIONAL → report CDF + reference 38.857 as CONTEXT, not a target 38.843 imposes. Generalization eval
  = train-on-drops/test-unseen-drop, clutter, sync/timing error, SNR mismatch (maps to our geo-split/cross-scene).

## TR 38.843 framework + use-case mapping (§4, §5.1, §5.3) — read firsthand, OUR WORK MAPS EXACTLY
- **§5.1 CSI sub-use-cases:** primary = "**Spatial-frequency domain CSI compression using two-sided AI model**"
  (pre/post-proc + quant/dequant in scope) = EXACTLY our CsiNet+ angular-delay two-sided AE. Secondary =
  "Time domain CSI prediction using UE-side model" (= our Phase-3 temporal axis). Training collaboration
  Type 1 (joint single-side) / Type 2 (joint NW+UE, over-air DEPRIORITIZED Rel-18) / Type 3 (separate
  sequential NW-first or UE-first). Temporal sub-use Cases 0-5 (Table 5.1-3: UE/NW use of past CSI; present
  vs future slot — Case 0 = standard compression, Cases 3/4 = prediction).
- **§5.3 Positioning sub-use-cases:** "**Direct AI/ML positioning: model output = UE location; e.g.,
  FINGERPRINTING based on channel observation as the input**" = VERBATIM our method (codeword=channel obs →
  loc head → location). vs "AI/ML assisted" (output = LOS/NLOS, timing/angle, likelihood). FIVE cases:
  Case 1 (UE-based, UE-side model), 2a (UE-assisted/LMF-based, UE-side model, assisted), 2b (LMF-side, direct),
  **3a (NG-RAN/gNB-side model, assisted), 3b (LMF-side model, direct)**. OUR architecture = gNB/network-side
  DIRECT positioning from the COMMS CODEWORD → sits between 3a (network-side model) & 3b (direct output);
  novelty = input is the CSI feedback codeword, not dedicated positioning measurements.
- **§4 framework vocabulary** (for thesis framing): collaboration **Level x/y/z** (x none, y signalling no
  model-transfer, z with model-transfer; Table 4.3-1 delivery cases y/z1-z5, z4=known structure, z5=unknown);
  model ID **Type A** (no OTA) / **B1** (UE-init) / **B2** (NW-init); **§4.2.4 scenario/config-specific incl
  SITE-SPECIFIC models** (model generalization vs switching vs update/fine-tune) = legitimizes our site-specific
  Munich + cross-scene fine-tuning; §4.4 functional framework (Data Collection→Training/Management/Inference/
  Storage). Our two-sided CsiNet+ = a Level-y/z two-sided model. §6 intro: eval baseline = TR 38.901 + TR 38.857.
- READING STATUS (38.843 j00 full read in progress): DONE §3.3/§4/§5.1/§5.3/§6.1/§6.2.1/§6.4.1; skim §5.2+§6.3
  (beam mgmt, N/A to us); TODO §6.2.2.19-21 (CSI result summaries), §6.4.2.5-6 (non-ideal labels + loc summary),
  §7.1.2/§7.1.4 (spec impact), §7.2.2/§7.2.4 (protocol), §7.3.2.4 (test enc/dec for 2-sided model), §8 conclusions.

## TR 38.843 §6 RESULT SUMMARIES — 3GPP's own study CORROBORATES BOTH our headline findings (read firsthand)
- **§6.2.2.19 CSI compression — CORROBORATES §4c [[matched-overhead-classical-vs-dl]].** Metrics = SGCS + mean
  UPT + 5% UPT + overhead reduction; benchmark = Rel-16 Type II CB (NMSE + Type-I/R17-TII benchmarks "lack of
  observations"). Headline: "AI/ML CSI compression OUTPERFORMS Rel-16 eType-II CB IN GENERAL (1-on-1 joint,
  generalization Case 1)" — BUT gains MODEST + HIGHLY VARIABLE with NEGATIVE lower bounds: mean-UPT gain
  **0.2~2% (rank1) / −0.3~6% (rank2) / −4~6% (rank4) @ RU≤39%**; 0.1~4% / −0.5~10% / −1.8~12% @ RU40-69%;
  0.23~9% / −0.2~15% / −1~17% @ RU≥70%. ⇒ gains SMALLEST at RANK 1 + LOW LOAD (0.2-2%, some sources negative),
  grow with RU(load)+rank. OUR regime = rank 1 (n_rx=1) → our "eType-II ≥ MSE-DL at matched overhead" is NOT an
  outlier, it's the LOW END of 3GPP's OWN range; the gains 3GPP sees need rank 2/4 (multi-layer UE) + high load,
  which our single-antenna setup lacks. STRONG independent corroboration that eType-II is competitive at rank-1.
- **§6.4.2.6 positioning — CORROBORATES our LOC pillar firsthand.** AI/ML vs RAT-dependent: heavy-NLOS InF-DH
  AI/ML **<1 m @90% vs >15 m conventional** = our "DL loc beats classical which breaks in NLOS"
  ([[classical-loc-baseline]]). Training-data DENSITY→accuracy w/ SATURATION = our data-scaling
  ([[identifiability-diagnostic]]). Fine-tuning/mixed-dataset for cross-scenario = our cross-scene
  ([[cross-scene-generalization]]). Semi-supervised helps w/ limited ideal labels + direct AI/ML robust to label
  std L∈(0,5)m (error ∝ L) = our label-efficiency/charting angle ([[code-vs-literature-audit]] faithful-CC).
  §6.4.2.5: ground-truth labels can come from existing NR-RAT positioning (noisy-label training 3.73→1.72m@90%).
  ⇒ 3GPP independently validates: DL massively beats classical positioning in NLOS; data scales; fine-tune for
  cross-scene; semi-sup for label scarcity. All thesis pillars echoed in the standard's own evaluation.

## TR 38.843 §8 CONCLUSIONS + §7.1.2 spec impact — THE CAPSTONE (read firsthand)
- **§8: AI/ML CSI compression = NO RAN1 CONSENSUS for normative work** — reasons (verbatim): "trade-off between
  performance and complexity/overhead" + "issues related to inter-vendor training collaboration." THIS IS THE
  FIRSTHAND SOURCE for the "gain not sufficient to justify two-sided complexity" caveat that
  [[references-and-prior-art]] flagged UNVERIFIED — now VERIFIED from 38.843's own conclusion (Rel-18 part).
  Rel-19 adds: most SGCS gain achievable w/ <10M-FLOP, <1M-param encoder (bigger models marginal); "study of
  CSI feedback two-sided model is COMPLETE from RAN1 perspective"; recommend Case 0 + spec impacts if pursued.
- **§8: AI/ML POSITIONING = RECOMMENDED to proceed with normative work** — both direct & assisted "significantly
  improve positioning accuracy compared to RAT-dependent methods" (InF-DH/NLOS). Beam mgmt also recommended.
  CSI prediction: study complete, improvement "with increased complexity," no Rel-18 consensus.
- **⇒ 3GPP's OWN bottom line mirrors OUR thesis split EXACTLY: AI/ML value is standardization-worthy for
  POSITIONING but NOT for matched CSI COMPRESSION (complexity/gain trade-off).** = strongest external validation
  of experiment #1's framing (DL wins on positioning/ISAC axis; competitive-not-dominant on CSI sum-rate). Cite
  38.843 §8 as the authoritative source for both halves.
- **§7.1.2 spec impact — the four named output options:** "Option 1a: precoding matrix in spatial-frequency
  domain; **Option 1b: precoding matrix in ANGULAR-DELAY domain projection**"; Option 2a/2b = EXPLICIT CHANNEL
  matrix (spatial-freq / angular-delay). CSI Part 1 (CQI+RI) + Part 2 (generation output). Ground-truth CSI for
  training/monitoring = scalar OR "codebook-based (e-type II like)" quantization. Monitoring KPIs = SGCS
  (intermediate) + throughput/BLER/ACK (eventual). CQI determination options 1a/1b/1c (target/legacy) vs 2a/2b.
  §6.2.2.19 finds **precoding matrix > explicit channel** = the mainstream/stronger spec design.
- **CORRECTION (2026-06-25, verified firsthand against code):** OUR code implements **Option 2b — EXPLICIT
  channel matrix in angular-delay**, NOT Option 1b. `multitask_ae.py decoder(z)` reconstructs the normalized
  channel H (the same object `data_feed` provides) with element-wise NMSE; there is NO eigenvector/precoding
  extraction. An earlier note here WRONGLY said "Option 1b = OUR exact representation" — RETRACTED. This is the
  crux of [[matched-overhead-classical-vs-dl]] sec4c: we compress explicit-H (MSE) while a faithful eType-II feeds
  back a precoding-subspace PMI (Option 1b-style) -> eType-II >= MSE-DL on sum-rate. Quantization (`code_bits`)
  = **Case 2-1** (fixed quantization-aware). RANK-1 nuance: at n_rx=1 the precoder is h*/||h||, so Option 1b/2b
  carry near-identical info; the precoding-vs-explicit gap is mainly a rank>1 effect -> migrating to Option 1b
  (target/loss = per-subband eigenvector + SGCS) is best paired with rank 2/4 (Tier 4). See [[38843-csi-alignment]].
## TS 22.261 V19.12 — positioning service levels + sensing delegation (read firsthand §6.47, §7.3.2.2)
- **§7.3.2.2 Table 7.3.2.2-1: 7 positioning SERVICE LEVELS (at 95% CONFIDENCE — differs from 38.857's
  90th-PERCENTILE).** L1 H10m/V3m/95%/1s; L2 H3m/V3m/99%; L3 H1m/V2m/99%; L4 H1m/V2m/99.9%/15ms; L5 H0.3m/V2m/99%;
  L6 H0.3m/V2m/99.9%/10ms; L7 RELATIVE H0.2m/V0.2m/99%. §7.3.2.3: TTFF<30s(some<10s); velocity<0.5m/s; heading<30°.
  OUR outdoor dense-urban regime ≈ SERVICE LEVEL 1 (10m H) — multi-gNB loc (~10-20m p90) sits around L1.
- **§6.47 "5G wireless sensing service" = DELEGATION STUB → reqs in TS 22.137 (NOT in 22.261, not on disk).
  CORRECTION: my earlier "22.261 Rel-19 sensing service requirements" was WRONG — 22.261 only points to 22.137.**
  Study-phase sensing KPIs I read (22.837 §7.2) cover it; cite 22.137 for normative sensing service reqs. ⇒ last
  memory-only claim now corrected. PROVENANCE COMPLETE for experiment #1 (all metrics/targets firsthand).

- 38.843 FULL READ DONE (core): §3.3/§4/§5.1/§5.3/§6.1/§6.2.1/§6.2.2.19/§6.4.1/§6.4.2.5-6/§7.1.2/§8 read firsthand;
  §6.2.2.1-18 per-source CSI tables + §6.3/§7.1.3 beam-mgmt + §7.2 protocol-detail + §7.3.2.4 test-enc/dec SKIMMED
  (mechanics, not metrics/findings — revisit only if a deployment/testability claim is needed).

## Positioning methods & resource cost — TS 38.305 V19.0.0 (ts_138305v190000p.pdf), read firsthand
Sections read: §4.3.10–4.3.17 (methods), §7.6 (on-demand PRS), §7.13 (integrity), §7.14 (area-specific SRS).
- **Every RAT-dependent method needs DEDICATED reference signals + MULTIPLE anchors:** Multi-RTT/DL-AoD/
  DL-TDOA → DL-PRS at multiple TRPs (§4.3.11–4.3.13); UL-TDOA/UL-AoA → UL-SRS-for-positioning at multiple
  RPs (§4.3.14–4.3.15). NR E-CID (§4.3.10) is the ONLY low-overhead one ("not expected to make additional
  measurements for the sole purpose of positioning") but it's coarse/cell-ID-grade. ⇒ classical arm hitting
  38.857 accuracy is structurally charged DL-PRS + UL-SRS + ≥3 anchors + measurement gaps (UE can't RX data).
- **Resource machinery is spec-defined/chargeable:** §7.6 On-Demand PRS (LMF toggles DL-PRS via NRPPa PRS
  CONFIG REQUEST to TRPs; PRS occupies DL REs = the 38.857 net-efficiency KPI made concrete). §7.14
  Area-specific SRS explicitly = LPHAP (Low Power High Accuracy Positioning) ⇒ standard ACKNOWLEDGES
  UL-SRS-for-positioning costs UE POWER + dedicated UL resources (gNBs reserve SRS across validity area).
- **BONUS — §4.3.17 "DL AI/ML positioning" IS a standardized NR positioning method, but Rel-19 ONLY**
  (verified firsthand doc p.28, ts_138305v190000p; ABSENT from the Rel-16 copy ts_138305v160100p — that's
  why it can look missing if you open the wrong file). VERBATIM: "makes use of the downlink signals received
  from MULTIPLE TPs to determine AI/ML model input at the UE. The UE performs inference using AI/ML model
  with assistance data... clause 8.16." So the STANDARD's AI/ML positioning is (a) UE-BASED inference and
  (b) NOT reference-signal-free — it still needs DL signals from MULTIPLE TPs. ⇒ legitimizes AI/ML
  positioning as recognized (not exotic) AND sharpens OUR contribution: ours = AI/ML loc from the
  CSI-FEEDBACK CODEWORD (zero dedicated positioning RS, single gNB works, network-side inference) vs the
  standard's multi-TP DL-signal UE-based method. [CORRECTION 2026-06-21: earlier I wrote
  "read §4.3.17 firsthand" when I'd only seen the TOC + the §7.13.1 cross-ref — ETSI PDF has a 1-page offset
  so "pages 26-28" returned doc pages 25-27, short of §4.3.17. Now read.]
- **CLAUSE 8.16 + §7.15 READ firsthand (doc p.186-188, p.79) — the PRECISE standardized picture:**
  · Clause 8.16 = "UE-BASED DL AI/ML positioning". §8.16.1 verbatim: "the UE position is inferred as an output
    of the AI/ML model. The inference technique... is UP TO IMPLEMENTATION and BEYOND THE SCOPE of this spec."
    ⇒ 3GPP standardizes only signaling/assistance/reporting, NOT the model. Model INPUT = DL-PRS from MULTIPLE
    TRPs (entire LMF→UE assistance table 8.16.2.1.0-1 is DL-PRS config: PRS IDs, DL-PRS config/BW-agg, TRP
    coords, LOS/NLOS indic, on-demand DL-PRS). So standardized AI/ML positioning is fundamentally DL-PRS-BASED.
    Reporting (8.16.2.2-1) = lat/long/alt + uncertainty shape + Protection Level + Target Integrity Risk.
  · §7.15 "NG-RAN node assisted positioning with gNB-side model" = in Rel-19 ONLY a Positioning Data Collection
    procedure (§7.15.1: gNB-side model "may require GROUND TRUTH LABELS and related data from the LMF and
    measurements from the TRPs") — NOT a complete gNB-side method, just label/data-collection scaffolding.
  · THESIS CONTRIBUTION (now exact): ours = gNB/NETWORK-SIDE AI/ML positioning from the COMMS FEEDBACK CODEWORD
    ⇒ (a) removes the DL-PRS dependency of the standardized UE-based clause-8.16 method, (b) instantiates the
    gNB-side model Rel-19 only scaffolds via §7.15 data collection, (c) σ-head (#5) maps onto the standard's
    Protection-Level/TIR reporting.
- **META (provenance discipline, user-flagged):** for experiment #1 spec grounding is COMPLETE; residual
  uncertainty is in OUR code/data, not the specs → BUILD, don't keep reading (more = diminishing returns).
  Lesson from Rel-16/19 slip = verify VERSION + read the actual CLAUSE BODY at citation time, not the TOC.
  One optional NON-blocking read: TS 38.214 §5.2.2.2 (eType-II codebook) to firsthand-validate the §4c overhead
  bit-count (currently an audit note) — baseline validation, parallel/later, not a gate on the frontier.
- **§7.13 integrity** uses Bound = mean + K·stdDev (Protection Level, Target Integrity Risk, Time-to-Alert)
  = a calibrated-uncertainty bound ⇒ our #5 σ-head could emit a 3GPP-style protection level (integrity KPI
  tie-in; thesis note, not this experiment). [[self-aided-probabilistic-pareto]].

## OUTDOOR CONVENTIONAL BASELINES + LATENCY TABLE + INTEGRITY (firsthand 2026-06-26, 38.855 §8/§9, 38.857 §5.2.3/§8.4/§9)
Read the WHOLE of 38.855 §8 structure + 38.857 §8.4 (user pushed: "only a few clauses useful? skeptical").
Detail in `literature/explainers/38843-positioning-deepdive.md` PART B2. Which evals to read for OUR scene:
**UMi (Scenario 2) = primary** (Munich = UMi-density ISD-200m): 38.855 §8.1.2 DL / §8.2.2 UL / §8.3.2 DL+UL
→ verdicts §8.5.1.2 / §8.5.2.2 / §8.5.3.2. **UMa (Scenario 3) = secondary** (our 27m gNB = UMa height):
§8.1.3/§8.2.3/§8.3.3 → §8.5.x.3. Skip Scenario 1 Indoor-Office.
- **OUTDOOR CONVENTIONAL ACCURACY (the reference our DL-loc + classical baseline compare to, NOT InF <1m):**
  **UMa ≈ 10 m @90%** (Rel-16; ≤1m@90% = ZERO sources, ≤1m@80% outdoor only 1/2); **UMi ≈ 1 m @90% best-case**
  (2/4 sources, NO abs-ToA), breaks WITH abs-ToA/sync. (38.857 §8.4.)
- **★ SYNC/TIMING ERROR BREAKS CLASSICAL (spec's own empirical basis for [[classical-loc-baseline]]):** DL-TDOA
  meets commercial only with NO sync error → **0/6 sources once 50ns sync modeled** (UMi §8.5.1.2, UMa §8.5.1.3);
  UL-TDOA same (0/4). **Multi-cell RTT is SYNC-ROBUST** (round-trip cancels clock bias): UMi Reg 3/3 AND Comm 3/3
  where TDOA collapses (§8.5.3.2). ⇒ **Multi-RTT = the sync-honest classical method to implement (P1)**; TDOA
  cancels only COMMON bias. Timing-error model (38.855 T6.1.1-1 / 38.857 T6-1): truncated Gaussian std T1, trunc
  [−2T1,2T1], T1∈{0,50ns} for network sync; UE/gNB Rx/Tx error per-panel std X(gNB)/Y(UE), [−2Y,2Y].
- **★ DL-TDOA PER-SOURCE DETAIL (38.855 §8.1.2 UMi / §8.1.3 UMa, FR1 — DOWNLINK = our branch; deep-dive PART B2.9).**
  Spec-faithful DL-TDOA config (src[10]): TR38.901, **comb-6 PRS Gold 1-port, 8 sym/occasion, 4 occasions, 7.8dB
  boost, ideal muting, 19 sites, SVD precoding**, meas = Gauss-Newton(regular)/MUSIC/threshold-ToA+CHAN. ACHIEVED
  CDF [m] p50/67/80/90 (the reference our DL-loc compares to): **UMi 100MHz perfect-sync ≈ 1.2/1.6/3.5/9.1
  (regular), 0.82/1.1/1.4/5.6 (threshold-ToA src11); sync-50ns → 12.9/15.6/19.5/25.2 (up to 47@90%). UMa-outdoor
  100MHz perfect ≈ 1.1/1.5/3.5/62.4 (regular, huge NLOS tail), 1.1/2.6/7.3/21.7 (src11); sync-50ns → 12.5/17.4/
  23.1/42.** TWO DOMINANT DRIVERS, firsthand: (1) **bandwidth** — 100MHz≈9m@90% UMi vs 5MHz≈40m@90% → **our 100MHz
  MATCHES spec best-BW** (config match, not just 38.857 carrier); (2) **sync error** — perfect≈9m→50ns≈25-47m@90%.
  Baselines use **19 sites/57 sectors** + often "only LOS path to calc ToA" → our 1-3 near-collinear gNB is far
  less anchored = reinforces hex/3-sector regen; our multi-gNB DL-loc p90~25-37m is COMPETITIVE with spec DL-TDOA
  in the realistic sync/NLOS regime AND spends ZERO PRS vs comb-6/8-sym/4-occ/19-site budget. If P1 adds a faithful
  classical DL-TDOA: mirror that PRS recipe.
- **★ WIDENED across ~14 sources each (DL §8.1.2/8.1.3 + DL+UL §8.3.2/8.3.3) — THREE drivers + the NLOS lever
  (deep-dive PART B2.10).** (1) THREE drivers, not two: bandwidth (100MHz~2-10m vs 5MHz~20-50m@90% UMi), sync
  error (perfect~2-10m→50ns~16-47m@90%), and **★NLOS bias = the SINGLE BIGGEST lever** — raw DL-TDOA has NLOS
  first-path bias even at PERFECT sync ([20] UMi 2.1→6.1m@90%); **NLOS mitigation (BLADE [14], NLOS-path removal)
  collapses it: UMi 61→3.1m@90%, UMa 130→8.6m@90%.** (2) **★ HONEST COMPARATOR = NLOS-MITIGATED classical, NOT
  raw DL-TDOA** — our DL net learns NLOS-robustness implicitly; fair baseline = BLADE-mitigated (~3m UMi / ~9m UMa
  @90%), not the 60-130m raw tail → [[classical-loc-baseline]] should ADD an NLOS-mitigated arm so "DL beats
  classical" is the fair fight. (3) **DL-AoD (angle) ≫ DL-TDOA in urban** (UMi 3.8 vs 8; UMa 9.5 vs 43m@90%) =
  gNB spatial/beam resolution, EXACTLY what our 8×8 UPA+DL net exploits → frame our method as angular/spatial
  FINGERPRINTING (sidesteps sync + NLOS-timing-bias that cripple DL-TDOA). (4) **★ Multi-RTT is SYNC-INVARIANT**
  — source [23] reports IDENTICAL numbers for "Perfect & Realistic Sync" (UMi 100MHz 16.6m@90%), CDF unchanged by
  50ns (round-trip cancels clock bias) ⇒ **Multi-RTT = the sync-honest classical baseline for P1** (DL-TDOA needs
  timing-model + NLOS-mitigation to be fair; Multi-RTT needs neither for sync). E-CID worse (UMi 11.3 / UMa 70.3
  m@90%). Realistic UMa-outdoor DL-TDOA ([23] common-assumptions) = 63m@90% perfect / 65m realistic → our multi-gNB
  DL-loc p90~25-37m BEATS realistic DL-TDOA in UMa at ZERO PRS.
- **★ LATENCY COMPONENT TABLE (38.857 Table 5.2.3.1.2-1) — feeds P2 analytical latency module (no ns-3):**
  T_DL-Meas **88.5 ms** (min DL-PRS measurement), T_UL-Meas **12 ms** (SRS), T_LMF-Calc **2–30 ms**; processing
  UE RRC/LPP 2–20 ms, gNB/AMF/LMF 3 ms; signalling UE-gNB 0–0.5, gNB-AMF 3–10, AMF-LMF 1–10. **DL-ISAC reframe:
  positions from the already-sent codeword → NO DL-PRS phase → saves the dominant 88.5 ms** = latency Pareto win
  on top of the zero-RS-overhead win. PHY-latency facts (§8.4): DL-TDOA/AoD >10ms (11/11); Multi-RTT >10ms (6/6).
- **★ POSITIONING INTEGRITY / PROTECTION LEVEL (38.857 §9.1.1) = formal home of #5 σ-head.** "Accuracy alone
  insufficient — the 5% tail is unbounded (10s-100s m)." KPIs: **TIR** (Target Integrity Risk = P[error>AL w/o
  warning within TTA]), **AL** (Alert Limit, HAL/VAL), **TTA** (Time-to-Alert), **Integrity Availability** (% time
  PL<AL). **Protection Level (PL) = real-time statistical UPPER BOUND on positioning error** at TIR confidence;
  equation IMPLEMENTATION-DEFINED (just satisfy Prob[(PE>AL)&(PL≤AL) for>TTA]<TIR). ⇒ **our calibrated decoupled-σ
  head output IS a Protection-Level estimate** ([[self-aided-probabilistic-pareto]]) — grounds #5 in spec PL/TIR/
  AL/TTA vocabulary, and §9's "accuracy-alone-insufficient" IS the motivation for it. (Fuller than the 38.305 §7.13
  Bound=mean+K·std note above.) NLOS coping (§8.4/§9.4): LOS/NLOS-ID + outlier-rejection + triangle-inequality all
  improve accuracy; §9.4.3 multipath-from-single-BS justifies our single-gNB DL loc.

## THE REFRAME → the standards-grounded "DL ahead of everything" (drives experiment #1)
Network efficiency (positioning resource utilization) being a NAMED 38.857 KPI is the lever: DL-ISAC
positions the UE from the CSI feedback codeword it ALREADY sends → **ZERO dedicated PRS/SRS positioning
resources.** Classical positioning that meets 38.857 accuracy must spend dedicated PRS/SRS + anchors;
eType-II provides NO positioning. ⇒ on 3GPP's own network-efficiency KPI, DL-ISAC is Pareto-optimal:
positioning at zero positioning overhead. Experiment #1 = a 3-KPI comparison in standardized language:
(1) throughput sum-rate MEAN + CELL-EDGE [38.843/38.913], (2) positioning accuracy CDF p50/67/80/90
[38.857], (3) positioning resource cost PRS/SRS [38.857 net-efficiency]; + report CsiNet+ params/FLOPs
[38.843 complexity] for honesty. DL is the only method near-top on throughput AND providing positioning
AND spending zero positioning resources. Also have on disk: TS 38.214 v19 (eType-II codebook), TS 38.305
v19 (positioning measurements: RSTD/UE-Rx-Tx/AoD/AoA/multi-RTT), TR 38.859 (Rel-18 positioning), TR
38.913 (system KPIs), TS 22.261 v19.12 (5G service reqs incl Rel-19 sensing). TR 38.901 NOT on disk.
