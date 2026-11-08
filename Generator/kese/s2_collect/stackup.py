"""Stack-up: read from (setup (stackup ...)), or made from the parameters when the board has none."""
from kese.core.sexp import child, children, num, number
from kese.model.stackup import Dielectric, Stackup
from parameters import P


def read_stackup(setup, copper_layers, file_thickness, log):
    """Build the Stackup from the board's (setup (stackup ...)) or from the parameters."""
    B, C, M = P.Board, P.Copper, P.SolderMask
    st = child(setup, "stackup")
    cu_t, colors, mask_t, finish = {}, {}, None, None
    flags = {"edge_plating": False, "castellated_pads": False}
    gaps = []                          # dielectric layers between consecutive copper layers
    if st:
        cu_t, colors, mask_t, gaps = stackup_layers(st, log)
        cf = child(st, "copper_finish")
        if cf:
            finish = str(cf[1])
        flags = {k: str((child(st, k) or [None, "no"])[1]).lower() == "yes" for k in ("edge_plating", "castellated_pads")}
    n = len(copper_layers)
    for l in copper_layers:
        if l not in cu_t:
            cu_t[l] = C.DEFAULT_OUTER_FOIL_MM if l in ("F.Cu", "B.Cu") else C.DEFAULT_INNER_FOIL_MM

    usable = bool(st) and len(gaps) == n - 1 and all(sum(d.thickness for d in g) > 0 for g in gaps)
    inner_cu = sum(cu_t[l] for l in copper_layers[1:-1])
    if B.BOARD_THICKNESS_MM:
        laminate = B.BOARD_THICKNESS_MM
        source = "Board.BOARD_THICKNESS_MM"
        if usable:   # keep the stackup's proportions, scaled to the requested laminate
            total = sum(d.thickness for g in gaps for d in g)
            scale = (laminate - inner_cu) / total
            for g in gaps:
                for d in g:
                    d.thickness *= scale
            source += " (stackup dielectric proportions kept)"
    elif usable:
        laminate = sum(d.thickness for g in gaps for d in g) + inner_cu
        source = f"stackup dielectrics (+ inner copper); board total in file {file_thickness} mm"
    else:
        # KiCad's (general (thickness)) is the finished board: as KiCad's default stack-up does
        # (BOARD_STACKUP::BuildDefaultStackupList), the outer copper and the two masks come off it
        total = file_thickness or B.DEFAULT_BOARD_THICKNESS_MM
        mask = mask_t or M.MASK_OVER_COPPER_MM          # mask_t is only read when USE_STACKUP_MASK_THICKNESS
        laminate = total - cu_t[copper_layers[0]] - cu_t[copper_layers[-1]] - 2 * mask
        source = (f"file (general (thickness {total})) less the outer copper and the masks - no usable stackup"
                  if file_thickness else f"default {total} mm (Board.DEFAULT_BOARD_THICKNESS_MM) less the outer copper and the masks (no thickness in file)")
    if not usable:
        if B.DIELECTRIC_SPLIT != "even":
            log(f"warning: DIELECTRIC_SPLIT={B.DIELECTRIC_SPLIT!r} unknown, using 'even'")
        each = (laminate - inner_cu) / (n - 1)
        gaps = [[Dielectric(f"dielectric {k + 1}", B.DEFAULT_DIELECTRIC_TYPE, B.DEFAULT_DIELECTRIC_MATERIAL, each,
                            B.DEFAULT_EPSILON_R, B.DEFAULT_LOSS_TANGENT)] for k in range(n - 1)]
    note = f"(laminate {laminate:.4f} mm from {source}, {inner_cu:.4f} mm of it inner copper)"
    dielectrics = one_per_gap(gaps, copper_layers, note)
    return Stackup(copper_layers=copper_layers, copper_thickness=cu_t, dielectrics=dielectrics,
                   laminate_thickness=laminate, thickness_source=source, mask_thickness=mask_t,
                   colors=colors, copper_finish=finish,
                   edge_plating=flags["edge_plating"], castellated_pads=flags["castellated_pads"])


def stackup_layers(st, log):
    """The layers of (stackup ...), top to bottom -> (copper thickness {layer: mm}, colours {layer: name},
    mask thickness or None, [[Dielectric] between each two copper layers])."""
    B, C, M = P.Board, P.Copper, P.SolderMask
    cu_t, colors, mask_t, gaps = {}, {}, None, []
    acc, seen_cu = [], False
    for l in children(st, "layer"):
        name = str(l[1])
        t = sum(number(c[1], c) for c in children(l, "thickness")) or None
        if t is not None and t < 0:
            log(f"warning: stackup layer {name}: thickness {t} mm is less than 0: read as not given")
            t = None
        typ = (child(l, "type") or [None, ""])[1].lower()
        col = child(l, "color")
        if col:
            colors[name] = str(col[1])
        if name.endswith(".Cu"):
            if t and C.USE_STACKUP_COPPER_THICKNESS:
                cu_t[name] = t
            if seen_cu:
                gaps.append(acc)
            acc, seen_cu = [], True
        elif name.endswith(".Mask"):
            if t and M.USE_STACKUP_MASK_THICKNESS and mask_t is None:
                mask_t = t
        elif seen_cu and (typ in ("core", "prepreg", "dielectric") or name.startswith("dielectric")):
            acc.append(Dielectric(
                name=name, kind=typ if typ in ("core", "prepreg") else B.DEFAULT_DIELECTRIC_TYPE,
                material=(child(l, "material") or [None, B.DEFAULT_DIELECTRIC_MATERIAL])[1],
                thickness=t or 0.0,
                epsilon_r=num(l, "epsilon_r", B.DEFAULT_EPSILON_R) if B.USE_STACKUP_EPSILON_R else B.DEFAULT_EPSILON_R,
                loss_tangent=num(l, "loss_tangent", B.DEFAULT_LOSS_TANGENT) if B.USE_STACKUP_LOSS_TANGENT else B.DEFAULT_LOSS_TANGENT))
    return cu_t, colors, mask_t, gaps


def one_per_gap(gaps, copper_layers, laminate_note):
    """One Dielectric per gap between two copper layers (a gap made of several prepreg plies is one solid
    of the summed thickness), with the copper above and below it; `laminate_note` explains a gap that
    comes out too thin."""
    dielectrics = []
    for k, g in enumerate(gaps):
        d = g[0]
        if len(g) > 1:
            d = Dielectric(" + ".join(x.name for x in g), g[0].kind, g[0].material, sum(x.thickness for x in g),
                           g[0].epsilon_r, g[0].loss_tangent)
        d.above, d.below = copper_layers[k], copper_layers[k + 1]
        if d.thickness <= 0:             # a board too thin for its copper: every part would be turned inside out
            raise ValueError(f"the dielectric between {d.above} and {d.below} comes out {d.thickness:.4f} mm thick "
                             f"{laminate_note}: "
                             "the board is too thin for its copper; set Board.BOARD_THICKNESS_MM (parameters/board.py)")
        dielectrics.append(d)
    return dielectrics
