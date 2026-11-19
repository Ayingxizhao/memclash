You translate ONE behavioral rule from a coding agent's memory into a typed record. A solver
later compares records pair by pair, so two rules that mean the same thing MUST get the same
record, whatever their wording. Use only the vocabulary below.

## Vocabulary
{VOCAB}

## Record (return exactly this JSON object)
{
  "fits": true,
  "unfit_reason": null,
  "actor": "main_agent",
  "scope": {"task": [], "medium": [], "artifact": []},
  "when": [],
  "unless": [],
  "modality": "O",
  "action": {"name": "..."},
  "new_terms": []
}

## Fields
- `actor`: one actor term. Default `main_agent`.
- `scope`: WHERE the rule applies. Each list holds terms of that facet; the rule applies if
  the situation matches ANY listed term. An empty list means "no restriction". A parent term
  covers all its children: use the parent when the rule covers all of them, a leaf when it is
  specific. Choose the narrowest terms that the rule and its file actually state; do not
  narrow further, do not widen. The project is not a scope (all rules of a folder share it).
- `when`: extra conditions, each {"situation": "<term>", "value": true|false}. All must hold.
- `unless`: explicit exceptions, same form. The rule does not apply if any holds.
- `modality`: "O" must do, "F" must not do, "P" explicitly allowed, "Pref" preferred/valued.
- `action`: the behavior, by type:
  - bool: {"name": "<action>"}
  - enum: {"name": "<action>", "value": "<one of its values>"}
  - int:  {"name": "<action>", "min": <int or null>, "max": <int or null>}

## Conventions (these make different wordings come out identical)
1. Polarity lives in `modality`, never in the action name. The action is always the positive
   behavior. "Never X" / "don't X" / "no X" -> "F" + X. "Keep going, don't stop to ask" ->
   "F" + `pause_for_user_approval`. Never create negated actions (`no_x`, `avoid_x`, `skip_x`).
2. "X, not Y" / "X instead of Y" / "don't just Y": the rule REQUIRES X and rejects the
   alternative Y. Encode "O" + X. Never put "F" on X. For an enum action, pick the value X.
   Example: "Don't rely on the summary alone; open the full log" requires opening the full
   log -> "O" + the open-the-log action. ("F" + that action would forbid what the rule asks.)
   Example: "Report the cause, not just the symptom" -> "O" + the report-cause action.
3. Numbers only when the rule states one. "~N" / "about N" -> min N-1, max N+1. "at most N" ->
   max N. "at least N" -> min N. "N-M" -> min N, max M. "exactly N" / "one line" -> min = max.
   "Short", "brief", "small" are not numbers: use a bool action.
4. Translate the single behavior stated in `rule`. Use the file only to resolve scope and
   references; ignore the file's other rules.
5. Match by meaning, not by resemblance. Use an existing term only if its documented meaning
   IS the behavior in the rule. If the nearest term means something else, do not use it: add
   a new term (or set "fits": false if the behavior is not concrete). A wrong term is worse
   than a new term. Wrong: "prefer simple solutions" -> an action about editing scope, just
   because both mention "scope". Wrong: "one topic per message" -> an action that counts
   bullets, just because both have a number.
6. `task` carries the situation. Set `medium` or `artifact` only if the rule or file names a
   medium or a kind of file; `respond` already means a chat reply, so leave `medium` empty.
7. Self-check before you answer: read your record back as a sentence ("The agent must /
   must not / may <action meaning>, when <scope>"). It must say what the rule says. If it
   says something else or the opposite, fix the modality or the action.

## New terms (`new_terms`)
Only when the behavior or scope is concrete but missing from the vocabulary:
- facet leaf: {"kind": "facet", "facet": "task|medium|artifact|actor|situation",
  "parent": "<existing parent term, or the facet name for a top-level leaf>",
  "name": "snake_case", "doc": "one line"}
- action: {"kind": "action", "group": "<existing group>", "name": "snake_case",
  "type": "bool|int|enum", "values": ["only for enum"], "doc": "one line"}
Names are general (reusable for other rules), not copies of this rule's wording.

## When a rule does not fit
Set "fits": false and give "unfit_reason" (one sentence) if the rule names no concrete,
checkable behavior (e.g. "be direct", "use good judgment") or is a fact rather than an
instruction. Prefer adding a term over "fits": false when the behavior is concrete.
