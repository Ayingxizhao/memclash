---
name: Avoid time-sampled visibility for spawning particles
description: Time-sampled visibility causes particles to reappear when timeline loops in Omniverse
type: feedback
---

Do not use `visibility.timeSamples` or `rigidBodyEnabled.timeSamples` to stagger particle spawning.

**Why:** When the Omniverse timeline loops, time samples reset — particles go invisible at frame 0 then reappear, causing a visual glitch. The user reported "why there are reappearing?"

**How to apply:** Instead of time samples, stagger particles by vertical height and let gravity create natural arrival timing. Higher particles take longer to fall = same effect, no timeline dependency.
