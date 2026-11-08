"""Items: every element of the board file as a flat shape on its layer, with its net, in KiCad's
frame (mm, Y down).  Filled by stage 2 (collect)."""
from collections import Counter, defaultdict
from dataclasses import dataclass, field


@dataclass
class Hole:
    drill: object          # outline of the drilled hole
    i: int                 # top copper layer index it spans
    j: int                 # bottom copper layer index
    plated: bool
    net: str
    wall: float            # plating wall thickness (0 for NPTH)
    castellated: bool = False   # plated and cut by the board edge (Copper.CASTELLATION)
    kind: str = "drill"         # "drill"; "backdrill" (KiCad 10, drills a plated hole out from layer i through j);
                                # "knockout" (a counterbore or countersink where it crosses copper layer i = j)
    protect: object = None      # a via's Protection (KiCad 10), or None
    of: int = -1                # a backdrill or knockout: the index in Items.holes of the hole it machines


@dataclass
class Protection:
    """A via's protection (KiCad 10, IPC-4761), as stage 2 resolves it from the via and the board."""
    filled: bool = False
    capped: bool = False
    plugged: dict = field(default_factory=lambda: {"F": False, "B": False})
    covered: dict = field(default_factory=lambda: {"F": False, "B": False})
    opened: dict = field(default_factory=lambda: {"F": False, "B": False})   # an end a backdrill or post machining opens

    def copper_shut(self, side, fill):
        """Whether copper shuts the hole at its end on `side` (the outer copper is then not cut by it):
        a cap, or a copper fill (fill: Copper.VIA_FILL)."""
        return not self.opened[side] and (self.capped or (self.filled and fill == "copper"))

    def shut(self, side):
        """Whether anything shuts the hole at its end on `side`, so that the solder mask can span it:
        a cap, a fill, or a plug or covering on that side."""
        return not self.opened[side] and (self.capped or self.filled or self.plugged[side] or self.covered[side])


@dataclass
class PostMachining:
    """A counterbore or countersink (KiCad 10) of a pad or via, KiCad frame."""
    center: tuple
    side: str                   # "F" or "B": the face it is cut from
    mode: str                   # "counterbore" or "countersink"
    size: float                 # diameter at the face
    depth: float                # from the face, copper included (a countersink of depth 0: the whole cone)
    angle: float = 0.0          # a countersink's included angle, degrees
    of: int = -1                # index in Items.holes of the hole it machines (-1: none)


@dataclass
class Items:
    raw: object                                       # the RawBoard they were read from
    name: str
    layers: list                                      # copper layers, outermost first
    stackup: object
    nets: dict = field(default_factory=dict)          # net number as written -> net name
    found: Counter = field(default_factory=Counter)   # what was read, for the report
    skipped: Counter = field(default_factory=Counter) # what was left out, for the report
    notes: list = field(default_factory=list)
    copper_items: dict = field(default_factory=lambda: defaultdict(list))   # layer -> [(geom, net)]
    mask_open_items: dict = field(default_factory=lambda: {"F": [], "B": []})
    silk_items: dict = field(default_factory=lambda: {"F": [], "B": []})
    edge_closed: list = field(default_factory=list)
    edge_open: list = field(default_factory=list)
    holes: list = field(default_factory=list)
    via_tenting: list = field(default_factory=list)   # (pad geom, span layers, {"F": tented, "B": tented})
    tent_default: dict = field(default_factory=dict)
    tent_source: str = ""
    via_protection: dict = field(default_factory=dict)  # KiCad 10: covering, plugging, ... when a via does not say
    post_machining: list = field(default_factory=list)  # PostMachining of pads and vias (KiCad 10)
    mask_clearance: float = 0.0
    mask_min_width: float = 0.0          # setup (solder_mask_min_width): narrower mask webs are not made
    via_classes: tuple = None            # the net classes' via sizes, read at the first via that gives none
    text_vars: object = None             # s2_collect/text_vars.py TextVars, read at the first text with ${...}
