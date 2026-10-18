#!/usr/bin/env python3
"""
KiCad EM Stackup Exporter (KESE)

    kese                                         every .kicad_pcb in Input/, settings from Parameters/
    kese Input/board.kicad_pcb                   one board
    kese board.kicad_pcb --mode visual           simulation (solids) or visual (surface for viewers)
    kese board.kicad_pcb --format glb step stl
    kese board.kicad_pcb --for hfss              a preset: units, origin, grouping, formats (Run_Parameters.PRESETS)
    kese board.kicad_pcb --verify
    kese board.kicad_pcb --set Copper.VIA_WALL_MM=0.02 --set Board.BOARD_THICKNESS_MM=0.8
    kese --version

Without `pip install .` run it as  python run_KESE.py ...  from the project folder.
Every parameter lives in Parameters/*.py; --for and --set override values for this run and the
overrides are recorded in the output's parameters.txt.  Outputs go to Output/<board>/<mode>_<FORMATS>/,
numbered __1, __2, ... when the folder already exists.
"""
import argparse
import ast
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from Generator import __version__  # noqa: E402
from Parameters import P  # noqa: E402

REQUIRED = ["numpy", "scipy", "networkx", "shapely", "trimesh", "manifold3d", "mapbox_earcut", "rtree"]
OPTIONAL = {"step": "cadquery"}


def missing_packages(formats):
    """Names of packages that are not installed, so the run can say so instead of a traceback."""
    needed = REQUIRED + [pkg for fmt, pkg in OPTIONAL.items() if fmt in formats]
    return [pkg for pkg in needed if importlib.util.find_spec(pkg) is None]


def main():
    ap = argparse.ArgumentParser(prog="kese", description="KiCad EM Stackup Exporter: .kicad_pcb -> solids for EM simulation, or a visual surface")
    ap.add_argument("boards", nargs="*", help=".kicad_pcb files (default: all in Input/)")
    ap.add_argument("--mode", choices=["simulation", "visual", "real", "pretty"], help="real / pretty are the old names")
    ap.add_argument("--format", nargs="+", metavar="FMT", help="glb stl obj step")
    ap.add_argument("--for", dest="preset", choices=sorted(P.Run.PRESETS), help="apply a preset from Run_Parameters.PRESETS")
    ap.add_argument("--verify", action="store_true", help="run the Verifier (opt-in)")
    ap.add_argument("--out", help="output root (default Run_Parameters.OUTPUT_DIR)")
    ap.add_argument("--set", action="append", default=[], metavar="Module.NAME=value",
                    help="override a parameter, e.g. Copper.ETCH_FACTOR=0.5")
    ap.add_argument("--version", action="version", version=f"kese {__version__}")
    args = ap.parse_args()

    overrides = []
    if args.preset:
        overrides.append(("PRESET", args.preset))
        for key, value in P.Run.PRESETS[args.preset].items():
            P.override(key, value)
            overrides.append((key, value))
    for item in args.set:
        key, _, val = item.partition("=")
        try:
            value = ast.literal_eval(val)
        except Exception:
            value = val
        P.override(key.strip(), value)
        overrides.append((key.strip(), value))

    formats = args.format or P.Run.FILE_FORMAT
    missing = missing_packages(formats)
    if missing:
        sys.exit(f"missing Python package(s): {', '.join(missing)}\n"
                 f"install them with:  python -m pip install {' '.join(missing)}\n"
                 "(or everything at once:  python -m pip install -r requirements.txt)")

    from Generator.Pipeline import generate  # after the overrides, so the modules see them

    boards = [Path(b) for b in args.boards] or sorted(Path(P.Run.INPUT_DIR).glob("*.kicad_pcb"))
    if not boards:
        sys.exit(f"no boards given and none found in {P.Run.INPUT_DIR}/")
    out_root = Path(args.out) if args.out else Path(P.Run.OUTPUT_DIR)
    failures = 0
    for pcb in boards:
        try:
            generate(pcb, mode=args.mode, formats=args.format, out_root=out_root, overrides=overrides,
                     verify=True if args.verify else None)
        except Exception as exc:
            failures += 1
            print(f"{pcb.name}: FAILED - {exc}")
            if len(boards) == 1:
                raise
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
