/* SectionStencil.js - cross-section method 1: the cut faces drawn by the GPU in every frame (stencil capping).

   This is how CAD viewers fill a cut solid in real time (the OpenGL technique of the SIGGRAPH '99 advanced OpenGL
   notes; Open CASCADE's capping; three.js's webgl_clipping_stencil example).  For each part, in turn:
     1. its back faces add 1 to the stencil buffer and its front faces take 1 away, both clipped by the cut plane and
        drawn without colour or depth test.  Where the count is not 0, the eye looks into that solid through the cut;
     2. a plane lying in the cut, in the part's colour, is drawn only where the count is not 0, and sets it back to 0
        for the next part.
   Nothing is computed on the CPU, so the faces follow the slider in the same frame.  It needs closed solids:
   simulation models are; a visual model is a skin with no inside, so there the cut stays open (viewer.closedSolids).

   The interface every cross-section method gives the viewer (see Viewer.js, "cross-section"):
     new Method(viewer)   load()   cut(x | null)   partVisibility()   pickables()   dispose()
   Delete this file and the viewer still cuts, without faces. */
import * as THREE from "three";

const FIRST_ORDER = 10;                   // drawn after the model (renderOrder 0): two orders per part

export default class SectionStencil {
  constructor(viewer) {
    this.v = viewer;
    this.items = [];                      // per part: {part, stencils: [Mesh], cap: Mesh}
    this.group = null;                    // the caps, in world space
    this.on = false;
  }

  load() {
    this.dispose();
    const v = this.v;
    if (!v.root || v.closedSolids === false) return;
    const size = v.box.getSize(new THREE.Vector3());
    const span = Math.max(size.y, size.z) * 4 || 1;
    const capGeo = new THREE.PlaneGeometry(span, span).rotateY(-Math.PI / 2);        // in the plane x = 0, facing -X
    this.capGeo = capGeo;
    this.group = new THREE.Group();
    this.group.visible = false;
    v.parts.forEach((p, k) => {
      const order = FIRST_ORDER + 2 * k;
      const count = (side, op) => new THREE.MeshBasicMaterial({
        side, colorWrite: false, depthWrite: false, depthTest: false, clippingPlanes: [v.clip],
        stencilWrite: true, stencilFunc: THREE.AlwaysStencilFunc, stencilFail: op, stencilZFail: op, stencilZPass: op });
      const back = count(THREE.BackSide, THREE.IncrementWrapStencilOp), front = count(THREE.FrontSide, THREE.DecrementWrapStencilOp);
      const stencils = [];
      for (const m of p.meshes) {
        for (const mat of [back, front]) {
          const s = new THREE.Mesh(m.geometry, mat);
          s.renderOrder = order;
          s.visible = false;
          s.raycast = () => {};                                // never picked by the hover
          m.add(s);                                            // follows the body's transform
          stencils.push(s);
        }
      }
      const base = p.meshes[0].material, b = Array.isArray(base) ? base[0] : base;
      const cap = new THREE.Mesh(capGeo, new THREE.MeshStandardMaterial({
        color: b.color ? b.color.clone() : new THREE.Color("#b0b0b0"), metalness: b.metalness ?? 0, roughness: b.roughness ?? 0.7,
        stencilWrite: true, stencilRef: 0, stencilFunc: THREE.NotEqualStencilFunc,
        stencilFail: THREE.ReplaceStencilOp, stencilZFail: THREE.ReplaceStencilOp, stencilZPass: THREE.ReplaceStencilOp }));
      cap.renderOrder = order + 1;
      cap.raycast = () => {};
      this.group.add(cap);
      this.items.push({ part: p, stencils, cap, back, front });
    });
    const c = v.box.getCenter(new THREE.Vector3());
    this.group.position.set(0, c.y, c.z);
    v.scene.add(this.group);
    if (this.x != null) this.cut(this.x);
  }

  cut(x) {
    this.x = x;
    this.on = x != null;
    if (!this.group) return;
    this.group.position.x = this.on ? x : 0;
    this.group.visible = this.on;
    this.partVisibility();
  }

  partVisibility() {
    for (const it of this.items) {
      const show = this.on && it.part.visible;
      it.cap.visible = show;
      for (const s of it.stencils) s.visible = show;
    }
  }

  pickables() { return []; }              // the hover finds the cut part by its inside faces (Viewer.hover)

  dispose() {
    for (const it of this.items) {
      for (const s of it.stencils) s.parent && s.parent.remove(s);
      it.back.dispose(); it.front.dispose(); it.cap.material.dispose();
    }
    this.items = [];
    if (this.group) this.v.scene.remove(this.group);
    if (this.capGeo) this.capGeo.dispose();
    this.group = null; this.capGeo = null;
  }
}
