# Memory index

- [Editing subagent guideline files](editing-subagent-guideline-files.md) — how to compact agent prompts: assume competence, state it once, delete a rule once its cause is fixed, generalize feedback never transcribe it, don't skip objective synthesis; and what the measured floor is worth
- [Pipeline ecosystem](pipeline-ecosystem.md) — the project→feature→commit pipeline under `~/.claude/` (3 skills, 2 cores + reader-profile, opt-in `domains/` field layer, 6 subagents, git-guard hooks, 2 check scripts): its altitude contract, every design decision with the alternative it rejected, and the dated record of what changed when
- [Pipeline metrics](pipeline-metrics.md) — what each finished feature actually cost (tokens, turns, review rounds); read it before changing a rule that claims to affect cost, and never trust a token figure an agent reported
- [Pipeline improvement inbox](pipeline-improvement-inbox.md) — rolling queue of pipeline-improvement suggestions (pipeline-retrospector files at feature close; pipeline-maintenance consumes + reconciles)
- [Figure legibility requirements](figure-legibility-requirements.md) — figures must be self-explanatory (title/axes/legend) and labels must not be clipped outside the frame
