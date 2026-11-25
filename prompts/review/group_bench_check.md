You check test material for a research experiment. Work read-only (final message saved). Read
ONLY `data/runs/natural/group_bench_blind.json`. No paid API calls.

Each group has three coding-agent memory rules. Definition: a group CLASHES if in some situation
the rules talk about, no single course of action follows all three (an explicit "you may X"
must stay usable), while EVERY PAIR of the three can be followed together. A group is
COMPATIBLE if all three can always be followed. Mark PAIR if some pair already clashes by
itself, and AMBIGUOUS if it depends on a reading (say which).

Output a JSON array (```json block) of {"group", "label": "clash"|"compatible"|"pair"|"ambiguous",
"why": "<one line>"}.
