---
name: no-figure-generator-scripts
description: "Don't write Python generator scripts for the explainer SVGs — edit figures/*.svg directly"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e9528d0e-6ba3-4347-a5f4-47b89c893666
  modified: 2026-08-10T17:10:40.780Z
---

The user does not want generator scripts for the figures. On 2026-08-10 they deleted the whole
`tools/` directory (`svg_kit.py` plus `gen_virt.py`, `gen_csirs_grid.py`, `gen_txchain.py`,
`gen_steering.py`) and said not to create more. The 21 SVGs in `figures/` are the artifacts; edit
them directly.

**Why:** the scripts were overhead the user never uses — they read and ship the SVG, not the code
that emitted it, so a second representation of the same figure is just something else to keep in
sync.

**How to apply:** when a figure in `literature/explainers/` needs changing, edit the `.svg` by hand
and re-render it (headless Chrome screenshot into an `<img>` wrapper page) to check the result
before claiming it is right. Do not propose reintroducing a build step. Note the cost this accepts:
figures are no longer reproducible from source, and `C:\Users\javid\Documents\Javier\CSI` is not a git
repo, so a bad hand-edit is not recoverable — read the region of the file being changed first.
Related: [[walkthrough-html-render]], [[5g-system-primer]].
