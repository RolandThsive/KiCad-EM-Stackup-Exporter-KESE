/* PyodideWorker.js - runs KESE in a background thread, so the page never freezes.

   The page sends {id, cmd, args}; the worker answers {id, ok, result} or {id, ok: false, error}, and sends
   {type: "progress", text} while it loads, and {type: "line", kind, text, t} for each step of a run.  The commands:
     init       {pyodideBase, packages, config}  ->  {description, version, seconds}
     generate   {board: {name, bytes}, values, tabId}
                                                 ->  {ok, name, files [{path, size}], checks, log, seconds,
                                                      storage: "disk" | "memory", memory?: {path: ArrayBuffer}}
     exportZip  {values}                         ->  {zipBytes}
     readValues {text, fileName}                 ->  {values, ignored}

   On start it loads Pyodide with numpy and shapely, fetches generator.zip (Generator/kese and Generator/parameters
   of this branch, packed by build_site.py) and unpacks it into the in-memory file system.  version.json carries a
   hash of the zip, so the browser downloads the zip again only when it changed.

   Where a finished model lives: KESE writes it into the in-memory file system (RAM); the worker then moves every file
   to the browser's private storage on the visitor's own disk (OPFS, folder runs/<tabId>/) and frees the RAM.  The
   page (OutputStore.js) deletes that folder when the tab is closed or reloaded.  A browser without OPFS keeps the
   files in RAM instead (storage: "memory"). */

import earcut from "./earcut.js";
globalThis.earcut = earcut;                    // mapbox_earcut.py calls it

let pyodide = null, WG = null;
const ROOT = "/kese";
const OUT = `${ROOT}/Output`;

let step = "";                                 // what init is doing now, named in the message if it fails
function progress(text) { step = text; postMessage({ type: "progress", text }); }

// A dropped connection is tried again (twice) before it is reported, and the report names the file.
async function fetchBytes(url, cache = "default") {
  for (let tries = 1; ; tries++) {
    let r;
    try { r = await fetch(url, { cache }); }
    catch (e) {
      if (tries < 3) { await new Promise((done) => setTimeout(done, 400 * tries)); continue; }
      throw new Error(`${url} could not be downloaded (${e.message})`);
    }
    if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
    return new Uint8Array(await r.arrayBuffer());
  }
}
const here = (file) => new URL(file, import.meta.url).href;

async function init({ pyodideBase, packages, config }) {
  const t0 = performance.now();
  try {
    progress("Loading Python (Pyodide)…");
    const { loadPyodide } = await import(pyodideBase + "pyodide.mjs");   // Pyodide 314 runs in module workers only
    pyodide = await loadPyodide({ indexURL: pyodideBase });
    progress(`Loading ${packages.join(" and ")}…`);
    await pyodide.loadPackage(packages);
    progress("Fetching the generator…");
    const version = JSON.parse(new TextDecoder().decode(await fetchBytes(here("version.json"), "no-cache")));
    const [zip, wg, shim] = await Promise.all([
      fetchBytes(here(`generator.zip?v=${version.zip}`)),
      fetchBytes(here("WebGenerator.py"), "no-cache"),
      fetchBytes(here("mapbox_earcut.py"), "no-cache"),
    ]);
    for (const d of [`${ROOT}/web`, `${ROOT}/Input`, OUT]) pyodide.FS.mkdirTree(d);
    pyodide.unpackArchive(zip, "zip", { extractDir: ROOT });
    pyodide.FS.writeFile(`${ROOT}/web/WebGenerator.py`, wg);
    pyodide.FS.writeFile(`${ROOT}/web/mapbox_earcut.py`, shim);
    pyodide.runPython(`import sys; sys.path.insert(0, "${ROOT}/web")`);
    WG = pyodide.pyimport("WebGenerator");
    WG.configure(JSON.stringify(config));
    progress("Reading the parameter files…");
    const description = JSON.parse(WG.describe());
    return { description, version, seconds: (performance.now() - t0) / 1000 };
  } catch (e) {
    const early = /^Loading/.test(step) ? ` from ${pyodideBase}` : "";
    throw new Error(`${e && e.message || e} [${step.replace("…", "")}${early}]`);
  }
}

/* ---- the run's files: from RAM to the visitor's disk ------------------------------------------- */
async function opfsRoot() {
  try {
    if (!navigator.storage || !navigator.storage.getDirectory) return null;
    const root = await navigator.storage.getDirectory();
    const probe = await (await root.getDirectoryHandle("runs", { create: true })).getFileHandle(".probe", { create: true });
    if (!probe.createSyncAccessHandle) return null;          // old browsers: OPFS without the worker's fast writes
    return root;
  } catch (e) { return null; }
}

// runs/<tabId>/ emptied, then every file of the run moved into it (written, then deleted from RAM, one at a time)
async function moveToDisk(folder, files, tabId) {
  const root = await opfsRoot();
  if (!root) return null;
  const runs = await root.getDirectoryHandle("runs", { create: true });
  try { await runs.removeEntry(tabId, { recursive: true }); } catch (e) { /* first run of this tab */ }
  const tab = await runs.getDirectoryHandle(tabId, { create: true });
  for (const f of files) {
    const parts = f.path.split("/");
    let dir = tab;
    for (const p of parts.slice(0, -1)) dir = await dir.getDirectoryHandle(p, { create: true });
    const fh = await dir.getFileHandle(parts[parts.length - 1], { create: true });
    const access = await fh.createSyncAccessHandle();
    try {
      const src = `${folder}/${f.path}`;
      const bytes = pyodide.FS.readFile(src);
      access.truncate(0);
      access.write(bytes, { at: 0 });
      access.flush();
      pyodide.FS.unlink(src);
    } finally { access.close(); }
  }
  return true;
}

function readAll(folder, files) {
  const out = {};
  for (const f of files) {
    const b = pyodide.FS.readFile(`${folder}/${f.path}`);
    out[f.path] = b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);
  }
  return out;
}

function clearInput() {
  for (const n of pyodide.FS.readdir(`${ROOT}/Input`)) if (n !== "." && n !== "..") pyodide.FS.unlink(`${ROOT}/Input/${n}`);
}

async function generate({ board, values, tabId }) {
  const t0 = performance.now();
  clearInput();
  pyodide.FS.writeFile(`${ROOT}/Input/${board.name}`, new Uint8Array(board.bytes));
  // Each stage and log line goes to the page as it happens (the page is free while Python works here).
  const onLine = (kind, text) => postMessage({ type: "line", kind, text, t: (performance.now() - t0) / 1000 });
  const result = JSON.parse(WG.generate(board.name, JSON.stringify(values), onLine));
  result.seconds = (performance.now() - t0) / 1000;
  if (!result.ok) return { result };
  let onDisk = null;
  try { onDisk = await moveToDisk(result.folder, result.files, tabId); }
  catch (e) { onDisk = null; result.diskError = String(e && e.message || e); }
  if (onDisk) { result.storage = "disk"; return { result }; }
  result.storage = "memory";
  result.memory = readAll(result.folder, result.files);
  return { result, transfer: Object.values(result.memory) };
}

function readFileBuffer(path) {
  const bytes = pyodide.FS.readFile(path);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

onmessage = async (ev) => {
  const { id, cmd, args } = ev.data;
  try {
    let result, transfer = [];
    if (cmd === "init") result = await init(args);
    else if (cmd === "generate") ({ result, transfer = [] } = await generate(args));
    else if (cmd === "exportZip") {
      const path = `${ROOT}/parameter_files.zip`;
      WG.export_zip(JSON.stringify(args.values), path);
      result = { zipBytes: readFileBuffer(path) };
      pyodide.FS.unlink(path);
      transfer = [result.zipBytes];
    } else if (cmd === "readValues") result = JSON.parse(WG.read_values(args.text, args.fileName || ""));
    else throw new Error("unknown command " + cmd);
    postMessage({ id, ok: true, result }, transfer);
  } catch (e) {
    postMessage({ id, ok: false, error: String(e && e.message || e) });
  }
};
