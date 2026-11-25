---
name: GitHub Repositories
description: All TSIKanati repos, branches, server paths, and sync workflow
type: reference
---

## Repositories

| Repo | Primary Branch | Server Path | Notes |
|------|---------------|-------------|-------|
| `TSIKanati/URBot` | `main` + `tsinc` | `C:\inetpub\vhosts\urbot.net\httpdocs\` | Monorepo: 84 bot subdomains, billing, ecosystem. `tsinc` branch = Brain Empire 3D Highrise |
| `TSIKanati/tsinc-enterprise` | `main` | `C:\inetpub\vhosts\urbot.net\tsinc.URBot.net\` | Brain Empire command center — 293 agents, Atlas self-dev, training pipeline |
| `TSIKanati/URBot-PeerPower` | `main` | `C:\inetpub\vhosts\urbot.net\peerpower\` | Rust workspace (10 crates) + Node.js P2P registry. Own repo, excluded from urbot.net .gitignore |
| `TSIKanati/CLIEAIR` | `main` | `C:\inetpub\vhosts\clieair.com\httpdocs\` | v2.0.0 constitutional enforcement platform (Python FastAPI) |
| `TSIKanati/IMS-MachinistZen` | `main` | `C:\inetpub\vhosts\machinistzen.com\IMS.Machinistzen.com\` | IMS + Wendy bot + Sally endpoint |
| `TSIKanati/TheBridle` | `main` | `C:\inetpub\vhosts\charitypats.com\thebridle.charitypats.com\httpdocs\` | TheBridle Next.js frontend |
| `TSIKanati/claude-onboarding` | `main` | `C:\inetpub\vhosts\onboarding\` | This repo — local Claude Code onboarding |

## Sync Workflow

```bash
# Standard: edit locally → push → pull on server
git add <files> && git commit -m "message" && git push

# On server (via SSH):
git -C "C:/inetpub/vhosts/<project-path>" pull origin main
pm2 restart <name>
pm2 save
```

## Important Repo Notes

- `urbot.net/peerpower/` has its own `.git` — NOT tracked by parent urbot.net repo
- `tsinc` branch of URBot repo has the Highrise 3D code (Three.js + command center)
- After pushing tsinc-enterprise changes, the server's `tsinc-api` PM2 process needs restart
- CLIEAIR uses Python venv — after pulling, may need `pip install -r requirements.txt` in `api/venv/`

## GitHub CLI Setup

```bash
gh auth login   # use browser flow
gh repo list TSIKanati --limit 20
```
