---
name: contentguard-rebuild
description: Goal/constraints of rebuilding GENZ-ContentGuard-AI as a Cloudflare demo in ~/dev/contentguard
metadata:
  node_type: memory
  type: project
  originSessionId: 01ef75b6-e33b-4b2e-8c2a-b22225f3cc22
  modified: 2026-10-18T04:03:35.241Z
---

As of 2026-10-17: rebuilding this old Flask project as a demo (not rigorous publication) in a new repo `/Users/yingxizhao/dev/contentguard`.
- Site: paste text → moderation verdict; also analyze a Reddit URL.
- Stack: single Cloudflare Worker (TS) serving static assets.
- LLM: user's own OpenAI-compatible provider; user supplies URL later.
- Caps approved: 10/IP/day, 200/day global (Durable Object counter) + Turnstile.
- Preserve: merged sarcasm-aware prompt, 7-category taxonomy, Gen Z lexicon (server-side only). Drop the immigrant "not malicious" prompt example.
- Steps: 0 scaffold+assets, 1 /analyze, 2 limits+Turnstile, 3 frontend, 4 Reddit (verify API access first), 5 optional eval set.

Status 2026-10-18: all steps built and running on real services locally (nothing committed yet).
- Secrets come from /Users/yingxizhao/dev/agents/.env (user said: load, never expose). LLM = freeinference.org/v1, model deepseek-v4-flash, key var MINIMAX_M3_API_KEY (same as user's agents project). User's Reddit app creds work with client_credentials.
- Real eval: AI 94% acc / 100% precision vs keyword 69% (38 cases).
- Added needs_support (crisis disclosure → OK + helplines) and moderator actions (Remove/Review/Flag/Allow).
- Remaining for user: Cloudflare login/deploy + real Turnstile widget, review prompt.md + eval labels, commit/GitHub.

Workflow: [[rebuild-workflow]]
