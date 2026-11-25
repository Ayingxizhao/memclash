---
name: release-modifiers-after-a-chord
description:
  "after peekaboo press ctrl+c (or any chord), run cliclick ku:ctrl ku:cmd ku:alt ku:shift; a stuck
  modifier turns every later click into a control-click."
metadata:
  type: feedback
---

After a `peekaboo press` chord, release the modifiers with `cliclick ku:ctrl ku:cmd ku:alt
ku:shift` before the next click. On 2026-10-02 `peekaboo press ctrl+c` into Android Studio's
terminal left Control down: three clicks on an AdvantageScope tree triangle did nothing, and the
next click opened a context menu, which is what a control-click does. Releasing the keys fixed it at
once.

**Why:** the symptom looks like a missed coordinate, so the obvious response is to re-aim, and every
re-aim fails the same way.

**How to apply:** any click that opens a context menu, or a tree that will not expand, means check
the modifiers first. The `mac-gui-automation` skill does not say this yet; adding it is an amendment
for Mike to agree, per [[one-fact-one-home]].
