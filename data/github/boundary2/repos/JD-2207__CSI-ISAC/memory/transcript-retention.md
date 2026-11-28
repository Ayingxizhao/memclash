---
name: transcript-retention
description: "Claude Code auto-deletes transcripts after cleanupPeriodDays; set to 365 on 2026-08-12 after discovering old sessions were already gone"
metadata:
  type: reference
---

Claude Code deletes session transcripts (and other data under `~/.claude`) older than
`cleanupPeriodDays` **at startup** — default **30 days**. This is why only 7 transcripts existed at
the 2026-08 machine migration ([[machine-migration-2026-08]]) even though `history.jsonl` records
**137 session IDs back to 2026-02-06**: the rest had already aged out on the old machine, long
before the crash. Set to **365** in `~/.claude/settings.json` on 2026-08-12.

Two useful facts when history seems missing:

- `~/.claude/history.jsonl` is NOT swept by that cleanup — the raw text of every prompt ever typed
  survives there (1062 records back to February), even for sessions whose transcript is gone. Only
  the assistant side of those conversations is lost.
- A session ID in `history.jsonl` is not the same as a distinct conversation. When a session runs
  out of context it continues under a NEW id, and the earlier part survives as the summary block
  inside the new transcript (verified: `44be4423` → summary at line 796 of the `e9528d0e`
  transcript). Many other one-prompt ids are one-shot invocations. So the count of genuinely lost
  conversations is well below 137 − 7.
