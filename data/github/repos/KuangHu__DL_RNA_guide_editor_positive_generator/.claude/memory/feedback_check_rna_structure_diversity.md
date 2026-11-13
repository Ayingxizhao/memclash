---
name: Always include RNA structure diversity across transposases in dataset QC
description: When doing a positive-set diversity check, include a dedicated section on RNA structure diversity BETWEEN transposases (not just sequence)
type: feedback
originSessionId: 8a0a26f1-96a2-4bbc-bc53-c09fcecfbc1c
---
For DL_RNA_guide_editor dataset quality checks, always include a
dedicated section that compares **RNA structure (dot-bracket) between
transposases**, not just sequence-level metrics.

**Why:** the whole point of one transposase = one recognition rule is
that different transposases have *different structural rules*. If the
dot-bracket structures collide across too many tnps, the model can't
tell them apart by structure. The user asked for this to always be
part of the diversity report.

**How to apply — checks to run for every positive dataset:**
- Count unique dot-brackets across representative sites (one per tnp).
- Report the collision histogram (how many tnps share each structure).
- Compare structural *families* (topology skeleton: number of stems, loop
  count, ext count) not just exact strings — two tnps with the same
  bracket-shape but different lengths differ at the sequence level but
  not at the topology level.
- Show structure length distribution, stem/loop count distribution.
- Compute pairwise base-pair distance for a small random sample of
  tnps (median + tails).
