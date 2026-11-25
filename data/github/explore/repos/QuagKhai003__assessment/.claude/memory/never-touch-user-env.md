---
name: never-touch-user-env
description: "Never read or edit the user's .env; communicate config/secret changes via .env.example only"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 41ea88ec-b02d-4d56-870d-77f0c67c4730
  modified: 2026-08-14T06:32:53.237Z
---

Never read, open, `cat`, or `sed` the user's `.env` file — it holds their real Gemini API key/credentials and they don't want it exposed to the assistant. Never edit `.env` either. To tell the user what to change, edit `.env.example` (the safe committed template) with the right values + comments, or explain in chat; the user copies it into their own `.env`.

**Why:** `.env` holds secrets; the user explicitly asked me never to look into or modify it.

**How to apply:** for any env/config fix, update `.env.example` or describe the change in chat — never touch the real `.env`. Relates to [[never-commit-without-approval]].
