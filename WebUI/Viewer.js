/* Viewer.js - the 3D preview: our own three.js viewer with <model-viewer>'s look (mvEnvironment.js: the neutral
   studio light, PBR Neutral tone mapping, exposure 1.3, no direct lights).

   It shows the files KESE wrote, read in the browser: GLB (three's GLTFLoader), OBJ + MTL (OBJLoader, MTLLoader),
   the STL folder (STLLoader, with the colours of materials.json) and STEP (StepReader.js, in StepWorker.js).
   Every solid of the model is a "part" with a name; the page lists them, hides them, and the hover card names the
   one under the mouse.

   The board lies flat in the scene, its top up (+Y), whatever orientation the files have (Run.ORIENTATION): the
   thinnest side of the model is taken as the board's thickness.  Tools: views (Iso, Top, Bottom, Side), Fit,
   cross-section (a cut across X; the cut faces come from a cross-section method module, see "cross-section"
   below), screenshot.
   It draws only when something changed (a 600k-triangle STEP would make a constant loop heavy). */
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { STLLoader } from "three/addons/loaders/STLLoader.js";
import { OBJLoader } from "three/addons/loaders/OBJLoader.js";
import { MTLLoader } from "three/addons/loaders/MTLLoader.js";
import { useModelViewerLook } from "./mvEnvironment.js";

const METAL_ROLES = /^(copper|plating|finish|via|pad)/i;

/* Simulation models are solids that touch: the mask lies on the copper, the copper on the laminate, so two parts
   share the same faces and the GPU cannot tell which is in front (z-fighting, a flickering pattern).  Each part is
   pulled toward the camera by a depth offset that grows with how much it should win where faces meet: silkscreen
   over mask, mask over finish, finish over copper, copper over laminate.  A finish is a stack of its own (nickel,
   then palladium, then gold, bottom to top; ENIG's gold is only 80 nm thick, so its faces sit on the nickel's), so
   its metals are ranked in that order too.  Only the depth test changes, not the geometry.  The rank is read from
   the part's role (materials.json) and its name ("Top Finish Gold"). */
const FINISH = /finish|nickel|gold|palladium|silver|tin|osp/;
const FINISH_METALS = [[/gold/, 4], [/palladium/, 3], [/nickel/, 2]];      // others (tin, silver, OSP) are one layer: 3
const DEPTH_RANKS = [[/silk/, 7], [/mask.?over.?copper/, 6], [/mask/, 5]];
function depthRank(text) {
  const t = text.toLowerCase();
  for (const [re, rank] of DEPTH_RANKS) if (re.test(t)) return rank;
  if (FINISH.test(t)) { for (const [re, rank] of FINISH_METALS) if (re.test(t)) return rank; return 3; }
  return /copper|plating|via|pad/.test(t) ? 1 : 0;
}

export class Viewer {
  constructor(canvas, { onHover = () => {}, onProgress = () => {}, roleOf = () => "", section = "stencil" } = {}) {
    this.canvas = canvas;
    this.roleOf = roleOf;
    this.onHover = onHover;
    this.onProgress = onProgress;
    this.renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true, stencil: true });
    this.renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    this.renderer.localClippingEnabled = true;
    this.scene = new THREE.Scene();
    useModelViewerLook(this.renderer, this.scene);
    this.camera = new THREE.PerspectiveCamera(30, 1, 0.001, 100);
    this.controls = new OrbitControls(this.camera, canvas);
    this.controls.enableDamping = false;
    this.controls.addEventListener("change", () => this.draw());
    this.clip = new THREE.Plane(new THREE.Vector3(1, 0, 0), 0);     // keeps x >= -constant: the cut faces the Iso camera
    this.clipOn = false;
    this.root = null;
    this.parts = [];                       // [{name, meshes: [Mesh], color, triangles, visible, baseY}]
    this.size = 1;
    this.raycaster = new THREE.Raycaster();
    this.pointer = null;
    new ResizeObserver(() => this.resize()).observe(canvas.parentElement);
    canvas.addEventListener("pointermove", (e) => { this.pointer = e; if (!this.hoverQueued) { this.hoverQueued = true; requestAnimationFrame(() => this.hover()); } });
    canvas.addEventListener("pointerleave", () => { this.pointer = null; this.onHover(null); });
    this.resize();
    this.closedSolids = true;              // the page says so per model: false for a visual model (a skin, no inside)
    this.useSection(section);
  }

  /* ---- cross-section ----------------------------------------------------------------------------
     The cut itself is the clipping plane (the GPU hides the cut-away side).  The faces where the solids are cut come
     from a cross-section method, a module loaded by name, so a method can be deleted without touching this file:
       stencil   SectionStencil.js: drawn by the GPU in every frame (stencil capping)          (used)
       geometry  SectionGeometry.js + SectionWorker.js + Section.js: the exact section, on the CPU (kept for later)
     A method is a class: new Method(viewer), load() after a model is shown, cut(x | null), partVisibility() after a
     part is hidden or shown, pickables() (extra meshes for the hover) and dispose().  Without one (missing file,
     or section: null) the model is still cut, without faces. */
  useSection(name) {
    const file = { stencil: "./SectionStencil.js", geometry: "./SectionGeometry.js" }[name];
    if (this.section) { this.section.dispose(); this.section = null; }
    this.sectionReady = !file ? Promise.resolve() : import(file).then((m) => {
      this.section = new m.default(this);
      if (this.root) { this.section.load(); this.setCut(this.cut ?? 1); }
    }).catch((e) => { console.warn(`cross-section method ${name} not available: ${e.message}`); });
    return this.sectionReady;
  }
  depthRankOf(p) { return depthRank(`${this.roleOf(p.name) || ""} ${p.name}`); }

  resize() {
    const r = this.canvas.parentElement.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const ratio = Math.min(2, window.devicePixelRatio || 1);       // browser zoom changes it: keep the canvas sharp
    if (ratio !== this.renderer.getPixelRatio()) this.renderer.setPixelRatio(ratio);
    this.renderer.setSize(r.width, r.height, false);
    this.camera.aspect = r.width / r.height;
    this.camera.updateProjectionMatrix();
    this.draw();
  }

  draw() {
    if (this.drawQueued) return;
    this.drawQueued = true;
    requestAnimationFrame(() => { this.drawQueued = false; this.fitDepth(); this.renderer.render(this.scene, this.camera); });
  }

  // the near and far planes follow the camera, so the depth buffer's precision is spent on the model, close up too
  fitDepth() {
    const d = this.camera.position.distanceTo(this.controls.target);
    const near = Math.max(d - this.size, d / 50, this.size / 1e5);
    const far = d + this.size * 2;
    if (Math.abs(near - this.camera.near) > 1e-9 * d || Math.abs(far - this.camera.far) > 1e-9 * d) {
      this.camera.near = near; this.camera.far = far; this.camera.updateProjectionMatrix();
    }
  }

  clear() {
    if (this.section) this.section.dispose();
    if (this.root) {
      this.scene.remove(this.root);
      this.root.traverse((o) => {
        if (o.geometry) o.geometry.dispose();
        const m = o.material;
        if (m) (Array.isArray(m) ? m : [m]).forEach((x) => { for (const k in x) if (x[k] && x[k].isTexture) x[k].dispose(); x.dispose(); });
      });
    }
    this.root = null; this.parts = [];
    this.onHover(null);
    this.draw();
  }

  /* ---- loading ---------------------------------------------------------------------------------- */
  material(color, alpha = 1, metal = false) {
    const c = Array.isArray(color) ? new THREE.Color().setRGB(color[0], color[1], color[2], THREE.SRGBColorSpace) : new THREE.Color(color || "#b0b0b0");
    return new THREE.MeshStandardMaterial({ color: c, metalness: metal ? 1 : 0, roughness: metal ? 0.35 : 0.7,
      transparent: alpha < 1, opacity: alpha, side: THREE.DoubleSide, clippingPlanes: [this.clip] });
  }

  // the parts of a loaded object: one per named node with meshes under it
  show(object, partOf) {
    this.clear();
    const root = new THREE.Group();
    root.add(object);
    // the board's thickness is the model's thinnest side: turn that side to +Y (the board's top up)
    const box0 = new THREE.Box3().setFromObject(object), s0 = box0.getSize(new THREE.Vector3());
    if (s0.z < s0.y && s0.z <= s0.x) object.rotation.x = -Math.PI / 2;           // flat in XY, top toward +Z
    else if (s0.x < s0.y && s0.x < s0.z) object.rotation.z = Math.PI / 2;        // standing in YZ
    object.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(object), c = box.getCenter(new THREE.Vector3());
    object.position.sub(c);
    object.updateMatrixWorld(true);
    this.size = box.getSize(new THREE.Vector3()).length() || 1;
    this.thickness = Math.max(1e-9, box.max.y - box.min.y);
    const byName = new Map();
    object.traverse((o) => {
      if (!o.isMesh) return;
      const mats = Array.isArray(o.material) ? o.material : [o.material];
      for (const m of mats) { m.clippingPlanes = [this.clip]; m.side = THREE.DoubleSide; }
      const name = partOf(o);
      if (!byName.has(name)) byName.set(name, { name, meshes: [], triangles: 0, visible: true, color: "#" + (mats[0].color ? mats[0].color.getHexString(THREE.SRGBColorSpace) : "b0b0b0") });
      const p = byName.get(name);
      p.meshes.push(o);
      const g = o.geometry;
      p.triangles += g.index ? g.index.count / 3 : g.attributes.position.count / 3;
    });
    for (const p of byName.values()) {
      const rank = depthRank(`${this.roleOf(p.name) || ""} ${p.name}`);
      for (const m of [...p.meshes]) {
        m.material = Array.isArray(m.material) ? m.material.map((x) => x.clone()) : m.material.clone();
        const mats = Array.isArray(m.material) ? m.material : [m.material];
        for (const x of mats) {
          x.clippingPlanes = [this.clip];                         // clone() copies the planes: keep the shared one
          x.side = THREE.FrontSide;
          x.polygonOffset = rank > 0; x.polygonOffsetFactor = -rank; x.polygonOffsetUnits = -4 * rank;
        }
        m.userData.part = p;
      }
    }
    this.parts = [...byName.values()];
    this.root = root;
    this.scene.add(root);
    this.box = new THREE.Box3().setFromObject(root);         // once: the slider must not walk 900k corners per move
    if (this.section) this.section.load();
    this.setCut(this.cut ?? 1);
    this.view(this.lastView || "iso");
    return this.parts;
  }

  async loadGLB(buffer) {
    const gltf = await new GLTFLoader().parseAsync(buffer, "");
    // a part is the node the mesh belongs to (KESE names one node per part; a node with several primitives is a
    // Group of meshes in three.js)
    return this.show(gltf.scene, (o) => (o.parent && o.parent.isGroup && o.parent !== gltf.scene && o.parent.name) || o.name || "part");
  }

  loadOBJ(objText, mtlText) {
    const loader = new OBJLoader();
    if (mtlText) {
      const mats = new MTLLoader().parse(mtlText, "");
      mats.preload();
      loader.setMaterials(mats);
    }
    const obj = loader.parse(objText);
    obj.traverse((o) => {
      if (!o.isMesh) return;
      const m = o.material;
      if (m && !m.isMeshStandardMaterial) {
        const metal = METAL_ROLES.test(o.name);
        o.material = this.material("#" + m.color.getHexString(THREE.SRGBColorSpace), m.opacity ?? 1, metal);
        m.dispose();
      }
    });
    return this.show(obj, (o) => o.name || "part");
  }

  // files: [{name (stem), buffer}], looks: {stem: {color, alpha, role}} from materials.json
  loadSTL(files, looks = {}) {
    const g = new THREE.Group(), loader = new STLLoader();
    for (const f of files) {
      const geo = loader.parse(f.buffer);
      const look = looks[f.name] || {};
      const mesh = new THREE.Mesh(geo, this.material(look.color || "#b0b0b0", look.alpha ?? 1, METAL_ROLES.test(look.role || f.name)));
      mesh.name = f.name;
      g.add(mesh);
    }
    return this.show(g, (o) => o.name);
  }

  loadSTEP(buffer) {
    return new Promise((resolve, reject) => {
      const w = new Worker(new URL("./StepWorker.js", import.meta.url), { type: "module" });
      w.onmessage = (ev) => {
        const m = ev.data;
        if (m.type === "progress") { this.onProgress(m.fraction); return; }
        w.terminate();
        if (m.type === "error") { reject(new Error(m.error)); return; }
        const g = new THREE.Group();
        for (const s of m.solids) {
          const geo = new THREE.BufferGeometry();
          geo.setAttribute("position", new THREE.BufferAttribute(s.positions, 3));
          geo.computeVertexNormals();
          const mesh = new THREE.Mesh(geo, this.material(s.color, 1, METAL_ROLES.test(s.name)));
          mesh.name = s.name;
          g.add(mesh);
        }
        resolve(this.show(g, (o) => o.name));
      };
      w.onerror = (e) => { w.terminate(); reject(new Error(e.message || "the STEP reader stopped")); };
      w.postMessage({ buffer }, [buffer]);
    });
  }

  /* ---- tools ------------------------------------------------------------------------------------ */
  // Iso is <model-viewer>'s camera-orbit="-25deg 60deg auto": 25 deg left, 30 deg above the board
  view(name) {
    this.lastView = name;
    const deg = THREE.MathUtils.degToRad;
    // Top and Bottom look straight down or up, the board's top edge up on screen (Bottom mirrored, as KiCad's flipped view).  OrbitControls keeps camera.up as
    // it was when it started (+Y), so the views go near the poles instead of changing up (which made turning wild);
    // turning is off there, zoom and pan stay.  3D View (iso) turns freely again.
    const [theta, phi] = { iso: [-25, 60], top: [0, 0.001], bottom: [180, 179.999] }[name] || [-25, 60];
    const fit = 0.5 * this.size / Math.sin(deg(this.camera.fov / 2)) * 0.8 / Math.min(1, this.camera.aspect);
    let d = Math.max(fit, 1e-6);
    if ((name === "top" || name === "bottom") && this.root) {     // straight on: the whole board fits, with a margin
      const sz = new THREE.Box3().setFromObject(this.root).getSize(new THREE.Vector3()), t = Math.tan(deg(this.camera.fov / 2));
      d = 1.35 * Math.max(sz.z / 2 / t, sz.x / 2 / (t * this.camera.aspect)) + sz.y / 2;
    }
    const th = deg(theta), ph = deg(phi);
    this.camera.position.set(d * Math.sin(ph) * Math.sin(th), d * Math.cos(ph), d * Math.sin(ph) * Math.cos(th));
    this.camera.up.set(0, 1, 0);
    this.controls.enableRotate = !(name === "top" || name === "bottom");
    // the studio light comes from above; seen from below the board would face the dim floor, so for Bottom the
    // studio is turned over and the bottom gets the same light the top gets in Top
    this.scene.environmentRotation.set(name === "bottom" ? Math.PI : 0, 0, 0);
    this.controls.target.set(0, 0, 0);
    this.controls.update();
    this.draw();
  }
  fit() { this.view(this.lastView || "iso"); }

  // 0 .. 1: how much of the model is kept, cut across X from the side the Iso view looks from; 1 = no cut
  setCut(f) {
    this.cut = f;
    if (!this.root) return;
    const x = this.box.max.x - (this.box.max.x - this.box.min.x) * f;
    this.clip.constant = f >= 1 ? Infinity : -x;             // the GPU hides the cut-away side at once
    if (this.section) this.section.cut(f >= 1 ? null : x);
    this.draw();
  }


  setVisible(name, on) {
    for (const p of this.parts) if (p.name === name) { p.visible = on; for (const m of p.meshes) m.visible = on; }
    if (this.section) this.section.partVisibility();
    this.draw();
  }

  hover() {
    this.hoverQueued = false;
    if (!this.pointer || !this.root) return;
    const r = this.canvas.getBoundingClientRect();
    const v = new THREE.Vector2(((this.pointer.clientX - r.left) / r.width) * 2 - 1, -((this.pointer.clientY - r.top) / r.height) * 2 + 1);
    this.raycaster.setFromCamera(v, this.camera);
    // While cut, faces are picked from both sides: through a cut face the first face the ray meets is the inside of
    // the solid that was cut, so the card names that part.
    const cutting = this.cut < 1, flipped = [];
    if (cutting) this.root.traverse((o) => { if (o.isMesh) for (const m of [].concat(o.material)) if (m.side !== THREE.DoubleSide) { flipped.push([m, m.side]); m.side = THREE.DoubleSide; } });
    const extra = this.section ? this.section.pickables() : [];
    const hits = this.raycaster.intersectObjects([this.root, ...extra], true).filter((h) => h.object.visible && (!cutting || this.clip.distanceToPoint(h.point) >= -1e-9 * this.size));
    for (const [m, side] of flipped) m.side = side;
    this.onHover(hits.length ? hits[0].object.userData.part : null);
  }

  screenshot() {
    this.renderer.render(this.scene, this.camera);
    return new Promise((resolve) => this.canvas.toBlob(resolve, "image/png"));
  }

  boardSize(unitsPerMm) {
    if (!this.root) return null;
    const s = new THREE.Box3().setFromObject(this.root).getSize(new THREE.Vector3());
    return [s.x / unitsPerMm, s.z / unitsPerMm, this.thickness / unitsPerMm];
  }
}
