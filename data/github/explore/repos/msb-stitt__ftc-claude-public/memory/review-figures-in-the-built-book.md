---
name: review-figures-in-the-built-book
description:
  "Never ask Mike to approve a figure's stand-in text when the figure exists; show him the built
  book, with every figure in place."
metadata:
  type: feedback
---

When a figure has been drawn or taken, do not ask Mike to approve the words of its pencil box.
Put the picture in `corbels-lfs-lessons`' `figures/`, build the books with
`book/tools/publish_check.py`, and give him those to read.

**Why:** on 2026-10-16 Claude listed L020's pencil-box text as differences to approve, for figures
that were already drawn. His words: "you're asking me to approve stand in text for figures that
exists. That seems like a waste of time." He also called a step that ran the release build only to
watch it fail "make work that we don't really need to do".

**How to apply:** a review is of the books in `book/build/publish/`, which a release would publish.
The local `ninja book` shows pencil boxes in place of pictures, so it is not what Mike reviews.
