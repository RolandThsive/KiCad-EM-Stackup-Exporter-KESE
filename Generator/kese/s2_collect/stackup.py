"""Stack-up: read from (setup (stackup ...)), or made from the parameters when the board has none.
What each gap between two copper layers is made of, ply by ply, is plies.py."""
from kese.core.dielectric import check_models
from kese.core.sexp import child, children, num, number, word
from kese.model.stackup import Ply, Stackup
from kese.s2_collect.plies import by_hand, file_plies, fused, of_plies, solids
from parameters import GROUPS, P


def read_stackup(setup, copper_layers, file_thickness, log, board=""):
    """Build the Stackup from the board's (setup (stackup ...)) or from the parameters; `board`: the
    board file's name without .kicad_pcb, for Board.PLIES_BY_HAND."""
    B, C, M = P.Board, P.Copper, P.SolderMask
    st = child(setup, "stackup")
    cu_t, colors, mask_t, finish, mask_materials = {}, {}, None, None, {}
    flags = {"edge_plating": False, "castellated_pads": False}
    gaps = []                          # dielectric layers between consecutive copper layers
    if st:
        cu_t, colors, mask_t, gaps, mask_materials = stackup_layers(st, log)
        cf = word(st, "copper_finish")
        if cf is not None:
            finish = str(cf)
        flags = {k: str(word(st, k, "no")).lower() == "yes" for k in ("edge_plating", "castellated_pads")}
    n = len(copper_layers)
    for l in copper_layers:
        if l not in cu_t:
            cu_t[l] = {"F.Cu": C.DEFAULT_TOP_FOIL_MM, "B.Cu": C.DEFAULT_BOTTOM_FOIL_MM}.get(l, C.DEFAULT_INNER_FOIL_MM)
    if B.PLIES_BY_HAND.get(board) and len(gaps) != n - 1:
        gaps = [[] for _ in range(n - 1)]             # no usable stack-up in the file: every gap empty, but those by hand
    hand = by_hand(board, copper_layers, gaps) if gaps else []

    usable = len(gaps) == n - 1 and all(sum(d.thickness for d in g) > 0 for g in gaps)
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
                    for ply in d.plies:
                        ply.thickness *= scale
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
        given = sum(d.thickness for k in hand for d in gaps[k])       # the gaps given by hand keep their plies
        each = (laminate - inner_cu - given) / (n - 1 - len(hand))
        gaps = [gaps[k] if k in hand else [default_dielectric(f"dielectric {k + 1}", each)] for k in range(n - 1)]
    note = f"(laminate {laminate:.4f} mm from {source}, {inner_cu:.4f} mm of it inner copper)"
    dielectrics = one_per_gap(gaps, copper_layers, note, log)
    check_models(dielectrics, log)
    if P.Stackup.FUSION_BUILD == "PLIES_SEPARATE":
        for d in dielectrics:
            d.solids = solids(d, log)
    stackup = Stackup(copper_layers=copper_layers, copper_thickness=cu_t, dielectrics=dielectrics,
                      laminate_thickness=laminate, thickness_source=source, mask_thickness=mask_t,
                      colors=colors, copper_finish=finish, mask_materials=mask_materials,
                      edge_plating=flags["edge_plating"], castellated_pads=flags["castellated_pads"])
    if any(P.value(f"Stackup.{line}") for line in GROUPS["finish"]):
        finish_type(stackup)                           # a finish that cannot be built stops the run here
    return stackup


def default_dielectric(name, thickness):
    """A dielectric of one ply with the parameters' values, where the board file gives none."""
    B = P.Board
    return of_plies(name, [Ply(name, B.DEFAULT_DIELECTRIC_TYPE, B.DEFAULT_DIELECTRIC_MATERIAL, thickness,
                               B.DEFAULT_EPSILON_R, B.DEFAULT_LOSS_TANGENT, B.DEFAULT_SPEC_FREQUENCY_HZ,
                               B.DIELECTRIC_MODEL, of=name)])


def stackup_layers(st, log):
    """The layers of (stackup ...), top to bottom -> (copper thickness {layer: mm}, colours {layer: name},
    mask thickness or None, [[Dielectric] between each two copper layers], what each mask layer gives
    of its material {layer: {material, epsilon_r, loss_tangent}})."""
    B, C, M = P.Board, P.Copper, P.SolderMask
    cu_t, colors, mask_t, gaps, mask_materials = {}, {}, None, [], {}
    acc, seen_cu = [], False
    for l in children(st, "layer"):
        name = str(l[1])
        typ = str(word(l, "type", "")).lower()
        col = word(l, "color")
        if col is not None:
            colors[name] = str(col)
        if seen_cu and not name.endswith((".Cu", ".Mask")) and (typ in ("core", "prepreg", "dielectric") or name.startswith("dielectric")):
            acc.append(of_plies(name, file_plies(l, name, typ if typ in ("core", "prepreg") else B.DEFAULT_DIELECTRIC_TYPE, log)))
            continue
        t = sum(number(c[1] if len(c) > 1 else None, c) for c in children(l, "thickness")) or None
        if t is not None and t < 0:
            log(f"warning: stackup layer {name}: thickness {t} mm is less than 0: read as not given")
            t = None
        if name.endswith(".Cu"):
            if t and C.USE_STACKUP_COPPER_THICKNESS:
                cu_t[name] = t
            if seen_cu:
                gaps.append(acc)
            acc, seen_cu = [], True
        elif name.endswith(".Mask"):
            if t and M.USE_STACKUP_MASK_THICKNESS and mask_t is None:
                mask_t = t
            given = {"material": word(l, "material"), "epsilon_r": num(l, "epsilon_r"),
                     "loss_tangent": num(l, "loss_tangent")}
            mask_materials[name] = {k: v for k, v in given.items() if v is not None}
    return cu_t, colors, mask_t, gaps, mask_materials


def one_per_gap(gaps, copper_layers, laminate_note, log):
    """One Dielectric per gap between two copper layers (a gap made of several dielectrics is one of
    the summed thickness, plies.py fused()), with the copper above and below it and its plies;
    `laminate_note` explains a gap that comes out too thin."""
    dielectrics = []
    for k, g in enumerate(gaps):
        d = fused(g, log)
        d.above, d.below = copper_layers[k], copper_layers[k + 1]
        if d.thickness <= 0:             # a board too thin for its copper: every part would be turned inside out
            raise ValueError(f"the dielectric between {d.above} and {d.below} comes out {d.thickness:.4f} mm thick "
                             f"{laminate_note}: "
                             "the board is too thin for its copper; set Board.BOARD_THICKNESS_MM (parameters/PCB_elements/Board.py)")
        dielectrics.append(d)
    return dielectrics


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
                         "> Copper finish), or leave the finish out (the three finish lines of Stackup.py False). "
                         "On the command line: --set Finish.FINISH_TYPE=ENIG, or --set Stackup.finish=False")
    if name == "none":
        return None                                      # the board says: no finish
    for key in list(F.FINISH_TYPES) + list(F.FINISH_NAME_ALIASES):
        if fold(key) == name:
            return F.FINISH_NAME_ALIASES.get(key, key)
    raise ValueError(f"FINISH ERROR: the KiCad file's finish {st.copper_finish!r} is not one KESE knows. Change "
                     f"Finish.FINISH_TYPE to one of {', '.join(F.FINISH_TYPES)}, or add the name to "
                     "Finish.FINISH_NAME_ALIASES, or correct the finish in KiCad")
