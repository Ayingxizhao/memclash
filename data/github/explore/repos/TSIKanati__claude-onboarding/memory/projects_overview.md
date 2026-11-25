---
name: Projects Overview
description: All active projects, their purpose, priority, and current state
type: project
---

## Priority Tiers

**P0 — translatorseries.com**: TSI main app (MariaDB, port 3000). Core business.

**P1 — Active platforms**:
- `clieair.com` (port 8000) — v2.0.0 constitutional enforcement, 52 AI agents, self-dev pipeline
- `charitypats.com` hub — autozen (3012), flightdeck (3015), thebridle (3020), otwh (3007), studio (3028)
- `tsinc.urbot.net` (port 3022) — Brain Empire, 293 agents, Atlas autonomous training
- `urbot.net` ecosystem (ports 3021-3032) — 84 bots, billing, P2P, royalties

**P2 — Maintained**:
- `onthewayhome.charitypats.com` (port 3007)
- `quantumledgerbookkeeping.com` (port 3005)
- `realworldprizes.com` (port 3003)

**P3 — Legacy/Stable**:
- `machinistzen.com` IMS (port 3001) — Living Dashboard, 61 tiles, Spindle Pete

**P4 — Static/No backend**:
- `transyndicate.com` — static only

## URBot.net — The Big Picture

84 bot subdomains, 8 active backends, 3 databases, Atlas AI training the bots 24/7.

Revenue model: $1/$5/$20 tiers via Stripe. Ecosystem tracks royalties in UBT tokens.
PeerPower: purchased bots can form a federated P2P network using their Ed25519 identities.
TSInc Brain Empire: private enterprise command center with 3D visualization and swarm AI.

## Atlas Self-Dev System (tsinc-api, port 3022)

Three autonomous training layers:
1. Bot Self-Developer: hourly, fills knowledge gaps across 78 bots
2. Training Reviewer: hourly at :50, QA gate for 7900 XT training jobs
3. Atlas Dispatch/Implement: 4h cycle — generates Qwen prompts → 7900 XT → implements Q&A pairs

Learning state: `training/atlas-learning-state.json` — persists across restarts.

## URMovie Creative Studio (port 3028)

12-stage pipeline: ADLIB_ANALYZE → RESEARCH → OUTLINE → CHARACTER_MAP → STORYLINE_PLAN → DRAFT → BOT_COLLAB → FACT_BLEND → REVIEW → REVISION → STORYBOARD → PRODUCE

16 cc_* database tables in urbot_billing. Revenue split: 50% creator / 50% platform on rentals.

## Last Major Sessions

- 2026-02-13: Port registry, CLAUDE.md, health check created
- 2026-02-14: IMS Living Dashboard (61 tiles, SVG icons, tile intelligence ML)
- 2026-02-17: Sally security hardening (webhook auth, health endpoint, Plesk panel)
- 2026-02-18: URBot billing system deployed
- 2026-02-20: PeerPower P2P ecosystem full scaffold (Rust workspace + Node registry)
- 2026-02-22: Atlas self-dev system (3-layer autonomous training pipeline)
- 2026-02-24: Personalized bot experience (6 phases, 204 files changed)
- 2026-02-25 (AM): CLIEAIR v2.0.0 full overhaul (constitutional enforcement)
- 2026-02-25 (PM): URMovie Creative Studio full build

**Why:** These sessions represent cumulative production work. Any new work builds on all of the above.
