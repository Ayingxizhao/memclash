/**
 * memclash for Pi: a Z3 gate over the agent's memory rules (test use only).
 *
 * - Gives the agent exactly one memory file (MEMCLASH_MEMORY, default MEMORY.md) in its prompt.
 * - Before every tool call, asks `memclash gate`; blocks the call if it breaks a compiled rule.
 * - Before the agent changes the memory file, compiles the new content and runs `memclash check`.
 *   If a new rule clashes with an old one, the user chooses: keep the old rule, replace it, or keep
 *   both. If the change deletes an old rule that the new one contradicts, the user confirms it. After an allowed change the rules are recompiled so the gate uses them.
 * - /memclash [status|compile|clash]
 *
 * Load for one run only:  pi -e ./integrations/pi --no-context-files --no-session
 * The Python core is pipeline/rules/memclash.py in this repository.
 */
import { readFileSync, existsSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const ROOT = process.env.MEMCLASH_ROOT ?? resolve(dirname(fileURLToPath(import.meta.url)), "../../..");
const PY = process.env.MEMCLASH_PY ?? join(ROOT, ".venv/bin/python");
const MEMORY = process.env.MEMCLASH_MEMORY ?? "MEMORY.md";
// MEMCLASH_SHOW_MEMORY=0 hides the memory file from the agent: only the gate knows the rules
const SHOW_MEMORY = process.env.MEMCLASH_SHOW_MEMORY !== "0";

type Event = Record<string, unknown>;

export default function (pi: ExtensionAPI) {
  const prior: Event[] = []; // earlier steps of this session, for "only after X" rules
  const pending = new Map<string, Event[]>(); // allowed calls waiting for their result
  let userAskedTests = false; // the user's latest message asks to run tests (simple keyword match)

  pi.on("input", async (event) => {
    if (event.source === "extension") return;
    userAskedTests = /\b(run|rerun|execute|start)\b[^.?!]{0,30}\btests?\b|\btests?\b[^.?!]{0,15}\b(run|go)\b/i.test(event.text);
  });

  async function core(args: string[], cwd: string) {
    // pi.exec has no env option, so PYTHONPATH goes through `env`
    const r = await pi.exec("env", [`PYTHONPATH=${join(ROOT, "pipeline")}`, PY, "-m", "rules.memclash", ...args],
      { cwd: ROOT, timeout: 600_000 });
    if (r.code !== 0) throw new Error(`memclash ${args[0]} failed: ${r.stderr.slice(-400)}`);
    return JSON.parse(r.stdout.trim().split("\n").pop() ?? "{}");
  }

  function rulesInfo(cwd: string) {
    const p = join(cwd, ".memclash/rules.json");
    if (!existsSync(p)) return null;
    const rules = JSON.parse(readFileSync(p, "utf8")).rules as { gate: boolean }[];
    return { translated: rules.length, gate: rules.filter((r) => r.gate).length };
  }

  pi.on("session_start", async (_e, ctx) => {
    const info = rulesInfo(ctx.cwd);
    ctx.ui.notify(info ? `memclash: ${info.gate} gate rules from ${MEMORY}`
                       : `memclash: no compiled rules; run /memclash compile`, info ? "info" : "warning");
  });

  // the one memory file the agent gets (run Pi with --no-context-files so nothing else loads)
  pi.on("before_agent_start", async (event, ctx) => {
    const p = join(ctx.cwd, MEMORY);
    if (!SHOW_MEMORY || !existsSync(p)) return;
    return { systemPrompt: `${event.systemPrompt}\n\n# Project memory (${MEMORY})\n\n${readFileSync(p, "utf8")}` };
  });

  const isMemory = (path: unknown, cwd: string) =>
    typeof path === "string" && resolve(cwd, path) === resolve(cwd, MEMORY);

  // the memory file as it would be after this edit/write call
  function nextMemory(toolName: string, input: any, cwd: string): string | null {
    if (toolName === "write") return input.content ?? "";
    let text = readFileSync(join(cwd, MEMORY), "utf8");
    for (const e of input.edits ?? []) {
      if (!text.includes(e.oldText)) return null; // the edit tool will reject it anyway
      text = text.replace(e.oldText, e.newText);
    }
    return text;
  }

  const KEEP_OLD = "Keep the existing rule (do not save the new one)";
  const REPLACE = "Replace: save the new rule and remove the rule(s) it clashes with";
  const BOTH = "Keep both anyway";
  const CONFIRM = "Yes, replace the old rule";

  const approved = new Set<string>(); // old rules the user already chose to replace
  async function checkMemoryEdit(event: any, ctx: any) {
    const next = nextMemory(event.toolName, event.input, ctx.cwd);
    if (next === null) return;
    mkdirSync(join(ctx.cwd, ".memclash"), { recursive: true });
    const file = join(ctx.cwd, ".memclash/next_memory.md");
    writeFileSync(file, next);
    ctx.ui.notify(`memclash: checking the new rule(s) against ${MEMORY} ...`, "info");
    const c = await core(["check", ctx.cwd, MEMORY, file], ctx.cwd);
    c.replaced = c.replaced.filter((x: { removed: string }) => !approved.has(x.removed)); // already chosen by the user
    if (!c.clashes.length && !c.replaced.length) return;
    const added = new Set<string>(c.new_rules);
    const eg = (a?: Record<string, unknown>) => a ? ` (e.g. ${a.cmd}${a.branch ? " on " + a.branch : ""})` : "";
    const lines: string[] = [];
    for (const x of c.clashes as { english: string[] | null; verdict: string; action?: Record<string, unknown> }[]) {
      if (!x.english) { lines.push(`  - all rules together cannot be followed (${x.verdict})`); continue; }
      const [a, b] = x.english;
      const [nu, ex] = added.has(a) ? [a, b] : [b, a];
      lines.push(`  - new: "${nu}"\n    clashes with: "${ex}"${eg(x.action)}`);
    }
    for (const x of c.replaced as { removed: string; new: string; action?: Record<string, unknown> }[])
      lines.push(`  - new: "${x.new}"\n    deletes and overrides: "${x.removed}"${eg(x.action)}`);
    const oldRules = [...new Set((c.clashes as { english: string[] | null }[]).flatMap((x) => (x.english ?? []).filter((r) => !added.has(r))))];
    const summary = `memclash: this change to ${MEMORY} conflicts with existing rules:\n${lines.join("\n")}`;
    if (!ctx.hasUI) return { block: true, reason: `${summary}\nAsk the user what to do before changing ${MEMORY}.` };
    // a clash between rules that would both stay: keep old / replace / keep both
    // only an overwrite of an old rule: confirm it or keep the old rule
    const options = c.clashes.length ? [KEEP_OLD, REPLACE, BOTH] : [CONFIRM, KEEP_OLD];
    const choice = await ctx.ui.select(summary, options);
    if (choice === CONFIRM) { ctx.ui.notify("memclash: replacement confirmed by the user", "info"); return; }
    if (choice === BOTH) {
      ctx.ui.notify("memclash: saved with the clash; the gate keeps enforcing the old rule(s)", "warning");
      return;
    }
    if (choice === REPLACE) {
      oldRules.forEach((r) => approved.add(r));
      return { block: true, reason: `${summary}\nThe user chose to REPLACE. Edit ${MEMORY} again: add the new rule and remove these rules:\n` +
        oldRules.map((r) => `  - ${r}`).join("\n") };
    }
    return { block: true, reason: `${summary}\nThe user chose to KEEP the existing rule(s). ${MEMORY} was not changed; tell the user.` };
  }

  pi.on("tool_call", async (event, ctx) => {
    if (["edit", "write"].includes(event.toolName) && isMemory((event.input as any)?.path, ctx.cwd)) {
      const r = await checkMemoryEdit(event, ctx);
      if (r) return r;
    }
    const r = await core(["gate", ctx.cwd, JSON.stringify({ tool: event.toolName, input: event.input, prior, flags: { user_asked: userAskedTests } })], ctx.cwd);
    if (r.block) {
      ctx.ui.notify(r.reason, "warning");
      return { block: true, reason: r.reason };
    }
    pending.set(event.toolCallId, r.events as Event[]);
  });

  pi.on("tool_result", async (event, ctx) => {
    // record the step with its real outcome (a failed lint or test run does not count as "ran successfully")
    prior.push(...(pending.get(event.toolCallId) ?? []).map((e) => ({ ...e, ok: !event.isError })));
    pending.delete(event.toolCallId);
    // the memory file changed: recompile so the gate enforces the new rules
    if (event.isError || !["edit", "write"].includes(event.toolName) || !isMemory((event.input as any)?.path, ctx.cwd)) return;
    const r = await core(["compile", ctx.cwd, "--memory", MEMORY], ctx.cwd);
    ctx.ui.notify(`memclash: ${MEMORY} recompiled, ${r.gate} gate rules`, "info");
  });

  pi.registerCommand("memclash", {
    description: "memclash: status | compile | clash",
    handler: async (args, ctx) => {
      const sub = (args || "status").trim();
      if (sub === "compile") {
        ctx.ui.notify(`memclash: compiling ${MEMORY} ...`, "info");
        const r = await core(["compile", ctx.cwd, "--memory", MEMORY], ctx.cwd);
        ctx.ui.notify(`memclash: ${r.rules} rules, ${r.translated} translated, ${r.gate} usable by the gate, ` +
                      `${r.untranslated} not expressible`, "info");
      } else if (sub === "clash") {
        const c = await core(["clash", ctx.cwd], ctx.cwd);
        ctx.ui.notify(c.clashes.length ? JSON.stringify(c.clashes, null, 1) : "memclash: no clashes", "info");
      } else {
        const info = rulesInfo(ctx.cwd);
        ctx.ui.notify(info ? `memclash: ${info.translated} translated rules, ${info.gate} in the gate (${MEMORY})`
                           : "memclash: no compiled rules", "info");
      }
    },
  });
}
