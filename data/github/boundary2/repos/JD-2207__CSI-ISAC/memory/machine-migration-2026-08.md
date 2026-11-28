---
name: machine-migration-2026-08
description: "2026-08-12 OS reinstall: paths moved Fernando -> javid, env rebuilt with relaxed pins, driver still 610.88"
metadata:
  type: project
---

On 2026-08-12 the PC died and Windows was reinstalled under a new account. Everything moved:

- Project: `C:\Users\Fernando\Documents\CSI` -> `C:\Users\javid\Documents\Javier\CSI`.
- Home: `C:\Users\Fernando` -> `C:\Users\javid` (env now `C:\Users\javid\miniforge3\envs\venv`).
- Claude home restored from a backup at `C:\Users\javid\Documents\Javier\.claude` (kept as the only
  copy of the pre-crash state — do not delete). All 7 old transcripts, the 37 memories and the prompt
  history were path-rewritten into `c--Users-javid-Documents-Javier-CSI`. Old `*.log` files under
  `src/data/` still contain the original Fernando paths on purpose (they are historical records).

The `venv` env was rebuilt from scratch, so it is NOT byte-identical to the pre-crash one:
`torch 2.13.0+cu126`, `numpy 2.2.6` (deepmimo pin, as before), `scipy 1.17.1`, `h5py 3.16.0`,
`matplotlib 3.11.1`, `ipywidgets 8.1.8`. Those five pins in `venv.txt` (`scipy==1.15.1`,
`h5py==3.12.1`, `matplotlib==3.10.0`, `ipywidgets==8.0.5`, `jupyterlab-widgets==3.0.5`,
`ipydatawidgets==4.3.2`) are now unsatisfiable — sionna 2.0.1 / sionna-rt require
`h5py>=3.15.1` and `ipywidgets>=8.1.5`, so a plain `pip install -r venv.txt` fails with
ResolutionImpossible. Verified working: dataset load + GPU train step + checkpoint load.
The `scene.preview()` pythreejs viewer has NOT been re-verified under the newer widget stack.

The driver shipped as 610.88 and was downgraded back to **560.94** (RT verified: `rt_smoke_test.py`
passes, OptiX compiles). NVIDIA's driver-search page no longer lists anything below 590, but the
installers are still on the CDN — direct URL pattern
`https://us.download.nvidia.com/Windows/<ver>/<ver>-desktop-win10-win11-64bit-international-dch-whql.exe`
(signature verified NVIDIA Corporation). Windows Update will re-push 610.x unless optional driver
updates stay off.

Git had to be reinstalled from scratch (git 2.55.0 + git-lfs 3.7.1, via winget); the repo itself and
its ~63 uncommitted working changes survived, with `origin` still upstream `jmoraispk` as
[[csi-isac-github-repo]] records. Restore is complete — nothing outstanding.
