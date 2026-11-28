# Memory Index

- [feedback_monospace_font.md](feedback_monospace_font.md) — Use "Courier New" for monospace inputs, not generic `monospace`
- [feedback_mri_windowing.md](feedback_mri_windowing.md) — MRI viewer VOI must come from backend percentile stats, not cornerstone's reported min/max
- [feedback_cornerstone_z_flip.md](feedback_cornerstone_z_flip.md) — cornerstone reverses z when z-sign > 0; backend must use `_loader_slice_index` to compensate
