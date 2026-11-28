---
name: reference-astro-webhome-visual-testing
description: "How to spin up a headless browser to screenshot-verify CSS/layout changes in this repo, on either machine it's worked from"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 37b80f78-a56f-4059-a23f-26598f5c9ccf
  modified: 2026-09-18T12:05:33.992Z
---

This project is worked on from at least two machines (Linux and this Windows one) — the setup differs per machine, so check which one you're on before following either recipe.

**On the Linux machine**: has system Chromium at `/usr/bin/chromium` and no global Playwright — install `playwright-core` (lighter than full `playwright`, no bundled browser download needed since it points at system Chromium) per-session in /tmp (not the project) and point `chromium.launch` at the system binary, with `--no-sandbox` in that sandboxed shell environment:

```
mkdir -p /tmp/pw-shot && cd /tmp/pw-shot && npm init -y >/dev/null 2>&1 && npm install playwright-core --no-audit --no-fund
```

```js
const { chromium } = require('playwright-core');
const browser = await chromium.launch({ executablePath: '/usr/bin/chromium', args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width: 420, height: 600 }, deviceScaleFactor: 2 });
await page.goto('http://127.0.0.1:4321/', { waitUntil: 'load', timeout: 15000 });
await page.evaluate(() => { window.switchTheme('solid'); window.switchFont('meslo'); }); // optional
await page.screenshot({ path: '/tmp/pw-shot/out.png' });
```

Prefer `npm run build && npm run preview -- --port <N> --host 127.0.0.1` over `astro dev` for screenshotting there. Astro 7's `astro dev` (what `npm run dev` runs) daemonizes itself — the npm script process exits immediately after printing `Dev server running at http://localhost:4321 (pid ..., background)`, but the server keeps running (`npx astro dev status`/`stop`/`logs` to manage it). The catch: this daemon binds only `[::1]:4321` (IPv6 loopback), not `127.0.0.1` — `curl http://localhost:4321` still works (resolves to `::1` and the native client connects fine), but Playwright's Chromium in that environment fails to reach `::1` (`page.goto` times out on `localhost`, `ERR_CONNECTION_REFUSED` on `127.0.0.1`). `npm run preview` doesn't have this problem — pass `--host 127.0.0.1` explicitly and it binds there reliably.

`/tmp` gets wiped between sessions there — the playwright install and any saved scripts/screenshots need to be recreated each new session.

**On this Windows machine**: no system Chromium (`/usr/bin/chromium` doesn't exist, confirmed 2026-09-18), and `astro dev` binds fine on `localhost:4321` for both `curl` and Playwright — no IPv6-loopback issue seen here. Install the full `playwright` package (not `playwright-core`) ad hoc under the scratchpad temp dir and run `npx playwright install chromium` to fetch its bundled browser, since there's no system binary to point at:

```
mkdir -p /tmp/pw-verify && cd /tmp/pw-verify && npm init -y >/dev/null 2>&1 && npm install playwright@latest >/dev/null 2>&1 && npx playwright install chromium >/dev/null 2>&1
```

Then `require('playwright')` (not `playwright-core`) and `chromium.launch()` with no `executablePath` override. Screenshot files land under the Bash tool's `/tmp`, which maps to a real Windows path — resolve it with `cygpath -w "$(pwd)"` (or `pwd -W`) and Read the `.png` from that Windows path, not the posix one. Delete the temp install directory when done verifying, same as the Linux side.

One rendering caveat seen on this machine: headless/software-rendered Chromium may not actually apply `backdrop-filter` blur even when the CSS is correct (no GPU acceleration in this sandboxed environment) — don't over-tune opacity/blur values based on a headless screenshot alone if something still looks unblurred; a real GPU-accelerated browser may render it correctly. Prefer a background-opacity fallback that reads fine with or without the blur actually applying.

`window.switchTheme('solid'|'transparent')` and `window.switchFont('inter'|'meslo')` are exposed globally by Layout.astro's inline script — use them in `page.evaluate` to force a theme/font without clicking the UI toggle, on either machine.
