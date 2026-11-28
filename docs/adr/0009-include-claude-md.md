# 0009. Check the repo's CLAUDE.md together with the memory folder

Date: 2026-11-22. Status: Accepted. Widens the scope of the project.

## Context
The agent reads two sources of instructions at the start of a session: the repo's root
`CLAUDE.md` and its memory folder. The rule extraction (`prep/extract.py`) read only the memory
folder. In the survey, two of the clashes found with confidence (QuagKhai003/assessment: "never
delete git branches" vs "merged branches may be deleted once the user asks"; jamieleecho/
space-bandits: object files `game/objects/XX-name.c` vs "create `game/objects/XX-name/`") have one
side in `CLAUDE.md`, so they could not be found from memory-folder rules.

## Decision
For the survey folders used from now on, rules are extracted from the memory folder **and** the
root `CLAUDE.md` (`prep/extract.py --claude-md`). Pairs are checked across both. Each rule keeps
its source file name, so results can be reported separately for memory-only pairs.

## Consequences
- Earlier results used memory folders only; they are not re-extracted.
