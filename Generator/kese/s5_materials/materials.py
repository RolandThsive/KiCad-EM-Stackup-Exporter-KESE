"""Stage 5 - materials: give every part of the PrismSet a material (its look) from
parameters/color.py, honouring the board's stackup colours when asked.  EM/physical properties
stay on the prisms."""
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
    colour, whose opacity is left to MATERIALS, mixed `lighten` of the way toward white.  -> None
    when the table has no colour for it."""
    user = _USER_COLOR.match(value)
    if user:
        return "#" + "".join(f"{round(c + lighten * (255 - c)):02X}" for c in _hex_to_rgb(user.group(1)))
    return table.get(value.lower())


def unknown_colors(stackup):
    """The stack-up's mask and silk colours that are neither a name in the tables nor #RRGGBB(AA):
    -> [(layer, value)]; those parts keep their MATERIALS colour."""
    C = P.Color
    tables = {"Mask": C.STACKUP_MASK_COLORS, "SilkS": C.STACKUP_SILK_COLORS}
    return [(layer, value) for layer, value in sorted(stackup.colors.items())
            if layer.split(".")[-1] in tables and not _USER_COLOR.match(value)
            and value.lower() not in tables[layer.split(".")[-1]]]


def _key(part, role, props, mode):
    mats = P.Color.MATERIALS
    if role == "board":
        kind = props.get("kind", "")
        return f"Board_{kind}" if P.Run.DIELECTRIC_GROUPING == "layer" and f"Board_{kind}" in mats else "Board"
    if role in ("copper", "plating"):
        if mode == "visual":
            return "Copper_exposed"
        return "Plating" if role == "plating" else "Copper"
    if role in ("mask", "mask_over_copper", "silk"):
        return part                                   # "Top Solder Mask", "Top Mask over Copper", ...
    if role == "finish":
        return props["metal"]                         # "Gold", "Nickel", ...
    return "Board"


def material_for(part, role, props, stackup, mode):
    C = P.Color
    key = _key(part, role, props, mode)
    m = dict(C.MATERIALS.get(key) or C.MATERIALS["Board"])
    m["name"] = key
    if C.USE_STACKUP_COLORS and stackup is not None:
        side, picked = "F" if part.startswith("Top") else "B", None
        if role in ("mask", "mask_over_copper"):
            over = role == "mask_over_copper" and mode == "visual"
            picked = _stackup_color(stackup.colors.get(f"{side}.Mask") or "",
                                    C.STACKUP_MASK_OVER_COPPER_COLORS if over else C.STACKUP_MASK_COLORS,
                                    C.USER_MASK_OVER_COPPER_LIGHTEN if over else 0.0)
        elif role == "silk":
            picked = _stackup_color(stackup.colors.get(f"{side}.SilkS") or "", C.STACKUP_SILK_COLORS)
        if picked:
            m["color"] = picked
    if mode == "visual" and role in ("mask", "mask_over_copper") and C.VISUAL_MASK_OPAQUE:
        m["alpha"] = 1.0
    m["rgb"] = _hex_to_rgb(m["color"])
    return m


def color(ps, stackup, mode, log=lambda s: None):
    """-> {part: material dict}; also writes prism.material."""
    if P.Color.USE_STACKUP_COLORS and stackup is not None:
        for layer, value in unknown_colors(stackup):
            log(f"warning: the stack-up colour {value!r} of {layer} is neither a colour name of "
                f"parameters/color.py nor #RRGGBBAA; its parts keep their MATERIALS colour")
    out = {}
    for p in ps.prisms:
        if p.part not in out:
            out[p.part] = material_for(p.part, p.role, p.props, stackup, mode)
        p.material = out[p.part]["name"]
    return out
