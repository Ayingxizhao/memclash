---
name: Local Machine Setup
description: ASUS ProArt StudioBook specs, tools, Ollama/GPU, workflow role
type: user
---

**Machine**: ASUS ProArt StudioBook — "Local Tower"
**OS**: Windows (fresh install after BitLocker recovery incident, 2026-03-25)
**GPU**: AMD Radeon RX 7900 XT — handles Atlas-dispatched LLM training jobs

## Local Services

| Service | Port | Purpose |
|---------|------|---------|
| Ollama | 11434 | LLM inference — model: qwen2.5:14b |
| CaricatureBridge | 8182 | SDXL img2img avatar stylization (LOCAL ONLY) |
| QwenBridge | 8181 | WebSocket bridge between app and Ollama (if running locally) |

## Tools Required

- **VS Code**: installed (fresh)
- **Claude Code extension**: installed + signed in (Anthropic account)
- **Git**: needs install + config
- **GitHub CLI (gh)**: needs install + `gh auth login`
- **Node.js**: needs install (use v24 to match server)
- **Python**: needs install (3.11+ for CLIEAIR compatibility)
- **Rust**: needs install (for PeerPower crate development)
- **Ollama**: for local LLM — `ollama pull qwen2.5:14b`

## VS Code Extensions (see setup/install-extensions.ps1)

Required:
- `ms-vscode-remote.remote-ssh` — connect to 72.167.227.50
- `ms-vscode-remote.remote-ssh-edit`
- `ms-vscode.remote-explorer`
- `eamodio.gitlens`
- `ms-python.python`
- `ms-python.vscode-pylance`
- `rust-lang.rust-analyzer`
- `dbaeumer.vscode-eslint`
- `esbenp.prettier-vscode`
- `ms-vscode.powershell`
- `rangav.vscode-thunder-client` (API testing)
- `GitHub.vscode-pull-request-github`
- `bradlc.vscode-tailwindcss`
- `ms-ossdata.vscode-postgresql`

## SSH Key Setup

Generate a key for server access:
```powershell
ssh-keygen -t ed25519 -C "proart@tsikanati" -f "$env:USERPROFILE\.ssh\id_ed25519_server"
# Then copy public key to server:
# ssh-copy-id -i "$env:USERPROFILE\.ssh\id_ed25519_server.pub" tsikanati@72.167.227.50
```

## Role in Twin Tower Architecture

Local Tower → development, testing, local LLM training dispatch
Server Tower → production serving, IIS, PM2, databases

Sync: Git is the bridge. Local pushes, server pulls.
For direct server edits: VS Code Remote-SSH extension connects directly.

## Why This Was Created

BitLocker recovery loop destroyed the Windows installation on 2026-03-25. This onboarding repo is the complete recovery kit so Claude Code can be fully operational on the rebuilt machine without losing any context from previous sessions.
