"""A 2.5D prism mesh for Elmer, built from KESE's export.

A KiCad board is layered: every solid KESE writes is a stack of prisms, flat at a few heights. So the model is
cut into slabs at every height any part has, each part is sectioned in the middle of each slab it spans, and one
triangle mesh is made of the whole domain with every copper edge of every slab as a line of it. That triangle
mesh is swept through all the slabs as wedges (Elmer's 706 elements), each wedge given the body whose section
holds its triangle's centre. Copper slabs get several wedge layers through their thickness, so the skin depth is
resolved; a few wedge layers of air sit above and below, then tetrahedra take over.

Because every slab shares one triangle mesh, a part that only moves in its own slabs (the rotor turning between
runs) can have every one of its positions drawn into the triangle mesh at once: then the mesh is the same at
every rotor angle and only the rotor's wedges change body. The stator's mesh is identical in every run.

No 3D Booleans: the wedges follow the layers exactly, where tetrahedra through 35 um copper and a 1.6 mm board
would number in the tens of millions. Tetrahedra fill only the air above and below the wedge block, out to the
domain's top and bottom, growing away from it.

The same idea as the layered mesh of kicad2ems-fem (github.com/lowprocess/kicad2ems-fem, elmer/layered.py),
which sweeps a board's triangles through its stack for DC and heat; this one adds the air, several layers
through the copper, the rotor and the terminals, and takes its geometry from KESE's solids.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.polygon import orient

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
    region: Polygon                 # the domain's footprint (a disc round the axis)
    zbox: tuple                     # (z bottom, z top) of the air domain
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


# --------------------------------------------------------------------------------------------- 2D mesh

def _rings(g):
    for p in shapely.get_parts(g):
        if p.geom_type == 'Polygon' and not p.is_empty:
            yield p.exterior
            yield from p.interiors


def disc(centre, radius, h=None, n=None):
    """The domain's footprint: a regular polygon round centre. Give h (mm), the mesh size at the rim, and its
    sides are about h long, so the side band and the air's tetrahedra meet it at their own size (a fine rim
    under coarse tetrahedra makes slivers); or give n sides."""
    if n is None:
        n = max(32, int(math.ceil(2 * math.pi * radius / h))) if h else 256
    a = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return Polygon(np.c_[centre[0] + radius * np.cos(a), centre[1] + radius * np.sin(a)])


def size_raster(fine_geoms, region, h_edge, h_in, h_max, grade, box_margin):
    """The element size wanted, as a raster lookup: h_edge at copper edges, growing by `grade` per mm away from
    them, at most h_in inside copper and h_max outside. Returns size(x, y)."""
    from scipy import ndimage
    fine = shapely.unary_union(fine_geoms)
    x0, y0, x1, y1 = fine.bounds
    x0, y0, x1, y1 = x0 - box_margin, y0 - box_margin, x1 + box_margin, y1 + box_margin
    step = max(0.5 * h_edge, max(x1 - x0, y1 - y0) / 3000.0)
    gx = np.arange(x0, x1 + step, step)
    gy = np.arange(y0, y1 + step, step)
    X, Y = np.meshgrid(gx, gy)
    inside = shapely.contains_xy(fine, X, Y)
    edge = inside ^ ndimage.binary_erosion(inside)
    edge |= ndimage.binary_dilation(inside) ^ inside
    d = ndimage.distance_transform_edt(~edge) * step
    out = np.clip(h_edge + grade * d, h_edge, h_max)
    out = np.where(inside, np.minimum(out, h_in), out)

    def size(x, y):
        if x < x0 or x > x1 or y < y0 or y > y1:
            dx = max(x0 - x, 0.0, x - x1)
            dy = max(y0 - y, 0.0, y - y1)
            return float(min(h_max, h_edge + grade * (box_margin + math.hypot(dx, dy))))
        i = min(int((y - y0) / step), len(gy) - 1)
        j = min(int((x - x0) / step), len(gx) - 1)
        return float(out[i, j])
    return size


def triangulate(region, lines, size, grid, log=print):
    """Triangles of `region` with every segment of `lines` (noded) as an edge. Returns xy [n, 2], tri [m, 3]
    counter-clockwise, and the region's boundary edges as node pairs."""
    import gmsh
    gmsh.initialize()
    try:
        gmsh.option.setNumber('General.Terminal', 0)
        gmsh.model.add('layout')
        geo = gmsh.model.geo
        pts, segs = {}, {}

        def point(c):
            k = (round(c[0] / grid), round(c[1] / grid))
            if k not in pts:
                pts[k] = geo.addPoint(k[0] * grid, k[1] * grid, 0.0)
            return pts[k]

        def seg(a, b):
            a, b = point(a), point(b)
            if a == b:
                return None
            k = (min(a, b), max(a, b))
            if k not in segs:
                segs[k] = geo.addLine(*k)
            return segs[k] if a < b else -segs[k]

        ring = list(orient(region, 1.0).exterior.coords)[:-1]
        loop = [s for s in (seg(ring[i], ring[(i + 1) % len(ring)]) for i in range(len(ring))) if s]
        outer = {abs(s) for s in loop}
        surface = geo.addPlaneSurface([geo.addCurveLoop(loop)])
        inner = set()
        for l in lines:
            c = list(l.coords)
            for a, b in zip(c[:-1], c[1:]):
                s = seg(a, b)
                if s and abs(s) not in outer:
                    inner.add(abs(s))
        geo.synchronize()
        if inner:
            gmsh.model.mesh.embed(1, sorted(inner), 2, surface)
        gmsh.model.mesh.setSizeCallback(lambda dim, tag, x, y, z, lc: size(x, y))
        for k, v in {'Mesh.MeshSizeExtendFromBoundary': 0, 'Mesh.MeshSizeFromPoints': 0,
                     'Mesh.MeshSizeFromCurvature': 0, 'Mesh.Algorithm': 6}.items():
            gmsh.option.setNumber(k, v)
        log(f'2D mesh: {len(pts):,} points, {len(inner):,} embedded segments')
        gmsh.model.mesh.generate(2)
        tags, xyz, _ = gmsh.model.mesh.getNodes()
        tri = gmsh.model.mesh.getElementsByType(2)[1].reshape(-1, 3).astype(np.int64)
    finally:
        gmsh.finalize()
    where = np.full(int(tags.max()) + 1, -1)
    where[tags.astype(np.int64)] = np.arange(len(tags))
    used = np.unique(tri)
    index = np.full(int(tags.max()) + 1, -1)
    index[used] = np.arange(len(used))
    xy = xyz.reshape(-1, 3)[where[used], :2]
    tri = index[tri]
    a, b, c = xy[tri[:, 0]], xy[tri[:, 1]], xy[tri[:, 2]]
    flip = (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]) < 0
    tri[flip] = tri[flip][:, [0, 2, 1]]
    return xy, tri


# --------------------------------------------------------------------------------------------- the mesh

@dataclass
class Settings:
    h_edge: float = 0.03          # mm, at copper edges
    h_in: float = 0.10            # mm, at most inside copper
    h_max: float = 4.0            # mm, at most anywhere
    grade: float = 0.3            # mm of size per mm of distance from copper
    box_margin: float = 2.0       # mm round the copper where the size raster is kept
    grid: float = 0.0005          # mm, the plane's snap grid for the noded lines
    simplify: float = 0.0005      # mm, copper outlines simplified this much before meshing
    dz_copper: float = 0.012      # mm, the thickest wedge layer in a slab with copper (delta / 3 at 3.5 MHz)
    dz_max: float = 0.25          # mm, the thickest wedge layer elsewhere in the board and the gap
    foil_max: float = 0.15        # mm, the thickest slab still treated as a copper foil (thicker: vias only)
    pads: tuple = (0.03, 0.08)    # mm, wedge layers of air above and below the boards, before the tetrahedra
    tet_max: float = 8.0          # mm, the largest tetrahedron in the air
    tet_grade: float = 0.7        # mm of tetrahedron size per mm of height above (below) the wedges


def _levels(layout, st, copper_slabs):
    """The z of every wedge level, bottom to top, and for each layer the slab it lies in (-1: air)."""
    lo, hi = layout.slabs[0][0], layout.slabs[-1][1]
    zs = [lo - sum(st.pads[:i]) for i in range(len(st.pads), 0, -1)]
    slab_of = [-1] * len(st.pads)
    for k, (a, b) in enumerate(layout.slabs):
        dz = st.dz_copper if k in copper_slabs else st.dz_max
        n = max(1, int(math.ceil((b - a) / dz - 1e-9)))
        for i in range(n):
            zs.append(a + (b - a) * i / n)
            slab_of.append(k)
    zs += [hi + sum(st.pads[:i]) for i in range(len(st.pads) + 1)]
    slab_of += [-1] * len(st.pads)
    return np.array(zs), np.array(slab_of)


def boundary_loop(tri):
    """The triangle mesh's outer boundary as one ordered loop of node indices, counter-clockwise."""
    e = np.vstack([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]])
    key = np.sort(e, axis=1)
    _, inv, cnt = np.unique(key, axis=0, return_inverse=True, return_counts=True)
    b = e[cnt[inv.ravel()] == 1]                       # directed as in their (counter-clockwise) triangle
    nxt = dict(zip(b[:, 0].tolist(), b[:, 1].tolist()))
    loop = [int(b[0, 0])]
    while True:
        n = nxt[loop[-1]]
        if n == loop[0]:
            break
        loop.append(n)
    if len(loop) != len(b):
        raise RuntimeError('the 2D mesh has more than one boundary loop')
    return np.array(loop)


def cap_mesh(ring_xy, h):
    """A 2D triangle mesh of the polygon `ring_xy` (counter-clockwise) keeping exactly its points on the
    boundary. Returns (xy of the new inner points, triangles indexing ring points then inner points)."""
    import gmsh
    gmsh.initialize()
    try:
        gmsh.option.setNumber('General.Terminal', 0)
        gmsh.model.add('cap')
        geo = gmsh.model.geo
        pts = [geo.addPoint(x, y, 0.0, h) for x, y in ring_xy]
        n = len(pts)
        lines = [geo.addLine(pts[i], pts[(i + 1) % n]) for i in range(n)]
        surf = geo.addPlaneSurface([geo.addCurveLoop(lines)])
        geo.synchronize()
        for l in lines:
            gmsh.model.mesh.setTransfiniteCurve(l, 2)
        gmsh.option.setNumber('Mesh.MeshSizeMax', h)
        gmsh.option.setNumber('Mesh.Algorithm', 6)
        gmsh.model.mesh.generate(2)
        tags, xyz, _ = gmsh.model.mesh.getNodes()
        tri = gmsh.model.mesh.getElementsByType(2)[1].reshape(-1, 3).astype(np.int64)
        ptag = {}
        for i, p in enumerate(pts):
            t, _, _ = gmsh.model.mesh.getNodes(0, p)
            ptag[int(t[0])] = i
    finally:
        gmsh.finalize()
    xyz = xyz.reshape(-1, 3)
    index, inner = {}, []
    for t, c in zip(tags.astype(np.int64).tolist(), xyz):
        if t in ptag:
            index[t] = ptag[t]
        else:
            index[t] = n + len(inner)
            inner.append(c[:2])
    tri = np.vectorize(index.get)(tri)
    return np.array(inner).reshape(-1, 2), tri


def tet_fill(nodes, tris, h_max, size=None, log=print):
    """Tetrahedra filling the closed surface `tris` (indices into `nodes` [n, 3]). Returns (new nodes [m, 3],
    tetrahedra [k, 4] indexing nodes then the new ones)."""
    import gmsh
    used = np.unique(tris)
    local = np.full(len(nodes), -1, np.int64)
    local[used] = np.arange(len(used))
    gmsh.initialize()
    try:
        gmsh.option.setNumber('General.Terminal', 0)
        gmsh.model.add('air')
        gmsh.model.addDiscreteEntity(2, 1)
        gmsh.model.mesh.addNodes(2, 1, (np.arange(len(used)) + 1).tolist(), nodes[used].ravel().tolist())
        gmsh.model.mesh.addElements(2, 1, [2], [(np.arange(len(tris)) + 1).tolist()],
                                    [(local[tris] + 1).ravel().tolist()])
        sl = gmsh.model.geo.addSurfaceLoop([1])
        vol = gmsh.model.geo.addVolume([sl])
        gmsh.model.geo.synchronize()
        gmsh.option.setNumber('Mesh.MeshSizeMax', h_max)
        if size is not None:
            gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)
            gmsh.model.mesh.setSizeCallback(lambda dim, tag, x, y, z, lc: size(x, y, z))
        gmsh.option.setNumber('Mesh.Algorithm3D', 1)
        gmsh.option.setNumber('Mesh.Optimize', 1)
        gmsh.model.mesh.generate(3)
        # slivers (four nearly coplanar corners) stall the iterative solvers of the edge-element system: Netgen's
        # optimiser swaps and smooths them away without touching the surface
        gmsh.model.mesh.optimize('Netgen')
        gmsh.model.mesh.optimize('')
        tags, xyz, _ = gmsh.model.mesh.getNodes(3, vol)
        et, en = gmsh.model.mesh.getElementsByType(4)
    finally:
        gmsh.finalize()
    tags = tags.astype(np.int64)
    if len(tags) and tags.min() <= len(used):
        raise RuntimeError('gmsh reused a surface node number')
    back = np.zeros(len(used) + len(tags) + 2, np.int64)
    back[1:len(used) + 1] = used
    tet = en.astype(np.int64).reshape(-1, 4)
    order = np.argsort(tags)
    new_index = np.full(int(tags.max()) + 1 if len(tags) else 1, -1, np.int64)
    new_index[tags] = len(nodes) + np.arange(len(tags))
    out = np.where(tet <= len(used), back[np.minimum(tet, len(used))], new_index[np.minimum(tet, len(new_index) - 1)])
    if (out < 0).any():
        raise RuntimeError('a tetrahedron names an unknown node')
    return xyz.reshape(-1, 3), out


def _label(layout, cen, slab_of, names=None):
    """The body of every wedge: in each slab, the part of highest priority whose section holds the triangle's
    centre (later parts win ties), air elsewhere. Returns (names, body [layers, triangles])."""
    nt = len(cen)
    names = list(names) if names else ['AIR']
    body_of_slab = np.zeros((len(layout.slabs), nt), np.int32)
    best = np.full((len(layout.slabs), nt), -1, np.int32)
    for p in sorted(layout.parts, key=lambda p: p.priority):
        if p.body not in names:
            names.append(p.body)
        b = names.index(p.body)
        for k, g in p.polys.items():
            hit = shapely.contains_xy(g, cen[:, 0], cen[:, 1])
            win = hit & (p.priority >= best[k])
            body_of_slab[k, win] = b
            best[k, win] = p.priority
    body = np.zeros((len(slab_of), nt), np.int32)
    for k, s in enumerate(slab_of):
        if s >= 0:
            body[k] = body_of_slab[s]
    return names, body


def relabel(m, layout, log=print):
    """The mesh m with its wedges' bodies taken from another layout of the same slabs: the rotor turned to a
    new angle, when every angle's outline was drawn into the triangle mesh (extra_lines). The nodes and
    elements are untouched, so every angle is solved on one mesh. Body names keep their numbers."""
    old = m['layout']
    if [tuple(np.round(s, 6)) for s in old.slabs] != [tuple(np.round(s, 6)) for s in layout.slabs]:
        raise ValueError('the new layout has other slabs: its parts moved in z')
    cen = m['xy'][m['tri']].mean(axis=1)
    names, body = _label(layout, cen, m['slab_of'], names=m['names'])
    out = dict(m)
    out.update(names=names, body_layers=body, body=body.reshape(-1), layout=layout)
    log(f'relabelled: ' + ', '.join(f'{n} {int((body == i).sum()):,}' for i, n in enumerate(names)))
    return out


def build_mesh(layout, st=Settings(), extra_lines=(), extra_fine=(), log=print):
    """The mesh of the layout: wedges through the boards (one triangle mesh of the whole footprint, every copper
    edge of every slab in it), a few wedge layers of air above and below, then tetrahedra out to the domain's top
    and bottom. extra_lines: lines drawn into the triangle mesh (port sheets, a rotor's outline at other
    angles). extra_fine: shapes meshed as finely as copper (the rotor's copper at other angles), so that a
    relabelled mesh is as fine at the rotor's edges at every angle. Returns dict(nodes, cells, names, ...)."""
    copper_parts = [p for p in layout.parts if p.role in ('copper', 'bridge')]
    # a slab gets the thin copper layers only where it is a copper foil: a slab through the board that holds copper
    # only as via barrels carries its current along z, where the skin depth plays no part in the layers' height
    copper_slabs = {k for p in copper_parts for k in p.polys
                    if layout.slabs[k][1] - layout.slabs[k][0] <= st.foil_max + 1e-9}
    rings, fine = [], []
    for p in layout.parts:
        for k, g in p.polys.items():
            if p.role in ('copper', 'bridge'):
                g2 = g.simplify(st.simplify) if st.simplify else g
                rings += [LineString(r.coords) for r in _rings(g2)]
                fine.append(g2)
            elif p.role == 'board':
                rings += [LineString(r.coords) for r in _rings(g.simplify(10 * st.grid))]
    rings += [l if isinstance(l, LineString) else LineString(l.coords) for l in extra_lines]
    rings.append(LineString(orient(layout.region, 1.0).exterior.coords))
    noded = shapely.unary_union(rings, grid_size=st.grid)
    lines = [l for l in shapely.get_parts(noded) if l.geom_type == 'LineString']
    region = shapely.set_precision(layout.region, st.grid)
    keep = region.buffer(st.grid)
    lines = [l for l in lines if keep.covers(l)]
    fine += [g.simplify(st.simplify) if st.simplify else g for g in extra_fine]
    size = size_raster(fine, layout.region, st.h_edge, st.h_in, st.h_max, st.grade, st.box_margin)
    xy, tri = triangulate(region, lines, size, st.grid, log)
    nt, n2 = len(tri), len(xy)
    cen = xy[tri].mean(axis=1)
    log(f'2D mesh: {nt:,} triangles, {n2:,} nodes')

    levels, slab_of = _levels(layout, st, copper_slabs)
    nk = len(levels) - 1
    names, body = _label(layout, cen, slab_of)
    nodes = np.c_[np.tile(xy, (nk + 1, 1)), np.repeat(levels, n2)]
    wk = np.repeat(np.arange(nk), nt)
    wt = np.tile(np.arange(nt), nk)
    wedges = np.c_[tri[wt] + wk[:, None] * n2, tri[wt] + (wk[:, None] + 1) * n2]
    log(f'wedges: {len(wedges):,} in {nk} layers')

    # the air above and below: tetrahedra inside the wedges' top (bottom) face, a side band and a cap
    loop = boundary_loop(tri)
    ring_xy = xy[loop]
    seg = np.hypot(*(np.roll(ring_xy, -1, axis=0) - ring_xy).T).mean()
    cap_inner, cap_tri = cap_mesh(ring_xy, max(seg, st.tet_max))
    z0, z1 = layout.zbox
    tets, tet_outer = [], []
    all_nodes = [nodes]
    count = len(nodes)
    for side in ('top', 'bottom'):
        zf = levels[-1] if side == 'top' else levels[0]
        ze = z1 if side == 'top' else z0
        face_nodes = loop + (nk * n2 if side == 'top' else 0)
        nz = max(2, int(math.ceil(abs(ze - zf) / max(seg, 1e-9))))
        zr = zf + (ze - zf) * np.linspace(0.0, 1.0, nz + 1)[1:]
        nb = len(loop)
        band_nodes = np.vstack([np.c_[ring_xy, np.full(nb, z)] for z in zr])
        band_ids = count + np.arange(len(band_nodes)).reshape(nz, nb)
        cap_ids = np.r_[band_ids[-1], count + len(band_nodes) + np.arange(len(cap_inner))]
        cap_nodes = np.c_[cap_inner, np.full(len(cap_inner), ze)]
        all_nodes += [band_nodes, cap_nodes]
        count += len(band_nodes) + len(cap_nodes)
        rows = np.vstack([face_nodes, band_ids])
        band = []
        for r in range(nz):
            a, b = rows[r], rows[r + 1]
            a2, b2 = np.roll(a, -1), np.roll(b, -1)
            band += [np.c_[a, a2, b2], np.c_[a, b2, b]]
        band = np.vstack(band)
        cap = cap_ids[cap_tri]
        face = (tri + nk * n2)[:, [0, 2, 1]] if side == 'top' else tri
        if side == 'bottom':
            band = band[:, [0, 2, 1]]
            cap = cap[:, [0, 2, 1]]
        surf = np.vstack([face, band, cap])
        pool = np.vstack(all_nodes)
        grow = (lambda x, y, z, zf=zf: min(st.tet_max, size(x, y) + st.tet_grade * abs(z - zf)))
        new_xyz, tet = tet_fill(pool, surf, st.tet_max, grow, log)
        all_nodes.append(new_xyz)
        tets.append(tet)
        count += len(new_xyz)
        tet_outer.append(np.vstack([band, cap]))
        log(f'tetrahedra {side}: {len(tet):,}')
    nodes = np.vstack(all_nodes)
    tets = np.vstack(tets)
    # a tetrahedron is air unless its centre lies in a board part's section (the board below a one-sided board)
    tbody = np.zeros(len(tets), np.int32)
    return dict(nodes=nodes, wedges=wedges, body=body.reshape(-1), names=names, xy=xy, tri=tri, levels=levels,
                slab_of=slab_of, nk=nk, nt=nt, body_layers=body, layout=layout, tets=tets, tet_body=tbody,
                tet_outer=np.vstack(tet_outer))


def outer_faces(m):
    """The domain's outside: (triangles, parent element index) of the tetrahedra's band and caps, and (quads,
    parent wedge) round the side of the wedges. Element indices: wedges first, then tetrahedra."""
    nk, nt, n2 = m['nk'], m['nt'], len(m['xy'])
    tri = m['tri']
    tets = m['tets']
    faces = np.vstack([tets[:, [0, 1, 2]], tets[:, [0, 1, 3]], tets[:, [0, 2, 3]], tets[:, [1, 2, 3]]])
    owner = np.tile(np.arange(len(tets)), 4)
    fk = np.sort(faces, axis=1)
    want = np.sort(m['tet_outer'], axis=1)
    lookup = {tuple(f): i for f, i in zip(fk.tolist(), owner.tolist())}
    tpar = np.array([lookup[tuple(f)] for f in want.tolist()]) + len(m['wedges'])
    loop = boundary_loop(tri)
    e = np.c_[loop, np.roll(loop, -1)]
    edge_tri = {}
    for t, (a, b, c) in enumerate(tri.tolist()):
        for u, v in ((a, b), (b, c), (c, a)):
            edge_tri[(u, v)] = t
    bt = np.array([edge_tri[(int(u), int(v))] for u, v in e])
    quads, qpar = [], []
    for k in range(nk):
        quads.append(np.c_[e[:, 0] + k * n2, e[:, 1] + k * n2, e[:, 1] + (k + 1) * n2, e[:, 0] + (k + 1) * n2])
        qpar.append(k * nt + bt)
    return m['tet_outer'], tpar, np.vstack(quads), np.concatenate(qpar)


def body_faces(m, body_ids, select=None):
    """The faces between wedges of `body_ids` and wedges of any other body: (tris, (wedge in, wedge out)),
    (quads, (wedge in, wedge out)). select(x, y, z) -> bool array keeps only faces whose centre passes."""
    nk, nt, n2 = m['nk'], m['nt'], len(m['xy'])
    tri, body = m['tri'], m['body_layers']
    inside = np.isin(body, list(body_ids))
    tris, tpar = [], []
    for k in range(nk - 1):                                     # between layer k and k + 1
        up = inside[k] & ~inside[k + 1]
        dn = ~inside[k] & inside[k + 1]
        t = np.flatnonzero(up | dn)
        if len(t):
            tris.append(tri[t] + (k + 1) * n2)
            win = np.where(up[t], k * nt + t, (k + 1) * nt + t)
            wout = np.where(up[t], (k + 1) * nt + t, k * nt + t)
            tpar.append(np.c_[win, wout])
    e = np.sort(np.vstack([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]]), axis=1)
    et = np.tile(np.arange(nt), 3)
    o = np.lexsort((e[:, 1], e[:, 0]))
    e, et = e[o], et[o]
    pair = np.flatnonzero(np.r_[(e[1:] == e[:-1]).all(1), False])
    a, b, ed = et[pair], et[pair + 1], e[pair]
    quads, qpar = [], []
    for k in range(nk):
        ia, ib = inside[k, a], inside[k, b]
        d = ia != ib
        if d.any():
            q = np.c_[ed[d, 0] + k * n2, ed[d, 1] + k * n2, ed[d, 1] + (k + 1) * n2, ed[d, 0] + (k + 1) * n2]
            win = np.where(ia[d], a[d], b[d]) + k * nt
            wout = np.where(ia[d], b[d], a[d]) + k * nt
            quads.append(q)
            qpar.append(np.c_[win, wout])
    tris = np.vstack(tris) if tris else np.zeros((0, 3), int)
    tpar = np.vstack(tpar) if tpar else np.zeros((0, 2), int)
    quads = np.vstack(quads) if quads else np.zeros((0, 4), int)
    qpar = np.vstack(qpar) if qpar else np.zeros((0, 2), int)
    if select is not None:
        if len(tris):
            c = m['nodes'][tris].mean(axis=1)
            k = select(c[:, 0], c[:, 1], c[:, 2])
            tris, tpar = tris[k], tpar[k]
        if len(quads):
            c = m['nodes'][quads].mean(axis=1)
            k = select(c[:, 0], c[:, 1], c[:, 2])
            quads, qpar = quads[k], qpar[k]
    return (tris, tpar), (quads, qpar)


def level_faces(m, z, select):
    """The horizontal faces at height z (a level of the wedge layers) whose triangle centre passes
    select(x, y) -> bool array: (tris, (wedge below, wedge above)). A port sheet is made of these."""
    levels = np.asarray(m['levels'])
    k = int(np.argmin(np.abs(levels - z)))
    if abs(levels[k] - z) > 1e-6 or k == 0 or k == len(levels) - 1:
        raise ValueError(f'z = {z} is not an inner level of the wedge layers')
    nt, n2, tri = m['nt'], len(m['xy']), m['tri']
    c = m['xy'][tri].mean(axis=1)
    t = np.flatnonzero(select(c[:, 0], c[:, 1]))
    return tri[t] + k * n2, np.c_[(k - 1) * nt + t, k * nt + t]


def vertical_faces(m, z0, z1, line, tol=1e-6):
    """The vertical faces between z0 and z1 on the triangle edges that lie along `line` (a shapely LineString in
    xy, embedded in the triangle mesh): (quads, (wedge, wedge)). A port sheet across a gap through the board."""
    levels = np.asarray(m['levels'])
    nt, n2, tri, xy = m['nt'], len(m['xy']), m['tri'], m['xy']
    e = np.sort(np.vstack([tri[:, [0, 1]], tri[:, [1, 2]], tri[:, [2, 0]]]), axis=1)
    et = np.tile(np.arange(nt), 3)
    o = np.lexsort((e[:, 1], e[:, 0]))
    e, et = e[o], et[o]
    pair = np.flatnonzero(np.r_[(e[1:] == e[:-1]).all(1), False])
    a, b, ed = et[pair], et[pair + 1], e[pair]
    mid = xy[ed].mean(axis=1)
    on = shapely.distance(line, shapely.points(mid)) < tol
    on &= (shapely.distance(line, shapely.points(xy[ed[:, 0]])) < tol)
    on &= (shapely.distance(line, shapely.points(xy[ed[:, 1]])) < tol)
    quads, par = [], []
    for k in range(len(levels) - 1):
        if levels[k] < z0 - 1e-9 or levels[k + 1] > z1 + 1e-9:
            continue
        q = np.c_[ed[on, 0] + k * n2, ed[on, 1] + k * n2, ed[on, 1] + (k + 1) * n2, ed[on, 0] + (k + 1) * n2]
        quads.append(q)
        par.append(np.c_[a[on] + k * nt, b[on] + k * nt])
    if not quads or not len(quads[0]):
        raise ValueError('no triangle edges along the line: embed it in the mesh (extra_lines)')
    return np.vstack(quads), np.vstack(par)


def write_elmer(m, folder, boundaries, log=print):
    """Elmer's mesh files. boundaries: [(name, tris, tri parents [n] or [n, 2], quads, quad parents)], tagged
    1, 2, ... in that order. Bodies are numbered as m['names'] (AIR = 1)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    nodes, wedges, body = m['nodes'], m['wedges'], m['body'] + 1
    tets, tbody = m['tets'], m['tet_body'] + 1
    ne = len(wedges) + len(tets)
    nb = sum(len(t) + len(q) for _, t, _, q, _ in boundaries)
    ntri = sum(len(t) for _, t, _, _, _ in boundaries)
    nquad = sum(len(q) for _, _, _, q, _ in boundaries)
    types = 1 + (len(tets) > 0) + (ntri > 0) + (nquad > 0)
    head = f'{len(nodes)} {ne} {nb}\n{types}\n706 {len(wedges)}\n' + (f'504 {len(tets)}\n' if len(tets) else '')
    head += (f'303 {ntri}\n' if ntri else '') + (f'404 {nquad}\n' if nquad else '')
    (folder / 'mesh.header').write_text(head)
    with open(folder / 'mesh.nodes', 'w') as fh:
        np.savetxt(fh, np.c_[np.arange(1, len(nodes) + 1), np.full(len(nodes), -1), nodes],
                   fmt='%d %d %.10g %.10g %.10g')
    with open(folder / 'mesh.elements', 'w') as fh:
        np.savetxt(fh, np.c_[np.arange(1, len(wedges) + 1), body, np.full(len(wedges), 706), wedges + 1], fmt='%d')
        if len(tets):
            np.savetxt(fh, np.c_[np.arange(len(wedges) + 1, ne + 1), tbody, np.full(len(tets), 504), tets + 1],
                       fmt='%d')
    eid = 1
    with open(folder / 'mesh.boundary', 'w') as fh:
        for tag, (name, t, tp, q, qp) in enumerate(boundaries, start=1):
            for faces, par, typ in ((t, tp, 303), (q, qp, 404)):
                if not len(faces):
                    continue
                par = np.asarray(par)
                p1 = (par[:, 0] if par.ndim == 2 else par) + 1
                p2 = (par[:, 1] + 1) if par.ndim == 2 else np.zeros(len(faces), int)
                n = len(faces)
                np.savetxt(fh, np.c_[np.arange(eid, eid + n), np.full(n, tag), p1, p2, np.full(n, typ), faces + 1],
                           fmt='%d')
                eid += n
    with open(folder / 'mesh.names', 'w') as fh:
        fh.write('! ----- names for bodies -----\n')
        for i, n in enumerate(m['names'], start=1):
            fh.write(f'$ {n} = {i}\n')
        fh.write('! ----- names for boundaries -----\n')
        for i, (n, *_r) in enumerate(boundaries, start=1):
            fh.write(f'$ {n} = {i}\n')
    log(f'wrote Elmer mesh to {folder}: {len(nodes):,} nodes, {len(wedges):,} wedges, {len(tets):,} tetrahedra, '
        f'{nb:,} boundary faces')
