---
name: sensitivity-cut-experiment
description: "power-limited coverage cut — trimming sub-SNR UEs shrinks loc p90 tail, p50 robust (headline not an artifact)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 085e82b3-d901-43b7-98e4-426b8fa3036e
---

2026-07-05: Added a POWER-limited coverage boundary (receiver-sensitivity cell edge) to close the
asymmetry that bandwidth is a hard modeled limit but power was only graded per-UE noise (coverage was
purely geometric = drop UEs with NO ray path). Because channels keep absolute gain (normalize_cfr=False),
the cut is pure POST-PROCESSING, no regen. Script: `src/exp/exp_sensitivity_cut.py`
(results/sensitivity_cut/results_loc.json). Controlled A/B: FIXED physical link-budget offset shared by
all conditions (anchor full-set median UE→10 dB ⇒ offset 105.6 dB, implied EIRP 18.6 dBm, Nfloor
−87 dBm @100 MHz/NF7), meta.json copied unchanged so normalization box (hence reported meters) identical
across cuts; only POPULATION changes. Per-UE SNR = offset + 20·log10‖H‖_F; drop SNR < threshold; retrain
under linkbudget noise, geographic split, 100k Munich, 120 ep.

RESULT (loc p50 / p90 m): baseline(N=100017,17%LOS) 12.3/48.0 → cut≥−6dB(83.9%,20%LOS) 11.2/36.3 →
cut≥0dB(72%,23%) 11.8/36.5 → cut≥6dB(60%,26%) 10.6/33.8. p90 tail collapses −12 to −14 m; p50 barely
moves (±1 m); NMSE flat 3.0 dB. CONCLUSION: headline loc numbers are NOT an artifact of including
un-localizable sub-sensitivity far/deep-NLOS UEs — the p50 is robust, only the tail (exactly those UEs)
shrinks under a cell edge, and LOS fraction rises as expected. Closes the "coverage is only geometric"
caveat.

POWER SWEEP (exp/exp_power_sweep.py, results/power_sweep/results_loc.json): full pop, sweep median-anchor
SNR = EIRP proxy. loc MEAN/p50/p90 m: 5dB 22.3/14.6/48.9 → 10dB 21.2/13.0/47.9 → 20dB 17.5/11.0/38.9 →
30dB 16.9/11.2/33.8 → phys 44dBm(medSNR35.4) 16.9/11.4/32.3. SATURATES: 1000× power span moves mean only
−5.5m, and 20→30→44dBm mean flat 17.5→16.9→16.9 / p50 flat ~11m; only p90 tail keeps dropping (some far
UEs noise-limited). CONFIRMS loc floor is identifiability/representation-limited NOT power-limited (higher
EIRP cleans noisy UEs then saturates, can't separate degenerate NLOS fingerprints); real lever = NEW INFO
(multi-gNB) not power. ABSOLUTE op-point @spec 44dBm gNB EIRP: mean 16.9m / p50 11.4m / p90 32.3m. Wedge
288×509m diag 585m, centre-guess floor ~293m ⇒ p50~11m ≈ 2% diag / 24× better than guessing. Both
experiments = Topic 76 in thesis_code_walkthrough_QA.md.

SPEC caveat: framework spec-consistent (thermal noise physics, BW/fc per 38.857, PL vs 38.901,
graded SNR per 38.843, sensitivity-edge concept per 38.101 REFSENS) BUT absolute EIRP is an implied
anchor not a spec operating point (‖H‖ folds in array gain — not abs-dBm calibrated), so thresholds are
RELATIVE/illustrative, not certified coverage requirements. See [[realistic-impairments-scope]],
[[simulation-audit-caveats]], [[spec-scenario-grounding]], [[localization-analysis]].
