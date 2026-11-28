---
name: teacher-prompts-received
description: The teacher's real 7 system prompts arrived (case design dossier) and are checked into prompts/*.ts; where the dossier's framing diverges from CLAUDE.md's role table
metadata:
  type: project
---

On 2026-08-28 the user supplied the teacher's real content as a .docx: "CASE DESIGN DOSSIER — THE
TRIBUNAL" (case: Jon Snow and the death of Daenerys Targaryen). It contains §1 a canonical charge
sheet (a demo/seed case, not wired into the app), §2 the four advocate character profiles (Jon
Snow/Tyrion Lannister on the defense seat, Daenerys Targaryen/Grey Worm on the prosecution seat),
and §3–5 the three judge profiles (Aharon Barak / Menachem Elon / Meir Shamgar judicial-reasoning
models).

Extracted the character-description paragraphs (not the "SIMULATION RULE" framing text or the
"Length check"/"Research basis" editorial notes) into `prompts/defense-1.ts`, `defense-2.ts`,
`prosecution-1.ts`, `prosecution-2.ts`, `judge-1.ts`, `judge-2.ts`, `judge-3.ts`, wired through
`prompts/index.ts`'s `PROMPT_SEED` (replacing `prompts/placeholder.ts`, which is now dead code kept
only as a documented fallback shape). Verified byte-for-byte (script-diffed) against what was
already live in production's `agent_configs` (`GET /api/agent-config` on the deployed App Runner
URL) — someone had already hand-pasted this same text into the Console before this file existed,
so the checked-in defaults now match production exactly (mod CRLF vs LF, immaterial).

**Why this matters — a real tension, flagged not resolved:** the dossier's own "SIMULATION RULE"
says the assigned seat fixes only the *procedural* role, explicitly **not** an opinion, factual
inference, or final position — the model should "reason in character." That's in tension with
[CLAUDE.md](../../CLAUDE.md) §2's table, which describes defense/prosecution as each arguing a
fixed INNOCENT/GUILTY stance. The seeded prompt text itself contains no "argue for X" instruction
at all — it's purely the character-description paragraph — so actual current behavior leans toward
the dossier's "reason in character" framing. Left as a flagged discrepancy in CLAUDE.md §6 rather
than silently picking a side; if it matters for grading, ask the user/teacher which framing should
win before adding any "argue for acquittal/conviction" instruction ourselves (adding one would also
cross the "we never author prompt content" line).

**How to apply:** Don't re-derive or re-paste this content from the .docx again — the checked-in
`prompts/*.ts` files are now the source of truth, gitignored `*.docx` so the source file itself
never enters git. A **fresh/wiped database** will seed correctly from these files
(`lib/db/setup.ts`'s `$setOnInsert`); an **already-seeded** database (prod already had rows before
this change, or any dev DB seeded from the old placeholder) will *not* pick up a code change
automatically — that only happens via `PUT /api/agent-config/:role` (Console edit) or a fresh
insert. See [[all-prompts-teacher-provided]] and [[editable-agent-config-scope-change]].
