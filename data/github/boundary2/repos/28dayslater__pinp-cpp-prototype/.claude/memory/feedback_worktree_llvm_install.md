---
name: Worktree needs third_party/llvm-{install,project} symlinks
description: New git worktrees of parserkg/ lack both the LLVM install (build artefact) and the llvm-project submodule (uninitialised). Symlink both from the canonical worktree.
type: feedback
---

A new `git worktree` of `parserkg/` is missing **two** things from `third_party/`,
each with its own failure mode:

## 1. `third_party/llvm-install/` (build artefact, not git-tracked)

The working tree lacks this directory entirely because it's a build artefact.
`find_package(LLVM REQUIRED CONFIG)` in `CMakeLists.txt` doesn't error — it silently
falls back to a system LLVM (e.g. `/usr/lib/cmake/llvm`). Configure succeeds. Link
fails much later with cryptic undefined references to MC layer symbols, for example:

    undefined reference to `llvm::MCFixup::getLoc() const'
    undefined reference to `llvm::TargetRegistry::RegisterTarget(...)`

The system LLVM and the locally-built LLVM are usually different versions or built
with different options, so partial linking against system libs produces these errors.

**Why:** the symptom is at link time, far from the cause (the configure-time silent
fallback). Easy to misdiagnose as a code bug or as something the most recent edit
broke. Cost ~5 minutes during the `parserkg-llvm-trim` worktree setup for spec 0014.

**How to apply:**

Immediately after `git worktree add ...`, symlink the install dir from the canonical
worktree:

    ln -s /home/glb/fuckups/ai/parserkg/third_party/llvm-install \
          third_party/llvm-install

If the build dir was already configured before the symlink, wipe and re-configure:

    rm -rf build && cmake -S . -B build

Verify the configure output names the local install and version (22.1.0 at time of
writing), not the system version:

    -- Using local LLVM install at .../third_party/llvm-install
    -- Found LLVM 22.1.0

If you see a different version (e.g. distro-packaged LLVM 22.1.3 on Manjaro), the
symlink is missing or pointing to the wrong place — fix and re-configure before
building.

`third_party/llvm-build/` (the LLVM CMake build dir) is in the same boat but is only
needed to re-link LLVM itself; irrelevant for typical worktree work on pinp.

## 2. `third_party/llvm-project/` (submodule, uninitialised in worktree)

`git worktree add` does **not** initialise the project's submodules into the new
worktree — the `third_party/llvm-project/` directory exists but is empty. This is
only visible if you try to *rebuild* LLVM (e.g. via `scripts/build_llvm.sh`), at
which point cmake errors with:

    CMake Error: The source directory "...third_party/llvm-project/llvm" does not exist.

`git submodule status` from inside the worktree shows the submodule with a `-`
prefix on its SHA, confirming "not initialised here".

**How to apply:**

Same fix as the install dir — symlink from the canonical worktree:

    rmdir third_party/llvm-project   # remove the empty placeholder
    ln -s /home/glb/fuckups/ai/parserkg/third_party/llvm-project \
          third_party/llvm-project

The source is pinned at a specific SHA in the parent repo, so sharing it across
worktrees is safe; you would never edit `llvm-project/` per-branch anyway. If you
ever do need a divergent LLVM source state per worktree, run
`git submodule update --init third_party/llvm-project` inside the worktree instead
— but for the normal case symlinking is cheaper and avoids re-cloning.

## Both at once — recommended one-liner after `git worktree add`

    cd <new-worktree>
    rmdir third_party/llvm-project
    ln -s /home/glb/fuckups/ai/parserkg/third_party/llvm-install \
          third_party/llvm-install
    ln -s /home/glb/fuckups/ai/parserkg/third_party/llvm-project \
          third_party/llvm-project

Natural place to automate this: `scripts/bootstrap.sh` (see the bootstrap TODO) — it
already checks for the install and currently builds it from scratch if missing; it
could instead detect a sibling worktree, offer to symlink both dirs from it, and
fall back to the from-source path when no sibling exists.
