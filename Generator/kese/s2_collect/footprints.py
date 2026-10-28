"""Footprints: their drawings, pads, zones and text, placed by the footprint's position and angle."""
from kese.core import shapes2d as sh
from kese.core.sexp import child, children, layer_of, num, numbers
from kese.s2_collect.drawings import GRAPHICS, add_drawing
from kese.s2_collect.left_out import UNKNOWN
from kese.s2_collect.pads import add_pad
from kese.s2_collect.text import TEXT, add_text
from kese.s2_collect.zones import add_zone


def add_footprint(ctx, fp):
    items = ctx.items
    T = sh.make_transform(numbers(child(fp, "at")))
    fp_margin = num(fp, "solder_mask_margin")
    subst = {}
    for prop in children(fp, "property"):
        if len(prop) > 2 and not isinstance(prop[2], list):
            subst[str(prop[1]).upper()] = str(prop[2])
    for t in children(fp, "fp_text"):
        if len(t) > 2 and t[1] in ("reference", "value"):
            subst[t[1].upper()] = str(t[2])
    items.found["footprints"] += 1
    if children(fp, "model"):
        items.skipped["3D component models (bare board only)"] += len(children(fp, "model"))
    for node in fp[1:]:
        if not isinstance(node, list) or not node:
            continue
        if node[0] in GRAPHICS:
            add_drawing(ctx, node, T, in_footprint=True)
        elif node[0] == "pad":
            add_pad(ctx, node, T, fp_margin)
        elif node[0] == "zone":
            add_zone(ctx, node)
        elif node[0] in TEXT or (node[0] == "property" and layer_of(node)):
            add_text(ctx, node, T, subst, in_footprint=True)
        elif node[0] == "barcode":                   # KiCad 10: drawn from its text, no shape in the file
            items.skipped["barcode items"] += 1
        elif str(node[0]).startswith("fp_"):          # a drawing of a kind KESE does not know (fp_ellipse ...)
            items.skipped[f"{node[0]} {UNKNOWN}"] += 1
