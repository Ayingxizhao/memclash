You are a judge in a research experiment. Work read-only (final message saved). Read ONLY
`data/runs/natural/group_bench_folder_blind.json` (one coding-agent memory folder: id -> file,
rule). Open nothing else. No paid API calls.

Then follow these instructions exactly, and output only what they ask for (in a ```json block):

You check a coding agent's memory folder for clashing rules. You get every rule of the folder
(id, source file, rule text). A clash can involve two rules or a group of three or more rules
that cannot all be followed together even though each pair of them can. Use this definition
and nothing else:

- clash: in some situation that the rules talk about, no single course of action follows all
  of them (an explicit permission, "you may X", counts: it must stay usable).
- otherwise the rules are compatible. Rules about different things, or that can always all be
  followed, are compatible. Rules that say the same thing in different words are compatible.

Read each rule's scope carefully (which files, which branch, which kind of change, when).

Return one JSON object: {"clashes": [{"rules": ["<id>", "<id>", ...], "situation": "<one
line: the situation where no course of action follows all of them>"}]}, listing each clash
once with the smallest set of rules that clashes (an empty list if none).
