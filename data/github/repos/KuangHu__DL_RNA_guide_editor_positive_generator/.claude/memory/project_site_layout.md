---
name: Site layout in DL_RNA_guide_editor_positive_generator
description: Biological structure of a synthetic training site — flanks, non-coding regions, tnp CDS, and where the guide RNA lives
type: project
originSessionId: 8a0a26f1-96a2-4bbc-bc53-c09fcecfbc1c
---
Each site models an IS-element locus and its flanks:

```
[flank_upstream (60 bp DNA)]  [non-coding region 1]  [tnp CDS]  [non-coding region 2]  [flank_downstream (60 bp DNA)]
```

**Why:** matches the user's biological model of IS110-style RNA-guided editors — the transposase CDS sits between two non-coding regions, and the ncRNA (bridge RNA) comes from ONE of those two non-coding regions.

**How to apply when generating training data:**
- Each site has TWO flanks: upstream and downstream, sampled as *independent* 60 bp windows from the same genome (not two halves of one contiguous window). The DNA target lives in exactly one of them (per-CDS choice).
- Each site has TWO non-coding regions. Exactly ONE of them contains the guide-bearing ncRNA; the OTHER has no guide RNA.
- The non-coding region is NOT "full RNA" — the ncRNA is embedded inside a longer non-coding stretch (with padding around it) rather than being the whole region.
- The tnp CDS between the two non-coding regions is NOT part of the model input for v1 (project is intentionally protein-free).
- Per CDS, all sites share:
  - which side is the *active* non-coding region (left vs right)
  - which flank the target lives in (upstream vs downstream)
