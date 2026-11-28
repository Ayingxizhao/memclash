---
name: thesis-project
description: "Master's thesis goal, scenario, and locked architecture/tooling decisions for the CSI project"
metadata: 
  node_type: memory
  type: project
  originSessionId: b77e8d24-536c-47f7-82d9-b7a4ef3690b3
---

Master's thesis (Telecommunications): a **multi-task deep model** for 5G **FDD massive MU-MIMO** that, from one compressed CSI feedback codeword, both (a) reconstructs denoised downlink CSI for 3D beamforming and (b) predicts each UE's `[X,Y]` position (ISAC localization). Scenario: **urban NLOS**, many UEs simultaneously.

Built on the cloned baseline repo `StochasticRTcomparison` (jmoraispk), local folder `C:\Users\javid\Documents\Javier\CSI\csi_isac`. That repo does CSI compression only; it uses DeepMIMO for ray tracing and Sionna for *stochastic* 3GPP models — NOT Sionna RT, and it discards UE positions.

Locked decisions (2026-06): **Sionna 2.0.1 RT** (upgrade from pinned 0.19.1; API `PathSolver` + `paths.cfr()`), Munich scene, **gNB = 64-element 8×8 UPA** transmitter / single-antenna UE receiver, **CsiNet+ backbone** (locked after plain-Transformer and Swin both lost — see [[swin-backbone]], [[localization-analysis]]; CODE-vs-PAPER AUDIT 2026-06-19 vs CsiNet+ Guo et al. 2020 / arXiv 1906.06007: the DEFINING features match — RefineNet block (ch 2→8→16→2, kernels 7/5/3, BN, identity skip) ×5, 7×7 conv encoder, FC compression — but the output layer is adapted (Tanh + per-sample **Frobenius normalization** instead of the paper's Sigmoid→[0,1], because our CSI is unit-norm COMPLEX not [0,1] magnitude) → cite as **"CsiNet+-based"** not verbatim CsiNet+. Minor unverified: encoder uses 2× 7×7 convs (paper may use 1, or a Sigmoid 2nd conv); non-refine conv placed before refines vs paper's after) with a **codeword-direct localization head** (Head B reads the bottleneck), loss balanced by **homoscedastic uncertainty weighting** (or a fixed-λ recon↔loc knob). See related preference [[baselines-requirement-and-theory]].

Phase-1 deliverable (approved proposal) lives at `C:\Users\javid\.claude\plans\context-project-master-s-thesis-jolly-hamming.md`. Phase 1 was proposal-only ("do not write code yet"); implementation is a later phase.
