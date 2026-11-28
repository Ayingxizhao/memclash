---
name: External service credentials and endpoints
description: Locations of API tokens, secrets, and service endpoints for the postflow project
type: reference
---

- **Feishu app**: managed at https://open.feishu.cn/app, app name "测试应用"
- **Cloudflare**: Worker "lark-postflow-bridge", KV namespace IMAGE_CACHE
- **Worker URL**: https://bot.akbot.top (custom domain, primary)
- **Domain**: akbot.top (DNS on Cloudflare)
- **Meta App**: "MyFirstTest" (Development mode), App ID 326293570148
- **Instagram Business Account**: tktx03 (ID: 17841441880533108), linked via Facebook Page "MyPage" (ID: 992021360669625)
- **Meta token**: long-lived (60 days), expires ~2026-05-23, stored in .env as META_ACCESS_TOKEN
- **Local secrets**: D:\bs\.env (LARK_APP_ID, LARK_APP_SECRET, GITHUB_PAT, CLOUDFLARE_API_TOKEN, META_APP_ID, META_APP_SECRET, META_PAGE_ID, META_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID)
- **GitHub secrets**: BSKY_HANDLE, BSKY_PASSWORD, GEMINI_API_KEY, UNSPLASH_ACCESS_KEY, META_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID
