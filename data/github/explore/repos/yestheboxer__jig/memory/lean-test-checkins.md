---
name: lean-test-checkins
description: "Write many tests while developing, but prune before EVERY PR is opened or pushed; trim unit tests hard, keep integration tests; PR size and CI time are both the constraint"
metadata:
  node_type: memory
  type: feedback
---

After a feature stack shipped with several hundred tests per side, the user said: "you write an absurd amount of tests. which is fine when writing code but not all of it should get checked in. it slows down our ci. unit tests for sure. integrations are probably fine."

**Why:** large checked in unit suites slow every CI run for every PR forever. Test volume during development is scaffolding; the checked in suite is a permanent tax. Large PRs also cost review time, and tests are often half of their size.

**How to apply:** use as many tests as needed while developing (TDD scaffolding is fine). Before committing, prune unit tests by **measured CI cost, not by count or line count**, and also drop redundant cases that only add PR size. Time the suite first. Cheap parametrized matrices over pure functions (microseconds per cell) are fine to keep even at 30 or more cells. The knife targets what actually costs CI time: tests with real sleeps, subprocess or container spins, big fixtures, per test service setup, and duplicate *slow* coverage across levels. Integration and end to end tests are worth keeping. When a delegated agent delivers a diff (the `jig:principle-verify-delegated-work` skill), time its suite and prune the expensive redundancy before committing.

**Delete the tests when you delete the code.** A test for deleted code is pure CI cost with no signal, and a later reader cannot tell whether it guards something real. When a member or module goes, its dedicated tests go in the same commit; where a test file covers the dead thing alongside live things, strip only the dead assertions.

The subtlety that makes this easy to get wrong: **tests do not count as consumers when deciding whether code is dead, but they DO have to be deleted with it.** To establish that a few members of a shared hook are dead, grep consumers with `grep -v test`, because their tests would otherwise make them look live. The same tests are then part of the deletion, not evidence against it. So run the liveness check excluding tests, then run a second grep INCLUDING tests to find everything that has to come out.

**Parallel per test durations lie.** `--durations` and JUnit `time` from a parallel run are contention artifacts, not test cost. A test reported at 81 seconds can take half a second in isolation. Always re time a candidate alone before optimising or deleting it. Much of unit suite cost is fixed per worker (collection runs once per worker), so deleting N percent of tests does not buy N percent of the time.

## Prune before every PR, as a step of opening it

The user's follow up, after a stack came out at several thousand added lines per PR, about half of it tests, stories and fixtures: "always prune tests before posting prs. you make too many tests."

**How to apply:** pruning is a gate on `gh pr create` and on every push that adds tests, not a cleanup pass later. Before opening a PR, measure the test share with `git diff --numstat <base>...HEAD` split by `*.test.*`, `*.stories.*`, fixtures and mocks. Delete near duplicate cases, implementation detail and constant restating tests, render only checks and duplicate stories; keep contracts, boundary cases and regressions for bugs fixed in that PR. Put the same rule in every coder brief, since coders default to writing many tests. A PR well over about 2k added lines needs a split plan before it goes up. 2k is a guide, not a hard limit: do not split a PR whose source alone is near 2k just to hit the number. Related: [[scout-counts-need-independent-recount]].
