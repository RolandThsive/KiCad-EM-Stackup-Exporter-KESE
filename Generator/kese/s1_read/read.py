"""Stage 1 - read: the .kicad_pcb file -> RawBoard: the parsed tree and the copper layers,
after checking it is a board KESE can handle."""
import re
from pathlib import Path

from kese.core.sexp import child, num, parse
from kese.model.raw_board import RawBoard
from parameters import P

TESTED_COPPER_LAYERS = 8      # the most copper layers among the test boards (featureTest/05_vias_micro)


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
    renamed = _canonical_copper_names(layers_node)
    if renamed:
        _rename_layers(tree, renamed)
        warnings.append("copper layers named by the user, read by their number: "
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
    return RawBoard(path=path, name=path.stem, tree=tree, version=version, generator=generator,
                    copper_layers=copper, all_layers=all_layers, file_thickness=file_thickness,
                    title=title, warnings=warnings)


COPPER_TYPES = ("signal", "power", "mixed", "jumper")
CANONICAL_COPPER = re.compile(r"F\.Cu|B\.Cu|In\d+\.Cu")


def _canonical_copper_names(layers_node):
    """KiCad 4 and 5 write a copper layer the user renamed under its new name only, e.g.
    (0 TOP_L1.Sig mixed) or (1 GND.Cu power), and every item on it uses that name; its number says
    which layer it is (0 = F.Cu, 31 = B.Cu, n = In<n>.Cu).  KiCad 6 and later keep the canonical
    name and put the user's name after the type.
    -> {user name: canonical name} for the renamed copper layers, or {}."""
    renamed = {}
    for l in layers_node[1:]:
        if not (isinstance(l, list) and len(l) > 2 and str(l[0]).isdigit()):
            continue
        name, kind, number = str(l[1]), str(l[2]), int(l[0])
        if kind in COPPER_TYPES and not CANONICAL_COPPER.fullmatch(name) and 0 <= number <= 31:
            renamed[name] = "F.Cu" if number == 0 else "B.Cu" if number == 31 else f"In{number}.Cu"
    return renamed


def _rename_layers(node, renamed):
    """Every (layer ...) and (layers ...) in the tree, and the (layers ...) block itself, with the
    user's copper names replaced by the canonical ones."""
    stack = [node]
    while stack:
        n = stack.pop()
        if n and n[0] in ("layer", "layers"):
            for i in range(1, len(n)):
                if isinstance(n[i], str) and n[i] in renamed:
                    n[i] = renamed[n[i]]
                elif isinstance(n[i], list) and len(n[i]) > 1 and isinstance(n[i][1], str) and n[i][1] in renamed:
                    n[i][1] = renamed[n[i][1]]      # the board's (layers (0 TOP_L1.Sig mixed) ...) block
        stack.extend(c for c in n if isinstance(c, list))
