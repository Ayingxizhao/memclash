---
name: Database Reference
description: All database connections, schemas, Redis DB assignments
type: reference
---

## PostgreSQL 16 — port 5432

**Primary PostgreSQL instance** (postgresql-x64-16 service)

### urbot_billing
User: `urbot_billing`
Tables: products (90 bots), price_tiers (270), purchases, email_signups, discount_eligibility, pp_* (PeerPower: peers/certificates/activations/heartbeats), ms_* (Mountain Safety), pod_* (Podcast), dip_* (Diplomat), cc_* (Creative Studio: 16 tables), user_profiles, onboarding_answers, salesman_conversations, analytics_events, bot_activity

### urbot_ecosystem
User: (set in ecosystem/.env)
Tables: 29 tables — creators, revenue_events, knowledge_items, provenance_chain, royalty_distributions, token_balances, token_ledger, treasury_snapshots, stakes, knowledge_packs, pack_items, pack_ratings, pack_purchases, creator_bots, teaching_sessions, session_enrollments, internal_contributions, house_wallet, tax_nexus, tax_calculations, audit_log, challenges, challenge_votes, redemptions, beneficiaries, donation_receipts, payout_batches, payout_items, curve_params

### ims (IMS MachinistZen)
User: `ims_admin`
Contains: 81+ migrations, tile intelligence system (5 tables), user management, machines, work orders, quality, maintenance, supply chain, shift reports

### CLI connection (from server)
```bash
"C:/Program Files/PostgreSQL/16/bin/psql.exe" -U urbot_billing -d urbot_billing -p 5432
```

## PostgreSQL 13 — port 5432 (same IP, different service port 5433 in old context)

**Legacy instance** (postgresql-x64-13 service)
NOTE: Both PG13 and PG16 are on port 5432 as of current config. The tsinc_enterprise DB is on PG13 but was migrated to use port 5432.

### tsinc_enterprise
User: `tsinc_admin`
Contains: 293 seeded agents, tasks, grades, knowledge base, communications, swarm AI assignments, bot factory records

## MariaDB 11.4 — port 3307

Service: MariaDB114
Used by: translatorseries.com (tsiapp)

## Redis — port 6379

Service: Redis (C:\Redis\)
DB assignments:
- DB 0: billing (urbot-billing)
- DB 1: tsinc-api cache
- DB 2: ecosystem cache (urbot-ecosystem)
- DB 3: mountain-safety

```bash
"C:/Redis/redis-cli.exe" ping
"C:/Redis/redis-cli.exe" -n 1 info keyspace
```

## SQLite (better-sqlite3)

- realworldprizes.com: `httpdocs/data/database.sqlite`
- quantumledgerbookkeeping.com: `httpdocs/data/database.sqlite`
- After Node version change: `npm rebuild better-sqlite3`

## Connection Templates

```
# PG16 connection string pattern
postgresql://USER:PASSWORD@localhost:5432/DATABASE

# Redis
redis://localhost:6379/DB_NUMBER
```

Actual passwords are in the respective `.env` files in each project directory.
Check: `C:\inetpub\vhosts\<project>\*.env` or `<project>\.env`
