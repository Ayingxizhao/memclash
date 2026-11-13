# Open coding comparison: agent_a vs agent_b

Matching is by quote overlap, not IDs (segmentation differs). One relation may match
several on the other side (e.g. B splits one index line into several pairs).

**Totals:** A relations matched by B: 15; A only: 19; B relations unmatched: 23; label agreement on matched A relations: 10/15.

## Consteon/web-spreadsheet-example

- **BOTH** A:R35-R32 `contradiction` | B:R2-R53 `other`  ← label differs
- **BOTH** A:R40-R32 `override` | B:R2-R53 `other`  ← label differs
- **A only** R3-R6 `contradiction` (medium): R3 says always fix the stored value, never the enum; R4/R6 (lesson learned from the same incident) say question the constraint and allow a schema change when th
- **A only** R36-R37 `other` (medium): Inconsistent trigger: R36 requires confirming the target DB before every migration, while R37/R38 say use the user-specified DB exactly and ask only when there 
- **A only** R41-R24 `other` (high): Stale index: R41 calls the target_status lesson the 'latest', but it is the first entry in code-improvement.md; the latest entry is the employee.repository bare
- **A only** R21-R13 `duplicate` (high): R13 (numeric CAST) is a special case of the general rule R21 (every CASE...WHEN must CAST to the target type). Subsumed duplicate.
- **A only** R21-R19 `duplicate` (high): R19 (timestamptz CAST) is a special case of the general rule R21. Subsumed duplicate.
- **BOTH** A:R32-R34 `duplicate` | B:R53-R57 `duplicate`
- **A only** R29-R24 `other` (low): Tension: R24 keeps code because it matches the nearby file-wide pattern, whereas R29/R31 say references win over nearby code. Whether the reference prescribes G
- **B only** R2-R56 `other` (medium): The index says SELECT-only, but the application instruction asks confirmation before running a mutation. Whether confirmation expands the agent's role is left u
- **B only** R53-R56 `duplicate` (high): Both require confirmation before executing a db-analyst mutation.
- **B only** R56-R57 `duplicate` (medium): The application paragraph repeats the same no-unconfirmed-mutation requirement positively and negatively.
- **B only** R7-R44 `duplicate` (high): The index and file both require regular async functions rather than arrows for the referenced layer code.
- **B only** R10-R47 `duplicate` (high): Both prohibit using nearby module code as the implementation reference.
- **B only** R28-R34 `duplicate` (high): Both reserve APPROVED transitions exclusively to the external approval service callback/writeback.
- **B only** R8-R51 `duplicate` (high): Both require exact adherence to the reference's parameter types for architectural-layer code.
- **B only** R9-R63 `duplicate` (high): The index and the explicitly marked Good example require the same workspace-filter helper instead of manual filters.
- **B only** R12-R68 `duplicate` (high): The target-status memory and improvement-log heading both prohibit interpreting target_status as a generic core approval state.

## MCMike0399/from-tcp-to-http

- **A only** R2-R18 `duplicate` (high): Both forbid video references; R18 adds the ThePrimeagen exception, consistent with the course-design file calling it 'inspiration only'.
- **A only** R1-R17 `duplicate` (high): Both require text-based resources (R17 also lists blog posts).
- **A only** R8-R19 `duplicate` (high): Both say do not withhold information / act as an accelerating tutor.
- **A only** R20-R6 `other` (low): Soft tension: R6/R8/R19 favor giving direct answers and generated boilerplate; R20 favors the user's self-directed research over being spoon-fed. Both can be pa

## M-Hernandez/setflow

- **BOTH** A:R2-R5 `other` | B:R10-R14 `other`
- **A only** R16-R11 `other` (high): Stale index: the index says issues #4 and #5 are next; the file says Phase 0 is complete and #17 is next.
- **BOTH** A:R3-R5 `duplicate` | B:R2-R24 `duplicate`
- **BOTH** A:R3-R13 `duplicate` | B:R2-R24 `duplicate`
- **A only** R1-R14 `duplicate` (medium): user_profile 'no stale branches' restates the branch-cleanup rule (less specific).
- **A only** R6-R14 `duplicate` (medium): user_profile 'no credentials' restates the no-credentials rule.
- **A only** R7-R8 `other` (low): Ambiguity: R8 says verify no '.env files' are staged; .env.example could be read as a .env file, which R7 says to commit.
- **B only** R3-R16 `duplicate` (high): The index and feedback file both prohibit committing any credentials.
- **B only** R4-R17 `duplicate` (high): Both direct storage of credentials in gitignored .env files.
- **B only** R5-R7 `duplicate` (high): Both require local feature-branch deletion after every merge to main.
- **B only** R6-R8 `duplicate` (high): Both require remote feature-branch deletion after every merge to main.
- **B only** R11-R9 `other` (high): The stated sequence deletes the local feature branch before switching to main. If gh pr merge leaves that branch checked out, git branch -d refuses to delete it
- **B only** R10-R13 `other` (medium): Remote deletion is itself git push, but the confirmation rule asks which files will be pushed or merged. A deletion pushes no file changes, leaving the required

## shabelson-picker/applied_math

- **BOTH** A:R8-R20 `contradiction` | B:R17-R37, R4-R37 `contradiction/other`
- **BOTH** A:R8-R18 `contradiction` | B:R17-R32, R4-R32, R4-R38 `contradiction/other`
- **BOTH** A:R8-R33 `contradiction` | B:R17-R67, R4-R67, R4-R38 `contradiction/other`
- **BOTH** A:R36-R33 `contradiction` | B:R3-R67, R4-R67, R4-R38 `other`  ← label differs
- **BOTH** A:R6-R19 `override` | B:R14-R47 `override`
- **BOTH** A:R37-R19 `other` | B:R14-R47 `override`  ← label differs
- **BOTH** A:R3-R10 `contradiction` | B:R10-R20 `override`  ← label differs
- **A only** R7-R4 `override` (medium): R7 says create expansions lazily, only when friction is hit; the teaching-stance file (R2/R4/R5) says build prerequisites explicitly and cover everything unless
- **A only** R21-R19 `other` (medium): Possibly stale instruction: the resume point (Module 1 §4) comes from a status block dated 2026-07-11, before the 2026-08-29 CLRS re-pacing; the DS file also sa
- **A only** R38-R14 `other` (low): Possible tension in register: 'simple formal English' for DS proof sessions vs 'high register, do not simplify' for the AofA course. The scopes are different pr
- **BOTH** A:R38-None `other` | B:R50-R72, R50-R73 `other`
- **A only** R1-None `other` (medium): Unindexed file: aofa-course-teaching-stance.md has no entry in MEMORY.md.
- **B only** R1-R51 `duplicate` (high): Index and file both restrict a targeted correction to the indicated item.
- **B only** R1-R56 `duplicate` (high): Both require one targeted edit rather than additional changes.
- **B only** R51-R56 `duplicate` (high): The application bullet repeats the main targeted-edit instruction.
- **B only** R5-R70 `duplicate` (high): Index and file both prohibit re-debugging launch.json for this known freeze.
- **B only** R7-R20 `override` (medium): The course calibration permits relying on a familiar theorem instead of starting from zero, narrowing the teaching-stance requirement to teach everything from t
- **B only** R8-R20 `override` (medium): The default says to teach rather than assume knowledge, but the specific calibration permits treating the integral test as already familiar. This is a default-v
- **B only** R14-R34 `override` (high): The old rule maps nine modules onto Sedgewick-Flajolet chapters; the newer instruction explicitly asks for a CLRS-based replacement. It supersedes the old struc

## thesteve0/local-llm-benchmark

- **BOTH** A:R4-R7 `duplicate` | B:R1-R15, R5-R15 `duplicate`
- **A only** R9-None `other` (medium): Dangling reference: project_model_selection.md links [[user-hardware]], which is not in the folder.
- **B only** R1-R5 `duplicate` (high): The index and metrics file both select server metrics rather than GuideLLM as the primary source.
