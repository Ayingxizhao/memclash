---
name: focus-the-vm-before-typing
description:
  "cliclick and peekaboo keystrokes go to whatever window is in front; when Mike brings Ghostty
  forward, typing meant for a VM lands in Claude's own prompt."
metadata:
  type: feedback
---

`cliclick t:` and `peekaboo press` send keys to the frontmost window, not to the VM named in the
capture. On 2026-10-08 Mike brought Ghostty forward to check on the run, and
`/opt/android-studio/bin/studio`, meant for the Ubuntu guest's terminal, was typed into Claude's
own prompt and arrived as a message that looked like Mike's.

AppleScript's `tell application "System Events" to tell process "X" to key code 53` goes to the
front window too, not to X. On 2026-10-14 and again on 2026-10-15 an Escape meant for Android
Studio or AdvantageScope went to Ghostty, which the command before had brought forward, and the
second one interrupted Claude's own turn.

**Why:** Mike looks in on unattended runs by switching to Ghostty, so focus can change between any
two tool calls.

**How to apply:** right before sending a key to an app, `osascript -e 'tell application "X" to
activate'` in the same command, and check it is frontmost before the key. Right before typing
into a VM, bring its Parallels window forward (`open -a
"Parallels Desktop"` or a click on the window) in the same command as the keystrokes, and confirm
the result with a capture. A user message that matches text Claude just tried to type is most
likely Claude's own keystrokes, so ask before acting on it. Related: [[this-mac-is-claudes]].
