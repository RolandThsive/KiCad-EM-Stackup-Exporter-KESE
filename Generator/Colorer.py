"""Step 4 - Colorer: give every part a material (its look) from Color_Parameters, honouring the
board's stackup colours when asked.  EM/physical properties stay on the prisms."""
from Parameters import P


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _key(part, role, props, mode):
    mats = P.Color.MATERIALS
    if role == "board":
        kind = props.get("kind", "")
        return f"Board_{kind}" if P.Run.DIELECTRIC_GROUPING == "layer" and f"Board_{kind}" in mats else "Board"
    if role in ("copper", "plating"):
        if mode == "pretty":
            return "Copper_exposed"
        return "Plating" if role == "plating" else "Copper"
    if role in ("mask", "mask_over_copper", "silk"):
        return part                                   # "Top Solder Mask", "Top Mask over Copper", ...
    if role == "finish":
        return part.split()[-1]                       # "Top Finish Gold" -> "Gold"
    return "Board"


def material_for(part, role, props, stackup, mode):
    C = P.Color
    key = _key(part, role, props, mode)
    m = dict(C.MATERIALS.get(key) or C.MATERIALS["Board"])
    m["name"] = key
    if C.USE_STACKUP_COLORS and stackup is not None:
        side = "F" if part.startswith("Top") else "B"
        mask_name = (stackup.colors.get(f"{side}.Mask") or "").lower()
        if role in ("mask", "mask_over_copper") and mask_name:
            table = C.STACKUP_MASK_OVER_COPPER_COLORS if (role == "mask_over_copper" and mode == "pretty") \
                else C.STACKUP_MASK_COLORS
            if table.get(mask_name):
                m["color"] = table[mask_name]
        silk_name = (stackup.colors.get(f"{side}.SilkS") or "").lower()
        if role == "silk" and C.STACKUP_SILK_COLORS.get(silk_name):
            m["color"] = C.STACKUP_SILK_COLORS[silk_name]
    if mode == "pretty" and role in ("mask", "mask_over_copper") and C.PRETTY_MASK_OPAQUE:
        m["alpha"] = 1.0
    m["rgb"] = _hex_to_rgb(m["color"])
    return m


def color(ps, stackup, mode):
    """-> {part: material dict}; also writes prism.material."""
    out = {}
    for p in ps.prisms:
        if p.part not in out:
            out[p.part] = material_for(p.part, p.role, p.props, stackup, mode)
        p.material = out[p.part]["name"]
    return out
