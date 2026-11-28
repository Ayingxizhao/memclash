---
name: project-astro-webhome-overview
description: "What astro-webhome is and its current structure (Astro bookmark dashboard, Everforest theme, two themes, font toggle)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 37b80f78-a56f-4059-a23f-26598f5c9ccf
  modified: 2026-09-18T12:04:59.692Z
---

astro-webhome is Bojan's personal bookmark/dashboard homepage built with Astro 7 (static output, deployed via Cloudflare Pages per wrangler.toml). Same repo is worked on from at least two machines — this Windows machine (`D:\My Backups\Bojan\astro-webhome`) and a Linux machine (`/home/bojanstrko/DATA/astro-webhome`, seen in an earlier session's memory) — kept in sync via git; see [[feedback-sync-project-memory-mirror]] for how memory itself is kept in sync across machines via the repo's own `memory/` folder. Pages: index (home, email/info/cloud/webapps link groups + search bar), e-servisi (government e-service buttons, no page title), institucii (ministries/institutions/banks, tabbed, no page title), linux (distro/news/forum/github links, tabbed, no page title). `.page-header` (the old on-page `<h1>` title) was removed from all three non-home pages and its CSS deleted — don't reintroduce without re-adding a template usage.

Styling lives almost entirely in [src/layouts/Layout.astro](src/layouts/Layout.astro) as one large `<style is:global>` block — pages just provide markup/data.

Two themes toggled via `data-theme` attribute, saved to localStorage key `theme`:
- `solid` — solid-bg.jpg background image, cards at 90% opacity (10% transparent), no blur/backdrop-filter (sun icon)
- `transparent` — self-hosted wallpaper.jpg background with translucent/blurred cards (moon icon)

Both themes now use a background image via the same `--bg-image` custom-property pattern (`url('/wallpaper.jpg')` vs `url('/solid-bg.jpg')`) — solid theme did NOT always have this, it was flat gradient-only until [[project-astro-webhome-redesign]]'s later session.

Color system: raw Everforest vars (`--bg-dim`, `--bg0`..`--bg5`, `--fg`, `--green`, etc.) defined once in `:root`, then semantic vars (`--primary-bg`, `--card-bg`, `--accent-bg`, etc.) redefined per `[data-theme]`.

Font toggle (separate from color theme) via `data-font` attribute, localStorage key `font`: `inter` (self-hosted via @fontsource/inter) or `meslo` (MesloLGS Nerd Font, self-hosted ttf in public/fonts/meslo/, copied from user's system fonts). Toggle buttons "in"/"me" sit next to the theme toggle in the nav.

See [[project-astro-webhome-keycap-buttons]] for the button redesign, [[project-astro-webhome-redesign]] for the fuller/more current redesign history (frames, tabs, backgrounds), [[project-astro-webhome-search-dropdown-rebuild]] for the search-row/dropdown followup, and [[reference-astro-webhome-visual-testing]] for how changes were verified.
