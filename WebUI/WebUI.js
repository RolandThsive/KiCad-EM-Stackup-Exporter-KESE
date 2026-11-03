/* WebUI.js - the page: the board, the Mode switch, the settings (one section per parameter file), Generate, the
   3D preview, the checks, the parts and the downloads.

   KESE itself runs in PyodideWorker.js.  Nothing about a parameter is written here: the names, defaults, help
   texts, choices, presets, modes and formats come from Generator/parameters/*.py and kese/job.py, read when the page
   starts (WebGenerator.describe).  The page's own settings are in webui.json: which parameters Basic shows, the
   section titles, the few parameters shown outside the sections (Mode, the file formats, Verify), the preview order.

   Every value lives in one object (state.values, keyed "Module.NAME" as `kese --set` takes them) that Basic and
   Advanced both edit.  A run's files are kept on the visitor's disk until the page is left (OutputStore.js).

   Sections: state, worker, small helpers, tooltips, labels, value changes, widgets, sections, mode and formats,
   board, generate, preview, checks, parts, downloads, dialogs, import / export, start. */

import { OutputStore } from "./OutputStore.js";
import { Viewer } from "./Viewer.js";

const QUERY = new URLSearchParams(location.search);
const CFG = window.KESE_CONFIG;
const PYODIDE = QUERY.get("pyodide") || CFG.pyodide;           // ?pyodide=<url> for local testing

/* ---- state --------------------------------------------------------------------------------------- */
const state = {
  desc: null, params: [], byKey: {}, values: {}, start: {},
  ui: "basic", open: new Set(CFG.basicOpen || []), lastNumbers: {}, noneEditing: new Set(),
  formatsByMode: {},                      // the formats last ticked in each mode
  board: null,                            // {name, bytes, meta}
  result: null, runValues: null, stale: false, showInfo: false, busy: false, ready: false,
  preview: { key: null }, materials: null, version: null,
};
const store = new OutputStore();
let viewer = null;
const $ = (id) => document.getElementById(id);

/* ---- worker ---------------------------------------------------------------------------------------- */
let worker, nextId = 1;
const pending = new Map();
function ask(cmd, args) {
  return new Promise((resolve, reject) => {
    const id = nextId++;
    pending.set(id, { resolve, reject });
    worker.postMessage({ id, cmd, args });
  });
}
function startWorker() {
  worker = new Worker(new URL("./PyodideWorker.js", import.meta.url), { type: "module" });
  worker.onmessage = (ev) => {
    const m = ev.data;
    if (m.type === "progress") { setProgressText(m.text); return; }
    if (m.type === "line") { runLine(m); return; }
    const p = pending.get(m.id); if (!p) return;
    pending.delete(m.id);
    if (m.ok) p.resolve(m.result); else p.reject(new Error(m.error));
  };
  worker.onerror = (e) => fatal("The Python worker stopped: " + (e.message || e));
}

/* ---- small helpers ------------------------------------------------------------------------------- */
function el(tag, attrs = {}, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else if (v === true) e.setAttribute(k, "");
    else if (v !== false && v != null) e.setAttribute(k, v);
  }
  for (const k of kids.flat()) if (k != null) e.append(k.nodeType ? k : document.createTextNode(k));
  return e;
}
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const clone = (x) => JSON.parse(JSON.stringify(x));
function fmt(x) { return typeof x === "number" ? String(Number(x.toPrecision(10))) : String(x); }
function bytesText(n) { return n >= 1048576 ? `${(n / 1048576).toFixed(1)} MB` : n >= 1024 ? `${Math.round(n / 1024)} KB` : `${n} B`; }
function countText(n) { return n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${Math.round(n / 1e3)}k` : String(n); }
let toastTimer;
function toast(text, ms = 2600) {
  const t = $("toast"); t.textContent = text; t.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => (t.hidden = true), ms);
}
function setProgressText(text) {
  if (!state.ready) $("btn-generate").textContent = text.replace("…", "") + "…";
  $("checks-list").replaceChildren(el("p", { class: "hint" }, text));
}
function checkRow(level, stage, msg) {
  return el("div", { class: "check " + level }, el("span", { class: "lvl" }, level.toUpperCase()), el("span", { class: "stage" }, stage),
    el("span", { class: "msg" }, msg));
}
/* ---- while a run works: the generator's current line, as its command line shows it ------------------------- */
// A stage line ("running geometry (...) ... 1m 23s") counts up each second, like the terminal's status line;
// a log line replaces it until the next stage starts.
function hms(s) { const m = Math.floor(s / 60); return `${m}m ${String(Math.floor(s % 60)).padStart(2, "0")}s`; }
const run = { t0: 0, timer: 0, stage: null };
function runStart() {
  run.t0 = performance.now(); run.stage = null;
  $("run-line").textContent = "Starting…";
  $("run-card").hidden = false;
  $("run-note").textContent = "KESE is running in your browser. A big board can take from a minute to an hour.";
  run.timer = setInterval(runTick, 1000);
}
function runTick() {
  if (run.stage) $("run-line").textContent = `running ${run.stage} ... ${hms((performance.now() - run.t0) / 1000)}`;
}
function runLine(m) {
  if (m.kind === "stage") { run.stage = m.text; runTick(); }
  else { run.stage = null; $("run-line").textContent = m.text.trim(); }
}
function runStop() { clearInterval(run.timer); run.timer = 0; run.stage = null; $("run-card").hidden = true; }
function seconds(s) { return s < 60 ? `${s.toFixed(0)} s` : hms(s); }

function setBusy(on) { state.busy = on; $("progress").classList.toggle("busy", on); }
function fatal(text) {
  setBusy(false);
  $("btn-generate").textContent = "Python Did Not Start";
  $("checks-list").replaceChildren(checkRow("error", "start", text));
}
function download(blob, name) {
  const url = URL.createObjectURL(blob instanceof Blob ? blob : new Blob([blob]));
  const a = el("a", { href: url, download: name });
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 10000);
}
const stem = (name) => name.replace(/\.[^.]+$/, "");

/* ---- tooltips: every parameter (data-help = its key) and every button (data-tip = the text) ------ */
function showValue(v) {
  if (v === null || v === undefined) return "None";
  if (typeof v === "boolean") return v ? "True" : "False";
  if (Array.isArray(v)) return `[${v.map(showValue).join(", ")}]`;
  if (typeof v === "object") return JSON.stringify(v);
  return fmt(v);
}
let tipTimer = null, tipFor = null;
function hideTip() { clearTimeout(tipTimer); tipFor = null; $("popover").hidden = true; }
function showTip(node) {
  const pop = $("popover");
  pop.replaceChildren();
  if (node.dataset.help) {
    const p = state.byKey[node.dataset.help];
    pop.append(el("span", { class: "mono-name" }, `${p.file} · ${p.name}`));
    pop.append(p.help || "No notes in the parameter file.");
    pop.append(el("span", { class: "tip-foot" }, `In the file: ${showValue(p.default)}`));
  } else pop.append(node.dataset.tip);
  pop.hidden = false;
  const r = node.getBoundingClientRect();
  const below = r.bottom + 8, above = r.top - pop.offsetHeight - 8;
  pop.style.top = (below + pop.offsetHeight < innerHeight - 6 || above < 6 ? Math.max(6, Math.min(below, innerHeight - pop.offsetHeight - 6)) : above) + "px";
  pop.style.left = Math.max(6, Math.min(innerWidth - pop.offsetWidth - 6, r.left)) + "px";
}
document.addEventListener("mouseover", (e) => {
  const node = e.target.closest("[data-tip], [data-help]");
  if (node === tipFor) return;
  hideTip();
  if (!node || (node.dataset.tip !== undefined && !node.dataset.tip)) return;
  tipFor = node;
  tipTimer = setTimeout(() => showTip(node), e.target.closest(".info-dot") ? 0 : 450);
});
document.addEventListener("mousedown", hideTip);
document.addEventListener("scroll", hideTip, true);

/* ---- labels: made from the parameter's name ---------------------------------------------------- */
const UNITS = { MM: "mm", UM: "µm", DEG: "deg", HZ: "Hz", S_PER_M: "S/m", PCT: "%" };
function labelOf(name) {
  let rest = name, unit = "";
  for (const [suffix, u] of Object.entries(UNITS)) {
    if (rest.endsWith("_" + suffix)) { rest = rest.slice(0, -suffix.length - 1); unit = u; break; }
  }
  const words = rest.split("_").map((w) => (w.length <= 3 && !/^(ON|OF|TO|IN|AND|OR|PER|THE|FOR|MAX|MIN|USE|ARC|AUTO|PAD|VIA|PTH|NET)$/.test(w) ? w : w[0] + w.slice(1).toLowerCase()));
  return { text: words.join(" "), unit };
}
// a choice as words: "copper_hull" -> "Copper hull"; names with capitals (ENIG, F.SilkS) stay as they are
function choiceText(v) {
  if (typeof v !== "string") return showValue(v);
  if (v !== v.toLowerCase() || /^[^aeiouy]{1,3}$/.test(v)) return v;    // units ("mm", "m") stay as they are
  const s = v.replace(/_/g, " ");
  return s[0].toUpperCase() + s.slice(1);
}
function attachHelp(node, key) {
  node.dataset.help = key;
  node.append(el("i", { class: "info-dot", "aria-label": "Help" }, "i"));
  return node;
}

/* ---- value changes ----------------------------------------------------------------------------- */
function setValues(changes, from) {
  let any = false;
  for (const [k, v] of Object.entries(changes)) {
    if (!(k in state.byKey)) continue;
    if (!same(state.values[k], v)) { state.values[k] = clone(v); any = true; }
  }
  if (!any) return;
  if (state.result) state.stale = true;
  refresh(from);
}
function refresh() {
  renderMode();
  renderSections();
  renderFormats();
  $("verify").checked = !!state.values[CFG.verify];
  updateStale();
}
function updateStale() {
  const ok = state.result && state.result.ok;
  $("stale-badge").hidden = !(ok && state.stale);
  $("btn-download").disabled = !ok || state.stale || state.busy;
  $("btn-download").dataset.tip = state.stale ? "The settings changed: press Generate first" : "Download this run as one zip";
  for (const b of $("download-files").querySelectorAll("button")) b.disabled = !ok || state.stale || state.busy;
}

/* ---- widgets ----------------------------------------------------------------------------------- */
function stepOf(p) {
  if (p.kind === "int") return 1;
  const d = typeof p.default === "number" ? p.default : state.lastNumbers[p.key];
  if (typeof d !== "number" || d === 0) return 0.001;
  const dec = (String(d).split(".")[1] || "").length;
  if (!dec) return Math.abs(d) >= 10 ? 1 : 0.1;
  return Math.pow(10, -Math.min(dec, 6));
}
function stepper(value, onCommit, { step = 0.001, integer = false, disabled = false, placeholder = "" } = {}) {
  const input = el("input", { type: "text", inputmode: "decimal", value: value == null ? "" : fmt(value), disabled, placeholder });
  const len = (value == null ? "" : fmt(value)).length;
  if (len > 6) input.style.width = `${len + 2}ch`;
  const commit = (x) => {
    if (!Number.isFinite(x)) { input.value = value == null ? "" : fmt(value); return; }
    if (integer) x = Math.round(x);
    onCommit(Number(x.toPrecision(10)));
  };
  input.addEventListener("change", () => commit(parseFloat(input.value)));
  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowUp" || e.key === "ArrowDown") { e.preventDefault(); commit((parseFloat(input.value) || 0) + (e.key === "ArrowUp" ? step : -step)); }
  });
  return el("span", { class: "stepper" },
    el("button", { type: "button", disabled, "aria-label": "Less", onclick: () => commit((value ?? 0) - step) }, "−"), input,
    el("button", { type: "button", disabled, "aria-label": "More", onclick: () => commit((value ?? 0) + step) }, "+"));
}
function switchRow(checked, text, onChange, attrs = {}) {
  const cb = el("input", { type: "checkbox" }); cb.checked = !!checked;
  cb.addEventListener("change", () => onChange(cb.checked));
  return el("label", { class: "switch-row", ...attrs }, el("span", { class: "switch" }, cb, el("span", { class: "knob" })), text);
}
function dropdown(options, value, onPick) {
  const dd = el("div", { class: "dropdown" });
  const btn = el("button", { type: "button", class: "dropdown-btn" }, el("span", {}, choiceText(value)), el("span", { class: "arrow" }, "▾"));
  const menu = el("div", { class: "dropdown-content" });
  for (const o of options) menu.append(el("a", { class: same(o, value) ? "on" : "", onclick: () => { dd.classList.remove("open"); onPick(o); } }, choiceText(o)));
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    document.querySelectorAll(".dropdown.open").forEach((d) => d !== dd && d.classList.remove("open"));
    dd.classList.toggle("open");
  });
  dd.append(btn, menu);
  return dd;
}
document.addEventListener("click", () => document.querySelectorAll(".dropdown.open").forEach((d) => d.classList.remove("open")));

function widget(p) {
  const key = p.key, v = state.values[key], set = (x) => setValues({ [key]: x }, "field");
  switch (p.kind) {
    case "bool":
      return switchRow(v, v ? "On" : "Off", set);
    case "choice": {
      if (p.choices.length <= 3 && p.choices.every((c) => choiceText(c).length <= 10)) {
        const seg = el("div", { class: "segmented" });
        for (const c of p.choices) seg.append(el("button", { type: "button", class: same(v, c) ? "on" : "", onclick: () => set(c) }, choiceText(c)));
        return seg;
      }
      return dropdown(p.choices, v, set);
    }
    case "multi": {
      const box = el("div", { class: "multi-row" });
      for (const c of p.choices) {
        box.append(switchRow((v || []).includes(c), choiceText(c), (on) => {
          const now = new Set(state.values[key] || []);
          if (on) now.add(c); else now.delete(c);
          set(p.choices.filter((x) => now.has(x)));                 // in the file's order
        }));
      }
      return box;
    }
    case "int": case "num":
      return stepper(v, set, { step: stepOf(p), integer: p.kind === "int" });
    case "num_or_none": {
      const isNone = v === null && !state.noneEditing.has(key);
      const row = el("div", { class: "auto-row" });
      row.append(switchRow(isNone, "None", (on) => {
        if (on) { if (typeof state.values[key] === "number") state.lastNumbers[key] = state.values[key]; state.noneEditing.delete(key); set(null); renderSections(); }
        else if (typeof state.lastNumbers[key] === "number") set(state.lastNumbers[key]);
        else { state.noneEditing.add(key); renderSections(); const i = document.querySelector(`[data-key="${key}"] .stepper input`); if (i) i.focus(); }
      }, { "data-tip": "None: KESE takes the value from the board file or works it out (see the help)" }));
      row.append(stepper(v, (x) => { state.noneEditing.delete(key); set(x); }, { step: stepOf(p), disabled: isNone, placeholder: "number" }));
      return row;
    }
    case "str": {
      const t = el("input", { class: "text-input", value: v ?? "" });
      t.addEventListener("change", () => set(t.value));
      return t;
    }
    default: {
      const table = tableWidget(p, v, set);
      if (table) return table;
                                                                     // any other shape: edited as JSON text
      const t = el("textarea", { class: "text-input literal", rows: Math.min(8, JSON.stringify(v, null, 1).split("\n").length), spellcheck: "false" });
      t.value = JSON.stringify(v, null, 1);
      t.addEventListener("change", () => {
        try { set(JSON.parse(t.value)); } catch (e) { toast(`${p.name}: not valid (${e.message})`, 5000); t.value = JSON.stringify(state.values[key], null, 1); }
      });
      return t;
    }
  }
}

/* ---- tables (the dict parameters: Finish.FINISH_TYPES, Color.MATERIALS, ...) ------------------------------
   A dropdown picks one entry; under it, that entry's value with the widget its shape needs: a colour, a number,
   a name (a dropdown when the names come from another table), a few named values (a material), or a list of
   (metal, mm) layers. */
const HEX = /^#[0-9a-f]{6}$/i;
// a table whose values name entries of another table: its value is picked from that table's names
const NAMES_FROM = { "Finish.FINISH_NAME_ALIASES": "Finish.FINISH_TYPES" };
// a table whose (name, number) layers name entries of another table
const LAYER_NAMES_FROM = { "Finish.FINISH_TYPES": "Finish.FINISH_CONDUCTIVITY_S_PER_M" };
const isLayers = (x) => Array.isArray(x) && x.every((r) => Array.isArray(r) && r.length === 2 && typeof r[0] === "string" && typeof r[1] === "number");
const isScalar = (x) => typeof x === "number" || typeof x === "string" || typeof x === "boolean";
function tableShape(v) {
  if (!v || typeof v !== "object" || Array.isArray(v)) return null;
  const vals = Object.values(v);
  if (!vals.length) return null;
  if (vals.every((x) => typeof x === "string" && HEX.test(x))) return "color";
  if (vals.every((x) => typeof x === "number")) return "number";
  if (vals.every((x) => typeof x === "string")) return "name";
  if (vals.every(isLayers)) return "layers";
  if (vals.every((x) => x && typeof x === "object" && !Array.isArray(x) && Object.values(x).every(isScalar))) return "record";
  return null;
}
function numStep(x) {
  if (typeof x !== "number" || x === 0) return 0.001;
  const a = Math.abs(x);
  return a >= 1e4 ? Math.pow(10, Math.floor(Math.log10(a)) - 1) : a >= 10 ? 1 : a >= 1 ? 0.1 : Math.pow(10, Math.floor(Math.log10(a)) - 1);
}
// the colour as a whole swatch with its hex code on it; clicking it opens the system's colour picker
function inkOn(hex) {                                              // dark or light text, whichever reads on the colour
  const n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
  return 0.299 * r + 0.587 * g + 0.114 * b > 150 ? "#1d1d1f" : "#ffffff";
}
function colorPicker(value, onPick) {
  const start = HEX.test(value) ? value.toUpperCase() : "#000000";
  const c = el("input", { type: "color", value: start.toLowerCase(), "aria-label": "Colour" });
  const hex = el("span", { class: "swatch-hex" }, start);
  const box = el("label", { class: "swatch", "data-tip": "Click to choose the colour" }, c, hex);
  const paint = (h) => { box.style.background = h; box.style.color = inkOn(h); hex.textContent = h; };
  paint(start);
  c.addEventListener("input", () => paint(c.value.toUpperCase()));
  c.addEventListener("change", () => onPick(c.value.toUpperCase()));
  return box;
}
function valueWidget(x, onSet, names) {
  if (typeof x === "boolean") return switchRow(x, x ? "On" : "Off", onSet);
  if (typeof x === "number") return stepper(x, onSet, { step: numStep(x) });
  if (typeof x === "string" && HEX.test(x)) return colorPicker(x, onSet);
  if (typeof x === "string" && names && names.length) return dropdown(names.includes(x) ? names : [x, ...names], x, onSet);
  const t = el("input", { class: "text-input", value: x ?? "" });
  t.addEventListener("change", () => onSet(t.value));
  return t;
}
function tableWidget(p, v, set) {
  const shape = tableShape(v);
  if (!shape) return null;
  const keys = Object.keys(v);
  state.tableSel = state.tableSel || {};
  let sel = keys.includes(state.tableSel[p.key]) ? state.tableSel[p.key] : keys[0];
  const pick = (k) => { state.tableSel[p.key] = k; renderSections(); };
  const put = (val) => set({ ...state.values[p.key], [sel]: val });
  const namesOf = (k) => (state.values[k] && typeof state.values[k] === "object" ? Object.keys(state.values[k]) : null);

  // the entry row: a dropdown of the table's entries
  const head = el("div", { class: "table-head" }, dropdown(keys, sel, pick));

  // the entry's value
  const x = v[sel], body = el("div", { class: "table-body" });
  if (shape === "record") {
    for (const [k, y] of Object.entries(x))
      body.append(el("div", { class: "table-row" }, el("span", { class: "table-label" }, choiceText(k)),
        valueWidget(y, (z) => put({ ...state.values[p.key][sel], [k]: z }))));
  } else if (shape === "layers") {
    const names = namesOf(LAYER_NAMES_FROM[p.key]);
    body.append(el("div", { class: "table-row table-cols" }, el("span", {}, "Layer, bottom to top"), el("span", {}, "mm")));
    x.forEach(([name, mm], i) => {
      const rowSet = (j, z) => { const rows = clone(state.values[p.key][sel]); rows[i][j] = z; put(rows); };
      body.append(el("div", { class: "table-row layer-row" }, valueWidget(name, (z) => rowSet(0, z), names),
        stepper(mm, (z) => rowSet(1, z), { step: numStep(mm) }),
        el("button", { type: "button", class: "table-x", disabled: x.length < 2, "aria-label": "Remove layer", "data-tip": "Remove this layer",
          onclick: () => { const rows = clone(state.values[p.key][sel]); rows.splice(i, 1); put(rows); } }, "×")));
    });
    body.append(el("button", { type: "button", class: "table-btn", "data-tip": "Add a layer on top",
      onclick: () => { const rows = clone(state.values[p.key][sel]); rows.push(clone(rows[rows.length - 1])); put(rows); } }, "+ Layer"));
  } else {
    body.append(el("div", { class: "table-row" }, valueWidget(x, put, shape === "name" ? namesOf(NAMES_FROM[p.key]) : null)));
  }
  return el("div", { class: "table-edit" }, head, body);
}

function field(p) {
  const { text, unit } = labelOf(p.name);
  const changed = !same(state.values[p.key], p.default);
  const head = el("div", { class: "field-head" }, el("span", { class: "field-label" }, text, unit ? el("span", { class: "unit" }, ` (${unit})`) : null));
  attachHelp(head, p.key);
  if (state.ui === "advanced") {
    head.append(el("span", { class: "mono-name field-note" }, p.module === p.key.split(".")[0] ? p.name : p.key));
    if (changed) head.append(el("button", { type: "button", class: "reset-one", "data-tip": `Back to the file's value: ${showValue(p.default)}`,
      onclick: () => { state.noneEditing.delete(p.key); setValues({ [p.key]: clone(p.default) }, "field"); } }, "↺"));
  }
  return el("div", { class: "field" + (changed ? " changed" : ""), "data-key": p.key }, head, widget(p));
}

/* ---- Colorization: one dropdown per kind of part -----------------------------------------------------
   color.py keeps every look in one MATERIALS table and the stack-up's colour names in three more.  Here they are
   sorted by what they colour (board, copper, finish, solder mask, silkscreen), and only what this run would use is
   offered: the mode (visual has exposed copper and mask over copper; simulation has core / prepreg and plating),
   the dielectric grouping, the finish switch and the stack-up colour switch.  Each group is one dropdown; its
   entries are the parts' materials and, with stack-up colours on, the colour names the board's stack-up can use. */
function colorGroups(keys) {
  const V = state.values, mats = V["Color.MATERIALS"] || {}, visual = V[CFG.mode] === "visual";
  const stackup = !!V["Color.USE_STACKUP_COLORS"], has = (k) => k in mats;
  const mat = (k, label = k) => (has(k) ? { param: "Color.MATERIALS", key: k, label } : null);
  const names = (param, suffix = "") => Object.keys(V[param] || {}).map((k) => ({ param, key: k, label: `Stack-up ${k.replace(/\b\w/g, (c) => c.toUpperCase())}${suffix}` }));
  const layered = !visual && V["Run.DIELECTRIC_GROUPING"] === "layer" && has("Board_core");
  const finishOn = !!V["Finish.FINISH_ENABLED"];
  const metals = Object.keys(V["Finish.FINISH_CONDUCTIVITY_S_PER_M"] || {});
  const groups = [
    { title: "Board Colors", tip: "The laminate", items: layered ? [mat("Board_core", "Core"), mat("Board_prepreg", "Prepreg")] : [mat("Board", "Laminate")] },
    { title: "Copper Colors", tip: "Traces, pads, zones and the plating of holes",
      items: visual ? [mat("Copper_exposed", "Copper")] : [mat("Copper", "Copper"), mat("Plating", "Hole plating")] },
    finishOn && { title: "Finish Colors", tip: "The finish metals on the exposed copper (Finish Enabled is on)",
      items: metals.length ? metals.map((m) => mat(m)) : ["Nickel", "Gold", "Palladium", "Tin", "Silver", "OSP"].map((m) => mat(m)) },
    { title: "Solder Mask Colors", tip: "The solder mask; with Use Stackup Colors on, the colour names the board's stack-up can use",
      items: [mat("Top Solder Mask"), mat("Bottom Solder Mask"),
        ...(visual ? [mat("Top Mask over Copper"), mat("Bottom Mask over Copper")] : []),
        ...(stackup ? names("Color.STACKUP_MASK_COLORS") : []),
        ...(stackup && visual ? names("Color.STACKUP_MASK_OVER_COPPER_COLORS", " over copper") : [])],
      extra: [visual && "Color.VISUAL_MASK_OPAQUE", visual && stackup && "Color.USER_MASK_OVER_COPPER_LIGHTEN"] },
    { title: "Silkscreen Colors", tip: "The silkscreen; with Use Stackup Colors on, the colour names the board's stack-up can use",
      items: [mat("Top Silkscreen"), mat("Bottom Silkscreen"), ...(stackup ? names("Color.STACKUP_SILK_COLORS") : [])] },
  ].filter(Boolean);
  const out = [];
  if (keys.includes("Color.USE_STACKUP_COLORS")) out.push(field(state.byKey["Color.USE_STACKUP_COLORS"]));
  for (const g of groups) {
    const items = g.items.filter(Boolean);
    if (!items.length) continue;
    out.push(colorGroup(g, items));
    for (const k of g.extra || []) if (k && keys.includes(k)) out.push(field(state.byKey[k]));
  }
  return out;
}
function colorGroup(g, items) {
  const id = "color:" + g.title;
  state.tableSel = state.tableSel || {};
  const labelOfItem = (it) => it.label;
  const sel = items.find((it) => labelOfItem(it) === state.tableSel[id]) || items[0];
  const valueOf = (it) => (state.values[it.param] || {})[it.key];
  const defaultOf = (it) => (state.byKey[it.param].default || {})[it.key];
  const changed = items.filter((it) => !same(valueOf(it), defaultOf(it)));
  const put = (val) => setValues({ [sel.param]: { ...state.values[sel.param], [sel.key]: val } }, "field");

  const head = el("div", { class: "field-head" }, el("span", { class: "field-label", "data-tip": g.tip }, g.title));
  if (changed.length) head.append(el("button", { type: "button", class: "reset-one", "data-tip": "Back to the file's colours for this group",
    onclick: () => {
      const next = {};
      for (const it of changed) (next[it.param] = next[it.param] || { ...state.values[it.param] })[it.key] = clone(defaultOf(it));
      setValues(next, "field");
    } }, "↺"));
  const pick = dropdown(items.map(labelOfItem), sel.label, (label) => { state.tableSel[id] = label; renderSections(); });
  const x = valueOf(sel), body = el("div", { class: "table-body" });
  if (x && typeof x === "object") {
    for (const [k, y] of Object.entries(x))
      body.append(el("div", { class: "table-row" }, el("span", { class: "table-label" }, choiceText(k)),
        valueWidget(y, (z) => put({ ...state.values[sel.param][sel.key], [k]: z }))));
  } else body.append(el("div", { class: "table-row" }, valueWidget(x, put)));
  return el("div", { class: "field" + (changed.length ? " changed" : ""), "data-group": g.title }, head,
    el("div", { class: "table-edit" }, el("div", { class: "table-head" }, pick), body));
}

/* ---- sections: one per parameter file ---------------------------------------------------------- */
const OUTSIDE = () => new Set([CFG.mode, CFG.formats, CFG.verify]);
function sectionKeys(module) {
  const outside = OUTSIDE();
  if (state.ui === "basic") return (CFG.basic[module] || []).filter((k) => k in state.byKey && !outside.has(k));
  return state.params.filter((p) => p.module === module && !outside.has(p.key)).map((p) => p.key);
}
function presetRow() {
  const presets = state.desc.presets || {};
  const names = Object.keys(presets);
  if (!names.length) return null;
  const seg = el("div", { class: "segmented wide" });
  for (const n of names) {
    const match = Object.entries(presets[n]).every(([k, x]) => same(state.values[k], x));
    const tip = `Preset ${n} (Run.PRESETS): ` + Object.entries(presets[n]).map(([k, x]) => `${k.split(".")[1]} = ${showValue(x)}`).join(", ");
    seg.append(el("button", { type: "button", class: match ? "on" : "", "data-tip": tip,
      onclick: () => { setValues(presets[n], "preset"); toast(`Preset ${(CFG.presetTitles || {})[n] || n}`); } }, (CFG.presetTitles || {})[n] || n));
  }
  return el("div", { class: "field" }, el("div", { class: "field-head" }, el("span", { class: "field-label" }, "Preset")), seg);
}
function renderSections() {
  const box = $("sections"), scroller = $("controls-scroll"), top = scroller.scrollTop;
  box.replaceChildren();
  for (const f of state.desc.files) {
    const keys = sectionKeys(f.module);
    const isRun = f.module === CFG.mode.split(".")[0];
    if (!keys.length && !isRun) continue;
    const det = el("details", { class: "psec", "data-module": f.module });
    det.open = state.open.has(f.module);
    det.addEventListener("toggle", () => { if (det.open) state.open.add(f.module); else state.open.delete(f.module); });
    const nChanged = keys.filter((k) => !same(state.values[k], state.byKey[k].default)).length;
    det.append(el("summary", { "data-tip": f.doc || "" }, el("span", { class: "ps-name" }, (CFG.sectionTitles || {})[f.module] || f.module),
      el("span", { class: "ps-file" }, f.file.replace(/^parameters\//, "")),
      el("span", { class: "ps-n" + (nChanged ? " changed" : "") }, nChanged ? `${nChanged} changed` : String(keys.length))));
    const inner = el("div", { class: "psec-body" });
    if (isRun) { const pr = presetRow(); if (pr) inner.append(pr); }
    if (f.module === "Color" && "Color.MATERIALS" in state.byKey) inner.append(...colorGroups(keys));
    else for (const k of keys) inner.append(field(state.byKey[k]));
    det.append(inner);
    box.append(det);
  }
  const hiddenFiles = state.desc.files.filter((f) => !sectionKeys(f.module).length && f.module !== CFG.mode.split(".")[0]).map((f) => (CFG.sectionTitles || {})[f.module] || f.module);
  $("sections-note").textContent = state.ui === "basic"
    ? `Advanced shows all ${state.params.length} parameters${hiddenFiles.length ? `, ${hiddenFiles.join(" and ")} included` : ""}.`
    : "Mode, the file formats and Verify are the switches outside the sections. A dot marks a value that differs from the file.";
  scroller.scrollTop = top;
}
function setUI(ui) {
  if (ui === state.ui) return;
  state.ui = ui;
  document.querySelectorAll("#ui-switch button").forEach((b) => b.classList.toggle("on", b.dataset.ui === ui));
  $("app").classList.toggle("advanced", ui === "advanced");
  renderSections();
}

/* ---- mode and formats ------------------------------------------------------------------------- */
const visualOnly = () => new Set(state.desc.visualFormats);
function renderMode() {
  const box = $("mode-switch"), mode = state.values[CFG.mode];
  box.replaceChildren();
  for (const m of state.desc.modes) {
    box.append(el("button", { type: "button", role: "tab", class: m === mode ? "on" : "", "data-help": CFG.mode, onclick: () => pickMode(m) }, choiceText(m)));
  }
}
function pickMode(m) {
  const now = state.values[CFG.mode];
  if (m === now) return;
  state.formatsByMode[now] = clone(state.values[CFG.formats]);
  let formats = state.formatsByMode[m] || clone(state.values[CFG.formats]);
  if (m === "visual") {                                          // KESE writes only these formats in visual mode
    formats = formats.filter((f) => visualOnly().has(f));
    if (!formats.length) formats = [state.desc.visualFormats[0]];
  }
  setValues({ [CFG.mode]: m, [CFG.formats]: formats }, "mode");
}
function renderFormats() {
  const box = $("formats"), mode = state.values[CFG.mode], on = new Set(state.values[CFG.formats] || []);
  box.replaceChildren();
  for (const f of state.desc.formats) {
    const allowed = mode !== "visual" || visualOnly().has(f);
    const cb = el("input", { type: "checkbox", disabled: !allowed }); cb.checked = on.has(f) && allowed;
    cb.addEventListener("change", () => {
      const now = new Set(state.values[CFG.formats] || []);
      if (cb.checked) now.add(f); else now.delete(f);
      if (!now.size) { cb.checked = true; toast("At least one format"); return; }
      setValues({ [CFG.formats]: state.desc.formats.filter((x) => now.has(x)) }, "formats");
    });
    box.append(el("label", { class: "format" + (cb.checked ? " on" : "") + (allowed ? "" : " dis"),
      "data-tip": allowed ? `Write ${f.toUpperCase()} (${CFG.formats})` : `${f.toUpperCase()} is written in Simulation mode only` },
      el("span", { class: "switch" }, cb, el("span", { class: "knob" })), f.toUpperCase()));
  }
  const order = (CFG.previewOrder[mode] || []).map((x) => x.toUpperCase()).join(", then ");
  $("formats-note").textContent = `The formats ticked are written. The preview shows ${order}.`;
}

/* ---- board ------------------------------------------------------------------------------------- */
function boardMeta(text) {
  const m = (re) => { const x = re.exec(text); return x ? x[1] : null; };
  const out = [];
  const ver = m(/\(version\s+(\d+)/);
  if (ver) out.push(`file version ${ver}`);
  const cu = new Set([...text.matchAll(/\(\s*\d+\s+"?([^"\s)]*\.Cu)"?\s+(?:signal|power|mixed|jumper)/g)].map((x) => x[1]));
  if (cu.size) out.push(`${cu.size} copper layers`);
  const th = m(/\(general[\s\S]{0,200}?\(thickness\s+([\d.]+)/);
  if (th) out.push(`${th} mm`);
  const fp = (text.match(/\(footprint\s+"/g) || []).length;
  if (fp) out.push(`${fp} footprints`);
  const vias = (text.match(/\(via\s/g) || []).length;
  if (vias) out.push(`${vias} vias`);
  const zones = (text.match(/\(zone\s/g) || []).length;
  if (zones) out.push(`${zones} zones`);
  return out.join(" · ");
}
async function setBoard(name, bytes) {
  if (!/\.kicad_pcb$/i.test(name)) { toast("That is not a .kicad_pcb file", 4000); return; }
  const text = new TextDecoder().decode(bytes);
  if (!/^\s*\(kicad_pcb/.test(text)) { toast(`${name} does not look like a KiCad board`, 5000); return; }
  state.board = { name, bytes, meta: boardMeta(text) };
  $("board-name").textContent = name;
  $("board-meta").textContent = `${bytesText(bytes.byteLength)} · ${state.board.meta}`;
  $("drop").classList.add("has-board");
  if (state.result) state.stale = true;
  updateGenerate();
  updateStale();
  if (state.ready && !state.busy) generate();
}
function updateGenerate() {
  const b = $("btn-generate");
  if (!state.ready) return;
  b.disabled = state.busy || !state.board;
  if (!state.busy) b.textContent = "Generate";
  b.dataset.tip = state.board ? "Make the model with these settings (Ctrl+Enter)" : "Choose a board first";
}

/* ---- generate ------------------------------------------------------------------------------------ */
async function generate() {
  if (!state.ready || state.busy || !state.board) return;
  setBusy(true);
  const btn = $("btn-generate");
  btn.disabled = true; btn.textContent = "Generating…";
  runStart();
  updateStale();
  const sent = clone(state.values);
  try {
    const r = await ask("generate", { board: { name: state.board.name, bytes: state.board.bytes }, values: sent, tabId: store.tabId });
    state.result = r;
    state.runValues = sent;
    state.stale = false;
    if (r.ok) {
      store.setRun(r);
      state.materials = store.has("materials.json") ? JSON.parse(await store.text("materials.json")) : null;
      runStop();
      $("run-note").replaceChildren("Done in ", el("b", {}, seconds(r.seconds)), ".");
    } else { runStop(); $("run-note").textContent = "Not generated: see Checks."; }
    renderChecks();
    renderDownloads();
    renderPreviewTabs();
    if (r.ok) await showPreview();
  } catch (e) {
    runStop();
    state.result = { ok: false, checks: [{ level: "error", stage: "python", msg: String(e.message || e) }] };
    renderChecks();
  } finally {
    setBusy(false);
    updateGenerate();
    $("btn-report").disabled = !state.result;
    updateStale();
  }
}

/* ---- preview ----------------------------------------------------------------------------------- */
// the previewable files of the run, in webui.json's order for the run's mode
function previewChoices() {
  const r = state.result;
  if (!r || !r.ok) return [];
  const mode = state.runValues[CFG.mode], out = [];
  for (const fmtName of CFG.previewOrder[mode] || []) {
    if (fmtName === "stl") {
      const stls = r.files.filter((f) => /^stl\/.*\.stl$/i.test(f.path));
      if (stls.length) out.push({ key: "stl", format: "stl", label: `stl/ (${stls.length} files)`, files: stls });
    } else {
      for (const f of r.files) if (f.path.toLowerCase().endsWith("." + fmtName) && !f.path.includes("/")) out.push({ key: f.path, format: fmtName, label: f.path, files: [f] });
    }
  }
  return out;
}
// the Showing menu (top centre of the preview): the run's previewable files
function renderPreviewTabs() {
  const sel = $("showing"), choices = previewChoices();
  sel.replaceChildren(...choices.map((c) => el("option", { value: c.key }, c.label)));
  sel.disabled = false;
  sel.parentElement.hidden = choices.length < 2;          // one file: nothing to choose, no menu
  state.preview.key = choices.length ? choices[0].key : null;
}
async function showPreview() {
  const c = previewChoices().find((x) => x.key === state.preview.key);
  $("empty-note").hidden = !!c;
  if (!c) { viewer.clear(); renderParts(); return; }
  const ro = $("readout");
  ro.textContent = `Reading ${c.label}…`;
  const size = c.files.reduce((s, f) => s + f.size, 0);
  try {
    let parts;
    if (c.format === "glb") parts = await viewer.loadGLB(await store.bytes(c.key));
    else if (c.format === "obj") {
      const mtl = c.key.replace(/\.obj$/i, ".mtl");
      parts = viewer.loadOBJ(await store.text(c.key), store.has(mtl) ? await store.text(mtl) : null);
    } else if (c.format === "stl") {
      const looks = {};
      for (const [name, p] of Object.entries((state.materials || {}).parts || {})) {
        const fn = p.file_names && p.file_names.stl;
        if (fn) looks[stem(fn)] = { color: p.look && p.look.color, alpha: p.look && p.look.alpha, role: p.role, part: name };
      }
      const files = [];
      for (const f of c.files) files.push({ name: stem(f.path.split("/").pop()), buffer: await store.bytes(f.path) });
      parts = viewer.loadSTL(files, looks);
    } else if (c.format === "step") parts = await viewer.loadSTEP(await store.bytes(c.key));
    const tris = parts.reduce((s, p) => s + p.triangles, 0);
    const units = state.runValues[CFG.units], perMm = units === "m" ? 0.001 : 1;
    const dims = viewer.boardSize(perMm);
    ro.textContent = `${c.label} · ${bytesText(size)} · ${parts.length} parts · ${countText(tris)} triangles` +
      (dims ? ` · ${dims[0].toFixed(1)} × ${dims[1].toFixed(1)} × ${dims[2].toFixed(2)} mm` : "");
  } catch (e) {
    viewer.clear();
    ro.textContent = `${c.label} could not be shown: ${e.message}`;
  }
  renderParts();
}

// what materials.json says about a part (role, layer, net, height, and the solver properties)
function partInfo(name) {
  const parts = (state.materials || {}).parts || {};
  if (parts[name]) return parts[name];
  for (const [n, p] of Object.entries(parts)) if (p.file_names && stem(p.file_names.stl || "") === name) return { ...p, name: n };
  return null;
}
function showHover(part) {
  const card = $("hover-card");
  if (!part) { card.hidden = true; return; }
  const info = partInfo(part.name);
  card.replaceChildren(el("b", {}, part.name), ` · ${countText(part.triangles)} triangles`);
  card.style.borderLeftColor = part.color;
  if (info) {
    const bits = [info.role, info.layer, info.net && `net ${info.net}`].filter(Boolean);
    if (bits.length) card.append(el("br"), bits.join(" · "));
    const z = info.z_range_mm;
    if (z && z[0] != null) card.append(el("br"), `z ${fmt(Number(z[0].toFixed(4)))} … ${fmt(Number(z[1].toFixed(4)))} mm`);
    const props = Object.entries(info.properties || {}).filter(([, v]) => typeof v === "number" || typeof v === "string").slice(0, 4);
    if (props.length) card.append(el("br"), props.map(([k, v]) => `${k} ${typeof v === "number" ? fmt(Number(v.toPrecision(4))) : v}`).join(" · "));
  }
  card.hidden = false;
}

/* ---- checks ------------------------------------------------------------------------------------ */
function renderChecks() {
  const r = state.result, list = $("checks-list"), counts = $("counts");
  list.replaceChildren(); counts.replaceChildren();
  if (!r) return;
  const items = r.checks || [];
  const n = (l) => items.filter((i) => i.level === l).length;
  const ne = n("error"), nw = n("warning"), ni = n("info");
  if (r.ok) counts.append(el("span", { class: nw ? "w" : "ok" }, nw ? `${nw} Warning${nw > 1 ? "s" : ""}` : "No Warnings"), ` · ${ni} Info`);
  else counts.append(el("span", { class: "e" }, "Not Generated"), ne ? ` · ${ne} Error${ne > 1 ? "s" : ""}` : "");
  const order = { error: 0, warning: 1, info: 2 };
  const shown = items.filter((i) => state.showInfo || i.level !== "info").sort((a, b) => order[a.level] - order[b.level]);
  for (const i of shown) list.append(checkRow(i.level, i.stage, i.msg));
  if (!r.ok && r.trace) list.append(checkRow("info", "trace", r.trace));
  if (!shown.length) list.append(el("p", { class: "hint" }, r.ok ? "Nothing to report. Turn on Info to see KESE's notes." : ""));
}

/* ---- parts ------------------------------------------------------------------------------------- */
function renderParts() {
  const box = $("parts");
  box.replaceChildren();
  const parts = viewer ? viewer.parts : [];
  if (!parts.length) { box.append(el("p", { class: "hint" }, "The solids of the model, once it is made. Click one to hide it.")); return; }
  const sorted = [...parts].sort((a, b) => b.triangles - a.triangles);
  for (const p of sorted) {
    const row = el("button", { type: "button", class: "part" + (p.visible ? "" : " off"), "data-tip": "Click to hide or show this part",
      onclick: () => { viewer.setVisible(p.name, !p.visible); row.classList.toggle("off", !p.visible); } },
      el("i", { style: `background:${p.color}` }), el("span", { class: "part-name" }, p.name), el("small", {}, `${countText(p.triangles)} tris`));
    box.append(row);
  }
}

/* ---- downloads --------------------------------------------------------------------------------- */
function zipName(suffix = "") { return `${stem(state.board.name)}_${state.result.name}${suffix}.zip`; }
function renderDownloads() {
  const box = $("download-files"), r = state.result;
  box.replaceChildren();
  if (!r || !r.ok) return;
  const top = r.files.filter((f) => !f.path.includes("/"));
  const folders = [...new Set(r.files.filter((f) => f.path.includes("/")).map((f) => f.path.split("/")[0]))];
  for (const f of top) {
    box.append(el("button", { type: "button", class: "glass-btn small", "data-tip": `Download ${f.path} (${bytesText(f.size)})`,
      onclick: async () => download(await store.file(f.path), f.path) }, f.path));
  }
  for (const d of folders) {
    const inside = r.files.filter((f) => f.path.startsWith(d + "/"));
    box.append(el("button", { type: "button", class: "glass-btn small", "data-tip": `Download the ${d}/ folder as a zip (${inside.length} files)`,
      onclick: async () => { toast(`Zipping ${d}/…`); download(await store.zip(`${stem(state.board.name)}_${d}`, (p) => p.startsWith(d + "/")), zipName(`_${d}`)); } }, `${d}/`));
  }
  $("btn-download").dataset.tip = `Download this run as one zip: ${zipName()}`;
}

/* ---- dialogs ------------------------------------------------------------------------------------ */
function confirmBox(text) {
  const d = $("confirm-dialog");
  $("confirm-text").textContent = text;
  d.returnValue = "";
  d.showModal();
  return new Promise((resolve) => d.addEventListener("close", () => resolve(d.returnValue === "yes"), { once: true }));
}

/* ---- import / export ----------------------------------------------------------------------------- */
async function exportFiles() {
  if (!state.ready) return;
  try {
    const r = await ask("exportZip", { values: state.values });
    download(new Blob([r.zipBytes], { type: "application/zip" }), "KESE_parameters.zip");
  } catch (e) { toast("Export failed: " + e.message, 5000); }
}
async function importFiles(files) {
  const found = {}, ignored = [];
  for (const f of files) {
    const r = await ask("readValues", { text: await f.text(), fileName: f.name });
    Object.assign(found, r.values);
    for (const n of r.ignored) if (!ignored.includes(n)) ignored.push(n);
  }
  const n = Object.keys(found).length;
  if (!n) { toast(ignored.length ? `No settings of this version found (ignored: ${ignored.join(", ")})` : "No parameter values found in that file", 6000); return; }
  state.noneEditing.clear();
  setValues(found, "import");
  toast(`Loaded ${n} value${n > 1 ? "s" : ""}` + (ignored.length ? `. Ignored (not settings of this version): ${ignored.join(", ")}` : ""), ignored.length ? 7000 : 2600);
}

/* ---- start -------------------------------------------------------------------------------------- */
function wire() {
  const links = CFG.links || {};
  $("btn-help").href = links.help || links.repository || "#";
  $("nav-home").href = links.blogHome || "#";
  $("nav-back").addEventListener("click", (e) => { e.preventDefault(); if (history.length > 1) history.back(); else location.href = links.blogHome; });
  document.querySelectorAll("#ui-switch button").forEach((b) => b.addEventListener("click", () => setUI(b.dataset.ui)));
  $("btn-generate").addEventListener("click", generate);
  $("verify").addEventListener("change", () => setValues({ [CFG.verify]: $("verify").checked }, "verify"));
  $("verify-row").dataset.help = CFG.verify;
  $("btn-reset").addEventListener("click", async () => {
    if (!(await confirmBox("Are you sure to reset every setting?"))) return;
    state.noneEditing.clear();
    setValues(clone(state.start), "reset"); toast("Back to the values in the parameter files");
  });
  $("btn-export").addEventListener("click", exportFiles);
  $("btn-import").addEventListener("click", () => $("import-file").click());
  $("import-file").addEventListener("change", (e) => { importFiles([...e.target.files]); e.target.value = ""; });
  // the board: click to choose, or drop it on the card or anywhere on the page
  $("board-file").addEventListener("change", async (e) => { const f = e.target.files[0]; if (f) setBoard(f.name, await f.arrayBuffer()); e.target.value = ""; });
  addEventListener("dragover", (e) => { e.preventDefault(); $("drop").classList.add("over"); });
  addEventListener("dragleave", (e) => { if (!e.relatedTarget) $("drop").classList.remove("over"); });
  addEventListener("drop", async (e) => {
    e.preventDefault(); $("drop").classList.remove("over");
    const f = [...e.dataTransfer.files].find((x) => /\.kicad_pcb$/i.test(x.name)) || e.dataTransfer.files[0];
    if (f) setBoard(f.name, await f.arrayBuffer());
  });
  $("show-info").addEventListener("change", (e) => { state.showInfo = e.target.checked; renderChecks(); });
  $("btn-report").addEventListener("click", async () => {
    const r = state.result; if (!r) return;
    $("report-text").textContent = r.ok && store.has("report.txt") ? await store.text("report.txt") : (r.log || "") + "\n" + (r.trace || "");
    $("report-dialog").showModal();
  });
  $("report-dialog").addEventListener("click", (e) => {
    const d = e.currentTarget, b = d.getBoundingClientRect();
    if (e.target === d && (e.clientX < b.left || e.clientX > b.right || e.clientY < b.top || e.clientY > b.bottom)) d.close();
  });
  $("btn-download").addEventListener("click", async () => {
    if (!state.result || !state.result.ok || state.stale) return;
    toast("Zipping…");
    download(await store.zip(`${stem(state.board.name)}_${state.result.name}`), zipName());
  });
  $("showing").addEventListener("change", (e) => { state.preview.key = e.target.value; showPreview(); });
  // preview tools
  $("btn-fit").addEventListener("click", () => viewer.fit());
  $("btn-shot").addEventListener("click", async () => download(await viewer.screenshot(), `${state.board ? stem(state.board.name) : "KESE"}_preview.png`));
  $("btn-fullscreen").addEventListener("click", () => {
    const w = $("canvas-wrap");
    if (document.fullscreenElement) document.exitFullscreen(); else (w.requestFullscreen || w.webkitRequestFullscreen).call(w);
  });
  document.addEventListener("fullscreenchange", () => {
    const on = !!document.fullscreenElement, b = $("btn-fullscreen");
    b.querySelector("path").setAttribute("d", on ? "M8 3v5H3M16 3v5h5M21 16h-5v5M3 16h5v5" : "M3 8V3h5M16 3h5v5M21 16v5h-5M8 21H3v-5");
    b.dataset.tip = on ? "Leave full screen (Esc)" : "Show the preview full screen (Esc to leave)";
  });
  document.querySelectorAll("#views button").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll("#views button").forEach((x) => x.classList.toggle("on", x === b));
    viewer.view(b.dataset.view);
  }));
  $("cut").addEventListener("input", (e) => { const v = +e.target.value; viewer.setCut(v / 100); $("cut-out").textContent = v >= 100 ? "Off" : `${v} %`; });
  document.addEventListener("keydown", (e) => { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") generate(); });
}

async function examples() {
  const list = (state.version && state.version.examples) || [];
  if (!list.length) return;
  const box = $("examples");
  for (const name of list) {
    box.append(el("button", { type: "button", class: "glass-btn small", "data-tip": `Load ${name}, one of the boards in Generator/Input`,
      onclick: async () => {
        try {
          const r = await fetch(new URL(`examples/${name}`, import.meta.url));
          if (!r.ok) throw new Error(`HTTP ${r.status}`);
          setBoard(name, await r.arrayBuffer());
        } catch (e) { toast(`${name} could not be loaded: ${e.message}`, 5000); }
      } }, stem(name)));
  }
  box.hidden = false;
}

async function main() {
  const links = CFG.links || {};
  $("foot").replaceChildren("Generator: ", el("a", { href: links.repository, target: "_blank", rel: "noopener" }, "KiCad EM Stackup Exporter"),
    " · GPL-3.0-or-later · runs in your browser, nothing is uploaded");
  viewer = new Viewer($("view"), { roleOf: (name) => (partInfo(name) || {}).role, onHover: showHover, onProgress: (f) => { $("readout").textContent = `Reading the STEP… ${Math.round(f * 100)} %`; } });
  wire();
  store.start();
  startWorker();
  setBusy(true);
  let init;
  try {
    init = await ask("init", { pyodideBase: PYODIDE, packages: CFG.pyodidePackages, config: CFG });
  } catch (e) {
    fatal(`Python could not be loaded: ${e.message}. Check the internet connection and reload the page.`);
    return;
  }
  state.desc = init.description;
  state.version = init.version;
  state.params = state.desc.parameters;
  for (const p of state.params) { state.byKey[p.key] = p; state.start[p.key] = clone(p.default); }
  state.values = clone(state.start);
  $("foot").firstElementChild.after(` ${state.desc.version}`);
  state.ready = true;
  setBusy(false);
  updateGenerate();
  refresh();
  renderPreviewTabs();
  examples();
  $("checks-list").replaceChildren(el("p", { class: "hint" }, `Python is ready (${init.seconds.toFixed(1)} s). Choose a board: it is read here and never uploaded.`));
  // ?board=<example name> loads one of the examples (local testing, links from the blog)
  const b = QUERY.get("board");
  if (b && (state.version.examples || []).includes(b)) {
    const r = await fetch(new URL(`examples/${b}`, import.meta.url));
    if (r.ok) setBoard(b, await r.arrayBuffer());
  }
}

if (!window.KESE_PHONE) main();
