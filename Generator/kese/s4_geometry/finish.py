"""Surface finish (ENIG, HASL, ...) on the copper the solder mask leaves bare: the type and its
layers, and the finish on the faces of the top and bottom copper.  The finish on the walls, in the
holes, on the plated edge and in the castellations is finish_shells.py (shells.py lays them)."""
from kese.core import shapes2d as sh
from kese.core.conformal import grow
from kese.core.shapes2d import EMPTY
from parameters import P

MITRE = {"join_style": "mitre", "mitre_limit": 2.0}   # how the finish follows the copper's corners: a shell's
                                                      # outer side (shells.py) and the copper the mask wraps


def finish_type(st):
    """The key of FINISH_TYPES the board gets, or None when its stack-up says "None".  Raises
    ValueError for an unknown FINISH_TYPE, and with "file" for a board that names no finish or one
    KESE does not know."""
    F = P.Finish
    if F.FINISH_TYPE != "file":
        if F.FINISH_TYPE not in F.FINISH_TYPES:
            raise ValueError(f"FINISH ERROR: Finish.FINISH_TYPE = {F.FINISH_TYPE!r} is not a finish KESE knows; "
                             f"use \"file\" or one of {', '.join(F.FINISH_TYPES)}")
        return F.FINISH_TYPE
    fold = lambda s: s.lower().replace(" ", "").replace("-", "").replace("_", "")
    name = fold(st.copper_finish or "")
    if not name:
        raise ValueError("FINISH ERROR: Finish.FINISH_TYPE = \"file\" but no finish was found in the KiCad file "
                         "(no stack-up, or its Copper finish is empty). Change Finish.FINISH_TYPE to one of "
                         f"{', '.join(F.FINISH_TYPES)}, or set the finish in KiCad (Board Setup > Physical Stackup "
                         "> Copper finish), or turn the finish off (Finish.FINISH_ENABLED = False)")
    if name == "none":
        return None                                      # the board says: no finish
    for key in list(F.FINISH_TYPES) + list(F.FINISH_NAME_ALIASES):
        if fold(key) == name:
            return F.FINISH_NAME_ALIASES.get(key, key)
    raise ValueError(f"FINISH ERROR: the KiCad file's finish {st.copper_finish!r} is not one KESE knows. Change "
                     f"Finish.FINISH_TYPE to one of {', '.join(F.FINISH_TYPES)}, or add the name to "
                     "Finish.FINISH_NAME_ALIASES, or correct the finish in KiCad")


def finish_layers(st):
    """[(metal, mm)] of the finish the board gets, bottom to top, or None (off, or "None" in the
    file); -> (layers, type)."""
    F = P.Finish
    if not F.FINISH_ENABLED:
        return None, None
    kind = finish_type(st)
    return (F.FINISH_TYPES[kind] if kind is not None else None), kind


def under_mask_mm(st):
    """How much the finish raises the copper under the solder mask: its whole thickness when it goes
    on before the mask (FINISH_BEFORE_SOLDER_MASK), else 0.  The mask and the silkscreen on it sit
    this much higher over copper."""
    layers, _ = finish_layers(st)
    return sum(t for _, t in layers) if layers and P.Finish.FINISH_BEFORE_SOLDER_MASK else 0.0


def under_mask_copper(st, cu):
    """The copper the mask lies on, board frame: `cu` itself, or, with the finish applied before the
    mask, `cu` grown by the finish on its side walls (on the snapping grid), which the mask wraps."""
    layers, _ = finish_layers(st)
    if not (under_mask_mm(st) and layers) or cu.is_empty:
        return cu
    reach = sum(drawn_thickness(t) for _, t in layers)
    return grow(cu, reach, **MITRE)


def exposed(r, side, cu, take=lambda g: g):
    """The part of `cu` (copper on side's outer layer) the finish lands on.  Applied before the
    mask (FINISH_BEFORE_SOLDER_MASK) that is all of it; after the mask, only what is in a mask
    opening and not under ink kept in the opening (SILKSCREEN_OVER_COPPER: printed before the
    finish).  take(shape): the board's shapes as used (own, in a thread)."""
    if P.Finish.FINISH_BEFORE_SOLDER_MASK:
        return cu
    bare = sh.inter(cu, take(r.mask_open[side]))
    if P.Silkscreen.SILKSCREEN_OVER_COPPER:
        inked = take(r.silk.get(side, EMPTY))
        if not inked.is_empty:
            bare = sh.diff(bare, inked)
    return bare


def props(side, metal, t, **kw):
    """The finish part's properties for materials.json."""
    return {"side": side, "metal": metal, "thickness_mm": t,
            "conductivity_S_per_m": P.Finish.FINISH_CONDUCTIVITY_S_PER_M.get(metal, 0.0), **kw}


def build(r, ps):
    """The finish on the faces of the top and bottom copper, stacked upward from the copper.  The
    walls, the holes, the plated edge and the castellations are finish_shells.build."""
    F, st = P.Finish, r.stackup
    if not F.FINISH_ENABLED:
        return
    layers, kind = finish_layers(st)
    if kind is None:
        ps.notes.append("finish: the board's stackup says None, nothing applied")
        return
    ps.notes.append(f"finish: {kind} " + " + ".join(f"{m} {t} mm" for m, t in layers)
                    + (", before the solder mask: on all the outer copper, under the mask"
                       if F.FINISH_BEFORE_SOLDER_MASK else ""))
    for side, layer, sign, tb in (("F", "F.Cu", 1, "Top"), ("B", "B.Cu", -1, "Bottom")):
        # one part per metal and side, or per metal and net (FINISH_GROUPING = "net")
        groups = r.copper[layer].items() if F.FINISH_GROUPING == "net" else [(None, r.copper_all.get(layer, EMPTY))]
        for net, cu in groups:
            bare = exposed(r, side, cu)
            if bare.is_empty:
                continue
            z = abs(st.band[layer][1] if sign > 0 else st.band[layer][0])
            for metal, t in layers:
                part = f"{tb} Finish {metal}" + (f"_{net}" if net is not None else "")
                ps.add(part, "finish", bare, sign * z, sign * (z + t), layer=f"{side}.Finish", net=net,
                       props=props(side, metal, t))
                z += t


def drawn_thickness(t):
    """A finish metal's thickness as drawn across a wall, where it is a 2D shape on the snapping grid:
    the nearest whole number of grid steps, at least one (a thinner film is drawn one step thick)."""
    g = sh.grid()
    return max(1, round(t / g)) * g
