# OTel Skill Test Harness

This project exists to repeatedly test Claude's OpenTelemetry instrumentation skills against real application codebases in various languages and frameworks.

## Structure

```
run.ts                # Full-run orchestrator: reset → build → instrument → start → traffic → evaluate
src/
  instrumentation.ts  # Agent SDK runner — calls the instrumentation agent via @anthropic-ai/claude-agent-sdk
  evaluation.ts       # Honeycomb query-based evaluation criteria
  weaver.ts           # Finalizes + parses the weaver live-check report (weaver_live_check_{http,db,other} criteria)
  harness.ts          # Helpers that wrap harness.sh commands
  metrics.ts          # Run record persistence (runs.jsonl) and summary printing
harness.sh            # Low-level step runner: reset, build, bootstrap, start, stop, traffic, instrument
collector.run.template.yaml  # Per-run OTel Collector config (fan-out to Honeycomb + weaver live-check)
otel/                 # Downloaded tooling (gitignored): Java agent, weaver, otelcol-contrib
apps/
  <app>/              # One directory per target app (e.g. broadleaf, realworld-go, beaverhabits)
    config.sh         # App-specific variables (incl. the APP_* facts for the prompt) and start/stop/build hooks
    traffic.sh        # Traffic generation script
    EVALUATION.md     # Evaluation checklist for this app
checkouts/
  <app>/              # Cloned app code (gitignored)
```

The agent prompt is one preamble rendered from a shared, user-voice template
(`instrument-preamble.template.md` at the repo root) filled with each app's `APP_*` facts from
`config.sh` — there are no per-app preamble files. To add a new app, create `apps/<name>/` with
`config.sh` (including its `APP_*` fact vars), `traffic.sh`, and `EVALUATION.md`. No changes to shared
harness code required.

## Purpose

Each session simulates a fresh instrumentation engagement on a target application. The scripts in this repo exist to quickly reset the target to a clean, pre-instrumentation state so the same skill can be re-tested without leftover changes from a previous run.

## Workflow

Run a full test with:

```
npx tsx run.ts broadleaf                  # one app (runs inline)
npx tsx run.ts broadleaf realworld-go     # several apps, sequentially
npx tsx run.ts all --parallel             # every app under apps/, concurrently
npx tsx run.ts kill [app...|all]          # cleanly stop active run(s)
```

Each in-flight run records a PID file (`tmp/.run.<app>.pid`). Starting an app whose run is
already active is **refused** (avoids port/log collisions), and `run.ts kill <app|all>` stops
the run process and its app server / collector / weaver — use this rather than hand-rolled
`pkill`, which misses the child processes and leaves orphans that corrupt later runs' logs.

With more than one app, `run.ts` spawns one isolated child process per app
(`--parallel` runs them concurrently; otherwise sequentially) and prints a
combined pass/fail summary. Each app uses app-scoped logs (`logs/<app>/`), PID
file (`tmp/.harness.<app>.pids`), and prompt (`tmp/.instrument-prompt.<app>.md`), so
concurrent runs don't collide. All generated run-scoped scratch files live under
`tmp/` (gitignored), not the repo root. For `--parallel`, each app must bind distinct
ports — configured per app in `apps/<app>/config.sh` (`APP_HTTP_PORT` and any
other listener vars the app defines).

**Watching live progress:** each run writes phase markers and its final result to
`tmp/run-progress.<app>.log`, which is **truncated at the start of every run** — so
`tail -f tmp/run-progress.<app>.log` always reflects only the current run for that app.
Tail this rather than piping `run.ts` stdout through `tail` (buffers until exit) or
reading any hand-made cross-run redirect log (mixes stale entries from earlier runs).

During `start`, the harness also brings up a per-run OTel Collector + `weaver registry
live-check` OTLP receiver (dynamically-allocated ports, app-scoped config/pid/state) and
points the app's OTLP export at the collector, which fans telemetry out to **both**
Honeycomb (for the query-based criteria) and weaver (for the `weaver_live_check`
criterion). Disable with `HARNESS_WEAVER_CAPTURE=0`. Requires `download-tools` to have
fetched `otel/weaver` + `otel/otelcol-contrib`; if absent the harness falls back to
exporting straight to Honeycomb and skips the weaver criterion.

This orchestrates the complete cycle automatically:

1. `reset --purge` — discard the current scratch branch and create a fresh `scratch_YYYY-MM-DD` branch from `clean` *(host)*
2. `build` — build all modules *(host; the app is also rebuilt for Linux inside the lifecycle container, see below)*
3. `bootstrap` — one-time setup (e.g. seed a database) if the app defines it; skipped automatically if already done *(host)*
4. `instrument` — generate `tmp/.instrument-prompt.<app>.md` from the skill content + app preamble *(host)*
5. Agent step — `src/instrumentation.ts` drives a clean-context agent via `@anthropic-ai/claude-agent-sdk`, **in a container** (`runInstrumentationInContainer`)
6. Lifecycle step — **in one container** (`runLifecycleInContainer` → `docker/lifecycle.sh`): build → `start` → `traffic` → flush → evaluate, with the fan-out collector + weaver live-check alongside the app in the same netns
7. Record — results read back from the container and appended to `runs.jsonl` *(host)*

See **Containerized runs** below for how steps 5–6 are isolated; both run in per-language Docker images.

> **Note on bootstrap:** Some apps persist `bootstrap` state outside the checkout (e.g. a seeded database under `/tmp`), which can survive session restarts but be cleared on system reboot. If `start` fails with a schema/setup error, run `./harness.sh <app> bootstrap` manually before re-running.

## Containerized runs (container-only)

Every run executes its two heavy phases **inside Docker containers**, each with its own PID + network
namespace, so the skill's generic process/port commands (`ps`/`lsof`/`kill`, app boots, the agent's own
weaver) only ever see their own world — never the host or a sibling `--parallel` run. There is **no
in-process host fallback**; Docker is required.

Two container invocations per run, both from the same per-language image:
1. **Agent step** — `src/run-agent.ts`, sandbox **ON**. Drives the instrumentation agent. Answer key
   baked-but-denied (see below). Writes `tmp/.agent-metrics.<app>.json`, read back by the host.
2. **Lifecycle step** — `docker/lifecycle.sh`, sandbox **OFF** (trusted harness code). One foreground
   `docker run` that does the whole scored lifecycle in one netns: **build → start → traffic → flush →
   evaluate**, bringing up the fan-out collector + weaver live-check alongside the app. Writes
   `tmp/.eval-results.<app>.json`, read back by the host.

Everything else stays on the host: `download` / `download-tools` / `reset` / `bootstrap` / `instrument`
(git + text + the host-seeded broadleaf DB) and the durable `runs.jsonl` record. The agent's own
telemetry is **not** collected out-of-band any more: `src/agent-tracing.ts` builds gen_ai spans (one
`chat` per turn, main agent + sub-agents, under a root `invoke_agent`, with `execute_tool` children)
directly from the SDK message stream inside the agent step and exports them straight to Honeycomb —
no host-side collector, no `claude_code.* → gen_ai.*` remap.

The images share a base layer (`harness-agent-base`: Node runtime, weaver, Linux `otelcol-contrib`,
`lsof`, the full baked harness code, Node deps); each language image just adds its toolchain. **Build
the base first**, then the language image(s) — rebuild the base whenever harness code or deps change:

```
docker build -f docker/agent-base.Dockerfile   -t harness-agent-base   .   # base: one-time / on harness-code change
docker build -f docker/agent-python.Dockerfile -t harness-agent-python .   # + uv
docker build -f docker/agent-go.Dockerfile     -t harness-agent-go     .   # + Go toolchain (CGO_ENABLED=1)
docker build -f docker/agent-java.Dockerfile   -t harness-agent-java   .   # + JDK 17 + Maven + OTel java agent jar
npx tsx run.ts beaverhabits   # python · realworld-go (go) · broadleaf (java)
```

Supported for **all three apps** (Python/Go/Java); a new app's language just needs a `harness-agent-<lang>`
image (`node` would need one too).

How it fits together:
- **`src/container.ts`** has both launchers: `runInstrumentationInContainer` (agent step) and
  `runLifecycleInContainer` (lifecycle step). `src/run-agent.ts` and `docker/lifecycle.sh` are the
  matching in-container entrypoints. **Image selection:** `harness-agent-<lang>` from the app's
  `APP_OTEL_AGENT_TYPE` (via `readAppConfig`); `HARNESS_AGENT_IMAGE` overrides as an escape hatch.
- The image bakes the **full** harness code at **`/harness`** so paths resolve exactly as on the host
  (`harnessRoot=/harness`, `repoDir=/harness/checkouts/<app>`, `pluginRoot=/harness/agent-skill/honeycomb`)
  — `src/instrumentation.ts` / `sandbox.ts` and the in-container `harness.sh start`/`traffic` run unchanged.
- **In-container collector + weaver (lifecycle step):** `docker/lifecycle.sh` renders
  `collector.run.template.yaml` with the run id + skill-version attrs (forwarded as env) and **fixed**
  netns-internal ports (collector 4317/4318, weaver grpc 4319 / admin 4320 — safe because each run is its
  own netns), launches `otelcol-contrib` + `weaver registry live-check`, points the app's OTLP export at
  the local collector, then runs `harness.sh start`/`traffic` and `src/run-eval.ts`. weaver's admin port +
  registry pass to `run-eval` via env (`HARNESS_WEAVER_ADMIN_PORT`/`HARNESS_WEAVER_REGISTRY`) — **no host
  weaver state file**. Telemetry still egresses to Honeycomb; only inbound host ports are gone.
- **Build runs in-container (lifecycle):** a host build would produce host-platform artifacts (a macOS
  `.venv`, native objects) the Linux container can't run, so `lifecycle.sh` runs `harness.sh build` before
  start. It's idempotent and uses the bind-mounted caches, so when the agent container already built it
  this is fast. (The host `build` step still runs in `run.ts` — broadleaf's host `bootstrap` needs it.)
- **Mounts:** the checkout (RW — edits + the Linux build land on the host checkout the host later records),
  `tmp/` (RW), `logs/<app>` (RW — app/collector/weaver logs + the weaver report), and, for the agent step,
  the skill tree (RO). The eval "answer key" (`src/evaluation.ts`, `weaver.ts`, `envvars.ts`,
  `EVALUATION.md`, `apps/`) **is baked into the image** (the lifecycle/eval entrypoints need it). The
  **agent step** runs with the `src/sandbox.ts` hook — its default-deny whitelist denies every `/harness`
  path outside the checkout + `otel/`, so the answer key is present-but-unreadable to the agent, **equal to
  the old host posture**. The lifecycle step is trusted harness code and reads it freely.
- **Writable HOME:** `--user <host-uid>` leaves the container with no home dir, so `HOME` is pointed at a
  per-app dir (`tmp/.home-<app>`, pre-created host-side) — giving uv, Go (`GOPATH`/`GOCACHE`), and Maven
  (`~/.m2`) a writable, host-persisted cache shared between the agent and lifecycle steps.
- **Per-language / per-app extra mounts** (both steps, via `extraDockerArgs`): the **java** image mounts
  the host `~/.m2` (RW) so Maven doesn't re-download ~1 GB each run; **broadleaf** also mounts the
  host-seeded `/tmp/broadleaf-hsqldb` (run `./harness.sh broadleaf bootstrap` first) and the host's cached
  Solr distribution (`os.tmpdir()/solr-<ver>` → `/tmp/solr-<ver>`; `java.io.tmpdir` is the per-user
  `$TMPDIR` on macOS but `/tmp` in the Linux container — hence the cross-path mount).
- **Networking:** the agent step exports its gen_ai spans straight to Honeycomb from inside the
  container (using the forwarded `HARNESS_INGEST_KEY`), so no host-side receiver and no
  `host.docker.internal` rewrite are involved. Neither container publishes ports — the app's own boots
  (broadleaf's HTTP/HTTPS/HSQLDB:9001 etc.) bind only inside the netns and can't collide with the host
  or a `--parallel` peer.
- **weaver:** the base image ships a statically-linked **musl** Linux weaver (the host `otel/` weaver is a
  macOS binary, not mounted; the `latest` gnu build needs a newer glibc than the base image).
- **Go (cgo):** realworld-go's SQLite driver (`mattn/go-sqlite3`) is cgo, so the Go image sets
  `CGO_ENABLED=1` and relies on `build-essential` (gcc) from the base.
- **Java agent jar:** the skill downloads the latest OTel java agent itself (host parity); the java image
  also **bakes a copy** at `/opt/otel/opentelemetry-javaagent.jar` as an offline fallback.
- **Memory (broadleaf):** broadleaf needs GB-scale RAM (site + admin JVMs, `MAVEN_OPTS=-Xmx1g`); ensure
  the Docker Desktop VM has **≥6-8 GB** before a broadleaf run.

**Auth requirement:** the SDK authenticates from `run.ts`'s environment, and `src/container.ts` forwards
the credential vars **by name** (`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN`,
`ANTHROPIC_BASE_URL`). So `ANTHROPIC_API_KEY` (or equivalent) must be **exported in the shell that
launches `run.ts`** (or set in `.env`, which `run.ts` loads). A Claude Code OAuth credentials file
(`~/.claude/.credentials.json`) is NOT seen by the container unless mounted in (it isn't, currently).

Editing baked harness code (`src/instrumentation.ts`, `agent-tracing.ts`, `sandbox.ts`, `pricing.ts`,
`run-agent.ts`, `run-eval.ts`, `evaluation.ts`, `weaver.ts`, `envvars.ts`, `docker/lifecycle.sh`,
`harness.sh`) requires a `docker build` to take effect, since the image bakes those files.

## harness.sh — Individual Steps

`harness.sh` exposes each step individually for debugging. `run.ts` calls these internally; you rarely need to invoke them directly. Two env vars are required: `OTEL_EXPORTER_OTLP_HEADERS` (ingest key) and `HONEYCOMB_QUERY_API_KEY` (query key with Query Data permission) — both read from `.env`.

Run any step as `./harness.sh <app> <cmd>`:

- `download` — clone the app repo (skips if already present)
- `download-agent` — download the OTel agent for the app's language (if it uses one)
- `download-tools` — download `weaver` + `otelcol-contrib` to `otel/`
- `build` — build the app
- `bootstrap` — one-time setup (e.g. seed a database), if the app defines it
- `instrument` — generate `tmp/.instrument-prompt.<app>.md` (used internally by `run.ts`)
- `start` / `stop` / `restart` / `status` — manage the app's server(s) in the background
- `traffic` — generate representative traffic against the running app
- `reset [--purge]` — check out the app's `clean` baseline and create a fresh scratch branch
- `clean` — remove logs and Playwright session artifacts

Each app's checkout has a `clean` branch (the unmodified upstream baseline — never commit instrumentation changes there) and per-run `scratch_YYYY-MM-DD[-N]` working branches.

## Browsing a running app

Use the **Playwright MCP** tools (`playwright_navigate`, `playwright_screenshot`, etc.) when interacting with a running app's UI. Do not use `curl`, `WebFetch`, or raw HTTP calls to browse or verify UI behavior.

## Constraints

**All OpenTelemetry instrumentation changes must be made inside the target app's `checkouts/<app>/` only.** The root-level directory and `apps/<app>/` config files are the test harness and must never be modified as part of an instrumentation task. If an instrumentation skill tries to create or edit files outside `checkouts/<app>/`, that is a mistake.

This is enforced — not just documented — by a hard sandbox on the instrumentation agent (`src/sandbox.ts`, wired in as a `PreToolUse` hook in `src/instrumentation.ts`). The agent's filesystem access within the harness tree is confined to its own `checkouts/<app>/` plus the bundled `otel/` tooling (so it can run `weaver`); any `Read`/`Write`/`Edit`/`Bash` that touches the harness's own files — `src/` (incl. `evaluation.ts`/`weaver.ts`), `EVALUATION.md`, `harness.sh`, collector/weaver config, `.env`, or other apps' checkouts — is denied. Paths outside the harness entirely (system toolchains, dependency caches, `$HOME`, `/tmp`) stay reachable so the agent can still build and verify. This prevents the agent from reading the eval criteria ("the answer key") and overfitting the score.

## Reviewing a skill

The skills under `agent-skill/` are the deliverable. When reviewing or editing one, read it **as the
agent that will actually run it** — a fresh, context-less agent whose *only* inputs are the skill text
plus whatever the harness hands it. It cannot see this repo, prior runs, the evaluation criteria, or the
reasoning behind a given line. Judge the skill purely on whether that agent, with those inputs, can
follow it to a correct result. The deliverable is now **two self-contained skills** (the "two boxes" —
see `docs/observability-boxes.md`); there is no conductor agent or instrumenter/verifier sub-agent.
Review each skill from its real entry point:

- **`otel-instrumentation`** ("make my app observable") — the reader is a context-less implementer
  handed an **initial instrumentation prompt** (repo path + app facts, nothing more). It owns the whole
  job end to end: gather → auto-instrument → export → enrich → define a weaver registry → prove under
  real traffic → hand off to `otel-verification` and fix what it flags → hand back. In the harness it
  runs **non-interactively** — there is no user to answer mid-run, so it must proceed autonomously from
  the brief alone.
- **`otel-verification`** ("how good is it") — the reader is a **clean agent** judging telemetry that
  **already exists**, with no knowledge of what was changed or why. It is **read-only**: it does not run
  the app or generate traffic. It reads the emitted telemetry (via the Honeycomb MCP) and judges it
  against the standards — current OTel semantic conventions (`search_semconv`/`get_semconv_attribute`)
  plus any org registry. It stands alone (audit existing instrumentation) and nests inside
  `otel-instrumentation`'s prove step.

Guidelines for what to write into a skill:

- **Avoid "scar tissue."** Don't accrete hyper-specific defensive instructions from individual past
  failures. Each run surfaces a concrete defect, but the fix in the skill should be the *general
  principle* that prevents the class of defect — not a narrow patch describing that one occurrence.
  Excess scar tissue makes a skill long, brittle, and overfit to the apps we happen to test.
- **Don't hardcode attribute (or metric) names unless absolutely necessary.** Prefer general, reactive
  guidance (e.g. "catalogue any passed-through library attribute the live-check flags") over naming
  specific attributes. Hardcoded names overfit to today's apps/instrumentation versions and rot quickly.

(More review guidance will be added here as we learn more.)

## Adding a new app

1. `mkdir apps/<name>`
2. **Claim ports in `ports.sh`** (the central registry) — add the app to `registered_apps()` and `app_ports()`, and define a var for **every** port it binds, including *implicit* ones the framework opens (embedded DBs, admin connectors, etc. — e.g. Broadleaf's HSQLDB on 9001). Ports must be globally disjoint; run `./harness.sh <name> ports` to verify no collisions. The harness kills processes on these ports before each `start`, so they must be accurate.
3. Create `apps/<name>/config.sh` — set `APP_NAME`, `APP_REPO`, `APP_CLEAN_SHA` (a commit SHA from the upstream repo; no fork required), `APP_OTEL_AGENT_TYPE`, reference the registry port vars (e.g. `APP_HTTP_PORT="$<NAME>_HTTP_PORT"`), and define `cmd_build()`, `cmd_start()` (and optionally `cmd_bootstrap()`, `cmd_status()`). Also set the **`APP_*` fact vars** the shared prompt template renders: `APP_DATASET` (service name), `APP_DESCRIPTION`, `APP_LANGUAGE`, `APP_FRAMEWORKS`, `APP_CODE_LOCATION`, `APP_BUILD_HINT`, `APP_START_HINT`, `APP_ENV_SURFACE`, `APP_READINESS` (and optionally `APP_STOP_HINT`, `APP_ATTR_NAMING`, `APP_WEAVER_REGISTRY`, `APP_IMPORT_REGISTRIES`). Anything you omit falls back to a sensible default in `harness.sh`. Keep these to **plain app facts** — no instrumentation how-to (that lives in the skill).
4. Create `apps/<name>/traffic.sh` — standalone script that generates traffic against the running app (use `${APP_HTTP_PORT}` etc., never hardcode ports)
5. Create `apps/<name>/EVALUATION.md` — evaluation checklist for verifying instrumentation quality

**Weaver criteria split.** The weaver live-check verdict is scored as **three** criteria —
`weaver_live_check_http`, `weaver_live_check_db`, `weaver_live_check_other` — bucketing each violation by
convention family (http = http/url/network/server/client/user_agent; db = `db.*`; other = everything
else). `http` and `db` gate independently (custom registry created + telemetry received + zero non-waived
violations in that bucket), so an app whose libraries lag one family fails only that bucket. `other` is
**informational only** (reported but non-gating): it is dominated by standard resource/SDK attributes
(`service.*`, `telemetry.sdk.*`) and other signal-less namespaces the app's libraries emit but can't
reshape. Bucketing is namespace-level, not per-attribute, to avoid overfitting.

**Eval-side config (optional, NOT rendered into the prompt).** `APP_WEAVER_WAIVERS` in `config.sh` is a
whitespace-separated list of semconv attribute-key / metric-name prefixes whose weaver *violations* are
waived within their bucket — for conventions the app's instrumentation libraries can't yet emit (so the
agent has no way to fix them, and a failure there would conflate a library limitation with a real gap). A
bare namespace waives the whole subtree (`db` waives `db.statement`, `db.rows_affected`, … and empties the
db bucket); a full key waives just that one. It's read only by `src/weaver.ts` in the trusted eval step and
is deliberately kept out of the agent prompt so it can't leak the scoring criteria. Use it sparingly — only
when a dep provably lags the spec (e.g. `realworld-go`'s GORM plugin emits the old DB semconv). See the
comment in `apps/realworld-go/config.sh`.

(No per-app preamble file: the prompt is the shared `instrument-preamble.template.md` filled from the `APP_*` vars above. Avoid em-dashes/apostrophes inside `${VAR:-default}` defaults in `harness.sh` — macOS bash 3.2 mis-parses them.)
7. Run `./harness.sh <name> download` to clone the repo
