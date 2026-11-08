"""The part switches (Board.BOARD_ENABLED, Copper.COPPER_ENABLED, Finish.FINISH_ENABLED,
SolderMask.SOLDER_MASK_ENABLED, Silkscreen.SILKSCREEN_ENABLED): each one switched off leaves its
parts out and every other part exactly as it is with all of them on.  Takes a moment.

    python -m pytest tests/test_enabled.py           (or:  python tests/test_enabled.py)"""
import sys
from contextlib import ExitStack, contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.job import start  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s3_resolve import resolve  # noqa: E402
from kese.s4_geometry import geometry  # noqa: E402
from kese.s4_geometry.switches import SWITCHES, is_on  # noqa: E402
from parameters import P  # noqa: E402

PCB = ROOT.parent / "featureTest" / "17_mask_silk.kicad_pcb"      # has every role but plating and via resin
# the switches whose parts that board has none of, and a board that has them
BOARD_FOR = {"Copper.VIA_RESIN_ENABLED": ROOT.parent / "featureTest" / "03b_vias_k10.kicad_pcb"}
# {switch: the roles it leaves out}, from the table geometry.py goes by
ROLES = {key: {role for role, k in SWITCHES.items() if k == key} for key in set(SWITCHES.values())}


@contextmanager
def all_on():
    """Every switch on for the block (mask and silk are off by default), put back after it."""
    saved = {key: is_on(key) for key in ROLES}
    for key in ROLES:
        P.override(key, True)
    try:
        yield
    finally:
        for key, value in saved.items():
            P.override(key, value)


@contextmanager
def switched_off(key):
    saved = is_on(key)
    P.override(key, False)
    try:
        yield
    finally:
        P.override(key, saved)


def prisms(mode="simulation", pcb=PCB):
    job = start(mode, ["glb"], "/tmp/kese_test_enabled", (), False, lambda s: None)
    out = str(pcb)
    for stage in (read, collect, resolve, geometry):
        out = stage.run(out, job)
    return {(p.part, p.role, p.z0, p.z1, p.region.wkb) for p in out.prisms}


def test_each_switch_leaves_out_only_its_parts():
    with all_on():
        for mode in ("simulation", "visual"):
            check_mode(mode)


def check_mode(mode):
    made = {}
    for key, roles in sorted(ROLES.items()):
        pcb = BOARD_FOR.get(key, PCB)
        every = made.setdefault(pcb, prisms(mode, pcb))
        assert any(r in roles for _, r, *_ in every), f"{pcb.stem} has no {roles} parts to leave out"
        with switched_off(key):
            got = prisms(mode, pcb)
        assert got == {p for p in every if p[1] not in roles}, f"{key} = False in {mode} mode"


def test_all_off_is_refused():
    with ExitStack() as stack:
        for key in ROLES:
            stack.enter_context(switched_off(key))
        try:
            start("simulation", ["glb"], "/tmp/kese_test_enabled", (), False, lambda s: None)
        except ValueError as e:
            assert "nothing to build" in str(e)
        else:
            raise AssertionError("start() accepted a run with every part switched off")


if __name__ == "__main__":
    test_each_switch_leaves_out_only_its_parts()
    test_all_off_is_refused()
    print("ok")
