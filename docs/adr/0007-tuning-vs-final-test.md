# 0007. Large folders are tuning data; the held-out folders are run once

Date: 2026-11-19. Status: Accepted.

## Context
The translation instructions and the checker were changed after looking at errors on the pilot
and the large folders. Results on folders used for changes overstate how well the method works.

## Decision
The pilot and the four large folders are tuning data. The 10 held-out folders (52 git-looking
rules) are run once, with the final instructions and checker, after all changes are made. Their
labels are not read before that run.

## Consequences
- Numbers from tuning data are reported as such.
- Any change after the held-out run needs a new held-out set or must be reported as made after
  seeing the results.
