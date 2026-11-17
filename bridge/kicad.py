"""A .kicad_pcb read for FastHenry: its copper tracks, arcs, vias and copper polygons, by net and layer.

FastHenry is a filament solver: a conductor is a chain of straight segments, each with a width and a height, and
a sheet is a grid of such segments. A KiCad track is exactly that, its centre line with a width, so the board file
itself is where the conductors come from; KESE's export gives the heights of the copper layers (stackup.py).

Coordinates stay KiCad's in the plane, in mm, with y turned up (y_model = -y_kicad), as KESE writes them.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

_TOKEN = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+')


def parse_sexpr(text):
    """A KiCad s-expression as nested lists of strings (quotes taken off)."""
    stack, cur = [], []
    for tok in _TOKEN.findall(text):
        if tok == '(':
            stack.append(cur)
            cur = []
        elif tok == ')':
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(tok[1:-1] if tok.startswith('"') else tok)
    return cur[0]


def _find(node, key):
    return next((c for c in node if isinstance(c, list) and c and c[0] == key), None)


def _all(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def _xy(node, key):
    c = _find(node, key)
    return (float(c[1]), float(c[2])) if c else None


@dataclass
class Track:
    start: tuple
    end: tuple
    width: float
    layer: str
    net: str
    mid: tuple | None = None          # an arc's middle point; None for a straight segment

    def chords(self, max_deg=5.0, max_len=0.5):
        """The track as straight pieces: itself for a segment, an arc cut into chords of at most max_deg degrees
        and max_len mm."""
        if self.mid is None:
            return [(self.start, self.end)]
        c, r = _circle(self.start, self.mid, self.end)
        a0, am, a1 = (math.atan2(p[1] - c[1], p[0] - c[0]) for p in (self.start, self.mid, self.end))
        sweep = (a1 - a0) % (2 * math.pi)
        if (am - a0) % (2 * math.pi) > sweep:           # the arc runs the other way round
            sweep -= 2 * math.pi
        n = max(1, math.ceil(abs(math.degrees(sweep)) / max_deg), math.ceil(abs(sweep) * r / max_len))
        pts = [(c[0] + r * math.cos(a0 + sweep * k / n), c[1] + r * math.sin(a0 + sweep * k / n)) for k in range(n + 1)]
        pts[0], pts[-1] = self.start, self.end
        return list(zip(pts[:-1], pts[1:]))


@dataclass
class Via:
    at: tuple
    size: float
    drill: float
    layers: tuple
    net: str


@dataclass
class Board:
    path: Path
    nets: dict = field(default_factory=dict)          # number -> name
    tracks: list = field(default_factory=list)
    vias: list = field(default_factory=list)
    polygons: list = field(default_factory=list)      # (layer, net or '', [(x, y), ...]) copper polygons
    copper_layers: list = field(default_factory=list)


def _circle(p, q, r):
    """Centre and radius of the circle through three points."""
    ax, ay = p
    bx, by = q
    cx, cy = r
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return (ux, uy), math.hypot(ax - ux, ay - uy)


def read(path):
    """The copper of a .kicad_pcb (KiCad 6 to 9): nets, tracks and arcs, vias, and copper polygons (gr_poly on a
    copper layer, and zones' filled polygons). Points are KiCad's, in mm, y down."""
    root = parse_sexpr(Path(path).read_text())
    b = Board(path=Path(path))
    layers = _find(root, 'layers')
    if layers:
        b.copper_layers = [l[1] for l in layers[1:] if isinstance(l, list) and len(l) > 1 and l[1].endswith('.Cu')]
    for n in _all(root, 'net'):
        if len(n) >= 3:
            b.nets[n[1]] = n[2]

    def net_of(node):
        n = _find(node, 'net')
        if not n:
            return ''
        name = n[2] if len(n) > 2 else b.nets.get(n[1], n[1])
        return name

    for kind in ('segment', 'arc'):
        for t in _all(root, kind):
            w = _find(t, 'width')
            b.tracks.append(Track(start=_xy(t, 'start'), end=_xy(t, 'end'), width=float(w[1]),
                                  layer=_find(t, 'layer')[1], net=net_of(t),
                                  mid=_xy(t, 'mid') if kind == 'arc' else None))
    for v in _all(root, 'via'):
        lay = _find(v, 'layers')
        b.vias.append(Via(at=_xy(v, 'at'), size=float(_find(v, 'size')[1]), drill=float(_find(v, 'drill')[1]),
                          layers=tuple(lay[1:]) if lay else ('F.Cu', 'B.Cu'), net=net_of(v)))
    for p in _all(root, 'gr_poly'):
        layer = _find(p, 'layer')[1]
        if layer.endswith('.Cu'):
            pts = [(float(c[1]), float(c[2])) for c in _find(p, 'pts')[1:] if c[0] == 'xy']
            b.polygons.append((layer, net_of(p), pts))
    for z in _all(root, 'zone'):
        for fp in _all(z, 'filled_polygon'):
            layer = _find(fp, 'layer')[1]
            pts = [(float(c[1]), float(c[2])) for c in _find(fp, 'pts')[1:] if c[0] == 'xy']
            b.polygons.append((layer, net_of(z), pts))
    return b


def net_name(board, net):
    """A net's name as test_spec.json uses it: the name, or the number where the name is empty."""
    return board.nets.get(net, net) or net
