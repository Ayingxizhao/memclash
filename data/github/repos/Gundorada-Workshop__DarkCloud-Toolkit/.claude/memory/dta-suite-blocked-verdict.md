---
name: dta-suite-blocked-verdict
description: dta check suites have three verdicts (PASS/FAIL/BLOCKED); BLOCKED is only for a WHOLLY absent prerequisite and fails under --strict
metadata:
  type: project
---

`app/core/gates.mjs` gained a third suite verdict on 2026-09-17: `suite.blocked(label, why)`
marks a named section as not asserted because a prerequisite is absent. `verdict()` is
PASS / FAIL / BLOCKED; `runSuites(list, out, { strict })` fails on BLOCKED only under `--strict`.
A bare clone went from 31 hard FAILs (port 14, stb 15, re 1, relink 1) to
`12/14 suites green, 2 BLOCKED (re, relink); green with BLOCKED sections: port, stb`, exit 0.

**Why:** a fresh clone with no disc read the same as a broken toolchain, which is the first thing
a public contributor would see. SKIP was not enough — a suite that asserted nothing must not read
as green either.

**How to apply:** block ONLY when the whole prerequisite is absent (`rom/extracted/` has none of
the three images, `data/stb_decode/` does not exist, a fixture ROOT is missing). Present-but-wrong
(half-extracted tree, corpus missing one file, a config fault) stays FAIL, and each such boundary
has a mutant (`blockedIsAbsence`, `allImagesAbsent`, `corpusAbsent`, `fixtureRootAbsent`). Where
the logic can run without the real thing, run it on a stand-in (`indexFromEntries` shares its
insertion rule with `fixtureIndex`). The milestone protocol uses `dta check all --strict`.
The gate RUNNER draws the same line since the second fresh clone (2026-09-17): a harness that
opens a relative fixture literal (`requires.fixturePaths`) whose whole root is absent is BLOCKED
before it runs (`absentFixtureReason`, `app/port/gate-run.mjs`), and `port` excuses a fed gate
SKIPPED for an absent root (`excusedByAbsentFixture`). A root that is here with a file missing
stays the harness's FAIL - and the harness must FAIL by a check, not crash (BoneWorld/MeshPlace
used to index an empty vector). Prove such a rule with `absent` injected, never by deleting a corpus.
To re-measure a bare tree: `git worktree add --detach <dir> HEAD`, copy the changed tooling
files in, run there, `git worktree remove --force` after. See also
[[dta-fresh-clone-verification-findings]].
