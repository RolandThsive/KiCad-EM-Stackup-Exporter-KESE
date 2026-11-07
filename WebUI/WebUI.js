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

/* Where Python (Pyodide) comes from: jsDelivr first; if it gives no answer within webui.json "cdnWaitSeconds"
   (15 s) or fails while Python loads, the copy on this site (vendor/pyodide/, checked against vendor.json when the site
   was built).  ?pyodide=<url> replaces jsDelivr for local testing, and is taken only from this site, so a link
   cannot make the page run Python from someone else's server.  three.js has the same backup; boot.js chooses it. */
function pyodideOverride() {
  const q = QUERY.get("pyodide");
  if (!q) return null;
  try { const u = new URL(q, location.href); if (u.origin === location.origin) return u.href; } catch (e) { /* not a URL */ }
  console.warn(`?pyodide=${q} ignored: only a folder of this site may be named`);
  return null;
}
// When boot.js already had to take three.js from the backup (jsDelivr silent, refused or a changed file), Python
// skips jsDelivr too if it is the same server: no second 15 s wait.
const sameCdnDown = window.KESE_THREE === "backup" && new URL(CFG.pyodide).host === new URL(CFG.three).host;
const PYTHON_SOURCES = [
  pyodideOverride() ? { name: "the ?pyodide= folder", base: pyodideOverride() } : sameCdnDown ? null : { name: "jsDelivr", base: CFG.pyodide },
  { name: "this site's backup copy", base: new URL("vendor/pyodide/", import.meta.url).href },
].filter(Boolean);
const CDN_WAIT_MS = (CFG.cdnWaitSeconds || 15) * 1000;

/* ---- state --------------------------------------------------------------------------------------- */
const state = {
  desc: null, params: [], byKey: {}, values: {}, start: {},
  ui: "basic", open: new Set(CFG.basicOpen || []), lastNumbers: {}, noneEditing: new Set(),
  formatsByMode: {},                      // the formats last ticked in each mode
  preset: null,                           // the preset last clicked, lit while its values hold
  board: null,                            // {name, bytes, meta}
  result: null, runValues: null, stale: false, showInfo: false, busy: false, ready: false,
  preview: { key: null }, materials: null, version: null,
};
const store = new OutputStore();
let viewer = null;
const $ = (id) => document.getElementById(id);

/* ---- worker ---------------------------------------------------------------------------------------- */
let worker, nextId = 1, onStage = () => {};
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
    if (m.type === "stage") { onStage(m.stage); return; }
    const p = pending.get(m.id); if (!p) return;
    pending.delete(m.id);
    if (m.ok) p.resolve(m.result); else p.reject(Object.assign(new Error(m.error), { phase: m.phase }));
  };
  worker.onerror = (e) => {
    const msg = "The Python worker stopped: " + (e.message || e);
    for (const p of pending.values()) p.reject(new Error(msg));   // a run waiting on it ends, instead of spinning for ever
    pending.clear();
    fatal(msg);
  };
}

function stopWorker() {
  worker.onmessage = worker.onerror = null;
  worker.terminate();
  pending.clear();
}
// init on each source in turn: the next one when this one stays silent CDN_WAIT_MS before Pyodide's first file has
// arrived, or fails while the runtime and packages load ("runtime" errors).  Errors after that are not the CDN's.
async function startPython() {
  for (let i = 0; i < PYTHON_SOURCES.length; i++) {
    const src = PYTHON_SOURCES[i], last = i === PYTHON_SOURCES.length - 1;
    startWorker();
    try {
      const init = await new Promise((resolve, reject) => {
        const timer = last ? 0 : setTimeout(() => reject(Object.assign(new Error(`no answer from ${src.name} in ${CDN_WAIT_MS / 1000} s`), { phase: "runtime" })), CDN_WAIT_MS);
        onStage = (stage) => { if (stage === "runtime-js") clearTimeout(timer); };
        ask("init", { pyodideBase: src.base, packages: CFG.pyodidePackages, config: CFG })
          .then((r) => { clearTimeout(timer); resolve(r); }, (e) => { clearTimeout(timer); reject(e); });
      });
      state.python = src.name;
      return init;
    } catch (e) {
      if (last || e.phase !== "runtime") throw e;
      console.warn(`Python from ${src.name} failed (${e.message}): trying ${PYTHON_SOURCES[i + 1].name}`);
      stopWorker();
      setProgressText(`Loading Python from ${PYTHON_SOURCES[i + 1].name}…`);
    }
  }
}

/* ---- small helpers ------------------------------------------------------------------------------- */
function el(tag, attrs = {}, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k === "style") e.style.cssText = v;               // through the CSSOM: the page's CSP allows no style attributes
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else if (v === true) e.setAttribute(k, "");
    else if (v !== false && v != null) e.setAttribute(k, v);
  }
  for (const k of kids.flat()) if (k != null) e.append(k.nodeType ? k : document.createTextNode(k));
  return e;
}
// a long NAME_LIKE_THIS may wrap after its underscores and dots, never inside a word
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const clone = (x) => JSON.parse(JSON.stringify(x));
function fmt(x) { return typeof x === "number" ? String(Number(x.toPrecision(10))) : String(x); }
function bytesText(n) { return n >= 1048576 ? `${(n / 1048576).toFixed(1)} MB` : n >= 1024 ? `${Math.round(n / 1024)} KB` : `${n} B`; }
function countText(n) { return n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${Math.round(n / 1e3)}k` : String(n); }
let toastTimer;
function toast(text, ms = 2600) {
  const t = $("toast"); t.textContent = text; t.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => (t.hidden = true), ms);
  const sr = $("sr-status"); sr.textContent = "";                 // emptied first, so the same message twice is read twice
  setTimeout(() => (sr.textContent = text), 50);
}
function setProgressText(text) {
  if (!state.ready) $("btn-generate").textContent = text.replace("…", "") + "…";
  state.checksNote = text;
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
  state.checksFatal = text;
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
// The tips' words are in tips.json: a title, one plain line, then the choices, facts, a note and a picture where they
// help.  A button names its tip with data-tip-id (data-tip-args fills its {values}); a setting's tip is found by its
// key, with its title, unit, file value and wiki link taken from the parameter.  data-tip keeps one plain line, shown
// while tips.json loads, if it fails, or for a tip it does not have; a setting it does not have shows its comment.
let TIPS = {};
fetch(new URL("tips.json", import.meta.url), { cache: "no-cache" }).then((r) => (r.ok ? r.json() : {})).then((j) => { TIPS = j || {}; }).catch(() => {});
const tipAttrs = (id, text, args) => ({ "data-tip": text, "data-tip-id": id, "data-tip-args": args ? JSON.stringify(args) : null });
function setTip(node, id, text, args) {
  node.dataset.tip = text; node.dataset.tipId = id;
  if (args) node.dataset.tipArgs = JSON.stringify(args); else delete node.dataset.tipArgs;
}
const SUPERSCRIPT = { "-": "⁻", 0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴", 5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹" };
function sciText(x) {                                             // 41000000 -> "4.1 × 10⁷"
  if (!x || typeof x !== "number") return String(x);
  const e = Math.floor(Math.log10(Math.abs(x)));
  return `${+(x / 10 ** e).toPrecision(3)} × 10${String(e).replace(/./g, (c) => SUPERSCRIPT[c])}`;
}
// a setting's choices, [value, what it does], with the file's value marked
function markFile(options, v) {
  const words = (x) => String(x).toLowerCase().replace(/_/g, " ");
  const is = (chip) => (v === null || v === undefined ? chip === "None"
    : typeof v === "boolean" ? chip === (v ? "On" : "Off")
    : typeof v === "number" ? chip.trim() !== "" && Number(chip) === v
    : typeof v === "string" && words(chip) === words(v));
  const marks = options.map(([chip]) => is(chip));
  if (!marks.some(Boolean)) {      // "a number", "ENIG … HardGold", "GND" (any net name): the file's value is one of those
    const i = options.findIndex(([chip]) => (chip === "a number" && typeof v === "number") || (chip.includes("…") && typeof v === "string")
      || (chip === "GND" && typeof v === "string" && v !== "auto"));
    if (i >= 0) marks[i] = true;
  }
  return options.map(([chip, text], i) => [chip, text, marks[i]]);
}
const reference = (file) => {                                     // the parameter file's section of the Parameter Reference
  const r = TIPS.reference || {}, a = (r.anchors || {})[String(file).replace(/^parameters\//, "")];
  return r.page ? (a ? `${r.page}#${a}` : r.page) : null;
};
const wikiLink = (page, text) => el("a", { href: `${(CFG.links || {}).help}/${page}`, target: "_blank", rel: "noopener" }, `${text} ↗`);
const tipTable = (rows) => el("table", { class: "tp-table" }, el("tbody", {}, rows.map(([a, b]) => el("tr", {}, el("td", {}, a), el("td", {}, b)))));
function settingTip(p) {
  const s = (TIPS.settings || {})[p.key];
  if (!s) return null;
  const { text, unit } = labelOf(p.name), group = (TIPS.groups || {})[p.key];
  const c = { ...s, eyebrow: ((CFG.sectionTitles || {})[p.module] || p.module) + (group ? ` · ${group}` : ""), title: text, unit,
    badge: DESKTOP_ONLY().has(p.key) ? "Desktop only" : null, key: `${p.file} · ${p.name}`, o: s.o && markFile(s.o, p.default), wiki: reference(p.file) };
  if (s.table && p.default && typeof p.default === "object") c.footRows = Object.entries(p.default).map(([k, v]) => [k, `${sciText(v)} ${unit}`.trim()]);
  else c.foot = showValue(p.default);
  return c;
}
function sectionTip(mod) {
  const s = (TIPS.sections || {})[mod], f = state.desc && state.desc.files.find((x) => x.module === mod);
  if (!s || !f) return null;
  const n = state.params.filter((p) => p.module === mod).length, basic = ((CFG.basic || {})[mod] || []).length;
  return { ...s, eyebrow: "Section", title: (CFG.sectionTitles || {})[mod] || mod, key: `parameters/${f.file.replace(/^parameters\//, "")}`,
    f: [["Settings", String(n)], ["Basic shows", basic ? String(basic) : "none: Advanced only"]], wiki: reference(f.file) };
}
function presetTip(name) {
  const pr = ((state.desc || {}).presets || {})[name], words = (TIPS.presets || {})[name];
  if (!pr || !words) return null;
  const L = TIPS.presetLabels || {}, V = TIPS.presetValues || {};
  const value = (k, x) => (Array.isArray(x) ? x.map((y) => String(y).toUpperCase()).join(", ")
    : (V[k] || {})[String(x)] ?? (typeof x === "boolean" ? (x ? "on" : "off") : String(x)));
  return { eyebrow: "Preset", title: (CFG.presetTitles || {})[name] || name, t: words,
    rows: Object.entries(pr).map(([key, x]) => { const k = key.split(".").pop(); return [L[k] || k, value(k, x)]; }),
    n: "Only these change. Every other setting keeps its value.", wiki: reference("presets.py") };
}
function pageTip(id) {
  if (id.startsWith("section.")) return sectionTip(id.slice(8));
  if (id.startsWith("preset.")) return presetTip(id.slice(7));
  return (TIPS.page || {})[id] || null;
}
// one tip, in tips.json's shape, as the popover's children; {name} in its words is filled from args
function tipCard(c, args) {
  const fill = (x) => String(x).replace(/\{(\w+)\}/g, (_, k) => (args[k] ?? ""));
  const out = [];
  if (c.eyebrow) out.push(el("span", { class: "tp-eyebrow" }, c.eyebrow));
  if (c.title) out.push(el("span", { class: "tp-head" }, el("span", { class: "tp-title" }, fill(c.title)),
    c.unit ? el("span", { class: "tp-unit" }, c.unit) : null, c.badge ? el("span", { class: "tp-badge" }, c.badge) : null));
  if (c.key) out.push(el("span", { class: "mono-name tp-key" }, c.key));
  if (c.t) out.push(el("p", { class: "tp-lead" }, fill(c.t)));
  if (c.o) out.push(el("div", { class: "tp-opts" }, c.o.flatMap(([v, text, file]) => [
    el("span", { class: "tp-chip" + (file ? " file" : ""), title: file ? "The value in the parameter file" : null }, v), el("span", {}, text)])));
  const facts = (c.f || []).map(([k, v]) => [k, fill(v)]).filter(([, v]) => v.trim() !== "");
  if (facts.length) out.push(el("dl", { class: "tp-facts" }, facts.flatMap(([k, v]) => [el("dt", {}, k), el("dd", {}, v)])));
  if (c.rows) out.push(tipTable(c.rows));
  if (c.n) out.push(el("p", { class: "tp-note" }, fill(c.n)));
  if (c.kbd) out.push(el("span", { class: "tp-keys" }, c.kbd.flatMap((k, i) => [i ? "+" : null, el("kbd", {}, k)]), c.kbdText ? ` ${c.kbdText}` : null));
  const pic = c.img && (TIPS.pictures || {})[c.img];
  if (pic) out.push(el("figure", { class: "tp-fig" },      // width and height keep its place while it loads
    el("img", { src: new URL(`tooltips/${pic.file}`, import.meta.url).href, width: pic.w, height: pic.h, alt: pic.caption, decoding: "async" }),
    el("figcaption", {}, `${pic.caption} · `, wikiLink(pic.page, "Wiki"))));
  if (c.foot !== undefined || c.footRows || c.wiki) {
    const left = c.footRows ? el("span", {}, "In the file", tipTable(c.footRows))
      : c.foot !== undefined ? el("span", {}, "In the file: ", el("code", {}, c.foot)) : el("span");
    out.push(el("span", { class: "tp-foot" }, left, c.wiki ? wikiLink(c.wiki, "Parameter Reference") : null));
  }
  return out;
}
const isTable = (v) => !!v && typeof v === "object" && !Array.isArray(v);   // a table has no one-line value: its tip leaves the line out
function showValue(v) {
  if (v === null || v === undefined) return "None";
  if (typeof v === "boolean") return v ? "True" : "False";
  if (Array.isArray(v)) return `[${v.map(showValue).join(", ")}]`;
  if (typeof v === "object") return JSON.stringify(v);
  return fmt(v);
}
let tipTimer = null, tipFor = null, hideTimer = null;
function hideTip() { clearTimeout(tipTimer); clearTimeout(hideTimer); tipFor = null; $("popover").hidden = true; }
function showTip(node) {
  const pop = $("popover");
  pop.replaceChildren();
  pop.classList.remove("rich", "wide");
  const p = node.dataset.help && state.byKey[node.dataset.help];  // the parameters are known once Python has read them
  const c = p ? settingTip(p) : node.dataset.tipId ? pageTip(node.dataset.tipId) : null;
  if (c) {
    let args = {};
    try { args = JSON.parse(node.dataset.tipArgs || "{}"); } catch (e) { /* no values */ }
    pop.classList.add("rich");
    if (c.img || c.o || c.rows || c.footRows) pop.classList.add("wide");
    pop.append(...tipCard(c, args));
  } else if (p) {
    pop.append(el("span", { class: "mono-name" }, `${p.file} · ${p.name}`));
    pop.append(p.help || "No notes in the parameter file.");
    pop.append(el("span", { class: "tip-foot" }, `In the file: ${showValue(p.default)}`));
  } else if (node.dataset.tip) pop.append(node.dataset.tip);
  else { hideTip(); return; }
  pop.hidden = false;
  const r = node.getBoundingClientRect(), W = document.documentElement.clientWidth, H = document.documentElement.clientHeight;   // the window less its scrollbars
  const h = pop.offsetHeight, w = pop.offsetWidth, below = r.bottom + 8, above = r.top - h - 8;
  if (below + h <= H - 6 || above >= 6) {                         // under the target, else above it
    pop.style.top = (below + h <= H - 6 ? below : above) + "px";
    pop.style.left = Math.max(6, Math.min(W - w - 6, r.left)) + "px";
  } else {                                                        // too tall for either: beside it, never over it
    pop.style.top = Math.max(6, Math.min(H - h - 6, r.top + r.height / 2 - h / 2)) + "px";
    pop.style.left = (r.right + 8 + w <= W - 6 ? r.right + 8 : Math.max(6, r.left - w - 8)) + "px";
  }
}
const tipOf = (node) => (node && !(node.dataset.tip !== undefined && !node.dataset.tip) ? node : null);
// WCAG 1.4.13: the pointer may move onto a tip to read it (a short grace on the way), Escape closes it, and the
// keyboard gets the same tips as the mouse: the focused control's, or that of the field whose label names it
document.addEventListener("mouseover", (e) => {
  if (e.target.closest("#popover")) { clearTimeout(hideTimer); return; }
  const node = tipOf(e.target.closest("[data-tip], [data-help]"));
  if (node && node === tipFor) { clearTimeout(hideTimer); return; }
  if (!node && !$("popover").hidden) { clearTimeout(hideTimer); hideTimer = setTimeout(hideTip, 300); return; }
  hideTip();
  if (!node) return;
  tipFor = node;
  tipTimer = setTimeout(() => showTip(node), e.target.closest(".info-dot") ? 0 : 450);
});
document.addEventListener("focusin", (e) => {
  if (!(e.target instanceof Element) || !e.target.matches(":focus-visible") || e.target.closest("#popover")) return;
  const label = document.getElementById((e.target.getAttribute("aria-labelledby") || "").split(" ")[0]);
  const node = tipOf(e.target.closest("[data-tip], [data-help]") || label?.closest("[data-tip], [data-help]"));
  hideTip();
  if (!node) return;
  tipFor = node;
  tipTimer = setTimeout(() => showTip(node), 450);
});
document.addEventListener("focusout", () => { if (tipFor && !tipFor.matches(":hover")) hideTip(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && tipFor) hideTip(); });
document.addEventListener("mousedown", (e) => { if (!e.target.closest("#popover")) hideTip(); });
document.addEventListener("scroll", (e) => { if (!(e.target instanceof Element && e.target.closest("#popover"))) hideTip(); }, true);

/* ---- labels: made from the parameter's name ---------------------------------------------------- */
const UNITS = { MM: "mm", MM2: "mm²", MM3: "mm³", UM: "µm", DEG: "deg", HZ: "Hz", S_PER_M: "S/m", PCT: "%", S: "s" };
function labelOf(name) {
  let rest = name, unit = "";
  for (const [suffix, u] of Object.entries(UNITS)) {
    if (rest.endsWith("_" + suffix)) { rest = rest.slice(0, -suffix.length - 1); unit = u; break; }
  }
  const words = rest.split("_").map((w) => (w.length <= 3 && !/^(ON|OF|TO|IN|AND|OR|PER|THE|FOR|MAX|MIN|USE|ARC|AUTO|PAD|VIA|PTH|NET|A|AT|AIR|BIG|CUT|END|FEW|FIT|NO|NON|PEN|SET|WEB|DIR)$/.test(w) ? w : w[0] + w.slice(1).toLowerCase()));
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
  // stale while the settings differ from the run's: changing a value back makes the result current again
  if (state.result) state.stale = !same(state.values, state.runValues) || state.board !== state.runBoard;
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
  setTip($("btn-download"), state.stale ? "downloadStale" : "downloadZip", state.stale ? "The settings changed: press Generate first"
    : ok ? `Download this run as one zip: ${zipName()}` : "Download this run as one zip", ok && !state.stale ? { file: zipName() } : null);
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
function stepper(value, onCommit, { step = 0.001, integer = false, disabled = false, placeholder = "", limit = null } = {}) {
  const input = el("input", { type: "text", inputmode: "decimal", value: value == null ? "" : fmt(value), disabled, placeholder });
  const len = (value == null ? "" : fmt(value)).length;
  if (len > 6) input.style.width = `${len + 2}ch`;
  const commit = (x) => {
    if (!Number.isFinite(x)) { input.value = value == null ? "" : fmt(value); return; }
    if (integer) x = Math.round(x);
    if (limit && (x < limit.min || (limit.above && x <= limit.min))) {     // below what KESE takes (kese/job.py)
      toast(`${limit.above ? "More than" : "At least"} ${limit.min}${limit.integer ? ", a whole number" : ""}`);
      x = limit.above ? (value ?? step) : limit.min;
      if (limit.above && x <= limit.min) { input.value = value == null ? "" : fmt(value); return; }
    }
    x = Number(x.toPrecision(10));
    input.value = fmt(x);                                   // shown as stored, also when the value did not change ("0.0350")
    onCommit(x);
  };
  // what was typed: a decimal comma reads as a point ("1,5"); a number with anything else in it ("12abc") is refused
  const typed = () => { const t = input.value.trim().replace(",", "."); return t === "" ? NaN : Number(t); };
  input.addEventListener("change", () => {
    const x = typed();
    if (!Number.isFinite(x) && input.value.trim() !== "") toast(`"${input.value.trim()}" is not a number`);
    commit(x);
  });
  input.addEventListener("keydown", (e) => {
    if (e.key === "ArrowUp" || e.key === "ArrowDown") { e.preventDefault(); commit((Number.isFinite(typed()) ? typed() : value ?? 0) + (e.key === "ArrowUp" ? step : -step)); }
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
  const menu = el("div", { class: "dropdown-content", role: "listbox" });
  const btn = el("button", { type: "button", class: "dropdown-btn" }, el("span", {}, choiceText(value)), el("span", { class: "arrow" }, "▾"));
  for (const o of options) menu.append(el("a", { class: same(o, value) ? "on" : "", role: "option", tabindex: "0",
    onclick: () => { dd.classList.remove("open"); btn.focus(); onPick(o); } }, choiceText(o)));   // the focus goes back to the button (kept through the re-render)
  const items = () => [...menu.children];
  let fromKey = false;
  btn.addEventListener("keydown", (e) => { fromKey = e.key === "Enter" || e.key === " "; });
  btn.addEventListener("pointerdown", () => { fromKey = false; });
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    document.querySelectorAll(".dropdown.open").forEach((d) => d !== dd && d.classList.remove("open"));
    if (dd.classList.toggle("open")) {
      placeMenu(dd, menu);
      if (fromKey) (menu.querySelector(".on") || menu.firstChild)?.focus();   // opened from the keyboard: into the list
    }
  });
  // keys: Enter / Space pick, the arrows, Home and End move, Escape and Tab close (Escape gives the focus back to the button)
  dd.addEventListener("keydown", (e) => {
    const list = items(), at = list.indexOf(document.activeElement);
    if (e.key === "Escape" && dd.classList.contains("open")) { e.preventDefault(); e.stopPropagation(); dd.classList.remove("open"); btn.focus(); }
    else if ((e.key === "Enter" || e.key === " ") && at >= 0) { e.preventDefault(); list[at].click(); }
    else if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      if (!dd.classList.contains("open")) { fromKey = true; btn.click(); return; }   // opens on the picked option
      const next = at < 0 ? 0 : Math.max(0, Math.min(list.length - 1, at + (e.key === "ArrowDown" ? 1 : -1)));
      list[next].focus();
    } else if ((e.key === "Home" || e.key === "End") && at >= 0) { e.preventDefault(); list[e.key === "Home" ? 0 : list.length - 1].focus(); }
    else if (e.key === "Tab" && dd.classList.contains("open")) dd.classList.remove("open");
  });
  dd.append(btn, menu);
  return dd;
}
// a menu opens below its button, or above it when the room below (in its scrolling panel and the window) is too
// short and there is more above; a menu taller than both scrolls
function placeMenu(dd, menu) {
  let box = dd.parentElement;
  while (box && box !== document.body && !/auto|scroll|hidden/.test(getComputedStyle(box).overflowY)) box = box.parentElement;
  const c = box && box !== document.body ? box.getBoundingClientRect() : { top: 0, bottom: innerHeight };
  const r = dd.getBoundingClientRect(), gap = 12;
  const below = Math.min(c.bottom, document.documentElement.clientHeight) - r.bottom - gap, above = r.top - Math.max(c.top, 0) - gap;
  menu.style.maxHeight = "";
  const up = menu.scrollHeight > below && above > below;
  dd.classList.toggle("up", up);
  menu.style.maxHeight = menu.scrollHeight > (up ? above : below) ? `${Math.max(up ? above : below, 120)}px` : "";
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
      const dd = dropdown(p.choices, v, set);
      return PICKS_FINISH.has(key) ? finishPick(p, v, dd) : dd;
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
    case "int": case "num": {
      const lim = (state.desc.limits || {})[key];
      return stepper(v, set, { step: stepOf(p), integer: p.kind === "int" || !!(lim && lim.integer), limit: lim });
    }
    case "num_or_none": {
      const isNone = v === null && !state.noneEditing.has(key);
      const row = el("div", { class: "auto-row" });
      row.append(switchRow(isNone, "None", (on) => {
        if (on) { if (typeof state.values[key] === "number") state.lastNumbers[key] = state.values[key]; state.noneEditing.delete(key); set(null); renderSections(); }
        else if (typeof state.lastNumbers[key] === "number") set(state.lastNumbers[key]);
        else { state.noneEditing.add(key); renderSections(); const i = document.querySelector(`[data-key="${key}"] .stepper input`); if (i) i.focus(); }
      }, tipAttrs("none", "None: KESE takes the value from the board file or works it out (see the help)")));
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
const NAMES_FROM = CFG.namesFrom || {}, LAYER_NAMES_FROM = CFG.layerNamesFrom || {};   // see webui.json
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
// (metal, mm) layers, bottom to top: a metal dropdown and a thickness each, a layer added on top or removed
function layerRows(rows, putRows, names) {
  const out = [el("div", { class: "table-row table-cols" }, el("span", {}, "Layer, bottom to top"), el("span", {}, "mm"))];
  rows.forEach(([name, mm], i) => {
    const rowSet = (j, z) => { const r = clone(rows); r[i][j] = z; putRows(r); };
    out.push(el("div", { class: "table-row layer-row" }, valueWidget(name, (z) => rowSet(0, z), names),
      stepper(mm, (z) => rowSet(1, z), { step: numStep(mm) }),
      el("button", { type: "button", class: "table-x", disabled: rows.length < 2, "aria-label": "Remove layer", "data-tip": "Remove this layer",
        onclick: () => { const r = clone(rows); r.splice(i, 1); putRows(r); } }, "×")));
  });
  out.push(el("button", { type: "button", class: "table-btn", ...tipAttrs("addLayer", "Add a layer on top"),
    onclick: () => { const r = clone(rows); r.push(clone(r[r.length - 1])); putRows(r); } }, "+ Layer"));
  return out;
}
/* Finish Type picks a key of Finish.FINISH_TYPES (or "file"); under the pick, that finish's layers are edited in
   place, so FINISH_TYPES needs no field of its own. */
const PICKS_FINISH = new Set(["Finish.FINISH_TYPE"]);
const FOLDED = new Set(["Finish.FINISH_TYPES"]);                   // edited inside another field, not on its own
function finishPick(p, v, pickWidget) {
  const types = state.values["Finish.FINISH_TYPES"] || {}, rows = types[v];
  const box = el("div", { class: "table-edit" }, pickWidget);
  if (Array.isArray(rows) && rows.length) {
    const put = (r) => setValues({ "Finish.FINISH_TYPES": { ...state.values["Finish.FINISH_TYPES"], [v]: r } }, "field");
    box.append(el("p", { class: "hint table-note" }, `Layers of ${v}, bottom to top, in mm. Each becomes its own part.`),
      el("div", { class: "table-body" }, ...layerRows(rows, put, Object.keys(state.values["Finish.FINISH_CONDUCTIVITY_S_PER_M"] || {}))));
  } else if (v === "file") {
    box.append(el("p", { class: "hint table-note" }, "The board's stack-up names the finish (Board Setup > Physical Stackup > Copper finish). The run stops with an error if the board names none or one KESE does not know; a stack-up finish of \"None\" gives no finish."));
  }
  return box;
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
      body.append(el("div", { class: "table-row" }, k === "color" ? null : el("span", { class: "table-label" }, choiceText(k)),
        valueWidget(y, (z) => put({ ...state.values[p.key][sel], [k]: z }))));
  } else if (shape === "layers") {
    body.append(...layerRows(x, put, namesOf(LAYER_NAMES_FROM[p.key])));
  } else {
    body.append(el("div", { class: "table-row" }, valueWidget(x, put, shape === "name" ? namesOf(NAMES_FROM[p.key]) : null)));
  }
  return el("div", { class: "table-edit" }, head, body);
}

// the inputs of a table (a record's rows, a finish's layers): "Finish Type, layer 2, mm", "Copper, alpha"
function labelCells(box, title) {
  let layer = 0;
  for (const row of box.querySelectorAll(".table-row:not(.table-cols)")) {
    const what = row.classList.contains("layer-row") ? `layer ${++layer}, mm` : (row.querySelector(".table-label") || {}).textContent || "";
    for (const i of row.querySelectorAll("input:not([aria-label]):not([aria-labelledby])"))
      i.setAttribute("aria-label", [title, what, i.type === "color" ? "colour" : ""].filter(Boolean).join(", "));
  }
}
function field(p) {
  const { text, unit } = labelOf(p.name);
  // a finish pick also counts as changed when the layers of the finish it shows were edited
  const T = "Finish.FINISH_TYPES", pickedType = state.values[p.key];
  const layersChanged = PICKS_FINISH.has(p.key) && T in state.byKey
    && !same((state.values[T] || {})[pickedType], (state.byKey[T].default || {})[pickedType]);
  const changed = !same(state.values[p.key], p.default) || layersChanged;
  const labelId = "label-" + p.key.replace(/\W/g, "-");
  const head = el("div", { class: "field-head" }, el("span", { class: "field-label", id: labelId }, text, unit ? el("span", { class: "unit" }, ` (${unit})`) : null));
  attachHelp(head, p.key);
  if (state.ui === "advanced") {
    if (changed) head.append(el("button", { type: "button", class: "reset-one", ...tipAttrs("resetOne", `Back to the file's value: ${showValue(p.default)}`, { value: isTable(p.default) ? "" : showValue(p.default) }),
      onclick: () => {
        state.noneEditing.delete(p.key);
        const back = { [p.key]: clone(p.default) };
        if (layersChanged) back[T] = { ...state.values[T], [pickedType]: clone(state.byKey[T].default[pickedType]) };
        setValues(back, "field");
      } }, "↺"));
  }
  // Advanced: the parameter's name sits beside its control, so the title keeps the whole width for one line
  const control = state.ui === "advanced"
    ? el("div", { class: "field-body" }, widget(p), el("span", { class: "mono-name field-name", title: p.key }, p.module === p.key.split(".")[0] ? p.name : p.key))
    : widget(p);
  // screen readers name each input by the field's title, a table's cells by the title and their row
  labelCells(control, text);
  for (const i of control.querySelectorAll("input:not([aria-label]):not([aria-labelledby]), select, textarea")) i.setAttribute("aria-labelledby", labelId);
  if (DESKTOP_ONLY().has(p.key)) {          // threads and worker processes: greyed, the value kept as in the file
    control.setAttribute("inert", "");
    return el("div", { class: "field desktop-only", "data-key": p.key }, head, control,
      el("p", { class: "desktop-note" }, "Desktop only for now: support in the browser is in the works."));
  }
  return el("div", { class: "field" + (changed ? " changed" : ""), "data-key": p.key }, head, control);
}
const DESKTOP_ONLY = () => new Set(CFG.desktopOnly || []);

/* ---- Colorization: one dropdown per kind of part -----------------------------------------------------
   color.py keeps every look in one MATERIALS table and the stack-up's colour names in three more.  Here they are
   sorted by what they colour (board, copper, finish, solder mask, silkscreen), and only what this run would use is
   offered: the mode (visual has exposed copper and mask over copper; simulation has core / prepreg and plating),
   the dielectric grouping, the part switches (Board / Copper / Finish / Solder Mask / Silkscreen Enabled) and the
   stack-up colour switch.  Each group is one dropdown; its
   entries are the parts' materials and, with stack-up colours on, the colour names the board's stack-up can use. */
function colorGroups(keys) {
  const V = state.values, mats = V["Color.MATERIALS"] || {}, visual = V[CFG.mode] === VISUAL;
  const stackup = !!V["Color.USE_STACKUP_COLORS"], has = (k) => k in mats;
  const mat = (k, label = k) => (has(k) ? { param: "Color.MATERIALS", key: k, label } : null);
  const layered = !visual && V["Board.DIELECTRIC_GROUPING"] === "layer" && has("Board_core");
  const on = (k) => V[k] !== false;
  // With Use Stackup Colors on, the colour of a side's mask / silk comes from the board's stack-up when it names one
  // the tables know (or a #RRGGBB "User defined" colour), as kese/s5_materials/materials.py picks it.
  const boardColors = state.board ? state.board.colors || {} : null;
  const fromBoard = (side, kind) => {
    const v = boardColors && boardColors[`${side === "Top" ? "F" : "B"}.${kind}`];
    if (!v) return null;
    if (/^#[0-9a-f]{6}([0-9a-f]{2})?$/i.test(v)) return { name: v, color: v.slice(0, 7) };
    const t = V[kind === "Mask" ? "Color.STACKUP_MASK_COLORS" : "Color.STACKUP_SILK_COLORS"] || {}, c = t[v.toLowerCase()];
    return c ? { name: v, color: c } : { name: v, color: null };
  };
  const own = (side, kind) => !stackup || (boardColors && !(fromBoard(side, kind) || {}).color);
                               // the part switches: a group shows only while its parts are built
  const metals = Object.keys(V["Finish.FINISH_CONDUCTIVITY_S_PER_M"] || {});
  const groups = [
    on("Board.BOARD_ENABLED") && { title: "Board Colors", tip: "The laminate", tipId: "colorBoard", items: layered ? [mat("Board_core", "Core"), mat("Board_prepreg", "Prepreg")] : [mat("Board", "Laminate")] },
    on("Copper.COPPER_ENABLED") && { title: "Copper Colors", tip: "Traces, pads, zones and the plating of holes", tipId: "colorCopper",
      items: visual ? [mat("Copper_exposed", "Copper")] : [mat("Copper", "Copper"), mat("Plating", "Hole plating")] },
    on("Finish.FINISH_ENABLED") && { title: "Finish Colors", tip: "The finish metals on the exposed copper (Finish Enabled is on)", tipId: "colorFinish",
      items: metals.map((m) => mat(m)) },
    // One group per side, for MATERIALS' "<side> Solder Mask" (and, in visual mode, "<side> Mask over Copper").
    // Its dropdown picks a colour by name from STACKUP_MASK_COLORS; the over-copper shade of the same name
    // (STACKUP_MASK_OVER_COPPER_COLORS) is set with it.  With Use Stackup Colors on, a side shows only when the
    // board's stack-up names no colour for it (the board's own colours are listed above instead).
    ...["Top", "Bottom"].map((side) => on("SolderMask.SOLDER_MASK_ENABLED") && has(`${side} Solder Mask`) && own(side, "Mask") && {
      title: `${side} Solder Mask Colors` + (stackup ? " (the board names none)" : ""),
      tip: `The ${side.toLowerCase()} solder mask (Color.MATERIALS "${side} Solder Mask"${visual ? `, and "${side} Mask over Copper"` : ""})`,
      tipId: "colorMask", tipArgs: { title: `${side} Solder Mask Colors` + (stackup ? " (the board names none)" : ""), side: side.toLowerCase() },
      items: [{ ...mat(`${side} Solder Mask`), pair: visual && has(`${side} Mask over Copper`) ? { param: "Color.MATERIALS", key: `${side} Mask over Copper` } : null }],
      presets: { names: V["Color.STACKUP_MASK_COLORS"] || {}, pairNames: V["Color.STACKUP_MASK_OVER_COPPER_COLORS"] || {} } }),
    on("SolderMask.SOLDER_MASK_ENABLED") && { title: "", items: [], extra: [visual && "Color.VISUAL_MASK_OPAQUE", visual && stackup && "Color.USER_MASK_OVER_COPPER_LIGHTEN"] },
    on("Silkscreen.SILKSCREEN_ENABLED") && { title: "Silkscreen Colors" + (stackup ? " (the board names none)" : ""), tip: "The silkscreen (Color.MATERIALS)",
      tipId: "colorSilk", tipArgs: { title: "Silkscreen Colors" + (stackup ? " (the board names none)" : "") },
      items: ["Top", "Bottom"].filter((side) => own(side, "SilkS")).map((side) => mat(`${side} Silkscreen`)) },
  ].filter(Boolean);
  const out = [];
  if (keys.includes("Color.USE_STACKUP_COLORS")) out.push(field(state.byKey["Color.USE_STACKUP_COLORS"]));
  if (stackup && (on("SolderMask.SOLDER_MASK_ENABLED") || on("Silkscreen.SILKSCREEN_ENABLED"))) out.push(boardColorNote(fromBoard, on));
  for (const g of groups) {
    const items = g.items.filter(Boolean);
    if (items.length) out.push(colorGroup(g, items));
    for (const k of g.extra || []) if (k && keys.includes(k)) out.push(field(state.byKey[k]));
  }
  return out;
}
/* What the board's stack-up names for each side's mask and silk, with Use Stackup Colors on. */
function boardColorNote(fromBoard, on) {
  const box = el("div", { class: "field board-colors" }, el("div", { class: "field-head" },
    el("span", { class: "field-label", ...tipAttrs("boardColors", "The colours set in KiCad (Board Setup > Physical Stackup), used because Use Stackup Colors is on") }, "Board's Stack-up Colors")));
  if (!state.board) { box.append(el("p", { class: "hint" }, "Upload a board to see the colours its stack-up names.")); return box; }
  const kinds = [on("SolderMask.SOLDER_MASK_ENABLED") && ["Mask", "Solder Mask"], on("Silkscreen.SILKSCREEN_ENABLED") && ["SilkS", "Silkscreen"]].filter(Boolean);
  const list = el("div", { class: "board-colors-list" });
  for (const [kind, label] of kinds) for (const side of ["Top", "Bottom"]) {
    const c = fromBoard(side, kind);
    list.append(el("div", { class: "board-color" },
      el("span", { class: "board-color-dot" + (c && c.color ? "" : " none"), style: c && c.color ? `background:${c.color}` : "" }),
      el("span", { class: "board-color-name" }, `${side} ${label}`),
      el("span", { class: "board-color-value" }, !c ? "none named, set below" : c.color ? c.name : `${c.name} (unknown name, set below)`)));
  }
  box.append(list);
  return box;
}
function colorGroup(g, items) {
  const id = "color:" + g.title;
  state.tableSel = state.tableSel || {};
  const labelOfItem = (it) => it.label;
  const sel = items.find((it) => labelOfItem(it) === state.tableSel[id]) || items[0];
  const valueOf = (it) => (state.values[it.param] || {})[it.key];
  const defaultOf = (it) => (state.byKey[it.param].default || {})[it.key];
  const entries = items.flatMap((it) => (it.pair ? [it, it.pair] : [it]));             // an entry and its over-copper shade
  const changed = entries.filter((it) => !same(valueOf(it), defaultOf(it)));
  const putOf = (it) => (val) => setValues({ [it.param]: { ...state.values[it.param], [it.key]: val } }, "field");

  const head = el("summary", { class: "field-head" }, el("span", { class: "field-label", ...tipAttrs(g.tipId, g.tip, g.tipArgs) }, g.title));
  if (changed.length) head.append(el("button", { type: "button", class: "reset-one", ...tipAttrs("resetColors", "Back to the file's colours for this group"),
    onclick: (e) => {
      e.preventDefault(); e.stopPropagation();                      // in the summary: reset, do not open / close
      const next = {};
      for (const it of changed) (next[it.param] = next[it.param] || { ...state.values[it.param] })[it.key] = clone(defaultOf(it));
      setValues(next, "field");
    } }, "↺"));
  let pick;
  if (g.presets) {
    // a colour picked by name: the entry's colour and its pair's colour come from the two name tables
    const { names, pairNames } = g.presets, title = (k) => k.replace(/\b\w/g, (c) => c.toUpperCase());
    const colorOf = (it) => String((valueOf(it) || {}).color || valueOf(it) || "").toLowerCase();
    const now = Object.keys(names).find((k) => String(names[k]).toLowerCase() === colorOf(sel)
      && (!sel.pair || !(k in pairNames) || String(pairNames[k]).toLowerCase() === colorOf(sel.pair)));
    const labels = Object.keys(names).map(title);
    pick = dropdown(now ? labels : ["Custom", ...labels], now ? title(now) : "Custom", (label) => {
      const k = Object.keys(names).find((n) => title(n) === label);
      if (!k) return;
      const next = { [sel.param]: { ...state.values[sel.param] } };
      next[sel.param][sel.key] = { ...next[sel.param][sel.key], color: names[k] };
      if (sel.pair && k in pairNames) {
        next[sel.pair.param] = next[sel.pair.param] || { ...state.values[sel.pair.param] };
        next[sel.pair.param][sel.pair.key] = { ...next[sel.pair.param][sel.pair.key], color: pairNames[k] };
      }
      setValues(next, "field");
    });
  } else if (items.length > 1) pick = dropdown(items.map(labelOfItem), sel.label, (label) => { state.tableSel[id] = label; renderSections(); });
  // one entry only: no dropdown, the swatch sits right under the title
  const body = el("div", { class: "table-body" });
  const rows = (it, title) => {
    const x = valueOf(it), put = putOf(it);
    if (title) body.append(el("div", { class: "table-sub" }, title));
    if (x && typeof x === "object") {
      for (const [k, y] of Object.entries(x))
        body.append(el("div", { class: "table-row" }, k === "color" ? null : el("span", { class: "table-label" }, choiceText(k)),
          valueWidget(y, (z) => put({ ...state.values[it.param][it.key], [k]: z }))));    // the swatch says what it is
    } else body.append(el("div", { class: "table-row" }, valueWidget(x, put)));
  };
  rows(sel, sel.pair ? "Mask" : null);
  if (sel.pair) rows(sel.pair, "Over copper");
  // each group folds (closed when the page starts), so Colorization opens as a short list of what can be coloured
  labelCells(body, g.title);
  const det = el("details", { class: "field cgroup" + (changed.length ? " changed" : ""), "data-group": g.title }, head,
    el("div", { class: "table-edit" }, pick ? el("div", { class: "table-head" }, pick) : null, body));
  det.open = state.open.has(id);
  det.addEventListener("toggle", () => { if (det.open) state.open.add(id); else state.open.delete(id); });
  return det;
}

/* ---- sections: one per parameter file ---------------------------------------------------------- */
const OUTSIDE = () => new Set([CFG.mode, CFG.formats, CFG.verify]);
function sectionShown(module) {           // a format's own section (STEP) only while that format is ticked
  const f = (CFG.whenFormat || {})[module];
  return !f || (state.values[CFG.formats] || []).includes(f);
}
function sectionKeys(module) {
  if (!sectionShown(module)) return [];
  const outside = OUTSIDE();
  if (state.ui === "basic") return (CFG.basic[module] || []).filter((k) => k in state.byKey && !outside.has(k));
  return state.params.filter((p) => p.module === module && !outside.has(p.key) && !FOLDED.has(p.key)).map((p) => p.key);
}
function presetRow() {
  const presets = state.desc.presets || {};
  const names = Object.keys(presets);
  if (!names.length) return null;
  const seg = el("div", { class: "segmented wide" + (names.length > 4 ? " presets-wrap" : "") });
  // the preset these values match: the one last clicked while it still does, else (Elmer is FreeCAD with no
  // finish, so both can) the one that sets the most
  const fits = names.filter((n) => Object.entries(presets[n]).every(([k, x]) => same(state.values[k], x)));
  const most = Math.max(0, ...fits.map((n) => Object.keys(presets[n]).length));
  const lit = fits.includes(state.preset) ? state.preset : fits.find((n) => Object.keys(presets[n]).length === most);
  for (const n of names) {
    const match = n === lit;
    const tip = `Preset ${n} (parameters/presets.py): ` + Object.entries(presets[n]).map(([k, x]) => `${k.split(".")[1]} = ${showValue(x)}`).join(", ");
    seg.append(el("button", { type: "button", class: match ? "on" : "", ...tipAttrs(`preset.${n}`, tip),
      onclick: () => {
        state.formatsByMode[state.values[CFG.mode]] = clone(state.values[CFG.formats]);   // as a switch of mode would
        state.preset = n;
        setValues(presets[n], "preset"); renderSections(); toast(`Preset ${(CFG.presetTitles || {})[n] || n}`); } }, (CFG.presetTitles || {})[n] || n));
  }
  return el("div", { class: "field" }, el("div", { class: "field-head" }, el("span", { class: "field-label" }, "Preset")), seg);
}
function renderSections() {
  const box = $("sections"), scroller = $("controls-scroll"), top = scroller.scrollTop;
  // every saved value rebuilds the sections: remember which control had the focus, to give it back after
  const focusBack = (() => {
    const a = document.activeElement, f = a && box.contains(a) && a.closest("[data-key], [data-group]");
    if (!f) return null;
    const sel = f.dataset.key ? `[data-key="${f.dataset.key}"]` : `[data-group="${f.dataset.group}"]`;
    const all = [...f.querySelectorAll("input, button, select, textarea")];
    return { sel, i: all.indexOf(a), caret: typeof a.selectionStart === "number" ? [a.selectionStart, a.selectionEnd] : null };
  })();
  box.replaceChildren();
  for (const f of state.desc.files) {
    const keys = sectionKeys(f.module);
    const isRun = f.module === CFG.mode.split(".")[0];
    if (!keys.length && !isRun) continue;
    const det = el("details", { class: "psec", "data-module": f.module });
    det.open = state.open.has(f.module);
    det.addEventListener("toggle", () => { if (det.open) state.open.add(f.module); else state.open.delete(f.module); });
    const nChanged = keys.filter((k) => !same(state.values[k], state.byKey[k].default)).length;
    det.append(el("summary", tipAttrs(`section.${f.module}`, f.doc || (CFG.sectionTitles || {})[f.module] || f.module), el("span", { class: "ps-name" }, (CFG.sectionTitles || {})[f.module] || f.module),
      el("span", { class: "ps-file" }, f.file.replace(/^parameters\//, "")),
      el("span", { class: "ps-n" + (nChanged ? " changed" : "") }, nChanged ? `${nChanged} changed` : String(keys.length))));
    const inner = el("div", { class: "psec-body" });
    if (isRun) { const pr = presetRow(); if (pr) inner.append(pr); }
    if (keys.some((k) => DESKTOP_ONLY().has(k)) && CFG.desktopOnlyNote) inner.append(el("p", { class: "section-note" }, CFG.desktopOnlyNote));
    if (f.module === "Color" && "Color.MATERIALS" in state.byKey) inner.append(...colorGroups(keys));
    else for (const k of keys) inner.append(field(state.byKey[k]));
    det.append(inner);
    box.append(det);
  }
  const hiddenFiles = state.desc.files.filter((f) => sectionShown(f.module) && !sectionKeys(f.module).length && f.module !== CFG.mode.split(".")[0]
    && state.params.some((p) => p.module === f.module)).map((f) => (CFG.sectionTitles || {})[f.module] || f.module);
  const listed = hiddenFiles.length > 1 ? `${hiddenFiles.slice(0, -1).join(", ")} and ${hiddenFiles.at(-1)}` : hiddenFiles.join("");
  $("sections-note").textContent = state.ui === "basic"
    ? `Advanced shows all ${state.params.length} parameters${hiddenFiles.length ? `, with the ${listed} sections` : ""}.`
    : "Mode, the file formats and Verify are the switches outside the sections. A dot marks a value that differs from the file.";
  scroller.scrollTop = top;
  if (focusBack) {
    const f = box.querySelector(focusBack.sel), t = f && [...f.querySelectorAll("input, button, select, textarea")][focusBack.i];
    if (t) {
      t.focus({ preventScroll: true });
      if (focusBack.caret && typeof t.setSelectionRange === "function") try { t.setSelectionRange(...focusBack.caret); } catch { /* not a text field */ }
    }
  }
}
function setUI(ui) {
  if (ui === state.ui) return;
  state.ui = ui;
  document.querySelectorAll("#ui-switch button").forEach((b) => b.classList.toggle("on", b.dataset.ui === ui));
  $("app").classList.toggle("advanced", ui === "advanced");
  renderSections();
}

/* ---- mode and formats ------------------------------------------------------------------------- */
const VISUAL = "visual";                // kese/job.py MODES: the mode that writes a skin, in VISUAL_FORMATS only
const writable = (mode, f) => mode !== VISUAL || state.desc.visualFormats.includes(f);
// the formats `mode` can write out of `formats`, in KESE's order; never none: else the first one it can write
function formatsFor(mode, formats) {
  const ok = state.desc.formats.filter((f) => formats.includes(f) && writable(mode, f));
  return ok.length ? ok : [state.desc.formats.find((f) => writable(mode, f))];
}
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
  setValues({ [CFG.mode]: m, [CFG.formats]: formatsFor(m, state.formatsByMode[m] || state.values[CFG.formats]) }, "mode");
}
function renderFormats() {
  const box = $("formats"), mode = state.values[CFG.mode], on = new Set(state.values[CFG.formats] || []);
  box.replaceChildren();
  for (const f of state.desc.formats) {
    const allowed = writable(mode, f);
    const cb = el("input", { type: "checkbox", disabled: !allowed }); cb.checked = on.has(f) && allowed;
    cb.addEventListener("change", () => {
      const now = new Set(state.values[CFG.formats] || []);
      if (cb.checked) now.add(f); else now.delete(f);
      if (!now.size) { cb.checked = true; toast("At least one format"); return; }
      setValues({ [CFG.formats]: state.desc.formats.filter((x) => now.has(x)) }, "formats");
    });
    box.append(el("label", { class: "format" + (cb.checked ? " on" : "") + (allowed ? "" : " dis"),
      ...(allowed ? tipAttrs(`format.${f}`, `Write ${f.toUpperCase()} (${CFG.formats})`)
        : tipAttrs("format.simOnly", `${f.toUpperCase()} is written in Simulation mode only`, { F: f.toUpperCase() })) },
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
/* The colours the board's stack-up names (Board Setup > Physical Stackup): {"F.Mask": "Green", "B.SilkS": "White", ...},
   read as kese/s2_collect/stackup.py reads them (the (color ...) of each (layer ...) in (setup (stackup ...))). */
function stackupColors(text) {
  const at = text.search(/\(stackup[\s)]/);
  if (at < 0) return {};
  let depth = 0, end = at;
  for (; end < text.length; end++) {
    const c = text[end];
    if (c === '"') { end = text.indexOf('"', end + 1); if (end < 0) break; }
    else if (c === "(") depth++;
    else if (c === ")" && --depth === 0) break;
  }
  const block = text.slice(at, end + 1), out = {};
  for (const m of block.matchAll(/\(layer\s+"([^"]+)"([^()]*(?:\((?:[^()"]|"[^"]*")*\)[^()]*)*)\)/g)) {
    const col = /\(color\s+"([^"]*)"/.exec(m[2]);
    if (col) out[m[1]] = col[1];
  }
  return out;
}
// Bigger files are refused before they are read: the browser's Python has a few GB at most, and a parameter file is a
// few KB (a bigger one is a mistake, or a zip bomb).
const MAX_BOARD = 500 * 1048576, MAX_IMPORT = 20 * 1048576;
const tooBig = (name, size) => toast(`${name} is ${bytesText(size)}: boards up to ${bytesText(MAX_BOARD)} fit in the browser. Use the desktop KESE for this one.`, 7000);
// a file the visitor chose or dropped: its size is checked before it is read into memory
async function chooseBoard(f) {
  if (f.size > MAX_BOARD && /\.kicad_pcb$/i.test(f.name)) { tooBig(f.name, f.size); return; }
  setBoard(f.name, await f.arrayBuffer());
}
async function setBoard(name, bytes) {
  if (!/\.kicad_pcb$/i.test(name)) { toast("That is not a .kicad_pcb file", 4000); return; }
  if (bytes.byteLength > MAX_BOARD) { tooBig(name, bytes.byteLength); return; }
  const text = new TextDecoder().decode(bytes);
  if (!/^\s*\(kicad_pcb/.test(text)) { toast(`${name} does not look like a KiCad board`, 5000); return; }
  state.board = { name, bytes, meta: boardMeta(text), colors: stackupColors(text) };
  if (state.desc) renderSections();                                 // Colorization shows the board's own colours (once Python is up)
  // a file name too long for one line breaks after a _ - or . (never in the middle of a word)
  $("board-name").replaceChildren(...name.split(/(?<=[_.-])/).flatMap((part, i) => (i ? [document.createElement("wbr"), part] : [part])));
  // each item whole, a line breaking only after its " ·"
  const items = [bytesText(bytes.byteLength), ...state.board.meta.split(" · ")];
  $("board-meta").replaceChildren(...items.flatMap((t, i) => [i ? " " : "", el("span", { class: "meta-item" }, i < items.length - 1 ? `${t} ·` : t)]));
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
  setTip(b, state.board ? "generate" : "generateNoBoard", state.board ? "Make the model with these settings (Ctrl+Enter)" : "Choose a board first");
}

/* ---- generate ------------------------------------------------------------------------------------ */
async function generate() {
  if (!state.ready || state.busy || !state.board) return;
  setBusy(true);
  const btn = $("btn-generate");
  btn.disabled = true; btn.textContent = "Generating…";
  runStart();
  updateStale();
  const sent = clone(state.values), sentBoard = state.board;
  try {
    const r = await ask("generate", { board: { name: state.board.name, bytes: state.board.bytes }, values: sent, tabId: store.tabId });
    state.result = r;
    state.runValues = sent;
    state.runBoard = sentBoard;
    state.stale = !same(state.values, sent) || state.board !== sentBoard;                   // a setting changed while it ran: the result is already old
    if (r.ok) {
      store.setRun(r);
      state.materials = store.has("materials.json") ? JSON.parse(await store.text("materials.json")) : null;
      runStop();
      $("run-note").replaceChildren("Done in ", el("b", {}, seconds(r.seconds)), ".");
    } else { runStop(); $("run-note").textContent = "Not generated: see Checks."; }
    renderChecks();
    renderDownloads();
    renderPreviewTabs();
    await showPreview();                                       // a failed run clears the old model, so nothing stale is shown
  } catch (e) {
    runStop();
    state.result = { ok: false, checks: [{ level: "error", stage: "python", msg: String(e.message || e) }] };
    $("run-note").textContent = "Not generated: see Checks.";
    renderChecks();
    renderDownloads();
    renderPreviewTabs();
    await showPreview();
  } finally {
    setBusy(false);
    updateGenerate();
    $("btn-report").disabled = !state.result;
    updateStale();
  }
  if (state.board !== sentBoard && state.ready) generate();     // another board came while it ran: make that one now
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
let previewSeq = 0;
async function showPreview() {
  const seq = ++previewSeq;                                   // a newer pick (or run) wins over a slow load still going
  const c = previewChoices().find((x) => x.key === state.preview.key);
  const ro = $("readout");
  if (!viewer) { ro.textContent = c ? `${c.label} is made: download it on the right.` : ""; renderParts(); return; }   // no WebGL: no preview
  $("empty-note").hidden = !!c;
  if (!c) { viewer.clear(); renderParts(); return; }
  ro.textContent = `Reading ${c.label}…`;
  const size = c.files.reduce((s, f) => s + f.size, 0);
  viewer.closedSolids = state.runValues[CFG.mode] !== VISUAL;     // a visual model is a skin: its cut has no faces
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
    if (seq !== previewSeq) return;
    const tris = parts.reduce((s, p) => s + p.triangles, 0);
    const units = state.runValues[CFG.units], perMm = units === "m" ? 0.001 : 1;
    const dims = viewer.boardSize(perMm);
    // a long file name gives way (…), the numbers after it always show
    ro.replaceChildren(el("span", { class: "ro-name", title: c.label }, c.label), el("span", { class: "ro-rest" },
      `\u00a0· ${bytesText(size)} · ${parts.length} parts · ${countText(tris)} triangles` +
      (dims ? ` · ${dims[0].toFixed(1)} × ${dims[1].toFixed(1)} × ${dims[2].toFixed(2)} mm` : "")));
  } catch (e) {
    if (seq !== previewSeq) return;
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
// one line per fact: the title in bold, a colon, the value ("Layer: F.Cu")
const PROP_UNITS = [[/_mm2$/i, "mm²"], [/_mm$/i, "mm"], [/_um$/i, "µm"], [/_deg$/i, "°"], [/_s_per_m$/i, "S/m"], [/_pct$/i, "%"]];
function propLine(key, value) {
  let name = key, unit = "";
  for (const [re, u] of PROP_UNITS) if (re.test(name)) { name = name.replace(re, ""); unit = u; break; }
  name = name.replace(/_/g, " ").replace(/\bz\b/, "Z").replace(/^./, (c) => c.toUpperCase());
  if (key === "side") value = { F: "Top", B: "Bottom" }[value] || value;
  const v = typeof value === "number" ? fmt(Number(value.toPrecision(4))) : String(value);
  return [name, unit ? `${v} ${unit}` : v];
}
function showHover(part) {
  const card = $("hover-card");
  if (!part) { card.hidden = true; $("readout").style.maxWidth = ""; return; }
  const info = partInfo(part.name);
  const lines = [];
  if (info) {
    // the layer, with what the part is on it: "Layer: F.Mask (Role: Mask, Side: Top)", "Layer: F.Cu (Role: Copper, Net: GND)",
    // "Layer: dielectric 1 (Role: Board, Kind: Core, Material: FR4)"
    const props = { ...(info.properties || {}) };
    const about = [];
    if (info.role) about.push(`Role: ${choiceText(info.role.replace(/_/g, " "))}`);
    for (const k of ["side", "kind", "material", "metal"])            // what the part is, beside its layer
      if (typeof props[k] === "string") { const [t, v] = propLine(k, props[k]); about.push(`${t}: ${choiceText(v)}`); delete props[k]; }
    if (info.net) about.push(`Net: ${info.net}`);
    if (info.layer) lines.push(["Layer", info.layer + (about.length ? ` (${about.join(", ")})` : "")]);
    else if (about.length) for (const a of about) lines.push(a.split(": "));
    const z = info.z_range_mm;
    if (z && z[0] != null) lines.push(["Z height", `${fmt(Number(z[0].toFixed(4)))} to ${fmt(Number(z[1].toFixed(4)))} mm`]);
    for (const [k, v] of Object.entries(props))
      if (typeof v === "number" || typeof v === "string") lines.push(propLine(k, v));
  }
  card.replaceChildren(el("div", { class: "hover-title" }, el("b", {}, part.name), ` · ${countText(part.triangles)} triangles`),
    ...lines.map(([t, v]) => el("div", { class: "hover-line" }, el("b", {}, `${t}:`), ` ${v}`)));
  card.style.borderLeftColor = part.color;
  card.hidden = false;
  // the card and the readout share the bottom edge: the readout stops short of the card instead of running under it
  const ro = $("readout"), gap = card.getBoundingClientRect().left - ro.getBoundingClientRect().left - 12;
  ro.style.maxWidth = gap > 80 ? `${gap}px` : "";
}

/* ---- checks ------------------------------------------------------------------------------------ */
function renderChecks() {
  const r = state.result, list = $("checks-list"), counts = $("counts");
  list.replaceChildren(); counts.replaceChildren();
  if (!r) {
    if (state.checksFatal) list.append(checkRow("error", "start", state.checksFatal));
    else if (state.checksNote) list.append(el("p", { class: "hint" }, state.checksNote));
    return;
  }   // before a run: keep the note
  const items = r.checks || [];
  const n = (l) => items.filter((i) => i.level === l).length;
  const ne = n("error"), nw = n("warning"), ni = n("info");
  if (r.ok) counts.append(el("span", { class: nw ? "w" : "ok" }, nw ? `${nw} Warning${nw > 1 ? "s" : ""}` : "No Warnings"), " ", el("span", {}, `· ${ni} Info`));
  else counts.append(el("span", { class: "e" }, "Not Generated"), " ", ne ? el("span", {}, `· ${ne} Error${ne > 1 ? "s" : ""}`) : "");
  const order = { error: 0, warning: 1, info: 2 };
  const shown = items.filter((i) => state.showInfo || i.level !== "info").sort((a, b) => order[a.level] - order[b.level]);
  for (const i of shown) list.append(checkRow(i.level, i.stage, i.msg));
  if (!r.ok && r.trace) list.append(checkRow("info", "trace", r.trace));
  if (!shown.length) list.append(el("p", { class: "hint" }, r.ok ? "Nothing to report. Turn on Info to see KESE's notes." : ""));
}

/* ---- parts ------------------------------------------------------------------------------------- */
function renderParts() {
  const box = $("parts");
  box.replaceChildren(); box.style.removeProperty("--parts-min");
  const parts = viewer ? viewer.parts : [];
  if (!parts.length) { box.append(el("p", { class: "hint" }, viewer ? "The solids of the model, once it is made. Click one to hide it." : "The parts list comes with the 3D preview, which needs WebGL.")); return; }
  const sorted = [...parts].sort((a, b) => b.triangles - a.triangles);
  for (const p of sorted) {
    const row = el("button", { type: "button", class: "part" + (p.visible ? "" : " off"), ...tipAttrs("part", `${p.name}: click to hide or show it`, { name: p.name, tris: countText(p.triangles) }), "aria-pressed": String(p.visible),
      onclick: () => { viewer.setVisible(p.name, !p.visible); row.classList.toggle("off", !p.visible); row.setAttribute("aria-pressed", String(p.visible)); } },
      el("i", { style: `background:${p.color}` }), el("span", { class: "part-name" }, p.name), el("small", {}, `${countText(p.triangles)} tris`));
    box.append(row);
  }
  const PARTS_MIN_ROWS = 6;                                 // a short window: this many rows show before the column scrolls
  box.style.setProperty("--parts-min", `${Math.min(sorted.length, PARTS_MIN_ROWS) * box.firstChild.offsetHeight}px`);
}

/* ---- downloads --------------------------------------------------------------------------------- */
function zipName(suffix = "") { return `${stem((state.runBoard || state.board).name)}_${state.result.name}${suffix}.zip`; }   // the board the run was made from
function renderDownloads() {
  const box = $("download-files"), r = state.result;
  box.replaceChildren();
  if (!r || !r.ok) return;
  const top = r.files.filter((f) => !f.path.includes("/"));
  const folders = [...new Set(r.files.filter((f) => f.path.includes("/")).map((f) => f.path.split("/")[0]))];
  for (const f of top) {
    box.append(el("button", { type: "button", class: "glass-btn small", ...tipAttrs("file", `Download ${f.path} (${bytesText(f.size)})`, { name: f.path, size: bytesText(f.size) }),
      onclick: async () => download(await store.file(f.path), f.path) }, f.path));
  }
  for (const d of folders) {
    const inside = r.files.filter((f) => f.path.startsWith(d + "/"));
    box.append(el("button", { type: "button", class: "glass-btn small", ...tipAttrs("folder", `Download the ${d}/ folder as a zip (${inside.length} files)`, { name: `${d}/`, n: String(inside.length) }),
      onclick: async () => { toast(`Zipping ${d}/…`); download(await store.zip(`${stem(state.board.name)}_${d}`, (p) => p.startsWith(d + "/")), zipName(`_${d}`)); } }, `${d}/`));
  }
  setTip($("btn-download"), "downloadZip", `Download this run as one zip: ${zipName()}`, { file: zipName() });
}

/* ---- dialogs ------------------------------------------------------------------------------------ */
function confirmBox(text) {
  const d = $("confirm-dialog");
  $("confirm-text").textContent = text;
  d.returnValue = "";
  d.showModal();
  d.querySelector("button[value=no]").focus();   // No has the focus (in JS: autofocus is refused in the blog's cross-origin frame)
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
  if (!state.ready) { toast("Python is still loading: import the settings in a moment", 4000); return; }
  const found = {}, ignored = [], failed = [];
  for (const f of files) {
    if (f.size > MAX_IMPORT) { failed.push(`${f.name} is ${bytesText(f.size)}, too big for a parameter file`); continue; }
    let r;
    try {
      r = /\.zip$/i.test(f.name) ? await ask("readZip", { bytes: await f.arrayBuffer() })
        : await ask("readValues", { text: await f.text(), fileName: f.name });
    } catch (e) {                                              // a Python error: its last line says what was wrong
      failed.push(`${f.name} could not be read (${String(e.message).trim().split("\n").pop()})`); continue;
    }
    Object.assign(found, r.values);
    for (const n of r.ignored) if (!ignored.includes(n)) ignored.push(n);
  }
  const n = Object.keys(found).length;
  // a long list of names: the first few, then how many more
  const names = (list) => list.length > 6 ? `${list.slice(0, 6).join(", ")} and ${list.length - 6} more` : list.join(", ");
  const also = failed.length ? `. ${failed.join(". ")}` : "";
  if (!n) { toast((ignored.length ? `No settings of this version found (ignored: ${names(ignored)})` : failed.length ? failed.join(". ") : "No parameter values found in that file") + (ignored.length ? also : ""), 6000); return; }
  state.noneEditing.clear();
  if (CFG.formats in found || CFG.mode in found) {         // formats this mode can write, at least one
    const mode = found[CFG.mode] ?? state.values[CFG.mode];
    found[CFG.formats] = formatsFor(mode, found[CFG.formats] ?? state.values[CFG.formats] ?? []);
  }
  setValues(found, "import");
  toast(`Loaded ${n} value${n > 1 ? "s" : ""}` + (ignored.length ? `. Ignored (not settings of this version): ${names(ignored)}` : "") + also, ignored.length || failed.length ? 7000 : 2600);
}

/* ---- start -------------------------------------------------------------------------------------- */
function wire() {
  const links = CFG.links || {};
  $("btn-help").href = links.help || links.repository || "#";
  $("drop").dataset.tipArgs = JSON.stringify({ max: `${MAX_BOARD / 1048576} MB` });
  $("nav-home").href = links.blogHome || "#";
  $("nav-back").addEventListener("click", (e) => {
    e.preventDefault();
    if (history.length > 1) history.back();                    // in the blog's frame this is the blog's own history
    else window.open(links.blogHome || "/", "_top");            // the whole tab, not just the frame
  });
  document.querySelectorAll("#ui-switch button").forEach((b) => b.addEventListener("click", () => setUI(b.dataset.ui)));
  $("btn-generate").addEventListener("click", generate);
  $("verify").addEventListener("change", () => setValues({ [CFG.verify]: $("verify").checked }, "verify"));
  $("verify-row").dataset.help = CFG.verify;
  $("btn-reset").addEventListener("click", async () => {
    if (!(await confirmBox("Are you sure to reset every setting?"))) return;
    state.noneEditing.clear();
    state.formatsByMode = {};                                  // the formats remembered per mode go back too
    state.preset = null;
    setValues(clone(state.start), "reset"); toast("Back to the values in the parameter files");
  });
  $("btn-export").addEventListener("click", exportFiles);
  $("btn-import").addEventListener("click", () => $("import-file").click());
  $("import-file").addEventListener("change", (e) => { importFiles([...e.target.files]); e.target.value = ""; });
  // the board: click to choose, or drop it on the card or anywhere on the page
  $("board-file").addEventListener("change", (e) => { const f = e.target.files[0]; if (f) chooseBoard(f); e.target.value = ""; });
  addEventListener("dragover", (e) => { e.preventDefault(); $("drop").classList.add("over"); });
  addEventListener("dragleave", (e) => { if (!e.relatedTarget) $("drop").classList.remove("over"); });
  addEventListener("drop", async (e) => {
    e.preventDefault(); $("drop").classList.remove("over");
    const f = [...e.dataTransfer.files].find((x) => /\.kicad_pcb$/i.test(x.name)) || e.dataTransfer.files[0];
    if (f) chooseBoard(f);
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
  $("btn-fit").addEventListener("click", () => viewer && viewer.fit());
  $("btn-shot").addEventListener("click", async () => viewer && download(await viewer.screenshot(), `${state.board ? stem(state.board.name) : "KESE"}_preview.png`));
  $("btn-fullscreen").addEventListener("click", () => {
    const w = $("canvas-wrap");
    if (document.fullscreenElement) document.exitFullscreen(); else (w.requestFullscreen || w.webkitRequestFullscreen).call(w);
  });
  document.addEventListener("fullscreenchange", () => {
    const on = !!document.fullscreenElement, b = $("btn-fullscreen");
    b.querySelector("path").setAttribute("d", on ? "M8 3v5H3M16 3v5h5M21 16h-5v5M3 16h5v5" : "M3 8V3h5M16 3h5v5M21 16v5h-5M8 21H3v-5");
    setTip(b, on ? "fullscreenLeave" : "fullscreen", on ? "Leave full screen (Esc)" : "Show the preview full screen (Esc to leave)");
  });
  document.querySelectorAll("#views button").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll("#views button").forEach((x) => x.classList.toggle("on", x === b));
    if (viewer) viewer.view(b.dataset.view);
  }));
  $("cut").addEventListener("input", (e) => { const v = +e.target.value; if (viewer) viewer.setCut(v / 100); $("cut-out").textContent = v >= 100 ? "Off" : `${v} %`; });
  document.addEventListener("keydown", (e) => {
    if (!((e.ctrlKey || e.metaKey) && e.key === "Enter")) return;
    const a = document.activeElement;                          // a value still being typed is saved on blur ("change") first
    if (a && a !== document.body && /^(INPUT|TEXTAREA)$/.test(a.tagName)) a.blur();
    generate();
  });
}

async function examples() {
  const list = (state.version && state.version.examples) || [];
  if (!list.length) return;
  const box = $("examples");
  for (const name of list) {
    box.append(el("button", { type: "button", class: "glass-btn small", ...tipAttrs("example", `Load ${name}, one of the boards in Generator/Input`, { name: stem(name) }),
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

// The 3D preview needs WebGL 2.  A browser without it (turned off, blocked graphics driver, remote desktop) still
// generates and downloads: only the preview, its tools and the parts list are off, and the empty preview says why.
function hasWebGL2() {
  try {
    const gl = document.createElement("canvas").getContext("webgl2");
    if (gl) { const lose = gl.getExtension("WEBGL_lose_context"); if (lose) lose.loseContext(); }
    return !!gl;
  } catch (e) { return false; }
}
function startViewer() {
  try {
    if (hasWebGL2()) return new Viewer($("view"), { section: CFG.crossSection === undefined ? "stencil" : CFG.crossSection, roleOf: (name) => (partInfo(name) || {}).role, onHover: showHover, onProgress: (f) => { $("readout").textContent = `Reading the STEP… ${Math.round(f * 100)} %`; } });
  } catch (e) { console.warn("3D preview off:", e && e.message); }
  $("canvas-wrap").classList.add("no-webgl");
  $("empty-note").replaceChildren("The 3D preview is off: this browser does not give the page WebGL.", el("br"),
    el("span", { class: "hint" }, "Generate, the checks and the downloads still work. Turning on hardware acceleration in the browser's settings brings the preview back."));
  for (const b of document.querySelectorAll("#btn-fit, #btn-shot, #views button, #cut")) b.disabled = true;
  return null;
}

/* ---- footer, Report a Problem, crash details ------------------------------------------------------------------- */
// The footer names the build (version.json: the commit and date build_site.py stamped), so a report can say exactly
// which page it is about.  Report a Problem opens a GitHub issue filled in with what the page knows (never the board).
let build = {};
const threeSource = () => (window.KESE_THREE === "backup" ? "this site's backup copy" : "jsDelivr");
function renderFooter() {
  const links = CFG.links || {}, a = (href, text, tip) => el("a", { href, target: "_blank", rel: "noopener", "data-tip": tip }, text);
  const stamp = build.commit ? `build ${build.commit}${build.built ? ` · ${build.built}` : ""}` : "";
  $("foot").replaceChildren("Generator: ", a(links.repository, "KiCad EM Stackup Exporter", "The project on GitHub"),
    build.kese ? ` ${build.kese}` : "", stamp ? " · " : "",
    stamp ? el("span", { class: "build", ...tipAttrs("build", `Python from ${state.python || "(loading)"} · three.js from ${threeSource()}`,
      { commit: build.commit, python: state.python || "(loading)", three: threeSource() }) }, stamp) : "",
    " · GPL-3.0-or-later · runs in your browser, nothing is uploaded · ",
    a("privacy.html", "Privacy", "What this page does with your data: it stays in your browser"), " · ",
    a("licenses.html", "Licences", "The open-source parts this page is made of, and their licences"), " · ",
    el("a", { href: "#", id: "report-link", target: "_blank", rel: "noopener",
      ...tipAttrs("reportProblem", "Open a GitHub issue filled in with this page's build, browser and changed settings (never the board). You see it before it is sent."),
      onclick: (e) => { e.currentTarget.href = issueUrl(); } }, "Report a Problem"));
}
function problemDetails(extra) {
  const lines = [
    `KESE web tool ${build.kese || "?"}, build ${build.commit || "?"} (${build.built || "?"})`,
    `Browser: ${navigator.userAgent}`,
    `Window: ${innerWidth} x ${innerHeight} at ${devicePixelRatio}x · 3D preview ${viewer ? "on" : "off (no WebGL)"} · ${document.documentElement.classList.contains("embedded") ? "in the blog's frame" : "own tab"}`,
    `Python from: ${state.python || "not loaded yet"} · three.js from: ${threeSource()}`,
  ];
  const changed = Object.keys(state.values).filter((k) => !same(state.values[k], state.start[k]));
  lines.push(changed.length ? "Settings changed from the defaults:" : "Settings: all defaults");
  for (const k of changed) lines.push(`  ${k}=${showValue(state.values[k])}`);
  const r = state.result;
  if (r) {
    const n = (l) => (r.checks || []).filter((i) => i.level === l).length;
    lines.push(`Last run: ${r.ok ? "made" : "not made"} in ${seconds(r.seconds || 0)}, ${n("error")} errors, ${n("warning")} warnings`);
    if (!r.ok) for (const i of (r.checks || []).filter((c) => c.level === "error")) lines.push(`  ${i.stage}: ${i.msg}`);
  }
  if (state.checksFatal) lines.push(`Start: ${state.checksFatal}`);
  if (extra) lines.push("", extra);
  return lines.join("\n");
}
function issueUrl(extra) {
  const repo = (CFG.links || {}).repository;
  let details = problemDetails(extra);
  if (details.length > 5000) details = details.slice(0, 5000) + "\n(cut)";       // GitHub refuses very long links
  const body = `**What happened, and what did you expect?**\n\n\n\n**Details** (filled in by the page; it never includes your board):\n\n\`\`\`\n${details}\n\`\`\`\n`;
  return `${repo}/issues/new?title=${encodeURIComponent("Web tool: ")}&body=${encodeURIComponent(body)}`;
}

// An error nothing else caught: a dialog with the details, a Copy button and Report a Problem.  Only the first one
// opens the dialog (later ones are added to its details); errors from browser extensions and other sites are left out,
// and so is the harmless "ResizeObserver loop" notice.
const crashes = [];
function crashText(err, where) {
  const msg = err.message || String(err);
  let stack = err.stack ? String(err.stack) : "";
  if (msg && stack.includes(msg) && stack.indexOf(msg) < 40) stack = stack.split("\n").slice(1).join("\n");   // Chrome repeats the message first
  return `${where}: ${msg}${stack ? "\n" + stack.split("\n").slice(0, 8).join("\n") : ""}`;
}
function foreign(file) {
  if (!file) return false;
  try { const u = new URL(file); return u.origin !== location.origin && !file.startsWith(CFG.three); } catch (e) { return true; }
}
function showCrash(text) {
  crashes.push(text);
  const details = crashes.join("\n\n");
  $("crash-details").textContent = details;
  $("crash-report").href = issueUrl(details);
  const d = $("crash-dialog");
  if (crashes.length === 1 && !d.open) { d.showModal(); d.querySelector("button[value=close]").focus(); }
}
function catchCrashes() {
  addEventListener("error", (e) => {
    const msg = String(e.message || "");
    if (/ResizeObserver loop/.test(msg) || foreign(e.filename) || (msg === "Script error." && !e.filename)) return;
    if (!(e.error || msg)) return;                                  // a resource that failed to load, not a script error
    showCrash(crashText(e.error || { message: msg }, `Error${e.filename ? ` in ${e.filename.split("/").pop()}:${e.lineno}` : ""}`));
  });
  addEventListener("unhandledrejection", (e) => {
    const r = e.reason;
    if (r && r.name === "AbortError") return;
    const stack = r && r.stack ? String(r.stack) : "";
    if (/(chrome|moz|safari)-extension:/.test(stack)) return;
    showCrash(crashText(r instanceof Error ? r : { message: String(r) }, "Unhandled promise rejection"));
  });
  $("crash-copy").addEventListener("click", async () => {
    try { await navigator.clipboard.writeText($("crash-details").textContent); toast("Details copied"); }
    catch (e) { getSelection().selectAllChildren($("crash-details")); toast("Copy did not work: the details are selected, press Ctrl+C"); }
  });
}

async function main() {
  catchCrashes();
  try { build = await (await fetch(new URL("version.json", import.meta.url), { cache: "no-cache" })).json(); } catch (e) { build = {}; }
  renderFooter();
  viewer = startViewer();
  wire();
  store.start();
  setBusy(true);
  let init;
  try {
    init = await startPython();
  } catch (e) {
    fatal(`Python could not be loaded: ${e.message}. Check the internet connection and reload the page.`);
    return;
  }
  state.desc = init.description;
  state.version = init.version;
  state.params = state.desc.parameters;
  for (const p of state.params) { state.byKey[p.key] = p; state.start[p.key] = clone(p.default); }
  state.values = clone(state.start);
  if (!build.kese) build.kese = state.desc.version;
  renderFooter();                                              // now with where Python came from
  state.ready = true;
  setBusy(false);
  updateGenerate();
  refresh();
  renderPreviewTabs();
  examples();
  state.checksNote = `Python is ready (${init.seconds.toFixed(1)} s). Choose a board: it is read here and never uploaded.`;
  $("checks-list").replaceChildren(el("p", { class: "hint" }, state.checksNote));
  // ?board=<example name> loads one of the examples (local testing, links from the blog)
  const b = QUERY.get("board");
  if (b && (state.version.examples || []).includes(b)) {
    const r = await fetch(new URL(`examples/${b}`, import.meta.url));
    if (r.ok) setBoard(b, await r.arrayBuffer());
  } else if (state.board) generate();                         // a board chosen while Python was still loading
}

if (!window.KESE_PHONE) main();
