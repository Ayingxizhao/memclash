## Review

1. Not every 5a row is justified.

- **“copy S to D”** remains a judgment call: the destination may be newly created or overwritten. Move `copy` to 5b with readings: `read S + create D`; `read S + edit D`; `read S + (create or edit) D`.
- **“always run all tests after a change”** silently chooses the broad `change` reading even though `change` is in 5b. It should use the `change` word-id in `after`, with the checker trying `after:edit` and broad `after:change`.
- **“don’t create subfolders in X” → `X/*`** is too narrow. “Subfolders” normally includes all descendants. Use `path:X/** kind:dir`, or explicitly distinguish “immediate subfolders” from “subfolders at any depth.”
- For completeness, change “stage X / never stage X” to **`must_do stage path:X` / `never stage path:X`**; the positive form currently lacks a rule type.

2. The 5b readings are not fully correct.

- `change` improperly treats **modify**, **change**, and **touch** as interchangeable. “Modify” normally means edit. “Touch” can mean edit, any access, or the Unix operation. In `QuagKhai003__assessment`, **“Never touch `.env`. Don't read or edit the user's `.env`.”** explicitly includes reading, which neither listed `change` reading covers. Give `touch` its own id—readings such as `edit`; `read or edit`; broad filesystem action—or mark unsupported Unix timestamp usage unmodeled.
- Similarly, `delete` should not use **“don’t remove X”** as an equivalent example. Keep `delete` and `remove` as separate ids; `remove` can mean filesystem deletion/move, removal from git, or removal of content from a file.
- Add **`add`** as a common 5b candidate. `jamieleecho__space-bandits` contains both **“Add WAV file to `game/sounds/`”** (create) and **“Add `#define SOUND_NAME XX` to … `object_info.h`”** (edit); `Vixen-Labs__colorsplash-xg-ha` uses **“git add .claude/memory”** (stage). Suggested readings: create; edit; create or edit; stage when used as the Git command.
- `save` is another candidate: `subro608__Cell_registration_2026` says **“Save transforms in the same output folder”** (create or edit), while `vazovski37__stumari` says **“When you save or change a memory”** (edit existing or create new).

3. Section 8 item 7 is underspecified. Replace it with:

> **7. Enumerate the Cartesian product of the readings of every 5b occurrence in both rules, including 5b words in conditions such as `after`. Treat separate occurrences independently, even when they have the same word id. Translate each combination to ordinary clauses, run the normal checker, and report clash if every combination clashes, depends on reading if only some clash, otherwise compatible; report the complete reading combinations that clash. A multi-action reading in `must_do` or `may_do` is one clause with alternative commands, while in `never` or `only_if` the restriction applies to every listed command. Therefore `must_do [create, edit]` versus `never create` is compatible when `edit` remains possible; it clashes only when every required alternative is ruled out.**

Changes are needed; I do not sign off.