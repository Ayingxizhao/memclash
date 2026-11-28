---
name: fast-iteration-10k-preference
description: "User workflow: iterate on 10k (not 2h 100k runs); web-research approaches before testing; thesis writing starts 2026-06-16 week"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: edfb6c15-36c8-4d37-9f25-d77a35f6a308
---

The user finds multi-hour 100k training runs **demoralizing and wasteful** — "too much time wasted to
end up getting the same results." Default experiments to the **10k dataset**
(`data/rt_munich_64ant_10000ue_los15`, ~7 min/120ep arm); only escalate to 100k to CONFIRM a clear 10k
signal that's worth it. Don't propose a 2h+ run as a first probe.

Also: **do actual WEB RESEARCH for established approaches to the specific problem** (CSI feedback /
NLOS localization / channel charting) BEFORE proposing or running experiments — the user explicitly
wants researched, literature-backed candidates A/B'd on 10k, not guesses.

**Hard timeline:** the user starts WRITING the thesis document the week of **2026-06-16**. So favor cheap
fast experiments + consolidation over multi-week new pillars; any new direction must fit alongside
writing. Re-scope effort estimates honestly against this (e.g. a 10k multi-gNB proof-of-concept is days,
not the 3–4 weeks the old [[thesis-roadmap]] note implied — that was a full polished 100k pillar).

**Why:** repeated long runs that reproduce the baseline waste the schedule and morale, and the writing
deadline is now the binding constraint. **How to apply:** research → test best candidate on 10k → only
then 100k-confirm; quote fast (~10–30 min) runtimes; consolidate the already-strong deliverables.
See [[thesis-roadmap]], [[localization-analysis]], [[identifiability-diagnostic]].
