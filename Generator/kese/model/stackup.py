"""The board stack-up: layer order, thicknesses, materials and the height of every layer.

Everything is in mm, measured from the laminate's mid-plane (F side positive)."""
from dataclasses import dataclass, field


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
    band: dict = field(default_factory=dict)  # copper layer -> (z_lo, z_hi), set by stage 4 (heights.py)
    half: float = 0.0                         # half the laminate thickness, set with band
