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
    centre: tuple = None   # centre of a round hole (None for slots); with the drill radius it is the exact circle
    radius: float = 0.0


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
    mask_clearance: float = 0.0
    via_pads: list = field(default_factory=list)      # exact (centre, radius) of every via pad
