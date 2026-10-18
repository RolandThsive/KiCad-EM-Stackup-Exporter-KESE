"""The linear flow:  Reader -> BoardBreakdown -> Geometry -> Colorer -> Assembler -> Verifier -> Packager."""
import time
from pathlib import Path

from Generator import Assembler, BoardBreakdown, Colorer, Reader, Verifier
from Generator.Common.prisms import PrismSet
from Generator.Geometry import Board, Copper, Finish, Silkscreen, SolderMask
from Generator.Packager import glb, materials_json, obj, report, step, stl
from Parameters import P

PRETTY_FORMATS = {"glb", "obj"}


def generate(pcb_path, mode=None, formats=None, out_root=None, overrides=(), verify=None, log=print):
    R = P.Run
    mode = mode or R.MODE
    formats = list(formats or R.FILE_FORMAT)
    verify = R.VERIFY if verify is None else verify
    if mode not in ("real", "pretty"):
        raise ValueError(f"MODE must be 'real' or 'pretty', not {mode!r}")
    bad = [f for f in formats if f not in ("glb", "stl", "obj", "step")]
    if bad:
        raise ValueError(f"unknown FILE_FORMAT entries {bad}")
    if mode == "pretty" and set(formats) - PRETTY_FORMATS:
        raise ValueError("pretty mode is a surface, not solids: FILE_FORMAT may only contain glb / obj "
                         f"(asked for {sorted(set(formats) - PRETTY_FORMATS)})")

    log_lines = []

    def note(s):
        log_lines.append(s)
        log("  " + s)

    timings = []
    t = time.time()

    raw = Reader.read(pcb_path)
    log(f"{raw.name}: KiCad format {raw.version}, {len(raw.copper_layers)} copper layers, mode {mode}")
    for w in raw.warnings:
        note(f"warning: {w}")
    timings.append(("read", time.time() - t)); t = time.time()

    b = BoardBreakdown.breakdown(raw, note)
    timings.append(("breakdown", time.time() - t)); t = time.time()

    # heights: finished outer copper = foil + plating
    C = P.Copper
    outer = {l: b.stackup.copper_thickness[l] + C.OUTER_PLATING_ADDED_MM for l in ("F.Cu", "B.Cu")}
    b.stackup.heights(outer)

    ps = PrismSet()
    Board.build(b, ps)
    Copper.build(b, ps)
    SolderMask.build(b, ps, mode)
    Silkscreen.build(b, ps)
    Finish.build(b, ps)
    timings.append(("geometry", time.time() - t)); t = time.time()

    materials = Colorer.color(ps, b.stackup, mode)
    model = Assembler.assemble(raw.name, mode, ps, materials, note)
    timings.append(("assemble", time.time() - t)); t = time.time()

    out_dir = Path(out_root or R.OUTPUT_DIR) / raw.name / mode
    out_dir.mkdir(parents=True, exist_ok=True)
    written, glb_path = [], None
    if "glb" in formats:
        glb_path = glb.write(model, out_dir / f"{raw.name}.glb"); written.append(glb_path)
    if "obj" in formats:
        written.append(obj.write(model, out_dir / f"{raw.name}.obj"))
    if "stl" in formats:
        written += stl.write(model, out_dir / "stl")
    if "step" in formats:
        p = step.write(model, out_dir / f"{raw.name}.step", note)
        if p:
            written.append(p)
    if R.WRITE_MATERIALS_JSON:
        written.append(materials_json.write(model, out_dir / "materials.json"))
    timings.append(("package", time.time() - t)); t = time.time()

    verify_lines = []
    if verify:
        ok, verify_lines = Verifier.verify(model, glb_path)
        timings.append(("verify", time.time() - t))
        log("  " + verify_lines[0])

    report.write_parameters(out_dir / "parameters.txt", overrides)
    report.write_report(out_dir / "report.txt", raw, b, model, formats, timings, verify_lines, log_lines)
    log(f"  -> {out_dir}  ({', '.join(p.name if p.is_file() else p.name + '/' for p in written)})")
    return out_dir, model
