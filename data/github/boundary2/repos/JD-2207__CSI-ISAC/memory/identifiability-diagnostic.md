---
name: identifiability-diagnostic
description: "Is the loc floor an information limit or a representation-generalization gap? Decisive diagnostic: it's representation -> channel charting/contrastive is the lever, multi-gNB down-ranked"
metadata: 
  node_type: memory
  type: project
  originSessionId: edfb6c15-36c8-4d37-9f25-d77a35f6a308
---

2026-06-16 ran `exp/diag_identifiability.py` (new, self-contained) to settle whether single-gNB NLOS
localization error is an INFORMATION floor (distinct positions -> near-identical observable channels)
or a LEARNABILITY/REPRESENTATION gap. Three estimator-free measurements on the 100k los15 test set
(random AND geographic split): grid floor (oracle spatial-1NN), raw channel-1NN spatial error
(magnitude-Euclidean + metric-free complex correlation rho=|<hi,hj>|/||·||||·||), learned code-1NN
(keeper encoder), and intrinsic ambiguity = max rho to a SPATIALLY-FAR (>20 m) UE. Artifacts
`results/identifiability/identifiability_{random,geographic}.json`. See [[localization-analysis]],
[[thesis-roadmap]], [[simulation-audit-caveats]] (geo-split caveat #2).

**VERDICT — representation-generalization problem, NOT an information floor (user's instinct confirmed).**

p50 errors (m), random | geographic split:
- grid floor (oracle spatial-1NN): 1.0 | 8.1
- raw chan-1NN |h|: 1.6 | 24.9
- raw chan-1NN rho: 7.4 | 30.2
- **learned code-1NN: 2.3 | 16.3**
- trained net (MAE): 5.3 | 19.9

1. **No information floor.** Across both splits <2.5% of NLOS UEs have ANY spatially-distant channel
   confuser at rho>=0.9 (rho>=0.95: ~0.1-1.7%); the rare ones sit ~168 m away (global scene symmetry,
   not local ambiguity). rho_far median ~0.51, max ~0.95. The single-gNB observable channel is almost
   always UNIQUE to position -> the ~20 m geographic error is NOT an information limit. Far-confusers
   are LOS-concentrated (16.6% of LOS vs 4.1% NLOS at rho>=0.9, random split) = LOS angular aliasing
   (same azimuth, different range); NLOS multipath is a near-unique position hash.
2. **Raw channel-similarity does NOT generalize across geography (1.6->24.9 m p50), but the learned
   code does -- partially (24.9->16.3).** Proof that representation IS the effective lever: the learned
   code already beats raw channel by ~9 m p50 under the fair split, yet is still ~8 m above the 8.1 m
   grid floor. That headroom = representation quality, not information.
3. Capacity already ruled out (net memorizes train 3 m; bigger TransformerAE was worse).
4. LOS generalizes BETTER than NLOS for the learned code (13.5 vs 17.1 m p50) = opposite of ambiguity;
   NLOS map is high-frequency/hard-to-extrapolate -> exactly what a distance-preserving objective targets.

**ROADMAP IMPACT (re-ranked loc levers):**
- **#1 Channel charting / contrastive spatial loss (UP).** Theoretically on-target + cheap (~1 wk); the
  learned code already proves representation closes the raw->generalizable gap. Goal: close 16->8 m geo gap.
- **Multi-gNB DOWN** (was "highest-impact loc" in [[thesis-roadmap]]): ambiguity ~0, so it's NOT the
  bottleneck. Reframe as coverage/robustness + the <2% LOS-aliasing tail, not the headline loc fix.
- Swin stays recon-only (not loc). Data helps the floor but diminishing GENERALIZATION returns under fair split.

Geo grid floor 8.1 m = best any DB-fingerprint method reaches at this sampling under the 25m-block/5m-guard
split; a regression model isn't DB-limited so sub-8 m is the real target. Not yet written into isac_findings
(offered).

**UPDATE 2026-06-16 — the charting fix this diagnostic motivated TESTED NULL at scale.** Contrastive/charting
loss on the loc embedding (triplet, best 10k weight) helped at 10k (sparse, far from floor) but did NOT
transfer to 100k (control 19.1 m vs w=3 19.5 m MAE; only p90 −2.1 m). So the diagnosis (representation-
generalization, not information) stands, but the in-model representation fix does NOT close the gap at scale —
because the MSE regression already learns a near-floor map from 84k samples. CONCLUSION SHARPENED: below
~12 m geographic needs NEW INFORMATION (multi-gNB / temporal), not a cleverer single-snapshot representation.
See [[thesis-roadmap]] (charting → NEGATIVE; multi-gNB scaffolded = next).
