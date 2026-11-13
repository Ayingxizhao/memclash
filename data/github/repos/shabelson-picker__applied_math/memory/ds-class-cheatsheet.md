---
name: ds-class-cheatsheet
description: The HIT Data Structures class (sem3) — its own project, separate from the AofA course; master cheat sheet lives at sem3/data structure/cheatsheet.md
metadata:
  type: project
---

The **HIT Data Structures class** (sem3, graded, exam-bearing) is a *separate* project from
the self-paced [[aofa-course]], even though both live under `sem3/data structure/`.

**Layout:**
- `ex1/`–`ex5/` — tirgulim + solutions (1 exact running time, 2 O/Ω/Θ/o/ω, 3 stack & queue,
  4 linked list, 5 binary trees, 6 BST). Sheets are Hebrew, code is English.
- `presentations/` — 12 Hebrew lecture decks: complexity A/B, divide & conquer, stack/queue
  (with amortized analysis), linked lists, trees A/B/C, AVL, heap, hashing, union-find,
  comparison-sort lower bound + non-comparison sorts.
- `extra/Cormen Introduction to Algorithms.pdf` — **CLRS**, the reference text for this class.
- `course/` — the unrelated AofA self-study course.
- `cheatsheet.md` — **the master sheet** (written 2026-08-29), modelled on the
  `sem2/Series and Integral Transforms/theorems.md` sheet: topic sections, tables,
  "Common mistake" callouts, an exam workflow table up front, a one-page recall at the end,
  and §17 mapping every section to its CLRS chapter for when the sheet is too shallow.

**Conventions in the sheet:** LaTeX math as `\( … \)` inline / `$$ … $$` display so the
vendored `course/tools/render-pdfs.sh` pipeline can typeset it; course conventions
`h(empty) = −1`, 0-based heap indexing `left(i)=2i+1`. Cf. [[no-latex-explanations]] —
that rule governs *chat*, not these files.

**Rendered:** `cheatsheet.pdf` (15 pages, A4). Two-step build, since
`tools/render-pdfs.sh` only walks files under `course/`:
`node course/tools/render.mjs cheatsheet.md <tmp>.html cheatsheet`, then headless Chrome
`--print-to-pdf`. Re-run both after editing the markdown. Diagrams are ```mermaid fences
(MathJax has no TikZ); they render as vector SVG. Verify a render with
`pdftotext cheatsheet.pdf - | grep -c 'graph TD'` — a nonzero count means mermaid failed
and leaked its source into the page.

**Keep toolchain notes OUT of the sheet itself** — the user cut a line explaining the
mermaid/MathJax choice from §11: build details belong here, not in a revision document.

## Status (last session 2026-08-29)

`cheatsheet.md` complete, 20 pages, §§0–17. §11 (AVL) is the only section expanded beyond
base depth — 11.1 invariant · 11.2 the N(h)=N(h-1)+N(h-2)+1 → Fibonacci height proof ·
11.3 rotation mechanics · 11.4 the four cases with mermaid before/after diagrams ·
11.5 worked insertions · 11.6 insert-vs-delete asymmetry · 11.7 exam procedure.
Other sections can be expanded the same way on request.

**Finding to remember:** the course AVL slide states h ≤ 1.44·lg(n+2) − 0.328. That is valid
but slack by ~1 under the course's own h(∅) = −1 convention (tight constant: −1.3277); the
−0.328 form is the classical statement, which counts a leaf's height as 1. The sheet quotes
the slide's version, with the discrepancy noted, so it matches the exam.

**Open threads:**
- Terminal width that renders cleanly for this user — asked twice, never answered. Keeping
  chat lines narrow (~70 chars) and avoiding wide markdown tables in the meantime.
- Loop-complexity work also lives in the AofA course as expansion 0a (see [[aofa-course]]),
  which is written but unread — sessions 0a.1–0a.3 are queued in `course/PROGRESS.md`.
- `course/SYLLABUS.md` still describes the Sedgewick-Flajolet chapter-per-module structure and
  needs re-mapping onto CLRS after the 2026-08-29 text change.


## Exam prep (started 2026-09-12, test ≈ 2026-09-29)

Plan: week 1 = seven topic sessions (S1 complexity+asymptotics, S2 stack/queue/lists,
S3 trees+BST, S4 AVL, S5 heap+sort bound, S6 D&C, S7 hashing+union-find), week 2 = full
past exams from `tests/`, last 3 days = §16 recall + bonus T/F. Exam format: 4×25 pts +
15-pt T/F bonus. The `presentations/` folder lacks the first deck (פונקצית זמן ריצה).
Progress: 2026-09-13 — Tirgul 5 Q2 (leaf counting, full vs complete) done in depth; the
user had the tree-counting formulas mixed (2^h leaves / 2^h−1 internal / 2^(h+1)−1 nodes /
(n+1)/2 leaves in a full tree) — check-yourself rule agreed: plug h=1 or n=3 in the margin.
Next: Tirgul 5 Q3 onward; proof practice per [[ds-formal-proof-practice]].
