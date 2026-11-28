---
name: recon-nmse-zero-norm-bug
description: Recon NMSE diverges to +74 dB on large RT sets due to zero-norm (blocked) UEs; fixed by filtering
metadata: 
  node_type: memory
  type: project
  originSessionId: f4bbcb42-a71c-4faa-ae17-bc15b8ffc247
---

On the 100k Munich RT set, recon-only (task='recon') training pinned at **+74 dB NMSE** from epoch 1 (decoder dead-collapsed), while loc-only trained perfectly (4.6 m MAE). Root cause: a handful of **exactly/near-zero Frobenius-norm channels** (fully-blocked deep-indoor UEs with no ray paths — the set is ~54% indoor). `normalize_csi` leaves a true-zero channel at ~0, so `nmse_per_sample` divides `||pred||^2` by `clamp_min(1e-12)` -> ~1e12, dominating the mean and exploding gradients. 10k didn't have such samples, so it trained fine -> NOT an LR issue.

**Fix (both in place):** (1) `build_multitask_feeds(..., min_norm_frac=1e-3)` drops UEs with raw Frobenius norm < 1e-3 x median (dropped 460/100016 on the 100k set); (2) `nmse_per_sample` denominator floor raised 1e-12 -> 1e-4 (harmless since valid normalized targets have energy ~1). After fix, recon descends normally: -2.2 -> -3.7 -> -4.3 dB over 3 epochs.

**How to apply:** Any new RT set (esp. high indoor fraction) needs this filter; check `np.linalg.norm(H.reshape(M,-1),axis=1).min()` after generation. Loc is robust to these samples (xy still valid) but recon/beamforming are not. See [[rt-datagen-progress]], [[localization-analysis]], [[beamforming-eval-deliverable]].
