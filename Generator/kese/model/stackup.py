"""The board stack-up: layer order, thicknesses, materials and the height of every layer.

Everything is in mm, measured from the laminate's mid-plane (F side positive)."""
from dataclasses import dataclass, field


@dataclass
class Ply:
    name: str                 # "dielectric 1 ply 2", or "dielectric 2" where its dielectric has one ply
    kind: str                 # "core" / "prepreg"
    material: str
    thickness: float
    epsilon_r: float
    loss_tangent: float
    frequency_hz: float = 1e9   # the frequency epsilon_r and loss_tangent are given at
    model: str = "constant"   # how they change with frequency: "constant" / "djordjevic_sarkar" / "table"
    of: str = ""              # its dielectric in the board file: "dielectric 1"
    number: int = 1           # its place in the gap, from the top, counting from 1
    count: int = 1            # how many plies its gap has in the board file
    holds: list = field(default_factory=list)    # built with the plies separate: the file's plies this solid is made of


@dataclass
class Dielectric:
    name: str                 # "dielectric 1"
    kind: str                 # "core" / "prepreg"
    material: str
    thickness: float
    epsilon_r: float
    loss_tangent: float
    above: str = ""           # copper layer above
    below: str = ""           # copper layer below
    frequency_hz: float = 1e9   # as its plies
    model: str = "constant"
    plies: list = field(default_factory=list)    # Ply, top to bottom: what the board file makes the gap of
    solids: list = field(default_factory=list)   # Ply, top to bottom: the plies as built with the plies separate


@dataclass
class Stackup:
    copper_layers: list                       # outermost first: F.Cu, In1.Cu, ..., B.Cu
    copper_thickness: dict                    # layer -> foil thickness (mm)
    dielectrics: list                         # Dielectric, top to bottom: one for each gap between two copper layers
    laminate_thickness: float                 # sum of dielectrics + inner copper
    thickness_source: str
    mask_thickness: float | None              # from the stackup, or None
    colors: dict = field(default_factory=dict)   # layer -> colour name from the stackup
    copper_finish: str | None = None
    edge_plating: bool = False                # (edge_plating yes) in the stackup
    castellated_pads: bool = False            # (castellated_pads yes) in the stackup
    mask_materials: dict = field(default_factory=dict)   # "F.Mask" / "B.Mask" -> {material, epsilon_r, loss_tangent} of the file
    band: dict = field(default_factory=dict)  # copper layer -> (z_lo, z_hi), set by stage 3 (s3_resolve/heights.py)
    half: float = 0.0                         # half the laminate thickness, set with band
