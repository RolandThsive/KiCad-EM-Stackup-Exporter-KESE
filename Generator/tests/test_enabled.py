"""The part switches (Board.BOARD_ENABLED, Copper.COPPER_ENABLED, Finish.FINISH_ENABLED,
SolderMask.SOLDER_MASK_ENABLED, Silkscreen.SILKSCREEN_ENABLED): each one switched off leaves its
parts out and every other part exactly as it is with all of them on.  Takes a moment.

    python -m pytest tests/test_enabled.py           (or:  python tests/test_enabled.py)"""
from helpers import FEATURES, run_stages, run_tests, settings
from kese.job import start
from kese.s4_geometry import geometry
from kese.s4_geometry.switches import SWITCHES

PCB = FEATURES / "17_mask_silk.kicad_pcb"      # has every role but plating and via resin
# the switches whose parts that board has none of, and a board that has them
BOARD_FOR = {"Copper.VIA_RESIN_ENABLED": FEATURES / "03b_vias_k10.kicad_pcb"}
# {switch: the roles it leaves out}, from the table geometry.py goes by
ROLES = {key: {role for role, k in SWITCHES.items() if k == key} for key in set(SWITCHES.values())}


def prisms(mode="simulation", pcb=PCB):
    ps, _ = run_stages(pcb, geometry, mode)
    return {(p.part, p.role, p.z0, p.z1, p.region.wkb) for p in ps.prisms}


def test_each_switch_leaves_out_only_its_parts():
    with settings(dict.fromkeys(ROLES, True)):          # every switch on (mask and silk are off by default)
        for mode in ("simulation", "visual"):
            check_mode(mode)


def check_mode(mode):
    made = {}
    for key, roles in sorted(ROLES.items()):
        pcb = BOARD_FOR.get(key, PCB)
        every = made.setdefault(pcb, prisms(mode, pcb))
        assert any(r in roles for _, r, *_ in every), f"{pcb.stem} has no {roles} parts to leave out"
        with settings({key: False}):
            got = prisms(mode, pcb)
        assert got == {p for p in every if p[1] not in roles}, f"{key} = False in {mode} mode"


def test_all_off_is_refused():
    with settings(dict.fromkeys(ROLES, False)):
        try:
            start("simulation", ["glb"], None, (), False, lambda s: None)
        except ValueError as e:
            assert "nothing to build" in str(e)
        else:
            raise AssertionError("start() accepted a run with every part switched off")


if __name__ == "__main__":
    run_tests(__file__)
