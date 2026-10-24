"""Stage 1 - read: the .kicad_pcb file -> RawBoard: the parsed tree and the copper layers,
after checking it is a board KESE can handle."""
import re
from pathlib import Path

from kese.core.sexp import child, num, parse
from kese.model.raw_board import RawBoard
from parameters import P


def run(pcb_path, job):
    with job.stage("read", "read"):
        raw = read(pcb_path)
        job.say(f"{raw.name}: KiCad format {raw.version}, {len(raw.copper_layers)} copper layers, mode {job.mode}")
        for w in raw.warnings:
            job.note(f"warning: {w}")
    return raw


def read(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    tree = parse(text)
    if not tree or tree[0] != "kicad_pcb":
        raise ValueError(f"{path.name} is not a KiCad board file (expected (kicad_pcb ...))")
    warnings = []
    version = int(child(tree, "version")[1]) if child(tree, "version") else 0
    gen = child(tree, "generator")
    generator = f"{gen[1]}" if gen else "unknown"
    gv = child(tree, "generator_version")
    if gv:
        generator += f" {gv[1]}"
    R = P.Run
    if version == 0:
        warnings.append("file has no (version ...): treated as legacy KiCad 5")
    elif version < R.KICAD_VERSION_MIN or version > R.KICAD_VERSION_MAX:
        warnings.append(f"file format {version} is outside the tested range "
                        f"{R.KICAD_VERSION_MIN}-{R.KICAD_VERSION_MAX}; proceeding best-effort")

    layers_node = child(tree, "layers")
    if not layers_node:
        raise ValueError(f"{path.name}: no (layers ...) block")
    all_layers = [str(l[1]) for l in layers_node[1:] if isinstance(l, list) and len(l) > 1]
    names = [l for l in all_layers if l.endswith(".Cu")]
    inner = sorted((n for n in names if n.startswith("In")), key=lambda n: int(re.sub(r"\D", "", n)))
    copper = ["F.Cu"] + inner + ["B.Cu"]
    missing = [l for l in ("F.Cu", "B.Cu") if l not in names]
    if missing:
        raise ValueError(f"{path.name}: copper layers {missing} are not declared")
    if len(copper) > 6:
        warnings.append(f"{len(copper)} copper layers: more than the 6 this project has been tested with")

    general = child(tree, "general")
    file_thickness = num(general, "thickness") if general else None
    tb = child(tree, "title_block")
    title = str(child(tb, "title")[1]) if tb and child(tb, "title") else ""
    return RawBoard(path=path, name=path.stem, tree=tree, version=version, generator=generator,
                    copper_layers=copper, all_layers=all_layers, file_thickness=file_thickness,
                    title=title, warnings=warnings)
