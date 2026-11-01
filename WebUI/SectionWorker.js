/* SectionWorker.js - works out the cross-section faces in a background thread, so the page never waits for them.

   The page sends, once per model:
     {type: "model", model, meshes: [{part, positions, index, matrix}]}   the parts' triangles (local positions, the
                                                                            optional index and the 4x4 world matrix)
   and then, as the slider moves:
     {type: "cut", model, seq, x}                                          the cut plane x = c in world units
   and gets back {type: "faces", model, seq, x, faces: [{part, triangles}]} (Section.js does the tracing).

   To answer fast, each part's triangles are sorted into slices along X when the model arrives, so a cut looks only
   at the triangles of the slice the plane is in, not at all of them. */
import { sectionTriangles } from "./Section.js";

const SLICES = 512;
let model = null, parts = [], x0 = 0, x1 = 1;

function load(msg) {
  model = msg.model;
  const byPart = new Map();
  for (const m of msg.meshes) {
    const p = m.positions, idx = m.index, e = m.matrix, n = idx ? idx.length : p.length / 3;
    const out = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      const v = idx ? idx[i] : i, x = p[3 * v], y = p[3 * v + 1], z = p[3 * v + 2];
      out[3 * i] = e[0] * x + e[4] * y + e[8] * z + e[12];
      out[3 * i + 1] = e[1] * x + e[5] * y + e[9] * z + e[13];
      out[3 * i + 2] = e[2] * x + e[6] * y + e[10] * z + e[14];
    }
    if (!byPart.has(m.part)) byPart.set(m.part, []);
    byPart.get(m.part).push(out);
  }
  x0 = Infinity; x1 = -Infinity;
  parts = [];
  for (const [part, chunks] of byPart) {
    const tris = new Float32Array(chunks.reduce((s, c) => s + c.length, 0));
    let o = 0; for (const c of chunks) { tris.set(c, o); o += c.length; }
    for (let k = 0; k < tris.length; k += 3) { x0 = Math.min(x0, tris[k]); x1 = Math.max(x1, tris[k]); }
    parts.push({ part, tris });
  }
  const w = (x1 - x0) / SLICES || 1;
  for (const p of parts) {                                 // slice s holds every triangle that reaches into it
    const lists = Array.from({ length: SLICES }, () => []);
    const t = p.tris;
    for (let k = 0, tri = 0; k < t.length; k += 9, tri++) {
      const lo = Math.min(t[k], t[k + 3], t[k + 6]), hi = Math.max(t[k], t[k + 3], t[k + 6]);
      const a = Math.max(0, Math.floor((lo - x0) / w)), b = Math.min(SLICES - 1, Math.floor((hi - x0) / w));
      for (let s = a; s <= b; s++) lists[s].push(tri);
    }
    p.slices = lists.map((l) => Uint32Array.from(l));
  }
}

function cut(x) {
  const w = (x1 - x0) / SLICES || 1;
  const s = Math.min(SLICES - 1, Math.max(0, Math.floor((x - x0) / w)));
  const faces = [];
  for (const p of parts) {
    const list = p.slices[s];
    if (!list.length) continue;
    const cand = new Float32Array(list.length * 9);
    for (let i = 0; i < list.length; i++) cand.set(p.tris.subarray(list[i] * 9, list[i] * 9 + 9), i * 9);
    const tri = sectionTriangles(cand, x);
    if (tri) faces.push({ part: p.part, triangles: tri });
  }
  return faces;
}

onmessage = (ev) => {
  const m = ev.data;
  if (m.type === "model") { load(m); return; }
  if (m.type === "cut" && m.model === model) {
    const faces = cut(m.x);
    postMessage({ type: "faces", model, seq: m.seq, x: m.x, faces }, faces.map((f) => f.triangles.buffer));
  }
};
