# Finding conflicting rules in coding-agent memory

CS2520 class project. A coding agent's memory folder holds rules written on different days.
Some pairs of rules cannot both be followed. This repo finds those pairs.

Research question: for rules in agent memory, does a solver-assisted check leave fewer
conflicting rule pairs than keeping every rule or asking an LLM, and how much of its error
comes from translating rules into logic?

## Contributions and where they live

| # | Contribution | Code | Prompts | Runs |
|---|---|---|---|---|
| 1 | Dataset: real memory folders from GitHub, split into rules, with labelled rule pairs | `prep/` | `prompts/data_prep/` | `data/dev`, `data/gold` |
| 2 | Negative result: one fixed format for every rule, checked by Z3, finds 0 of 10 labelled conflicts | `gate_v1/` | `prompts/gate_v1/` | `data/runs/gate_v1/` |
| 3 | General method: LLM lists related pairs, LLM judges each pair, Z3 confirms | `pipeline/general/` | `prompts/general/` | `data/runs/general/` |
| 4 | Exact method for git rules: each rule translated alone into a fixed git model, Z3 checks every pair | `pipeline/git/` | `prompts/git/` | `data/runs/git/` |
| 5 | Test with planted rules: a second model writes a conflicting rule and a rewording for a real rule | `pipeline/eval/` | `prompts/eval/` | `data/inject/` |

`pipeline/llm.py` is the shared LLM client. Every call is cached in `data/llm_cache.jsonl`,
so a rerun is free.

### 3. General method (`pipeline/general/`)

1. `filter_folder.py`: one LLM call per folder lists the pairs that look related. Repeated with
   shuffled rule order (default 4 times) and the pairs are pooled, because one call is unstable.
2. `judge_pair.py`: one LLM call per listed pair labels it (duplicate, contradiction, override,
   stale, tension, none). Without `--candidates` it judges every pair (the LLM baseline).
3. `verify_pair.py`: for each pair the judge calls a conflict, one LLM call writes both rules
   as logic formulas with shared names, and Z3 decides whether some situation makes both rules
   apply with no way to follow both. If Z3 says "no conflict" only because the two actions were
   never related, one more call asks how they relate, and Z3 decides again.
4. `run_pipeline.py`: runs the three steps into one run folder.

A pair is reported when the judge calls it a conflict and Z3 confirms it.

### 4. Exact git method (`pipeline/git/git_check.py`)

Each rule is translated alone into clauses over git operations (`never`, `only_if`,
`must_do`, `may_do`); non-git rules are marked `fits: false`. What git means is written in
the code, not guessed by the LLM: every kind of push is a push, every kind of merge is a merge,
and file patterns such as `.env*` are matched exactly. Z3 then checks every pair of git rules.
`selftest` checks the logic on hand-written translations without any LLM call.

### 5. Planted-rule test (`pipeline/eval/`)

`inject.py` asks a second model to write, for a chosen real rule, a conflicting rule in the
same words, a conflicting rule in other words, and a rewording that must not be flagged. Every
planted rule is reviewed by hand. `inject_eval.py build` makes one folder copy per kind;
`inject_eval.py score` scores each step. `score.py` scores a run against labelled pairs and
appends a row to `data/results.jsonl`.

## Commands

```
# general method
uv run python pipeline/general/run_pipeline.py --run general/<run> --rules data/dev/rules.json --repeats 4
uv run python pipeline/eval/score.py --name <name> --pred data/runs/general/<run>/reported.json \
    --labels data/open_coding/agent_a.json
uv run python pipeline/general/judge_pair.py --run general/<run> --rules data/dev/rules.json   # LLM baseline

# exact git method
uv run python pipeline/git/git_check.py selftest
uv run python pipeline/git/git_check.py translate --rules <rules.json> --out data/runs/git/<run>/translate.json
uv run python pipeline/git/git_check.py check --translations data/runs/git/<run>/translate.json \
    --out data/runs/git/<run>/check.json

# planted-rule test
uv run python pipeline/eval/inject.py --rules data/dev/rules.json --folder setflow \
    --hosts R1:opposite,R12:value --out data/inject/dev_pilot.json
uv run python pipeline/eval/inject_eval.py build --inject data/inject/dev_pilot.json --rules data/dev/rules.json
uv run python pipeline/general/run_pipeline.py --run general/<run> --rules data/inject/dev_pilot_rules.json
uv run python pipeline/eval/inject_eval.py score --inject data/inject/dev_pilot.json --run general/<run>
```

The endpoint and key are read from `../.env`. `LLM_PROVIDER=2` selects the second endpoint
(`DEEPSEEK_API_KEY2`, `Base_URL2`).

## Data

```
data/own/          the author's own memory folders (smoke test)
data/dev/          5 folders (125 rules) used for development; labels in data/open_coding/agent_a.json
data/gold/         10 held-out folders (389 rules) and 4 large folders (677 rules)
data/inject/       planted rules and the folder copies built from them
data/runs/         one folder per run, grouped by method (gate_v1, general, git)
data/results.jsonl one row per scored run
```

| Run | What it is |
|---|---|
| `gate_v1/own_v1..v3`, `gate_v1/dev_v1`, `gate_v1/dev_v2` | the fixed-format attempt |
| `general/dev_judge` | LLM judge on every dev pair (baseline) |
| `general/dev_folder`, `general/dev_folder_x5` | the folder-level listing, once and five times |
| `general/dev_confirm`, `general/dev_verify2` | Z3 check on the judge's dev conflicts (without / with the follow-up question) |
| `general/inj_pilot`, `general/inj_pilot_v2` | general method on the planted-rule pilot (without / with the follow-up question) |
| `git/git_pilot` | git method on the planted-rule pilot (`check.json` before the fixes, `check_v2.json` after) |

## Status (development results only)

- General method: on dev, Z3 kept 8 of the judge's 21 conflict flags, all real by the author's
  reading; the judge misses about half of the labelled conflicts. On the planted-rule pilot it
  caught 10 of 11 planted conflicts and flagged 0 of 5 rewordings.
- Git method: on the pilot, 6 of 6 planted git conflicts caught, 0 of 3 rewordings flagged, no
  false conflicts. Two checker errors were fixed on this same folder, so a fair test on new
  folders is still needed.
- Git method, large folders (212 git rules, tuning data): the checker reports 0 clashes, but the
  reference built from two readers and the author's labels has 11 clashes (2 more depend on a
  word's meaning). The checker misses all 11 because they involve things the git model cannot
  express (9 tool choice, 1 dev-bot testing, 1 "backlog sweep"). Definition of a clash and the
  other decisions: `docs/adr/`.
- Missing: fair git test on the large folders; full general run on dev in `results.jsonl`; the
  single run on the held-out folders (needs both labellers finished); novelty and citation checks.
- Dev labels come from one annotator and are incomplete. The held-out labels have not been used.
