"""A coil's port in the voxels: where it is opened, and its two terminals.

A coil is opened at a gap: a region with no copper of the coil in it, either cut out here (the space across a cut
trace, a via's barrel left out) or already in the board (two trace ends stacked on two layers). Its terminals are
the coil's voxels that border the gap, in two separate groups, one each side. pypeec_case.py drives a current into
one terminal and takes it out of the other, so the coil's voltage is the voltage between them.
"""
from __future__ import annotations

import numpy as np
import shapely

from .voxels import flat


def _inside(grid, idx, region, z0, z1, tol=1e-6):
    x, y, z = grid.xyz(idx)
    return shapely.contains_xy(region, x, y) & (z > z0 - tol) & (z < z1 + tol)


def cut(grid, vox, body, region, z0, z1):
    """Take the voxels of `body` whose centres lie in region (shapely, in the plane) between heights z0 and z1 out
    of it: the gap that opens the coil. Returns how many were taken."""
    n = 0
    for k, idx in vox[body].items():
        keep = ~_inside(grid, idx, region, z0, z1)
        n += int((~keep).sum())
        vox[body][k] = idx[keep]
    return n


def groups(grid, idx, corners=False):
    """Split voxels into the groups that touch face to face (corners=True: or edge or corner). Returns a list of
    index arrays."""
    idx = np.asarray(idx)
    pos = {int(v): i for i, v in enumerate(idx)}
    ix, iy, iz = grid.ijk(idx)
    label = -np.ones(len(idx), int)
    steps = ([(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1) if (a, b, c) != (0, 0, 0)]
             if corners else [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
    n = 0
    for s in range(len(idx)):
        if label[s] >= 0:
            continue
        label[s] = n
        stack = [s]
        while stack:
            i = stack.pop()
            for dx, dy, dz in steps:
                a, b, c = ix[i] + dx, iy[i] + dy, iz[i] + dz
                if 0 <= a < grid.nx and 0 <= b < grid.ny and 0 <= c < grid.nz:
                    j = pos.get(int(grid.index(a, b, c)))
                    if j is not None and label[j] < 0:
                        label[j] = n
                        stack.append(j)
        n += 1
    return [idx[label == g] for g in range(n)]


def terminals(grid, vox, body, region, z0, z1, tol=1e-6):
    """The two terminals of `body` at a gap: the gap's cells are the grid cells whose centres lie in region (in the
    plane) between heights z0 and z1 and hold none of the body's copper, and a terminal voxel is one of the body's
    that shares a face with a gap cell: the copper faces that border the gap.
    They must fall in exactly two groups (touching at a face, an edge or a corner). They are taken out of the body's
    own voxels (a terminal is a domain of its own in PyPEEC) and returned ordered by the mean of (x, y, z), so a
    coil's sense follows from where its terminals sit."""
    allv = flat(vox[body])
    own = set(allv.tolist())
    near = region.buffer(1.5 * max(grid.d, grid.dz))
    x, y, _ = grid.xyz(allv)
    cand = allv[shapely.contains_xy(near, x, y)]
    ix, iy, iz = grid.ijk(cand)
    hit = np.zeros(len(cand), bool)
    for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
        a, b, c = ix + dx, iy + dy, iz + dz
        ok = (a >= 0) & (a < grid.nx) & (b >= 0) & (b < grid.ny) & (c >= 0) & (c < grid.nz)
        nb = grid.index(np.where(ok, a, 0), np.where(ok, b, 0), np.where(ok, c, 0))
        free = ok & ~np.isin(nb, list(own))
        if free.any():
            xs, ys, zs = grid.xyz(nb[free])
            inside = shapely.contains_xy(region, xs, ys) & (zs > z0 - tol) & (zs < z1 + tol)
            hit[np.flatnonzero(free)[inside]] = True
    g = groups(grid, cand[hit], corners=True)
    if len(g) != 2:
        raise ValueError(f'{body} borders its gap in {len(g)} places, not 2: the gap does not open it into one '
                         'conductor')
    cen = [np.mean(np.vstack(grid.xyz(a)), axis=1) for a in g]
    order = sorted(range(2), key=lambda i: tuple(np.round(cen[i], 6)))
    t = [g[i] for i in order]
    both = np.concatenate(t)
    for k, idx in vox[body].items():
        vox[body][k] = np.setdiff1d(idx, both)
    return t


def connected(grid, vox, body):
    """Whether the voxels of `body`, with its terminals still in, are one piece."""
    return len(groups(grid, flat(vox[body]))) == 1
