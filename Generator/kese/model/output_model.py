"""The Model: one board ready to be written, as each part's faces (for STEP) and meshes (for
glb / stl / obj)."""
from dataclasses import dataclass, field

from kese.model.prisms import PrismSet


@dataclass
class Model:
    """What stage 6 (assemble) hands to stage 7 (write): meshes for glb/stl/obj, in output units and
    orientation, and each part's Boundary, the faces STEP is written from (mm, board frame, taken to
    the output by `transform`); with Run.BUILD_WITH_KERNELS STEP is built from the prisms instead."""
    name: str
    mode: str
    prismset: PrismSet
    meshes: dict                 # part name -> trimesh.Trimesh (output units)
    materials: dict              # part name -> material dict (colour, alpha, ...)
    props: dict                  # part name -> physical/EM properties
    transform: object            # 4x4 numpy matrix mm-board -> output
    units: str
    report: list                 # lines
    circles: list = field(default_factory=list)   # exact (centre, radius) of holes and via pads, mm board frame
    boundaries: dict = field(default_factory=dict)  # part name -> Boundary (mm, board frame), the faces STEP writes
