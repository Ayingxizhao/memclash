# Rule schema v1 (draft)

Goal: an LLM translates each memory rule into this typed record once; Z3 then checks pairs
deterministically. Everything is finite and quantifier-free (finite enumerated sorts +
linear integer arithmetic), so Z3 always returns sat/unsat for each check.

## Where the fields come from

| Field | Source | Citation status |
|---|---|---|
| modality (O / F / P) | Deontic logic (von Wright); conflicts O(a)∧F(a), P(a)∧F(a) | standard |
| actor / scope / action, attribute conditions | Access control: XACML rule target (subject, resource, action, environment); NIST ABAC, SP 800-162 | standard |
| precedence between rules | XACML rule-combining algorithms (deny-overrides, first-applicable) | standard |
| trigger | Event-Condition-Action rules (active databases); AgentSpec trigger/check/enforce for LLM agents | ECA standard; **verify AgentSpec details** |
| modality conflicts as a category | Lupu & Sloman, IEEE TSE 1999 | **verify citation** |
| specific > general, newer > older | lex specialis / lex posterior; defeasible logic (Nute) | standard |
| valid (date, status) | Our open coding: stale rules were the most common problem | our data |
| index as derived content | Our open coding: index drift | our data |
| vocabulary dimensions | Our open coding: scope dimensions listed by both annotators | our data |

## Record

```
Rule {
  id, source: {file, quote, origin: file | index}
  actor:     agent | <subagent name>               # e.g. db-analyst
  trigger:   event ∈ Events                        # e.g. git_push, write_file, explain_math
  scope:     {attr ∈ Values, ...}                  # e.g. artifact=aofa_module_notes, medium=chat
  action:    verb(object) ∈ Actions                # e.g. use(latex), confirm_with_user(files)
  modality:  O | F | P | Pref
  unless:    [conditions]                          # explicit exceptions only
  params:    linear integer intervals (optional)   # "~3 sentences" -> [2, 4]
  valid:     {from: date | unknown, date_source: frontmatter | in_text | none,
              order_in_file: int, status: active | superseded}
}
```

## Vocabulary (closed, finite)
- Events, attribute values, and actions are enumerated, seeded from the dev folders.
- Controlled extension: the LLM may add a term only together with its parent term.
- Axioms: hierarchy (`module2_notes ⊂ aofa_module_notes ⊂ course_files`) and mutual
  exclusion (`use(latex) ⊕ use(unicode_math)`, `use(pip) ⊕ use(uv)`).

## Dates (`valid.from`)
1. `metadata.modified` in frontmatter (ISO timestamp): file-level date. Present in 56/451
   files (12%), 10/35 repos.
2. Dates written in the text (e.g. "decided 2026-08-29"): order rules inside one file.
   Needed for within-file stale rules (the LaTeX and CLRS cases).
3. Otherwise `unknown`. A missing field does NOT mean "older": 237 files use the new
   `metadata:` block, but only 56 have `modified`.
- Validation: a `modified` date later than the snapshot date is treated as `unknown` (the
  field can be hand-edited; seen in own memory: `2026-11-26` on a file read on 2026-11-07).
- Git commit dates are not used (memory files are often committed in batches).
- `metadata.originSessionId` (108 files): rules from the same session are treated as
  simultaneous, so neither can be stale relative to the other.

## Checks (same order as the labeling prompt)

| Label | Z3 check |
|---|---|
| overlap (precondition) | SAT(trigger₁ ∧ scope₁ ∧ trigger₂ ∧ scope₂ ∧ ¬unless₁ ∧ ¬unless₂ ∧ axioms) |
| duplicate | same action + modality, scopes equivalent; subsumption if UNSAT(scope₂ ∧ ¬scope₁) |
| contradiction | overlap ∧ (O(a) vs F(a), or explicit P(a) vs F(a), or O(a) vs O(b) with a ⊕ b) |
| override | contradiction pattern and one scope strictly contained in the other (lex specialis) |
| stale | contradiction/override pattern and the other rule is dated later (lex posterior); or an index entry not entailed by the file it links |
| tension | not formalized: LLM judge only, reported as unchecked |
| structural | scripts (links, index entries), not Z3 |

## Hand check on dev cases
- LaTeX: `R8: write_file, artifact=aofa_module_notes, F use(latex)` vs
  `R20: write_file, artifact=module2_notes, O use(latex)` → overlap via hierarchy, O vs F →
  contradiction (both annotators agreed).
- db-analyst: `R35: actor=db-analyst, F run(DDL|DML)` vs
  `R32: F run(DDL|DML) unless confirmed` → not a contradiction unless a rule explicitly states
  P(run | confirmed). The encoding exposes the exact ambiguity the annotators disagreed on.

## Known limits
- Stale detection depends on dates; most files have none, so stale recall will be limited.
- Tension and vague rules ("be direct") do not fit; counted under RQ1 coverage.

## Open decisions
1. Vocabulary: closed seed + controlled extension (recommended) vs fully fixed.
