"""What most feature boards share: a rectangular outline from (100, 100), a plain FR4 stack-up, and
KiCad 7's zone filler."""
import ctypes
import functools
import re
import tempfile
from pathlib import Path

from kicad7 import Board, core, outline, prepreg, stackup

X0, Y0 = 100.0, 100.0
OUTER, INNER = 0.035, 0.0175

# dielectrics between the copper layers, for a 1.6 mm board
PLAIN = {2: [core(1.51)],
         4: [prepreg(0.2), core(1.095), prepreg(0.2)],
         6: [prepreg(0.2), core(0.36), prepreg(0.34), core(0.36), prepreg(0.2)],
         8: [prepreg(0.07), prepreg(0.257), core(0.257), prepreg(0.257), core(0.257), prepreg(0.257),
             prepreg(0.07)]}


def new_board(name, copper=2, size=(30, 20), stack=True):
    """A board with a rectangular outline of size (none when size is None) and, unless stack is
    False, the plain stack-up."""
    b = Board(name, copper)
    if size:
        b.add(outline(b, X0, Y0, X0 + size[0], Y0 + size[1]))
    if stack:
        stackup(b, PLAIN[copper], [OUTER] + [INNER] * (copper - 2) + [OUTER])
    return b


def at(x, y):
    """A point given from the board's top-left corner."""
    return (X0 + x, Y0 + y)


@functools.lru_cache(maxsize=None)
def kicad7():
    """KiCad 7's Python module (pcbnew), or None when it is not installed.  wxWidgets' image
    handlers are registered first, as KiCad does when it starts: without them it saves pictures
    with no data."""
    try:
        import pcbnew
    except ImportError:
        return None
    if not pcbnew.GetBuildVersion().startswith("7."):
        return None
    maps = Path("/proc/self/maps")
    for lib in sorted(set(re.findall(r"\S*libwx_gtk3u_core\S*\.so\S*", maps.read_text() if maps.exists() else ""))):
        ctypes.CDLL(lib)._Z22wxInitAllImageHandlersv()
    return pcbnew


def kicad7_filled(pcbnew, text, unfilled=()):
    """KiCad 7's board for a file in its format, with every zone filled but the ones named in unfilled."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "board.kicad_pcb"
        path.write_text(text, encoding="utf-8")
        board = pcbnew.LoadBoard(str(path))
    board.BuildConnectivity()
    zones = pcbnew.ZONES()
    for z in board.Zones():
        if not z.GetIsRuleArea() and z.GetZoneName() not in unfilled:
            zones.push_back(z)
    pcbnew.ZONE_FILLER(board).Fill(zones)
    return board
