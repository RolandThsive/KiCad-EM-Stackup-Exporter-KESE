"""The voxels: KESE's parts, cut into the board's slabs (layers.py), drawn onto PyPEEC's uniform grid.

PyPEEC solves on a grid of equal voxels: d by d in the board's plane and dz through it. A board's copper is thin
(35 um) and its layers far apart (0.7 mm and more), so the grid's z follows the copper. Every copper sheet (a slab of
trace copper) is n_cu voxel layers thick, centred on its own height, and dz is chosen so that the distance between
any two sheets is a whole number of voxels to within a micron or so (choose_dz). Each sheet's resistivity is then
scaled by its voxels' thickness over the copper's, so it keeps its sheet resistance (the scale is close to 1). The
voxel layers between two sheets stand for the heights between them, evenly: each takes the slab its height falls in,
which is a via's barrel through the board or nothing (an air gap). A via's barrel, a thin tube of plating, is drawn
as a solid column of its outer diameter: plating 25 um thick would fall between the voxels' centres, and the column
carries the same current with a negligible change to the loop.

In the plane a voxel is copper when its centre lies in the part's section: each trace is drawn as the voxels whose
centres it covers. Nothing here knows PyPEEC; pypeec_case.py turns the voxels into its input.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import shapely
from shapely.geometry import Polygon


@dataclass
class Grid:
    """The voxel grid. Lengths in mm. A voxel's linear index is ix + nx (iy + ny iz), as PyPEEC numbers them."""
    d: float                      # the voxel's size in x and y
    dz: float                     # its size in z
    x0: float                     # the grid's corner (the lowest voxel's outer corner) in x and y
    y0: float
    nx: int
    ny: int
    nz: int
    z_layer: np.ndarray = None    # the height each voxel layer stands for (its centre, in the model's real z)
    sheet_of_layer: np.ndarray = None   # the copper sheet each layer belongs to (-1: between sheets)
    sheets: list = field(default_factory=list)   # dicts: z0, z1 (real), layers (first, last), scale (rho factor)
    misfit_um: float = 0.0        # the largest error in where a sheet's centre lands (um)

    @property
    def size(self):
        return self.nx * self.ny * self.nz

    def xy_centres(self):
        x = self.x0 + (np.arange(self.nx) + 0.5) * self.d
        y = self.y0 + (np.arange(self.ny) + 0.5) * self.d
        return x, y

    def index(self, ix, iy, iz):
        return np.asarray(ix) + self.nx * (np.asarray(iy) + self.ny * np.asarray(iz))

    def ijk(self, idx):
        idx = np.asarray(idx)
        return idx % self.nx, (idx // self.nx) % self.ny, idx // (self.nx * self.ny)

    def xyz(self, idx):
        """The centre of each voxel: x and y on the grid, z the real height its layer stands for (mm)."""
        ix, iy, iz = self.ijk(idx)
        return (self.x0 + (ix + 0.5) * self.d, self.y0 + (iy + 0.5) * self.d, self.z_layer[iz])

    def summary(self):
        return dict(d_mm=self.d, dz_mm=round(self.dz, 7), n=[self.nx, self.ny, self.nz], voxels=self.size,
                    sheet_misfit_um=round(self.misfit_um, 3),
                    sheets=[dict(z_mm=[round(s['z0'], 6), round(s['z1'], 6)], layers=list(s['layers']),
                                 rho_scale=round(s['scale'], 6)) for s in self.sheets])


def copper_sheets(layout, copper_mm, factor=1.5):
    """The copper sheets of a layout: runs of touching slabs that hold copper and are thin (together at most factor
    times the copper's thickness); a slab of via barrels through the board is not one. Returns [(slab ids, z0, z1)]
    bottom to top."""
    cu = {k for p in layout.parts if p.role in ('copper', 'bridge') for k in p.polys}
    thin = [k for k, (a, b) in enumerate(layout.slabs) if k in cu and b - a <= factor * copper_mm + 1e-9]
    runs = []
    for k in thin:
        if runs and runs[-1][-1] == k - 1 and layout.slabs[k][1] - layout.slabs[runs[-1][0]][0] <= factor * copper_mm + 1e-9:
            runs[-1].append(k)
        else:
            runs.append([k])
    return [(r, layout.slabs[r[0]][0], layout.slabs[r[-1]][1]) for r in runs]


def choose_dz(centres, n_cu, thickness, lo=0.7, hi=1.3, step=1e-5, tol=1e-3):
    """The dz (mm) for sheets n_cu voxel layers thick whose centres are at `centres`: the distance from the lowest
    sheet to each other one must be a whole number of voxels, to within tol (1 um; or the least error any dz gives,
    if that is more). Of the dz from lo to hi times thickness / n_cu that keep within it, and keep at least one empty
    voxel layer between neighbouring sheets, the one nearest thickness / n_cu, so the sheets keep their thickness as
    nearly as they can. A micron in a 0.1 mm air gap moves M by about 0.1 %. Returns (dz, offsets in layers,
    error)."""
    c = np.asarray(centres, float) - centres[0]
    if len(c) == 1:                                       # one sheet: its own thickness, exactly
        return thickness / n_cu, np.zeros(1, int), 0.0
    best = []
    for dz in np.arange(lo * thickness / n_cu, hi * thickness / n_cu, step):
        k = np.rint(c / dz).astype(int)
        if np.min(np.diff(k)) < n_cu + 1:
            continue
        best.append((float(np.max(np.abs(k * dz - c))), float(dz), k))
    if not best:
        raise ValueError('no dz keeps the copper sheets apart; give a smaller thickness or n_cu')
    limit = max(tol, min(b[0] for b in best) + 5e-5)
    err, dz, k = min((b for b in best if b[0] <= limit), key=lambda b: abs(b[1] - thickness / n_cu))
    return dz, k, err


def solid(g):
    """A section with its holes filled: a via's barrel as a column."""
    polys = [Polygon(p.exterior) for p in shapely.get_parts(g) if p.geom_type == 'Polygon']
    return shapely.unary_union(polys)


def build(layout, d, copper_mm=0.035, n_cu=1, margin=1, log=print):
    """Draw every conducting part of a layout (layers.Layout, built with insulators=False) onto a grid of d (mm) in
    the plane and n_cu voxels through each copper sheet. Returns (grid, voxels): voxels maps each part's body to
    {'sheet k' or 'between': array of linear indices}, the voxels of that body in each sheet and between them."""
    sheets = copper_sheets(layout, copper_mm)
    if not sheets:
        raise ValueError('no copper sheet in the layout')
    centres = [0.5 * (a + b) for _, a, b in sheets]
    dz, k, err = choose_dz(centres, n_cu, copper_mm)
    first = n_cu // 2                                     # the lowest sheet's centre layer
    nz = first + int(k[-1]) + (n_cu - 1 - n_cu // 2) + 1
    centre_layer = first + k                              # the layer holding each sheet's centre
    z_layer = np.empty(nz)
    sheet_of = np.full(nz, -1)
    info = []
    for j, ((ids, a, b), c) in enumerate(zip(sheets, centre_layer, strict=True)):
        lo_ = c - n_cu // 2
        hi_ = lo_ + n_cu - 1
        sheet_of[lo_:hi_ + 1] = j
        z_layer[lo_:hi_ + 1] = a + (np.arange(n_cu) + 0.5) * (b - a) / n_cu
        info.append(dict(z0=a, z1=b, layers=(int(lo_), int(hi_)), slabs=ids, scale=n_cu * dz / (b - a)))
    for j in range(len(sheets) - 1):                      # between two sheets: their heights, evenly
        a, b = info[j]['layers'][1], info[j + 1]['layers'][0]
        za, zb = info[j]['z1'], info[j + 1]['z0']
        n = b - a - 1
        z_layer[a + 1:b] = za + (np.arange(n) + 0.5) * (zb - za) / n
    # the plane: every conductor's outline, one voxel of margin round it
    cond = [p for p in layout.parts if p.role in ('copper', 'bridge') and p.polys]
    bounds = np.array([g.bounds for p in cond for g in p.polys.values()])
    xmin, ymin = bounds[:, 0].min(), bounds[:, 1].min()
    xmax, ymax = bounds[:, 2].max(), bounds[:, 3].max()
    x0 = (np.floor(xmin / d) - margin) * d
    y0 = (np.floor(ymin / d) - margin) * d
    nx = int(np.ceil((xmax - x0) / d)) + margin
    ny = int(np.ceil((ymax - y0) / d)) + margin
    grid = Grid(d=d, dz=dz, x0=x0, y0=y0, nx=nx, ny=ny, nz=nz, z_layer=z_layer, sheet_of_layer=sheet_of,
                sheets=info, misfit_um=err * 1e3)
    xc, yc = grid.xy_centres()
    slab_of = []                                          # the slab each layer takes its sections from
    for iz in range(nz):
        j = sheet_of[iz]
        if j >= 0:
            ids = info[j]['slabs']
            slab_of.append(ids[len(ids) // 2])
        else:
            z = z_layer[iz]
            slab_of.append(next((s for s, (a, b) in enumerate(layout.slabs) if a < z < b), None))
    vox = {}
    for p in cond:
        for iz in range(nz):
            s = slab_of[iz]
            g = p.polys.get(s) if s is not None else None
            if g is None:
                continue
            if sheet_of[iz] < 0:
                g = solid(g)
            bx0, by0, bx1, by1 = g.bounds
            i0, i1 = np.searchsorted(xc, bx0), np.searchsorted(xc, bx1, side='right')
            j0, j1 = np.searchsorted(yc, by0), np.searchsorted(yc, by1, side='right')
            if i1 <= i0 or j1 <= j0:
                continue
            X, Y = np.meshgrid(xc[i0:i1], yc[j0:j1], indexing='ij')
            ix, iy = np.nonzero(shapely.contains_xy(g, X, Y))
            if not len(ix):
                continue
            key = f'sheet {sheet_of[iz]}' if sheet_of[iz] >= 0 else 'between'
            vox.setdefault(p.body, {}).setdefault(key, []).append(grid.index(ix + i0, iy + j0, iz))
    out = {b: {k: np.unique(np.concatenate(v)) for k, v in kv.items()} for b, kv in vox.items()}
    claimed = np.concatenate([a for kv in out.values() for a in kv.values()])
    if len(np.unique(claimed)) != len(claimed):
        raise ValueError('two conductors claim the same voxel: their copper is closer than a voxel (use a smaller d)')
    log(f'voxels: d {d * 1e3:g} um, dz {dz * 1e3:.3f} um ({n_cu} through each of {len(info)} copper sheets, centres '
        f'within {err * 1e3:.2f} um), grid {nx} x {ny} x {nz} = {grid.size / 1e6:.2f} M, copper voxels '
        + ', '.join(f'{b} {sum(len(a) for a in kv.values())}' for b, kv in out.items()))
    return grid, out


def flat(v):
    """All the voxels of one body, whatever sheet."""
    return np.unique(np.concatenate(list(v.values()))) if v else np.zeros(0, int)
