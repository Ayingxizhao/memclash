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
2. "X instead of Y" / "X, not Y": encode the positive part X with "O". For an enum action, pick
   the value X.
3. Numbers: "~N" / "about N" -> min N-1, max N+1. "at most N" -> max N. "at least N" -> min N.
   "N-M" -> min N, max M. "exactly N" / "one line" -> min = max.
4. Translate the single behavior stated in `rule`. Use the file only to resolve scope and
   references; ignore the file's other rules.
5. Reuse before you add. Read the whole vocabulary first; add a term only if no existing term
   has that meaning.

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
