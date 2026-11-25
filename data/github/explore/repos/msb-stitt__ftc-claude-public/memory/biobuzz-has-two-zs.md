---
name: biobuzz-has-two-zs
description:
  "The robot-code subproject is ftc31459-26-27-biobuzz, after this year's FTC game BIOBUZZ; the
  one-z spelling biobuz was a mistake, and some copies of it may remain."
metadata:
  type: project
---

The subproject is **`ftc31459-26-27-biobuzz`**, two z's, because this year's FTC game is called
BIOBUZZ. For a while this project spelled it `ftc31459-26-27-biobuz`, and the rename to two z's,
begun in `77fc139` on 2026-10-01, may not have caught every copy.

**Why:** the user (Mike), 2026-10-02: *"at one time we were spelling ftc31459-26-27-biobuz wrong,
this years FTC game is called BIOBUZZ, we have been renameing to ftc31459-26-27-biobuzz, but may
not have fixed all current misspellings."*

**How to apply:** write two z's. A path, command or link that names the one-z spelling points at a
directory that is no longer there, so treat it as the misspelling rather than as a second
subproject. `git grep -nE 'biobuz([^z]|$)'` finds what is left, so no count is kept here, per
[[derive-dont-maintain]]. A copy found outside the task in hand is reported rather than fixed, per
the Constitution's *Touch only what the task requires*.
