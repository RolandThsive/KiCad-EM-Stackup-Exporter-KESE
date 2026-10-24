"""The master geometry: a PrismSet.

A Prism is a flat region (shapely polygon, mm, board coordinates with Y up) between two
heights.  Stage 4 (geometry) makes them; stage 6 (assemble) turns them into triangle meshes
and stage 7 (write) into exact STEP solids, without recomputing anything."""
from dataclasses import dataclass, field


@dataclass
class Prism:
    part: str            # name of the solid this prism belongs to ("Copper_+3V3", "Top Solder Mask", ...)
    role: str            # "board", "copper", "plating", "mask", "mask_over_copper", "silk", "finish"
    region: object       # shapely (Multi)Polygon
    z0: float
    z1: float
    layer: str = ""      # KiCad layer or dielectric name
    net: str = ""        # net name for copper
    material: str = ""   # key into Color.MATERIALS (set by stage 5, materials)
    props: dict = field(default_factory=dict)   # EM / physical properties for materials.json


@dataclass
class PrismSet:
    regions: object = None                      # the Regions they were built from
    prisms: list = field(default_factory=list)
    notes: list = field(default_factory=list)   # free text for the report
    materials: dict = field(default_factory=dict)   # part name -> material dict (set by stage 5)

    def add(self, part, role, region, z0, z1, **kw):
        if region is None or region.is_empty or abs(z1 - z0) < 1e-12:
            return
        self.prisms.append(Prism(part, role, region, min(z0, z1), max(z0, z1), **kw))

    def parts(self):
        """Ordered unique part names."""
        seen, out = set(), []
        for p in self.prisms:
            if p.part not in seen:
                seen.add(p.part)
                out.append(p.part)
        return out

    def by_part(self):
        out = {}
        for p in self.prisms:
            out.setdefault(p.part, []).append(p)
        return out
