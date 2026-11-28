---
name: Debugging lessons from Phase 3
description: maplibre-gl CSS must be explicitly imported, headless Chrome can't render WebGL screenshots, Popup closeOnClick default behavior
type: feedback
---

## 1. maplibre-gl CSS must be explicitly imported in user code

maplibre-gl's CSS file (`maplibre-gl/dist/maplibre-gl.css`) does not auto-load; it must be manually `import`ed at the application entry point. Missing CSS makes the map canvas invisible (no position/size styles), but Popup/Marker Teleport content may still appear (since they are independent DOM nodes).

**Why:** maplibre-gl JS only creates DOM structure and binds logic; visual styles depend entirely on external CSS. This is consistent with mapbox-gl behavior. react-map-gl also doesn't auto-import CSS.
**How to apply:** playground/src/main.ts already has the import. When writing docs or examples in the future, remind users they must import CSS themselves.

## 2. Headless Chrome cannot capture WebGL canvas

`google-chrome --headless=new --screenshot` cannot render WebGL canvas content; screenshots are always white/blank even when the map works in a real browser. `--use-gl=angle` / `--use-gl=swiftshader` are both ineffective. `--dump-dom` with `--virtual-time-budget` also cannot wait for async dynamic imports to complete.

**Why:** Headless Chrome's screenshot pipeline doesn't support WebGL rendering; this is a known Chromium limitation.
**How to apply:** Don't use headless screenshots to diagnose map rendering issues. Instead check: (1) JS console errors (2) DOM structure (whether canvas exists) (3) whether CSS is loaded. If visual verification is needed, have the user check in a real browser.

## 3. Popup closeOnClick defaults to true

The Popup component's `closeOnClick` default value is `true` (consistent with maplibre-gl native behavior). Clicking anywhere on the map will close the popup. If you only want to close via the X button, explicitly set `:closeOnClick="false"`.

**Why:** Consistent with the underlying maplibre-gl Popup constructor default.
**How to apply:** The playground example already sets this to false. Documentation should explain this default behavior.
