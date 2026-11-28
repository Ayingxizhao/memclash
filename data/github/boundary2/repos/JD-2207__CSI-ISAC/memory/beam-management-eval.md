---
name: beam-management-eval
description: "Position-aided beam management (#2, sensing->comms payback) — built 2026-06-18; LOS: 1 beam from position ~= exhaustive (huge overhead cut), but a hard NLOS ceiling (best beam = reflector, not UE)"
metadata:
  node_type: memory
  type: project
  originSessionId: 51b9241a-484b-488c-921a-cc25e1a7a9f5
---

Roadmap **#2 position-aided beam management** — the ISAC PAYBACK direction
(sensing -> comms), complement to the rest of the thesis (comms -> sensing). Use the
predicted [X,Y] to PRE-SELECT downlink beams: sweep only the k codebook beams near the
predicted AoD instead of all N -> N/k overhead cut. See [[thesis-roadmap]],
[[beamforming-eval-deliverable]], [[classical-loc-baseline]], [[localization-analysis]].

**Code:** `exp/beam_mgmt_eval.py` (CPU/numpy, reuses classical_loc_baseline's EXACT
gNB0 manifold: upa_elem_positions/steer_matrix/aoa_directions). One serving cell (gNB0),
NO CoMP. Codebook = MRT beams over gNB0 front sector (default N=432, az+-70/el+-22 @ 4deg).
genie beam = argmax wideband power w^H R w from TRUE channel; aided = position -> geometric
AoD -> rank codebook by angular proximity -> sweep top-k -> best. Metrics vs k, LOS/NLOS:
realized gain 10log10(aided/exhaustive) dB, top-1 hit rate, MU-MIMO sum-rate (analog =
beams-as-precoder + hybrid = analog beam + digital RZF on the K-dim effective channel;
users unit-power-normalized like mu_mimo_eval). Run on 3gnb_toa dataset (gNB0 az170, 45% LOS).

**KEY PHYSICS (the framing):** position-aiding has an INTRINSIC NLOS CEILING no position
accuracy can beat. LOS: optimal beam points AT the UE so geometric AoD ~= best beam. Deep
NLOS: optimal beam points at a REFLECTOR, not the UE, so even a PERFECT position picks a
suboptimal beam. -> the localization-for-beams value is LOS-regime OVERHEAD REDUCTION; NLOS
needs the CSI codeword (why the system keeps the recon path). Quantified by genie(true xy)
vs exhaustive below.

**RESULT (full kept pop, 9749 UEs = 1791 LOS / 7958 NLOS, `results/beamforming/beam_mgmt.json`):**
realized gain dB below exhaustive (432 beams), k=1 / k=4 / k=32:
- **genie(true xy) LOS:  -0.33 / -0.16 / -0.02 dB** -> ~1 beam from position == exhaustive
  (432x overhead cut for 0.33 dB). THE headline ISAC payback.
- **genie(true xy) NLOS: -4.12 / -3.07 / -1.52 dB** -> the ceiling: 32 beams still lose 1.5 dB
  because best beam = reflector. Perfect position cannot close it.
- **UL-AoA pointing (Bartlett dominant-path angle, NOT a position source — needs UL sounding)**
  NLOS: -2.16 / -1.84 / -1.05 -> beats position in NLOS because it tracks the reflector.
MU-MIMO sum-rate K=4 @ 20 dB: exhaustive analog 8.31 / hybrid 9.21; genie-position k=1
analog 5.15 (62%) / hybrid 5.83; k=4 5.70 / 6.30. Hybrid digital-RZF recovers a lot of the
analog beam-collision loss. NLOS-dominated pop -> aggregate is conservative; LOS subset is the win.

**THESIS FRAMING:** localization is a near-free LOS beam-acquisition accelerator (1 beam vs
432-beam sweep). Its benefit is bounded by the NLOS reflector ceiling, not by position error.

**STEP B DONE (2026-06-18) — net positions, geo-test head-to-head (406 UEs = 56 LOS/350 NLOS):**
Added a position-export to `exp_multignb.py` (`--export_pos` -> `predict_xy` dumps test-set
pred+true xy; aligned in beam_mgmt_eval by nearest true xy, match err ~0). Ran the 1/2/3-gNB
A/B with export (`results/beamforming/multignb_pos_10k.npz`; A/B reproduced p90 65.6/35.3/23.9).
`beam_mgmt_eval.py --net_export ...` adds net 1/2/3-gNB sources. Realized gain dB, LOS, k=1/k=4:
- genie(true): -0.84 / -0.32   · net 1gNB: -1.00 / -0.52   · net 2gNB: -0.72 / -0.30   · net 3gNB: -0.73 / -0.27
THREE CLEAN FINDINGS (all CONFIRM the prediction):
1. **The net's LEARNED position captures the full genie beam-mgmt ceiling in LOS** (net 1gNB
   within ~0.2 dB of genie-true; net 2/3gNB MATCH/slightly beat it). So localization-aided beam
   mgmt is real AND the net delivers it: 1 beam ~= exhaustive in LOS (108-432x overhead cut).
2. **The multi-gNB localization gain (p90 66->24 m) does NOT translate to beam-mgmt gain**:
   net 1->2->3 gNB LOS k=1 = -1.00 -> -0.72 -> -0.73 dB (~0.3 dB once, gone by k=4). Beam
   selection is forgiving at beamwidth scale (~13deg >> net's few-m error); LOS already
   saturates with single-gNB position. The pillar's accuracy win is wasted on beams.
3. **NLOS is reflector-ceiling-limited for ALL sources** (~-1.5 dB at k=32). Ironically the
   MORE accurate multi-gNB position can slightly HURT in NLOS (net 2gNB nlos k=1 -5.39 < genie
   -4.94): it confidently points at the UE, but the optimal beam wants the REFLECTOR. UL-AoA
   (dominant-path tracking, nlos k=1 -3.12) wins NLOS but needs UL sounding.
NET: #2 is a defensible POSITIVE-with-nuance pillar — sensing->comms payback is real and free
in LOS (the net captures it), but its ceiling is set by LOS/NLOS geometry, not by localization
accuracy, so it does NOT consume the multi-gNB accuracy lever. Clean, honest, complete.
