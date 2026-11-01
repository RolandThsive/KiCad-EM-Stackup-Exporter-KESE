"""Stage 1 - read: the .kicad_pcb file -> RawBoard: the parsed tree and the copper layers,
after checking it is a board KESE can handle."""
import re
from pathlib import Path

from kese.core.sexp import child, num, parse
from kese.model.raw_board import RawBoard
from kese.s1_read import parse_kicad_version as kv
from parameters import P

TESTED_COPPER_LAYERS = 8      # the most copper layers among the test boards (featureTest/05_vias_micro)


def run(pcb_path, job):
    with job.stage("read", "read"):
        raw = read(pcb_path)
        job.say(f"{raw.name}: {raw.dialect.describe()}, {len(raw.copper_layers)} copper layers, mode {job.mode}")
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
    d = kv.dialect(tree)
    gen = child(tree, "generator")
    generator = f"{gen[1]}" if gen else "unknown"
    gv = child(tree, "generator_version")
    if gv:
        generator += f" {gv[1]}"
    w = kv.tested_range_warning(d, P.Run.KICAD_VERSION_MIN, P.Run.KICAD_VERSION_MAX)
    if w:
        warnings.append(w)

    layers_node = child(tree, "layers")
    if not layers_node:
        raise ValueError(f"{path.name}: no (layers ...) block")
    renamed = kv.copper_layer_names(layers_node)
    if renamed:
        kv.rename_layers(tree, renamed)
        warnings.append("layers named by the user or in an old language, read as KiCad reads them: "
                        + ", ".join(f"{a} = {b}" for a, b in renamed.items()))
    all_layers = [str(l[1]) for l in layers_node[1:] if isinstance(l, list) and len(l) > 1]
    names = [l for l in all_layers if l.endswith(".Cu")]
    inner = sorted((n for n in names if n.startswith("In")), key=lambda n: int(re.sub(r"\D", "", n)))
    copper = ["F.Cu"] + inner + ["B.Cu"]
    missing = [l for l in ("F.Cu", "B.Cu") if l not in names]
    if missing:
        raise ValueError(f"{path.name}: copper layers {missing} are not declared")
    if len(copper) > TESTED_COPPER_LAYERS:
        warnings.append(f"{len(copper)} copper layers: more than the {TESTED_COPPER_LAYERS} this project has been tested with")

    general = child(tree, "general")
    file_thickness = num(general, "thickness") if general else None
    tb = child(tree, "title_block")
    title = str(child(tb, "title")[1]) if tb and child(tb, "title") else ""
    return RawBoard(path=path, name=path.stem, tree=tree, dialect=d, generator=generator,
                    copper_layers=copper, all_layers=all_layers, file_thickness=file_thickness,
                    title=title, warnings=warnings)

