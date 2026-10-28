"""What KESE reads past, counted under "skipped" in report.txt and summed up in a warning: items of
a kind it does not know (such as KiCad 10's ellipses), and what a pad or via says that is not
modelled.  That is a padstack, another shape on the inner layers or on the back (KiCad 9 and later),
for which the front shape is used on every layer; and KiCad 10's drilling and protection of holes:
backdrills and tertiary drills (the hole stays plated through its whole span), counterbores and
countersinks (not cut), and vias that are covered, plugged, capped or filled (the hole stays open)."""
from kese.core.sexp import child, yes

UNKNOWN = "items (unknown to KESE)"
PROTECTION = {"covering": "covered vias (the covering is not modelled)",
              "plugging": "plugged vias (the plug is not modelled)",
              "capping": "capped vias (the cap is not modelled)",
              "filling": "filled vias (the filling is not modelled)"}


def _features(what):
    plated = "(the hole is plated through its whole span)"
    return {"padstack": f"{what} with a padstack (the front shape is used on every layer)",
            "backdrill": f"backdrills of {what} {plated}", "tertiary_drill": f"tertiary drills of {what} {plated}",
            "counterbore": f"counterbores of {what} (not cut)", "countersink": f"countersinks of {what} (not cut)"}


FEATURES = {"pads": _features("pads"), "vias": _features("vias")}


def sides(node, default):
    """(key (front yes) (back no)), or (key yes) for both sides -> {"F": bool, "B": bool}; a side
    the node leaves out, or says "none" for, keeps `default`."""
    out = dict(default)
    if node is not None and len(node) > 1 and not isinstance(node[1], list):
        return out if str(node[1]) == "none" else {"F": yes(node[1]), "B": yes(node[1])}
    for side, key in (("F", "front"), ("B", "back")):
        c = child(node, key) if node is not None else None
        if c is not None and len(c) > 1 and str(c[1]) != "none":
            out[side] = yes(c[1])
    return out


def protection_defaults(setup):
    """KiCad 10's board setup: whether a via that does not say is covered, plugged, capped or filled."""
    return {key: sides(child(setup, key), {"F": False, "B": False}) for key in PROTECTION}


def count(items, node, what):
    """The padstack, drills and post machining of a pad or via (`what`: "pads" or "vias"), and the
    protection of a via, under items.skipped."""
    names = FEATURES[what]
    for key in ("padstack", "backdrill", "tertiary_drill"):
        if child(node, key) is not None:
            items.skipped[names[key]] += 1
    for key in ("front_post_machining", "back_post_machining"):
        c = child(node, key)
        if c is not None and len(c) > 1 and str(c[1]) in names:
            items.skipped[names[str(c[1])]] += 1
    if what == "vias":
        for key, name in PROTECTION.items():
            if any(sides(child(node, key), items.via_protection.get(key, {})).values()):
                items.skipped[name] += 1


def warn(items, log):
    """One warning for what the board has that is not modelled, one for the kinds KESE does not know."""
    known = {name for names in FEATURES.values() for name in names.values()} | set(PROTECTION.values())
    left = [what.split(" (")[0] for what in sorted(items.skipped) if what in known]
    if left:
        log(f"warning: not modelled, see 'skipped' in report.txt: {', '.join(left)}")
    unknown = [f"{what[:-len(UNKNOWN)].strip()} ({n})" for what, n in sorted(items.skipped.items()) if what.endswith(UNKNOWN)]
    if unknown:
        log(f"warning: left out, of a kind KESE does not know: {', '.join(unknown)}")
