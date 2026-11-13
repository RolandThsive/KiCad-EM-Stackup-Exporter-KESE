"""The plies of the laminate: what each gap between two copper layers is made of.  KiCad's Board
Setup gives a dielectric one or more sub-layers, each with its own thickness and material, and the
file writes them in one (layer "dielectric N" ...), the bare word addsublayer between them: each
sub-layer is a ply.  Board.PLIES_BY_HAND gives a gap other plies than the file's.  With the plies
fused (Stackup.FUSION_BUILD) a gap is one solid, with its first ply's values or its plies' in series
(Board.FUSED_PROPERTIES); with the plies separate each ply is a solid, but those too thin to build
(Board.PLY_MIN_THICKNESS_MM) and, on request, equal neighbours (Board.JOIN_EQUAL_PLIES) are joined."""
from dataclasses import replace

from kese.core.dielectric import ds_fits
from kese.core.sexp import child, num
from kese.model.stackup import Dielectric, Ply
from parameters import P

MODELS = ("constant", "djordjevic_sarkar", "table")
HAND_KEYS = {"type": str, "thickness_mm": float, "material": str, "epsilon_r": float, "loss_tangent": float}
HAND_MORE = {"frequency_hz": float, "model": str}             # optional: left out, the defaults of Board.py


def sublayers(layer):
    """The children of a (layer ...) of the stack-up, sub-layer by sub-layer."""
    out = [[]]
    for c in layer[2:]:
        if isinstance(c, list):
            out[-1].append(c)
        elif c == "addsublayer":
            out.append([])
    return out


def file_plies(layer, name, kind, log):
    """[Ply] of one dielectric of the board file, top to bottom: one for each sub-layer, with its own
    values (the parameters' where it gives none, or a USE_STACKUP_* switch is False)."""
    B = P.Board
    subs, plies = sublayers(layer), []
    for n, sub in enumerate(subs, start=1):
        node = [name, *sub]
        own = f"{name} ply {n}" if len(subs) > 1 else name
        t = num(node, "thickness")
        if t is not None and t < 0:
            log(f"warning: stackup layer {own}: thickness {t} mm is less than 0: read as not given")
            t = None
        f = num(node, "spec_frequency") if B.USE_STACKUP_SPEC_FREQUENCY else None
        model = (child(node, "dielectric_model") or [None, None])[1] if B.USE_STACKUP_DIELECTRIC_MODEL else None
        plies.append(Ply(
            name=own, kind=kind, material=(child(node, "material") or [None, B.DEFAULT_DIELECTRIC_MATERIAL])[1],
            thickness=t or 0.0,
            epsilon_r=num(node, "epsilon_r", B.DEFAULT_EPSILON_R) if B.USE_STACKUP_EPSILON_R else B.DEFAULT_EPSILON_R,
            loss_tangent=num(node, "loss_tangent", B.DEFAULT_LOSS_TANGENT) if B.USE_STACKUP_LOSS_TANGENT else B.DEFAULT_LOSS_TANGENT,
            frequency_hz=f if f and f > 0 else B.DEFAULT_SPEC_FREQUENCY_HZ,
            model=model if model in MODELS else B.DIELECTRIC_MODEL, of=name))
    return plies


def hand_ply(given, where, name, of):
    """One ply of Board.PLIES_BY_HAND, checked: a Ply, or ValueError naming what is wrong with it."""
    B = P.Board
    if not isinstance(given, dict):
        raise ValueError(f"{where} must be a ply, as {{\"type\": \"prepreg\", \"thickness_mm\": 0.1, ...}}, not {given!r}")
    missing, unknown = [k for k in HAND_KEYS if k not in given], [k for k in given if k not in {**HAND_KEYS, **HAND_MORE}]
    if missing or unknown:
        raise ValueError(f"{where} " + " and ".join(w for w in (
            f"has no {', '.join(map(repr, missing))}" if missing else "",
            f"has {', '.join(map(repr, unknown))}, which a ply does not take" if unknown else "") if w)
            + f": a ply takes {', '.join(HAND_KEYS)}, and may take {', '.join(HAND_MORE)}")
    for key, kind in {**HAND_KEYS, **HAND_MORE}.items():
        value = given.get(key)
        if key in given and (type(value) not in (int, float) if kind is float else not isinstance(value, str)):
            raise ValueError(f"{where}: {key!r} must be {'a number' if kind is float else 'text, in quotes'}, not {value!r}")
    model, f = given.get("model", B.DIELECTRIC_MODEL), given.get("frequency_hz", B.DEFAULT_SPEC_FREQUENCY_HZ)
    for wrong, what in ((given["type"] not in ("core", "prepreg"), "'type' must be 'core' or 'prepreg'"),
                        (not given["thickness_mm"] > 0, "'thickness_mm' must be more than 0"),
                        (not given["epsilon_r"] >= 1, "'epsilon_r' must be 1 or more"),
                        (not given["loss_tangent"] >= 0, "'loss_tangent' must be 0 or more"),
                        (not f > 0, "'frequency_hz' must be more than 0"),
                        (model not in MODELS, f"'model' must be one of {', '.join(map(repr, MODELS))}")):
        if wrong:
            raise ValueError(f"{where}: {what}, not as in {given!r}")
    return Ply(name=name, kind=given["type"], material=given["material"], thickness=float(given["thickness_mm"]),
               epsilon_r=given["epsilon_r"], loss_tangent=given["loss_tangent"], frequency_hz=f, model=model, of=of)


def by_hand(board, copper_layers, gaps):
    """Give the gaps Board.PLIES_BY_HAND lists for this board (its file's name without .kicad_pcb)
    those plies in place of the file's: `gaps`, [[Dielectric] for each gap], is changed.  -> the gaps
    given by hand, as indices.  ValueError for a gap that is not one of the board's, or a wrong ply."""
    listed = P.Board.PLIES_BY_HAND.get(board) or {}
    pairs, done = list(zip(copper_layers, copper_layers[1:])), []
    if not isinstance(listed, dict):
        raise ValueError(f"Board.PLIES_BY_HAND[{board!r}] must be {{(copper above, copper below): [plies]}}, not {listed!r}")
    for pair, plies in listed.items():
        where = f"Board.PLIES_BY_HAND[{board!r}][{pair!r}]"
        if pair not in pairs:
            raise ValueError(f"{where}: {pair!r} is not two neighbouring copper layers of this board, the upper one "
                             f"first; its gaps are {', '.join(map(str, pairs))}")
        if not isinstance(plies, (list, tuple)) or not plies:
            raise ValueError(f"{where} must be a list of plies, top to bottom, not {plies!r}")
        k = pairs.index(pair)
        name = gaps[k][0].name if gaps[k] else f"dielectric {k + 1}"
        made = [hand_ply(ply, f"{where}[{n}]", f"{name} ply {n + 1}" if len(plies) > 1 else name, name)
                for n, ply in enumerate(plies)]
        gaps[k] = [of_plies(name, made)]
        done.append(k)
    return done


def of_plies(name, plies):
    """A dielectric of the board file (or a gap given by hand) from its plies: the first one's values,
    the thickness of them all."""
    first = plies[0]
    return Dielectric(name, first.kind, first.material, sum(p.thickness for p in plies), first.epsilon_r,
                      first.loss_tangent, frequency_hz=first.frequency_hz, model=first.model, plies=plies)


def fused(dielectrics):
    """The one Dielectric of a gap, from the dielectrics the board file puts in it: its plies fused
    (a gap of several is one solid of the summed thickness).  It has its first ply's material, er and
    tan d, or with Board.FUSED_PROPERTIES = "series" its plies' in series, as a field straight across
    the gap sees them: h / er = sum(h_p / er_p), and tan d weighted the same way."""
    first, plies = dielectrics[0], [p for d in dielectrics for p in d.plies]
    d = first if len(dielectrics) == 1 else replace(first, name=" + ".join(x.name for x in dielectrics),
                                                    thickness=sum(x.thickness for x in dielectrics), plies=plies)
    for n, p in enumerate(plies, start=1):
        p.number, p.count = n, len(plies)
    h = sum(p.thickness for p in plies)
    if P.Board.FUSED_PROPERTIES == "series" and len(plies) > 1 and h > 0:
        d.epsilon_r = round(h / sum(p.thickness / p.epsilon_r for p in plies), 6)
        d.loss_tangent = round(d.epsilon_r / h * sum(p.thickness * p.loss_tangent / p.epsilon_r for p in plies), 6)
        d.material = " + ".join(dict.fromkeys(str(p.material) for p in plies))
    return d


def solids(d, log):
    """The plies of gap d as they are built with the plies separate, top to bottom: the file's, but a
    ply thinner than Board.PLY_MIN_THICKNESS_MM is joined to its thicker neighbour (with a warning),
    and with Board.JOIN_EQUAL_PLIES neighbours of the same material and values are one."""
    B = P.Board
    out = [(replace(p), [p]) for p in d.plies]                 # (the solid, the file's plies it holds)
    while len(out) > 1:
        k = min(range(len(out)), key=lambda i: out[i][0].thickness)
        thin = out[k][0]
        if thin.thickness >= B.PLY_MIN_THICKNESS_MM:
            break
        into = max((i for i in (k - 1, k + 1) if 0 <= i < len(out)), key=lambda i: out[i][0].thickness)
        log(f"warning: {thin.name} is {thin.thickness:.6g} mm thick, less than Board.PLY_MIN_THICKNESS_MM "
            f"({B.PLY_MIN_THICKNESS_MM} mm): joined to {out[into][0].name}")
        out[into][0].thickness += thin.thickness
        out[into][1][len(out[into][1]) * (into < k):0] = out[k][1]        # the plies it holds, still top to bottom
        del out[k]
    if B.JOIN_EQUAL_PLIES:
        same = lambda a, b: (a.kind, a.material, a.epsilon_r, a.loss_tangent, a.frequency_hz, a.model) == \
                            (b.kind, b.material, b.epsilon_r, b.loss_tangent, b.frequency_hz, b.model)
        joined = out[:1]
        for solid, held in out[1:]:
            if same(joined[-1][0], solid):
                joined[-1][0].thickness += solid.thickness
                joined[-1][1].extend(held)
            else:
                joined.append((solid, held))
        out = joined
    for solid, held in out:
        solid.name, solid.holds = joined_name(held, d.plies), [p.name for p in held]
    return [solid for solid, _ in out]


def joined_name(held, plies):
    """The name of a solid that holds the file's plies `held` of a gap's `plies`: the ply's own, its
    dielectric's where it holds all of that dielectric's plies, or first-last: "dielectric 1 ply 2-3"."""
    if len(held) == 1:
        return held[0].name
    names = list(dict.fromkeys(p.of for p in held))
    whole = all(p in held for p in plies if p.of in names)
    if whole or len(names) > 1:
        return " + ".join(names if whole else [p.name for p in held])
    return f"{held[0].name}-{held[-1].name.rsplit(' ', 1)[-1]}"


def check_models(dielectrics, log):
    """A ply whose Djordjevic-Sarkar model cannot be fitted (its spec frequency is not between the
    corner frequencies) is written with constant values, with a warning, as KiCad falls back."""
    B = P.Board
    for d in dielectrics:
        for ply in d.plies:
            if ply.model == "djordjevic_sarkar" and not ds_fits(ply.frequency_hz, B.DS_LOW_FREQUENCY_HZ, B.DS_HIGH_FREQUENCY_HZ):
                log(f"warning: {ply.name}: the Djordjevic-Sarkar model needs its spec frequency ({ply.frequency_hz:g} Hz) "
                    f"between Board.DS_LOW_FREQUENCY_HZ ({B.DS_LOW_FREQUENCY_HZ:g}) and Board.DS_HIGH_FREQUENCY_HZ "
                    f"({B.DS_HIGH_FREQUENCY_HZ:g}): written with constant values")
                ply.model = "constant"
        d.model = d.plies[0].model
