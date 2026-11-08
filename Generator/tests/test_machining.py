"""KiCad 10's backdrills, counterbores and countersinks (kese/s2_collect/machining.py,
s3_resolve/machining.py, s4_geometry/laminate.py), checked against KiCad 10 itself and against the
geometry of a cone:
  - a counterbore cuts to its depth from the copper's outer face, a floor inside an inner copper
    layer included; a countersink is a stack of cylinders within its tolerance of the cone, with a
    step at every copper face, and keeps the cone's volume;
  - the copper knocked out on each layer is what KiCad 10's pcbnew gives it
    (PAD::GetPostMachiningKnockout), layer by layer, on featureTest/25;
  - the laminate (the board body) is what KiCad 10's own STEP export cuts (kicad-cli pcb export step
    --board-only --cut-vias-in-body), band by band, on featureTest/24, 25 and 26.  KiCad's STEP
    cuts every backdrill and post machining 1 um further (a margin "to ensure clean cuts"), which
    KESE does not copy; the bands still agree to 0.1 %;
  - the laminate near a cut is cut in stretches that fill it without overlapping, and a barrel is
    cut back only where a cut takes it, the plated board edge too (featureTest/28).
Takes a few seconds.

    python -m pytest tests/test_machining.py        (or:  python tests/test_machining.py)"""
import math

import numpy as np
import shapely
from shapely.geometry import Point, box

from helpers import FEATURES, run_stages, run_tests, settings
from kese.core.shapes2d import disk
from kese.model.items import PostMachining
from kese.s3_resolve import resolve
from kese.s3_resolve.holes import cut_back
from kese.s3_resolve.machining import post_machining_steps
from kese.s4_geometry import geometry
from kese.s4_geometry.laminate import cut_slab
LAYERS = ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"]
# featureTest/25's stackup, F up: copper 35 / 17.5 / 17.5 / 35 um, dielectrics 0.2, 1.095, 0.2 mm
BAND = {"F.Cu": (0.765, 0.8), "In1.Cu": (0.5475, 0.565), "In2.Cu": (-0.565, -0.5475), "B.Cu": (-0.8, -0.765)}
TOL = 0.025

# KiCad 10.0's pcbnew (PAD::GetPostMachiningKnockout) on featureTest/25: the diameter knocked out of
# each copper layer, by the pad's place (mm from the board's corner)
KICAD_KNOCKOUTS = {
    (24, 28): {"In2.Cu": 0.9, "B.Cu": 0.9},
    (30, 28): {"F.Cu": 1.0, "In1.Cu": 0.512501},
    (6, 6): {"F.Cu": 6.0, "In1.Cu": 6.0},
    (16, 6): {"In2.Cu": 6.0, "B.Cu": 6.0},
    (26, 6): {"F.Cu": 5.0, "In1.Cu": 5.0, "In2.Cu": 5.0, "B.Cu": 5.0},
    (36, 6): {"F.Cu": 5.0, "In1.Cu": 5.0},
    (46, 6): {"F.Cu": 6.3, "In1.Cu": 5.876223, "In2.Cu": 3.94206, "B.Cu": 3.518283},
    (56, 6): {"F.Cu": 6.3, "In1.Cu": 5.812501, "In2.Cu": 3.587501, "B.Cu": 3.100001},
    (6, 16): {"F.Cu": 6.3, "In1.Cu": 5.719021, "In2.Cu": 3.067369, "B.Cu": 2.486389},
    (16, 16): {"F.Cu": 6.3, "In1.Cu": 5.455626, "In2.Cu": 1.601813, "B.Cu": 0.757438},
    (26, 16): {"F.Cu": 6.0, "In1.Cu": 5.512501},
    (36, 16): {"F.Cu": 3.100001, "In1.Cu": 3.587501, "In2.Cu": 5.812501, "B.Cu": 6.3},
    (46, 16): {"F.Cu": 2.0, "In1.Cu": 1.512501},
    (6, 28): {"F.Cu": 2.2, "In1.Cu": 2.2, "In2.Cu": 1.912501, "B.Cu": 2.4},
    (16, 28): {"F.Cu": 1.6, "In1.Cu": 1.6}}

# KiCad 10.0's STEP export of the board body (mm3) between the copper layers' faces, from B.Cu's
# inner face up to F.Cu's: the dielectrics and the inner copper bands in turn
KICAD_BODY = {
    "24_backdrills": [330.316257, 28.899951, 594.626062, 28.905449, 563.116523, 28.972522, 596.062084,
                      28.967024, 331.082963],
    "25_post_machining": [400.390473, 35.041606, 2170.687352, 33.767398, 382.938322],
    "26_via_protection": [287.476854, 25.152994, 1573.981779, 25.136913, 287.307137]}


def pm(side, mode, size, depth=0.0, angle=0.0):
    return PostMachining((0.0, 0.0), side, mode, size, depth, angle)


def steps_of(p, tol=TOL):
    return post_machining_steps(p, BAND, LAYERS, tol)


def check_contiguous(steps, face, floor):
    zs = sorted((z0, z1) for z0, z1, _ in steps)
    assert math.isclose(zs[0][0], min(face, floor), abs_tol=1e-12) and math.isclose(zs[-1][1], max(face, floor), abs_tol=1e-12)
    for (_, a1), (b0, _) in zip(zs, zs[1:]):
        assert math.isclose(a1, b0, abs_tol=1e-12), (a1, b0)


def test_a_counterbore_cuts_to_its_depth_from_the_copper_face():
    steps, knocked = steps_of(pm("F", "counterbore", 6.0, 1.0))
    check_contiguous(steps, 0.8, -0.2)
    assert all(r == 3.0 for *_, r in steps)
    bounds = {z for z0, z1, _ in steps for z in (z0, z1)}
    assert {0.765, 0.565, 0.5475} <= bounds                       # a step at every copper face it passes
    assert knocked == [(0, 3.0), (1, 3.0)]                        # In2's middle is 1.356 down: not reached
    steps, knocked = steps_of(pm("B", "counterbore", 6.0, 0.5))   # from the back, the same upside down
    check_contiguous(steps, -0.8, -0.3)
    assert knocked == [(2, 3.0), (3, 3.0)]


def test_a_floor_inside_an_inner_copper_layer_cuts_the_laminate_to_the_floor_only():
    """KiCad's 3D board stops a counterbore at its depth even inside a copper layer's band; the copper
    is knocked out when the depth passes the layer's middle (0.035 + 0.2 + 0.00875 = 0.24375 down)."""
    steps, knocked = steps_of(pm("F", "counterbore", 5.0, 0.245))
    check_contiguous(steps, 0.8, 0.555)
    assert dict(knocked) == {0: 2.5, 1: 2.5}
    steps, knocked = steps_of(pm("F", "counterbore", 5.0, 0.24))
    check_contiguous(steps, 0.8, 0.56)                            # the laminate is cut all the same
    assert dict(knocked) == {0: 2.5}


def test_a_counterbore_through_the_board_knocks_out_the_far_copper_only_when_deeper_than_the_board():
    """KiCad counts the distance to the far outer layer through all of it, and wants it less than the depth."""
    steps, knocked = steps_of(pm("F", "counterbore", 5.0, 2.0))
    check_contiguous(steps, 0.8, -0.8)
    assert [k for k, _ in knocked] == [0, 1, 2, 3]
    steps, knocked = steps_of(pm("F", "counterbore", 5.0, 1.6))
    check_contiguous(steps, 0.8, -0.8)
    assert [k for k, _ in knocked] == [0, 1, 2]


def kicad_distance(k, front):
    """BOARD_STACKUP::GetLayerDistance from the face's copper to layer k: 0 to the near outer layer,
    to an inner layer's middle, through all of the far outer layer."""
    face = BAND["F.Cu"][1] if front else BAND["B.Cu"][0]
    near, far = (0, 3) if front else (3, 0)
    if k == near:
        return 0.0
    if k == far:
        return 1.6
    return abs(face - sum(BAND[LAYERS[k]]) / 2)


def test_a_countersink_keeps_within_its_tolerance_of_the_cone_and_keeps_its_volume():
    for angle in (82, 90, 100, 120):
        for side in ("F", "B"):
            for depth in (0.0, 0.8):
                for tol in (0.025, 0.005):
                    size = 6.3
                    t = math.tan(math.radians(angle / 2))
                    tip = size / 2 / t
                    reach = min(depth, tip) if depth else tip
                    front = side == "F"
                    face = 0.8 if front else -0.8
                    floor = max(face - reach, -0.8) if front else min(face + reach, 0.8)
                    steps, knocked = steps_of(pm(side, "countersink", size, depth, angle), tol)
                    check_contiguous(steps, face, floor)
                    cone = lambda z: size / 2 - abs(face - z) * t           # noqa: E731
                    for z0, z1, r in steps:
                        assert abs(r - cone(z0)) <= tol + 1e-12 and abs(r - cone(z1)) <= tol + 1e-12, (angle, z0, z1, r)
                    bounds = {round(z, 9) for z0, z1, _ in steps for z in (z0, z1)}
                    faces = {round(z, 9) for b in BAND.values() for z in b if min(face, floor) < z < max(face, floor)}
                    assert faces <= bounds, (angle, side, faces - bounds)
                    lo, hi = sorted((face, floor))
                    zz = np.linspace(lo, hi, 20001)
                    exact = np.trapezoid(math.pi * np.maximum(np.array([cone(z) for z in zz]), 0) ** 2, zz)
                    stacked = sum(math.pi * r * r * (z1 - z0) for z0, z1, r in steps)
                    assert abs(stacked - exact) <= math.pi * tol ** 2 * (hi - lo) / 3 + 1e-6, (angle, stacked, exact)
                    expect = {k: size / 2 - kicad_distance(k, front) * t for k in range(4)}
                    expect = {k: r for k, r in expect.items() if r > 0 and kicad_distance(k, front) < reach - 1e-7}
                    assert dict(knocked) == expect, (angle, side, depth, knocked, expect)


def resolved(name, changes=None):
    """Stage 3's Regions of a feature board, with the settings `changes`, and the Job."""
    with settings(changes or {}):
        return run_stages(FEATURES / f"{name}.kicad_pcb", resolve)


def test_the_copper_knocked_out_is_what_kicad_gives_each_layer():
    r, _ = resolved("25_post_machining")
    found = {}
    for h in r.items.holes:
        if h.kind == "knockout":
            c = h.drill.centroid
            radius = max(c.distance(Point(xy)) for xy in h.drill.exterior.coords)      # its corners are on the circle
            found.setdefault((round(c.x - 100, 6), round(c.y - 100, 6)), {})[r.layers[h.i]] = 2 * radius
    assert set(found) == set(KICAD_KNOCKOUTS), set(found) ^ set(KICAD_KNOCKOUTS)
    for at, layers in KICAD_KNOCKOUTS.items():
        assert set(found[at]) == set(layers), (at, found[at], layers)
        for layer, d in layers.items():
            assert abs(found[at][layer] - d) < 1e-5, (at, layer, found[at][layer], d)    # KiCad rounds to 1 nm


def test_the_board_body_is_what_kicad_cuts_band_by_band():
    for name, kicad in KICAD_BODY.items():
        r, job = resolved(name)
        ps = geometry.geometry(r, job.mode)
        st, layers = r.stackup, r.layers
        cuts = sorted({round(z, 9) for l in layers[1:-1] for z in st.band[l]} |
                      {round(st.band[layers[-1]][1], 9), round(st.band[layers[0]][0], 9)})
        assert len(cuts) - 1 == len(kicad)
        for (a, b), k in zip(zip(cuts, cuts[1:]), kicad):
            mine = sum(p.region.area * (min(p.z1, b) - max(p.z0, a)) for p in ps.prisms
                       if p.role in ("board", "copper") and min(p.z1, b) - max(p.z0, a) > 1e-12)
            assert abs(mine - k) <= 1e-3 * k, (name, a, b, mine, k)


def test_the_laminate_near_a_cut_is_cut_in_stretches_that_fill_it():
    region = box(0, 0, 10, 10)
    cuts = [(0.2, 0.6, disk((3, 3), 1.0)), (0.6, 1.0, disk((3, 3), 0.5)), (0.0, 1.0, disk((7, 7), 1.0)),
            (0.5, 0.8, disk((3.5, 3), 0.8))]
    pieces = cut_slab(region, 0.0, 1.0, cuts)
    for z in np.linspace(0.01, 0.99, 50):
        here = [g for g, z0, z1 in pieces if z0 < z < z1]
        assert abs(sum(g.area for g in here) - shapely.union_all(here).area) < 1e-9          # no overlaps
        cut = shapely.union_all([d for z0, z1, d in cuts if z0 < z < z1])
        assert shapely.union_all(here).symmetric_difference(region.difference(cut)).area < 1e-3, z   # but the grid
    assert cut_slab(region, 0.0, 1.0, []) == [(region, 0.0, 1.0)]


def test_a_barrel_is_cut_back_only_where_a_cut_takes_it():
    ring = disk((0, 0), 0.2).difference(disk((0, 0), 0.175))
    pieces = cut_back(ring, -0.8, 0.8, [(-math.inf, 0.1, disk((0, 0), 0.3))])          # a backdrill from the back
    assert all(z0 >= 0.1 - 1e-12 for g, z0, z1 in pieces if not g.is_empty)
    assert math.isclose(sum(g.area * (z1 - z0) for g, z0, z1 in pieces), ring.area * 0.7, rel_tol=1e-9)
    pieces = cut_back(ring, -0.8, 0.8, [(0.5, math.inf, disk((0, 0), 0.19))])           # narrower than the ring
    assert math.isclose(sum(g.area * (z1 - z0) for g, z0, z1 in pieces),
                        ring.area * 1.3 + ring.difference(disk((0, 0), 0.19)).area * 0.3, rel_tol=1e-3)   # the grid


def test_backdrills_cut_the_barrel_from_the_face_through_their_last_layer():
    r, _ = resolved("24_backdrills")
    holes, layers, st = r.items.holes, r.layers, r.stackup
    seen = 0
    for h in holes:
        if h.kind == "backdrill":
            cuts = r.barrel_cuts[h.of]
            z0 = -math.inf if h.j == len(layers) - 1 else st.band[layers[h.j]][0]
            z1 = math.inf if h.i == 0 else st.band[layers[h.i]][1]
            assert (z0, z1, h.drill) in cuts
            seen += 1
    assert seen >= 12


def test_a_cut_at_a_plated_edge_takes_the_plating_only_between_its_heights():
    r, _ = resolved("28_plated_edge_machining")
    band, cuts = r.edge_band, r.edge_cuts
    assert r.edge_net == "GND" and not any(g is band for g, *_ in r.barrels)
    spans = sorted({(z0, z1) for z0, z1, _ in cuts})
    top, bottom = BAND["F.Cu"][1], BAND["B.Cu"][0]
    assert any(math.isclose(z0, top - 0.5) for z0, _ in spans)             # the counterbore, 0.5 mm deep
    assert (bottom, BAND["B.Cu"][1]) in spans                                # the countersink, from the back
    assert (-math.inf, BAND["In2.Cu"][1]) in spans                           # the backdrill, up to In2.Cu
    assert (BAND["In1.Cu"][0], math.inf) in spans                            # the tertiary drill and blind vias
    pieces = [(g, z0, z1) for g, z0, z1, i, j, net in r.barrel_pieces if net == r.edge_net and (i, j) == (0, 3)]
    for z in np.linspace(BAND["B.Cu"][1] + 1e-4, BAND["F.Cu"][0] - 1e-4, 300):       # the plating's whole height
        here = [g for g, z0, z1 in pieces if z0 < z < z1]
        cut = shapely.union_all([d for z0, z1, d in cuts if z0 < z < z1])
        assert len(here) == 1 and here[0].symmetric_difference(band.difference(cut)).area < 1e-5, z    # the grid
        if -0.09 < z < 0.29:                                  # under the counterbore's floor, over the countersink
            assert here[0].symmetric_difference(band).area < 1e-9
    on_top = r.copper["F.Cu"]["GND"]                         # the band is F.Cu's copper but where a cut takes F.Cu
    face, front = (shapely.union_all([d for z0, z1, d in cuts if z1 >= z]) for z in (top, math.inf))
    assert on_top.intersection(face.difference(front)).intersection(band).area < 1e-6
    assert band.difference(face).difference(on_top).area < 1e-6


def test_drills_and_cuts_kicad_would_not_make_are_left_out_and_named():
    r, _ = resolved("24_backdrills")
    assert dict(r.items.skipped) == {"backdrills of pads with no hole (left out, as KiCad does)": 1,
                                     "backdrills of vias with no size (left out)": 1,
                                     "backdrills of vias on a copper layer the board does not have (left out)": 1}
    assert r.items.found["backdrills of vias"] == 10 and r.items.found["tertiary drills of vias"] == 4
    assert r.items.found["backdrills of pads"] == 2 and r.items.found["tertiary drills of pads"] == 1
    r, _ = resolved("25_post_machining")
    assert dict(r.items.skipped) == {
        "counterbores of pads with no size or no depth (not cut, as KiCad does)": 1,
        "counterbores of pads with no hole (left out, as KiCad does)": 1,
        "countersinks of vias with no size or no angle between 0 and 180 degrees (not cut, as KiCad does)": 1}
    assert r.items.found["counterbores of pads"] == 6 and r.items.found["countersinks of pads"] == 8


def test_switched_off_machining_is_left_out_and_named():
    r, _ = resolved("24_backdrills", {"Board.BACKDRILLS": False})
    assert not any(h.kind == "backdrill" for h in r.items.holes) and not r.barrel_cuts
    assert r.items.skipped["backdrills of vias (Board.BACKDRILLS is False)"] > 0
    r, _ = resolved("25_post_machining", {"Board.POST_MACHINING": False})
    assert not r.items.post_machining and not r.slab_cuts and not r.band_cuts
    assert not any(h.kind == "knockout" for h in r.items.holes)
    assert r.items.skipped["counterbores of pads (Board.POST_MACHINING is False)"] > 0


if __name__ == "__main__":
    run_tests(__file__)
