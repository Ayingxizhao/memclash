---
name: rt-datagen-progress
description: Steps 1-5 DONE; dataset + MultiTaskDataFeed + MultiTaskCsiNet + training loop built & validated; next=scale data (step 6)
metadata: 
  node_type: memory
  type: project
  originSessionId: f4bbcb42-a71c-4faa-ae17-bc15b8ffc247
---

Coding progress on the thesis ([[thesis-project]]), as of 2026-06-05. Env: [[env-setup]]; GPU fix: [[gpu-optix-blocker]].

**Done — implementation-order steps 1 & 2:**
- `src/rt_smoke_test.py` — Sionna RT smoke test, passes (OptiX OK, LOS delay == ‖gnb−ue‖/c).
- `src/sionna_rt_gen.py` — RT generator: `RTSceneConfig`, `build_scene`, `sample_positions`, `generate_batch`, `generate_dataset` (generator), `indoor_flags`, `meta_dict`. Returns **(H, xy, los, indoor)**.
- `src/rt_localization_data_gen.py` — runner, saves sharded `.npz` (H/xy/los/indoor) + `meta.json` to `data/rt_<scene>_<n_tx>ant_<n_ue>ue/`.
- First dataset (superseded): 203 kept UEs, H (N,64,20) — narrowband, regenerated below.
- `src/data_feed.py` — added `MultiTaskDataFeed`, `build_multitask_feeds`, `load_rt_shards`, `angular_dft_upa`, `normalize_csi`, `denorm_xy`, `_split_indices`. Original `DataFeed` untouched.

**Current dataset (2026-06-07): `data/rt_munich_64ant_200ue/`** — SOTA-aligned, regenerated.
- 218 kept UEs, **3 LOS / 215 NLOS** (near-pure NLOS by design; azimuth 235°), 101 indoor / 117 outdoor. H shape **(218, 64, 64)** complex64 delay-domain.
- Config: 100 MHz / 1024 subcarriers, n_taps=64 (90% delay energy by tap 47 → 64 justified, 32 would clip), diffuse scattering on (coeff 0.5), single-sector sampling (az 235°, downtilt 10°, span 120°, r 30-300 m), max_depth=10, batch_size=25 (Dr.Jit 2^32 limit), seed=40.
- Power spread 86 dB (kept as localization cue). meta.json has actual xy_min/xy_max for position norm.
- User decision: test pure-NLOS first; LOS/NLOS comparison (re-aim azimuth) deferred. See [[beamforming-eval-deliverable]].

**Key design decisions baked in (verified empirically):**
- `normalize_cfr=False` → keeps absolute path loss (localization distance cue; power spread ~85 dB across UEs). Per-sample Frobenius norm deferred to load time.
- Subcarriers: generate n_prbs×12 @30kHz, keep one per PRB → n_sub=20 (matches data_gen freq_selection).
- LOS label: geometric (first-path delay ≈ ‖gnb−ue‖/c).
- **Indoor UEs ARE included.** Munich materials transmit (0.1 m walls). `max_depth` is the key knob: indoor-with-signal yield 25%→41%→56% at depth 5→8→12. Default `max_depth=10`. Indoor/outdoor labeled via upward ray-cast (`scene.mi_scene.ray_intersect`). Zero-power UEs (deeply shielded, unlocalizable) still dropped.
- `n_ue_total` = number of KEPT UEs (generator oversamples; ~40-65% yield in ±250 m box around gNB). Generation is fast (~few sec for 200; GPU + synthetic_array).
- Scene bounds via `scene.mi_scene.bbox()` (no `scene.center`/`size` attr in 2.0.1).

**MultiTaskDataFeed design (step 3, DONE):** `build_multitask_feeds(data_dir, ...)` loads shards once, processes, returns (train,val,test) sharing arrays. Each `__getitem__` -> `(channel (2,64,64), xy (2,)[, mag (1,)][, flags (2,) los/indoor])`. Pipeline: optional delay-truncate -> optional **angular 2D-DFT over 8×8 UPA** (`angular_dft_upa`, unitary fft2, row-major reshape; sparsifies spatial peak/mean 1.05→12.2) -> per-sample Frobenius norm + global-phase removal (`normalize_csi`; phase ref = strongest element, NOT [0,0] which is ~0 in NLOS) -> xy min-max to scene bounds -> **log-Frobenius magnitude returned as `mag`, standardized on TRAIN split only** (no leakage). NOTE: my H is already delay-domain from generation, so I do NOT re-run `convert_channel_angle_delay` (that's freq->delay); only the angular DFT remains. Self-test passed (shapes, unit-norm, xy round-trip 5e-6 m, DFT energy preservation, no split leak).

**Step 4 (DONE): `src/multitask_ae.py`** — `MultiTaskCsiNet`: reuses repo `CsinetPlus.Encoder`/`Decoder` unchanged as Head A (so same class = fair single-task baseline), adds `LocHead` MLP. `forward(x, mag) -> {z, csi, xy}`. `loc_source='bottleneck'` (thesis design, ~100k params) or `'decoder'` (ablation via forward hook on conv_block1, ~2.1M). mag concatenated into Head B. out_activation sigmoid (matches pos_norm [0,1]). At eta=1/32 encoded_dim=256, full size 2*64*64=8192, total ~4.3M params.

**Step 5 (DONE): `src/multitask_train.py`** — `train_multitask(...)`, CLI argparse. Denoising AE: `add_awgn` adds AWGN to unit-Frobenius CSI BEFORE encoder, clean CSI = target; SNR is train/eval knob (snr_train range default (0,20)dB sampled per-sample, snr_val=10). **L_rec = NMSE (O(1)), NOT raw MSE** (MSE is ~2e-4 due to 8192-elem averaging → loc would dominate; key step-4 finding). `UncertaintyWeighting` (Kendall, learned log_var per task) primary; 'fixed' lambda baseline. Curriculum: recon-only warmup `warmup_epochs` then joint. Metrics: NMSE dB + loc MAE/p50/p90 in meters (denorm_xy). Saves best-by-val-loc-MAE checkpoint.

**Validation run (80ep, tiny 174-train):** pipeline learns — NMSE 3.02→1.92 dB, loc MAE 114→94 m, UW weights adapt. Numbers POOR but expected: 4.3M-param net on 174 samples (data-starved). Code is correct; this is exactly what step 6 (scale data) fixes.

**Step 6 IN PROGRESS — scaled dataset + CsiNet+ baseline (2026-06-07):**
- `data/rt_munich_64ant_2000ue/` — 2019 kept UEs, 9 LOS / 2010 NLOS, 1088 indoor / 931 outdoor, 85 shards. Same SOTA config as 218-UE set, n_ue_total=2000, seed=40, pure-NLOS (az 235°). User chose 2000 UEs + keep pure NLOS.
- **CsiNet+ multitask baseline** (eta=1/32, encoded_dim=256, 150ep, warmup 15, batch 64, UW, train SNR 0-20dB, eval 10dB): TEST NMSE **-1.91 dB**, loc MAE **51.4 m** (p50 36.6, p90 113.1). Checkpoint `checkpoint/mtl_csinet_2000_eta32.pt`. (vs 174-UE: 1.92 dB / 104.7 m — confirms pipeline scales.)
- **Mutual-benefit ablation (DONE, multi-seed n=5 [42,1,7,13,123], `src/ablation_multitask.py`, identical encoder/config, eta=1/32 CsiNet+):** recon-only NMSE **-1.96±0.23 dB**, loc-only MAE **47.8±2.0 m** (p50 34.9), joint NMSE **-2.06±0.21 dB** / MAE **53.9±2.6 m** (p50 43.5). Paired deltas: **loc→feedback +0.11±0.15 dB NOT significant**; **feedback→loc -6.1±1.7 m SIGNIFICANT** (2*SE=1.6). → **FLnet mutual-benefit does NOT replicate here; asymmetric NEGATIVE transfer: joint hurts localization ~6 m (~13% MAE, ~9 m p50), feedback unaffected.** Pure-NLOS macro, single 256-d bottleneck shaped mainly for recon (+ warmup head-start) = loc pays. ISAC story intact (one 1/32 codeword → good loc + free denoised CSI; 6 m = quantified cost of integration). Single-seed run earlier (-0.19 dB / +6.4 m) was partly noise (dNMSE flipped sign). Mitigations to try: PCGrad/GradNorm (guide fallback), bigger bottleneck, Head-B-from-decoder, TransformerAE capacity.
- NMSE -1.9 dB is modest (weak CNN backbone, eta 1/32, pure NLOS + noise = hard). This is the baseline to beat with TransformerAE.

**Datasets available (all pure-NLOS az 235, same SOTA config, seed 40):** `data/rt_munich_64ant_{200,2000,10000}ue/`. 10k = **10022 UEs** (48 LOS / 9974 NLOS, 5434 indoor / 4588 outdoor), 421 shards. Generated fast (~min, not the est. hrs).

**TransformerAE added (2026-06-08):** `multitask_ae.py` refactored to `MultiTaskAE(encoded_dim, Nc, Nt, backbone='csinet'|'transformer', ...)`; `MultiTaskCsiNet` kept as alias. Transformer ported from `unused models/compression/transformerAE.py` (TransformerEncoder/Decoder, tokens=angle bins, attn across angle, d_model=Nt*8, 3 layers, 8 heads) + **added unit-Frobenius decoder norm** (repo version lacked it) so NMSE comparable. csinet 4.3M params, transformer 35.8M. `multitask_train.py` now has `--backbone`, `--task`, `--loc_dropout` CLI flags. loc_source='decoder' only for csinet.

**Localization sweep IN PROGRESS:** `src/exp_backbone_data.py` — loc-only, {2k,10k} x {csinet,transformer}, 120ep, reports train/test MAE + gap. Goal: drive loc error below ~50m (user req). Background run b169qpwqx.

**Next:** pick winning backbone+data, then eta sweep, joint vs loc with best config, Step 7 baselines (eType-II + CS feedback; KNN [DONE, 128m] + AoA/ToA loc). Then [[beamforming-eval-deliverable]]. See [[localization-analysis]].
