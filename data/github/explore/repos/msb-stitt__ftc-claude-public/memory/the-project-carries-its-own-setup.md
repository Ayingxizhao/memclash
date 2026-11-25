---
name: the-project-carries-its-own-setup
description:
  "Configure a project in files it commits, so it works on any computer; never change ~/ or other
  machine-local settings to make a project work."
metadata:
  type: feedback
---

Put what a project needs to work into files the project commits, such as `.gitignore`, so a fresh
clone on another computer behaves the same. Do not change anything at the `~/` level to make a
project work.

**Why:** the user (Mike), 2026-10-02: *"my preference is to have a project configured so that it
works regarless of what compture it is on, you should not be changing things at the top ~/ level to
make this project work"*. He said it choosing a committed `/scratch/` rule in `.gitignore` over
`.git/info/exclude`, which works on one clone only.

**How to apply:** when a choice is between a committed setting and a per-machine one, the committed
one goes first, and `.git/info/exclude`, `~/.gitconfig` and shell profiles count as per-machine.
