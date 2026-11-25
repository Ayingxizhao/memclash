---
name: Working Preferences
description: How TSIKanati likes to work with Claude, confirmed patterns, things to avoid
type: feedback
---

Concise, direct responses — skip preamble. Lead with action, not explanation.

**Why:** TSIKanati is an experienced developer who reads code faster than prose. Verbose explanations slow things down.
**How to apply:** Use tools first, explain after only if something is non-obvious. Never say "Let me now..." — just do it.

---

Session logs appended to CLAUDE.md after every major work session. Format matches existing table style in CLAUDE.md.

**Why:** CLAUDE.md is the living knowledge base. Keeping it current ensures future sessions have full context.
**How to apply:** After completing a substantial feature/session, add a "## File Modifications Log" section to the root CLAUDE.md with the date and table of files changed.

---

Production-ready code, not scaffolds. When building features, implement the full thing.

**Why:** TSIKanati deploys immediately from what Claude produces. Half-implementations create more work.
**How to apply:** Don't stub out functions. If you write a route, write real logic. If you write a service, wire it into the server.

---

Always `pm2 save` after any PM2 changes.

**Why:** pm2-resurrect service depends on the saved process list. Missing this step means processes don't survive reboots.
**How to apply:** Every time a PM2 process is started, stopped, restarted, or deleted — end with `pm2 save`.

---

Always update port-registry.json when claiming a new port.

**Why:** Single source of truth. Server health check reads this file. Prevents port conflicts.
**How to apply:** Before assigning any port, check port-registry.json. Claim it there, update nextAvailable.

---

GitHub CLI (`gh`) is available and preferred for repo operations.

**Why:** Avoids needing to remember exact git remote URLs. TSIKanati has gh authenticated.
**How to apply:** Use `gh repo view`, `gh pr create`, etc. for GitHub operations.

---

Parallel tool calls preferred for independent operations.

**Why:** Speeds up multi-file reads, concurrent searches, etc.
**How to apply:** When reading multiple files or running multiple searches that don't depend on each other, issue them in one message.
