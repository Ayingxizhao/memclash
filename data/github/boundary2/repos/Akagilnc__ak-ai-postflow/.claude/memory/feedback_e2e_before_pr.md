---
name: End-to-end tests required before PR
description: Must run all E2E paths (manual + auto trigger) before submitting PR, not just one path
type: feedback
---

PR 前必须跑完所有主要路径的端到端测试，不能只测一条路径就提 PR。

**Why:** 自动触发路径（Gemini 生成文案 + Unsplash 配图）和手动触发路径（指定 content + image_url）走的代码分支不同。只测手动路径会漏掉自动路径的 bug（如 Unsplash URL 未保留导致 Instagram 跳过）。

**How to apply:** PR 前列出所有触发路径，逐一验证。至少包括：手动指定内容、自动生成内容、各平台组合。
