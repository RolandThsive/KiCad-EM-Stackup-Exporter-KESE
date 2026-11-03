/* OutputStore.js - where the page finds the files of the last run, and how it zips them.

   PyodideWorker.js moves each finished run onto the visitor's own disk, into the browser's private storage for this
   site (OPFS), folder runs/<tabId>/.  The files never leave the computer, and nothing is kept:
     - each open tab holds a Web Lock named after its folder, for as long as it is open;
     - when the tab is closed or reloaded (pagehide) its folder is deleted;
     - a browser that was closed before it could delete one (a crash, a killed process) leaves a folder that no tab
       holds a lock on: the next page load deletes it.
   A browser without OPFS gets the files from the worker in RAM, and the same calls read them from there. */

const LOCK_PREFIX = "kese-run-";

export class OutputStore {
  constructor() {
    this.tabId = (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2));
    this.memory = null;                          // {path: ArrayBuffer} when the run is kept in RAM
    this.files = [];                             // [{path, size}] of the last run
    this.storage = "none";
  }

  // hold this tab's lock, delete what closed tabs left behind, and delete our own folder when the tab goes
  async start() {
    if (navigator.locks) {
      navigator.locks.request(LOCK_PREFIX + this.tabId, () => new Promise(() => {}));   // held until the tab closes
    }
    addEventListener("pagehide", () => { this.removeOwn(); });
    try { await this.cleanLeftovers(); } catch (e) { /* storage blocked (private window): nothing to clean */ }
  }

  async runsDir(create = false) {
    if (!navigator.storage || !navigator.storage.getDirectory) return null;
    const root = await navigator.storage.getDirectory();
    try { return await root.getDirectoryHandle("runs", { create }); } catch (e) { return null; }
  }

  async cleanLeftovers() {
    const runs = await this.runsDir();
    if (!runs) return;
    const held = new Set();
    if (navigator.locks && navigator.locks.query) {
      const q = await navigator.locks.query();
      for (const l of [...(q.held || []), ...(q.pending || [])]) if (l.name.startsWith(LOCK_PREFIX)) held.add(l.name.slice(LOCK_PREFIX.length));
    } else return;                               // no way to tell another open tab's folder from a leftover
    for await (const [name] of runs.entries()) {
      if (name === this.tabId || held.has(name)) continue;
      try { await runs.removeEntry(name, { recursive: true }); } catch (e) { /* in use: next time */ }
    }
  }

  async removeOwn() {
    this.memory = null;
    try {
      const runs = await this.runsDir();
      if (runs) await runs.removeEntry(this.tabId, { recursive: true });
    } catch (e) { /* nothing written yet */ }
  }

  // the worker finished a run: remember where its files are
  setRun(result) {
    this.files = result.files || [];
    this.storage = result.storage;
    this.memory = result.storage === "memory" ? result.memory : null;
  }

  has(path) { return this.files.some((f) => f.path === path); }

  // one file of the run as a File (from the disk) or a Blob (from RAM)
  async file(path) {
    if (this.memory) {
      if (!(path in this.memory)) throw new Error(`${path} is not in this run`);
      return new File([this.memory[path]], path.split("/").pop());
    }
    const runs = await this.runsDir();
    let dir = await runs.getDirectoryHandle(this.tabId);
    const parts = path.split("/");
    for (const p of parts.slice(0, -1)) dir = await dir.getDirectoryHandle(p);
    return (await dir.getFileHandle(parts[parts.length - 1])).getFile();
  }

  async text(path) { return (await this.file(path)).text(); }
  async bytes(path) { return (await this.file(path)).arrayBuffer(); }

  // a zip of the files whose path passes keep(), every entry under folder/ (deflated in the browser, nothing uploaded)
  async zip(folder, keep = () => true) {
    const parts = [], central = [];
    let offset = 0;
    const enc = new TextEncoder();
    const { time, date } = dosTime(new Date());
    for (const f of this.files.filter((x) => keep(x.path))) {
      const raw = new Uint8Array(await this.bytes(f.path));
      const crc = crc32(raw);
      const deflated = new Uint8Array(await new Response(new Blob([raw]).stream().pipeThrough(new CompressionStream("deflate-raw"))).arrayBuffer());
      const stored = deflated.length >= raw.length;              // already compressed (a .glb with images): stored as it is
      const data = stored ? raw : deflated;
      const name = enc.encode(`${folder}/${f.path}`);
      const local = new DataView(new ArrayBuffer(30));
      local.setUint32(0, 0x04034b50, true); local.setUint16(4, 20, true); local.setUint16(6, 0x0800, true);
      local.setUint16(8, stored ? 0 : 8, true); local.setUint16(10, time, true); local.setUint16(12, date, true);
      local.setUint32(14, crc, true); local.setUint32(18, data.length, true); local.setUint32(22, raw.length, true);
      local.setUint16(26, name.length, true); local.setUint16(28, 0, true);
      parts.push(local.buffer, name, data);
      const c = new DataView(new ArrayBuffer(46));
      c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint16(8, 0x0800, true);
      c.setUint16(10, stored ? 0 : 8, true); c.setUint16(12, time, true); c.setUint16(14, date, true);
      c.setUint32(16, crc, true); c.setUint32(20, data.length, true); c.setUint32(24, raw.length, true);
      c.setUint16(28, name.length, true); c.setUint32(42, offset, true);
      central.push(c.buffer, name);
      offset += 30 + name.length + data.length;
    }
    const cdSize = central.reduce((s, p) => s + p.byteLength, 0);
    const end = new DataView(new ArrayBuffer(22));
    const n = central.length / 2;
    end.setUint32(0, 0x06054b50, true); end.setUint16(8, n, true); end.setUint16(10, n, true);
    end.setUint32(12, cdSize, true); end.setUint32(16, offset, true);
    return new Blob([...parts, ...central, end.buffer], { type: "application/zip" });
  }
}

function dosTime(d) {
  return { time: (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1),
           date: ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate() };
}

let CRC_TABLE = null;
function crc32(bytes) {
  if (!CRC_TABLE) {
    CRC_TABLE = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
      CRC_TABLE[n] = c >>> 0;
    }
  }
  let c = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
