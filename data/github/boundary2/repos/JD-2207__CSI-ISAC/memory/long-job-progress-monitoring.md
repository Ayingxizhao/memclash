---
name: long-job-progress-monitoring
description: User wants visible ETA/progress on long RT generation jobs; guard against silent death
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f4bbcb42-a71c-4faa-ae17-bc15b8ffc247
---

For long-running RT dataset generation (hours-long), always emit a progress bar with ETA AND write a `progress.json` sidecar (done/total/eta/rate/updated) that can be polled from another process. Reader: `src/gen_progress.py [data_dir]` — prints bar + warns if sidecar is >10 min stale.

**Why:** An 80k run died silently ~10h in (machine sleep or background shell killed) with no meta.json and no traceback — it looked like "still running." The user explicitly asked to "implement a progress bar so I can always check ETA." A stale-detection check turns an invisible death into an obvious one.

**How to apply:** Generation runner (`rt_localization_data_gen.py`) prints `PROGRESS [bar] % | done/total UE | rate | elapsed | ETA` per shard and updates `progress.json`. ETA is based on kept-UE fraction. When launching a multi-hour job in the background, also arm a watcher for the first progress line / error so startup is confirmed (not hung on Sionna init). See [[rt-datagen-progress]], [[env-setup]].
