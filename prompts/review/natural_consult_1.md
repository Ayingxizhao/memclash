You are the co-investigator on a class project (presented Dec 1). Work read-only (your final
message is saved). Do not open `data/gold/`, `labels_*`, `frozen_*`. No paid API calls.

Read `docs/review/hybrid_lit_codex.md` (your earlier review), `pipeline/rules/natural_test.py`,
`data/runs/natural/screen_codex.json`, `data/runs/natural/folder_deepseek.json`.

## New results (natural pairs, no planting)

951 same-folder pairs from 84 rules (5 real memory folders) whose 3-run translations were
already saved, so Z3 cost nothing.
- Z3 on saved translations: flags 2 pairs in any run: R118/R131 force-push (real, 3/3 runs) and
  R20/R74 (false alarm, 2/3 runs: scope "non-code" lost). Misses R24/R156 (the "may" permission
  was dropped in translation), R60/R213 ("map and player data" left out as having no path;
  linking it to server-world.dat needs the other rule), R28/R81 (debatable: flat .c/.h files
  vs an object folder; Z3 sees create-file and create-dir as jointly possible).
- Codex whole-folder screen (you, blind): 3 flags = R24/R156, R60/R213, R118/R131; 0 others.
- DeepSeek-v4-flash whole-folder, ONE call per folder, thinking on (5 calls, ~$0.025): 4 flags =
  the same 3 + R28/R81; 0 others.
- Claude's own (non-blind) screen: the same 3 clear clashes; R28/R81 and R133/R139 ("do not
  write E2E tests" vs "write a backend integration test through all 5 steps") ambiguous.

So at natural prevalence (~3-5 clashes in 951 pairs) the LLM alone, same model as our
translator, beats the Z3 pipeline on recall, ties on precision, at far lower cost. Budget left:
~$0.07 of DeepSeek. Codex and Claude time are free.

The full folders are much larger: 119-394 rules each (7k-77k pairs); the 84 rules above are a
subset. Known clashes all lie inside the subset.

## Questions

1. Interpret. Is there still a promising, honest story? Where could Z3 or a hybrid genuinely
   beat the LLM alone (scale/long context, stability, exhaustive "no clash" guarantees,
   explanation, multi-rule conflicts, adversarial/subtle cases)? Which of these can we test for
   ~$0.07 plus free Codex/Claude work?
2. Proposed next step (agree or replace): scale test. Give the FULL folders to (a) Codex, free,
   all 5 folders and (b) DeepSeek whole-folder, 1 call each for the two folders with known
   clashes (QuagKhai 159 rules, RDForward 394 rules), ~$0.04. Measure whether the known clashes
   are still found and how many extra flags appear; adjudicate extra flags (Claude + Codex).
   If the LLM degrades at full size, a candidate step (lexical filter) + pairwise check
   becomes necessary, and the pairwise check is where Z3 vs LLM vs hybrid is compared.
3. What story would you tell on Dec 1 if the scale test also favours the LLM alone?

Under 700 words. Plain language. End with AGREE / CHANGE and the exact next step.
