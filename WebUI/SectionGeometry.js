/* SectionGeometry.js - cross-section method 2 (kept, not used now): the exact section worked out on the CPU.

   SectionWorker.js gets the model's triangles once; for a cut it traces where the plane crosses each part's surface
   and fills the outlines (Section.js), so the faces are real geometry: exact, and pickable by the hover.  The cost
   is that they are rebuilt after each move of the slider, so they come a step behind it.  While the slider moves,
   only the newest position is ever sent: a request goes out when the worker is free, and when its answer comes
   back the next request carries wherever the slider is by then.

   Same interface as SectionStencil.js (see Viewer.js, "cross-section"):
     new Method(viewer)   load()   cut(x | null)   partVisibility()   pickables()   dispose()
   This file, SectionWorker.js and Section.js can be deleted together without touching the viewer. */
import * as THREE from "three";

// a copy of a position attribute as x, y, z floats (a glTF file may interleave them with other attributes)
function plainPositions(attr) {
  if (!attr.isInterleavedBufferAttribute && attr.array instanceof Float32Array && attr.itemSize === 3) return new Float32Array(attr.array);
  const out = new Float32Array(attr.count * 3);
  for (let i = 0; i < attr.count; i++) { out[3 * i] = attr.getX(i); out[3 * i + 1] = attr.getY(i); out[3 * i + 2] = attr.getZ(i); }
  return out;
}

export default class SectionGeometry {
  constructor(viewer) {
    this.v = viewer;
    this.worker = null;
    this.caps = null;
    this.modelId = 0;
  }

  load() {
    this.dispose();
    const v = this.v;
    if (!v.root) return;
    if (!this.worker) {
      this.worker = new Worker(new URL("./SectionWorker.js", import.meta.url), { type: "module" });
      this.worker.onmessage = (ev) => this.got(ev.data);
    }
    this.modelId++;
    this.caps = new THREE.Group();
    this.caps.visible = false;
    const meshes = [];
    v.parts.forEach((p, k) => {
      const base = p.meshes[0].material, b = Array.isArray(base) ? base[0] : base;
      const rank = v.depthRankOf(p);
      const mat = new THREE.MeshStandardMaterial({ color: b.color ? b.color.clone() : new THREE.Color("#b0b0b0"),
        metalness: b.metalness ?? 0, roughness: b.roughness ?? 0.7, side: THREE.DoubleSide,
        transparent: b.transparent, opacity: b.opacity ?? 1,
        polygonOffset: rank > 0, polygonOffsetFactor: -rank, polygonOffsetUnits: -4 * rank });
      p.cap = new THREE.Mesh(new THREE.BufferGeometry(), mat);
      p.cap.userData.part = p;
      p.cap.visible = false;
      this.caps.add(p.cap);
      for (const m of p.meshes) {
        const g = m.geometry;
        meshes.push({ part: k, positions: plainPositions(g.attributes.position), index: g.index ? new Uint32Array(g.index.array) : null,
          matrix: m.matrixWorld.elements.slice() });
      }
    });
    v.scene.add(this.caps);
    this.busy = false; this.sentX = null;
    this.worker.postMessage({ type: "model", model: this.modelId, meshes },
      meshes.flatMap((m) => (m.index ? [m.positions.buffer, m.index.buffer] : [m.positions.buffer])));
    if (this.wantX != null) this.ask();
  }

  cut(x) {
    this.wantX = x;
    if (x == null) { if (this.caps) this.caps.visible = false; return; }
    this.ask();
  }

  ask() {
    if (this.busy || this.wantX == null || this.wantX === this.sentX || !this.worker || !this.caps) return;
    this.busy = true;
    this.sentX = this.wantX;
    this.worker.postMessage({ type: "cut", model: this.modelId, seq: 0, x: this.wantX });
  }

  got(m) {
    if (m.model !== this.modelId || !this.caps) return;     // an answer for a model that is gone
    this.busy = false;
    const faces = new Map(m.faces.map((f) => [f.part, f.triangles]));
    this.v.parts.forEach((p, k) => {
      const tri = faces.get(k);
      p.cap.geometry.dispose();
      const g = new THREE.BufferGeometry();
      if (tri) {
        g.setAttribute("position", new THREE.BufferAttribute(tri, 3));
        const nrm = new Float32Array(tri.length);
        for (let i = 0; i < nrm.length; i += 3) nrm[i] = -1;  // every face lies in the plane, facing the cut-away side
        g.setAttribute("normal", new THREE.BufferAttribute(nrm, 3));
      }
      p.cap.geometry = g;
    });
    this.partVisibility();
    this.caps.visible = this.wantX != null;
    this.v.draw();
    this.ask();                                             // the slider moved meanwhile: catch up
  }

  partVisibility() {
    for (const p of this.v.parts) if (p.cap) p.cap.visible = p.visible && !!p.cap.geometry.attributes.position;
  }

  pickables() { return this.caps && this.caps.visible ? [this.caps] : []; }

  dispose() {
    if (this.caps) {
      this.v.scene.remove(this.caps);
      this.caps.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
      for (const p of this.v.parts) delete p.cap;
    }
    this.caps = null;
    this.modelId++;                                         // answers still on their way are ignored
  }
}
