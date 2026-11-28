# CSI-ISAC Thesis — Working Guide

Master's thesis: a multi-task deep model for 5G **FDD massive MU-MIMO** that, from a single
compressed CSI feedback codeword, jointly (a) reconstructs downlink CSI for 3D beamforming and
(b) predicts each UE's position `[X,Y]` (ISAC). Built on the cloned `StochasticRTcomparison` repo
(local folder `csi_isac/`),
re-tooled for **Sionna 2.0.1 RT** (Munich scene, 8×8 UPA / 64-element single-pol-V gNB, `n_rx=1` UE).

**Full architecture & data-pipeline plan:** `.claude/context-project.md` (the master design doc —
read it for the why behind any model/data/baseline decision). A mirror lives at
`C:\Users\javid\.claude\plans\context-project.md`.

## Where the code lives — `csi_isac/src/`

Active workflow files are at the **top level of `src/`**. Subfolders are data, experiments,
results, or the inherited (mostly unused) baseline stack.

### Core workflow (Tier 1 — load these for most model/training tasks)
- `model_config.py` — central config; every switch/hyperparameter other files read.
- `multitask_ae.py` — the model: `MultiTaskAE`, `LocalizationHead` (backbone-agnostic wrapper).
- `multitask_train.py` — training loop, loss balancing (uncertainty weighting), curriculum, joint metrics.
- `data_feed.py` — `MultiTaskDataFeed`, normalization (note the loc-critical magnitude caveat in the plan).

### Subsystem files (Tier 2 — load when the task touches them)
- **Backbones:** `swin_ae.py` (conv + windowed-attn hybrid, `backbone="swin"`), `CsinetPlus.py` (CNN baseline).
- **Data generation (Sionna RT):** `sionna_rt_gen.py`, `rt_localization_data_gen.py`, `rt_canyon_data_gen.py`, `gen_progress.py`, `scene_maps.py`, `scene_render.py`.
- **Beamforming / eval deliverable:** `beamforming_eval.py`, `beamforming_baselines.py`, `mu_mimo_eval.py`.

### `src/exp/` — experiments, diagnostics, validation (each script is self-contained)
- Experiments: `exp_*.py` (`exp_100k`, `exp_joint_100k`, `exp_eta_sweep`, `exp_backbone_data`, `exp_regularization`, `exp_final_loc`, `exp_bandwidth_loc`), `rt_bandwidth_sweep.py`, `ablation_multitask.py`.
- Localization analysis: `knn_localization.py`, `diag_localization.py`, `diag_delay_coverage.py`.
- Baseline validation: `validate_etype2_capture.py`, `validate_cs_sparsity.py`, `test_beamforming_math.py`, `rt_smoke_test.py`.

### Skip unless specifically needed
- `src/original/` — inherited `StochasticRTcomparison` baseline stack (DeepMIMO + stochastic 3GPP); mostly superseded.
- `src/data/`, `src/checkpoint/`, `src/results/`, `src/logs/` — generated artifacts (datasets, weights, JSON metrics, figures), not code.

## Environment
- Single conda/mamba env named **`venv`** (at `C:\Users\javid\miniforge3\envs\venv`) — NOT the README's
  two-env split. One combined env: `sionna 2.0.1` RT (Mitsuba/Dr.Jit backend, no TensorFlow) + `torch ...+cu126`.
  Requirements consolidated in `csi_isac/venv.txt`.
- Activate (PowerShell):
  ```
  mamba.exe shell hook -s powershell | Out-String | Invoke-Expression
  mamba activate venv
  ```
- **GPU driver constraint:** Sionna RT OptiX needs a CUDA-12.6-era driver (**560.94**). Newer drivers
  (610.x / CUDA 13.3) break the OptiX PTX compile. Keep 560.94. The harmless `jitc_llvm_init failed`
  LLVM warning (unused CPU backend) can be ignored.

## Conventions
- Cell-style runners use `#%%` blocks. SI units (meters, Hz). Datasets are sharded `.npz` + a `meta.json` sidecar.
- Verify memory-note `file:line` claims against current code before relying on them — notes are point-in-time.
- **Doc edits are seamless, not annotated:** when the user asks a question or makes a suggestion, fold the
  answer/change into the existing prose as if it had always been written that way. Do NOT quote the question
  back, do NOT add meta-notes about the change ("Notation warning", "As you asked…", "Note: renamed X to Y"),
  and do NOT leave changelog-style markers in the doc. Only add such a note if explicitly told to.
- **Never duplicate what the doc already says:** before adding anything, check whether the point is already
  covered. If it is, say so in chat and leave the doc alone, or sharpen/extend the existing passage in place.
  Add a new paragraph only when the information is genuinely new.
- **Math notation:** in the walkthrough doc (`thesis_code_walkthrough_QA.md`) write math in LaTeX (`$…$` inline, `$$…$$` display). In terminal/chat replies write math as PLAIN TEXT — the user cannot read LaTeX in the terminal. User is a non-native English speaker: avoid metaphorical/uncommon words (e.g. "knob"); if unavoidable, define inline.
- **Markdown math delimiters — the parser decides what is math before the LaTeX is ever read**, so valid
  LaTeX still renders raw if the delimiters break these rules. A closing `$` must NOT be followed by a
  letter or digit, an opening `$` must not be preceded by one, and neither may have a space just inside it:
  write `$1\ \mu\text{s}$`, never `$1\ \mu$s`; write `$\sim 230$ m`, never `$\sim$230 m`. A `$$…$$` display
  block must fit on ONE line — if it wraps, it renders as literal text. Verifying that an expression is
  valid LaTeX (e.g. with KaTeX) does NOT catch any of this; check the delimiters separately.
