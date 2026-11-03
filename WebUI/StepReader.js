/* stepReader.js - reads the STEP files KESE writes (AP214: faces on PLANE or CYLINDRICAL_SURFACE, edges on
   LINE or CIRCLE, as Run.STEP_EXACT_ARCS writes them) into triangle meshes: one {name, color, positions} per
   solid.  Not a general STEP reader. */
import earcut from './earcut.js';

export function readKeseStep(text, onProgress = () => {}) {
  // 1. every entity "#id = TYPE(args);" -> type and raw argument text (entities can span lines)
  const ent = new Map();
  const start = text.indexOf('DATA;');
  const re = /#(\d+)\s*=\s*([A-Z0-9_]+)\s*\(/g;
  re.lastIndex = start;
  let m, n = 0;
  while ((m = re.exec(text))) {
    const open = re.lastIndex;                       // just after "TYPE("
    const end = text.indexOf(';', open);             // KESE writes no ';' inside strings
    ent.set(+m[1], [m[2], text.slice(open, end - 1)]);
    re.lastIndex = end + 1;
    if (++n % 500000 === 0) onProgress(end / text.length);
  }
  const refs = (s) => { const out = []; const r = /#(\d+)/g; let k; while ((k = r.exec(s))) out.push(+k[1]); return out; };
  const nums = (s) => s.match(/-?[\d.]+(?:[eE][-+]?\d+)?/g).map(Number);
  const point = (id) => { const [, a] = ent.get(id); return nums(a.slice(a.indexOf('('))); };
  const dir = point;

  // 2. names: PRODUCT <- FORMATION <- PRODUCT_DEFINITION <- PRODUCT_DEFINITION_SHAPE <- SHAPE_DEFINITION_REPRESENTATION -> ADVANCED_BREP_SHAPE_REPRESENTATION -> solid
  //    colours: STYLED_ITEM -> ... -> COLOUR_RGB, keyed by the solid
  const nameOfSolid = new Map(), colorOfSolid = new Map();
  for (const [id, [type, a]] of ent) {
    if (type === 'SHAPE_DEFINITION_REPRESENTATION') {
      const [pds, rep] = refs(a);
      const pd = refs(ent.get(pds)[1])[0], form = refs(ent.get(pd)[1])[0], prod = refs(ent.get(form)[1])[0];
      const name = ent.get(prod)[1].match(/'([^']*)'/)[1];
      const r = ent.get(rep);
      if (r && r[0] === 'ADVANCED_BREP_SHAPE_REPRESENTATION')
        for (const s of refs(r[1])) if (ent.get(s) && ent.get(s)[0] === 'MANIFOLD_SOLID_BREP') nameOfSolid.set(s, name);
    } else if (type === 'STYLED_ITEM') {
      const rs = refs(a), solid = rs[rs.length - 1];
      let cur = rs[0];
      for (let hop = 0; hop < 8 && cur && ent.get(cur) && ent.get(cur)[0] !== 'COLOUR_RGB'; hop++) cur = refs(ent.get(cur)[1]).at(-1);
      if (cur && ent.get(cur) && ent.get(cur)[0] === 'COLOUR_RGB') colorOfSolid.set(solid, nums(ent.get(cur)[1]));
    }
  }

  // 3. edges -> points.  A LINE edge gives its start vertex; a CIRCLE edge is sampled by angle (at most
  //    ARC_STEP per piece).  Each EDGE_CURVE is sampled once and shared by its two faces, so no cracks.
  const ARC_STEP = Math.PI / 15;                                   // 12 degrees: 30 pieces per circle
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const axisOf = (id) => { const ax = refs(ent.get(id)[1]); const o = point(ax[0]), z = dir(ax[1]), x = dir(ax[2]); return { o, z, x, y: cross(z, x) }; };
  const edgeCache = new Map();
  function edgePath(ec) {                                          // points v1 .. v2 inclusive
    let path = edgeCache.get(ec);
    if (path) return path;
    const [, ea] = ent.get(ec);
    const [v1, v2, curve] = refs(ea), sense = ea.trim().endsWith('.T.');
    const p1 = point(refs(ent.get(v1)[1])[0]), p2 = point(refs(ent.get(v2)[1])[0]);
    const [ct, ca] = ent.get(curve);
    if (ct !== 'CIRCLE') path = [p1, p2];
    else {
      const { o, x, y } = axisOf(refs(ca)[0]), r = nums(ca.slice(ca.lastIndexOf(',') + 1))[0];
      const ang = (p) => { const d = [p[0] - o[0], p[1] - o[1], p[2] - o[2]]; return Math.atan2(d[0] * y[0] + d[1] * y[1] + d[2] * y[2], d[0] * x[0] + d[1] * x[1] + d[2] * x[2]); };
      const a1 = ang(p1), a2 = ang(p2), TAU = 2 * Math.PI;
      const sweep = sense ? ((a2 - a1) % TAU + TAU) % TAU || TAU : -(((a1 - a2) % TAU + TAU) % TAU || TAU);
      const n = Math.max(1, Math.ceil(Math.abs(sweep) / ARC_STEP - 1e-6));
      path = [p1];
      for (let i = 1; i < n; i++) {
        const t = a1 + sweep * i / n, c = Math.cos(t) * r, s = Math.sin(t) * r;
        path.push([o[0] + c * x[0] + s * y[0], o[1] + c * x[1] + s * y[1], o[2] + c * x[2] + s * y[2]]);
      }
      path.push(p2);
      path.circle = true;
    }
    edgeCache.set(ec, path);
    return path;
  }
  const oriented = (oe) => { const [, oa] = ent.get(oe); const p = edgePath(refs(oa)[0]); return oa.trim().endsWith('.T.') ? p : Object.assign([...p].reverse(), { circle: p.circle }); };

  // 4. every solid: faces -> triangles.  Planar faces: loops projected into the plane, earcut.
  //    Cylindrical faces (bottom arc, line, top arc, line): a strip between the two arcs.
  const solids = [];
  let done = 0;
  const brepIds = [...ent].filter(([, [t]]) => t === 'MANIFOLD_SOLID_BREP').map(([id]) => id);
  for (const sid of brepIds) {
    const shell = refs(ent.get(sid)[1])[0];
    const pos = [];
    for (const fid of refs(ent.get(shell)[1])) {
      const [, fa] = ent.get(fid);
      const ids = refs(fa), surfId = ids.pop(), same = fa.trim().endsWith('.T.');
      const [st, sa] = ent.get(surfId);
      const { o, z, x, y } = axisOf(refs(sa)[0]);
      if (st === 'CYLINDRICAL_SURFACE') {
        const edges = refs(ent.get(refs(ent.get(ids[0])[1])[0])[1]).map(oriented);
        const arcs = edges.filter((e) => e.circle);
        if (arcs.length !== 2) continue;
        const A = arcs[0], B = [...arcs[1]].reverse();
        const n = Math.min(A.length, B.length) - 1;
        for (let i = 0; i < n; i++) {
          for (const [p, q, r] of [[A[i], A[i + 1], B[i + 1]], [A[i], B[i + 1], B[i]]]) {
            const nrm = cross([q[0] - p[0], q[1] - p[1], q[2] - p[2]], [r[0] - p[0], r[1] - p[1], r[2] - p[2]]);
            const c = [(p[0] + q[0] + r[0]) / 3 - o[0], (p[1] + q[1] + r[1]) / 3 - o[1], (p[2] + q[2] + r[2]) / 3 - o[2]];
            const h = c[0] * z[0] + c[1] * z[1] + c[2] * z[2], rad = [c[0] - h * z[0], c[1] - h * z[1], c[2] - h * z[2]];
            const out = (nrm[0] * rad[0] + nrm[1] * rad[1] + nrm[2] * rad[2]) > 0;
            if (out === same) pos.push(...p, ...q, ...r); else pos.push(...p, ...r, ...q);
          }
        }
        continue;
      }
      const flat = [], holes = [], pts = [];
      ids.forEach((bid, bi) => {                         // outer bound first, then holes
        const loop = refs(ent.get(bid)[1])[0];
        if (bi) holes.push(flat.length / 2);
        for (const oe of refs(ent.get(loop)[1])) {
          const path = oriented(oe);
          for (let k = 0; k < path.length - 1; k++) {     // each edge adds its points but not its end
            const p = path[k], d = [p[0] - o[0], p[1] - o[1], p[2] - o[2]];
            flat.push(d[0] * x[0] + d[1] * x[1] + d[2] * x[2], d[0] * y[0] + d[1] * y[1] + d[2] * y[2]);
            pts.push(p);
          }
        }
      });
      const tri = earcut(flat, holes.length ? holes : null);
      for (let t = 0; t < tri.length; t += 3) {
        const [a, b, c] = same ? [tri[t], tri[t + 1], tri[t + 2]] : [tri[t], tri[t + 2], tri[t + 1]];
        pos.push(...pts[a], ...pts[b], ...pts[c]);
      }
    }
    solids.push({ name: nameOfSolid.get(sid) || `solid ${sid}`, color: colorOfSolid.get(sid) || [0.7, 0.7, 0.7],
                  positions: new Float32Array(pos) });
    onProgress(0.5 + 0.5 * (++done / brepIds.length));
  }
  return solids;
}
