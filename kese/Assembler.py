"""Step 5 - Assembler: one in-memory Model from the prisms: meshes per part (closed solids in
"simulation" mode, the visible skin in "visual" mode), output units and orientation, materials and
properties.  The Packager writes every file format from this Model; nothing is rebuilt per format."""
import numpy as np
import shapely
import trimesh

from kese.Common import shapes as sh
from kese.Common.prisms import Model
from kese.Geometry.Skin import skin_meshes
from parameters import P

PART_ORDER = ["Board", "Copper", "Plating", "Top Solder Mask", "Top Mask over Copper", "Bottom Solder Mask",
              "Bottom Mask over Copper", "Top Silkscreen", "Bottom Silkscreen", "Top Finish", "Bottom Finish"]


def output_transform():
    """4x4: board frame (mm, Y up, F.Cu toward +Z) -> output units and orientation."""
    R = P.Run
    scale = 1.0 if R.UNITS == "mm" else 0.001
    if R.ORIENTATION == "flat":      # board in XZ, F.Cu toward +Y
        rot = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], dtype=float)
    else:
        rot = np.eye(4)
    return np.diag([scale, scale, scale, 1.0]) @ rot


def rank(name):
    for i, prefix in enumerate(PART_ORDER):
        if name == prefix or name.startswith(prefix + "_") or name.startswith(prefix + " "):
            return (i, name)
    return (len(PART_ORDER), name)


def _finish_mesh(mesh, mat):
    # merge vertices two decades below the snap grid, then drop only faces that collapsed onto a
    # repeated vertex (zero-area triangles with three distinct vertices stay: the union needs them)
    digits = int(round(-np.log10(P.Geometry.SNAP_GRID_MM))) + 2
    mesh.merge_vertices(digits_vertex=digits)
    f = mesh.faces
    mesh.update_faces((f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2]))
    mesh.remove_unreferenced_vertices()
    if not len(mesh.faces):
        return None
    mesh.apply_transform(mat)
    mesh = trimesh.graph.smooth_shade(mesh, angle=np.radians(P.Run.SMOOTH_SHADE_ANGLE_DEG))
    normals = np.array(mesh.vertex_normals)
    bad = np.linalg.norm(normals, axis=1) < 0.5
    if bad.any():
        normals[bad] = [0.0, 0.0, 1.0]
        mesh.vertex_normals = normals
    return mesh


def _part_regions(prisms):
    """The 2D regions of one part, prepared so their solids union cleanly:
    - where two regions touch, each gets the other's boundary vertices (no T-junctions, so the
      shared faces are exactly coplanar);
    - regions that touch only at a point while overlapping in z would meet along a single edge in
      3D and are parted by Geometry.PINCH_POINT_OPENING_MM, as polygons() does inside one polygon."""
    regions = [p.region for p in prisms]
    grid = P.Geometry.SNAP_GRID_MM
    for i in range(len(prisms)):
        for j in range(i + 1, len(prisms)):
            if prisms[i].z1 <= prisms[j].z0 or prisms[j].z1 <= prisms[i].z0 or not regions[i].intersects(regions[j]):
                continue
            regions[i] = sh.polys_only(shapely.snap(regions[i], regions[j], grid / 2))
            regions[j] = sh.polys_only(shapely.snap(regions[j], regions[i], grid / 2))
            touch = regions[i].intersection(regions[j])
            if touch.is_empty or not all(g.geom_type == "Point" for g in getattr(touch, "geoms", [touch])):
                continue
            k = j if regions[j].area <= regions[i].area else i
            regions[k] = sh.polys_only(regions[k].difference(touch.buffer(P.Geometry.PINCH_POINT_OPENING_MM, quad_segs=1)))
    return regions


def assemble(name, mode, ps, materials, log):
    mat = output_transform()
    meshes = {}
    if mode == "visual":
        raw = skin_meshes(ps)
    else:
        raw = {}
        for part, prisms in ps.by_part().items():
            regions = _part_regions(prisms)
            solids = [m for m in (sh.extrude(r, p.z0, p.z1) for r, p in zip(regions, prisms)) if m is not None]
            raw[part] = sh.solid_union(solids, log=lambda s: log(f"{part}: {s}"))
    for part in sorted(raw, key=rank):
        m = raw[part]
        if m is None:
            continue
        m = _finish_mesh(m, mat)
        if m is not None:
            meshes[part] = m
    props = {}
    for part, prisms in ps.by_part().items():
        p0 = prisms[0]
        pr = dict(p0.props)
        pr.update({"role": p0.role, "layer": p0.layer, "net": p0.net,
                   "z_min_mm": round(min(p.z0 for p in prisms), 6), "z_max_mm": round(max(p.z1 for p in prisms), 6),
                   "prisms": len(prisms)})
        props[part] = pr
    return Model(name=name, mode=mode, prismset=ps, meshes=meshes, materials=materials, props=props,
                 transform=mat, units=P.Run.UNITS, report=[])
