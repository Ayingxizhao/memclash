---
name: Feishu-to-Bluesky bridge architecture
description: CF Worker bridges Feishu→Bluesky via GitHub Actions. PR #12 merged. Next phase: Instagram (milestone due 04-03).
type: project
---

## Current Status (2026-03-23)
- PR #12 merged (squash) to master — Feishu bridge fully working
- Issues #7, #8 closed
- CLAUDE.md rewritten + docs/process.md created (three-AI collaboration)
- Template repo created: Akagilnc/project-template

## Architecture
Feishu group @mention → CF Worker (bot.akbot.top) → GitHub Actions repository_dispatch → post_bot.py → Bluesky

**Key constraints:**
- workers.dev and vercel.app blocked from China — custom domain on Cloudflare required
- Worker deployed via `wrangler deploy`, not GitHub Actions
- GitHub Actions runs master branch code, not feature branches
- Feishu 3s webhook timeout — async processing via ctx.waitUntil()
- Feishu retries for hours — dedup TTL 24h
- Group @mention works; direct bot messages do NOT (p2p permission issue)
- Bluesky ~1MB image limit — compression via Pillow (progressive quality + dimension halving)

## Next Phase
Milestone "Instagram 平台支持" (due 2026-04-03):
- #15 Meta OAuth 公共认证模块
- #16 Instagram Graph API 发帖实现
- #17 集成到 post_bot 和 GitHub Actions

Other milestones (TBD):
- "多图支持": #14, #18, #19, #20
- "Threads 平台支持": #6 (depends on #15)
