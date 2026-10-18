"""Finish.py - surface finish (ENIG, HASL, ...) on copper left bare by the solder mask."""
from Generator.Common import shapes as sh
from Parameters import P


def finish_type(st):
    F = P.Finish
    if F.FINISH_TYPE != "file":
        return F.FINISH_TYPE
    name = (st.copper_finish or "").replace(" ", "").replace("-", "_")
    for key in F.FINISH_TYPES:
        if key.lower() == name.lower():
            return key
    return F.FINISH_DEFAULT_TYPE


def build(b, ps):
    F, st = P.Finish, b.stackup
    if not F.FINISH_ENABLED:
        return
    kind = finish_type(st)
    layers = F.FINISH_TYPES.get(kind)
    if not layers:
        ps.notes.append(f"finish: unknown type {kind!r}, none applied")
        return
    ps.notes.append(f"finish: {kind} " + " + ".join(f"{m} {t} mm" for m, t in layers))
    for side, layer, sign, tb in (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom")):
        # one part per metal and side, or per metal and net (FINISH_GROUPING = "net")
        groups = b.copper[layer].items() if F.FINISH_GROUPING == "net" else [(None, b.copper_all.get(layer, sh.EMPTY))]
        for net, cu in groups:
            exposed = sh.inter(cu, b.mask_open[side])
            if exposed.is_empty:
                continue
            z = abs(st.band[layer][1] if sign > 0 else st.band[layer][0])
            for metal, t in layers:
                props = {"side": side, "metal": metal, "thickness_mm": t,
                         "conductivity_S_per_m": F.FINISH_CONDUCTIVITY_S_PER_M.get(metal, 0.0)}
                part = f"{tb} Finish {metal}" + (f"_{net}" if net is not None else "")
                ps.add(part, "finish", exposed, sign * z, sign * (z + t), layer=f"{side}.Finish", net=net, props=props)
                z += t
