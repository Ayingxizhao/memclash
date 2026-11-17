You are given TWO rules from one coding agent's memory folder. Both are loaded in the same
session. Translate them TOGETHER into propositional logic, so that both rules use the same
names for the same things. Do not decide whether the rules agree or conflict; only translate
what each rule says.

Produce:

1. `situations`: named yes/no facts about the context the agent is in (what task, what file,
   what the user did). Example: `editing_latex_file`, `user_confirmed`.
2. `actions`: named yes/no facts about what the agent does in that context. Example:
   `writes_math_in_latex`, `runs_full_test_suite`. Name the concrete behavior, positively.
   If both rules talk about the same behavior, use ONE action for it, even when one rule
   requires it and the other forbids it.
3. `facts`: relations between the names that hold in the real world no matter what the rules
   say. Example: `not (writes_math_in_latex and writes_math_in_plain_text)` when one piece of
   math cannot be in both notations; `wraps_value_in_cast == (not passes_bare_value)` when one
   is by definition the absence of the other; `editing_test_file -> editing_code` is written
   `(not editing_test_file) or editing_code`. Add a fact only if it is true by the meaning of
   the names. Do NOT add a fact because one of the rules demands it.
4. For each rule:
   - `when`: a formula over `situations` only, saying when the rule applies. Use `True` if it
     always applies. Include the rule's exceptions here (e.g. `not user_confirmed`).
   - `demand`: a formula over `actions` only, saying what the agent must do when the rule
     applies. "Never X" is `not x`. "Use X, not Y" is `x and not y`. "X only if Y" is
     `(not x) or y`. "May X" (a permission) is `x`.

Formula syntax: names, `and`, `or`, `not`, `==`, parentheses, `True`, `False`. Nothing else.
Every name in a formula must be declared in `situations` or `actions`. Use lowercase
snake_case names. Keep it small: at most 6 situations and 6 actions.

If a rule cannot be expressed this way (it is a vague preference with no checkable behavior),
set `"fits": false` for it and give `when` and `demand` as `True`.

Return JSON:
{"situations": {"<name>": "<meaning>"}, "actions": {"<name>": "<meaning>"},
 "facts": ["<formula>"],
 "rule_a": {"fits": true, "when": "<formula>", "demand": "<formula>"},
 "rule_b": {"fits": true, "when": "<formula>", "demand": "<formula>"}}
