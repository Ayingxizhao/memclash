---
name: dta-product-dependencies-are-fetched-verified-never-shipped
description: DCFM's first-launch flow downloads the VC++ redistributable and Corlett's PSF2 kit on a Yes; where each comes from, how each is verified, and what mutation proved about the URL check
metadata:
  type: project
---

Phase 5 (2026-09-17). The user's decision, verbatim: "Download these and any other dependencies."
`src/DcDependencies.h/.cpp`, gate `harness/DcDependenciesCheck.cpp`, headless verb
`deps [fetch <vcredist|psf2kit>]`, menu Settings > Set up optional components...

- **PSF2 kit** (`psf2.irx`, `sq.irx`): neillcorlett.com no longer serves it. The original
  `PSF2Kit.zip` is in the Internet Archive
  (`web.archive.org/web/20110807193409id_/http://www.neillcorlett.com/downloads/PSF2Kit.zip`,
  13,995 bytes, SHA-256 `e0102223385611325763480e873048cd6f9867d7101ca31fafdd698bccc504fd`). The
  `id_` suffix matters: without it the Archive serves an HTML wrapper, not the file. The kit states
  no licence, so it is pinned and fetched, never committed or bundled
  ([[dta-dependencies-are-gitignored-not-committed]]). Installed to `%AppData%\.dcfm\psf2kit`,
  which `FindPsf2ModuleDir` now searches.
- **Sony's LIBSD / MODHSYN / MODMIDI are never downloaded** - PSF2 export reads them from the
  user's own disc (`MODULES/`). Only the two homebrew modules were ever missing.
- **VC++ redistributable**: `aka.ms/vs/17/release/vc_redist.x64.exe` redirects to
  `download.visualstudio.microsoft.com` and serves whatever is current, so there is NO hash to pin.
  It is run only if WinVerifyTrust passes AND the signer subject contains "Microsoft Corporation".
  Presence is the registry value `SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64\Installed`.
- **Headless never starts the installer** (a window plus a UAC prompt); it leaves the verified file
  in `%AppData%\.dcfm\downloads`. The message boxes and progress dialog cannot be driven headlessly;
  their decisions are the pure functions the gate holds.

**Why:** a program that downloads and installs is as safe as its refusals; every one of them had to
be something a check could fail.

**How to apply:** when adding a dependency, add a `DcDepSpec` with a verifier (hash if the bytes
are fixed, signer if the publisher rotates them) and its host to the allow-list - the gate fails a
spec whose own URL the allow-list refuses. Mutation lesson worth keeping: a separate "refuse `@`
and `:` in the host" test SURVIVED its mutant, because comparing the authority whole already
refuses both. It was deleted, not kept. A defence no check can fail is not evidence of anything.
