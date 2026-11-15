"""The laminate built ply by ply (Stackup.FUSION_BUILD = "PLIES_SEPARATE"): the solids of a real
four-layer build, the same laminate as with the plies fused (its volume, and every other part
untouched) on boards with blind vias, backdrills, counterbores and countersinks, the joined plies,
one laminate solid on request, and what materials.json says of every solid.  Takes a moment.

    python -m pytest tests/test_plies_built.py           (or:  python tests/test_plies_built.py)"""
import json
import math
import tempfile

from helpers import FEATURES, run_stages, run_tests, settings
from kese.pipeline import generate
from kese.s4_geometry import geometry
from parameters import P

SEPARATE = {"Stackup.FUSION_BUILD": "PLIES_SEPARATE"}
EVERY = {"Stackup.solder_mask": True, "Stackup.silkscreen": True}
REAL = FEATURES / "29d_stackup_real.kicad_pcb"
# boards whose laminate is cut by what ends inside it: blind and buried vias, backdrills, counterbores, countersinks, via plugs
CUT = ["04_vias_blind_buried", "14_stackup_full", "22_hdi_module", "24_backdrills", "25_post_machining", "26_via_protection",
       "28_plated_edge_machining", "29_stackup_plies", "29b_stackup_plies_machined", "29c_stackup_frequency", "29d_stackup_real"]


def prisms(pcb, changes, mode="simulation"):
    with settings({**EVERY, **changes}):
        return run_stages(pcb, geometry, mode)[0].prisms


def volume(prisms):
    return sum(p.region.area * (p.z1 - p.z0) for p in prisms)


def laminate(prisms):
    return [p for p in prisms if p.role == "board"]


def solids(prisms):
    """{part: (z0, z1)} of the laminate's parts."""
    out = {}
    for p in laminate(prisms):
        lo, hi = out.get(p.part, (p.z0, p.z1))
        out[p.part] = (min(lo, p.z0), max(hi, p.z1))
    return out


def test_a_real_four_layer_build_is_seven_laminate_solids():
    built = prisms(REAL, SEPARATE)
    got = {part: round(hi - lo, 6) for part, (lo, hi) in solids(built).items()}
    assert got == {"Board_dielectric 1 ply 1": 0.124, "Board_dielectric 1 ply 2": 0.0764, "Board_resin In1.Cu": 0.0152,
                   "Board_dielectric 2": 1.065, "Board_resin In2.Cu": 0.0152, "Board_dielectric 3 ply 1": 0.0764,
                   "Board_dielectric 3 ply 2": 0.124}, got
    assert math.isclose(sum(got.values()), 1.4962)
    faces = sorted(z for lo_hi in solids(built).values() for z in lo_hi)
    assert math.isclose(faces[0], -0.7481) and math.isclose(faces[-1], 0.7481)
    assert all(math.isclose(a, b) for a, b in zip(faces[1:-1:2], faces[2:-1:2]))       # each solid lies on the next
    props = {p.part: p.props for p in laminate(built)}
    assert props["Board_resin In1.Cu"]["flowed_from"] == "dielectric 1 ply 2"            # the ply that touches the copper
    assert props["Board_resin In2.Cu"]["flowed_from"] == "dielectric 3 ply 1"
    assert (props["Board_resin In1.Cu"]["epsilon_r"], props["Board_resin In1.Cu"]["kind"]) == (P.Board.RESIN_EPSILON_R, "resin")
    with settings({"Board.RESIN_EPSILON_R": None, "Board.RESIN_LOSS_TANGENT": None}):     # None: the ply's own values
        resin = {p.part: p.props for p in laminate(prisms(REAL, SEPARATE))}["Board_resin In2.Cu"]
        assert (resin["epsilon_r"], resin["loss_tangent"]) == (3.91, 0.02)
    fused = solids(prisms(REAL, {}))
    assert sorted(fused) == ["Board_dielectric 1", "Board_dielectric 2", "Board_dielectric 3"]


def test_the_laminate_is_the_same_fused_or_built_apart():
    key = lambda p: (p.part, p.role, p.layer, p.z0, p.z1, p.region.wkb)
    for name in CUT:
        pcb = FEATURES / f"{name}.kicad_pcb"
        for mode in ("simulation", "visual"):
            fused, apart = prisms(pcb, {}, mode), prisms(pcb, SEPARATE, mode)
            a, b = volume(laminate(fused)), volume(laminate(apart))
            assert a > 0 and abs(a - b) <= 1e-9 * a, f"{name}, {mode} mode: laminate {a} mm3 fused, {b} mm3 built apart"
            rest = lambda ps: sorted(key(p) for p in ps if p.role != "board")
            assert rest(fused) == rest(apart), f"{name}, {mode} mode: a part other than the laminate changed"
            # no two laminate solids in the same place: at every height the plies' outlines add up to the gap's
            for z in sorted({(p.z0 + p.z1) / 2 for p in laminate(apart)}):
                area = lambda ps: sum(p.region.area for p in laminate(ps) if p.z0 < z < p.z1)
                assert math.isclose(area(fused), area(apart), rel_tol=1e-9), f"{name}, {mode} mode, z {z}"


def test_plies_joined_and_the_laminate_as_one_solid():
    pcb = FEATURES / "29_stackup_plies.kicad_pcb"
    apart = solids(prisms(pcb, SEPARATE))
    assert sorted(apart) == sorted(
        [f"Board_dielectric 1 ply {n}" for n in (1, 2)] + ["Board_dielectric 2"] + [f"Board_dielectric 3 ply {n}" for n in (1, 2, 3)]
        + ["Board_dielectric 4"] + [f"Board_dielectric 5 ply {n}" for n in (1, 2)] + [f"Board_resin In{n}.Cu" for n in (1, 2, 3, 4)])
    lo, hi = apart["Board_dielectric 4"]
    assert math.isclose(hi - lo, 0.3005)                               # the core with its film of half a micrometre
    joined = prisms(pcb, {**SEPARATE, "Board.JOIN_EQUAL_PLIES": True})
    assert "Board_dielectric 3" in solids(joined) and len(solids(joined)) == len(apart) - 2
    assert math.isclose(volume(laminate(joined)), volume(laminate(prisms(pcb, SEPARATE))), rel_tol=1e-12)
    held = {p.part: p.props.get("joined_plies") for p in laminate(joined)}
    assert held["Board_dielectric 3"] == [f"dielectric 3 ply {n}" for n in (1, 2, 3)]
    assert held["Board_dielectric 4"] == ["dielectric 4 ply 1", "dielectric 4 ply 2"] and held["Board_dielectric 2"] is None
    for changes in (SEPARATE, {}):
        merged = prisms(pcb, {**changes, "Board.DIELECTRIC_GROUPING": "merged"})
        assert set(solids(merged)) == {"Board"}
        assert math.isclose(volume(laminate(merged)), volume(laminate(prisms(pcb, changes))), rel_tol=1e-12)


def materials(pcb, changes, mode="simulation"):
    """The parts of materials.json of one run."""
    with tempfile.TemporaryDirectory() as out, settings({**EVERY, **changes}):
        out_dir, _ = generate(pcb, mode=mode, formats=["glb"], out_root=out, overrides=tuple({**EVERY, **changes}.items()),
                              verify=True, log=lambda s: None)
        return json.loads((out_dir / "materials.json").read_text(encoding="utf-8"))["parts"]


def test_materials_json_says_what_every_laminate_solid_is():
    pcb = FEATURES / "29c_stackup_frequency.kicad_pcb"
    apart = materials(pcb, SEPARATE)
    ply = apart["Board_dielectric 1 ply 1"]["properties"]
    assert {k: ply[k] for k in ("kind", "material", "thickness_mm", "epsilon_r", "loss_tangent", "spec_frequency_hz", "between",
                                "ply", "plies_in_gap")} == {
        "kind": "prepreg", "material": "2116", "thickness_mm": 0.124, "epsilon_r": 4.16, "loss_tangent": 0.02,
        "spec_frequency_hz": 1e9, "between": ["F.Cu", "In1.Cu"], "ply": 1, "plies_in_gap": 2}
    assert ply["dielectric_model"]["model"] == "djordjevic_sarkar" and set(ply["dielectric_model"]) == {
        "model", "spec_frequency_hz", "low_frequency_hz", "high_frequency_hz", "epsilon_inf", "delta_epsilon"}
    assert apart["Board_dielectric 1 ply 2"]["properties"]["dielectric_model"] == {"model": "constant"}
    assert apart["Board_dielectric 2"]["properties"]["spec_frequency_hz"] == 1e10
    resin = apart["Board_resin In2.Cu"]["properties"]
    assert (resin["kind"], resin["resin_fill_beside"], resin["flowed_from"]) == ("resin", "In2.Cu", "dielectric 3 ply 1")
    assert resin["dielectric_model"]["model"] == "djordjevic_sarkar" and resin["spec_frequency_hz"] == 5e9   # as the ply it flowed from
    assert apart["Board_resin In2.Cu"]["look"]["color"] == P.Board.RESIN_COLOR["color"]
    fused = materials(pcb, {})
    gap = fused["Board_dielectric 1"]["properties"]
    assert (gap["thickness_mm"], gap["epsilon_r"], gap["fused_properties"]) == (0.2004, 4.16, "first")
    assert [(p["name"], p["material"], p["thickness_mm"], p["dielectric_model"]["model"]) for p in gap["plies"]] == [
        ("dielectric 1 ply 1", "2116", 0.124, "djordjevic_sarkar"), ("dielectric 1 ply 2", "1080", 0.0764, "constant")]
    series = materials(pcb, {"Board.FUSED_PROPERTIES": "series"})["Board_dielectric 1"]["properties"]
    assert (series["epsilon_r"], series["material"], series["fused_properties"]) == (4.06101, "2116 + 1080", "series")
    # the mask's material on each side, as the board file gives it
    front, back = (fused[part]["properties"] for part in ("Top Solder Mask", "Bottom Solder Mask"))
    assert (front["material"], front["epsilon_r"], front["loss_tangent"]) == ("LPI gloss", 3.5, 0.025)
    assert (back["material"], back["epsilon_r"], back["loss_tangent"]) == ("LPI matt", 3.8, 0.03)
    with settings({"SolderMask.USE_STACKUP_MASK_MATERIAL": False}):
        front = materials(pcb, {})["Top Solder Mask"]["properties"]
        assert (front["material"], front["epsilon_r"]) == (P.SolderMask.MASK_MATERIAL, P.SolderMask.MASK_EPSILON_R)


if __name__ == "__main__":
    run_tests(__file__)
