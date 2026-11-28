---
name: swin-backbone
description: "Swin conv+windowed-attention hybrid backbone, pre-drafted; GO decision for recon upgrade"
metadata: 
  node_type: memory
  type: project
  originSessionId: f4bbcb42-a71c-4faa-ae17-bc15b8ffc247
---

`src/swin_ae.py` = self-contained Swin Transformer CSI-feedback backbone (W-MSA + shifted-window MSA with relative position bias + canonical attn mask, conv stem/head, hierarchical patch-merging/expanding; no timm dep). Wired into `MultiTaskAE` as `backbone="swin"` and into the `--backbone` CLI choices, so it trains through the exact `multitask_train.py` pipeline as CsiNet+. Verified on CPU: interface (B,2,64,64)->z(256)->(B,2,64,64), unit-Frobenius output, 13.1M params (3x CsiNet+ 4.3M, vs 35.8M plain ViT). Assumes square Nc==Nt divisible 64->32->16->8.

**Why built (the proper upgrade #2):** the plain TransformerAE lost 2.4x to CsiNet+ (see [[localization-analysis]]); literature (SwinCFNet/AiANet) uses windowed-attention conv-hybrids, not plain ViT, to beat CNNs on CSI reconstruction.

**GO decision (2026-06-08):** beamforming eval showed DL recon rho=0.86 is **compression/capacity-limited** (saturates across feedback SNR 10->20dB, not noise-limited) with headroom to perfect — exactly the regime a stronger compressor helps. Realistic target: rho 0.86 -> ~0.90 at eta=1/32.

**TRAINING ATTEMPT FAILED (2026-06-09) -> CsiNet+ LOCKED as final backbone.** Swin recon smoke test (10k, lr=1e-3) failed two ways: (1) **~280 s/epoch on 10k** (~90x CsiNet+ 3s; ~75h for 100k/150ep) — eager manual windowed attention, first stage over full 64x64; (2) **NMSE flat ~2.87 dB, not learning** (CsiNet+ was -2.2->-4.3 by ep3) — pre-LN Swin needs lr~3e-4 + warmup. Third attention-backbone difficulty (after plain transformer). Decision: **lock CsiNet+** (deliverables already strong: 88% MU-MIMO sum-rate vs classical 60%); Swin = documented future work. To revive: fused F.scaled_dot_product_attention + torch.compile + stride-2 stem (start 32x32, 4x fewer tokens) for speed; lr 3e-4 + warmup for convergence. Code in `swin_ae.py` (shape-correct, wired as backbone="swin").
