# Finding conflicting rules in coding-agent memory

CS2520 class project. A coding agent's memory folder holds rules written on different days.
Some pairs of rules cannot both be followed. This repo finds those pairs.

## Method (three stages)

1. **Filter** (`pipeline/filter_folder.py`): one LLM call per folder lists the pairs of rules
   that look related. The call is repeated with shuffled rule order and the proposed pairs are
   pooled, because a single call is unstable.
2. **Pair judge** (`pipeline/judge_pair.py`): one LLM call per proposed pair labels it
   (duplicate, contradiction, override, stale, tension, none).
3. **Verifier** (`pipeline/verify_pair.py`): for each pair the judge calls a conflict, one LLM
   call writes both rules as logic formulas with shared names, and Z3 decides whether a
   situation exists in which both rules apply and no behavior meets both.

A pair is reported when the judge calls it a conflict and Z3 confirms it.

## Layout

```
pipeline/     the current method
  llm.py             LLM client with an on-disk cache (data/llm_cache.jsonl)
  filter_folder.py   stage 1
  judge_pair.py      stage 2 (without --candidates: the all-pairs baseline)
  verify_pair.py     stage 3
  run_pipeline.py    runs the three stages into one run folder
  score.py           precision / recall against pair labels; appends to data/results.jsonl
  inject.py          injection test: a second model writes conflicting rules
  inject_eval.py     injection test: builds the injected folders, scores the pipeline on them
gate_v1/      the first attempt: translate each rule alone into a fixed schema, then Z3
prep/         data collection (GitHub scrape) and rule extraction
prompts/      every prompt; prompts/labelling holds the instructions given to the labellers
archive/      one-off scripts from the open-coding phase
data/
  own/          the author's own memory folders (smoke test)
  dev/          5 folders used for development; labels in data/open_coding/agent_a.json
  gold/         10 held-out folders with pair labels, 4 large folders without
  inject/       injected rules and the folders built from them
  runs/<run>/   outputs of one run
  results.jsonl one row per scored run
```

## Commands

```
# the pipeline on a rule list
uv run python pipeline/run_pipeline.py --run <run> --rules data/dev/rules.json --repeats 4
uv run python pipeline/score.py --name <name> --pred data/runs/<run>/reported.json \
    --labels data/open_coding/agent_a.json

# the all-pairs LLM baseline
uv run python pipeline/judge_pair.py --run <run> --rules data/dev/rules.json

# the injection test
uv run python pipeline/inject.py --rules data/dev/rules.json --folder setflow \
    --hosts R1:opposite,R12:value --out data/inject/dev_pilot.json
uv run python pipeline/inject_eval.py build --inject data/inject/dev_pilot.json --rules data/dev/rules.json
uv run python pipeline/run_pipeline.py --run inj_pilot --rules data/inject/dev_pilot_rules.json
uv run python pipeline/inject_eval.py score --inject data/inject/dev_pilot.json --run inj_pilot
```

The LLM endpoint and key are read from `../.env`. Every call is cached, so a rerun is free.

## Run folders

A pipeline run writes `filter.json`, `judge.json`, `verify.json`, `reported.json` and
`summary.json` into `data/runs/<run>/`. Runs made before `run_pipeline.py` existed keep their
old names:

| Run | What it is |
|---|---|
| `own_v1`..`own_v3`, `dev_v1`, `dev_v2` | `gate_v1` runs |
| `dev_judge` | all-pairs judge on dev (`judge.json`) |
| `dev_folder` | one folder call per dev folder (`judge.json` is the filter output) |
| `dev_folder_x5` | five repeats of the folder call on dev |
| `dev_confirm` | verifier on the dev judge's conflict flags and on the labelled pairs (`confirm.json`) |
| `inj_pilot` | injection pilot on one dev folder |

## Status

Development results only. The dev labels come from one annotator and are incomplete, and the
gold folders have not been used yet. See `data/results.jsonl` for the scored runs.
