"""Shapes the corpus run (3,146 boards) found KESE handling badly: a triangle of no area that GEOS's
triangulation gives where points of a polygon's rings lie on one line is split away, the triangles
then closing on every ring edge and wound one way; and a visual face takes a vertex of the face at
the next height that lies on its edge, as the wall between them is split at it (else a crack up to 50 nm
wide beside the ink, where a ray of the Verifier fell through).

    python -m pytest tests/test_degenerate_shapes.py        (or:  python tests/test_degenerate_shapes.py)"""
import numpy as np
import shapely
from shapely.geometry import Polygon, box

from helpers import run_tests
from kese.core import shapes2d as sh
from kese.core.flat_triangles import flat_any, flats_split_away, twice_area
from kese.s6_assemble.skin_vertices import flats_sharing_vertices


def test_a_flat_triangle_is_split_away_and_the_triangles_close():
    xy = np.array([(0, 0), (2, 0), (4, 0), (4, 4), (0, 4)], dtype=float)     # (2, 0) on a straight run
    nxt = np.array([1, 2, 3, 4, 0])
    tri = np.array([[0, 1, 2], [0, 2, 4], [2, 3, 4]])                       # the first of no area
    assert flat_any(xy, tri)
    done = flats_split_away(xy, nxt, tri)
    assert not flat_any(xy, done) and abs(twice_area(xy, done).sum() / 2 - 16) < 1e-12
    edges = {(t[i], t[(i + 1) % 3]) for t in done.tolist() for i in range(3)}
    ring = set(zip(range(5), nxt.tolist()))
    assert ring <= edges and all((v, u) in edges or (u, v) in ring for u, v in edges)


def test_triangles_that_do_not_close_once_split_are_left_as_they_were():
    xy = np.array([(0, 0), (2, 0), (4, 0), (4, 4), (0, 4)], dtype=float)
    nxt = np.array([1, 2, 3, 4, 0])
    tri = np.array([[0, 1, 2], [2, 3, 4]])                                   # a triangle missing
    assert (flats_split_away(xy, nxt, tri) == tri).all()


def test_a_visual_face_takes_the_vertex_its_wall_is_split_at():
    g = sh.grid()
    ink = box(0, 0, 1, 1)
    off = (0.5, 1 + 0.5 * g)                                                  # half a grid step off the ink's top edge
    mask = Polygon(box(-1, -1, 2, 2).exterior, [[(0, 0), (1, 0), (1, 1), off, (0, 1)][::-1]])
    flats = {"Top Solder Mask": [(0.01, mask, True)], "Top Silkscreen": [(0.02, ink, True)]}
    slices = {"Top Solder Mask": [mask, sh.EMPTY], "Top Silkscreen": [sh.EMPTY, ink]}
    out = flats_sharing_vertices(flats, slices, [0.0, 0.01, 0.02])
    assert off in [tuple(p) for p in shapely.get_coordinates(out["Top Silkscreen"][0][1])]
    assert out["Top Solder Mask"][0][1] is mask                                # it had every vertex already

if __name__ == "__main__":
    run_tests(__file__)
