---
name: feedback_mri_windowing
description: MRI viewer VOI must come from backend percentile stats, not cornerstone's reported min/max
metadata:
  type: feedback
---

Always derive the MRI window/level (VOI) from backend-computed intensity stats, not from `image.minPixelValue`/`image.maxPixelValue` reported by `cornerstone-nifti-image-loader`.

**Why:** The loader returns 0/0 for min/max on many NIfTI files, causing `windowWidth = 1` and a completely black image.

**How to apply:** The `/raw/info` and `/{project}/{mrid}/info` endpoints return `vmin`/`vmax` (1st–99th percentile of non-zero voxels, computed via nibabel). `MriViewer.tsx` uses these to set `vp.voi`, with cornerstone's values as a fallback.
