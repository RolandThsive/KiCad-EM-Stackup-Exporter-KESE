"""The board stack-up: layer order, thicknesses, materials and the height of every layer.

Everything is in mm, measured from the laminate's mid-plane (F side positive)."""
from dataclasses import dataclass, field

from kese.Common.sexp import child, children, num
from parameters import P


@dataclass
class Dielectric:
    name: str                 # "dielectric 1"
    kind: str                 # "core" / "prepreg"
    material: str
    thickness: float
    epsilon_r: float
    loss_tangent: float
    above: str                # copper layer above
    below: str                # copper layer below


@dataclass
class Stackup:
    copper_layers: list                       # outermost first: F.Cu, In1.Cu, ..., B.Cu
    copper_thickness: dict                    # layer -> foil thickness (mm)
    dielectrics: list                         # Dielectric, top to bottom
    laminate_thickness: float                 # sum of dielectrics + inner copper
    thickness_source: str
    mask_thickness: float | None              # from the stackup, or None
    colors: dict = field(default_factory=dict)   # layer -> colour name from the stackup
    copper_finish: str | None = None
    file_board_thickness: float | None = None
    edge_plating: bool = False                # (edge_plating yes) in the stackup
    castellated_pads: bool = False            # (castellated_pads yes) in the stackup
    band: dict = field(default_factory=dict)  # copper layer -> (z_lo, z_hi) after heights()
    half: float = 0.0

    def inner(self):
        return self.copper_layers[1:-1]

    def heights(self, outer_copper_t):
        """Fill self.band: z range of every copper layer.  Outer copper sits on the laminate faces
        (outer_copper_t = {"F.Cu": finished thickness, "B.Cu": ...}); inner copper lies inside."""
        self.half = self.laminate_thickness / 2
        band = {"F.Cu": (self.half, self.half + outer_copper_t["F.Cu"]),
                "B.Cu": (-self.half - outer_copper_t["B.Cu"], -self.half)}
        z = self.half
        for i, d in enumerate(self.dielectrics):
            z -= d.thickness
            if i < len(self.dielectrics) - 1:
                l = d.below
                band[l] = (z - self.copper_thickness[l], z)
                z -= self.copper_thickness[l]
        self.band = band
        return band

    def dielectric_z(self, i):
        """(z_lo, z_hi) of dielectric i."""
        d = self.dielectrics[i]
        hi = self.half if i == 0 else self.band[d.above][0]
        lo = -self.half if i == len(self.dielectrics) - 1 else self.band[d.below][1]
        return lo, hi


def read_stackup(tree, copper_layers, file_thickness, log):
    """Build the Stackup from the board's (setup (stackup ...)) or from the parameters."""
    B, C, M = P.Board, P.Copper, P.SolderMask
    setup = child(tree, "setup") or []
    st = child(setup, "stackup")
    cu_t, colors, mask_t, finish = {}, {}, None, None
    flags = {"edge_plating": False, "castellated_pads": False}
    gaps = []                          # dielectric layers between consecutive copper layers
    found = False
    if st:
        found = True
        acc, seen_cu = [], False
        for l in children(st, "layer"):
            name = str(l[1])
            t = sum(float(c[1]) for c in children(l, "thickness")) or None
            typ = (child(l, "type") or [None, ""])[1].lower()
            col = child(l, "color")
            if col:
                colors[name] = str(col[1])
            if name.endswith(".Cu"):
                if t and C.USE_STACKUP_COPPER_THICKNESS:
                    cu_t[name] = t
                if seen_cu:
                    gaps.append(acc)
                acc, seen_cu = [], True
            elif name.endswith(".Mask"):
                if t and M.USE_STACKUP_MASK_THICKNESS and mask_t is None:
                    mask_t = t
            elif seen_cu and (typ in ("core", "prepreg", "dielectric") or name.startswith("dielectric")):
                acc.append(Dielectric(
                    name=name, kind=typ if typ in ("core", "prepreg") else B.DEFAULT_DIELECTRIC_TYPE,
                    material=(child(l, "material") or [None, B.DEFAULT_DIELECTRIC_MATERIAL])[1],
                    thickness=t or 0.0,
                    epsilon_r=num(l, "epsilon_r", B.DEFAULT_EPSILON_R) if B.USE_STACKUP_EPSILON_R else B.DEFAULT_EPSILON_R,
                    loss_tangent=num(l, "loss_tangent", B.DEFAULT_LOSS_TANGENT) if B.USE_STACKUP_LOSS_TANGENT else B.DEFAULT_LOSS_TANGENT,
                    above="", below=""))
        cf = child(st, "copper_finish")
        if cf:
            finish = str(cf[1])
        flags = {k: str((child(st, k) or [None, "no"])[1]).lower() == "yes" for k in ("edge_plating", "castellated_pads")}
    n = len(copper_layers)
    for l in copper_layers:
        if l not in cu_t:
            cu_t[l] = C.DEFAULT_OUTER_FOIL_MM if l in ("F.Cu", "B.Cu") else C.DEFAULT_INNER_FOIL_MM

    usable = found and len(gaps) == n - 1 and all(sum(d.thickness for d in g) > 0 for g in gaps)
    inner_cu = sum(cu_t[l] for l in copper_layers[1:-1])
    if B.BOARD_THICKNESS_MM:
        laminate = B.BOARD_THICKNESS_MM
        source = "Board.BOARD_THICKNESS_MM"
        if usable:   # keep the stackup's proportions, scaled to the requested laminate
            total = sum(d.thickness for g in gaps for d in g)
            scale = (laminate - inner_cu) / total
            for g in gaps:
                for d in g:
                    d.thickness *= scale
            source += " (stackup dielectric proportions kept)"
    elif usable:
        laminate = sum(d.thickness for g in gaps for d in g) + inner_cu
        source = f"stackup dielectrics (+ inner copper); board total in file {file_thickness} mm"
    else:
        laminate = file_thickness or 1.6
        source = "file (general (thickness)) - no usable stackup" if file_thickness else "default 1.6 mm (no thickness in file)"
    if not usable:
        if B.DIELECTRIC_SPLIT != "even":
            log(f"warning: DIELECTRIC_SPLIT={B.DIELECTRIC_SPLIT!r} unknown, using 'even'")
        each = (laminate - inner_cu) / (n - 1)
        gaps = [[Dielectric(f"dielectric {k + 1}", B.DEFAULT_DIELECTRIC_TYPE, B.DEFAULT_DIELECTRIC_MATERIAL, each,
                            B.DEFAULT_EPSILON_R, B.DEFAULT_LOSS_TANGENT, "", "")] for k in range(n - 1)]
    # one Dielectric object per gap (a gap made of several prepreg plies is one solid of the summed thickness)
    dielectrics = []
    for k, g in enumerate(gaps):
        d = g[0]
        if len(g) > 1:
            d = Dielectric(" + ".join(x.name for x in g), g[0].kind, g[0].material, sum(x.thickness for x in g),
                           g[0].epsilon_r, g[0].loss_tangent, "", "")
        d.above, d.below = copper_layers[k], copper_layers[k + 1]
        dielectrics.append(d)
    return Stackup(copper_layers=copper_layers, copper_thickness=cu_t, dielectrics=dielectrics,
                   laminate_thickness=laminate, thickness_source=source, mask_thickness=mask_t,
                   colors=colors, copper_finish=finish, file_board_thickness=file_thickness,
                   edge_plating=flags["edge_plating"], castellated_pads=flags["castellated_pads"])
