---
name: feedback-web-search
description: Do not run web searches without explicit user permission
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0915fc8d-24ef-4720-8196-bf8a16aec8a1
---

Do not run WebSearch or WebFetch without the user explicitly asking for it.

**Why:** User rejected web search tool calls mid-session — they did not ask to search the web, just asked a general question about finding better fixture models.

**How to apply:** When the user asks "can we find X" or "try to find X", respond with what you know and describe options. Only invoke WebSearch if the user explicitly says to search, look it up online, etc.
