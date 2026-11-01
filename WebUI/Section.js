/* Section.js - the true cross-section of a solid: where the plane x = c cuts its closed surface, the outlines of the
   cut are traced and filled, so a cut part shows its real section (the laminate, the copper, the mask, each in its
   own colour) instead of a hollow shell.

   triangles: world-space corners of every triangle of the part, 9 floats per triangle (Viewer.js keeps them).
   Returns the filled section as triangle corners (9 floats each, on the plane), or null when the plane misses it.

   1. every triangle that the plane crosses gives one segment of the outline (a corner exactly on the plane counts
      as being on the kept side, so no segment is made twice);
   2. the segments are joined end to end into closed loops (an edge's crossing point is computed from its corners in
      a fixed order, so the two triangles that share the edge give exactly the same point);
   3. loops inside loops alternate: outline, hole, island in the hole...;
   4. each outline with its holes is filled with earcut. */
import earcut from "./earcut.js";

export function sectionTriangles(triangles, c) {
  // 1. segments, in plane coordinates (u = z, v = y)
  const seg = [];
  const P = new Float64Array(9);
  const cross = (i, j) => {                                // the plane's crossing on the edge between corners i and j
    let a = i, b = j;
    if (P[3 * a] > P[3 * b] || (P[3 * a] === P[3 * b] && (P[3 * a + 1] > P[3 * b + 1] || (P[3 * a + 1] === P[3 * b + 1] && P[3 * a + 2] > P[3 * b + 2])))) { a = j; b = i; }
    const t = (c - P[3 * a]) / (P[3 * b] - P[3 * a]);
    return [P[3 * a + 2] + t * (P[3 * b + 2] - P[3 * a + 2]), P[3 * a + 1] + t * (P[3 * b + 1] - P[3 * a + 1])];
  };
  for (let k = 0; k < triangles.length; k += 9) {
    const x0 = triangles[k], x1 = triangles[k + 3], x2 = triangles[k + 6];
    if ((x0 < c && x1 < c && x2 < c) || (x0 >= c && x1 >= c && x2 >= c)) continue;
    for (let n = 0; n < 9; n++) P[n] = triangles[k + n];
    const s = [x0 >= c, x1 >= c, x2 >= c];
    const pts = [];
    for (const [i, j] of [[0, 1], [1, 2], [2, 0]]) if (s[i] !== s[j]) pts.push(cross(i, j));
    if (pts.length === 2) seg.push(pts[0], pts[1]);
  }
  if (!seg.length) return null;

  // 2. loops
  const key = (p) => p[0] + "," + p[1];
  const at = new Map();                                     // point -> segment ends there
  for (let i = 0; i < seg.length; i++) {
    const k = key(seg[i]);
    if (!at.has(k)) at.set(k, []);
    at.get(k).push(i);
  }
  const used = new Uint8Array(seg.length / 2);
  const loops = [];
  for (let s0 = 0; s0 < used.length; s0++) {
    if (used[s0]) continue;
    used[s0] = 1;
    const loop = [seg[2 * s0]];
    let end = seg[2 * s0 + 1];
    const startKey = key(seg[2 * s0]);
    let closed = false;
    for (let guard = 0; guard < used.length; guard++) {
      const k = key(end);
      if (k === startKey) { closed = true; break; }
      loop.push(end);
      const next = (at.get(k) || []).find((e) => !used[e >> 1]);
      if (next === undefined) break;
      used[next >> 1] = 1;
      end = seg[next ^ 1];                                  // the other end of that segment
    }
    if (closed && loop.length >= 3) loops.push(loop);
  }
  if (!loops.length) return null;

  // 3. nesting: each loop's parent is the smallest loop that contains it
  const info = loops.map((pts) => {
    let area = 0, u0 = Infinity, u1 = -Infinity, v0 = Infinity, v1 = -Infinity;
    for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      area += (pts[j][0] - pts[i][0]) * (pts[j][1] + pts[i][1]);
      u0 = Math.min(u0, pts[i][0]); u1 = Math.max(u1, pts[i][0]); v0 = Math.min(v0, pts[i][1]); v1 = Math.max(v1, pts[i][1]);
    }
    return { pts, area: Math.abs(area / 2), box: [u0, u1, v0, v1], parent: -1, depth: 0, holes: [] };
  });
  const order = info.map((_, i) => i).sort((a, b) => info[b].area - info[a].area);
  const inside = (p, pts) => {
    let inn = false;
    for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      if ((pts[i][1] > p[1]) !== (pts[j][1] > p[1]) && p[0] < (pts[j][0] - pts[i][0]) * (p[1] - pts[i][1]) / (pts[j][1] - pts[i][1]) + pts[i][0]) inn = !inn;
    }
    return inn;
  };
  for (let oi = 0; oi < order.length; oi++) {
    const L = info[order[oi]], p = L.pts[0];
    for (let pj = oi - 1; pj >= 0; pj--) {                  // smaller loops first: the first that contains it is its parent
      const C = info[order[pj]], b = C.box;
      if (C.area <= L.area || p[0] < b[0] || p[0] > b[1] || p[1] < b[2] || p[1] > b[3]) continue;
      if (inside(p, C.pts)) { L.parent = order[pj]; L.depth = C.depth + 1; break; }
    }
    if (L.depth % 2 === 1) info[L.parent].holes.push(L);
  }

  // 4. fill
  const out = [];
  for (const L of info) {
    if (L.depth % 2 === 1) continue;
    const flat = [], holes = [], all = [];
    for (const q of L.pts) { flat.push(q[0], q[1]); all.push(q); }
    for (const H of L.holes) {
      holes.push(all.length);
      for (const q of H.pts) { flat.push(q[0], q[1]); all.push(q); }
    }
    const tri = earcut(flat, holes.length ? holes : null);
    for (const i of tri) out.push(c, all[i][1], all[i][0]);
  }
  return out.length ? new Float32Array(out) : null;
}
