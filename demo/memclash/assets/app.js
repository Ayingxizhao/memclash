/* memclash report viewer: loads one report (a sample from reports/, or a report.json the user
   opens), draws the shared top bar, then renders the page named in <body data-page>. */
(function () {
  "use strict";
  var KEY_SAMPLE = "memclash:sample", KEY_OWN = "memclash:own-report";
  var TYPE_LABEL = { clash: "Clash", exception: "Exception", state_conflict: "State conflict" };
  var TYPE_HELP = {
    clash: "No single action follows both rules in this situation.",
    exception: "A rule says the agent may do something that the other rule forbids. The author may have meant an exception; a priority rule is needed.",
    state_conflict: "One rule needs a path in the repository, the other forbids it.",
  };
  var STATUS_LABEL = { ok: "checked", not_in_scope: "not in scope", unclear: "unclear wording", invalid_output: "bad output" };

  function store(fn) { try { return fn(); } catch (e) { return null; } }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function param(name) { var m = new RegExp("[?&]" + name + "=([^&]*)").exec(location.search); return m ? decodeURIComponent(m[1]) : ""; }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src; s.onload = resolve; s.onerror = function () { reject(new Error("Could not load " + src)); };
      document.head.appendChild(s);
    });
  }

  function loadReport() {
    var own = store(function () { return sessionStorage.getItem(KEY_OWN); });
    if (own) {
      try { return Promise.resolve({ report: JSON.parse(own), own: true }); } catch (e) { /* fall back to sample */ }
    }
    return loadScript("reports/index.js").then(function () {
      var samples = window.MEMCLASH_SAMPLES || [];
      var want = store(function () { return sessionStorage.getItem(KEY_SAMPLE); }) || (samples[0] && samples[0].name);
      if (!samples.some(function (s) { return s.name === want; })) want = samples[0].name;
      return loadScript("reports/" + want + ".js").then(function () {
        return { report: window.MEMCLASH_REPORT, own: false, sample: want, samples: samples };
      });
    });
  }

  function ruleById(rep, id) { return rep.rules.find(function (r) { return r.id === id; }); }
  function sev(type) { return '<span class="sev ' + type + '">' + esc(TYPE_LABEL[type] || type) + "</span>"; }
  function statusPill(r) {
    var cls = r.status === "ok" ? "ok" : "muted";
    var txt = STATUS_LABEL[r.status] || r.status;
    if (r.status === "unclear" && r.word) txt += ": “" + r.word + "”";
    return '<span class="sev ' + cls + '">' + esc(txt) + "</span>";
  }
  function ruleLink(rep, id) { var r = ruleById(rep, id); return '<a href="rule.html?id=' + encodeURIComponent(id) + '">' + esc(id) + "</a>" + (r ? ' <span class="file">' + esc(r.file) + "</span>" : ""); }

  function topBar(state) {
    var rep = state.report, page = document.body.dataset.page, s = rep.summary;
    var tabs = [
      ["index", "Overview", null], ["findings", "Findings", s.clash + s.exception + s.state_conflict],
      ["rules", "Rules", s.rules], ["ambiguous", "Ambiguous", s.unclear],
      ["skipped", "Not checked", s.not_in_scope + s.bad_output + s.with_unknown_condition],
    ];
    var current = page === "finding" ? "findings" : page === "rule" ? "rules" : page;
    var options = (state.samples || []).map(function (x) {
      return '<option value="' + esc(x.name) + '"' + (x.name === state.sample ? " selected" : "") + ">" + esc(x.label) + "</option>";
    }).join("");
    var picker = state.own
      ? '<span class="note">your report</span> <button class="btn" id="use-samples" type="button">Back to samples</button>'
      : '<label class="note" for="sample">Report</label> <select id="sample">' + options + "</select>";
    $("#bar").innerHTML =
      '<div class="bar-in gutter">' +
      '<a class="brand" href="index.html"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h10M4 12h7M4 18h12" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/><path d="M17 9l4 6M21 9l-4 6" stroke="var(--clash)" stroke-width="2" stroke-linecap="round" fill="none"/></svg>memclash</a>' +
      '<span class="folder" title="Scanned folder">' + esc(rep.folder) + "</span>" +
      '<div class="bar-tools">' + picker + "</div>" +
      '<nav class="tabs" aria-label="Report pages">' + tabs.map(function (t) {
        return '<a href="' + t[0] + '.html"' + (t[0] === current ? ' aria-current="page"' : "") + ">" + t[1] +
          (t[2] != null ? '<span class="count">' + t[2] + "</span>" : "") + "</a>";
      }).join("") + "</nav></div>";
    var sel = $("#sample");
    if (sel) sel.addEventListener("change", function () { store(function () { sessionStorage.setItem(KEY_SAMPLE, sel.value); }); location.reload(); });
    var back = $("#use-samples");
    if (back) back.addEventListener("click", function () { store(function () { sessionStorage.removeItem(KEY_OWN); }); location.reload(); });
  }

  /* ---------- pages ---------- */
  var pages = {};

  pages.index = function (state) {
    var rep = state.report, s = rep.summary;
    var tiles = [
      ["findings.html?type=clash", "clash", s.clash, "clashes"],
      ["findings.html?type=exception", "exception", s.exception, "exceptions (blocked “may”)"],
      ["findings.html?type=state_conflict", "state_conflict", s.state_conflict, "state conflicts"],
      ["rules.html", "", s.rules, "rules found"],
      ["rules.html?status=ok", "", s.checked, "rules checked"],
      ["skipped.html", "", s.not_in_scope + s.unclear + s.bad_output, "rules not checked"],
    ];
    $("#main").innerHTML =
      '<div class="pagehead"><span class="label">Overview</span><h1>' + esc(rep.folder) + "</h1>" +
      '<p class="sub">Scanned ' + esc(rep.created) + " · model " + esc(rep.model) + " · translation run " + esc(rep.run) + "</p></div>" +
      '<div class="grid">' + tiles.map(function (t) {
        return '<a class="tile ' + t[1] + '" href="' + t[0] + '"><span class="n">' + t[2] + '</span><span class="l">' + t[3] + "</span></a>";
      }).join("") + "</div>" +
      '<div class="panel"><h2>Top findings</h2><div class="list">' +
      (rep.findings.slice(0, 3).map(function (f) { return findingItem(rep, f); }).join("") || '<p class="empty">No clashes found in this folder.</p>') +
      '</div><a href="findings.html">All findings →</a></div>' +
      '<div class="two">' +
      '<div class="panel"><h2>Scan a folder</h2><p>Run the scanner on a repository or a memory folder. It writes a report file that this viewer opens.</p>' +
      '<div class="cmd">memclash scan path/to/repo --runs 3 --out report.json</div>' +
      '<p class="note">In this project the same steps run as <code>prep/extract.py</code>, then <code>pipeline/rules/cli.py translate</code> and <code>report</code>.</p></div>' +
      '<div class="panel"><h2>Open a report</h2><div class="drop" id="drop">Drop a <code>report.json</code> here, or <label class="btn" for="file">choose a file</label><input id="file" type="file" accept=".json,application/json" hidden></div>' +
      '<p class="note" id="open-msg">The report stays in this browser tab only.</p></div></div>';
    var drop = $("#drop"), input = $("#file"), msg = $("#open-msg");
    function open(file) {
      var fr = new FileReader();
      fr.onload = function () {
        try {
          var rep2 = JSON.parse(fr.result);
          if (rep2.tool !== "memclash" || !rep2.rules || !rep2.findings) throw new Error("not a memclash report");
          if (!store(function () { sessionStorage.setItem(KEY_OWN, fr.result); return true; })) throw new Error("this browser blocked storage for the tab");
          location.reload();
        } catch (e) { msg.textContent = "Could not open " + file.name + ": " + e.message + "."; msg.className = "note error"; }
      };
      fr.readAsText(file);
    }
    input.addEventListener("change", function () { if (input.files[0]) open(input.files[0]); });
    drop.addEventListener("dragover", function (e) { e.preventDefault(); drop.classList.add("over"); });
    drop.addEventListener("dragleave", function () { drop.classList.remove("over"); });
    drop.addEventListener("drop", function (e) { e.preventDefault(); drop.classList.remove("over"); if (e.dataTransfer.files[0]) open(e.dataTransfer.files[0]); });
  };

  function findingItem(rep, f) {
    var a = ruleById(rep, f.a), b = ruleById(rep, f.b);
    return '<a class="item ' + f.type + '" href="finding.html?id=' + f.id + '">' + sev(f.type) +
      '<div class="rules"><div><span class="rid">' + esc(f.a) + " · " + esc(a.file) + "</span><div>" + esc(a.rule) + "</div></div>" +
      '<span class="vs">VS</span><div><span class="rid">' + esc(f.b) + " · " + esc(b.file) + "</span><div>" + esc(b.rule) + "</div></div>" +
      '<div class="when">When: ' + esc(f.situation.join("; ")) + "</div></div>" +
      '<span class="go">' + esc(f.id) + " →</span></a>";
  }

  pages.findings = function (state) {
    var rep = state.report, active = param("type");
    var types = ["clash", "exception", "state_conflict"];
    function draw() {
      var list = rep.findings.filter(function (f) { return !active || f.type === active; });
      $("#list").innerHTML = list.map(function (f) { return findingItem(rep, f); }).join("") ||
        '<p class="empty panel">No findings of this kind.</p>';
      document.querySelectorAll(".chip").forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.type === active)); });
    }
    $("#main").innerHTML =
      '<div class="pagehead"><span class="label">Findings</span><h1>Pairs of rules that cannot both be followed</h1>' +
      '<p class="sub">Each finding names the situation where the two rules meet. Open one to see how both rules were read.</p></div>' +
      '<div class="filters" role="group" aria-label="Filter by kind"><button class="chip" type="button" data-type="">All ' + rep.findings.length + "</button>" +
      types.map(function (t) { return '<button class="chip" type="button" data-type="' + t + '">' + TYPE_LABEL[t] + " " + rep.summary[t] + "</button>"; }).join("") + "</div>" +
      '<div class="list" id="list"></div>';
    document.querySelectorAll(".chip").forEach(function (c) { c.addEventListener("click", function () { active = c.dataset.type; draw(); }); });
    draw();
  };

  function clauseBlock(rep, ref, cls) {
    var r = ruleById(rep, ref.rule), c = r.clauses[ref.clause];
    return '<li class="' + cls + '"><span class="rid">' + ruleLink(rep, ref.rule) + "</span><span>" + esc(ref.text) + "</span>" +
      '<details><summary>as translated</summary><pre>' + esc(JSON.stringify({ type: c.type, where: c.where, needs: c.needs, when_unmodeled: c.when_unmodeled }, null, 2)) + "</pre></details></li>";
  }

  pages.finding = function (state) {
    var rep = state.report, f = rep.findings.find(function (x) { return x.id === param("id"); });
    if (!f) { $("#main").innerHTML = '<p class="panel">No finding with this id. <a href="findings.html">See all findings</a>.</p>'; return; }
    var a = ruleById(rep, f.a), b = ruleById(rep, f.b);
    var detail = f.type === "state_conflict"
      ? '<p>Path <code>' + esc(f.path) + "</code> is required by " + esc(f.needs) + " and forbidden by " + esc(f.blocked_by) + ".</p>"
      : '<ul class="clauses">' + clauseBlock(rep, f.needs, "needs") + "</ul>" +
        '<p class="note">blocked by</p><ul class="clauses">' + f.blocked_by.map(function (x) { return clauseBlock(rep, x, "blocked"); }).join("") + "</ul>";
    $("#main").innerHTML =
      '<div class="pagehead"><span class="label"><a href="findings.html">Findings</a> / ' + esc(f.id) + "</span>" +
      "<h1>" + sev(f.type) + " " + esc(f.a) + " vs " + esc(f.b) + "</h1><p class=\"sub\">" + esc(TYPE_HELP[f.type]) + "</p></div>" +
      '<div class="two">' + [a, b].map(function (r) {
        return '<div class="panel"><span class="rid">' + ruleLink(rep, r.id) + '</span><p class="rule-text">' + esc(r.rule) + "</p></div>";
      }).join("") + "</div>" +
      '<div class="panel"><h2>Situation</h2><ul class="situation">' + f.situation.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul></div>" +
      '<div class="panel"><h2>Why no action works</h2><p class="note">This part is required</p>' + detail +
      '<p class="note">Checked with the Z3 solver: in this situation, no action meets the first part without breaking the second.</p></div>';
  };

  pages.rules = function (state) {
    var rep = state.report, filter = param("status"), q = "";
    function draw() {
      var rows = rep.rules.filter(function (r) {
        return (!filter || r.status === filter) && (!q || (r.rule + " " + r.file + " " + r.id).toLowerCase().indexOf(q) >= 0);
      });
      $("#rows").innerHTML = rows.map(function (r) {
        return '<tr><td class="id"><a href="rule.html?id=' + encodeURIComponent(r.id) + '">' + esc(r.id) + "</a></td><td>" + esc(r.rule) +
          '<div class="file">' + esc(r.file) + "</div></td><td>" + statusPill(r) + "</td><td>" +
          esc(r.clauses.map(function (c) { return c.text; }).join(" · ") || r.reason) + "</td></tr>";
      }).join("") || '<tr><td colspan="4" class="empty">No rules match.</td></tr>';
    }
    var statuses = ["", "ok", "not_in_scope", "unclear", "invalid_output"];
    $("#main").innerHTML =
      '<div class="pagehead"><span class="label">Rules</span><h1>Every rule found in the folder</h1>' +
      '<p class="sub">One line per rule, as extracted from the files, with how it was read.</p></div>' +
      '<div class="filters"><label class="note" for="q">Search</label><input id="q" type="search" placeholder="text, file or id">' +
      '<label class="note" for="st">Status</label><select id="st">' + statuses.map(function (s) {
        return '<option value="' + s + '"' + (s === filter ? " selected" : "") + ">" + (s ? STATUS_LABEL[s] : "all") + "</option>";
      }).join("") + "</select></div>" +
      '<div class="tablewrap"><table><thead><tr><th>Id</th><th>Rule</th><th>Status</th><th>Read as</th></tr></thead><tbody id="rows"></tbody></table></div>';
    $("#q").addEventListener("input", function (e) { q = e.target.value.toLowerCase(); draw(); });
    $("#st").addEventListener("change", function (e) { filter = e.target.value; draw(); });
    draw();
  };

  pages.rule = function (state) {
    var rep = state.report, r = ruleById(rep, param("id"));
    if (!r) { $("#main").innerHTML = '<p class="panel">No rule with this id. <a href="rules.html">See all rules</a>.</p>'; return; }
    var related = rep.findings.filter(function (f) { return f.a === r.id || f.b === r.id; });
    $("#main").innerHTML =
      '<div class="pagehead"><span class="label"><a href="rules.html">Rules</a> / ' + esc(r.id) + '</span><h1 class="rule-text">' + esc(r.rule) + "</h1>" +
      '<p class="file">' + esc(r.file) + "</p><div>" + statusPill(r) + "</div></div>" +
      '<div class="panel"><h2>How it was read</h2>' +
      (r.clauses.length ? '<ul class="clauses">' + r.clauses.map(function (c) {
        return "<li>" + esc(c.text) + '<details><summary>as translated</summary><pre>' + esc(JSON.stringify({ type: c.type, where: c.where, needs: c.needs, when_unmodeled: c.when_unmodeled }, null, 2)) + "</pre></details></li>";
      }).join("") + "</ul>" : "<p>" + esc(r.reason || "Not translated.") + "</p>") +
      (r.left_out ? '<p class="note">Left out: ' + esc(r.left_out) + "</p>" : "") +
      (r.retried ? '<p class="note">The first answer did not fit the format and was asked again.</p>' : "") + "</div>" +
      '<div class="panel"><h2>Findings with this rule</h2><div class="list">' +
      (related.map(function (f) { return findingItem(rep, f); }).join("") || '<p class="note">None.</p>') + "</div></div>";
  };

  pages.ambiguous = function (state) {
    var rep = state.report, rows = rep.rules.filter(function (r) { return r.status === "unclear"; });
    $("#main").innerHTML =
      '<div class="pagehead"><span class="label">Ambiguous</span><h1>Rules that can be read more than one way</h1>' +
      '<p class="sub">The wording does not settle what the rule asks. Another agent, or the same agent on another day, may read it differently. These are worth rewording in the memory folder.</p></div>' +
      '<div class="list">' + (rows.map(function (r) {
        return '<a class="item" href="rule.html?id=' + encodeURIComponent(r.id) + '"><span class="sev muted">“' + esc(r.word) + "”</span>" +
          '<div class="rules"><span class="rid">' + esc(r.id) + " · " + esc(r.file) + "</span><div>" + esc(r.rule) + '</div><div class="when">' + esc(r.reason) + '</div></div><span class="go">' + esc(r.id) + " →</span></a>";
      }).join("") || '<p class="empty panel">No ambiguous rules in this report.</p>') + "</div>";
  };

  pages.skipped = function (state) {
    var rep = state.report;
    var groups = [
      ["Conditions the format cannot check", "These rules apply only under a condition the format has no words for. A clash that depends on such a condition is not reported.",
        rep.rules.filter(function (r) { return r.unmodeled && r.unmodeled.length; }), function (r) { return r.unmodeled.join("; "); }],
      ["Not in scope", "Not about git, files or running a task (code style, tool choice, …), or nothing concrete was left to check.",
        rep.rules.filter(function (r) { return r.status === "not_in_scope"; }), function (r) { return r.reason; }],
      ["Bad output", "The translation did not fit the format twice in a row, so the rule was skipped.",
        rep.rules.filter(function (r) { return r.status === "invalid_output"; }), function (r) { return r.reason; }],
    ];
    $("#main").innerHTML =
      '<div class="pagehead"><span class="label">Not checked</span><h1>What this scan could not decide</h1>' +
      '<p class="sub">A clean report does not mean these rules are safe. Check them by hand.</p></div>' +
      groups.map(function (g) {
        return '<div class="panel"><h2>' + esc(g[0]) + ' <span class="count">' + g[2].length + "</span></h2><p class=\"note\">" + esc(g[1]) + "</p>" +
          (g[2].length ? '<div class="tablewrap"><table><thead><tr><th>Id</th><th>Rule</th><th>Why</th></tr></thead><tbody>' + g[2].map(function (r) {
            return '<tr><td class="id"><a href="rule.html?id=' + encodeURIComponent(r.id) + '">' + esc(r.id) + "</a></td><td>" + esc(r.rule) + '<div class="file">' + esc(r.file) + "</div></td><td>" + esc(g[3](r)) + "</td></tr>";
          }).join("") + "</tbody></table></div>" : '<p class="note">None.</p>') + "</div>";
      }).join("");
  };

  loadReport().then(function (state) {
    topBar(state);
    (pages[document.body.dataset.page] || pages.index)(state);
  }).catch(function (e) {
    $("#main").innerHTML = '<p class="panel error">' + esc(e.message) + ". Run <code>cli.py report</code> to write a report into <code>reports/</code>.</p>";
  });
})();
