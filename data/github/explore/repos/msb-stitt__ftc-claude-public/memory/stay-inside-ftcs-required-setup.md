---
name: stay-inside-ftcs-required-setup
description:
  "FTC's own install instructions set the required setup, such as Java 17; read them first, and
  never propose or record a path outside them, even one that happens to work."
metadata:
  node_type: memory
  type: feedback
---

FTC's documentation sets the configuration the robot code must stay within. Its *Installing Android
Studio* page calls for JDK 17 installed separately, because the Java bundled with Android Studio
does not suit the FtcRobotController workspace. Read FTC's page for the question in hand before
proposing a setup, and offer only options inside it.

**Why:** on 2026-10-07, asked why `gradlew` found no `JAVA_HOME` on a Windows computer, I proposed
pointing it at Android Studio's bundled Java, then ran a build on that Java 25 to show it worked.
Mike pointed out the FTC page requires 17. A path outside the required configuration is not an
option however well it runs, and he asked that it not be written down at all.

**How to apply:** for any FTC tool or version question, open the FTC docs first and treat what they
require as fixed. Do not document rejected paths outside it. Related:
[[trust-the-user-or-read-the-docs]].
