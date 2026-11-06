"""What the Verifier asks of each part in simulation mode (kese/s8_verify/meshes.py and volumes.py):
its mesh closed and wound the same way throughout, and its volume from its faces, its slices, its
prisms and its mesh.  With the Verifier on, the worker that builds a part also checks it, while the
part is at hand (kese/s6_assemble/boundaries.py), and stage 8 reads the checks from the Model;
otherwise stage 8 makes them itself.  Either way the numbers, and so report.txt, are the same."""
from typing import NamedTuple

import numpy as np
import shapely

from kese.core import shapes2d as sh
from kese.core.boundary import spanning_prisms
from kese.core.graph import connected_components
from parameters import P


class MeshCheck(NamedTuple):
    closed: bool            # every edge in two faces, once the vertices are merged on the grid
    consistent: bool        # every shared edge run opposite ways by its two faces
    merged_volume: float    # the merged mesh's, in output units cubed
    volume: float           # the mesh's as written, in output units cubed


class PieceCheck(NamedTuple):
    """A part's prisms and slices compared piece by piece (pieces_compared)."""
    pieces: int             # the pieces compared
    gone: int               # pieces of prisms with no slice left on them, or of slices with no prism under them
    worst: float            # mm3 the prisms hold more than the slices, in the piece furthest past what it may
    volume: float           # mm3: that piece's slices
    at: tuple               # (x, y, z0, z1) mm: the middle of that piece's box, and its slice's heights


class VolumeCheck(NamedTuple):
    faces: float            # mm3: between the part's faces (Boundary.volume)
    slices: float           # mm3: of its slices
    prisms: float           # mm3: of its prisms, before the pinch points were opened
    pieces: PieceCheck | None = None    # where prisms and slices differ by more than allowed in all


def mesh_check(mesh, units):
    """A finished mesh (in `units`) checked, its vertices merged at the snapping grid
    (Geometry.SNAP_GRID_MM, Verifier.VERIFY_MERGE_EXTRA_DIGITS finer) whatever the units."""
    scale = 1000.0 if units == "m" else 1.0
    m = mesh.copy()
    m.merge_vertices(digits_vertex=int(round(-np.log10(P.Geometry.SNAP_GRID_MM / scale))) + P.Verifier.VERIFY_MERGE_EXTRA_DIGITS)
    return MeshCheck(m.is_watertight, m.is_winding_consistent, m.volume, mesh.volume)


def allowed(volume):
    """mm3 two of the volumes of a part, or of a piece, may differ by, as the numerical noise of areas
    and meshes: Verifier.VERIFY_VOLUME_TOLERANCE of it, and Verifier.VERIFY_VOLUME_NOISE_MM3 (volumes: a
    number, or an array of them)."""
    return P.Verifier.VERIFY_VOLUME_TOLERANCE * np.abs(volume) + P.Verifier.VERIFY_VOLUME_NOISE_MM3


def opened_allowed(volume):
    """What a part's, or a piece's, slices may lack of its prisms, or hold more: the noise, and what
    opening pinch points and sharing vertices may move (Verifier.VERIFY_OPENED_VOLUME_MM3)."""
    return allowed(volume) + P.Verifier.VERIFY_OPENED_VOLUME_MM3


def whole(check):
    """Whether a part's slices hold what its prisms do (a VolumeCheck): in all, or else in every piece,
    none gone."""
    if abs(check.prisms - check.slices) <= opened_allowed(check.slices):
        return True
    p = check.pieces
    return bool(p is not None and not p.gone and abs(p.worst) <= opened_allowed(p.volume))


def volume_check(boundary, prisms):
    """A part's volumes, from its Boundary and its prisms, and where they differ by more than allowed
    in all, piece by piece."""
    faces, slices = boundary.volume(), boundary.volume_of_slices()
    built = sum(p.region.area * (p.z1 - p.z0) for p in prisms)
    far = abs(built - slices) > opened_allowed(slices)
    return VolumeCheck(faces, slices, built, pieces_compared(boundary.slices, prisms) if far else None)


def pieces_compared(slices, prisms):
    """A part's prisms and its slices, (z0, z1, region), compared piece by piece -> PieceCheck.  Stage 6
    moves each piece's edges a grid step here and there as it shares vertices, and opens its pinch
    points: on a board of thousands of holes that adds up past what a part may differ by in all, while
    no piece differs by more than a little.  A piece: per slice, the prisms' pieces that span it and
    the slice's own pieces, joined where they touch (a hole's finish, say, as built and as sliced)."""
    count, gone, worst = 0, 0, (-np.inf, 0.0, 0.0, (0.0, 0.0, 0.0, 0.0))
    for z0, z1, region in slices:
        given = [g for i in spanning_prisms(prisms, z0, z1) for g in shapely.get_parts(sh.polys_only(prisms[i].region))]
        both = np.array(given + list(shapely.get_parts(sh.polys_only(region))), dtype=object)
        if not len(both):
            continue
        n, group = connected_components(len(both), *shapely.STRtree(both).query(both, predicate="intersects"))
        sliced = np.arange(len(both)) >= len(given)
        area = shapely.area(both)
        lacks = np.bincount(group, weights=np.where(sliced, -area, area), minlength=n) * (z1 - z0)
        held = np.bincount(group, weights=np.where(sliced, area, 0.0), minlength=n) * (z1 - z0)
        count += n
        gone += n - len(np.intersect1d(group[sliced], group[~sliced]))
        past = np.abs(lacks) - opened_allowed(held)
        k = int(np.argmax(past))
        if past[k] > worst[0]:
            box = shapely.bounds(both[group == k])
            middle = (box[:, :2].min(axis=0) + box[:, 2:].max(axis=0)) / 2
            worst = (past[k], float(lacks[k]), float(held[k]), (*middle.round(6).tolist(), z0, z1))
    return PieceCheck(count, gone, *worst[1:])


def part_check(mesh, boundary, prisms, units):
    """(MeshCheck, or None without a mesh; VolumeCheck) of one part."""
    return (mesh_check(mesh, units) if mesh is not None else None), volume_check(boundary, prisms)
