---
name: Always submit long-running jobs via `sbatch --wrap` on this cluster
description: Never run multi-minute Part 1 / heavy pipeline jobs directly on the login node; use Slurm sbatch --wrap so it lands on a compute node
type: feedback
originSessionId: 8a0a26f1-96a2-4bbc-bc53-c09fcecfbc1c
---
For the DL_RNA_guide_editor project (and this Slurm cluster in general):
**never run long jobs directly on the login/interactive node.** Use
`sbatch --wrap` so the job goes to a compute node.

**Why:** the user caught this while running Part 1 (ncRNA design, ~5000
RNAfold-heavy calls). Running it locally on the login node was ~10× slower
than expected because the login node is shared and slow for CPU-bound work.
The user's exact reminder: "remember use sbatch --wrap".

**How to apply:**
- Any pipeline step estimated to take >5 min should be wrapped in
  `sbatch --wrap 'cd ... && PYTHONPATH=. python -m scripts.<foo> ...'`.
- Use `--output=logs/<name>.log` (and `--error=...`) so stdout/stderr
  land in the run's log dir.
- Parallelize Part 1 by splitting configs into chunks (e.g. 10 × 50 tnps)
  and submitting them as separate sbatch jobs (or a job array).
- Poll status with `squeue -u $USER` or `sacct`.
- Fast Part 2/3/4 can usually stay direct (Part 2 was 48 s for 25 K sites
  once GTDB was warm; Part 3/4 are seconds).
