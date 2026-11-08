"""KiCad 10's via protection (IPC-4761; kese/s2_collect/machining.py, s3_resolve/holes.py and mask.py,
s4_geometry/via_fill.py) on featureTest/26: every via's covering, plugging, capping and filling as the
file and the board's own setting give it; the fill and the plugs, via by via, as long as the rules
say (worked out here by hand from the stackup, not by KESE's functions); a cap or a copper fill
closing the outer copper, a covering closing the mask, a backdrill or counterbore leaving its end
open; and the settings: a resin fill, protection switched off, the resin left out of the files.

    python -m pytest tests/test_via_protection.py   (or:  python tests/test_via_protection.py)"""
import math
import sys
from pathlib import Path

from shapely.geometry import Point, box

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.job import start  # noqa: E402
from kese.model.items import Protection  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s3_resolve import resolve  # noqa: E402
from kese.s4_geometry import geometry  # noqa: E402
from parameters import P  # noqa: E402

BOARD = ROOT.parent / "featureTest" / "26_via_protection.kicad_pcb"
# (filled, capped, plugged, covered, opened) as the file and the board's setting (plugged on the back) give them
EXPECTED = {
    "T1_TENTED": None, "T1B_TENTED": None,                         # tenting is the mask's business
    "T2_TENT_COVER": (0, 0, "", "F", ""), "T3_PLUG": (0, 0, "F", "", ""), "T4_PLUG_COVER": (0, 0, "F", "F", ""),
    "T5_FILL": (1, 0, "", "", ""), "T6_FILL_COVER": (1, 0, "", "F", ""), "T7_FILL_CAP": (1, 1, "", "", ""),
    "T2B_TENT_COVER": (0, 0, "", "FB", ""), "T3B_PLUG": (0, 0, "FB", "", ""), "T4B_PLUG_COVER": (0, 0, "FB", "FB", ""),
    "T5B_FILL_OPEN": (1, 0, "", "", ""), "T6B_FILL_COVER": (1, 0, "", "FB", ""), "T7B_FILL_CAP_COVER": (1, 1, "", "FB", ""),
    "INHERIT": (0, 0, "B", "", ""), "COVER_UNTENTED": (0, 0, "", "FB", ""), "CAP_ONLY": (0, 1, "", "", ""),
    "FILL_BACKDRILL": (1, 0, "", "", "B"), "PLUG_COUNTERBORE": (0, 0, "F", "", "F"),
    "BLIND_FILLED": (1, 0, "", "", ""),
    "BURIED_CAPPED": (1, 0, "", "", ""),                           # a cap needs an outer end
    "BLIND_COVER_INNER": (0, 0, "", "B", "")}                      # its front end is inside the board
# the stackup, F up: F.Cu 0.765..0.8, In1 0.5475..0.565, In2 -0.565..-0.5475, B.Cu -0.8..-0.765
F_OUT, F_IN, IN1_LO, IN1_HI, IN2_LO, IN2_HI, B_IN, B_OUT = 0.8, 0.765, 0.5475, 0.565, -0.565, -0.5475, -0.765, -0.8
HALF = P.Copper.VIA_PLUG_DEPTH_FRACTION
# what fills each via, height by height: (role, [(z0, z1)]), with the copper fill (the default)
FILLS = {
    "T3_PLUG": ("via_resin", [(F_OUT - HALF * 1.6, F_OUT)]), "T4_PLUG_COVER": ("via_resin", [(F_OUT - HALF * 1.6, F_OUT)]),
    "T3B_PLUG": ("via_resin", [(B_OUT, F_OUT)]), "T4B_PLUG_COVER": ("via_resin", [(B_OUT, F_OUT)]),   # plugs that meet
    "INHERIT": ("via_resin", [(B_OUT, B_OUT + HALF * 1.6)]),
    "PLUG_COUNTERBORE": ("via_resin", []),                         # its plug's end is counterbored away
    "T5_FILL": ("plating", [(B_IN, F_IN)]), "T6_FILL_COVER": ("plating", [(B_IN, F_IN)]),
    "T7_FILL_CAP": ("plating", [(B_IN, F_IN)]), "T5B_FILL_OPEN": ("plating", [(B_IN, F_IN)]),
    "T6B_FILL_COVER": ("plating", [(B_IN, F_IN)]), "T7B_FILL_CAP_COVER": ("plating", [(B_IN, F_IN)]),
    "FILL_BACKDRILL": ("plating", [(IN2_HI, F_IN)]),               # the backdrill empties it up through In2
    "BLIND_FILLED": ("plating", [(IN1_LO, F_IN)]), "BURIED_CAPPED": ("plating", [(IN2_LO, IN1_HI)]),
    "CAP_ONLY": ("plating", []), "T2_TENT_COVER": ("via_resin", []), "BLIND_COVER_INNER": ("via_resin", [])}


# where the solder mask spans the bore: an end the mask is over (tented, the board's default here,
# or covered) and that something shuts (a fill, a cap, a plug or the covering); an end a backdrill
# or counterbore opens never; a face the via does not reach has the mask whole anyway
MASKED = {"T1_TENTED": "", "T2_TENT_COVER": "F", "T3_PLUG": "F", "T4_PLUG_COVER": "F", "T5_FILL": "FB",
          "T6_FILL_COVER": "FB", "T7_FILL_CAP": "FB", "T1B_TENTED": "", "T2B_TENT_COVER": "FB", "T3B_PLUG": "FB",
          "T4B_PLUG_COVER": "FB", "T5B_FILL_OPEN": "", "T6B_FILL_COVER": "FB", "T7B_FILL_CAP_COVER": "FB",
          "INHERIT": "B", "COVER_UNTENTED": "FB", "CAP_ONLY": "FB", "FILL_BACKDRILL": "F", "PLUG_COUNTERBORE": "",
          "BLIND_FILLED": "FB", "BURIED_CAPPED": "FB", "BLIND_COVER_INNER": "FB"}


def run(**settings):
    saved = {k: getattr(getattr(P, k.split(".")[0]), k.split(".")[1]) for k in settings}
    try:
        for k, v in settings.items():
            P.override(k, v)
        job = start("simulation", ["glb"], None, (), False, lambda s: None)
        r = resolve.run(collect.run(read.run(str(BOARD), job), job), job)
        return r, geometry.geometry(r, job.mode)
    finally:
        for k, v in saved.items():
            P.override(k, v)


def vias(r):
    return {h.net: h for h in r.items.holes if h.kind == "drill" and h.plated}


def filled_volume(ps, r, h, role):
    """The volume of `role` inside the bore of via h, and the heights it spans."""
    bore = r.to_board_T(h.drill.buffer(-h.wall))
    v, zs = 0.0, []
    for p in ps.prisms:
        if p.role == role:
            a = p.region.intersection(bore).area
            if a > 1e-9:
                v += a * (p.z1 - p.z0)
                zs.append((p.z0, p.z1))
    return v, bore.area, zs


def test_the_protection_of_every_via_is_as_the_file_and_the_board_say():
    r, _ = run()
    found = vias(r)
    assert set(found) == set(EXPECTED)
    word = lambda d: "".join(s for s in "FB" if d[s])          # noqa: E731
    for net, want in EXPECTED.items():
        p = found[net].protect
        got = None if p is None else (int(p.filled), int(p.capped), word(p.plugged), word(p.covered), word(p.opened))
        assert got == want, (net, got, want)
    assert r.items.skipped["capped vias with both ends inside the board (no effect)"] == 1
    assert r.items.skipped["covered vias at an end inside the board (no effect)"] == 1


def test_fills_and_plugs_are_as_long_as_the_rules_say():
    r, ps = run()
    found = vias(r)
    for net, (role, spans) in FILLS.items():
        v, area, _ = filled_volume(ps, r, found[net], role)
        want = area * sum(z1 - z0 for z0, z1 in spans)
        assert math.isclose(v, want, rel_tol=2e-3, abs_tol=1e-7), (net, v, want)


def test_a_cap_or_a_copper_fill_closes_the_outer_copper_and_a_covering_the_mask():
    r, _ = run(**{"SolderMask.SOLDER_MASK_ENABLED": True})
    found = vias(r)
    centre = {n: r.to_board_T(Point(h.drill.centroid).buffer(0.01)) for n, h in found.items()}
    for net in ("T5_FILL", "T7_FILL_CAP", "CAP_ONLY", "T5B_FILL_OPEN"):
        assert r.copper_all["F.Cu"].contains(centre[net]) and r.copper_all["B.Cu"].contains(centre[net]), net
    assert r.copper_all["F.Cu"].contains(centre["FILL_BACKDRILL"]) and not r.copper_all["B.Cu"].contains(centre["FILL_BACKDRILL"])
    for net in ("T1_TENTED", "T2_TENT_COVER", "T3_PLUG", "INHERIT", "PLUG_COUNTERBORE"):
        assert not r.copper_all["F.Cu"].contains(centre[net]), net
    for net, sides in MASKED.items():
        for s in "FB":
            assert r.mask[s].contains(centre[net]) == (s in sides), (net, s)


def test_a_resin_fill_is_resin_flush_with_the_copper_face_unless_capped():
    r, ps = run(**{"Copper.VIA_FILL": "resin"})
    found = vias(r)
    for net, spans in (("T5_FILL", [(B_OUT, F_OUT)]), ("T7_FILL_CAP", [(B_IN, F_IN)]),
                       ("FILL_BACKDRILL", [(IN2_HI, F_OUT)]), ("BLIND_FILLED", [(IN1_LO, F_OUT)])):
        v, area, _ = filled_volume(ps, r, found[net], "via_resin")
        assert math.isclose(v, area * sum(z1 - z0 for z0, z1 in spans), rel_tol=2e-3), (net, v)
        assert filled_volume(ps, r, found[net], "plating")[0] < 1e-9, net
    centre = r.to_board_T(Point(found["T5_FILL"].drill.centroid).buffer(0.01))
    assert not r.copper_all["F.Cu"].contains(centre)                  # resin does not close the copper
    assert r.copper_all["F.Cu"].contains(r.to_board_T(Point(found["T7_FILL_CAP"].drill.centroid).buffer(0.01)))


def test_protection_switched_off_leaves_every_via_open():
    r, ps = run(**{"Copper.VIA_PROTECTION": "off"})
    assert all(h.protect is None for h in r.items.holes)
    assert not any(p.role == "via_resin" for p in ps.prisms)
    found = vias(r)
    for net in ("T5_FILL", "T7_FILL_CAP", "CAP_ONLY"):
        assert not r.copper_all["F.Cu"].contains(r.to_board_T(Point(found[net].drill.centroid).buffer(0.01))), net
    assert filled_volume(ps, r, found["T7_FILL_CAP"], "plating")[0] < 1e-9


def test_the_resin_switch_leaves_the_resin_out_of_the_files_only():
    _, ps = run(**{"Copper.VIA_RESIN_ENABLED": False})
    assert not any(p.role == "via_resin" for p in ps.prisms)
    assert any("Copper.VIA_RESIN_ENABLED" in n for n in ps.notes)


def test_what_shuts_an_end():
    p = Protection(filled=True)
    assert p.copper_shut("F", "copper") and not p.copper_shut("F", "resin") and p.shut("F")
    p = Protection(capped=True, opened={"F": True, "B": False})
    assert not p.copper_shut("F", "resin") and p.copper_shut("B", "resin") and not p.shut("F")
    p = Protection(plugged={"F": True, "B": False}, covered={"F": False, "B": True})
    assert p.shut("F") and p.shut("B") and not p.copper_shut("F", "copper")
    assert not Protection().shut("F")


def test_the_board_outline_holds_every_fill():
    r, ps = run()
    outline = r.outline
    for p in ps.prisms:
        if p.role in ("via_resin",):
            assert p.region.difference(outline.buffer(1e-6)).area < 1e-9
    assert box(*outline.bounds).area > 0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
