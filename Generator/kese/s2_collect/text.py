"""Text on copper, mask and silkscreen layers (gr_text, fp_text, footprint properties), drawn with
the stroke font."""
import shapely
from shapely import affinity
from shapely.geometry import Polygon, box

from kese.core import font
from kese.core.shapes2d import EMPTY, polys_only
from kese.core.sexp import atoms, child, layer_of, numbers
from kese.s1_read.parse_kicad_version import (flag, is_hidden, is_knockout, kept_upright, overbar_markup,
                                              render_cache_rings, text_pen, text_size, text_value)
from kese.s2_collect.text_vars import saved_words, shown_text
from parameters import P

TEXT = {"gr_text", "fp_text", "gr_text_box", "fp_text_box", "dimension", "gr_dimension"}
KNOCKOUT_MARGIN_RATIO = 1 / 9         # of the text height, KiCad's GetKnockoutTextMargin (gr_text.h)
# KiCad's stroke font named as a face: FONT::GetFont gives the stroke font for an empty name or one that
# starts with this (common/font/font.cpp), and boards saved by KiCad 10 can say (face "KiCad Font")
KICAD_FONT_NAME = "KiCad Font"
STROKED = "text in a TrueType face, drawn with the stroke font"
FROM_CACHE = "text in a TrueType face, from the file's render cache"


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
    words = str(node[2]) if kind == "property" else text_value(node)       # unescaped when read (core/sexp.py)
    words = overbar_markup(words, items.raw.dialect)
    text = shown_text(items, words, layer, subst)
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
    if truetype_face(fnt):
        geom, how = cached_glyphs(node, text, angle), FROM_CACHE
        saved = saved_words(items, words, layer, subst) if geom is None else None
        if saved is not None:                       # KiCad's words when it saved, where KESE cannot know them
            geom, how = cached_glyphs(node, saved, angle), f"{FROM_CACHE} as KiCad last showed its variables"
        if geom is not None:
            items.found[f"{how}, on {layer}"] += 1
        elif not S.DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT:
            items.skipped[f"TrueType text on {layer} (DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT is False)"] += 1
            return
        else:
            items.found[f"{STROKED}, on {layer}"] += 1
    if geom is None:
        geom = font.render(text, pos, angle, h, w, thick, just, "mirror" in just, italic)
    if is_knockout(node) and not geom.is_empty:
        geom = knocked_out(geom, pos, angle, h, thick)
        items.found[f"knockout text on {layer}"] += 1
    ctx.add(layer, geom, "text")


def truetype_face(fnt):
    """The TrueType face a text's (font ...) names, or None for KiCad's stroke font."""
    face = child(fnt, "face")
    name = str(face[1]) if face is not None and len(face) > 1 else ""
    return None if not name or name.startswith(KICAD_FONT_NAME) else name


def warn_stroked(items, log):
    """A warning for TrueType text drawn with the stroke font, whose letters then differ from KiCad's."""
    n = sum(count for what, count in items.found.items() if what.startswith(STROKED))
    if n:
        log(f"warning: {n} text(s) in a TrueType face drawn with KiCad's stroke font, in other letter shapes: the "
            "file has no render cache for them, or one made for other words or another angle (open the board in "
            "KiCad and save it)")


def cached_glyphs(node, text, angle):
    """The filled glyphs the file stores with a TrueType text, in board coordinates: the text exactly
    as KiCad draws it in its face (PCB_TEXT::TransformTextToPolySet fills the glyphs, no pen), so the
    font need not be installed.  text is the words, or a regular expression the cache's words must match
    (saved_words).  None when there is none or it is stale; nothing when the cache holds no
    letters, as for an empty text or a character the face lacks, which KiCad draws as nothing."""
    polys = render_cache_rings(node, text, angle)
    if polys is None:
        return None
    glyphs = [polys_only(shapely.make_valid(Polygon(r[0], r[1:]))) for r in polys if r]
    return shapely.union_all(glyphs) if glyphs else EMPTY


def knocked_out(geom, pos, angle, h, thick):
    """Knockout text: the text's box, square to the text and grown
    by max(pen / 2, height / 9), with the letters cut out of it (PCB_TEXT::TransformTextToPolySet,
    buildBoundingHull and GetKnockoutTextMargin in KiCad's gr_text.h)."""
    margin = max(thick / 2, h * KNOCKOUT_MARGIN_RATIO)
    upright = affinity.rotate(geom, angle, origin=pos)          # font.render turned it by -angle
    x0, y0, x1, y1 = upright.bounds
    hull = affinity.rotate(box(x0 - margin, y0 - margin, x1 + margin, y1 + margin), -angle, origin=pos)
    return hull.difference(geom)
