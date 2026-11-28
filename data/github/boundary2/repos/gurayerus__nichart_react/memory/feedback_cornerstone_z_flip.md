---
name: feedback_cornerstone_z_flip
description: cornerstone-nifti-image-loader reverses z-axis when z-sign is positive — backend must compensate with nz-1-z
metadata:
  type: feedback
---

When serving ROI mask slices, use `_loader_slice_index(affine, z, nz)` to map the slider index to the correct array index.

**Why:** `cornerstone-nifti-image-loader`'s `convertToNeurologicalView()` applies `steps[2] = -1` (reverses z) when the NIfTI orientation string z-sense is `'+'` (i.e. `nib.io_orientation(affine)[2,1] > 0`), so that the patient's head appears at the top. Without compensation, the mask tracks slices in the opposite direction from the displayed image. The MUSE atlas has z-sign = +1, so the flip is always needed for those files.

**How to apply:** Any backend endpoint that extracts a 2D slice by z-index for overlay on a cornerstone-rendered image must call `_loader_slice_index` before indexing into the array. The function is defined in `backend/routers/mri.py`.
