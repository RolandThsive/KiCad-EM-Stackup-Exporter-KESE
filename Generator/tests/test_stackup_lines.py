"""The lines of the two stack-ups of parameters/PCB_elements/Stackup.py: a line set False leaves
its parts out and every other part exactly as it is with all of them True; a line True alone, or
one side alone, builds those parts and no other; the short names set their lines in both stack-ups;
and a stack-up with every line False, a line missing or a line misspelt is refused.  Takes a moment.

    python -m pytest tests/test_stackup_lines.py           (or:  python tests/test_stackup_lines.py)"""
import copy

from helpers import FEATURES, run_stages, run_tests, settings
from kese.job import start
from kese.s4_geometry import geometry
from parameters import GROUPS, LINES, STACKUPS, P

# the boards whose parts, between them, are on every line: both sides' mask and silk on two layers,
# filled vias, and four layers with a plane on each inner one
BOARDS = [FEATURES / f"{name}.kicad_pcb" for name in ("17_mask_silk", "03b_vias_k10", "29d_stackup_real")]
laminate = lambda p: p.role == "board"
resin = lambda p: "resin_fill_beside" in p.props
on = lambda role, layer: lambda p: p.role.startswith(role) and p.layer == layer
# what each line builds, said here on its own (kese/s4_geometry/switches.py is what is tested)
BUILDS = {
    "top_silkscreen": on("silk", "F.SilkS"), "bottom_silkscreen": on("silk", "B.SilkS"),
    "top_solder_mask": on("mask", "F.Mask"), "bottom_solder_mask": on("mask", "B.Mask"),
    "top_finish": on("finish", "F.Finish"), "bottom_finish": on("finish", "B.Finish"),
    "hole_finish": lambda p: p.role == "finish" and p.layer in ("Hole.Finish", "Edge.Finish"),
    "top_copper": on("copper", "F.Cu"), "bottom_copper": on("copper", "B.Cu"),
    "inner_copper": lambda p: p.role == "copper" and p.layer.startswith("In"),
    "plated_holes": lambda p: p.role == "plating", "via_resin": lambda p: p.role == "via_resin",
    "board": laminate,                                               # plies fused: every laminate solid, resin and all
    "resin_between_traces": lambda p: laminate(p) and resin(p),
    "prepreg_plies": lambda p: laminate(p) and not resin(p) and p.props["kind"] == "prepreg",
    "cores": lambda p: laminate(p) and not resin(p) and p.props["kind"] == "core",
}
EVERY = {f"Stackup.{line}": True for line in P.lines()}
NONE = {f"Stackup.{line}": False for line in P.lines()}
_made = {}


def prisms(pcb, mode):
    ps, _ = run_stages(pcb, geometry, mode)
    return ps.prisms


def every(pcb, stackup, mode):
    """The prisms of a board with every line True, made once."""
    key = (pcb, stackup, mode)
    if key not in _made:
        with settings({**EVERY, "Stackup.FUSION_BUILD": stackup}):
            _made[key] = prisms(pcb, mode)
    return _made[key]


def same(got, want):
    key = lambda p: (p.part, p.role, p.layer, p.z0, p.z1, p.region.wkb)
    return sorted(map(key, got)) == sorted(map(key, want))


def board_with(line, stackup, mode):
    """A board that has parts on `line`, and its prisms with every line True."""
    for pcb in BOARDS:
        if any(BUILDS[line](p) for p in every(pcb, stackup, mode)):
            return pcb, every(pcb, stackup, mode)
    raise AssertionError(f"no board of the test has a part on the line {line!r} ({stackup}, {mode} mode)")


def test_a_line_set_false_leaves_out_its_parts_and_no_other():
    for stackup in STACKUPS:
        for mode in ("simulation", "visual"):
            for line in LINES[stackup]:
                pcb, all_of_it = board_with(line, stackup, mode)
                with settings({**EVERY, "Stackup.FUSION_BUILD": stackup, f"Stackup.{line}": False}):
                    got = prisms(pcb, mode)
                assert same(got, [p for p in all_of_it if not BUILDS[line](p)]), f"{line} = False, {stackup}, {mode} mode"


def test_a_line_true_alone_builds_its_parts_and_no_other():
    for stackup in STACKUPS:
        for mode in ("simulation", "visual"):
            for line in LINES[stackup]:
                lines, builds = {line}, BUILDS[line]
                if (stackup, line) == ("PLIES_FUSED", "board"):                  # the resin beside the copper is a line of its own
                    builds = lambda p: laminate(p) and not resin(p)
                if (stackup, line) == ("PLIES_FUSED", "resin_between_traces"):   # and a part of its gap's solid: it needs "board"
                    lines, builds = {line, "board"}, laminate
                pcb, all_of_it = board_with(line, stackup, mode)
                with settings({**NONE, "Stackup.FUSION_BUILD": stackup, **{f"Stackup.{l}": True for l in lines}}):
                    got = prisms(pcb, mode)
                want = [p for p in all_of_it if builds(p)]
                assert want and same(got, want), f"{line} alone, {stackup}, {mode} mode"


def test_one_side_alone():
    pcb = BOARDS[0]
    for stackup in STACKUPS:
        for side, layers in (("top", ("F.SilkS", "F.Mask", "F.Finish", "F.Cu")), ("bottom", ("B.SilkS", "B.Mask", "B.Finish", "B.Cu"))):
            lines = {f"Stackup.{line}": True for line in LINES[stackup] if line.startswith(side)}
            assert len(lines) == 4
            with settings({**NONE, "Stackup.FUSION_BUILD": stackup, **lines}):
                got = prisms(pcb, "simulation")
            want = [p for p in every(pcb, stackup, "simulation") if p.layer in layers]
            assert {p.layer for p in want} == set(layers) and same(got, want), f"{side} alone, {stackup}"


def test_a_short_name_sets_its_lines_in_both_stack_ups():
    for name, lines in GROUPS.items():
        for value in (False, True):
            with settings({**{f"Stackup.{line}": not value for line in P.lines()}, f"Stackup.{name}": value}):
                for stackup in STACKUPS:
                    for line, is_on in getattr(P.Stackup, stackup).items():
                        assert is_on is (value if line in lines else not value), f"Stackup.{name}={value}: {line} of {stackup}"
                assert P.value(f"Stackup.{name}") is value


def refused(change, said):
    """A stack-up changed by `change` (given the dict of the one being built) is refused with `said`."""
    saved = copy.deepcopy(P.building())
    try:
        change(P.building())
        try:
            start("simulation", ["glb"], None, (), False, lambda s: None)
        except ValueError as e:
            assert said in str(e), f"{e}\n  does not say: {said}"
        else:
            raise AssertionError(f"start() accepted a stack-up that should be refused ({said})")
    finally:
        P.building().clear()
        P.building().update(saved)


def test_a_stack_up_that_cannot_be_built_is_refused():
    for stackup in STACKUPS:
        with settings({"Stackup.FUSION_BUILD": stackup}):
            refused(lambda s: s.update(dict.fromkeys(s, False)), f"nothing to build: every line of {stackup} is False")
            refused(lambda s: s.pop("top_copper"), f"{stackup} has no line 'top_copper'; every line must be there")
            refused(lambda s: s.update(top_coper=True), f"{stackup} has the line 'top_coper', which is not one of its "
                                                        "lines (did you mean top_copper?)")
            refused(lambda s: s.update(inner_copper="yes"), "Stackup.inner_copper must be True or False, not 'yes'")
    refused(lambda s: s.update(cores=True), "PLIES_FUSED has the line 'cores', which is not one of its lines")
    with settings({"Stackup.FUSION_BUILD": "PLIES_FUSED"}):
        P.Stackup.FUSION_BUILD = "FUSED"
        try:
            start("simulation", ["glb"], None, (), False, lambda s: None)
        except ValueError as e:
            assert "Stackup.FUSION_BUILD must be 'PLIES_FUSED' or 'PLIES_SEPARATE', not 'FUSED'" in str(e), e
        else:
            raise AssertionError("start() accepted Stackup.FUSION_BUILD = 'FUSED'")


def test_a_line_of_the_other_stack_up_says_it_changes_nothing():
    for built, line, other in (("PLIES_FUSED", "cores", "PLIES_SEPARATE"), ("PLIES_SEPARATE", "board", "PLIES_FUSED")):
        lines = []
        with settings({"Stackup.FUSION_BUILD": built}):
            given = ((f"Stackup.{line}", False), ("Stackup.top_copper", True), ("Stackup.finish", True))
            start("simulation", ["glb"], None, given, False, lines.append).status.stop()
        assert lines == [f'  warning: Stackup.{line} changes nothing in this run: "{line}" is a line of {other}, '
                         f"and {built} is built"], lines


def test_a_board_with_no_part_of_the_lines_built_is_written_empty(tmp_path):
    from kese.pipeline import generate
    only = {f"Stackup.{line}": line == "inner_copper" for line in P.lines()}      # a board of two layers has no inner copper
    for mode, formats in (("simulation", ["glb", "step", "stl", "obj"]), ("visual", ["glb", "obj"])):
        said = []
        with settings(only):
            out, model = generate(FEATURES / "17_mask_silk.kicad_pcb", mode, formats, tmp_path, (), True, said.append)
        assert not model.meshes and "  Verifier: PASS" in said, said
        assert any(s.startswith("  warning: nothing was built: this board has no part of the lines that are True") for s in said), said
        report = (out / "report.txt").read_text(encoding="utf-8")
        assert "lines built: inner_copper\n" in report and "Verifier: PASS" in report
        if mode == "visual":
            assert "no surface to check (nothing was built)" in report


def test_each_stackup_has_its_lines_in_the_files_order():
    assert {name: tuple(getattr(P.Stackup, name)) for name in STACKUPS} == LINES     # the lines, in the file's order


if __name__ == "__main__":
    run_tests(__file__)
