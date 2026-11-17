"""KESE's solids cut into the board's layers: the parts, their sections, and the slabs they make.

A KiCad board is layered: every solid KESE writes is a stack of prisms, flat at a few heights. So the model is cut
into slabs at every height any part has, and each part is sectioned in the middle of each slab it spans. The voxels
(voxels.py) are drawn from those sections. The same code as the Elmer branch's mesh25d.py, which builds its prism
mesh from the same slabs; this branch needs no mesh, so it keeps only the parts and their sections.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import shapely
from shapely.geometry import Polygon

ROUND = 7                                                     # decimals of a mm kept when sectioning (0.1 nm)


# --------------------------------------------------------------------------------------------- the parts

@dataclass
class Part:
    """One solid: a name, its body name in the mesh, and its triangle surface (trimesh) in model coordinates."""
    name: str
    body: str
    role: str                 # copper, board, mask, bridge, or void (air that overrides copper: a via left out)
    mesh: object = None       # trimesh.Trimesh, closed
    priority: int = 0         # where two parts claim one wedge, the higher one wins (copper over mask over board)
    polys: dict = field(default_factory=dict)       # slab index -> shapely geometry of its section there
    fixed: dict = field(default_factory=dict)       # (z0, z1) -> geometry: a part given in 2D (a bridge), not cut

    @property
    def zrange(self):
        if self.mesh is not None:                     # STL is single precision: heights to 1e-6 mm
            return round(float(self.mesh.bounds[0][2]), 6), round(float(self.mesh.bounds[1][2]), 6)
        zs = [z for k in self.fixed for z in k]
        return min(zs), max(zs)

    def levels(self):
        if self.mesh is not None:
            return set(np.round(self.mesh.vertices[:, 2], 6).tolist())
        return {round(z, 6) for k in self.fixed for z in k}


def even_odd(rings):
    """The region inside an odd number of the closed rings: a section's copper with its holes."""
    polys = [Polygon(r) for r in rings if len(r) >= 4]
    polys = [p if p.is_valid else p.buffer(0) for p in polys]
    polys = [p for p in polys if not p.is_empty and p.area > 1e-12]
    if not polys:
        return None
    g = shapely.symmetric_difference_all(polys)
    g = shapely.make_valid(g)
    g = shapely.unary_union([p for p in shapely.get_parts(g) if p.geom_type == 'Polygon'])
    return None if g.is_empty else g


def section(mesh, z):
    """The part's cross-section at height z, as shapely geometry (None where it has none)."""
    import trimesh
    lines = trimesh.intersections.mesh_plane(mesh, [0, 0, 1], [0, 0, z])
    if len(lines) == 0:
        return None
    segs = np.round(lines[:, :, :2], ROUND)
    segs = segs[np.any(segs[:, 0] != segs[:, 1], axis=1)]
    merged = shapely.line_merge(shapely.MultiLineString(list(segs)))
    rings = [np.asarray(g.coords) for g in shapely.get_parts(merged) if g.is_closed]
    return even_odd(rings)


# --------------------------------------------------------------------------------------------- the layout

@dataclass
class Layout:
    parts: list
    slabs: list = field(default_factory=list)       # [(z0, z1)] bottom to top, inside the parts' heights

    def build(self, log=print, merge_outside=True, insulators=True):
        """Section every part in every slab it spans. merge_outside: a board or mask part lying wholly outside
        the copper's span of heights (the FR-4 behind a one-sided board, the mask on its far side) is left out:
        in Elmer it is air in all but name (sigma 0, mu_r 1), and leaving it out keeps its layers out of the
        wedges. insulators=False leaves out every board and mask part: for the magneto-quasi-static solve an
        insulator with mu_r 1 is air (the A-V solver has no displacement current, so eps_r plays no part), and
        their heights then add no layers. The parts left out are listed in self.merged."""
        self.merged = []
        if not insulators:
            self.merged = [p.name for p in self.parts if p.role in ('board', 'mask')]
            self.parts = [p for p in self.parts if p.role not in ('board', 'mask')]
        elif merge_outside:
            cu = [p.zrange for p in self.parts if p.role in ('copper', 'bridge')]
            spans = _merge_spans(cu)
            keep = []
            for p in self.parts:
                lo, hi = p.zrange
                if p.role in ('copper', 'bridge'):
                    keep.append(p)
                    continue
                touch = 1e-6 if p.role == 'mask' else -1e-6        # a mask may just touch the copper
                if any(lo < b + touch and hi > a - touch for a, b in spans):
                    keep.append(p)
                else:
                    self.merged.append(p.name)
            self.parts = keep
        zs = sorted({z for p in self.parts for z in p.levels()})
        self.slabs = [(a, b) for a, b in zip(zs[:-1], zs[1:]) if b - a > 1e-7]
        for p in self.parts:
            lo, hi = p.zrange
            for k, (a, b) in enumerate(self.slabs):
                if a < lo - 1e-6 or b > hi + 1e-6:
                    continue
                if p.mesh is not None:
                    g = section(p.mesh, 0.5 * (a + b))
                else:
                    g = next((geo for (z0, z1), geo in p.fixed.items() if z0 - 1e-6 <= a and b <= z1 + 1e-6), None)
                if g is not None and not g.is_empty:
                    p.polys[k] = g
        log(f'layout: {len(self.parts)} parts, {len(self.slabs)} slabs from z {zs[0]:.4f} to {zs[-1]:.4f} mm'
            + (f'; merged into the air: {", ".join(self.merged)}' if self.merged else ''))
        return self


def _merge_spans(ranges):
    out = []
    for a, b in sorted(ranges):
        if out and a <= out[-1][1] + 1e-6:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out
