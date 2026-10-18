#!/usr/bin/env python3
"""
Kicad_PCB__to__3D_Model

    python run.py                                  every .kicad_pcb in Input/, settings from Parameters/
    python run.py Input/board.kicad_pcb            one board
    python run.py board.kicad_pcb --mode pretty    override the mode
    python run.py board.kicad_pcb --format glb step stl
    python run.py board.kicad_pcb --verify
    python run.py board.kicad_pcb --set Copper.VIA_WALL_MM=0.02 --set Board.BOARD_THICKNESS_MM=0.8

Every parameter lives in Parameters/*.py; --set overrides one for this run and the override is
recorded in the output's parameters.txt.  Outputs go to Output/<board>/<mode>/.
"""
import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from Parameters import P  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="KiCad .kicad_pcb -> 3D model (real stack-up or pretty skin)")
    ap.add_argument("boards", nargs="*", help=".kicad_pcb files (default: all in Input/)")
    ap.add_argument("--mode", choices=["real", "pretty"])
    ap.add_argument("--format", nargs="+", metavar="FMT", help="glb stl obj step")
    ap.add_argument("--verify", action="store_true", help="run the Verifier (opt-in)")
    ap.add_argument("--out", help="output root (default Run_Parameters.OUTPUT_DIR)")
    ap.add_argument("--set", action="append", default=[], metavar="Module.NAME=value",
                    help="override a parameter, e.g. Copper.ETCH_FACTOR=0.5")
    args = ap.parse_args()

    overrides = []
    for item in args.set:
        key, _, val = item.partition("=")
        try:
            value = ast.literal_eval(val)
        except Exception:
            value = val
        P.override(key.strip(), value)
        overrides.append((key.strip(), value))

    from Generator.Pipeline import generate  # after overrides, so modules see them

    boards = [Path(b) for b in args.boards] or sorted((ROOT / P.Run.INPUT_DIR).glob("*.kicad_pcb"))
    if not boards:
        sys.exit(f"no boards given and none found in {P.Run.INPUT_DIR}/")
    out_root = Path(args.out) if args.out else ROOT / P.Run.OUTPUT_DIR
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
