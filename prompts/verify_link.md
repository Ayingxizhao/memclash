Two rules from one coding agent's memory folder were translated into named yes/no actions.
The translation did not say how the actions of rule A relate to the actions of rule B. You are
given both rules, the action names with their meanings, and a list of action pairs (one action
from each rule). For each pair, state how the two actions relate in a situation where both
rules apply.

Choose exactly one relation per pair:
- `exclusive`: the agent cannot do both in the same situation; doing one means not doing the
  other. Example: "merges immediately" and "waits for the user to confirm before merging".
- `a_means_b`: whenever the agent does the first action, it is thereby also doing the second.
  Example: "commits the .env file" means "commits a file that contains credentials".
- `b_means_a`: whenever the agent does the second action, it is thereby also doing the first.
- `unrelated`: the agent can do both, one, or neither; neither action says anything about
  the other. Use this when in doubt.

Judge only by what the actions mean. Read the rule text to understand what each action name
stands for, including any part of the rule that the name summarizes (for example, an action
named `merge_immediately` taken from "bypass the approval step and merge immediately"
includes skipping the approval). Do not choose a relation because the rules would then agree
or disagree.

Return JSON: {"pairs": [{"a": "<action of rule A>", "b": "<action of rule B>",
  "relation": "exclusive|a_means_b|b_means_a|unrelated", "reason": "one sentence"}]}
