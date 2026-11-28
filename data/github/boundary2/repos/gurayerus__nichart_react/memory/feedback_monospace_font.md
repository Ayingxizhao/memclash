---
name: feedback_monospace_font
description: Use "Courier New", Courier, monospace for monospace-styled inputs — generic monospace makes underscores invisible on some systems
metadata:
  type: feedback
---

Use `fontFamily: '"Courier New", Courier, monospace'` for any input or text that needs monospace styling.

**Why:** Generic `monospace` maps to different system fonts (Monaco on macOS, Consolas on Windows, etc.) where underscores render very faintly or at the baseline and appear as spaces. Confirmed broken on this project with MRID inputs like `023_S_6346`.

**How to apply:** Any time `fontFamily: "monospace"` would be used in a `styles` or `style` prop on an input or text element, use the explicit Courier New stack instead.
