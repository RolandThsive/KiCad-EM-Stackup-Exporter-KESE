"""What the Verifier asks of each part in simulation mode (kese/s8_verify/meshes.py and volumes.py):
its mesh closed and wound the same way throughout, and its volume from its faces, its slices, its
prisms and its mesh.  With the Verifier on, the worker that builds a part also checks it, while the
part is at hand (kese/s6_assemble/boundaries.py), and stage 8 reads the checks from the Model;
otherwise stage 8 makes them itself.  Either way the numbers, and so report.txt, are the same."""
from typing import NamedTuple

import numpy as np

from parameters import P


class MeshCheck(NamedTuple):
    closed: bool            # every edge in two faces, once the vertices are merged on the grid
    consistent: bool        # every shared edge run opposite ways by its two faces
    merged_volume: float    # the merged mesh's, in output units cubed
    volume: float           # the mesh's as written, in output units cubed


class VolumeCheck(NamedTuple):
    faces: float            # mm3: between the part's faces (Boundary.volume)
    slices: float           # mm3: of its slices
    prisms: float           # mm3: of its prisms, before the pinch points were opened


def mesh_check(mesh, units):
    """A finished mesh (in `units`) checked, its vertices merged at the snapping grid
    (Geometry.SNAP_GRID_MM) whatever the units."""
    scale = 1000.0 if units == "m" else 1.0
    m = mesh.copy()
    m.merge_vertices(digits_vertex=int(round(-np.log10(P.Geometry.SNAP_GRID_MM / scale))) + 2)
    return MeshCheck(m.is_watertight, m.is_winding_consistent, m.volume, mesh.volume)


def volume_check(boundary, prisms):
    """A part's volumes, from its Boundary and its prisms."""
    return VolumeCheck(boundary.volume(), boundary.volume_of_slices(), sum(p.region.area * (p.z1 - p.z0) for p in prisms))


def part_check(mesh, boundary, prisms, units):
    """(MeshCheck, or None without a mesh; VolumeCheck) of one part."""
    return (mesh_check(mesh, units) if mesh is not None else None), volume_check(boundary, prisms)
