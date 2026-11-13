---
name: Don't over-verify small config changes in the RNA generator
description: For config-only jitter/range knob changes, skip the full smoke test; use a fast Python probe instead
type: feedback
originSessionId: 8a0a26f1-96a2-4bbc-bc53-c09fcecfbc1c
---
For small config-only changes to the RNA-guided-editor positive generator
(e.g. bumping a jitter range, tweaking a knob), **do not run a full smoke
test** (`python -m generator.main --n-cds ... --sites-per-cds ...`). That
path runs RNAinverse on ncRNA backbones and takes minutes even for a
handful of CDS.

**Why:** the user pointed out that a jitter-range change should be
verifiable in seconds, and the multi-minute smoke test was frustrating for
a one-line YAML edit.

**How to apply:**
- Unit tests (`tests/test_pairing.py`, `tests/test_structure.py`,
  `tests/test_audit.py`) run in a few seconds — always run these.
- For sampler-level changes, write a ~10-line probe that calls
  `sample_cds_rule` / `sample_site_params` directly and prints the drawn
  values across many CDS. No genome sampling, no RNAinverse, no RNAfold.
  Runs in <1 second.
- Only run the full `generator.main` smoke test when the change touches
  the end-to-end pipeline (site assembly, verify.py schema, output
  structure), not for tuning individual knobs.
