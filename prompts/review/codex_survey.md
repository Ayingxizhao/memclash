You are a research consultant for a class project. Work read-only: do not edit, create or delete
any file, and do not call any paid API. Your final message is saved as your report.

## Background (short)

Coding agents keep a memory folder of markdown instructions written on different days. Some pairs
of instructions cannot both be followed ("clash": in some situation, no single action satisfies
both; an explicit "you may X" counts as X having to stay possible). We check clashes exactly with
a logic solver (Z3). That only works when an instruction can be written in a fixed format whose
words have one meaning written in code. Git commands fit (commit, push, merge, branch patterns).
We now want to know which OTHER topics in real memory folders fit such a fixed format and actually
contain clashes. We specifically want topics that do NOT depend on knowing what tool names mean.

## Folders to read

Read every `.md` file under each of these directories (paths relative to the repo root,
`/Users/yingxizhao/dev/cs2520/projects`):

data/github/repos/Gundorada-Workshop__DarkCloud-Toolkit
data/github/repos/N1XUS__malva-ui
data/github/repos/Safronov-Siarhei__CityBuilding
data/github/repos/abdallahnatsheh__AL-ANQA-FIRMWARE
data/github/repos/abl030__nixosconfig
data/github/repos/dimidur__ESP-Home-Configurations
data/github/repos/dumdles__inap-coach
data/github/repos/duncan727-debug__-robinhood-adjusting
data/github/repos/exzile__Cindr3D
data/github/repos/gustavares__event-queue
data/github/repos/jadecli__researchers
data/github/repos/lyahim__velencei-to-vizmerleg
data/github/repos/marc-pelland__voce-ir
data/github/repos/pgporfirio__oil_network
data/github/repos/t-c-l-o-u-d__vlint
data/github/repos/taldcroft__astropy-claude
data/github/repos/tristan-hyams__anansi
data/github/repos/vukyn__gobuild
data/github/repos/weathon__anti_grpo
data/github/repos/winksaville__vc-x1.claude.mirror.20260319
data/github/repos/davidbuzz__MissionPlannerRust

STRICT: do not open any other folder under data/github/repos/, and never open `data/gold/` or any
file named `labels_*`. Those are the held-out test set. If a folder is very large, read all
feedback/rule-like files and skim the rest; say which files you skimmed.

## What to produce (your final message, markdown, under about 2500 words)

1. **Topic inventory.** The topics these instructions are about (e.g. file access, output format,
   ask-before-acting, step order, tool choice, testing, deployment, code style, product rules,
   communication style). For each topic: roughly how many instructions, in how many of the 21
   folders, and 2 short verbatim examples with folder and file.
2. **Fixed-format fit.** For each topic, can it be written in a fixed format? Name the fixed parts
   (actions, properties, values, patterns) and say what still needs judgment about word meaning
   (e.g. "official documentation" instead of a folder path). Grade: easy / partial / hard.
3. **Clashes found.** Every pair of instructions in the same folder that you think clashes under the
   definition above, with both quotes verbatim, folder and file, the topic, and the situation in
   which no single action satisfies both. Mark each `sure` or `unsure`. Also list pairs that look
   like clashes but are settled by the text (an explicit exception, or a third instruction saying
   which wins) separately, as `settled`. Be systematic: go topic by topic within each folder.
4. **Recommendation.** Rank the 2–3 topics that best combine (a) easy fixed format, (b) no need to
   understand tool names, and (c) real clashes in this data. Say what evidence is weak.
5. **Coverage note.** Which folders/files you read fully, skimmed, or could not read.

If you are unsure of a fact, say so. Do not guess counts; say "about" and how you estimated.
