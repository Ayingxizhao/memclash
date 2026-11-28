---
name: walkthrough-html-render
description: "How the walkthrough doc is turned into a phone-readable HTML page: MathML at build time, inlined SVGs, tools/render_walkthrough.py"
metadata: 
  node_type: memory
  type: project
  originSessionId: f613f78b-84ad-430d-b890-1e6c3d164eb1
  modified: 2026-08-03T02:12:38.393Z
---

`tools/render_walkthrough.py` in the CSI-ISAC repo builds `thesis_code_walkthrough_QA.html`
from the Markdown doc: one self-contained 1.7 MB file, no network, no scripts for maths.
Run from the repo root: `python tools/render_walkthrough.py` (needs `pip install markdown
latex2mathml`, both already in `venv`). `--frag` emits page-content-only for publishing as
an Artifact. Published 2026-08-03 at
https://claude.ai/code/artifact/c485922a-4892-4510-8ec9-c7443772d39a (private; republish the
same file path to keep the URL).

**Why:** the user reads the doc on an Android phone, where GitHub's app does not render
LaTeX at all and the web view renders it only in the blob view, never in diffs.

**How to apply:** maths is converted to **MathML at build time**, NOT with MathJax — a
MathJax build was tried first and the page never finished typesetting its ~1974 expressions.
`latex2mathml` converts all 1974 with zero failures, including `\boxed`, `\operatorname`,
`\bigl`. Gotchas baked into the script, do not regress them: fenced code blocks and inline
`code` spans must be stashed before any `$` rule; inline math wraps across source lines
(the doc is hard-wrapped) so the inline pattern must allow a newline but not a blank line;
image alt text contains balanced brackets (`x_i[n]`, `out[o,i,j]`) so the image regex must
tolerate them or those three figures silently vanish. See [[csi-isac-github-repo]] for the
clone-copy-commit push workflow and [[walkthrough-explanations-in-doc]] for the doc itself.
