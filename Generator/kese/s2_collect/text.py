"""Text on copper, mask and silkscreen layers (gr_text, fp_text, footprint properties), drawn with
the stroke font."""
import datetime
import re

import shapely
from shapely import affinity
from shapely.geometry import Polygon, box

from kese.core import font
from kese.core.shapes2d import polys_only
from kese.core.sexp import atoms, child, children, layer_of, numbers
from kese.s1_read.parse_kicad_version import (flag, footprint_text_fields, is_footprint, is_hidden, is_knockout,
                                              kept_upright, overbar_markup, render_cache_rings, text_pen, text_size)
from parameters import P

TEXT = {"gr_text", "fp_text", "gr_text_box", "fp_text_box", "dimension", "gr_dimension"}


TEXT_VAR = re.compile(r"\$\{([^{}]+)\}")
KNOCKOUT_MARGIN_RATIO = 1 / 9         # of the text height, KiCad's GetKnockoutTextMargin (gr_text.h)


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
        for fp in (n for n in tree[1:] if isinstance(n, list) and n and is_footprint(n)):
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
    out = footprint_text_fields(fp)
    lib, _, name = str(fp[1]).rpartition(":") if len(fp) > 1 and not isinstance(fp[1], list) else ("", "", "")
    out.setdefault("FOOTPRINT_LIBRARY", lib)
    out.setdefault("FOOTPRINT_NAME", name)
    return out


def shown_text(items, text, layer, fp_vars=None):
    """A text with its ${...} variables resolved as PCB_TEXT::GetShownText does (LAYER, the footprint's
    fields, the board's variables, ${REF:FIELD}); one that needs the project file stays as written."""
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
    effects = child(node, "effects") or []
    if is_hidden(node) and not S.DRAW_HIDDEN_TEXT:
        return
    kind = node[0]
    if kind in ("gr_text_box", "fp_text_box", "dimension", "gr_dimension") or child(node, "at") is None:
        items.skipped[f"{kind} on {layer} (not modelled)"] += 1
        return
    text = str(node[2] if kind in ("fp_text", "property") else node[1])     # unescaped when read (core/sexp.py)
    text = shown_text(items, overbar_markup(text, items.raw.dialect), layer, subst)
    vals = numbers(child(node, "at"))
    pos = T((vals[0], vals[1]))
    angle = vals[2] if len(vals) > 2 else 0.0          # text angles are stored absolute
    if in_footprint and kept_upright(node):
        angle = upright(angle)
    fnt = child(effects, "font") or []
    h, w = text_size(fnt)
    bold = flag(fnt, "bold")
    italic = flag(fnt, "italic")
    # KiCad's pen (EDA_TEXT::GetEffectiveTextPenWidth): the file's, else a fifth (bold) or an eighth of
    # the text width, and at most a quarter of its smaller size (ClampTextPenSize)
    thick = text_pen(fnt, items.raw.dialect)
    thick = (S.BOLD_THICKNESS_RATIO if bold else S.NORMAL_THICKNESS_RATIO) * abs(w) if thick is None else thick
    thick = min(thick, S.MAX_PEN_RATIO * min(abs(h), abs(w)))
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
    if is_knockout(node) and not geom.is_empty:
        geom = knocked_out(geom, pos, angle, h, thick)
        items.found[f"knockout text on {layer}"] += 1
    ctx.add(layer, geom, "text")


def cached_glyphs(node, text, angle):
    """The filled glyphs the file stores with a TrueType text, in board coordinates: the text exactly
    as KiCad draws it in its face (PCB_TEXT::TransformTextToPolySet fills the glyphs, no pen), so the
    font need not be installed.  None when there is none or it is stale."""
    polys = render_cache_rings(node, text, angle)
    glyphs = [polys_only(shapely.make_valid(Polygon(r[0], r[1:]))) for r in polys or [] if r]
    return shapely.union_all(glyphs) if glyphs else None


def knocked_out(geom, pos, angle, h, thick):
    """Knockout text: the text's box, square to the text and grown
    by max(pen / 2, height / 9), with the letters cut out of it (PCB_TEXT::TransformTextToPolySet,
    buildBoundingHull and GetKnockoutTextMargin in KiCad's gr_text.h)."""
    margin = max(thick / 2, h * KNOCKOUT_MARGIN_RATIO)
    upright = affinity.rotate(geom, angle, origin=pos)          # font.render turned it by -angle
    x0, y0, x1, y1 = upright.bounds
    hull = affinity.rotate(box(x0 - margin, y0 - margin, x1 + margin, y1 + margin), -angle, origin=pos)
    return hull.difference(geom)
