"""Stage 1 - read: the .kicad_pcb file -> RawBoard: the parsed tree and the copper layers,
after checking it is a board KESE can handle."""
import re
from pathlib import Path

from kese.core.sexp import NotANumber, child, num, parse
from kese.model.raw_board import RawBoard
from kese.s1_read import parse_kicad_version as kv
from parameters import P


def run(pcb_path, job):
    with job.stage("read", "read"):
        try:
            raw = read(pcb_path)
        except NotANumber as exc:
            raise NotANumber(f"{Path(pcb_path).name}: {exc}") from None
        job.say(f"{raw.name}: {raw.dialect.describe()}, {len(raw.copper_layers)} copper layers, mode {job.mode}")
        for w in raw.warnings:
            job.note(f"warning: {w}")
    return raw


def read(path):
    path = Path(path)
    try:                        # utf-8-sig: a byte order mark an editor put in front is passed over
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path.name} is not a KiCad board file: it is not UTF-8 text, as KiCad writes "
                         f"(byte 0x{exc.object[exc.start]:02x} at {exc.start})") from None
    try:
        tree = parse(text)
    except ValueError as exc:
        raise ValueError(f"{path.name}: {exc}") from None
    if not tree or tree[0] != "kicad_pcb":
        raise ValueError(f"{path.name} is not a KiCad board file (expected (kicad_pcb ...))")
    warnings = []
    d = kv.dialect(tree)
    gen = child(tree, "generator")
    generator = str(gen[1]) if gen else "unknown"
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
    tested = P.Run.TESTED_COPPER_LAYERS
    if len(copper) > tested:
        warnings.append(f"{len(copper)} copper layers: more than the {tested} this project has been tested with")

    general = child(tree, "general")
    file_thickness = num(general, "thickness") if general else None
    if file_thickness is not None and file_thickness <= 0:
        warnings.append(f"board thickness in the file is {file_thickness} mm: read as not given")
        file_thickness = None
    tb = child(tree, "title_block")
    title = str(child(tb, "title")[1]) if tb and child(tb, "title") else ""
    return RawBoard(path=path, name=path.stem, tree=tree, dialect=d, generator=generator,
                    copper_layers=copper, file_thickness=file_thickness,
                    title=title, warnings=warnings)

