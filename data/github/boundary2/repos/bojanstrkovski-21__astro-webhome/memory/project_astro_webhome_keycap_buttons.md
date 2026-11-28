---
name: project-astro-webhome-keycap-buttons
description: Keycap-style button redesign for .link-item/.service-button/.search-btn — current state and how it was built
metadata: 
  node_type: memory
  type: project
  originSessionId: 37b80f78-a56f-4059-a23f-26598f5c9ccf
  modified: 2026-09-18T12:05:14.606Z
---

All clickable link/service/search buttons (`.link-item` on index/institucii/linux, `.service-button` on e-servisi, `.search-btn` on index) were redesigned to mimic the "Keyboard Keys Style Button Dark Color" from css-buttons.com/buttons/136. The original demo's `.btn-136` is sized for an 80px square key — sizes/insets here are scaled down/adapted per button, not copied verbatim.

Markup: each button is `<a>`/`<button>` containing `<span><i>Label</i></span>` (real DOM elements, not `::before` overlapping the anchor) — this real-span approach was adopted after a `::before`-on-the-anchor version caused a z-index/stacking bug (text rendered behind the bevel layer). Span = the lighter inset "bevel" surface (positioned via `::before` insets relative to span, or as the span itself depending on iteration — check current Layout.astro for exact state); `<i>` = the text, styled with `font-family: var(--font-family)` (respects the font toggle) and `font-weight: 600`.

Colors were ported from literal grayscale hex (#282828/#202020 outer, #232323/#4a4a4a bevel, #fff text) to Everforest vars: outer gradient `var(--bg1)`→`var(--bg-dim)`, bevel gradient `var(--bg2)`→`var(--bg4)`, text `var(--fg)`.

**Superseded twice since**: styling is no longer theme-agnostic, and `.search-btn` no longer even shares the keycap shape. As of [[project-astro-webhome-redesign]], `.link-item`/`.service-button`/`.search-btn` each had explicit `[data-theme="transparent"]` (frosted glass: translucent gradient, `backdrop-filter: blur(14px) saturate(140%)`, light border) and `[data-theme="solid"]` (same shape, no blur) blocks in Layout.astro. Then, as of [[project-astro-webhome-search-dropdown-rebuild]] (2026-09-18), `.search-btn` was pulled back OUT of the keycap treatment entirely and given a flat, bordered style matching `.search-input`/the engine dropdown beside it instead — `.link-item`/`.service-button` still use the rounded frosted-glass keycap look, `.search-btn` does not anymore.

Known tuning so far (may have shifted since — verify against Layout.astro): `.link-item` min-height 60px, font-size 14px; `.service-button` min-height 80px, font-size 14px (e-servisi explicitly asked to match link-item's font); `.search-btn` is now flat/bordered at a fixed 29px height matching the search input and dropdown, not the keycap sizing this entry originally described. All use font-weight 600/700.

A backup of one finished iteration was saved to [src/styles/keycap-buttons.backup.css](src/styles/keycap-buttons.backup.css) (not imported, reference only) before the colors were ported to Everforest — CLAUDE.md notes it predates the current per-theme split.

See [[feedback-astro-webhome-iteration-style]] for how the user directs these tweaks, [[project-astro-webhome-redesign]] for the frame/tab history, and [[project-astro-webhome-search-dropdown-rebuild]] for why `.search-btn` diverged from this pattern.
