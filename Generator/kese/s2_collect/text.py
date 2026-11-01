"""Text on copper, mask and silkscreen layers (gr_text, fp_text, footprint properties), drawn with
the stroke font."""
import datetime
import re

import shapely
from shapely import affinity
from shapely.geometry import Polygon, box

from kese.core import font
from kese.core.shapes2d import polys_only
from kese.core.sexp import atoms, child, children, flag, layer_of, num, numbers, yes
from parameters import P

TEXT = {"gr_text", "fp_text", "gr_text_box", "fp_text_box", "dimension", "gr_dimension"}


TEXT_VAR = re.compile(r"\$\{([^{}]+)\}")


def board_text_vars(items):
    """{variable: value} for the ${...} a board text can use, as KiCad resolves them without its
    project file (board.cpp BOARD::ResolveTextVar, title_block.cpp TITLE_BLOCK::TextVarResolver):
    the title block, the file name and path, and the board's own (property "name" "value")."""
    if getattr(items, "_text_vars", None) is None:
        tree, raw = items.raw.tree, items.raw
        out = {"FILENAME": raw.path.name, "FILEPATH": str(raw.path.resolve()),
               "CURRENT_DATE": datetime.date.today().isoformat()}
        tb = child(tree, "title_block") or []
        for key, var in (("title", "TITLE"), ("date", "ISSUE_DATE"), ("rev", "REVISION"), ("company", "COMPANY")):
            c = child(tb, key)
            out[var] = str(c[1]) if c is not None and len(c) > 1 else ""
        for c in children(tb, "comment"):
            if len(c) > 2:
                out[f"COMMENT{c[1]}"] = str(c[2])
        for n in range(1, 10):
            out.setdefault(f"COMMENT{n}", "")
        for prop in children(tree, "property"):
            if len(prop) > 2:
                out.setdefault(str(prop[1]), str(prop[2]))
        layer_names = {}
        for l in child(tree, "layers")[1:]:
            if isinstance(l, list) and len(l) > 1:
                layer_names[str(l[1])] = str(l[3]) if len(l) > 3 and not isinstance(l[3], list) else str(l[1])
        fps = {}
        for fp in children(tree, "footprint") + children(tree, "module"):
            fields = footprint_fields(fp)
            for key in (child(fp, "uuid"), child(fp, "tstamp")):
                if key is not None and len(key) > 1:
                    fps[str(key[1])] = fields
            if "REFERENCE" in fields:
                fps.setdefault(fields["REFERENCE"].upper(), fields)
        items._text_vars, items._layer_names, items._footprint_fields = out, layer_names, fps
    return items._text_vars


def footprint_fields(fp):
    """{FIELD: value} of a footprint, for its own texts' ${...} and other texts' ${REF:FIELD}
    (FOOTPRINT::ResolveTextVar): its properties and reference / value, and its library and name."""
    out = {}
    for prop in children(fp, "property"):
        if len(prop) > 2 and not isinstance(prop[2], list):
            out[str(prop[1]).upper()] = str(prop[2])
    for t in children(fp, "fp_text"):
        if len(t) > 2 and t[1] in ("reference", "value"):
            out[t[1].upper()] = str(t[2])
    lib, _, name = str(fp[1]).rpartition(":") if len(fp) > 1 and not isinstance(fp[1], list) else ("", "", "")
    out.setdefault("FOOTPRINT_LIBRARY", lib)
    out.setdefault("FOOTPRINT_NAME", name)
    return out


def shown_text(items, text, layer, fp_vars=None):
    """A text with its ${...} variables resolved as PCB_TEXT::GetShownText does: LAYER (the layer's
    name as the board shows it), then the footprint's fields, then the board's variables, and
    ${REF:FIELD} from another footprint (by its uuid, as KiCad saves it, or its reference).  One that
    needs the project file stays as written, as KiCad leaves an unknown variable."""
    if "${" not in text:
        return text
    board = board_text_vars(items)

    def resolve(m):
        token = m.group(1)
        if token == "LAYER":
            return items._layer_names.get(layer, layer)
        if fp_vars and token.upper() in fp_vars:
            return fp_vars[token.upper()]
        if ":" in token:                            # ${<footprint uuid or reference>:<field>}
            ref, _, field = token.partition(":")
            fields = items._footprint_fields.get(ref) or items._footprint_fields.get(ref.upper())
            shown = fields.get("REFERENCE", ref) if fields else ref
            return fields[field.upper()] if fields and field.upper() in fields else f"<Unresolved: {shown}:{field}>"
        return board.get(token, m.group(0))
    return TEXT_VAR.sub(resolve, text)


def kept_upright(node):
    """Whether KiCad keeps a footprint text upright: unless the file says (unlocked yes), or before
    KiCad 8 a bare unlocked in its (at ...)."""
    if "unlocked" in [str(a) for a in atoms(child(node, "at"))]:
        return False
    unlocked = child(node, "unlocked")
    return unlocked is None or (len(unlocked) > 1 and not yes(unlocked[1]))


def upright(angle):
    """The angle KiCad draws a footprint text at when it keeps it upright, in ]-90, 90] degrees
    (PCB_TEXT::GetDrawRotation): turned half a turn when it would read upside down."""
    while angle > 90.0:
        angle -= 180.0
    while angle <= -90.0:
        angle += 180.0
    return angle


def add_text(ctx, node, T=lambda p: p, subst=None, in_footprint=False):
    S = P.Silkscreen
    items = ctx.items
    layer = layer_of(node)
    if not (layer in ctx.layers or layer in ("F.SilkS", "B.SilkS", "F.Mask", "B.Mask")):
        return
    h_ = child(node, "hide")
    effects = child(node, "effects") or []
    hidden = (yes(h_[1]) if h_ is not None and len(h_) > 1 else h_ is not None) \
        or "hide" in atoms(node) or "hide" in atoms(effects) \
        or (child(effects, "hide") is not None and yes((child(effects, "hide") + ["yes"])[1]))
    if hidden and not S.DRAW_HIDDEN_TEXT:
        return
    kind = node[0]
    if kind in ("gr_text_box", "fp_text_box", "dimension", "gr_dimension") or child(node, "at") is None:
        items.skipped[f"{kind} on {layer} (not modelled)"] += 1
        return
    text = str(node[2] if kind in ("fp_text", "property") else node[1])     # unescaped when read (core/sexp.py)
    text = shown_text(items, text, layer, subst)
    vals = numbers(child(node, "at"))
    pos = T((vals[0], vals[1]))
    angle = vals[2] if len(vals) > 2 else 0.0          # text angles are stored absolute
    if in_footprint and kept_upright(node):
        angle = upright(angle)
    fnt = child(effects, "font") or []
    size = child(fnt, "size")
    h, w = (float(size[1]), float(size[2])) if size else (1.0, 1.0)
    bold = flag(fnt, "bold")
    italic = flag(fnt, "italic")
    thick = num(fnt, "thickness", (S.BOLD_THICKNESS_RATIO if bold else S.NORMAL_THICKNESS_RATIO) * h)
    just = child(effects, "justify")
    just = [str(j) for j in atoms(just)] if just else []
    geom = None
    if child(fnt, "face") is not None:
        geom = cached_glyphs(node, text, angle)
        if geom is not None:
            items.found[f"text in a TrueType face, from the file's render cache, on {layer}"] += 1
        elif not S.DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT:
            items.skipped[f"TrueType text on {layer} (DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT is False)"] += 1
            return
        else:
            items.found[f"text in a TrueType face, drawn with the stroke font, on {layer}"] += 1
    if geom is None:
        geom = font.render(text, pos, angle, h, w, thick, just, "mirror" in just, italic)
    if "knockout" in [str(a) for a in atoms(child(node, "layer"))] and not geom.is_empty:
        geom = knocked_out(geom, pos, angle, h, thick)
        items.found[f"knockout text on {layer}"] += 1
    ctx.add(layer, geom, "text")


def cached_glyphs(node, text, angle):
    """The filled glyphs KiCad 7+ stores with a TrueType text, (render_cache "text" angle (polygon
    (pts outline) (pts hole) ...) ...), in board coordinates, footprint texts too: the text exactly
    as KiCad draws it in its face (PCB_TEXT::TransformTextToPolySet fills the glyphs, no pen), so
    the font need not be installed.  None when there is none or it is stale - made for another
    text or angle - as KiCad then draws it anew (EDA_TEXT::GetRenderCache)."""
    rc = child(node, "render_cache")
    if rc is None or len(rc) < 3 or isinstance(rc[1], list) or str(rc[1]) != text:
        return None
    try:
        turned = (float(rc[2]) - angle + 180.0) % 360.0 - 180.0
    except (TypeError, ValueError):
        return None
    if abs(turned) > 1e-6:
        return None
    glyphs = []
    for poly in children(rc, "polygon"):
        rings = [[(float(p[1]), float(p[2])) for p in pts[1:] if isinstance(p, list) and p[0] == "xy"]
                 for pts in children(poly, "pts")]
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            glyphs.append(polys_only(shapely.make_valid(Polygon(rings[0], rings[1:]))))
    return shapely.union_all(glyphs) if glyphs else None


def knocked_out(geom, pos, angle, h, thick):
    """Knockout text (KiCad 7+, (layer "F.Cu" knockout)): the text's box, square to the text and grown
    by max(pen / 2, height / 9), with the letters cut out of it (PCB_TEXT::TransformTextToPolySet,
    buildBoundingHull and GetKnockoutTextMargin in KiCad's gr_text.h)."""
    margin = max(thick / 2, h / 9)
    upright = affinity.rotate(geom, angle, origin=pos)          # font.render turned it by -angle
    x0, y0, x1, y1 = upright.bounds
    hull = affinity.rotate(box(x0 - margin, y0 - margin, x1 + margin, y1 + margin), -angle, origin=pos)
    return hull.difference(geom)
