"""The kese command (KiCad EM Stackup Exporter).

    kese                                         every .kicad_pcb in Input/, settings from parameters/
    kese Input/board.kicad_pcb                   one board
    kese board.kicad_pcb --mode visual           simulation (solids) or visual (surface for viewers)
    kese board.kicad_pcb --format glb step stl
    kese board.kicad_pcb --for freecad           a preset: units, origin, grouping, formats (parameters/presets.py)
    kese board.kicad_pcb --verify
    kese board.kicad_pcb --set Copper.VIA_WALL_MM=0.02 --set Board.BOARD_THICKNESS_MM=0.8
    kese --version

Without `pip install .` run it as  python run_KESE.py ...  from the Generator/ folder.
Every parameter lives in parameters/*.py; --for and --set override values for this run and the
overrides are recorded in the output's parameters.txt.  Outputs go to Output/<board>/<mode>_<FORMATS>/,
numbered __1, __2, ... when the folder already exists.
"""
import argparse
import ast
import importlib.util
import sys
from pathlib import Path

from kese import __version__
from parameters import P

REQUIRED = ["numpy", "shapely", "mapbox_earcut"]


def missing_packages():
    """Names of packages that are not installed, so the run can say so instead of a traceback."""
    return [pkg for pkg in REQUIRED if importlib.util.find_spec(pkg) is None]


def old_packages():
    """Packages installed but too old: shapely before 2.1 has no constrained Delaunay triangulation."""
    import shapely
    return [] if hasattr(shapely, "constrained_delaunay_triangles") else [f"shapely {shapely.__version__} (2.1 or newer)"]


def overrides_of(ap, args):
    """The preset's settings, then each --set, then the command-line choices, each applied to the
    parameters: [(key, value)] in that order, for parameters.txt.  A wrong name stops the run here."""
    overrides = []

    def apply(key, value, said):
        try:
            P.override(key, value)
        except ValueError as e:                           # a misspelt name, here or in a preset: said before any work
            ap.error(f"{said}: {e}")
        overrides.append((key, value))

    if args.preset:
        overrides.append(("PRESET", args.preset))
        preset = P.Presets.PRESETS[args.preset]
        if not isinstance(preset, dict):
            ap.error(f"--for {args.preset}: parameters/presets.py gives it {preset!r}, not {{\"Module.NAME\": value}}")
        for key, value in preset.items():
            apply(key, value, f"--for {args.preset}")
    for item in args.set:
        key, is_, val = item.partition("=")
        if not is_:
            ap.error(f"--set {item}: give it a value, as in {item}=value")
        try:
            value = ast.literal_eval(val)
        except Exception:
            value = val
        apply(key.strip(), value, f"--set {item}")
    for key, value in (("Run.MODE", args.mode), ("Run.FILE_FORMAT", args.format), ("Verifier.VERIFY", True if args.verify else None)):
        if value is not None:                             # command-line choices are overrides too
            P.override(key, value)
            overrides.append((key, value))
    return overrides


def check_packages():
    """Stop with what to install when a package is missing or too old."""
    missing = missing_packages()
    if missing:
        sys.exit(f"missing Python package(s): {', '.join(missing)}\n"
                 f"install them with:  python -m pip install {' '.join(missing)}\n"
                 "(or the tested versions:  python -m pip install -r requirements.txt)")
    old = old_packages()
    if old:
        sys.exit(f"Python package(s) too old: {', '.join(old)}\n"
                 "upgrade with:  python -m pip install --upgrade shapely\n"
                 "(or the tested versions:  python -m pip install -r requirements.txt)")


def main():
    ap = argparse.ArgumentParser(prog="kese", description="KiCad EM Stackup Exporter: .kicad_pcb -> solids for EM simulation, or a visual surface")
    ap.add_argument("boards", nargs="*", help=".kicad_pcb files (default: all in Input/)")
    ap.add_argument("--mode", choices=["simulation", "visual"])
    ap.add_argument("--format", nargs="+", metavar="FMT", help="glb stl obj step")
    ap.add_argument("--for", dest="preset", choices=sorted(P.Presets.PRESETS), help="apply a preset from parameters/presets.py")
    ap.add_argument("--verify", action="store_true", help="run the Verifier (opt-in)")
    ap.add_argument("--out", help="output root (default Run.OUTPUT_DIR)")
    ap.add_argument("--set", action="append", default=[], metavar="Module.NAME=value",
                    help="override a parameter, e.g. Copper.ETCH_FACTOR=0.5")
    ap.add_argument("--version", action="version", version=f"kese {__version__}")
    args = ap.parse_args()

    overrides = overrides_of(ap, args)
    check_packages()

    from kese.pipeline import generate  # after the overrides, so the modules see them

    boards = [Path(b) for b in args.boards] or sorted(Path(P.Run.INPUT_DIR).glob("*.kicad_pcb"))
    if not boards:
        sys.exit(f"no boards given and none found in {P.Run.INPUT_DIR}/")
    out_root = Path(args.out) if args.out else Path(P.Run.OUTPUT_DIR)
    failures = 0
    for pcb in boards:
        try:
            generate(pcb, out_root=out_root, overrides=overrides)
        except Exception as exc:
            if len(boards) == 1:
                raise                                     # the traceback, which ends with the reason
            failures += 1
            print(f"{pcb.name}: FAILED - {exc}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
