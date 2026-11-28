---
name: feedback-native-select-no-blur-custom-dropdown
description: "Native <select> popups can't take backdrop-filter; astro-webhome's engine picker is a custom div-based dropdown instead — watch for stacking-context traps when floating it over page content"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 37b80f78-a56f-4059-a23f-26598f5c9ccf
  modified: 2026-09-18T11:58:45.510Z
---

Native `<select>` dropdown popups are rendered outside CSS's reach for `backdrop-filter` in Chromium/most browsers — you cannot get a real frosted-glass blur on the native options list no matter what CSS is applied to `<select>`/`<option>`.

**Why**: User wanted the search-engine dropdown list frosted-glass to match the [[project-astro-webhome-search-dropdown-rebuild]] keycap buttons. Confirmed via `AskUserQuestion` that the user wanted a real custom dropdown (not a best-effort native-select fake) — built a div-based `.engine-dropdown-toggle` + `.engine-dropdown-list` widget in `Layout.astro`, with a hidden native `<select id="search-engine">` kept purely as the value store so `performSearch()` needed zero changes.

Two non-obvious traps hit while building it:
1. **Stacking context from `backdrop-filter`**: `.navigation` has `backdrop-filter: blur(10px)`, which creates a new stacking context. The dropdown list's `z-index: 50` only elevated it *within* that context — `<main>` (later in the DOM, no explicit z-index) still painted on top and ate clicks. Fix: give `.navigation` itself `position: relative; z-index: 10` so the whole header (dropdown included) sits above `<main>`.
2. **`hidden` attribute silently defeated by author CSS**: the browser's own `[hidden] { display: none }` rule and an author rule `.engine-dropdown-list { display: flex; ... }` have equal specificity, and author-stylesheet rules always beat the UA stylesheet regardless of specificity ties — so the list ignored `hidden` entirely and stayed visibly open. Fix: add `.engine-dropdown-list[hidden] { display: none; }` (higher specificity by one attribute selector) to force it closed.

**How to apply**: For any future "make this native form control's popup look like X" request in this project, assume it's not possible with the native element and ask whether a custom widget is wanted before building — same pattern as this one, see also [[feedback-verify-css-selectors-hit-real-dom]] for the general "verify the DOM/CSS interaction, don't assume" lesson. When floating any new absolutely-positioned panel over `<main>` in this layout, check whether an intervening ancestor has `backdrop-filter`/`filter`/`transform` creating a stacking context that traps your z-index.
