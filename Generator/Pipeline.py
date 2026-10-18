"""The linear flow:  Reader -> BoardBreakdown -> Geometry -> Colorer -> Assembler -> Packager -> Verifier -> report."""
import time
from pathlib import Path

from Generator import Assembler, BoardBreakdown, Colorer, Reader, Verifier
from Generator.Status import Status, hms
from Generator.Common.prisms import PrismSet
from Generator.Geometry import Board, Copper, Finish, Silkscreen, SolderMask
from Generator.Packager import glb, materials_json, obj, report, step, stl
from Parameters import P

MODES = {"simulation": "simulation", "visual": "visual", "real": "simulation", "pretty": "visual"}   # old names accepted
VISUAL_FORMATS = {"glb", "obj"}
FORMATS = ("glb", "stl", "obj", "step")


def generate(pcb_path, mode=None, formats=None, out_root=None, overrides=(), verify=None, log=print):
    R = P.Run
    mode = MODES.get(mode or R.MODE)
    formats = list(formats or R.FILE_FORMAT)
    verify = R.VERIFY if verify is None else verify
    if mode is None:
        raise ValueError(f"MODE must be 'simulation' or 'visual', not {(mode or R.MODE)!r}")
    bad = [f for f in formats if f not in FORMATS]
    if bad:
        raise ValueError(f"unknown FILE_FORMAT entries {bad}")
    if mode == "visual" and set(formats) - VISUAL_FORMATS:
        raise ValueError("visual mode is a surface, not solids: FILE_FORMAT may only contain glb / obj "
                         f"(asked for {sorted(set(formats) - VISUAL_FORMATS)})")

    log_lines = []
    status = Status(R.SHOW_PROGRESS)

    def say(s):
        status.clear()
        log(s)

    def note(s):
        log_lines.append(s)
        say("  " + s)

    timings = []
    t = time.time()

    status.set("read")
    raw = Reader.read(pcb_path)
    say(f"{raw.name}: KiCad format {raw.version}, {len(raw.copper_layers)} copper layers, mode {mode}")
    for w in raw.warnings:
        note(f"warning: {w}")
    timings.append(("read", time.time() - t)); t = time.time()

    status.set("breakdown (tracks, pads, zones, holes -> regions per layer and net)")
    b = BoardBreakdown.breakdown(raw, note)
    timings.append(("breakdown", time.time() - t)); t = time.time()

    # heights: finished outer copper = foil + plating
    C = P.Copper
    outer = {l: b.stackup.copper_thickness[l] + C.OUTER_PLATING_ADDED_MM for l in ("F.Cu", "B.Cu")}
    b.stackup.heights(outer)

    status.set("geometry (prisms for laminate, copper, mask, silk)")
    ps = PrismSet()
    Board.build(b, ps)
    Copper.build(b, ps)
    SolderMask.build(b, ps, mode)
    Silkscreen.build(b, ps)
    Finish.build(b, ps)
    timings.append(("geometry", time.time() - t)); t = time.time()

    materials = Colorer.color(ps, b.stackup, mode)
    status.set("assemble (" + ("visible skin" if mode == "visual" else "joining the solids of every part") + ")")
    model = Assembler.assemble(raw.name, mode, ps, materials, note)
    timings.append(("assemble", time.time() - t)); t = time.time()

    # Output/<board>/<mode>_<FORMATS>, then <mode>_<FORMATS>__1, __2, ... so no run overwrites another
    base = Path(out_root or R.OUTPUT_DIR) / raw.name / (mode + "_" + "_".join(f.upper() for f in formats))
    out_dir, n = base, 0
    while out_dir.exists():
        n += 1
        out_dir = base.with_name(f"{base.name}__{n}")
    out_dir.mkdir(parents=True)
    written, glb_path = [], None
    if "glb" in formats:
        status.set("writing GLB")
        glb_path = glb.write(model, out_dir / f"{raw.name}.glb"); written.append(glb_path)
    if "obj" in formats:
        status.set("writing OBJ")
        written.append(obj.write(model, out_dir / f"{raw.name}.obj"))
    if "stl" in formats:
        status.set("writing STL")
        written += stl.write(model, out_dir / "stl")
    if "step" in formats:
        status.set("writing STEP (exact solids, fusing per part - the slowest step on dense boards)")
        p = step.write(model, out_dir / f"{raw.name}.step", note)
        if p:
            written.append(p)
    if R.WRITE_MATERIALS_JSON:
        written.append(materials_json.write(model, out_dir / "materials.json"))
    timings.append(("package", time.time() - t)); t = time.time()

    verify_lines = []
    if verify:
        status.set("verify")
        ok, verify_lines = Verifier.verify(model, glb_path)
        timings.append(("verify", time.time() - t))
        say("  " + verify_lines[0])

    report.write_parameters(out_dir / "parameters.txt", overrides)
    report.write_report(out_dir / "report.txt", raw, b, model, formats, timings, verify_lines, log_lines)
    total = status.elapsed()
    status.stop()
    log(f"  -> {out_dir}  ({', '.join(p.name if p.is_file() else p.name + '/' for p in written)})  in {hms(total)}")
    return out_dir, model
