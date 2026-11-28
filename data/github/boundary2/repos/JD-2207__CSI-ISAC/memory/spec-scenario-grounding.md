---
name: spec-scenario-grounding
description: "How to ground the thesis's outdoor dense-urban scenario + ray-tracing in 3GPP specs (38.901/38.855/38.857/38.843) — clause/table provenance, the Munich parameter-table mapping, and Sionna-RT = TR 38.901 clause 8"
metadata:
  node_type: memory
  type: reference
  originSessionId: fb5095de-fba1-407a-8c92-6de98651cc52
---

Firsthand spec read (2026-06-26) to write the thesis methodology/scenario chapter spec-faithfully.
38.843 §6.4 positioning eval ONLY tabulates InF-DH (Table 6.4.1-1); there is NO outdoor positioning
table inside 38.843 or 38.857. You CONSTRUCT one (same way 38.843 built its InF table = modify a base
scenario). See [[38843-csi-alignment]], [[3gpp-kpi-targets]].

## RELEASE LOGIC (why all 3 docs, what each is authoritative for)
- **Geometry/propagation → TR 38.901 §7.2 Table 7.2-1** (release-stable channel model): UMi-street-canyon
  (hex, 19 micro×3sec, ISD 200m, BS h=10m) and UMa (ISD 500m, BS h=25m). UMi generic UT = 80% INDOOR.
- **Radio operating point → TR 38.857 (Rel-17) §6 Table 6-1**: FR1 **3.5 GHz / 100 MHz / 30 kHz SCS**,
  gNB NF 5 dB, UE NF 9 dB, UE TX 23 dBm. This is the Rel-17 UPDATE (38.855 was 2/4 GHz) → our carrier.
- **Positioning drop + KPI → TR 38.855 (Rel-16) §6.1/§6.2.1** — UNAVOIDABLE because 38.857 §6.2 "General
  commercial use cases" NORMATIVELY REUSES 38.855 for outdoor UMa/UMi/IOO. Tables: 6.1.1-1 common,
  **6.1.1-4 UMi-SC** (positioning OVERRIDE = 100% OUTDOOR, 0 dB pen, gNB 44 dBm, (8,8,2,1,1)), 6.1.1-5
  UMi/UMa gNB pattern, **6.1.1-6 UMa** (49 dBm). KPI §6.2.1 = horizontal CDF **p50/67/80/90**.
- **AI/ML method on top → TR 38.843 §6.4.1** (Direct AI, model input = CIR, KPI horiz-CDF p90 + opt 50/67/80,
  complexity #params+FLOPs). §6.4.1 "Target requirements NOT defined for AI/ML" → no target we fail.

## KEY CONTRASTS to state in the thesis
- **UT drop:** generic 38.901 UMi = 80% indoor; 38.855 positioning OVERRIDES UMi to 100% outdoor. Our Munich
  RT = physical indoor/outdoor mix (~58% indoor-flagged) → we match the generic 38.901 distribution, NOT the
  100%-outdoor idealization (a more-realistic deviation, state it).
- **Carrier:** cite 38.857 (3.5 GHz), not 38.855 (2/4 GHz).
- **Munich placement:** single rooftop gNB at **27 m** ≈ UMa height (25m) over a **UMi-density (ISD-200m-class)
  street layout**, single 120° sector → a single dense-urban macro sector = UMa-height over UMi-density.
  Cite UMi-SC geometry + note the rooftop/UMa BS height. Our scene: fc 3.5 GHz, BW 100 MHz, 1024 sc →
  SCS 97.66 kHz (uniform CFR grid, NOT NR 30 kHz = a deviation), 8×8=64 single-pol-V (vs 128 dual-pol),
  n_rx=1 (rank-1), UE 1.5m, area ~288×507m, 1 gNB (multi-gNB study 1/2/3), perfect timing (no Rx/Tx error).

## RAY TRACING IS 3GPP-SANCTIONED → TR 38.901 CLAUSE 8 (the strongest methodology citation)
Clause 8 = **"Map-based hybrid channel model (Alternative channel model methodology)"** = 3GPP's OWN ray-
tracing model (alternative to statistical §7.2-7.5). §8.4 "Channel generation" (Fig 8.4-1): import digital
map (3D geom + wall material/thickness + permittivity/conductivity) → ray-trace each Tx/Rx → optional merge
with random clusters. **Table 8.4-1 "Principles applied in ray-tracing"** maps ~1:1 to our Sionna meta.json:
LOS(Friis), Reflection(Snell+image/Fresnel)=`specular_reflection`, Penetration(slab/Fresnel)=`refraction`,
Scattering(RCS coeff)=`diffuse_reflection`+`scattering_coefficient=0.5`, Diffraction(UTD)=CONFIRM enabled.
3GPP recommends penetration order ≤5 / reflection{1,2,3}; ours max_depth=10 (note it). PRECISIONS: (1) we
implement the DETERMINISTIC half of the hybrid (RT clusters + diffuse scatter) WITHOUT the statistical
random-cluster augmentation (Steps 4-7) → frame as "a map-based deterministic instantiation of TR 38.901
clause 8". (2) Wideband: Step 2f splits B into K_B≥B/(c/D) bins; our 8×8 aperture ~0.3m → c/D≈1 GHz, B=100MHz
→ **K_B=1** single bin (consistent w/ Sionna per-subcarrier CFR). ⇒ cite clause 8: Sionna-RT is 3GPP's
alternative-but-equally-defined methodology, NOT a departure.

## ISAC CHANNEL MODEL → TR 38.901 §7.9 (scope demarcation only)
§7.9 (Rel-19 ISAC channel) = DEVICE-FREE passive-target sensing (RCS-based; the TR 22.837 branch). §7.9.1
Tables 7.9.1-1..-5 = ISAC-UAV/Automotive/Human/AGV/Objects, all REUSE UMi/UMa/RMa/SMa as the COMMUNICATION
scenario; channel = target channel (ST reflections) + background channel (§7.9.4). OUR ISAC = device-BASED
(position a connected UE from its own comms channel, 38.843 §6.4) → cite §7.9 to SCOPE OUT the device-free
branch, not as a model we use. §7.7 CDL/TDL = link-level abstraction we don't use (full-spatial RT instead).
§7.8 calibration (Tables 7.8-x UMa/UMi reference CDFs) = optional belt-and-suspenders RT-statistics check.

## ASSEMBLED PROVENANCE (one line): geometry=38.901 §7.2 T7.2-1 | radio=38.857 §6 T6-1 (Rel-17) |
positioning drop+KPI=38.855 §6.1 T6.1.1-4/-6 + §6.2.1 (reused via 38.857 §6.2) | AI method=38.843 §6.4.1 |
RT methodology=38.901 clause 8 T8.4-1 | ISAC device-free demarcation=38.901 §7.9.

## DEEP-DIVE DOC (2026-06-26) + PER-ITEM DECISION TABLE
Wrote `literature/explainers/38843-positioning-deepdive.md` = full firsthand read of 38.843 positioning
clauses §5.3 / §6.4.1 / §6.4.2.1-.6 / §7.1.4 / §7.2.4 / §7.3.5 / §8 (verbatim Table 6.4.1-1 InF, model
input N_TRP×N_port×N_t @8.14ns, Table 6.4.1-2, truncated-Gaussian labels, fine-tune/timing/TRP-reduction
multipliers) + the PART-B cross-spec table + PART-C spec-faithful "what we'd need" + PART-D honest code
comparison. KPI alignment CONFIRMED: 38.843 §6.4.1 main KPI = horizontal-error CDF **p90 + {50,67,80} opt**,
**"target requirements NOT defined for AI/ML positioning"** (no target we fail); complexity = #params(×2 if
complex)+FLOPs. Our evaluate() p50/67/80/90 + enc/dec/loc params+FLOPs = ALIGNED. Spec classical baseline
(T6.4.1-1) = "DL-TDOA / Multi-RTT, method used to be reported" → our P1 gap.

**★ DIFFRACTION CONFIRMED (the one unverified T8.4-1 mechanism):** Sionna 2.0.1 `PathSolver.__call__`
DOES expose `diffraction=False`, `edge_diffraction=False`, `diffraction_lit_region=True`. Our
`sionna_rt_gen.py` passes specular_reflection/diffuse_reflection/refraction ONLY → **UTD diffraction is
AVAILABLE but currently OFF**. Enabling = a regen choice, NOT a Sionna limitation. = only missing T8.4-1
mechanism (max_depth=10 already rich → low priority).

## CROSS-SPEC EVALUATION EXTRACTION (2026-06-26, 38.855 §6-10 + 38.857 §5-10 read in FULL)
User pushed back on "only a few clauses useful" — read 38.855 §8 (DL/UL/DL+UL × Indoor/UMi/UMa) + §8.5
summaries + §9 impacts + §7 method menu, and 38.857 §5/§8.4/§9 firsthand. ⇒ NEW deep-dive PART B2.
**VERIFIED firsthand (were memory-only): UMi T6.1.1-4** (hex 19/7 sites 3-sec ISD200m, 44dBm, (8,8,2,1,1)
128-elem, 8dBi, 100% outdoor, gNB h=10m or [5-20]m, min 10m); **UMa T6.1.1-6** (ISD500m, 49dBm, gNB h
uniform[20-50]m, 50% indoor+50% outdoor, min 35m, outdoor 60km/h); **T6.1.1-1 common** (NF gNB5/UE9,
UE TX23, sync truncated-Gaussian T1∈{0,50ns}). 6-method menu (§7): DL-TDOA, DL-AoD, UL-TDOA, UL-AoA,
Multi-RTT, E-CID. KEY EVAL FINDINGS (outdoor baselines, sync-breaks-classical, Multi-RTT-robust, latency
table, integrity/PL → σ-head) all recorded in [[3gpp-kpi-targets]] "OUTDOOR CONVENTIONAL BASELINES" section.

**PER-ITEM KEEP vs CHANGE/REGEN (verified vs RTSceneConfig/meta.json):** carrier/BW 3.5GHz/100MHz=MATCH;
SCS 97.66kHz vs 30kHz=KEEP (total BW sets delay res); 64 single-pol-V vs 128 dual-pol=KEEP→Tier4; n_rx=1
rank-1 vs 2/4=KEEP→Tier4; gNB h 27m vs 10m=KEEP (UMa-height/UMi-density rooftop); **1-sector/collinear
multi-gNB vs hex 57 TRP=FLAG REGEN (biggest loc deviation, bad GDOP, hex/3-sector makes classical TDOA/RTT
meaningful)**; perfect timing vs 38.855 truncated-Gaussian=CHANGE (P1, inject into save_toa data, no regen);
diffraction OFF=FLAG optional regen; max_depth 10 vs rec {1,2,3}=KEEP (note); UE drop ~58% indoor vs 100%
outdoor override=KEEP (matches generic 38.901 80%-indoor, more realistic). Regen priority: (1) hex/3-sector
multi-TRP [highest loc value], (2) rank2/4+dual-pol [Tier4, moves CSI headline], (3) diffraction-on [low].

**FDD-AT-3.5GHz DEFENCE + TDD-TRANSFER ARGUMENT (2026-08-07, written up in
`literature/explainers/5g-frame-waterfall-walkthrough.md` Part II preamble + §18).** No FDD band exists at
3.5 GHz (n78 = TDD); all paired FDD spectrum is ≤2.6 GHz and caps ~40–50 MHz/channel (~20 MHz typical
holding). Separate the two requirements: **duplexing is hard** (TDD reciprocity deletes the feedback
problem outright), **carrier/bandwidth is soft** — a deployable version of this system exists TODAY at
~2 GHz FDD with 1/5 the bandwidth, and the ARRAY IS UNAFFECTED (angular resolution = aperture in
wavelengths, so 8×8 λ/2 resolves angle identically at 2 GHz, just 60 cm instead of 34 cm). ⇒ the joint
compression-and-sensing contribution needs **FDD**, NOT 3.5 GHz.
**OPEN EXPERIMENT — run the bandwidth sweep DOWNWARD to 20 MHz** (`rt_bandwidth_sweep.py` /
`exp/exp_bandwidth_loc.py` already exist; earlier sweep only went UP 100→200→400). Do NOT assume 38.857's
bandwidth scaling (100 MHz≈9m@90% vs 5 MHz≈40m): that is derived for TIMING-based methods where first-path
resolution rules, whereas our own sweep found the OPPOSITE dependence for fingerprinting (loc got worse as
BW rose, coverage-limited not resolution-limited — see [[localization-analysis]]). At 20 MHz resolution
coarsens (~15 m/tap) but the delay window widens (~960 m); which wins is UNMEASURED. Either outcome is
publishable: modest degradation ⇒ "works in a deployable 2 GHz FDD config"; severe ⇒ quantifies the BW
dependence of learned CSI-fingerprint loc. Rel-18 PRS/SRS **bandwidth aggregation** is the real-world
mitigation (aggregate n1+n3), at the cost of non-contiguous-sampling ambiguity.
**TDD-TRANSFER:** loc physics is duplex-agnostic (position lives in angles+delays). FDD gives NO loc
advantage — TDD's reciprocity hands the gNB the FULL uncompressed channel. But that extra info would NOT
have helped us: [[identifiability-diagnostic]] geo-split p50 = raw-channel-1NN 24.9 m vs learned-code-1NN
16.3 m — the codeword BEATS the raw channel by ~9 m (compression acts as a generalization constraint), and
ambiguity ~0. ⇒ accuracy numbers/NLOS-vs-LOS/multi-gNB scaling all TRANSFER to 3.5 GHz TDD; what does NOT
transfer is the FRAMING ("position free from the codeword" is trivial in TDD, where the gNB already holds
the channel).
