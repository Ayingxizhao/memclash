---
name: Server Infrastructure
description: VPS details, services running, architecture pattern, Plesk, IIS, PM2
type: project
---

**Server**: Windows Server 2022 Standard (10.0.20348)
**IP**: 72.167.227.50
**PM2 User**: tsikanati
**Node**: v24.0.0
**Hosting**: Plesk panel on HTTPS port 8443 (HTTP 8880 blocked)

**Architecture pattern**: Internet → IIS (port 80/443) → web.config URL Rewrite → localhost:{PORT} ← PM2-managed process

**Active PM2 processes** (as of 2026-03-02):
tsiapp (3000), ims-api-production (3001), ims-wendy-switchboard (3002), realworldprizes (3003), ideallearning (3004), quantumledger (3005), otwh-api (3007), autozen (3012), tsi-flightdeck (3015), thebridle-frontend (3020), urbot-billing (3021), tsinc-api (3022), urbot-peerpower (3023), urbot-ecosystem (3024), urbot-mountain-safety (3025), urbot-podcast (3026), urbot-diplomat (3027), urbot-studio (3028), clieair (8000)

**Windows services**:
- W3SVC (IIS): RUNNING
- Redis: port 6379, RUNNING
- postgresql-x64-16: port 5432, RUNNING (primary)
- postgresql-x64-13: port 5433, RUNNING (legacy tsinc_enterprise)
- MariaDB114: port 3307, RUNNING
- MariaDB: port 3306, START_PENDING (known issue — non-blocking)
- ClaudeAgentServer: port 5000, RUNNING (IMS Claude agents)
- MachinistZenFlask: RUNNING
- pm2-resurrect: PAUSED (by design — manually run `pm2 save` after changes)
- CLIEAIR: PAUSED (PM2 manages instead)

**Security hardening done (2026-02-17)**:
- FTP disabled, SFTP only
- Sally webhook: X-Telegram-Bot-Api-Secret-Token required
- IMS /health: minimal unauth response
- X-Powered-By headers removed from Sally
- Plesk panel: brute-force protection + HTTPS redirect

**Why:** IIS reverse proxy pattern was established to work with Plesk's domain management while allowing PM2 to own process lifecycle. ESM modules require pm2-entry.mjs wrappers (PM2 can't natively run ESM).
**How to apply:** Always check port-registry.json before assigning ports, always run `pm2 save` after changes, always use icacls to grant tsikanati access when Plesk creates files.
