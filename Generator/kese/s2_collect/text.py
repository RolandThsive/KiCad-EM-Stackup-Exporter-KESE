"""Text on copper, mask and silkscreen layers (gr_text, fp_text, footprint properties), drawn with
the stroke font."""
import re

from kese.core import font
from kese.core.sexp import atoms, child, flag, layer_of, num, numbers, yes
from parameters import P

TEXT = {"gr_text", "fp_text", "gr_text_box", "fp_text_box", "dimension", "gr_dimension"}
ESCAPES = {"n": "\n", "r": "\r", "t": "\t"}


def unescape(text):
    """A quoted string of the file as KiCad reads it: \\n a new line, \\t a tab, \\" and \\\\ the
    character itself (KiCad writes \\n, \\r, \\" and \\\\, and a tab as it is)."""
    return re.sub(r"\\(.)", lambda m: ESCAPES.get(m.group(1), m.group(1)), text, flags=re.DOTALL)


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
    text = unescape(str(node[2] if kind in ("fp_text", "property") else node[1]))
    for key, val in (subst or {}).items():
        text = text.replace("${" + key + "}", val)
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
    if child(fnt, "face") is not None:
        if not S.DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT:
            items.skipped[f"TrueType text on {layer} (DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT is False)"] += 1
            return
        items.found[f"text in a TrueType face, drawn with the stroke font, on {layer}"] += 1
    geom = font.render(text, pos, angle, h, w, thick, just, "mirror" in just, italic)
    ctx.add(layer, geom, "text")
