"""The overlap check of stage 8 in simulation mode: no two parts share material.  Every part is
built from flat regions between two heights: its slices (kese/core/boundary.py), or its prisms
when the solids were built with a kernel (Run.BUILD_WITH_KERNELS).  So two parts overlap exactly
where a slice of one and a slice of the other overlap in height and their regions share an area,
and every pair of them is looked at.  Each polygon is shrunk by a grid step first
(Geometry.SNAP_GRID_MM): parts that only touch, along an edge or across the grid step that sharing
vertices may bend an edge by, then no longer meet.  An R-tree gives the polygons whose boxes
meet; of those from different parts at overlapping heights, the shrunk polygons are tested, the
one with more vertices prepared (a laminate full of holes is tested once against an index)."""
import numpy as np
import shapely

from kese.core import shapes2d as sh
from parameters import P

HEIGHT_TOLERANCE_MM = 1e-9       # heights are told apart to 1e-9 mm, a picometre (kese/core/boundary.py)


def slices_of(model):
    """[(part, z0, z1, region)] in mm and board coordinates."""
    if model.boundaries:
        return [(part, z0, z1, region) for part, b in model.boundaries.items() for z0, z1, region in b.slices]
    return [(p.part, p.z0, p.z1, p.region) for p in model.prismset.prisms]


def overlaps(model):
    """[(volume mm3, part, other part, z0, z1)] of every two slices of different parts that share
    material, the biggest first."""
    rows = slices_of(model)
    owner, polys = [], []
    for k, (_, _, _, region) in enumerate(rows):
        for poly in sh.polygons(region):
            owner.append(k)
            polys.append(poly)
    if not polys:
        return []
    owner, polys = np.array(owner), np.array(polys, dtype=object)
    i, j = shapely.STRtree(polys).query(polys)                      # boxes that meet
    part = np.unique([r[0] for r in rows], return_inverse=True)[1]
    z0, z1 = np.array([r[1] for r in rows]), np.array([r[2] for r in rows])
    dz = np.minimum(z1[owner[i]], z1[owner[j]]) - np.maximum(z0[owner[i]], z0[owner[j]])
    keep = (i < j) & (part[owner[i]] != part[owner[j]]) & (dz > HEIGHT_TOLERANCE_MM)
    i, j, dz = i[keep], j[keep], dz[keep]
    first = shapely.get_num_coordinates(polys[i]) >= shapely.get_num_coordinates(polys[j])
    i, j = np.where(first, i, j), np.where(first, j, i)            # the one with more vertices first
    shrunk = np.empty(len(polys), dtype=object)
    used = np.unique(np.r_[i, j])
    shrunk[used] = shapely.buffer(polys[used], -P.Geometry.SNAP_GRID_MM, join_style="mitre")
    shapely.prepare(shrunk[np.unique(i)])
    meet = shapely.intersects(shrunk[i], shrunk[j])
    found = [(polys[p].intersection(polys[q]).area * h, rows[owner[p]][0], rows[owner[q]][0],
              max(z0[owner[p]], z0[owner[q]]), min(z1[owner[p]], z1[owner[q]]))
             for p, q, h in zip(i[meet], j[meet], dz[meet])]
    return sorted(found, key=lambda f: -f[0])
