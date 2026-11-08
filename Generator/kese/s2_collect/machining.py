"""KiCad 10's extra drills of pads and vias - backdrills, tertiary drills, counterbores and
countersinks - and the protection of vias: covering, plugging, capping and filling (IPC-4761).
They are read here; stage 3 drills and cuts them, stage 4 builds the plugs and fills."""
import math

from kese.core.sexp import child, num, yes
from kese.core.shapes2d import disk
from kese.model.items import Hole, PostMachining, Protection
from parameters import P

PROTECTION = ("covering", "plugging", "capping", "filling")
DRILLS = {"backdrill": "backdrills", "tertiary_drill": "tertiary drills"}
POST = {"front_post_machining": "F", "back_post_machining": "B"}
MODES = ("counterbore", "countersink")
# how report.txt names what a setting switches off; the "not modelled" warning lists these (left_out.warn)
BACKDRILLS_OFF = " (Board.BACKDRILLS is False)"
POST_MACHINING_OFF = " (Board.POST_MACHINING is False)"
PROTECTION_OFF = ' (Copper.VIA_PROTECTION is "off")'
SWITCHED_OFF = (BACKDRILLS_OFF, POST_MACHINING_OFF, PROTECTION_OFF)


def sides(node, default):
    """(key (front yes) (back no)), or (key yes) for both sides -> {"F": bool, "B": bool}; a side
    the node leaves out, or says "none" for, keeps `default`, as KiCad's parseOptBool leaves it unset."""
    out = dict(default)
    if node is not None and len(node) > 1 and not isinstance(node[1], list):
        return out if str(node[1]) == "none" else {"F": yes(node[1]), "B": yes(node[1])}
    for side, key in (("F", "front"), ("B", "back")):
        c = child(node, key) if node is not None else None
        if c is not None and len(c) > 1 and str(c[1]) != "none":
            out[side] = yes(c[1])
    return out


def protection_defaults(setup):
    """KiCad 10's board setup: whether a via that does not say is covered, plugged, capped or filled
    (covering and plugging per side, capping and filling one flag for both)."""
    return {key: sides(child(setup, key), {"F": False, "B": False}) for key in PROTECTION}


def drills_of(ctx, node, center, what, of):
    """A pad's or via's backdrill and tertiary drill (KiCad 10, (backdrill (size d) (layers start
    must-cut))) as Holes of kind "backdrill" in Items.holes, from the start layer through the must-cut
    layer; `of` is the index of the hole they drill out.  -> the board faces they open."""
    items, opened = ctx.items, {"F": False, "B": False}
    last = len(ctx.layers) - 1
    for key, name in DRILLS.items():
        c = child(node, key)
        if c is None:
            continue
        if not P.Board.BACKDRILLS:
            items.skipped[f"{name} of {what}{BACKDRILLS_OFF}"] += 1
            continue
        size = num(c, "size", 0.0)
        ends = [str(x) for x in (child(c, "layers") or [])[1:3]]
        if size <= 0:
            items.skipped[f"{name} of {what} with no size (left out)"] += 1
        elif len(ends) < 2 or not set(ends) <= set(ctx.layers):
            items.skipped[f"{name} of {what} on a copper layer the board does not have (left out)"] += 1
        elif of < 0:
            items.skipped[f"{name} of {what} with no hole (left out, as KiCad does)"] += 1
        else:
            a, b = sorted(ctx.layers.index(e) for e in ends)
            items.holes.append(Hole(disk(center, size / 2), a, b, False, "", 0.0, kind="backdrill", of=of))
            items.found[f"{name} of {what}"] += 1
            opened["F"] |= a == 0
            opened["B"] |= b == last
    return opened


def post_machining_of(ctx, node, center, what, of):
    """A pad's or via's counterbores and countersinks (KiCad 10, (front_post_machining counterbore
    (size d) (depth h)), (back_post_machining countersink (size d) (angle a))) into Items.post_machining,
    when KiCad's STEP export would cut them: a size, and a depth (counterbore) or an angle (countersink).
    -> the board faces they open."""
    items, opened = ctx.items, {"F": False, "B": False}
    for key, side in POST.items():
        c = child(node, key)
        if c is None or len(c) < 2:
            continue
        mode = str(c[1])
        if mode not in MODES:
            items.skipped[f"post machining of {what} of a kind KESE does not know ({mode})"] += 1
            continue
        if not P.Board.POST_MACHINING:
            items.skipped[f"{mode}s of {what}{POST_MACHINING_OFF}"] += 1
            continue
        size, depth = num(c, "size", 0.0), num(c, "depth", 0.0)
        angle = math.floor(num(c, "angle", 0.0) * 10 + 0.5) / 10      # KiCad keeps tenths of a degree (KiROUND)
        valid = size > 0 and (depth > 0 if mode == "counterbore" else 0 < angle < 180)
        if not valid:
            need = "depth" if mode == "counterbore" else "angle between 0 and 180 degrees"
            items.skipped[f"{mode}s of {what} with no size or no {need} (not cut, as KiCad does)"] += 1
        elif of < 0:
            items.skipped[f"{mode}s of {what} with no hole (left out, as KiCad does)"] += 1
        else:
            items.post_machining.append(PostMachining(center, side, mode, size, max(depth, 0.0), angle, of))
            items.found[f"{mode}s of {what}"] += 1
            opened[side] = True
    return opened


def protection_of(ctx, node, i, j, opened):
    """A via's Protection from its (covering ...), (plugging ...), (capping ...) and (filling ...),
    and the board's setup where it leaves one out or says none; None when it has none, or when
    Copper.VIA_PROTECTION is "off".  An end inside the board (a blind or buried via's) takes no
    plug, covering or cap."""
    items = ctx.items
    got = {key: sides(child(node, key), items.via_protection.get(key, {"F": False, "B": False}))
           for key in PROTECTION}
    if not any(any(v.values()) for v in got.values()):
        return None
    if P.Copper.VIA_PROTECTION == "off":
        for key in PROTECTION:
            if any(got[key].values()):
                items.skipped[f"{WORDS[key]} vias{PROTECTION_OFF}"] += 1
        return None
    outer = {"F": i == 0, "B": j == len(ctx.layers) - 1}
    p = Protection(filled=any(got["filling"].values()), capped=any(got["capping"].values()), opened=dict(opened))
    for key, store in (("plugging", p.plugged), ("covering", p.covered)):
        for side in ("F", "B"):
            if got[key][side] and not outer[side]:
                items.skipped[f"{WORDS[key]} vias at an end inside the board (no effect)"] += 1
            elif got[key][side]:
                store[side] = True
                items.found[f"{WORDS[key]} vias, {'front' if side == 'F' else 'back'}"] += 1
    if p.capped and not (outer["F"] or outer["B"]):
        p.capped = False
        items.skipped["capped vias with both ends inside the board (no effect)"] += 1
    for key, on in (("filling", p.filled), ("capping", p.capped)):
        if on:
            items.found[f"{WORDS[key]} vias"] += 1
    for side in ("F", "B"):
        if opened[side] and outer[side] and (p.plugged[side] or p.covered[side] or p.capped):
            items.skipped["via protection at an end a backdrill or post machining opens (left open)"] += 1
    return p


WORDS = {"covering": "covered", "plugging": "plugged", "capping": "capped", "filling": "filled"}


def machine(ctx, node, of, center, what):
    """Everything KiCad 10 adds to a pad's or via's hole: its drills and post machining, and a via's
    protection on its Hole.  `of`: the hole's index in Items.holes, or -1 for a pad with none."""
    opened = drills_of(ctx, node, center, what, of)
    machined = post_machining_of(ctx, node, center, what, of)
    opened = {s: opened[s] or machined[s] for s in opened}
    if what == "vias" and of >= 0:
        hole = ctx.items.holes[of]
        hole.protect = protection_of(ctx, node, hole.i, hole.j, opened)
