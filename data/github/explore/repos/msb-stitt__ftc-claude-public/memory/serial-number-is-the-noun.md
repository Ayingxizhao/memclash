---
name: serial-number-is-the-noun
description:
  "\"serial\" alone is an adjective, or a noun meaning a TV series; the noun for a device's
  identifier is \"serial number\"."
metadata:
  type: feedback
---

Write **serial number** wherever prose needs the noun. "Serial" on its own is an adjective, or a
noun meaning a story told in installments, so "the pad's serial" names a television programme.

**Why:** the user (Mike), 2026-09-28: *"Note that 'serial' when used as noun, without the word
'number' means a TV series. To be a noun it needs 'serial number'. Let's be precise."* The
shorthand entered this project from the API the value is read through, `SDL_GetGamepadSerial`, and
spread from there into the plan, the working notes and the program's own output.

**How to apply:** code identifiers keep the spelling of the API they name, so the field `serial`,
the `local.properties` keys `sim.gamepad1.serial` and `sim.gamepad2.serial`, and
`onlyPadWithSerial` all stay. Everything a reader reads as English takes the full term, strings a
program prints included. A quotation of output a program did print stays verbatim, because it is
evidence of what was seen; it changes when the program's own string changes. Same reasoning as
[[plain-words-for-middle-schoolers]]: the label is chosen for the reader, and precision wins.
