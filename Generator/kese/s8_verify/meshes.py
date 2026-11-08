"""The checks of stage 8 (verify).  simulation: every part closed and consistently wound, no two
parts overlapping (overlap.py); visual: faces take turns in and out along vertical rays; both: the
Khronos gltf_validator, when on PATH."""
import shutil
import subprocess

import numpy as np

from kese.core.part_checks import mesh_check
from kese.s8_verify.overlap import overlaps
from kese.s8_verify.vertical_rays import vertical_hits
from parameters import P


def check_meshes(model, glb_path):
    """(ok, report lines) of the checks below."""
    lines = []
    meshes = model.meshes
    scale = 1000.0 if model.units == "m" else 1.0      # report in mm
    ok = True
    if model.mode == "simulation":
        for part, g in meshes.items():                  # checked where the part was built, or here
            checked = model.checks.get(part)
            c = checked[0] if checked and checked[0] else mesh_check(g, model.units)
            lines.append(f"  {part:36s} closed={c.closed} winding={c.consistent} volume={c.merged_volume * scale ** 3:.4f} mm3")
            ok &= c.closed and c.consistent
        found = overlaps(model)
        lines.append("  overlap between different parts, every slice against the others: " + (
            f"worst {found[0][0]:.3e} mm3, {found[0][1]} and {found[0][2]} at z {found[0][3]:+.4f} .. "
            f"{found[0][4]:+.4f} mm ({len(found)} place{'s' * (len(found) > 1)})" if found else "none"))
        ok &= not found
    else:
        met, wrong = _skin_surfaces(meshes, P.Verifier.VERIFY_RAYS, model.transform)
        lines.append(f"  visible surfaces per vertical ray: faces met {met}; rays where in and out do not alternate: {wrong}")
        ok &= wrong == 0
    if glb_path is not None:
        exe = shutil.which("gltf_validator")
        if exe:
            r = subprocess.run([exe, "-a", str(glb_path)], capture_output=True, text=True, check=False)
            tail = (r.stdout or r.stderr).strip().splitlines()[-1:] or ["(no output)"]
            lines.append(f"  gltf_validator: {tail[0]}")
        else:
            lines.append("  gltf_validator not on PATH: glTF validation skipped")
    return ok, lines


def _skin_surfaces(meshes, n, transform):
    """({faces met: rays}, rays whose faces, from the top down, do not take turns into the material
    and out of it, as a closed outer surface does).  The n rays start at random points (fixed seed)
    over the bounding box of every mesh and run along the board's normal, in either orientation: the
    meshes are turned back by the quarter turns of `transform` (the output transform), exactly."""
    vs, fs, at = [], [], 0
    for m in meshes.values():
        vs.append(np.asarray(m.vertices, dtype=float))
        fs.append(np.asarray(m.faces) + at)
        at += len(vs[-1])
    M = np.asarray(transform, dtype=float)[:3, :3]
    turn = np.round(M / np.abs(M).max())                    # the orientation alone, without the units
    V, F = np.concatenate(vs) @ turn, np.concatenate(fs)
    used = V[np.unique(F)]
    lo, hi = used.min(axis=0), used.max(axis=0)
    xy = np.random.default_rng(1).uniform(lo[:2], hi[:2], size=(n, 2))
    t = V[F]
    normal = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    nz = normal[:, 2] / np.maximum(np.linalg.norm(normal, axis=1), 1e-300)
    flat = np.flatnonzero(np.abs(nz) > 0.5)                 # only the faces a vertical ray meets square on
    ri, z, ti = vertical_hits(V, F[flat], xy)
    into = nz[flat][ti] > 0
    order = np.lexsort((-z, ri))
    ri, into = ri[order], into[order]
    count = np.bincount(ri, minlength=n)
    k = np.arange(len(ri)) - (np.cumsum(count) - count)[ri]      # 0, 1, 2, ... down each ray
    wrong = count % 2 == 1
    wrong[ri[into != (k % 2 == 0)]] = True
    met = np.unique(count[count > 0], return_counts=True)
    return {int(a): int(b) for a, b in zip(*met)}, int(wrong.sum())
