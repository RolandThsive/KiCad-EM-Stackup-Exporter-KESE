"""Stage 5 - materials: give every part of the PrismSet a material (its look) from the Color
section of its element's file in parameters/PCB_elements/, honouring the board's stackup colours
when asked.  EM/physical properties stay on the prisms."""
import re

from parameters import P

_USER_COLOR = re.compile(r"#([0-9A-Fa-f]{6})(?:[0-9A-Fa-f]{2})?$")   # KiCad's "User defined": #RRGGBBAA


def run(ps, job):
    with job.stage("materials", "materials (a colour per part)"):
        ps.materials = color(ps, ps.regions.stackup, job.mode, job.note)
    return ps


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _stackup_color(value, table, lighten=0.0):
    """The colour a stack-up colour stands for: a colour name looked up in `table`, or a user-defined
    colour, whose opacity is left to the part's colour setting, mixed `lighten` of the way toward white.  -> None
    when the table has no colour for it."""
    user = _USER_COLOR.match(value)
    if user:
        return "#" + "".join(f"{round(c + lighten * (255 - c)):02X}" for c in _hex_to_rgb(user.group(1)))
    return table.get(value.lower())


def looks():
    """{a look's name: its colour setting}, each from its element's file: the laminate's by kind,
    the copper's, the mask's and the ink's by part, the finish's by metal."""
    B, C, M, S = P.Board, P.Copper, P.SolderMask, P.SilkScreen
    return {"Board": B.BOARD_COLOR, "Board_core": B.CORE_COLOR, "Board_prepreg": B.PREPREG_COLOR,
            "Board_resin": B.RESIN_COLOR, "Copper": C.COPPER_COLOR, "Plating": C.PLATING_COLOR,
            "Copper_exposed": C.EXPOSED_COPPER_COLOR, "Via Resin": C.VIA_RESIN_COLOR,
            "Top Solder Mask": M.TOP_MASK_COLOR, "Bottom Solder Mask": M.BOTTOM_MASK_COLOR,
            "Top Mask over Copper": M.TOP_MASK_OVER_COPPER_COLOR, "Bottom Mask over Copper": M.BOTTOM_MASK_OVER_COPPER_COLOR,
            "Top Silkscreen": S.TOP_SILK_COLOR, "Bottom Silkscreen": S.BOTTOM_SILK_COLOR, **P.Finish.FINISH_COLORS}


def stackup_tables():
    """{"Mask" / "SilkS": the table of colour names} for the layers whose stack-up colour is honoured."""
    M, S = P.SolderMask, P.SilkScreen
    return {**({"Mask": M.STACKUP_MASK_COLORS} if M.USE_STACKUP_MASK_COLOR else {}),
            **({"SilkS": S.STACKUP_SILK_COLORS} if S.USE_STACKUP_SILK_COLOR else {})}


def unknown_colors(stackup):
    """The stack-up's mask and silk colours that are neither a name in the tables nor #RRGGBB(AA):
    -> [(layer, value)]; those parts keep the colour of their file."""
    tables = stackup_tables()
    return [(layer, value) for layer, value in sorted(stackup.colors.items())
            if layer.split(".")[-1] in tables and not _USER_COLOR.match(value)
            and value.lower() not in tables[layer.split(".")[-1]]]


def _key(part, role, props, mode, mats):
    if role == "board":
        kind = props.get("kind", "")
        return f"Board_{kind}" if P.Board.DIELECTRIC_GROUPING == "layer" and f"Board_{kind}" in mats else "Board"
    if role in ("copper", "plating"):
        if mode == "visual":
            return "Copper_exposed"
        return "Plating" if role == "plating" else "Copper"
    if role in ("mask", "mask_over_copper", "silk"):
        return part                                   # "Top Solder Mask", "Top Mask over Copper", ...
    if role == "finish":
        return props["metal"]                         # "Gold", "Nickel", ...
    if role == "via_resin":
        return "Via Resin"
    return "Board"


def material_for(part, role, props, stackup, mode):
    M, S, mats = P.SolderMask, P.SilkScreen, looks()
    key = _key(part, role, props, mode, mats)
    m = dict(mats.get(key) or mats["Board"])
    m["name"] = key
    side, picked = "F" if part.startswith("Top") else "B", None
    if role in ("mask", "mask_over_copper") and M.USE_STACKUP_MASK_COLOR:
        over = role == "mask_over_copper" and mode == "visual"
        picked = _stackup_color(stackup.colors.get(f"{side}.Mask") or "",
                                M.STACKUP_MASK_OVER_COPPER_COLORS if over else M.STACKUP_MASK_COLORS,
                                M.USER_MASK_OVER_COPPER_LIGHTEN if over else 0.0)
    elif role == "silk" and S.USE_STACKUP_SILK_COLOR:
        picked = _stackup_color(stackup.colors.get(f"{side}.SilkS") or "", S.STACKUP_SILK_COLORS)
    if picked:
        m["color"] = picked
    if mode == "visual" and role in ("mask", "mask_over_copper") and M.VISUAL_MASK_OPAQUE:
        m["alpha"] = 1.0
    m["rgb"] = _hex_to_rgb(m["color"])
    return m


def color(ps, stackup, mode, log):
    """-> {part: material dict}; also writes prism.material."""
    for layer, value in unknown_colors(stackup):
        log(f"warning: the stack-up colour {value!r} of {layer} is neither a colour name of its table "
            f"(parameters/PCB_elements/{'SolderMask' if layer.endswith('Mask') else 'SilkScreen'}.py) nor "
            "#RRGGBBAA; its parts keep the colour of that file")
    out = {}
    for p in ps.prisms:
        if p.part not in out:
            out[p.part] = material_for(p.part, p.role, p.props, stackup, mode)
        p.material = out[p.part]["name"]
    return out
