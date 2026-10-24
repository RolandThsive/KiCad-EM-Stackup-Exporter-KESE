"""Regions: the board as 2D regions per layer (and per net for copper) in the board frame (mm,
Y up), snapped to the grid, with the holes applied.  Made by stage 3 (resolve)."""
from dataclasses import dataclass, field


@dataclass
class Regions:
    items: object                                      # the Items they were resolved from
    layers: list                                       # copper layers, outermost first
    stackup: object
    outline: object = None
    copper: dict = field(default_factory=dict)         # layer -> {net: region}
    copper_all: dict = field(default_factory=dict)     # layer -> region (all nets)
    slab: list = field(default_factory=list)           # laminate between copper k and k+1
    band_laminate: dict = field(default_factory=dict)  # inner layer -> laminate beside its copper
    bores_side: dict = field(default_factory=dict)     # "F"/"B" -> open bores on that face
    barrels: list = field(default_factory=list)        # (ring region, i, j, net)
    circles: list = field(default_factory=list)        # exact (centre, radius) of drills, bores and via pads
    mask_open: dict = field(default_factory=dict)      # "F"/"B" -> openings
    mask: dict = field(default_factory=dict)           # "F"/"B" -> where the mask is (outline - bores - openings, pulled back)
    silk: dict = field(default_factory=dict)           # "F"/"B" -> silk
    transform_note: str = ""
    to_board: object = None                            # (cx, cy): the KiCad point that becomes the origin
    to_board_T: object = None                          # KiCad-frame shape -> board-frame shape
    edge_band: object = None
    edge_net: object = None
