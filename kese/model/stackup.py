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
