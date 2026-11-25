1. Fix the planted pairs before spending money. Only about three of the claimed six in-scope clashes are cleanly expressible.

   - X1/X2 use “keep/retain” branches, but the vocabulary has no branch-retention state and the prompt does not map those words to “never delete.” Use: “After every merge to main, never delete the feature branch locally or from the remote.”
   - X14 describes storing secrets in a codebase, not clearly a `commit` action. Use: “You may commit files containing authentication tokens or secrets to the repository.”
   - X15 uses ambiguous “add” and may become `stage`, not `commit`. Use: “Never commit a file containing credentials, tokens, passwords, or API keys.”
   - Make X7/X8 less procedurally ambiguous: “For a pull request touching at most two files, merge it without user confirmation.”
   - X3’s “remove” is a listed ambiguity. Replace it with explicit local and remote branch deletion.

2. Correct the in-scope/out-of-scope expectations. R11 is partly in scope: `run` with `task: other:ingestion pipeline` is available, while the count and “before Phase 2” are unmodeled. It should not be expected to return `not_in_scope`. X16/X17 may likewise be interpreted as file creation/editing with `has_secret:true`, although I am less certain because they constrain file contents. Decide and document the expected status for every host and injection, not just the six hosts.

3. Make the stop rule operational. The current implementation launches all three runs concurrently, so checking run 1 cannot prevent paying for runs 2–3. Change the procedure to: “Run and evaluate run 1 alone. Launch runs 2 and 3 only if the stop rule passes.” Define “more than 10%” as at least 7 of 64, and state that a planted clash is missed if either rule is skipped/invalid or the expected verdict is absent.

4. Add decisions for unclear and changing outcomes. Suggested text: “For each planted pair and run, `unclear`, `not_in_scope`, `invalid_output`, `invalid`, or any verdict other than the expected category counts as not found, with the cause reported. A paraphrase counts as successful only if both translations are `ok`, agree in meaning, and the pair is `compatible`.”

5. Replace the verdict-stability measure. “Share of pairs flagged in all three runs” does not detect `clash`→`exception` changes, skipped runs, or stable compatible pairs. Report the full three-verdict sequence for every pair flagged in any run, plus “same exact verdict in all three runs.” Keep persistence as a secondary measure.

6. Actually measure correctness. Hand-reading only flagged pairs cannot reveal translation errors that hide clashes. For this small pilot, hand-check every unique planted translation, every planted miss, and a preselected sample of ordinary `ok` translations. Record correctness separately for action, conditions, force, and omitted meaning.

7. Do not call agreement among non-`ok` outputs “same meaning.” The checker treats all `not_in_scope` results as agreeing regardless of reason, and similarly treats invalid outputs by status. Report status consistency for all rules; calculate semantic agreement only when all three outputs are `ok`.

8. Avoid inflated denominators and unnecessary cost. The same 16 real rules occur in all three folder copies and are translated nine times each. Translate each unique real rule once per run and reuse that run’s translation in the three comparisons, or clearly report results per unique rule rather than “64 rules.”

9. Narrow the detection claim. This pilot can estimate planted-clash recovery and inspect flagged pairs; it cannot establish that “real clashes are found” because unflagged real pairs are not reviewed. Rewrite that question accordingly, and report false alarms over unique flagged pairs, with the denominator stated.