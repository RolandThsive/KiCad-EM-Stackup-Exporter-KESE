"""A FastHenry case: the board's copper as segments and filaments, the ports, the input file, running FastHenry and
reading its impedance matrix back.

FastHenry (M.I.T.'s, in FastFieldSolvers' release 3.0.1; see Solver_FastHenry) solves the magneto-quasi-static problem on conductors cut into
filaments, each carrying a uniform current along its length: a straight segment of width w and height h is split
into nwinc x nhinc filaments across its section, so the current can crowd towards the edges at high frequency, and
every filament couples to every other through its partial inductance. Only the copper is discretised; the space
round it is handled exactly. Ports are pairs of nodes named in .external lines; FastHenry gives back the matrix of
open-circuit impedances between them, Z[i][j] = V_i / I_j with every other port open, at each frequency.

What the bridge makes of a board:
* a track is a segment between two nodes at its ends, at the middle of its copper layer, w its width and h the
  layer's copper thickness; an arc is cut into chords; tracks of one net meeting at a point share a node;
* a via is a vertical bar from its node on one layer to its node on the other, a square of about the plated barrel's
  copper section (the via's pads, a fraction of a square millimetre each, are left out);
* a copper polygon (the rotor) is a grid of bars, each as wide as the cell it stands for: a polar grid, graded
  towards the edges, where the polygon is a sector of a ring (no staircase on its arcs), a square grid clipped to it
  otherwise;
* a coil is opened at its port: between its two stacked trace ends, at a left-out via (between the via's two layer
  nodes), or at a cut across a trace (the copper inside the cut taken out, the port between the two cut faces).
"""
from __future__ import annotations

import math
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SIGMA_CU = 5.8e7                       # S/m


def fasthenry_exe():
    """FastHenry: $FASTHENRY, else the branch's Solver_FastHenry/install/bin/fasthenry, else on the PATH."""
    env = os.environ.get('FASTHENRY')
    for c in ([Path(env)] if env else []) + [HERE.parent / 'Solver_FastHenry' / 'install' / 'bin' / 'fasthenry']:
        if c.is_file():
            return str(c)
    return 'fasthenry'


def fasthenry_version():
    """FastHenry's version as it prints it on a run (it has no --version)."""
    try:
        r = subprocess.run([fasthenry_exe(), '-h'], capture_output=True, text=True, timeout=20)
        m = re.search(r'FastHenry version ([\d.]+)', r.stdout + r.stderr, re.I)
        return m.group(1) if m else 'unknown'
    except Exception as e:              # noqa: BLE001
        return f'unknown ({e})'


@dataclass
class Model:
    """Nodes (merged by key), segments as FastHenry lines, ports, and what each segment belongs to."""
    title: str = 'KESE board'
    nodes: dict = field(default_factory=dict)         # key -> (name, x, y, z)
    segs: list = field(default_factory=list)          # FastHenry element lines
    owner: list = field(default_factory=list)         # the body of each segment ('TX', 'ROTOR', ...)
    ports: list = field(default_factory=list)         # (name, node1, node2)
    filaments: int = 0
    geometry: list = field(default_factory=list)      # (body, kind, (x0, y0, z0), (x1, y1, z1), w, h) for pictures
    where: dict = field(default_factory=dict)         # node name -> (x, y, z)

    made: int = 0                                     # nodes ever made: the next node's number
    origin: tuple = (0.0, 0.0)                        # the point (mm) model.inp's x and y are written about

    def node(self, key, x, y, z):
        if key not in self.nodes:
            name = f'N{self.made}'
            self.made += 1
            self.nodes[key] = (name, float(x), float(y), float(z))
            self.where[name] = (float(x), float(y), float(z))
        return self.nodes[key][0]

    def xyz(self, name):
        return self.where[name]

    def segment(self, body, a, b, w, h, nwinc=1, nhinc=1, rw=None, rh=None, wdir=None, kind='track'):
        opts = f' w={w:.6g} h={h:.6g} nwinc={nwinc} nhinc={nhinc}'
        if rw and nwinc > 1:
            opts += f' rw={rw:g}'
        if rh and nhinc > 1:
            opts += f' rh={rh:g}'
        if wdir is not None:
            opts += f' wx={wdir[0]:.6f} wy={wdir[1]:.6f} wz={wdir[2]:.6f}'
        self.segs.append(f'E{len(self.segs)} {a} {b}{opts}')
        self.owner.append(body)
        self.filaments += nwinc * nhinc
        self.geometry.append((body, kind, self.xyz(a), self.xyz(b), w, h))

    def port(self, name, a, b):
        self.ports.append((name, a, b))

    def text(self, freq_hz, sigma=SIGMA_CU):
        # x and y are written about the middle of the model, rounded to the whole millimetre, and to 12 significant
        # digits. FastHenry takes two filaments as parallel when their cosine is 1 to within 1e-13, an absolute
        # test, and for filaments a few widths apart it adds four side filaments, each the filament moved half its
        # width or height, keeping its length. 100 mm from the origin (where KiCad puts the boards) moving a point
        # rounds it by up to 1.4e-17 m, 2e-13 of a 0.06 mm rotor bar: two bars on one line (the two halves of
        # S0d2's rotor, on opposite rays) then failed the test, went to FastHenry's formula for skew filaments,
        # which is infinite for two on one line, and the whole impedance matrix came out NaN. About the middle,
        # every point is within 12 mm of the origin and the rounding is ten times smaller
        xs = [v[1] for v in self.nodes.values()] or [0.0]
        ys = [v[2] for v in self.nodes.values()] or [0.0]
        ox, oy = self.origin = (float(round((min(xs) + max(xs)) / 2)), float(round((min(ys) + max(ys)) / 2)))
        lines = [f'* {self.title}', f'* x and y in mm from ({ox:g}, {oy:g}), the model\'s middle', '.units mm',
                 f'.default sigma={sigma * 1e-3:g}', '']
        lines += [f'{n} x={x - ox:.12g} y={y - oy:.12g} z={z:.12g}' for n, x, y, z in self.nodes.values()]
        lines += [''] + self.segs + ['']
        lines += [f'.external {a} {b} {name}' for name, a, b in self.ports]
        lines += [f'.freq fmin={freq_hz:g} fmax={freq_hz:g} ndec=1', '.end']
        return '\n'.join(lines) + '\n'


def _seg_box_clip(p0, p1, centre, u, n, half_len, half_wid):
    """The part of segment p0-p1 inside the box |(x-c).u| <= half_len, |(x-c).n| <= half_wid, as (t0, t1) along it
    (Liang-Barsky), or None."""
    p0, p1, c = np.asarray(p0, float), np.asarray(p1, float), np.asarray(centre, float)
    d = p1 - p0
    t0, t1 = 0.0, 1.0
    for axis, h in ((u, half_len), (n, half_wid)):
        a, b = float(np.dot(p0 - c, axis)), float(np.dot(d, axis))
        for sgn in (1, -1):                       # sgn * (a + b t) <= h
            if abs(b) < 1e-15:
                if sgn * a > h:
                    return None
                continue
            t = (h - sgn * a) / (sgn * b)
            if sgn * b > 0:
                t1 = min(t1, t)
            else:
                t0 = max(t0, t)
    return (t0, t1) if t1 > t0 else None


MERGE_DEG = 0.01   # consecutive pieces of a trace closer than this to a straight line become one segment


def merge_collinear(pieces, model, keep, max_deg=MERGE_DEG):
    """Join consecutive pieces of a trace that are straight to within max_deg degrees into one segment, dropping the
    node between them from the model. FastHenry takes two filaments that meet end to end as parallel only if they
    are exactly so; at a few ten-thousandths of a degree apart (a straight track the generator split in two, its
    points rounded to KiCad's nanometre) it computes their mutual inductance with its non-parallel formula, which
    is infinite for filaments that touch, and the whole impedance matrix comes out NaN. pieces: [body, a, b, w, h,
    nwinc, nhinc, rw, rh] with node names a and b; keep: node names never dropped (ports, cuts, vias)."""
    def angle(n, p, q):
        (x, y, _), (px, py, _), (qx, qy, _) = model.xyz(n), model.xyz(p), model.xyz(q)
        u, v = (x - px, y - py), (qx - x, qy - y)
        c = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
        return math.degrees(math.acos(max(-1.0, min(1.0, c))))

    dropped = 0
    while True:
        at = {}
        for i, s in enumerate(pieces):
            for n in (s[1], s[2]):
                at.setdefault(n, []).append(i)
        for n, ii in at.items():
            if len(ii) != 2 or n in keep:
                continue
            s, t = pieces[ii[0]], pieces[ii[1]]
            if s[0] != t[0] or s[3:] != t[3:] or model.xyz(n)[2] != model.xyz(s[1])[2]:
                continue
            p = s[1] if s[2] == n else s[2]
            q = t[1] if t[2] == n else t[2]
            if p == q or angle(n, p, q) >= max_deg:
                continue
            pieces[ii[0]] = [s[0], p, q] + s[3:]
            del pieces[ii[1]]
            key = next(k for k, v in model.nodes.items() if v[0] == n)
            del model.nodes[key]
            dropped += 1
            break
        else:
            return dropped


def add_board(model, board, zlayers, bodies, nwinc=1, nhinc=1, rw=None, rh=None, open_vias=(), cuts=(),
              via_bar_mm=None, max_deg=5.0, plating_mm=0.025, log=print):
    """The tracks and vias of the nets in `bodies` ({net name: body}) as segments at their layers' mid-heights
    (zlayers: {layer: (z_bottom, z_top)} in model coordinates). open_vias: (x, y) of vias left out (each coil's
    port goes between their two layer nodes, see via_nodes). cuts: dicts with xy, along (unit vector), gap_mm and
    half_width_mm, each taking a trace's copper out of a box on 'layer' (its port goes between the two cut faces,
    see cut_nodes). A via is a square bar with the copper section of its barrel plated plating_mm thick, unless
    via_bar_mm gives the side. Points are model coordinates (x, -y of KiCad's)."""
    zmid = {k: (a + b) / 2 for k, (a, b) in zlayers.items()}
    thick = {k: b - a for k, (a, b) in zlayers.items()}
    cut_ends = {i: [] for i in range(len(cuts))}
    straight = []                                        # the tracks' straight pieces, before they are joined
    for t in board.tracks:
        body = bodies.get(t.net)
        if body is None or t.layer not in zmid:
            continue
        for (x0, y0), (x1, y1) in t.chords(max_deg=max_deg):
            p0, p1 = np.array([x0, -y0]), np.array([x1, -y1])
            if np.hypot(*(p1 - p0)) < 1e-6:
                continue
            pieces = [(0.0, 1.0)]
            for ci, c in enumerate(cuts):
                if c['net'] != t.net or c['layer'] != t.layer:
                    continue
                u = np.asarray(c['along'], float) / np.linalg.norm(c['along'])
                n = np.array([-u[1], u[0]])
                new = []
                for a, b in pieces:
                    q0, q1 = p0 + (p1 - p0) * a, p0 + (p1 - p0) * b
                    clip = _seg_box_clip(q0, q1, c['xy'], u, n, c['gap_mm'] / 2, c['half_width_mm'])
                    if clip is None:
                        new.append((a, b))
                        continue
                    s0, s1 = a + (b - a) * clip[0], a + (b - a) * clip[1]
                    for lo, hi, end in ((a, s0, s0), (s1, b, s1)):
                        if hi - lo > 1e-9:
                            new.append((lo, hi))
                            cut_ends[ci].append(tuple(p0 + (p1 - p0) * end))
                pieces = new
            for a, b in pieces:
                q0, q1 = p0 + (p1 - p0) * a, p0 + (p1 - p0) * b
                na = model.node((t.net, t.layer, round(q0[0], 5), round(q0[1], 5)), q0[0], q0[1], zmid[t.layer])
                nb = model.node((t.net, t.layer, round(q1[0], 5), round(q1[1], 5)), q1[0], q1[1], zmid[t.layer])
                straight.append([body, na, nb, t.width, thick[t.layer], nwinc, nhinc, rw, rh])
    keep = {model.nodes[(c['net'], c['layer'], round(x, 5), round(y, 5))][0]
            for ci, c in enumerate(cuts) for x, y in cut_ends[ci]}
    for v in board.vias:                                 # where vias land, and where left-out vias were
        if bodies.get(v.net) is not None:
            keep |= {name for key, (name, nx, ny, _) in model.nodes.items()
                     if key[0] == v.net and math.hypot(nx - v.at[0], ny + v.at[1]) <= max(v.size / 2 + 0.05, 0.45)}
    dropped = merge_collinear(straight, model, keep)
    if dropped:
        log(f'{dropped} track joints straight to within {MERGE_DEG} degrees: their pieces joined')
    for p in straight:
        model.segment(*p)
    for v in board.vias:
        body = bodies.get(v.net)
        if body is None:
            continue
        x, y = v.at[0], -v.at[1]
        if any(math.hypot(x - ox, y - oy) < 1e-3 for ox, oy in open_vias):
            continue
        lays = [l for l in zlayers if l in v.layers or (v.layers == ('F.Cu', 'B.Cu'))]
        lays = sorted(lays, key=lambda l: -zmid[l])
        side = via_bar_mm or barrel_square(v.drill, plating_mm)
        for top, bot in zip(lays[:-1], lays[1:]):
            a, b = nearest_node(model, v.net, top, x, y, v.size / 2 + 0.05), nearest_node(model, v.net, bot, x, y,
                                                                                         v.size / 2 + 0.05)
            if a is None or b is None:
                continue                               # a via no track of this net reaches on that layer
            model.segment(body, a, b, side, side, 1, 1, wdir=(1, 0, 0), kind='via')
    return {ci: ends for ci, ends in cut_ends.items()}


def barrel_square(drill_mm, plating_mm=0.025):
    """The side of a square bar with the copper section of a via's plated barrel."""
    r = drill_mm / 2
    return math.sqrt(math.pi * (r * r - (r - plating_mm) ** 2))


def nearest_node(model, net, layer, x, y, within):
    best = None
    for key, (name, nx, ny, _) in model.nodes.items():
        if key[0] == net and key[1] == layer:
            d = math.hypot(nx - x, ny - y)
            if d <= within and (best is None or d < best[0]):
                best = (d, name)
    return best[1] if best else None


def via_nodes(model, net, x, y, layers=('F.Cu', 'B.Cu'), within=0.45):
    """The two nodes of a left-out via: where its net's tracks reach (x, y) on each of its layers."""
    out = [nearest_node(model, net, l, x, y, within) for l in layers]
    if None in out:
        raise ValueError(f'no track of net {net} reaches ({x:.3f}, {y:.3f}) on {layers}')
    return out


def cut_nodes(model, net, layer, ends):
    """The two nodes at a cut's faces: of the track ends the cut made, the two farthest apart."""
    names = []
    for x, y in ends:
        names.append(model.nodes[(net, layer, round(x, 5), round(y, 5))][0])
    names = sorted(set(names))
    if len(names) < 2:
        raise ValueError(f'the cut on net {net} made {len(names)} ends: it does not cross the trace')
    pts = {n: model.xyz(n) for n in names}
    a, b = max(((p, q) for i, p in enumerate(names) for q in names[i + 1:]),
               key=lambda pq: math.dist(pts[pq[0]][:2], pts[pq[1]][:2]))
    return a, b


def graded(a, b, h_edge, h_max, q=1.3):
    """Cell edges from a to b: h_edge at both ends, growing by q up to h_max in the middle."""
    span, side, h = b - a, [], h_edge
    while 2 * (sum(side) + h) < span - h_max and h < h_max:
        side.append(h)
        h *= q
    mid = span - 2 * sum(side)
    nm = max(1, int(math.ceil(mid / h_max)))
    sizes = side + [mid / nm] * nm + side[::-1]
    return a + np.concatenate([[0.0], np.cumsum(sizes)]) * (span / sum(sizes))


def ring_sector(pts, axis):
    """(r_in, r_out, a0, a1) when the polygon (KiCad points) is a sector of a ring about axis, angles in KiCad's
    frame (y down) with a0 < a1; None otherwise. A polygon is taken as one when the sector with its extreme radii and
    angles has its area to 0.5 %."""
    from shapely.geometry import Polygon
    p = np.asarray(pts, float) - np.asarray(axis, float)
    r = np.hypot(p[:, 0], p[:, 1])
    a = np.unwrap(np.arctan2(p[:, 1], p[:, 0]))
    r_in, r_out, a0, a1 = r.min(), r.max(), a.min(), a.max()
    if r_in < 1e-6 or a1 - a0 > 2 * math.pi - 1e-6:
        return None
    area = 0.5 * (r_out ** 2 - r_in ** 2) * (a1 - a0)
    poly = Polygon(pts).buffer(0)
    if abs(poly.area - area) > 5e-3 * area:
        return None
    return r_in, r_out, a0, a1


def add_polygon(model, body, pts, axis, angle_deg, z, h, h_edge=0.05, h_max=0.3, square_mm=0.2):
    """A copper polygon (KiCad points) turned by angle_deg about axis (KiCad's sense) as a grid of bars at height z,
    h thick: a polar grid graded towards all four edges where it is a sector of a ring, a square grid clipped to it
    otherwise. Returns the number of bars."""
    sec = ring_sector(pts, axis)
    th = math.radians(angle_deg)
    cx, cy = axis
    n0 = len(model.segs)
    if sec:
        r_in, r_out, a0, a1 = sec
        re_ = graded(r_in, r_out, h_edge, h_max)
        rm = (r_in + r_out) / 2
        te = a0 + (graded(0.0, (a1 - a0) * rm, h_edge, h_max) / rm)
        rc, tc, dr, dt = (re_[1:] + re_[:-1]) / 2, (te[1:] + te[:-1]) / 2, np.diff(re_), np.diff(te)

        def xy(i, j):
            return cx + rc[i] * math.cos(tc[j] + th), -(cy + rc[i] * math.sin(tc[j] + th))
        tag = f'{body}{model.made}_'
        names = {(i, j): model.node((tag, i, j), *xy(i, j), z) for i in range(len(rc)) for j in range(len(tc))}
        for (i, j), n in names.items():
            for di, dj in ((0, 1), (1, 0)):
                m = names.get((i + di, j + dj))
                if not m:
                    continue
                (x0, y0), (x1, y1) = xy(i, j), xy(i + di, j + dj)
                ln = math.hypot(x1 - x0, y1 - y0)
                w = dr[i] if dj else (rc[i] + rc[i + 1]) / 2 * dt[j]
                model.segment(body, n, m, w, h, 1, 1, wdir=(-(y1 - y0) / ln, (x1 - x0) / ln, 0.0), kind='rotor')
        return len(model.segs) - n0
    import shapely
    from shapely.geometry import Polygon
    poly = Polygon(pts).buffer(0)
    x0, y0, x1, y1 = poly.bounds
    xs, ys = np.arange(x0 + square_mm / 2, x1, square_mm), np.arange(y0 + square_mm / 2, y1, square_mm)
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    inside = shapely.contains_xy(poly, X, Y)
    dx, dy = X - cx, Y - cy
    Xr, Yr = cx + dx * math.cos(th) - dy * math.sin(th), cy + dx * math.sin(th) + dy * math.cos(th)
    tag = f'{body}{model.made}_'
    names = {(i, j): model.node((tag, i, j), Xr[i, j], -Yr[i, j], z) for i, j in zip(*np.nonzero(inside))}
    for (i, j), n in names.items():
        for di, dj in ((1, 0), (0, 1)):
            m = names.get((i + di, j + dj))
            if m:
                (ax, ay, _), (bx, by, _) = model.xyz(n), model.xyz(m)
                ln = math.hypot(bx - ax, by - ay)
                model.segment(body, n, m, square_mm, h, 1, 1, wdir=(-(by - ay) / ln, (bx - ax) / ln, 0.0),
                              kind='rotor')
    return len(model.segs) - n0


def read_zc(path):
    """FastHenry's Zc.mat: {port name: index} and one complex matrix per frequency, [(f, Z), ...]."""
    txt = Path(path).read_text()
    rows = {int(k): (pname or node).rstrip(',').upper()
            for k, node, pname in re.findall(r'Row (\d+):\s+(\S+)\s+to\s+\S+?(?:,\s+port name:\s+(\S+))?\n', txt)}
    out = []
    for block in txt.split('Impedance matrix for frequency = ')[1:]:
        head, body = block.split('\n', 1)
        f = float(head.split()[0])
        n = int(head.split()[1])
        vals = [complex(float(a), float(b)) for a, b in
                re.findall(r'([-+]?\d[\d.]*(?:e[-+]?\d+)?)\s*([-+]\d[\d.]*(?:e[-+]?\d+)?)j', body)]
        out.append((f, np.array(vals[:n * n]).reshape(n, n)))
    return {v: k - 1 for k, v in rows.items()}, out


def run(model, freq_hz, folder, options=(), log=print, sigma=SIGMA_CU):
    """Write model.inp in folder, run FastHenry there and read Zc.mat. Returns the port names in order, the
    impedance matrix (ohm), the seconds, FastHenry's peak memory (GB) and its log."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'model.inp').write_text(model.text(freq_hz, sigma))
    for old in ('Zc.mat',):
        (folder / old).unlink(missing_ok=True)
    t0 = time.time()
    with open(folder / 'fasthenry.log', 'w') as out:
        p = subprocess.Popen([fasthenry_exe(), 'model.inp', *options], cwd=folder, stdout=out, stderr=subprocess.STDOUT)
        _, status, usage = os.wait4(p.pid, 0)
    secs = time.time() - t0
    text = (folder / 'fasthenry.log').read_text(errors='replace')
    if status or not (folder / 'Zc.mat').exists():
        raise RuntimeError(f'FastHenry failed in {folder} (status {status}):\n{text[-2000:]}')
    order, mats = read_zc(folder / 'Zc.mat')
    names = [name for name, *_ in model.ports]
    idx = [order[n.upper()] for n in names]
    Z = mats[0][1][np.ix_(idx, idx)]
    return names, Z, secs, usage.ru_maxrss / 1e6, text


def coil_rows(names, Z, freq_hz, driven='TX'):
    """Each port's numbers from the impedance matrix: the driven coil's Z, R and L; each other coil's mutual
    impedance from the driven one, Zm = Z[coil, driven], its M and the reverse M from Z[driven, coil], which an
    exact solve makes equal (reciprocity)."""
    w = 2 * math.pi * freq_hz
    k = names.index(driven)
    out = {}
    for i, n in enumerate(names):
        z = Z[i, k]
        if i == k:
            out[n] = dict(Z=[z.real, z.imag], R=z.real, L=z.imag / w)
        else:
            out[n] = dict(Zm=[z.real, z.imag], M=z.imag / w, Rm=z.real, M_reverse=Z[k, i].imag / w,
                          driven_by=driven, Z_self=[Z[i, i].real, Z[i, i].imag], L_self=Z[i, i].imag / w)
    return out


def size_of(log_text):
    """What FastHenry reports of the problem's size: filaments and, where it prints them, mesh currents."""
    out = {}
    for key, pat in (('filaments', r'Total number of filaments[^\d]*(\d+)'),
                     ('segments', r'Total number of segments[^\d]*(\d+)'),
                     ('mesh_currents', r'Number of mesh currents[^\d]*(\d+)'),
                     ('groups', r'Number of groups[^\d]*(\d+)')):
        m = re.search(pat, log_text, re.I)
        if m:
            out[key] = int(m.group(1))
    return out
