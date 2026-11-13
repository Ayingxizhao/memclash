---
name: dcfm-menu-pointer-is-drawmenuobjectvibe
description: The menu pointer three tab headers called "not located" is DrawMenuObjectVibe, three cells on the stayframe sheet the tab bar already loads
metadata:
  type: reference
---

Every 2D menu screen in this game points with a white gloved hand, and for three ports in a row
this project recorded it as missing: the Item, Weapon and Chara tab headers each disclosed
"retail's pointer sprite at SysCur was not located". It was never missing. It is
`DrawMenuObjectVibe__Fiiii @0x00216f40`, and it draws out of `stayframe` -- the *tab bar's* own
sheet, which the pause menu already had loaded the whole time.

Three 32x32 cells, side by side on row **y = 40**, and the cell's x IS the value the caller
passes:

| x | hand |
|---|---|
| 64 | the pointing finger, nothing under it |
| 96 | the open palm, something here can be picked up |
| 128 | the closed hand, carrying something |

The row is not a continuous strip of cursors -- x=0 and x=32 are other art -- so a "32 times n"
rule samples the wrong thing.

`DrawObjectVibe @0x00216d90` wobbles it through **two sine waves of different frequency**:
`dx = 7*cos(0.08055366*t)` and `dy = 5*sin(0.116355285*t)`, where `t` is a free-running global
counter. Those are 2*pi/78 and 2*pi/54, so the hand traces a Lissajous figure that repeats every
702 frames, not a circle. Using one amplitude or one frequency for both looks plausible and is
wrong; `DcMenuPointerCheck` has a mutant control for each.

Over a personal-board cell the hand is drawn **beside** what it points at, not on top of it:
`DrawAtoraSelect` puts it at `(334 + col*40, 138 + row*40)` over icons at
`(362 + col*40, 127 + row*40)`, so 28 px left and 11 px below the icon's own top-left. Centring
it hides the item the player is choosing.

Retail draws the sprite twice, a flat black shadow at (+5,+3) then the hand. This port draws it
once: the 2D sprite program has no colour uniform at all, so the shadow would be a white ghost.
The same limit is why the Chara tab prints figures where retail draws coloured bars, and why
`MGFillBox` is unported. See [[dcfm-chara-tab-retail-model]] and [[dcfm-pause-menu-icon-sheets]].
