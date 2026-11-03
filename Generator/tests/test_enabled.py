"""The part switches (Board.BOARD_ENABLED, Copper.COPPER_ENABLED, Finish.FINISH_ENABLED,
SolderMask.SOLDER_MASK_ENABLED, Silkscreen.SILKSCREEN_ENABLED): each one switched off leaves its
parts out and every other part exactly as it is with all of them on.  Takes a moment.

    python -m pytest tests/test_enabled.py           (or:  python tests/test_enabled.py)"""
import sys
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from kese.job import start  # noqa: E402
from kese.s1_read import read  # noqa: E402
from kese.s2_collect import collect  # noqa: E402
from kese.s3_resolve import resolve  # noqa: E402
from kese.s4_geometry import geometry  # noqa: E402
from parameters import P  # noqa: E402

PCB = ROOT.parent / "featureTest" / "17_mask_silk.kicad_pcb"      # has every role but plating
SWITCHES = {"Board.BOARD_ENABLED": {"board"}, "Copper.COPPER_ENABLED": {"copper", "plating"},
            "Finish.FINISH_ENABLED": {"finish"}, "SolderMask.SOLDER_MASK_ENABLED": {"mask", "mask_over_copper"},
            "Silkscreen.SILKSCREEN_ENABLED": {"silk"}}


@contextmanager
def switched_off(key):
    module, name = key.split(".")
    saved = getattr(getattr(P, module), name)
    P.override(key, False)
    try:
        yield
    finally:
        P.override(key, saved)


def prisms(mode="simulation"):
    job = start(mode, ["glb"], "/tmp/kese_test_enabled", (), False, lambda s: None)
    out = str(PCB)
    for stage in (read, collect, resolve, geometry):
        out = stage.run(out, job)
    return {(p.part, p.role, p.z0, p.z1, p.region.wkb) for p in out.prisms}


def test_each_switch_leaves_out_only_its_parts():
    for mode in ("simulation", "visual"):
        every = prisms(mode)
        for key, roles in SWITCHES.items():
            assert any(r in roles for _, r, *_ in every), f"{PCB.stem} has no {roles} parts to leave out"
            with switched_off(key):
                got = prisms(mode)
            assert got == {p for p in every if p[1] not in roles}, f"{key} = False in {mode} mode"


def test_all_off_is_refused():
    with switched_off("Board.BOARD_ENABLED"), switched_off("Copper.COPPER_ENABLED"), \
            switched_off("Finish.FINISH_ENABLED"), switched_off("SolderMask.SOLDER_MASK_ENABLED"), \
            switched_off("Silkscreen.SILKSCREEN_ENABLED"):
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
