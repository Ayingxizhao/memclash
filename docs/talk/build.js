// 7-minute CS2520 talk. Build: NODE_PATH=$(npm root -g) node build.js  -> talk.pptx
// Slides are added one at a time as they are agreed (academic-pptx: action titles, one exhibit per slide).
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = "/Users/yingxizhao/.claude/skills/synced/3933c22a-eca4-4299-a3d9-9838ccc72c4d_d8c5afa6-e7c4-4711-ad25-27b8c2793fd2/pptx";
const { applyTheme } = require(path.join(SKILL, "scripts/apply_theme.js"));

const THEME = {
  name: "CS2520 talk", headFontFace: "Arial", bodyFontFace: "Arial",
  colors: {
    dk1: "2D2D2D", lt1: "FFFFFF", dk2: "1F4E79", lt2: "F3F5F8",
    accent1: "2E75B6", accent2: "C0392B", accent3: "777777", accent4: "FFF2CC",
    accent5: "CCCCCC", accent6: "1F4E79", hlink: "2E75B6", folHlink: "1F4E79",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Memory rules for coding agents: read them with an LLM, enforce the clear ones with Z3";
const C = pres.SchemeColor;
const M = 0.5;

pres.defineSlideMaster({
  title: "TITLE_ONLY",
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.3, w: 9.0, h: 0.85,
        fontSize: 26, bold: true, color: C.text2, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 9.1, y: 5.2, w: 0.4, h: 0.3, fontSize: 11, color: C.accent3, align: "right" },
});

pres.defineSlideMaster({
  title: "TITLE",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 1.45, w: 8.6, h: 0.7,
        fontSize: 34, bold: true, color: C.background1, valign: "top", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.7, y: 3.3, w: 8.6, h: 1.0,
        fontSize: 16, color: C.background2, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});

// ---------------------------------------------------------------- slide 0: title
{
  const s = pres.addSlide({ masterName: "TITLE" });
  s.addText("Memory rules for coding agents", { placeholder: "title" });
  s.addText("Comparing an LLM judge and a Z3 solver on finding clashes and stopping rule breaks", { x: 0.7, y: 2.15, w: 8.6, h: 0.6,
    fontSize: 22, color: C.background2, margin: 0, isTextBox: true, objectName: "subtitle" });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.7, y: 3.15, w: 2.0, h: 0.04, fill: { color: C.background2 },
                                      line: { type: "none" }, objectName: "rule above author" });
  s.addText([
    { text: "Yuhe Tian", options: { bold: true, breakLine: true } },
    { text: "CS2520 class project" },
  ], { placeholder: "body" });
  s.addNotes("Hi, I'm Yuhe. This project is about the rules coding agents keep in their memory files: " +
             "whether we can find rules that clash, and whether we can make agents actually follow them.");
}

// ---------------------------------------------------------------- slide 1: the problem
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY" });
  s.addText("Coding agents break memory rules, even with the rule files loaded", { placeholder: "title" });
  // real transcript: hidden-rules trial, run D1-V-1 (aspect 2240 x 988)
  s.addImage({ path: path.join(__dirname, "assets/break_case.png"), x: M, y: 1.4, w: 5.7, h: 5.7 * 988 / 2240,
               altText: "CLAUDE.md says do not start tests unless asked; the agent reads its memory, edits the decoder, then runs the test suite anyway.",
               objectName: "break case screenshot" });
  s.addText([
    { text: "Rules sit in CLAUDE.md, loaded every session", options: { bullet: { indent: 14 }, breakLine: true } },
    { text: "The agent read its memory, then ran the tests anyway", options: { bullet: { indent: 14 }, breakLine: true } },
    { text: "With rule files loaded, 8 of 30 runs broke a rule", options: { bullet: { indent: 14 } } },
  ], { x: 6.45, y: 1.4, w: 3.05, h: 2.6, fontSize: 18, color: C.text1, valign: "top", paraSpaceAfter: 12,
       margin: 0, isTextBox: true, objectName: "takeaways" });
  s.addText("Real run from our hidden-rules trial (Claude Code, Sonnet 5.5). Repo: martinambrus/RDForward (public).",
            { x: M, y: 4.95, w: 8.4, h: 0.3, fontSize: 12, color: C.accent3, margin: 0, isTextBox: true, objectName: "source" });
  s.addNotes(
    "Coding agents like Claude Code keep project rules in memory files such as CLAUDE.md, loaded every session. " +
    "Here the project says: do not start tests unless the user asks. The user asked for a decoder fix. " +
    "The agent read its memory folder, made the fix, and then ran the test suite anyway, and reported it proudly. " +
    "This is not a one-off: in our trial, with the rule files loaded, 8 of 30 runs broke a rule. That counts rules in plain view (2 of 10) and rules we moved into a side file or buried among hundreds of others (3 of 10 each). " +
    "So the question of this talk: how do we make agents actually keep these rules?");
}

// ---------------------------------------------------------------- slide 2: two checkpoints
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY" });
  s.addText("Is formal verification useful for agent memory? We test it at two points",
            { placeholder: "title" });
  const box = (x, y, w, h, title, sub, name, strong) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08,
      fill: { color: strong ? C.text2 : C.background1 }, line: { color: C.text2, width: 1.25 }, objectName: name + " box" });
    const runs = [{ text: title, options: { bold: true, fontSize: 18, color: strong ? C.background1 : C.text2,
                                           breakLine: !!sub } }];
    if (sub) runs.push({ text: sub, options: { fontSize: 15, color: strong ? C.background2 : C.text1 } });
    s.addText(runs, { x: x + 0.15, y, w: w - 0.3, h, valign: "middle", margin: 0, paraSpaceAfter: 4,
                      isTextBox: true, objectName: name + " text" });
  };
  const arrow = (x, y, w, name) => s.addShape(pres.shapes.LINE, { x, y, w, h: 0,
    line: { color: C.accent3, width: 1.5, endArrowType: "triangle" }, objectName: name });
  const outcome = (y, text, name) => s.addText(text, { x: 7.2, y, w: 2.3, h: 0.9, fontSize: 16, bold: true,
    color: C.accent2, valign: "middle", margin: 0, isTextBox: true, objectName: name });

  // step 0: translation pipeline, policy-as-code style (vocab.py = fixed schema; boundary2.compiles = schema check)
  const step = (x, w, title, sub, name) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.3, w, h: 0.8, rectRadius: 0.06,
      fill: { color: C.background2 }, line: { color: C.accent1, width: 1 }, objectName: name + " box" });
    s.addText([{ text: title, options: { bold: true, fontSize: 14, color: C.text2, breakLine: true } },
               { text: sub, options: { fontSize: 12, color: C.text1 } }],
      { x: x + 0.1, y: 1.3, w: w - 0.2, h: 0.8, valign: "middle", margin: 0, isTextBox: true, objectName: name + " text" });
  };
  step(0.5, 1.75, "English rule", "from the memory file", "step rule");
  arrow(2.25, 1.7, 0.3, "arrow s1");
  step(2.55, 2.35, "LLM translates", "into our fixed schema", "step translate");
  arrow(4.9, 1.7, 0.3, "arrow s2");
  step(5.2, 2.05, "Schema check", "known fields, compiles", "step check");
  arrow(7.25, 1.7, 0.3, "arrow s3");
  step(7.55, 1.95, "Z3 constraints", "used at 1 and 2", "step z3");

  // row 1: memory update
  box(0.5, 2.4, 2.3, 0.85, "New rule", "written to memory", "new rule");
  arrow(2.8, 2.825, 0.5, "arrow rule to check");
  box(3.3, 2.4, 3.3, 0.85, "1  Z3 checks it", "against the existing rules", "check 1", true);
  arrow(6.6, 2.825, 0.5, "arrow check to outcome 1");
  outcome(2.375, "Clash?\nWarn before saving", "outcome 1");

  // row 2: agent action
  box(0.5, 3.45, 2.3, 0.85, "Agent wants", "to take a step", "agent step");
  arrow(2.8, 3.875, 0.5, "arrow step to gate");
  box(3.3, 3.45, 3.3, 0.85, "2  Z3 gate checks it", "against the rules", "check 2", true);
  arrow(6.6, 3.875, 0.5, "arrow gate to outcome 2");
  outcome(3.425, "Breaks a rule?\nBlock it", "outcome 2");

  s.addText([
    { text: "Rules in focus: ", options: { bold: true } },
    { text: "concrete actions on git, files and tasks, e.g. \"Never force-push main\"" },
  ], { x: M, y: 4.4, w: 9.0, h: 0.3, fontSize: 14, color: C.text1, margin: 0, isTextBox: true, objectName: "focus" });
  s.addText("Baseline for both: an LLM reading the same rules in English, no translation", { x: M, y: 4.72, w: 9.0, h: 0.3,
    fontSize: 14, color: C.text1, margin: 0, isTextBox: true, objectName: "baseline" });
  s.addText("Translation borrows the policy-as-code idea (cf. Open Policy Agent, AWS Cedar).",
    { x: M, y: 5.08, w: 8.4, h: 0.3, fontSize: 12, color: C.accent3, margin: 0, isTextBox: true, objectName: "source" });
  s.addNotes(
    "Before Z3 can check anything, each English rule is translated once. We borrow the policy-as-code idea: an LLM writes the rule as code over a fixed schema we defined, only git commands, file actions, tasks and a few yes-or-no facts. " +
    "If the output uses a field outside the schema or does not compile, it is rejected. The schema keeps the translation in a checkable form, but it cannot guarantee the meaning is right. " +
    "Our research question: is formal verification useful for agent memory? We test it at the two moments where it could help. First, when the memory file is updated: a new rule is checked " +
    "by Z3 against the existing rules, and if the two cannot both be followed we warn before saving. " +
    "Second, when the agent acts: a Z3 gate checks each step against the rules and blocks a step that breaks one. " +
    "We focus on rules about concrete actions: git commands, files, running tasks, like never force-push main. " +
    "For both, the baseline is simply an LLM reading the same rules in English, and that is what we measure Z3 against.");
}

// ---------------------------------------------------------------- slide 3: checkpoint 1 result (clashes)
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY" });
  s.addText("An LLM reading the whole folder finds more real clashes than Z3, because rules lose meaning in logic", { placeholder: "title" });
  // Counts: natural-folder study (5 repos, 22 clashes, data/runs/natural/full_gold.json) + the user's second run
  // (51 repos incl. the user's own: 7 with clashes, 20 clashes; reported by the user). Types / Z3 fit: the 22 only.
  const big = (t) => ({ text: t, options: { bold: true, color: C.text2, fontSize: 24 } });
  const small = (t) => ({ text: t, options: { color: C.text1, fontSize: 18 } });
  const arr = { text: "   \u2192   ", options: { color: C.accent3, fontSize: 18 } };
  s.addText([big("56"), small(" repos checked"), arr, big("12"), small(" had a clash"), arr, big("42"), small(" clashes")],
    { x: M, y: 1.3, w: 9.0, h: 0.55, margin: 0, valign: "middle", isTextBox: true, objectName: "funnel line" });

  // unit chart: one square per labelled clash, navy = fits Z3's logic
  s.addText("The 22 clashes we labelled in detail, by type", { x: M, y: 2.05, w: 5.9, h: 0.35, fontSize: 15,
    bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "chart title" });
  const rows = [["Which tool or command to use", 0, 12], ["A plan step vs a standing rule", 2, 2],
                ["Where files go", 2, 0], ["Allowed vs forbidden", 1, 1], ["A setting's value", 0, 2]];
  const SQ = 0.2, GAP = 0.06, X0 = 3.25;
  rows.forEach(([label, fit, nofit], k) => {
    const y = 2.5 + k * 0.38;
    s.addText(label, { x: M, y, w: 2.7, h: 0.3, fontSize: 14, color: C.text1, margin: 0, valign: "middle",
      isTextBox: true, objectName: "row " + label });
    for (let q = 0; q < fit + nofit; q++) {
      s.addShape(pres.shapes.RECTANGLE, { x: X0 + q * (SQ + GAP), y: y + 0.05, w: SQ, h: SQ,
        fill: { color: q < fit ? C.text2 : C.accent5 }, line: { type: "none" }, objectName: `${label} clash ${q + 1}` });
    }
  });
  const key = (x, color, text) => {
    s.addShape(pres.shapes.RECTANGLE, { x, y: 4.53, w: SQ, h: SQ, fill: { color }, line: { type: "none" },
      objectName: "key " + text });
    s.addText(text, { x: x + 0.3, y: 4.47, w: 2.2, h: 0.32, fontSize: 14, color: C.text1, margin: 0, valign: "middle",
      isTextBox: true, objectName: "key text " + text });
  };
  key(M, C.text2, "fits Z3's logic: 5");
  key(M + 2.4, C.accent5, "does not fit: 17");

  // two real examples, colour-matched
  const card = (y, color, head, body, name) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 6.75, y, w: 0.07, h: 0.82, fill: { color }, line: { type: "none" },
      objectName: name + " marker" });
    s.addText([{ text: head, options: { bold: true, color: C.text1, breakLine: true } },
               { text: body, options: { color: C.text1 } }],
      { x: 6.95, y, w: 2.55, h: 0.82, fontSize: 12, valign: "top", margin: 0, isTextBox: true, objectName: name });
  };
  card(2.05, C.text2, "Fits Z3's logic",
       "\"Never force push the fork main branch\" vs \"Force-push the reset main branch for each fork\"", "example fits");
  card(2.97, C.accent5, "Does not fit",
       "\"Call powershell -File script.ps1\" vs \"Quote the whole -Command argument\"", "example does not fit");
  card(3.89, C.accent2, "Why Z3 found fewer",
       "Meaning lost in translation: a dropped \"may\", a target with no file path, a narrowed scope", "why z3 lost");

  s.addText("Clash: two rules in one repo's memory that cannot both be followed. Labels: two AI reviewers and the author.",
            { x: M, y: 4.98, w: 8.4, h: 0.3, fontSize: 11, color: C.accent3, margin: 0, isTextBox: true, objectName: "source" });
  s.addNotes(
    "Checkpoint one: when a new rule is written, does it clash with an old one? We checked 56 repos; 12 had at least one " +
    "clash, 42 in all. Here are the 22 we labelled in detail, one square each. Navy squares are clashes Z3's logic can " +
    "express, like never force-push main versus force-push main for each fork. Grey ones it cannot, mostly which tool or " +
    "command to use, like two different ways to call PowerShell. Only 5 of 22 are navy, so at memory-update time Z3 can " +
    "only ever catch a small share of real clashes. Head to head, one LLM call reading the whole folder found more of " +
    "the real clashes than Z3. Z3 lost on translation, not on solving: a dropped may, a target with no file path, a narrowed scope.");
}

// ---------------------------------------------------------------- slide 4: checkpoint 2 accuracy (actions)
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY" });
  s.addText("When the agent acts, Z3 rivals the LLM on rules it can express, but few rules qualify", { placeholder: "title" });
  // Frozen (preregistered) F1 on violations. enforce_results.md (B2 vs A2, one review each); boundary_judge/
  // scores_frozen.json (Z3 0.908, DeepSeek 1.0); boundary2/judge_s1/scores.json primary (Z3 0.936, Haiku 0.864).
  const base = 4.05, full = 1.95;
  s.addText("F1, catching rule breaks", { x: M, y: 1.35, w: 3.0, h: 0.35, fontSize: 15, bold: true,
    color: C.text1, margin: 0, isTextBox: true, objectName: "chart title" });
  const key = (x, color, label) => {
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.44, w: 0.18, h: 0.18, fill: { color }, line: { type: "none" },
      objectName: "legend " + label });
    s.addText(label, { x: x + 0.25, y: 1.36, w: 1.4, h: 0.34, fontSize: 13, color: C.text1, margin: 0, isTextBox: true,
      objectName: "legend text " + label });
  };
  // Updated F1 (user's runs on another device): all rules n=334 (114 + 200 new actions): Z3 0.78, DeepSeek 0.87,
  // Haiku 0.85. Rules Z3 can express, 101 actions (boundary2 stage 1): Z3 0.97, DeepSeek 0.90, Haiku 0.89. Round 1 dropped.
  const COLS = [C.text2, C.accent5, "999999"], NAMES = ["Z3", "DeepSeek", "Haiku"];
  key(3.1, COLS[0], "Z3"); key(3.75, COLS[1], "DeepSeek"); key(4.95, COLS[2], "Haiku");
  const groups = [
    { name: "All rules\n334 actions", v: [0.78, 0.87, 0.85], x: 0.8 },
    // 101 actions: boundary2 stage 1 minus S1-009/049/103 (no folder contents stated; undecidable for every arm).
    // Z3 0.967 and Haiku 0.894 recomputed from judge_s1/; DeepSeek 0.90 from the user's run.
    { name: "Rules Z3 can express\n101 actions", v: [0.97, 0.90, 0.89], x: 3.65 },
  ];
  for (const g of groups) {
    g.v.forEach((val, b) => {
      const h = full * val, x = g.x + b * 0.68;
      s.addShape(pres.shapes.RECTANGLE, { x, y: base - h, w: 0.58, h, fill: { color: COLS[b] },
        line: { type: "none" }, objectName: `${g.name} bar ${NAMES[b]}` });
      s.addText(val.toFixed(2), { x: x - 0.15, y: base - h - 0.32, w: 0.88, h: 0.3, fontSize: 14, bold: true,
        color: C.text1, align: "center", margin: 0, isTextBox: true, objectName: `${g.name} value ${NAMES[b]}` });
    });
    s.addText(g.name, { x: g.x - 0.2, y: base + 0.06, w: 2.38, h: 0.5, fontSize: 12,
      color: C.text1, align: "center", valign: "top", margin: 0, isTextBox: true, objectName: g.name + " label" });
  }
  s.addShape(pres.shapes.LINE, { x: M, y: base, w: 5.6, h: 0, line: { color: C.accent3, width: 1 }, objectName: "baseline" });

  s.addText([{ text: "1\u20132%", options: { fontSize: 32, bold: true, color: C.accent2, breakLine: true } },
             { text: "of about 8,000 real rules can be written exactly in Z3's logic", options: { fontSize: 14, color: C.text1 } }],
    { x: 6.55, y: 1.4, w: 2.95, h: 1.3, valign: "top", margin: 0, isTextBox: true, objectName: "coverage stat" });
  s.addText([
    { text: "Every Z3 miss: a rule it could not express, or a translation gap", options: { bullet: { indent: 14 }, breakLine: true } },
    { text: "Z3: 0.5 s for 114 actions, free, same answer every time", options: { bullet: { indent: 14 } } },
  ], { x: 6.55, y: 2.85, w: 2.95, h: 1.8, fontSize: 14, color: C.text1, valign: "top", paraSpaceAfter: 8, margin: 0,
       isTextBox: true, objectName: "takeaways" });
  s.addText("Frozen, preregistered runs. After logged fixes Z3 scores 1.00 and 0.97 on the two expressible-rule tests. Codex left out: it helped build the tests.",
            { x: M, y: 4.98, w: 9.0, h: 0.3, fontSize: 10, color: C.accent3, margin: 0, isTextBox: true, objectName: "source" });
  s.addNotes(
    "Checkpoint two: the agent is about to act; does the action break a rule? On all real rules (334 actions), Z3 reaches " +
    "F1 0.78 against 0.87 for DeepSeek and 0.85 for Haiku reading the same rules, because some rules cannot be written in " +
    "its logic. On rules that can be (101 actions), Z3 wins: 0.97 against 0.90 and 0.89. Every Z3 miss came from a rule " +
    "it could not express or a translation gap, never the solver. Where it applies, it is instant, free and deterministic.");
}

// ---------------------------------------------------------------- slide 5: live gate in real agent runs
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY" });
  s.addText("In real agent runs, the Z3 gate caught every tracked rule break, with no false blocks",
            { placeholder: "title" });
  // data/runs/hidden_rules/scores.json: N 4/10, V 2/10, T 3/10, B 3/10; TG+BG 10 runs, 4 attempted breaks, all blocked;
  // replay over all 50 runs: 21 of 21 gold breaks flagged, 0 false flags.
  s.addText("Claude Code agent (Sonnet 5.5), 10 runs per setup", { x: M, y: 1.35, w: 5.9, h: 0.35, fontSize: 15,
    bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "chart title" });
  const rows = [["Rules in CLAUDE.md", 2, 0], ["Rule in a side file", 3, 0],
                ["Rule buried among hundreds", 3, 0], ["Side file or buried + Z3 gate", 0, 4]];
  const SQ = 0.24, GAP = 0.06, X0 = 3.25;
  rows.forEach(([label, broke, blocked], k) => {
    const y = 1.85 + k * 0.46 + (k === 3 ? 0.14 : 0);
    s.addText(label, { x: M, y, w: 2.7, h: 0.32, fontSize: 14, bold: k === 3, color: k === 3 ? C.text2 : C.text1,
      margin: 0, valign: "middle", isTextBox: true, objectName: "row " + label });
    for (let q = 0; q < 10; q++) {
      const isBroke = q < broke, isBlocked = q < blocked;
      s.addShape(pres.shapes.RECTANGLE, { x: X0 + q * (SQ + GAP), y: y + 0.04, w: SQ, h: SQ,
        fill: { color: isBroke ? C.accent2 : isBlocked ? C.text2 : C.accent5 }, line: { type: "none" },
        objectName: `${label} run ${q + 1}` });
      if (isBlocked) s.addText("\u00d7", { x: X0 + q * (SQ + GAP), y: y + 0.04, w: SQ, h: SQ, fontSize: 14, bold: true,
        color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: `${label} blocked ${q + 1}` });
    }
  });
  const key = (x, color, text, mark) => {
    s.addShape(pres.shapes.RECTANGLE, { x, y: 4.12, w: 0.2, h: 0.2, fill: { color }, line: { type: "none" },
      objectName: "key " + text });
    if (mark) s.addText("\u00d7", { x, y: 4.12, w: 0.2, h: 0.2, fontSize: 11, bold: true, color: C.background1,
      align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "key mark" });
    s.addText(text, { x: x + 0.28, y: 4.06, w: 2.0, h: 0.32, fontSize: 13, color: C.text1, margin: 0, valign: "middle",
      isTextBox: true, objectName: "key text " + text });
  };
  key(M, C.accent2, "broke a rule");
  key(M + 1.75, C.text2, "break blocked by gate", true);
  key(M + 4.0, C.accent5, "no break");

  s.addText("What the gate did", { x: 6.6, y: 1.35, w: 2.75, h: 0.35, fontSize: 15, bold: true, color: C.text1,
    margin: 0, isTextBox: true, objectName: "gate header" });
  const gl = (y, big, small, name) => {
    s.addText(big, { x: 6.5, y, w: 1.05, h: 0.48, fontSize: 17, bold: true, color: C.text2, align: "right",
      valign: "middle", margin: 0, isTextBox: true, objectName: name + " number" });
    s.addText(small, { x: 7.65, y, w: 1.9, h: 0.48, fontSize: 12, color: C.text1, valign: "middle", margin: 0,
      isTextBox: true, objectName: name + " label" });
  };
  // count runs, to match the squares: rows 1-3 = 2+3+3 = 8 runs with a break (11 breaks), all flagged in replay;
  // row 4 = 4 runs, one attempted break each, all blocked live.
  gl(1.72, "8 of 8", "runs with a break flagged (rows 1\u20133)", "gate watching");
  gl(2.22, "4 of 4", "runs with a break blocked (row 4)", "gate blocking");
  gl(2.72, "0", "false flags, all 40 runs", "gate false flags");
  s.addShape(pres.shapes.RECTANGLE, { x: 6.75, y: 3.35, w: 0.07, h: 1.1, fill: { color: C.text2 }, line: { type: "none" },
    objectName: "quote marker" });
  s.addText([{ text: "After a block, the agent complied:", options: { bold: true, breakLine: true } },
             { text: "\"I didn't run the tests, because a project policy here blocks running them unless you ask.\"",
               options: { italic: true } }],
    { x: 6.95, y: 3.35, w: 2.55, h: 1.1, fontSize: 12, color: C.text1, valign: "top", margin: 0, isTextBox: true,
      objectName: "agent quote" });
  s.addText("5 tasks, sandboxed, 40 runs with rules loaded. Gate holds the 25 rules Z3 can express. Two AI labellers agreed on every run.",
            { x: M, y: 4.98, w: 9.0, h: 0.3, fontSize: 11, color: C.accent3, margin: 0, isTextBox: true, objectName: "source" });
  s.addNotes(
    "Last, a real agent: Claude Code with Sonnet, on five coding tasks, ten runs per setup, with the rules loaded. " +
    "Each square is a run; red means it broke a rule. With the rule in CLAUDE.md, 2 of 10 runs broke one; with it in a " +
    "side file or buried among hundreds, 3 of 10. With the Z3 gate on, the agent tried to break a rule 4 times and the gate " +
    "blocked all 4 before they ran; after each block it complied and told the user why. In the other runs the gate only " +
    "watched: across all 40 runs it flagged all 15 breaks, with no false flags. For context, with no rules given at all, the " +
    "same tasks led to a forbidden step in 4 of 10 runs. Caveat: the gate only covers rules Z3 can express, here 25.");
}

// ---------------------------------------------------------------- slide 6: speed and cost, by task
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY" });
  s.addText("Z3 is faster per check, and a new rule costs one translation, not a full re-read", { placeholder: "title" });
  // Task 1 (one new rule). Z3: whole-folder joint check, largest folder 51 rules = 6.3 s (group_timing.json); translate the new rule ~8 s est. (group bench: ~1,350 output tokens per
  // rule at ~160 tok/s) + joint check 6.3 s = ~14 s; pair check 5 ms median (clash_timing.json); ~$0.001 (bench: $0.04 / 48
  // rules). LLM: one whole-folder call ~47k output tokens (experiment_log N3) at ~160 tok/s (DeepSeek, measured in the
  // action tests: 145-169 tok/s) = ~300 s est.; ~$0.03 per folder (billed).
  // Task 2 (per 100 actions, measured): Z3 0.5 s; Haiku 16 s; DeepSeek 150 s (171 s / 114); DeepSeek ~$0.01.
  // Layout: columns = task, rows = time and cost. Haiku ran on a subscription: no billed cost, so not in the cost row.
  const head = (x, t, sub, name) => s.addText([{ text: t, options: { bold: true, fontSize: 16, color: C.text2, breakLine: true } },
      { text: sub, options: { fontSize: 12, color: C.text1 } }],
    { x, y: 1.3, w: 4.3, h: 0.55, valign: "top", margin: 0, isTextBox: true, objectName: name + " head" });
  const bars = (x, y, rowName, rows, name) => {
    s.addText(rowName, { x, y, w: 4.3, h: 0.26, fontSize: 13, bold: true, color: C.accent3, margin: 0, valign: "middle",
      isTextBox: true, objectName: `${name} ${rowName} row` });
    const MAX = Math.max(...rows.map(r => r[1])), MAXW = 1.75;
    rows.forEach(([label, v, txt, isZ3], k) => {
      const yy = y + 0.3 + k * 0.32, w = Math.max(MAXW * v / MAX, 0.03);
      s.addText(label, { x, y: yy, w: 1.4, h: 0.28, fontSize: 12, bold: isZ3, color: C.text1, margin: 0, valign: "middle",
        isTextBox: true, objectName: `${name} ${rowName} ${label} label` });
      s.addShape(pres.shapes.RECTANGLE, { x: x + 1.45, y: yy + 0.04, w, h: 0.2, fill: { color: isZ3 ? C.text2 : C.accent5 },
        line: { type: "none" }, objectName: `${name} ${rowName} ${label} bar` });
      s.addText(txt, { x: x + 1.45 + w + 0.08, y: yy, w: 1.0, h: 0.28, fontSize: 12, bold: true, color: C.text1, margin: 0,
        valign: "middle", isTextBox: true, objectName: `${name} ${rowName} ${label} value` });
    });
  };
  head(M, "1  Finding clashes", "Same memory for both: 51 rules", "task 1");
  bars(M, 1.95, "Time", [["Z3, add 1 rule", 14, "~14 s", true], ["Z3, first check", 66, "~1 min", true],
                         ["LLM, every check", 180, "~3 min", false]], "task 1");
  bars(M, 3.3, "Cost", [["Z3, add 1 rule", 0.001, "~$0.001", true], ["Z3, first check", 0.04, "~$0.04", true],
                        ["LLM, every check", 0.02, "~$0.02", false]], "task 1");
  s.addShape(pres.shapes.LINE, { x: 4.95, y: 1.4, w: 0, h: 3.3, line: { color: C.accent5, width: 1 }, objectName: "divider" });
  head(5.2, "2  Stopping rule breaks", "Per 100 agent actions", "task 2");
  bars(5.2, 1.95, "Time", [["Z3", 0.5, "0.5 s", true], ["Haiku", 16, "16 s", false], ["DeepSeek", 150, "150 s", false]], "task 2");
  bars(5.2, 3.3, "Cost", [["Z3", 0, "$0", true], ["DeepSeek", 0.01, "~$0.01", false]], "task 2");
  s.addText("~ = estimate: LLM output scaled from an 84-rule call (47k tokens) at ~160 tokens/s; Z3 check (6 s) and translation speed measured.",
            { x: M, y: 4.98, w: 9.0, h: 0.3, fontSize: 11, color: C.accent3, margin: 0, isTextBox: true, objectName: "source" });
  s.addNotes(
    "Speed and cost, compared on the same memory: 51 rules, our largest translated folder. Finding clashes: when you add a rule, Z3 only " +
    "translates that one rule, then checks all the rules together, so clashes among three or more rules are caught too: about 14 seconds and a tenth of a cent. " +
    "An LLM has to re-read all 51 rules every time, about 3 minutes and 2 cents by our estimate. The very first check is different: Z3 must translate every rule, about a minute and 4 cents, so Z3 pays off as memory grows rule by rule. " +
    "Stopping rule breaks: Z3 checks 100 actions in half a second, free, and gives the same answer every run; an LLM takes " +
    "16 to 150 seconds and bills every check; Codex even changed 6 of 114 verdicts between runs. Haiku ran on a subscription, so it has no billed cost. The tilde numbers are estimates from measured token speed and billing.");
}

// ---------------------------------------------------------------- slide 7: conclusion
{
  const s = pres.addSlide({ masterName: "TITLE_ONLY" });
  s.addText("Formal verification is useful as a fast gate for simple action rules, not as a general rule reader",
            { placeholder: "title" });
  const finding = (y, n, head, body, name) => {
    s.addText(n, { x: M, y, w: 0.45, h: 0.7, fontSize: 24, bold: true, color: C.accent1, margin: 0, valign: "top",
      isTextBox: true, objectName: name + " number" });
    s.addText([{ text: head, options: { bold: true, fontSize: 16, color: C.text2, breakLine: true } },
               { text: body, options: { fontSize: 14, color: C.text1 } }],
      { x: M + 0.55, y, w: 5.3, h: 0.85, valign: "top", margin: 0, isTextBox: true, objectName: name });
  };
  finding(1.4, "1", "Finding clashes: the LLM finds more",
          "Most real clashes are about tools and plans that Z3's logic cannot express", "finding 1");
  finding(2.4, "2", "Stopping rule breaks: Z3 matches where it applies",
          "In real agent runs the gate caught every tracked break, with no false blocks", "finding 2");
  finding(3.4, "3", "Speed and cost: Z3 wins and scales",
          "Milliseconds, free, same answer every run; a new rule is one more constraint", "finding 3");

  s.addShape(pres.shapes.RECTANGLE, { x: 6.55, y: 1.4, w: 2.95, h: 2.7, fill: { color: C.accent4 }, line: { type: "none" },
    objectName: "recommendation box" });
  s.addText([{ text: "Use both", options: { bold: true, fontSize: 22, color: C.text2, breakLine: true } },
             { text: "An LLM reads the whole memory. Z3 gates the few rules it can express exactly, like \"never read .env\".",
               options: { fontSize: 16, color: C.text1 } }],
    { x: 6.75, y: 1.4, w: 2.6, h: 2.7, valign: "middle", margin: 0, paraSpaceAfter: 8, isTextBox: true, objectName: "recommendation" });

  s.addText([{ text: "Limits: ", options: { bold: true } },
             { text: "only 1\u20132% of rules fit Z3's logic; small samples; labels by AI reviewers and the author." }],
    { x: M, y: 4.4, w: 9.0, h: 0.35, fontSize: 13, color: C.text1, margin: 0, isTextBox: true, objectName: "limits" });
  s.addText("Code and data: github.com/Ayingxizhao/memclash", { x: M, y: 4.95, w: 8.4, h: 0.3, fontSize: 12,
    color: C.accent1, margin: 0, isTextBox: true, hyperlink: { url: "https://github.com/Ayingxizhao/memclash" },
    objectName: "repo link" });
  s.addNotes(
    "So, is formal verification useful for agent memory? Yes, but narrowly. For finding clashes, an LLM reading the whole " +
    "folder finds more, because most real clashes are about tools and plans that Z3 cannot express. For stopping rule " +
    "breaks, Z3 matches the LLM on the rules it can express, and as a live gate it caught every tracked break with no false " +
    "blocks. And it is milliseconds, free, and consistent, and it scales as memory grows. My recommendation: use both. Let " +
    "an LLM read the memory, and put Z3 in front of the few clear-cut action rules. Limits: only 1 to 2 percent of rules " +
    "fit, samples are small, and labels come from AI reviewers and me. Thank you.");
}

(async () => {
  const out = path.join(__dirname, "talk.pptx");
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("wrote", out);
})();
