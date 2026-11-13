"""What 25.2 tells the solver of a material beyond one er and tan d: how a dielectric changes with
frequency (constant, Djordjevic-Sarkar as KiCad fits it, or a table), how rough the copper is
(Hammerstad or Huray), and the copper's own values by position: foil, plating, etch factor and
treated face of the top, the inner and the bottom layers, listed for every layer a part lies on.

    python -m pytest tests/test_material_models.py           (or:  python tests/test_material_models.py)"""
import cmath
import math

from helpers import FEATURES, run_stages, run_tests, settings
from kese.core.dielectric import ds_at, ds_fit, ds_fits, model_props
from kese.s4_geometry import geometry
from kese.s6_assemble.assemble import props_of
from parameters import P

REAL = FEATURES / "29d_stackup_real.kicad_pcb"
LOW, HIGH = 1e3, 1e12                    # KiCad's corner frequencies, and Board.DS_LOW_/DS_HIGH_FREQUENCY_HZ


def test_the_djordjevic_sarkar_model_has_the_given_values_at_the_spec_frequency():
    assert (P.Board.DS_LOW_FREQUENCY_HZ, P.Board.DS_HIGH_FREQUENCY_HZ) == (LOW, HIGH)
    for er, tand, f in ((4.16, 0.02, 1e9), (4.6, 0.018, 1e10), (3.0, 0.001, 5e9), (9.8, 0.0001, 1e6), (4.4, 0.02, LOW), (4.4, 0.02, HIGH)):
        e_inf, delta = ds_fit(er, tand, f, LOW, HIGH)
        got = ds_at(e_inf, delta, f, LOW, HIGH)
        assert math.isclose(got[0], er, rel_tol=1e-12) and math.isclose(got[1], tand, rel_tol=1e-12), (er, tand, f, got)
        assert e_inf < er and delta > 0                        # er falls with frequency, to epsilon_inf
    assert ds_fit(4.4, 0.0, 1e9, LOW, HIGH) == (4.4, 0.0)      # no loss: no dispersion


def test_the_fit_is_the_one_of_the_papers_formula():
    # er(f) = e_inf + d_e / (m2 - m1) * log10((w2 + j w) / (w1 + j w)), with w = 2 pi f and w1, w2 = 10^m1, 10^m2
    # (the form of Djordjevic et al. 2001), worked here with its own numbers, not the code's
    er, tand, f = 4.16, 0.02, 1e9
    e_inf, delta = ds_fit(er, tand, f, LOW, HIGH)
    w, w1, w2 = (2 * math.pi * x for x in (f, LOW, HIGH))
    m1, m2 = math.log10(w1), math.log10(w2)
    paper = e_inf + delta / (m2 - m1) * cmath.log((w2 + 1j * w) / (w1 + 1j * w)) / math.log(10)
    assert math.isclose(paper.real, er, rel_tol=1e-12) and math.isclose(-paper.imag / paper.real, tand, rel_tol=1e-12)
    # the loss is e'' = er tan d = d_e / ln(f2 / f1) * (atan(f / f1) - atan(f / f2))
    assert math.isclose(er * tand, delta / math.log(HIGH / LOW) * (math.atan(f / LOW) - math.atan(f / HIGH)), rel_tol=1e-12)
    assert (round(e_inf, 6), round(delta, 6)) == (3.793885, 1.098344)
    # between the corners the loss tangent is nearly flat and er falls by about the same step each decade
    at = {x: ds_at(e_inf, delta, x, LOW, HIGH) for x in (1e6, 1e7, 1e8, 1e9, 1e10)}
    assert all(0.017 < tan < 0.022 for _, tan in at.values()), at
    steps = [at[a][0] - at[b][0] for a, b in ((1e6, 1e7), (1e7, 1e8), (1e8, 1e9), (1e9, 1e10))]
    assert all(math.isclose(s, delta * math.log(10) / math.log(HIGH / LOW), rel_tol=2e-3) for s in steps), steps


def test_the_model_entry_of_materials_json():
    assert model_props("constant", 4.4, 0.02, 1e9) == {"model": "constant"}
    assert model_props("djordjevic_sarkar", 4.16, 0.02, 1e9) == {
        "model": "djordjevic_sarkar", "spec_frequency_hz": 1e9, "low_frequency_hz": LOW, "high_frequency_hz": HIGH,
        "epsilon_inf": 3.793885, "delta_epsilon": 1.098344}
    assert not ds_fits(100, LOW, HIGH) and not ds_fits(1e13, LOW, HIGH) and ds_fits(LOW, LOW, HIGH) and not ds_fits(1e9, 1e9, 1e3)
    assert model_props("djordjevic_sarkar", 4.16, 0.02, 100) == {"model": "constant"}      # cannot be fitted, as KiCad
    with settings({"Board.DS_LOW_FREQUENCY_HZ": 1e4, "Board.DS_HIGH_FREQUENCY_HZ": 1e11}):
        got = model_props("djordjevic_sarkar", 4.16, 0.02, 1e9)
        assert (got["low_frequency_hz"], got["high_frequency_hz"]) == (1e4, 1e11)
        assert math.isclose(ds_at(got["epsilon_inf"], got["delta_epsilon"], 1e9, 1e4, 1e11)[0], 4.16, rel_tol=1e-6)
    table = [(1e9, 4.2, 0.018), (5e9, 4.1, 0.02), (1e10, 4.05, 0.022)]
    with settings({"Board.DIELECTRIC_TABLE": table}):
        assert model_props("table", 4.4, 0.02, 1e9) == {"model": "table", "table": [list(row) for row in table]}


def laminate_props(changes):
    with settings(changes):
        return {p.part: p.props for p in run_stages(REAL, geometry)[0].prisms if p.role == "board"}


def test_the_model_of_the_parameters_where_the_file_gives_none():
    for build in ("PLIES_FUSED", "PLIES_SEPARATE"):
        table = [(1e9, 4.2, 0.018), (1e10, 4.05, 0.022)]
        got = laminate_props({"Stackup.FUSION_BUILD": build, "Board.DIELECTRIC_MODEL": "table", "Board.DIELECTRIC_TABLE": table})
        assert all(props["dielectric_model"] == {"model": "table", "table": [list(row) for row in table]}
                   for part, props in got.items() if "resin_fill_beside" not in props), got
        resin = [props for props in got.values() if props.get("kind") == "resin"]        # the table is the laminate's, not the resin's
        assert all(props["dielectric_model"] == {"model": "constant"} for props in resin) and len(resin) == 2 * (build == "PLIES_SEPARATE")
        got = laminate_props({"Stackup.FUSION_BUILD": build, "Board.DIELECTRIC_MODEL": "djordjevic_sarkar",
                              "Board.DEFAULT_SPEC_FREQUENCY_HZ": 2e9})
        assert all(props["dielectric_model"]["model"] == "djordjevic_sarkar" and props["spec_frequency_hz"] == 2e9
                   for props in got.values() if "dielectric_model" in props), got
        assert all(props["dielectric_model"] == {"model": "constant"} for props in laminate_props({"Stackup.FUSION_BUILD": build}).values()
                   if "dielectric_model" in props)


def copper(changes, pcb=REAL):
    with settings(changes):
        ps = run_stages(pcb, geometry)[0]
    return ps, [p for p in ps.prisms if p.role == "copper"]


def test_the_copper_roughness_models():
    _, prisms = copper({})
    assert {str(p.props["roughness"]) for p in prisms} == {"{'model': 'none'}"}
    _, prisms = copper({"Copper.COPPER_ROUGHNESS_MODEL": "hammerstad", "Copper.COPPER_ROUGHNESS_RMS_TREATED_UM": 1.2,
                        "Copper.COPPER_ROUGHNESS_RMS_OTHER_UM": 0.4})
    assert all(p.props["roughness"] == {"model": "hammerstad", "rms_treated_um": 1.2, "rms_other_um": 0.4} for p in prisms)
    assert all(p.props["surface_roughness_um"] == 1.2 for p in prisms)                   # the entry of before 25.2
    _, prisms = copper({"Copper.COPPER_ROUGHNESS_MODEL": "huray", "Copper.COPPER_HURAY_RADIUS_TREATED_UM": 0.6,
                        "Copper.COPPER_HURAY_RADIUS_OTHER_UM": 0.3, "Copper.COPPER_HURAY_SURFACE_RATIO_TREATED": 2.5,
                        "Copper.COPPER_HURAY_SURFACE_RATIO_OTHER": 1.5})
    assert all(p.props["roughness"] == {"model": "huray", "radius_treated_um": 0.6, "radius_other_um": 0.3,
                                        "surface_ratio_treated": 2.5, "surface_ratio_other": 1.5} for p in prisms)


def test_the_copper_by_top_inner_and_bottom():
    ps, prisms = copper({"Copper.TOP_PLATING_ADDED_MM": 0.02, "Copper.BOTTOM_PLATING_ADDED_MM": 0.01,
                         "Copper.TOP_ETCH_FACTOR": 0.5, "Copper.INNER_ETCH_FACTOR": 0.0, "Copper.BOTTOM_ETCH_FACTOR": 0.25})
    band = ps.regions.stackup.band
    thick = {layer: round(hi - lo, 6) for layer, (lo, hi) in band.items()}
    assert thick == {"F.Cu": 0.055, "In1.Cu": 0.0152, "In2.Cu": 0.0152, "B.Cu": 0.045}, thick
    assert math.isclose(band["F.Cu"][0], 0.7481) and math.isclose(band["B.Cu"][1], -0.7481)     # the laminate does not move
    own = {p.layer: p.props["layers"][0] for p in prisms}
    assert own == {
        "F.Cu": {"layer": "F.Cu", "position": "top", "thickness_mm": 0.055, "foil_mm": 0.035, "plating_added_mm": 0.02,
                 "etch_factor": 0.5, "treated_face": "lower"},
        "In1.Cu": {"layer": "In1.Cu", "position": "inner", "thickness_mm": 0.0152, "foil_mm": 0.0152, "plating_added_mm": 0.0,
                   "etch_factor": 0.0, "treated_face": "lower"},
        "In2.Cu": {"layer": "In2.Cu", "position": "inner", "thickness_mm": 0.0152, "foil_mm": 0.0152, "plating_added_mm": 0.0,
                   "etch_factor": 0.0, "treated_face": "upper"},
        "B.Cu": {"layer": "B.Cu", "position": "bottom", "thickness_mm": 0.045, "foil_mm": 0.035, "plating_added_mm": 0.01,
                 "etch_factor": 0.25, "treated_face": "upper"}}, own
    # an etched layer is built in slices, narrower away from its foot; a layer with factor 0 is one prism per net
    steps = P.Copper.ETCH_STEPS
    slices = lambda layer, net: sorted((p for p in prisms if (p.layer, p.net) == (layer, net)), key=lambda p: p.z0)
    assert len(slices("F.Cu", "RF")) == len(slices("B.Cu", "CTRL")) == steps and len(slices("In1.Cu", "GND")) == 1
    top = [p.region.area for p in slices("F.Cu", "RF")]
    bottom = [p.region.area for p in slices("B.Cu", "CTRL")]
    assert top == sorted(top, reverse=True) and bottom == sorted(bottom) and top[0] > top[-1] and bottom[0] < bottom[-1]
    # each slice is inset by factor x thickness x its share of the height: the area falls by that along the outline
    outline = slices("F.Cu", "RF")[0].region.length
    assert math.isclose(top[0] - top[-1], outline * 0.5 * 0.055 * (steps - 1) / steps, rel_tol=0.02), (top, outline)
    outline = slices("B.Cu", "CTRL")[-1].region.length
    assert math.isclose(bottom[-1] - bottom[0], outline * 0.25 * 0.045 * (steps - 1) / steps, rel_tol=0.02), (bottom, outline)
    _, inner = copper({"Copper.INNER_ETCH_FACTOR": 0.5})
    assert len([p for p in inner if (p.layer, p.net) == ("In1.Cu", "GND")]) == steps
    assert len([p for p in inner if (p.layer, p.net) == ("F.Cu", "RF")]) == 1


def test_a_copper_part_lists_every_layer_it_lies_on():
    _, prisms = copper({})
    by_net = lambda net: props_of([p for p in prisms if p.net == net])
    assert [own["layer"] for own in by_net("GND")["layers"]] == ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"]     # its vias' rings too
    assert [own["position"] for own in by_net("GND")["layers"]] == ["top", "inner", "inner", "bottom"]
    assert [own["layer"] for own in by_net("CTRL")["layers"]] == ["B.Cu"]
    assert [own["layer"] for own in by_net("RF")["layers"]] == ["F.Cu"]
    _, prisms = copper({"Copper.COPPER_GROUPING": "layer"})
    assert {p.part: [own["layer"] for own in props_of([q for q in prisms if q.part == p.part])["layers"]] for p in prisms} == {
        f"Copper_{layer}": [layer] for layer in ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")}


def test_the_foil_of_a_board_with_no_stack_up_by_position():
    pcb = FEATURES / "15_stackup_none.kicad_pcb"
    ps, _ = copper({"Copper.DEFAULT_TOP_FOIL_MM": 0.07, "Copper.DEFAULT_INNER_FOIL_MM": 0.0175, "Copper.DEFAULT_BOTTOM_FOIL_MM": 0.018}, pcb)
    assert ps.regions.stackup.copper_thickness == {"F.Cu": 0.07, "In1.Cu": 0.0175, "In2.Cu": 0.0175, "B.Cu": 0.018}
    with settings({"Copper.DEFAULT_TOP_FOIL_MM": 0.035}):
        P.override("Copper.DEFAULT_OUTER_FOIL_MM", 0.05)                    # the name of before 25.2 sets both outer layers
        assert (P.Copper.DEFAULT_TOP_FOIL_MM, P.Copper.DEFAULT_BOTTOM_FOIL_MM) == (0.05, 0.05)
        P.override("Copper.DEFAULT_BOTTOM_FOIL_MM", 0.035)


if __name__ == "__main__":
    run_tests(__file__)
