"""The volume check of stage 8, for solids built without a kernel (Run.BUILD_WITH_KERNELS off).
A closed surface encloses, by the divergence theorem, the sum over its flat faces of height
times signed area (positive looking up, negative looking down; walls are vertical and count for
nothing).  So every part's Boundary must come to the volume of its material slice by slice, and
the mesh cut from the same faces must enclose that volume too.  The prisms the part was built
from come to the same volume as well, less the pinch points that were opened (a small disc cut
out around each, see kese/core/pinches.py)."""
from parameters import P

RELATIVE_TOLERANCE = 1e-7       # of the part's volume: numerical noise of areas and meshes
OPENED_TOLERANCE_MM3 = 1e-3     # what the opened pinch points may take from the prisms' volume


def volumes_agree(model):
    """(ok, report lines): per part, the volume from its faces, its slices, its mesh and its prisms."""
    if model.mode != "simulation" or P.Run.BUILD_WITH_KERNELS:
        return True, []
    scale = 1000.0 if model.units == "m" else 1.0
    prisms = model.prismset.by_part()
    ok, lines = True, []
    for part, boundary in model.boundaries.items():
        faces, slices = boundary.volume(), boundary.volume_of_slices()
        mesh = float(model.meshes[part].volume) * scale ** 3 if part in model.meshes else 0.0
        built = sum(p.region.area * (p.z1 - p.z0) for p in prisms[part])
        allowed = RELATIVE_TOLERANCE * max(slices, 1e-9) + 1e-9
        closed = abs(faces - slices) <= allowed and abs(mesh - slices) <= allowed
        whole = abs(built - slices) <= allowed + OPENED_TOLERANCE_MM3
        ok &= closed and whole
        lines.append(f"  {part:36s} volume from faces {faces:.6f} mesh {mesh:.6f} slices {slices:.6f} "
                     f"prisms {built:.6f} mm3 closed={closed} whole={whole}")
    return ok, lines
