"""Step 2 - BoardBreakdown: the parsed tree -> every board element as a flat shape, then the
resolved 2D regions per layer (with nets, hole spans and heights) that the Geometry modules extrude.

Coordinates: elements are collected in KiCad's frame (mm, Y down).  `resolve()` converts
everything to the board frame (mm, Y up, origin per Run_Parameters.ORIGIN) and snaps it to the grid."""
import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field

import numpy as np
import shapely
from shapely import affinity
from shapely.geometry import LineString, Polygon, box
from shapely.ops import polygonize

from Generator.Common import shapes as sh
from Generator.Common.sexp import atoms, child, children, flag, layer_of, num, numbers, pt, yes
from Generator.Common.shapes import EMPTY, arc3, arc_pts, bezier, disk, thicken, union
from Generator.Common.stackup import read_stackup
from Generator.Geometry import Text
from Parameters import P

GRAPHICS = {"gr_line", "gr_arc", "gr_circle", "gr_rect", "gr_poly", "gr_curve", "gr_bezier",
            "fp_line", "fp_arc", "fp_circle", "fp_rect", "fp_poly", "fp_curve"}
TEXT = {"gr_text", "fp_text", "gr_text_box", "fp_text_box", "dimension", "gr_dimension"}


# ---- drawings --------------------------------------------------------------------------------------
def graphic(node, T):
    """A gr_*/fp_* drawing -> (centre-line geometry, closed?, stroke width, filled?)."""
    kind = node[0].split("_", 1)[1]
    w = num(node, "width")
    if w is None:
        stroke = child(node, "stroke")
        w = num(stroke, "width", 0.0) if stroke else 0.0
    fill = child(node, "fill")
    filled = yes(fill[1]) if fill and len(fill) > 1 else kind == "poly"
    if kind == "line":
        return LineString([T(pt(child(node, "start"))), T(pt(child(node, "end")))]), False, w, False
    if kind == "arc":
        if child(node, "mid"):
            pts = arc3(T(pt(child(node, "start"))), T(pt(child(node, "mid"))), T(pt(child(node, "end"))))
        else:  # KiCad 5: (start centre) (end arc-start) (angle deg)
            c, p0 = T(pt(child(node, "start"))), T(pt(child(node, "end")))
            r = math.hypot(p0[0] - c[0], p0[1] - c[1])
            a0 = math.atan2(p0[1] - c[1], p0[0] - c[0])
            pts = arc_pts(c, r, a0, math.radians(num(node, "angle", 0.0)), first=p0)
        return LineString(pts), False, w, False
    if kind == "circle":
        c, e = T(pt(child(node, "center"))), T(pt(child(node, "end")))
        return disk(c, math.hypot(e[0] - c[0], e[1] - c[1])), True, w, filled
    if kind == "rect":
        (x1, y1), (x2, y2) = pt(child(node, "start")), pt(child(node, "end"))
        return Polygon([T(p) for p in ((x1, y1), (x2, y1), (x2, y2), (x1, y2))]), True, w, filled
    if kind == "poly":
        pts = []
        for p in child(node, "pts")[1:]:
            if p[0] == "xy":
                pts.append(T(pt(p)))
            elif p[0] == "arc":
                pts.extend(arc3(T(pt(child(p, "start"))), T(pt(child(p, "mid"))), T(pt(child(p, "end"))))[1:])
        return (Polygon(pts).buffer(0) if len(pts) >= 3 else EMPTY), True, w, filled
    if kind in ("curve", "bezier"):
        pts = [T(pt(p)) for p in child(node, "pts")[1:] if p[0] == "xy"]
        return LineString(bezier(pts)), False, w, False
    return None, False, 0.0, False


def painted(geom, closed, w, filled):
    """What a drawing covers on a non-outline layer."""
    if geom is None or geom.is_empty:
        return EMPTY
    parts = [geom] if closed and filled else []
    parts.append(thicken(geom.exterior if closed else geom, w))
    return union(parts)


# ---- the breakdown -----------------------------------------------------------------------------------
@dataclass
class Hole:
    drill: object          # outline of the drilled hole
    i: int                 # top copper layer index it spans
    j: int                 # bottom copper layer index
    plated: bool
    net: str
    wall: float            # plating wall thickness (0 for NPTH)


@dataclass
class Breakdown:
    name: str
    layers: list
    stackup: object
    nets: dict = field(default_factory=dict)
    found: Counter = field(default_factory=Counter)
    skipped: Counter = field(default_factory=Counter)
    notes: list = field(default_factory=list)
    # collected (KiCad frame)
    copper_items: dict = field(default_factory=lambda: defaultdict(list))   # layer -> [(geom, net)]
    mask_open_items: dict = field(default_factory=lambda: {"F": [], "B": []})
    silk_items: dict = field(default_factory=lambda: {"F": [], "B": []})
    edge_closed: list = field(default_factory=list)
    edge_open: list = field(default_factory=list)
    holes: list = field(default_factory=list)
    via_tenting: list = field(default_factory=list)   # (pad geom, span layers, {"F": tented, "B": tented})
    tent_default: dict = field(default_factory=dict)
    tent_source: str = ""
    mask_clearance: float = 0.0
    # resolved (board frame, Y up, snapped)
    outline: object = None
    copper: dict = field(default_factory=dict)        # layer -> {net: region}
    copper_all: dict = field(default_factory=dict)    # layer -> region (all nets)
    slab: list = field(default_factory=list)          # laminate between copper k and k+1
    band_laminate: dict = field(default_factory=dict) # inner layer -> laminate beside its copper
    bores_side: dict = field(default_factory=dict)    # "F"/"B" -> open bores on that face
    barrels: list = field(default_factory=list)       # (ring region, i, j, net)
    mask_open: dict = field(default_factory=dict)     # "F"/"B" -> openings
    silk: dict = field(default_factory=dict)          # "F"/"B" -> silk
    transform_note: str = ""
    to_board: object = None                            # affine params used
    to_board_T: object = None
    edge_band: object = None
    edge_net: object = None


class _Collector:
    """Walks the tree and fills a Breakdown (KiCad frame)."""

    def __init__(self, raw, log):
        self.log = log
        tree = raw.tree
        C, M, S = P.Copper, P.SolderMask, P.Silkscreen
        b = Breakdown(name=raw.name, layers=raw.copper_layers, stackup=None)
        self.b = b
        self.layers = raw.copper_layers
        setup = child(tree, "setup") or []
        b.stackup = read_stackup(tree, raw.copper_layers, raw.file_thickness, log)
        b.mask_clearance = num(setup, "pad_to_mask_clearance", 0.0) if M.PAD_TO_MASK_CLEARANCE_MM is None \
            else M.PAD_TO_MASK_CLEARANCE_MM

        for n in children(tree, "net"):
            b.nets[str(n[1])] = str(n[2]) if len(n) > 2 and str(n[2]) else C.NO_NET_NAME

        # via tenting default
        ten = child(setup, "tenting")
        if ten is not None:
            b.tent_default = {}
            for side, key in (("F", "front"), ("B", "back")):
                c = child(ten, key)
                b.tent_default[side] = yes(c[1]) if c is not None and len(c) > 1 else key in atoms(ten)
            b.tent_source = "board setup (tenting)"
        else:
            pp = child(setup, "pcbplotparams")
            vom = child(pp, "viasonmask") if pp else None
            open_ = bool(vom) and yes(vom[1])
            b.tent_default = {"F": not open_, "B": not open_}
            b.tent_source = "plot setting viasonmask" if vom else "KiCad default (vias tented)"

        self.conditional_pads = []
        vias = []
        for node in tree[1:]:
            if not isinstance(node, list) or not node:
                continue
            k = node[0]
            if k == "segment":
                self._track(LineString([pt(child(node, "start")), pt(child(node, "end"))]), node)
            elif k == "arc":
                self._track(LineString(arc3(pt(child(node, "start")), pt(child(node, "mid")), pt(child(node, "end")))), node)
            elif k == "via":
                vias.append(node)
            elif k == "zone":
                self._zone(node)
            elif k in GRAPHICS:
                self._graphic(node, lambda p: p)
            elif k in ("footprint", "module"):
                self._footprint(node)
            elif k in TEXT:
                self._text(node)
            elif k in ("image", "target", "group", "generated", "table"):
                b.skipped[f"{k} items"] += 1
        for v in vias:
            self._via(v)
        if self.conditional_pads:
            existing = {l: union([g for g, _ in gs]) for l, gs in b.copper_items.items()}
            kept = 0
            for l, pad, net in self.conditional_pads:
                if l in existing and existing[l].intersects(pad):
                    b.copper_items[l].append((pad, net))
                    kept += 1
            b.found["via rings removed on unconnected layers"] += len(self.conditional_pads) - kept

    # ---- helpers ----
    def net_name(self, node):
        """(net 3) in KiCad <= 9 is a net number; KiCad 10 writes the net name itself."""
        n = child(node, "net")
        if not n or len(n) < 2:
            return P.Copper.NO_NET_NAME
        key = str(n[1])
        if key in self.b.nets:
            return self.b.nets[key]
        return key if key and key != "0" else P.Copper.NO_NET_NAME

    def _expand(self, layers):
        out = []
        for l in layers:
            l = str(l)
            if l in ("*.Cu", "F&B.Cu"):
                out += self.layers if l == "*.Cu" else ["F.Cu", "B.Cu"]
            elif l.startswith("*."):
                out += ["F." + l[2:], "B." + l[2:]]
            elif l.startswith("F&B."):
                out += ["F." + l[4:], "B." + l[4:]]
            else:
                out.append(l)
        return out

    def _span(self, a, b):
        i, j = sorted((self.layers.index(a), self.layers.index(b)))
        return self.layers[i:j + 1]

    def _add(self, layer, geom, what, net=None):
        b = self.b
        if geom is None or geom.is_empty:
            return
        if layer in self.layers:
            b.copper_items[layer].append((geom, net or P.Copper.NO_NET_NAME))
        elif layer in ("F.Mask", "B.Mask"):
            b.mask_open_items[layer[0]].append(geom)
        elif layer in P.Silkscreen.SILK_LAYERS:
            b.silk_items[layer[0]].append(geom)
        else:
            b.skipped[f"{what} on {layer} (not a physical layer)"] += 1
            return
        b.found[f"{what} on {layer}"] += 1

    # ---- items ----
    def _track(self, line, node):
        self._add(layer_of(node), thicken(line, num(node, "width", 0.0)),
                  "tracks" if node[0] == "segment" else "arc tracks", self.net_name(node))

    def _zone(self, node):
        zone_layer = layer_of(node)
        fills = children(node, "filled_polygon")
        net = self.net_name(node)
        for fp in fills:
            pts = [pt(p) for p in child(fp, "pts")[1:] if p[0] == "xy"]
            if len(pts) >= 3:
                self._add(layer_of(fp) or zone_layer, Polygon(pts).buffer(0), "zone fills", net)
        if not fills:
            if child(node, "keepout"):
                self.b.skipped["keepout / rule areas (no copper by design)"] += 1
            else:
                self.b.skipped["zones with no fill (unfilled - press B in KiCad and save)"] += 1

    def _graphic(self, node, T, in_footprint=False):
        layer = layer_of(node)
        geom, closed, w, filled = graphic(node, T)
        if geom is None or geom.is_empty:
            return
        if layer == "Edge.Cuts":
            (self.b.edge_closed if closed else self.b.edge_open).append(geom)
            self.b.found["outline shapes on Edge.Cuts"] += 1
        else:
            self._add(layer, painted(geom, closed, w, filled), "footprint graphics" if in_footprint else "graphics")

    def _text(self, node, T=lambda p: p, subst=None):
        S = P.Silkscreen
        b = self.b
        layer = layer_of(node)
        if not (layer in self.layers or layer in ("F.SilkS", "B.SilkS", "F.Mask", "B.Mask")):
            return
        h_ = child(node, "hide")
        effects = child(node, "effects") or []
        hidden = (yes(h_[1]) if h_ is not None and len(h_) > 1 else h_ is not None) \
            or "hide" in atoms(node) or "hide" in atoms(effects) \
            or (child(effects, "hide") is not None and yes((child(effects, "hide") + ["yes"])[1]))
        if hidden and not S.DRAW_HIDDEN_TEXT:
            return
        kind = node[0]
        if kind in ("gr_text_box", "fp_text_box", "dimension", "gr_dimension") or child(node, "at") is None:
            b.skipped[f"{kind} on {layer} (not modelled)"] += 1
            return
        text = str(node[2] if kind in ("fp_text", "property") else node[1]).replace("\\n", "\n")
        for key, val in (subst or {}).items():
            text = text.replace("${" + key + "}", val)
        vals = numbers(child(node, "at"))
        pos = T((vals[0], vals[1]))
        angle = vals[2] if len(vals) > 2 else 0.0          # text angles are stored absolute
        fnt = child(effects, "font") or []
        size = child(fnt, "size")
        h, w = (float(size[1]), float(size[2])) if size else (1.0, 1.0)
        bold = flag(fnt, "bold")
        italic = flag(fnt, "italic")
        thick = num(fnt, "thickness", (S.BOLD_THICKNESS_RATIO if bold else S.NORMAL_THICKNESS_RATIO) * h)
        just = child(effects, "justify")
        just = [str(j) for j in atoms(just)] if just else []
        if child(fnt, "face") is not None:
            if not S.DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT:
                b.skipped[f"TrueType text on {layer} (DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT is False)"] += 1
                return
            b.found[f"text in a TrueType face, drawn with the stroke font, on {layer}"] += 1
        geom = Text.render(text, pos, angle, h, w, thick, just, "mirror" in just, italic)
        self._add(layer, geom, "text")

    def _footprint(self, fp):
        b = self.b
        T = sh.make_transform(numbers(child(fp, "at")))
        fp_margin = num(fp, "solder_mask_margin")
        subst = {}
        for prop in children(fp, "property"):
            if len(prop) > 2 and not isinstance(prop[2], list):
                subst[str(prop[1]).upper()] = str(prop[2])
        for t in children(fp, "fp_text"):
            if len(t) > 2 and t[1] in ("reference", "value"):
                subst[t[1].upper()] = str(t[2])
        b.found["footprints"] += 1
        if children(fp, "model"):
            b.skipped["3D component models (bare board only)"] += len(children(fp, "model"))
        for node in fp[1:]:
            if not isinstance(node, list) or not node:
                continue
            if node[0] in GRAPHICS:
                self._graphic(node, T, in_footprint=True)
            elif node[0] == "pad":
                self._pad(node, T, fp_margin)
            elif node[0] == "zone":
                self._zone(node)
            elif node[0] in TEXT or (node[0] == "property" and layer_of(node)):
                self._text(node, T, subst)

    def _pad_shape(self, pad, w, h):
        shape = pad[3]
        if shape == "circle":
            return disk((0, 0), w / 2)
        if shape == "rect":
            return box(-w / 2, -h / 2, w / 2, h / 2)
        if shape == "oval":
            if abs(w - h) < 1e-9:
                return disk((0, 0), w / 2)
            d = abs(w - h) / 2
            return thicken(LineString([(-d, 0), (d, 0)] if w > h else [(0, -d), (0, d)]), min(w, h))
        if shape == "roundrect":
            r = min(num(pad, "roundrect_rratio", 0.25) * min(w, h), min(w, h) / 2)
            core = box(-w / 2 + r, -h / 2 + r, w / 2 - r, h / 2 - r) if r < min(w, h) / 2 else \
                LineString([(-w / 2 + r, -h / 2 + r), (w / 2 - r, h / 2 - r)])
            return core.buffer(r, quad_segs=sh.circle_quads(r)) if r > 0 else box(-w / 2, -h / 2, w / 2, h / 2)
        if shape == "trapezoid":
            rd = child(pad, "rect_delta")
            dx, dy = (float(rd[1]) / 2, float(rd[2]) / 2) if rd else (0.0, 0.0)
            return Polygon([(-w / 2 - dy, h / 2 + dx), (w / 2 + dy, h / 2 - dx),
                            (w / 2 - dy, -h / 2 + dx), (-w / 2 + dy, -h / 2 - dx)])
        if shape == "custom":
            opts = child(pad, "options")
            anchor = child(opts, "anchor")[1] if opts and child(opts, "anchor") else "circle"
            parts = [disk((0, 0), w / 2) if anchor == "circle" else box(-w / 2, -h / 2, w / 2, h / 2)]
            for prim in (child(pad, "primitives") or [])[1:]:
                if isinstance(prim, list) and prim[0] in GRAPHICS:
                    geom, closed, pw, filled = graphic(prim, lambda p: p)
                    parts.append(painted(geom, closed, pw, filled))
            return union(parts)
        self.b.skipped[f"pads of shape {shape}"] += 1
        return EMPTY

    def _pad(self, pad, T, fp_margin):
        b, C = self.b, P.Copper
        ptype = pad[2]
        vals = numbers(child(pad, "at"))
        pos = T((vals[0], vals[1]))
        ang = vals[2] if len(vals) > 2 else 0.0            # pad angles are stored absolute
        size = child(pad, "size")
        w, h = float(size[1]), float(size[2])
        drill = child(pad, "drill")
        net = self.net_name(pad)

        def place(g, offset=(0.0, 0.0)):
            g = affinity.translate(g, *offset)
            return affinity.translate(affinity.rotate(g, -ang, origin=(0, 0)), *pos)

        offset, hole = (0.0, 0.0), EMPTY
        if drill is not None:
            off = child(drill, "offset")
            offset = (float(off[1]), float(off[2])) if off else (0.0, 0.0)
            a = atoms(drill)
            if a and a[0] == "oval":
                dw, dh = float(a[1]), float(a[2]) if len(a) > 2 else float(a[1])
                d = abs(dw - dh) / 2
                hole = disk((0, 0), dw / 2) if d < 1e-9 else thicken(
                    LineString([(-d, 0), (d, 0)] if dw > dh else [(0, -d), (0, d)]), min(dw, dh))
            elif a:
                hole = disk((0, 0), float(a[0]) / 2)
            hole = place(hole)
        shape = place(self._pad_shape(pad, w, h), offset if drill is not None else (0.0, 0.0))
        layers = self._expand(child(pad, "layers")[1:])
        margin = num(pad, "solder_mask_margin")
        margin = margin if margin is not None else (fp_margin if fp_margin is not None else b.mask_clearance)
        last = len(self.layers) - 1
        if ptype == "np_thru_hole":
            if not hole.is_empty and P.Board.INCLUDE_NON_PLATED_HOLES:
                b.holes.append(Hole(hole, 0, last, False, "", 0.0))
            b.found["non-plated holes"] += 1
        else:
            for l in layers:
                if l in self.layers:
                    b.copper_items[l].append((shape, net))
            if ptype == "thru_hole" and not hole.is_empty:
                b.holes.append(Hole(hole, 0, last, True, net, C.PTH_WALL_MM))
            b.found["pads"] += 1
        for side in ("F", "B"):
            if f"{side}.Mask" in layers:
                b.mask_open_items[side].append(shape.buffer(margin) if margin else shape)
                b.found[f"pad mask openings on {side}.Mask"] += 1

    def _via(self, node):
        b, C = self.b, P.Copper
        x, y = pt(child(node, "at"))
        size, drill = num(node, "size"), num(node, "drill")
        ends = [str(l) for l in child(node, "layers")[1:]]
        span = self._span(ends[0], ends[-1]) if len(ends) >= 2 else self.layers
        net = self.net_name(node)
        pad = disk((x, y), size / 2)
        prune = C.HONOUR_REMOVE_UNUSED_LAYERS and flag(node, "remove_unused_layers")
        keep_ends = flag(node, "keep_end_layers")
        for l in span:
            if prune and not (keep_ends and l in (span[0], span[-1])):
                self.conditional_pads.append((l, pad, net))
            else:
                b.copper_items[l].append((pad, net))
        i, j = self.layers.index(span[0]), self.layers.index(span[-1])
        b.holes.append(Hole(disk((x, y), drill / 2), i, j, True, net, C.VIA_WALL_MM))
        through = i == 0 and j == len(self.layers) - 1
        b.found["through vias" if through else "blind/buried vias"] += 1
        tent = dict(b.tent_default)
        vt = child(node, "tenting")
        if vt is not None:
            for side, key in (("F", "front"), ("B", "back")):
                c = child(vt, key)
                if c is not None:
                    tent[side] = yes(c[1])
                elif key in atoms(vt):
                    tent[side] = True
        b.via_tenting.append((pad, span, tent))


# ---- outline ---------------------------------------------------------------------------------------------
def outline_from(b, log):
    B = P.Board
    rings = list(b.edge_closed)
    if b.edge_open:
        digits = max(0, round(-math.log10(B.OUTLINE_LINE_SNAP_MM)))
        noded = shapely.union_all([LineString(np.round(np.asarray(g.coords), digits)) for g in b.edge_open])
        faces = list(polygonize(noded))
        rings += [Polygon(f.exterior) for f in faces]
        if not faces:
            log("warning: Edge.Cuts lines/arcs do not form a closed outline")
    uniq = []
    for r in rings:
        if r.is_valid and r.area > 1e-9 and not any(r.symmetric_difference(u).area < 1e-6 for u in uniq):
            uniq.append(r)
    if not uniq:
        if B.OUTLINE_FALLBACK == "error":
            raise ValueError("no Edge.Cuts outline and OUTLINE_FALLBACK is 'error'")
        log(f"warning: no Edge.Cuts outline; using the copper's convex hull + {B.OUTLINE_FALLBACK_MARGIN_MM} mm")
        allcu = union([g for gs in b.copper_items.values() for g, _ in gs])
        return allcu.convex_hull.buffer(B.OUTLINE_FALLBACK_MARGIN_MM)
    depth = [sum(1 for j, o in enumerate(uniq) if j != i and o.contains(s)) for i, s in enumerate(uniq)]
    solid = union([s for s, d in zip(uniq, depth) if d % 2 == 0])
    cut = union([s for s, d in zip(uniq, depth) if d % 2 == 1])
    return solid.difference(cut)


# ---- resolve -------------------------------------------------------------------------------------------------
def via_openings(b):
    """Mask openings over vias that are not tented, per Copper_Parameters.VIA_TENTING."""
    C = P.Copper
    out = {"F": [], "B": []}
    for pad, span, tent in b.via_tenting:
        for side, layer in (("F", "F.Cu"), ("B", "B.Cu")):
            tented = {"file": tent[side], "tented": True, "open": False}[C.VIA_TENTING]
            if layer in span and not tented:
                out[side].append(pad.buffer(b.mask_clearance) if b.mask_clearance else pad)
    return out


def edge_plating(b, drills, log):
    """Copper band inside the outline when the board edge is plated (Copper_Parameters.EDGE_PLATING).
    Sets b.edge_band (board frame) and b.edge_net, and moves other nets' copper out of the band."""
    C = P.Copper
    plated = {"file": b.stackup.edge_plating, "yes": True, "no": False}[C.EDGE_PLATING]
    b.edge_band, b.edge_net = None, None
    if not plated:
        return
    band = sh.snap(sh.diff(b.outline, b.outline.buffer(-C.EDGE_PLATING_WALL_MM)))
    hole = b.to_board_T(drills(lambda h: True))          # every hole that reaches the edge interrupts the plating
    band = sh.diff(band, hole)
    if C.EDGE_PLATING_NET == "auto":
        touching = defaultdict(float)
        for l in b.layers:
            for net, r in b.copper[l].items():
                a = r.intersection(band).area
                if a > 0:
                    touching[net] += a
        named = {n: a for n, a in touching.items() if n != C.NO_NET_NAME}
        net = max(named, key=named.get) if named else C.NO_NET_NAME
    else:
        net = C.EDGE_PLATING_NET
    moved = Counter()
    for l in b.layers:
        for other in list(b.copper[l]):
            if other != net and b.copper[l][other].intersects(band):
                inside = sh.inter(b.copper[l][other], band)
                if inside.area > 0:
                    moved[other] += 1
                    b.copper[l][other] = sh.diff(b.copper[l][other], band)
                    if b.copper[l][other].is_empty:
                        del b.copper[l][other]
                    b.copper[l][net] = sh.snap(union([b.copper[l].get(net, EMPTY), inside]))
    for other, n in moved.items():
        log(f"edge plating: copper of net {other!r} inside the edge band moved to net {net!r} on {n} layer(s)")
    b.edge_band, b.edge_net = band, net
    b.found["edge plating band (net " + net + ")"] += 1


def resolve(b, log):
    """KiCad-frame items -> board-frame regions, snapped; holes applied per layer span."""
    R = P.Run
    outline_k = outline_from(b, log)
    minx, miny, maxx, maxy = outline_k.bounds
    if R.ORIGIN == "center":
        cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
        b.transform_note = f"origin: outline centre ({cx:.4f}, {cy:.4f}) in KiCad coordinates"
    else:
        cx, cy = 0.0, 0.0
        b.transform_note = "origin: KiCad page origin"
    b.to_board = (cx, cy)
    # KiCad (x, y down) -> board (x - cx, -(y - cy)): Y up, F.Cu toward +Z
    T = lambda g: sh.snap(affinity.affine_transform(sh.polys_only(g), [1, 0, 0, -1, -cx, cy])) \
        if g is not None and not g.is_empty else EMPTY
    b.to_board_T = T
    layers, last = b.layers, len(b.layers) - 1
    b.outline = T(outline_k)
    C = P.Copper
    # castellations: plated holes the outline cuts through
    castellate = C.CASTELLATION == "auto" or (C.CASTELLATION == "file" and b.stackup.castellated_pads)
    for h in b.holes:
        if h.plated and not outline_k.contains(h.drill) and h.drill.intersects(outline_k):
            b.found["castellated holes (plated holes cut by the board edge)"] += 1
            if castellate:
                h.wall = C.CASTELLATION_WALL_MM
            else:
                h.plated, h.wall = False, 0.0
                b.skipped["castellation plating (CASTELLATION is 'off')"] += 1
    if C.CASTELLATION == "file" and not b.stackup.castellated_pads and \
            b.found["castellated holes (plated holes cut by the board edge)"]:
        b.notes.append("plated holes cross the board edge but the stackup has no (castellated_pads yes); "
                       "set Copper.CASTELLATION = 'auto' to plate them")

    def drills(pred):
        return union([h.drill for h in b.holes if pred(h)])

    def bores(pred):
        return union([h.drill.buffer(-h.wall) if h.wall > 0 else h.drill for h in b.holes if pred(h)])

    b.slab = [sh.diff(b.outline, T(drills(lambda h, k=k: h.i <= k and h.j >= k + 1))) for k in range(last)]
    b.bores_side = {"F": T(bores(lambda h: h.i == 0)), "B": T(bores(lambda h: h.j == last))}
    for k, l in enumerate(layers):
        if k in (0, last):
            cut = bores(lambda h, k=k: h.i <= k <= h.j)         # outer copper caps the barrel
        else:
            cut = drills(lambda h, k=k: h.i <= k <= h.j)        # inner copper stops at the drill wall
        per_net = defaultdict(list)
        for g, net in b.copper_items.get(l, []):
            per_net[net].append(g)
        regions = {}
        for net, gs in per_net.items():
            cu = union(gs).intersection(outline_k).difference(cut)
            if P.Geometry.SIMPLIFY_TOLERANCE_MM > 0:
                cu = cu.simplify(P.Geometry.SIMPLIFY_TOLERANCE_MM)
            cu = T(cu)
            if not cu.is_empty:
                regions[net] = cu
        # copper of different nets never overlaps on a real board; if the file has overlaps, the
        # first net keeps the shared area so the solids stay disjoint
        taken = EMPTY
        for net in list(regions):
            if not taken.is_empty:
                regions[net] = sh.diff(regions[net], taken)
            taken = union([taken, regions[net]])
        b.copper[l] = {n: r for n, r in regions.items() if not r.is_empty}
        b.copper_all[l] = sh.snap(union(list(b.copper[l].values())))
    edge_plating(b, drills, log)
    if b.edge_band is not None:
        # the band takes the laminate's place at the edge (like a barrel in its drill hole); on the
        # outer layers it is part of the edge net's copper, which caps it like an annular ring
        b.slab = [sh.diff(s, b.edge_band) for s in b.slab]
        for l in (layers[0], layers[-1]):
            b.copper[l][b.edge_net] = sh.snap(union([b.copper[l].get(b.edge_net, EMPTY), b.edge_band]))
    for l in layers:
        b.copper_all[l] = sh.snap(union(list(b.copper[l].values())))
    for k, l in enumerate(layers):
        if 0 < k < last:
            hole = T(drills(lambda h, k=k: h.i <= k <= h.j))
            lam = sh.diff(sh.diff(b.outline, hole), b.copper_all[l])
            b.band_laminate[l] = sh.diff(lam, b.edge_band) if b.edge_band is not None else lam
    spans = defaultdict(list)
    for h in b.holes:
        if h.plated:
            spans[(h.i, h.j, h.net)].append(h.drill.difference(h.drill.buffer(-h.wall)).intersection(outline_k))
    b.barrels = [(T(union(rings)), i, j, net) for (i, j, net), rings in spans.items()]
    if b.edge_band is not None:
        b.barrels.append((b.edge_band, 0, last, b.edge_net))
    vo = via_openings(b)
    for side in ("F", "B"):
        openings = union(b.mask_open_items[side] + vo[side])
        b.mask_open[side] = T(openings.intersection(outline_k))
        silk = union(b.silk_items[side]).intersection(outline_k).difference(
            bores(lambda h: h.i == 0) if side == "F" else bores(lambda h: h.j == last))
        if not P.Silkscreen.SILKSCREEN_OVER_COPPER:      # no ink where there is no mask (openings, bare copper)
            silk = silk.difference(openings)
        b.silk[side] = T(silk)
    return b


def breakdown(raw, log):
    b = _Collector(raw, log).b
    unfilled = b.skipped.get("zones with no fill (unfilled - press B in KiCad and save)", 0)
    if unfilled:
        log(f"warning: {unfilled} copper zone(s) have no fill stored in the file and are ignored "
            "(fill the zones in KiCad, press B, and save; see Copper_Parameters)")
    _, note = Text.font()
    b.notes.append(note)
    return resolve(b, log)
