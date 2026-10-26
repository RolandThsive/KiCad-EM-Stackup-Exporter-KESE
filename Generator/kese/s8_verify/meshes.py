"""The checks of stage 8 (verify): the Model proves itself.

simulation : every part is a closed, consistently wound solid; no two parts overlap (vertical rays)
visual     : along every vertical ray the skin's faces take turns, into the material and out of it
both   : the glTF file passes the Khronos validator, if the `gltf_validator` CLI is on PATH"""
import shutil
import subprocess

import numpy as np
import trimesh

from parameters import P


def verify(model, glb_path=None, rays=3000):
    lines = []
    meshes = model.meshes
    scale = 1000.0 if model.units == "m" else 1.0      # report in mm
    # merge vertices at the geometry snap grid (Geometry.SNAP_GRID_MM), whatever the units
    digits = int(round(-np.log10(P.Geometry.SNAP_GRID_MM / scale))) + 2
    ok = True
    if model.mode == "simulation":
        for part, g in meshes.items():
            m = g.copy()
            m.merge_vertices(digits_vertex=digits)
            closed, consistent = m.is_watertight, m.is_winding_consistent
            vol = m.volume * scale ** 3
            lines.append(f"  {part:36s} closed={closed} winding={consistent} volume={vol:.4f} mm3")
            ok &= closed and consistent
        worst = _overlap(meshes, rays, scale)
        lines.append(f"  overlap between different parts along {rays} vertical rays: worst {worst * 1000:.3f} um")
        ok &= worst < 1e-4
    else:
        met, wrong = _skin_surfaces(meshes, rays)
        lines.append(f"  visible surfaces per vertical ray: faces met {met}; rays where in and out do not alternate: {wrong}")
        ok &= wrong == 0
    if glb_path is not None:
        exe = shutil.which("gltf_validator")
        if exe:
            r = subprocess.run([exe, "-a", str(glb_path)], capture_output=True, text=True)
            tail = (r.stdout or r.stderr).strip().splitlines()[-1:] or ["(no output)"]
            lines.append(f"  gltf_validator: {tail[0]}")
        else:
            lines.append("  gltf_validator not on PATH: glTF validation skipped")
    lines.insert(0, f"Verifier: {'PASS' if ok else 'FAIL'}")
    return ok, lines


def _rays(meshes, n):
    corners = np.array([m.bounds for m in meshes.values()])
    b = np.array([corners[:, 0].min(axis=0), corners[:, 1].max(axis=0)])
    rng = np.random.default_rng(1)
    pts = rng.uniform(b[0][:2], b[1][:2], size=(n, 2))
    zs = b[1][2] + (b[1][2] - b[0][2]) + 1e-6
    return np.c_[pts, np.full(n, zs)], np.tile([0, 0, -1.0], (n, 1))


def _overlap(meshes, n, scale):
    O, D = _rays(meshes, n)
    iv = {}
    for name, g in meshes.items():
        g = trimesh.Trimesh(g.vertices, g.faces, process=False)    # the ray index it builds goes with it
        locs, ri, _ = g.ray.intersects_location(O, D, multiple_hits=True)
        locs = np.asarray(locs).reshape(-1, 3)
        for r in np.unique(ri):
            z = np.sort(np.unique(np.round(locs[ri == r, 2] * scale, 6)))[::-1]
            if len(z) % 2 == 0:
                iv.setdefault(r, []).extend((name, z[k], z[k + 1]) for k in range(0, len(z), 2))
    worst = 0.0
    for L in iv.values():
        for a in range(len(L)):
            for c in range(a + 1, len(L)):
                if L[a][0] != L[c][0]:
                    worst = max(worst, min(L[a][1], L[c][1]) - max(L[a][2], L[c][2]))
    return worst


def _skin_surfaces(meshes, n):
    """({faces met: rays}, rays whose faces, from the top down, do not take turns into the material
    and out of it).  A closed outer surface gives in, out on every ray, or in, out, in, out where
    the ray crosses a hollow open to the air (the bore of a buried via under stacked micro vias); a
    face left inside the material or a doubled one gives two of a kind in a row."""
    O, D = _rays(meshes, n)
    allm = trimesh.util.concatenate(list(meshes.values()))
    locs, ri, ti = allm.ray.intersects_location(O, D, multiple_hits=True)
    nz = allm.face_normals[ti][:, 2]
    flat = np.abs(nz) > 0.5
    ri, z, into = ri[flat], np.asarray(locs).reshape(-1, 3)[flat, 2], nz[flat] > 0
    order = np.lexsort((-z, ri))
    ri, into = ri[order], into[order]
    count = np.bincount(ri, minlength=n)
    k = np.arange(len(ri)) - (np.cumsum(count) - count)[ri]      # 0, 1, 2, ... down each ray
    wrong = count % 2 == 1
    wrong[ri[into != (k % 2 == 0)]] = True
    met = np.unique(count[count > 0], return_counts=True)
    return {int(a): int(b) for a, b in zip(*met)}, int(wrong.sum())
