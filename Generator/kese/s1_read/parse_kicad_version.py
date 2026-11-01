"""Every way a board file differs by KiCad version, and nothing else.  The other files of KESE ask
the questions below and never test a format number or a KiCad release themselves
(tests/test_layout.py, test_version_checks_stay_in_parse_kicad_version, keeps it so).

Where KiCad decides by what the file holds - (mid ...) on an arc, (filled_areas_thickness no) on a
zone, a (layers ...) pair - so does this file, before it looks at the number, so a development
build's file reads as KiCad reads it.  The numbers are the (version N) KiCad writes; their history
is in KiCad's pcb_io_kicad_sexpr.h, and the rules are those of its board parser,
pcb_io_kicad_sexpr_parser.cpp (cited by function below)."""
import math
import re
from dataclasses import dataclass

from kese.core.sexp import atoms, child, children, layer_of, num, pt, yes

# (KiCad release, first format number it writes).  A development build (x.99) writes the numbers
# between two releases and counts as the next release.
RELEASES = ((3, 3), (4, 4), (5, 20171130), (6, 20211014), (7, 20221018), (8, 20240108), (9, 20241229),
            (10, 20260206))
NO_VERSION = 20201115           # parseHeader: a file without (version) is read as this format
LEGACY_ARC_FORMATTING = 20210925       # up to here an arc is (start centre) (end first point) (angle)
LEGACY_ZERO_MARGIN = 20240201          # up to here a solder_mask_margin of 0 means "inherit"
NEW_OVERBAR = 20210606                 # from here an overbar is ~{text}; before, text between two ~
STROKED_FILL_UNTIL = 20250210          # before this a zone fill is stroked, unless the zone says not
KICAD_DEFAULT_VIA = (0.6, 0.3, 0.3, 0.1)    # via size, drill, micro via size, drill (netclass.cpp)
ROUNDRECT_RRATIO = 0.25                # a roundrect pad that gives no ratio (padstack.cpp, PADSTACK defaults)


@dataclass
class KicadDialect:
    format: int                 # the file's (version N), or NO_VERSION when it has none
    release: int                # the KiCad release that writes it (11 for a format after KiCad 10)
    stated: bool                # whether the file says its version

    def describe(self):
        late = self.release > RELEASES[-1][0]
        name = f"after KiCad {RELEASES[-1][0]}" if late else f"KiCad {self.release}"
        return f"KiCad format {self.format if self.stated else 'not stated'} ({name})"


def dialect(tree):
    """The (kicad_pcb (version N) ...) of a parsed board -> KicadDialect."""
    v = child(tree, "version")
    stated = v is not None and len(v) > 1 and str(v[1]).isdigit()
    fmt = int(v[1]) if stated else NO_VERSION
    release = next((r for r, first in RELEASES if fmt <= first), RELEASES[-1][0] + 1)
    return KicadDialect(fmt, release, stated)


def tested_range_warning(d, lo, hi):
    """A warning when the file's format is outside lo..hi (parameters/run.py), or None."""
    if not d.stated:
        return f"file has no (version ...): read as format {NO_VERSION}, as KiCad does"
    if d.format < lo or d.format > hi:
        return f"file format {d.format} is outside the tested range {lo}-{hi}; proceeding best-effort"
    return None


# ---- layers ------------------------------------------------------------------------------------
COPPER_TYPES = ("signal", "power", "mixed", "jumper")
CANONICAL_COPPER = re.compile(r"F\.Cu|B\.Cu|In\d+\.Cu")


OLD_LAYER_NAMES = {
    "Adesivo.Retro": "B.Adhes", "Adesivo.Fronte": "F.Adhes", "Pasta.Retro": "B.Paste", "Pasta.Fronte": "F.Paste",
    "Serigrafia.Retro": "B.SilkS", "Serigrafia.Fronte": "F.SilkS", "Maschera.Retro": "B.Mask",
    "Maschera.Fronte": "F.Mask", "Grafica": "Dwgs.User", "Commenti": "Cmts.User", "Eco1": "Eco1.User",
    "Eco2": "Eco2.User", "Contorno.scheda": "Edge.Cuts",
    "Kleju_Dolna": "B.Adhes", "Kleju_Gorna": "F.Adhes", "Pasty_Dolna": "B.Paste", "Pasty_Gorna": "F.Paste",
    "Opisowa_Dolna": "B.SilkS", "Opisowa_Gorna": "F.SilkS", "Maski_Dolna": "B.Mask", "Maski_Gorna": "F.Mask",
    "Rysunkowa": "Dwgs.User", "Komentarzy": "Cmts.User", "ECO1": "Eco1.User", "ECO2": "Eco2.User",
    "Krawedziowa": "Edge.Cuts",
    "Dessous.Adhes": "B.Adhes", "Dessus.Adhes": "F.Adhes", "Dessous.Pate": "B.Paste", "Dessus.Pate": "F.Paste",
    "Dessous.SilkS": "B.SilkS", "Dessus.SilkS": "F.SilkS", "Dessous.Masque": "B.Mask", "Dessus.Masque": "F.Mask",
    "Dessin.User": "Dwgs.User", "Contours.Ci": "Edge.Cuts"}


def copper_layer_names(layers_node):
    """KiCad 4 and 5 write a copper layer the user renamed under its new name only, e.g.
    (0 TOP_L1.Sig mixed), and every item on it uses that name.  KiCad reads the copper layers by
    their place in the list, not their number (parseLayers): the first is F.Cu, the last B.Cu, and
    one between is In<n>.Cu by its canonical name, else by its place (KiCad 3 numbered them the other
    way round, 15 F.Cu and 0 B.Cu).  A canonical name keeps its layer: KiCad writes the list in stack
    order, so that is what KiCad reads too, and a list written in another order still reads right.  Non-copper layers KiCad 3 wrote in Italian, Polish or French
    take their English names.  -> {name in the file: name KESE uses}, or {}."""
    cu = [l for l in layers_node[1:] if isinstance(l, list) and len(l) > 2 and str(l[2]) in COPPER_TYPES]
    renamed = {}
    for i, l in enumerate(cu):
        name = str(l[1])
        place = "F.Cu" if i == 0 else "B.Cu" if i == len(cu) - 1 else f"In{i}.Cu"
        if not CANONICAL_COPPER.fullmatch(name):
            renamed[name] = place
    for l in layers_node[1:]:          # KiCad 3's Italian, Polish and French names (createOldLayerMapping)
        if isinstance(l, list) and len(l) > 1 and str(l[1]) in OLD_LAYER_NAMES:
            renamed[str(l[1])] = OLD_LAYER_NAMES[str(l[1])]
    return renamed


def rename_layers(node, renamed):
    """Every (layer ...) and (layers ...) in the tree, and the (layers ...) block itself, with the
    names in `renamed` replaced."""
    stack = [node]
    while stack:
        n = stack.pop()
        if n and n[0] in ("layer", "layers"):
            for i in range(1, len(n)):
                if isinstance(n[i], str) and n[i] in renamed:
                    n[i] = renamed[n[i]]
                elif isinstance(n[i], list) and len(n[i]) > 1 and isinstance(n[i][1], str) and n[i][1] in renamed:
                    n[i][1] = renamed[n[i][1]]      # the board's (layers (0 TOP_L1.Sig mixed) ...) block
        stack.extend(c for c in n if isinstance(c, list))


def layer_and_mask(node):
    """A track's or drawing's layer, and the side ("F" / "B") whose solder mask leaves it bare, or None.
    KiCad 9+ writes such an item with both layers, (layers "F.Cu" "F.Mask"); as in KiCad, only F.Cu
    is bared by F.Mask and only B.Cu by B.Mask."""
    c = child(node, "layers")
    if c is None:
        return layer_of(node), None
    names = [str(l) for l in c[1:]]
    layer = next((l for l in names if l.endswith(".Cu")), names[0] if names else None)
    masked = any(l in ("F.Mask", "B.Mask") for l in names)
    return layer, (layer[0] if masked and layer in ("F.Cu", "B.Cu") else None)


# ---- flags and small syntax ---------------------------------------------------------------------
def flag(node, name):
    """KiCad <= 8: bare keyword or (name); KiCad 9+: (name yes|no)."""
    c = child(node, name)
    return name in atoms(node) or (c is not None and (len(c) < 2 or yes(c[1])))


def is_footprint(node):
    """(footprint ...), or (module ...) in KiCad 5 and older."""
    return node[0] in ("footprint", "module")


def stroke_width(node):
    """A drawing's pen: (width w) in KiCad 5 and 6, (stroke (width w) ...) from KiCad 7."""
    w = num(node, "width")
    if w is None:
        stroke = child(node, "stroke")
        w = num(stroke, "width", 0.0) if stroke else 0.0
    return w


def is_filled(node, kind, w):
    """Whether a drawing is filled: its (fill yes|solid|no) from KiCad 6, else, as KiCad reads a file
    with no fill flag (KiCad 5, and KiCad 6 pad primitives), a circle or rectangle of width 0 is,
    and so is a polygon off Edge.Cuts (parsePCB_SHAPE)."""
    fill = child(node, "fill")
    if fill and len(fill) > 1:
        return yes(fill[1])
    return (kind in ("circle", "rect") and w == 0) or (kind == "poly" and layer_of(node) != "Edge.Cuts")


def legacy_arc(node, T):
    """An arc of KiCad 5 and older, (start centre) (end first point) (angle deg), as (centre, radius,
    start angle, sweep, first point), or None for an arc with (mid ...) (parsePCB_SHAPE,
    LEGACY_ARC_FORMATTING)."""
    if child(node, "mid"):
        return None
    c, p0 = T(pt(child(node, "start"))), T(pt(child(node, "end")))
    r = math.hypot(p0[0] - c[0], p0[1] - c[1])
    return c, r, math.atan2(p0[1] - c[1], p0[0] - c[0]), math.radians(num(node, "angle", 0.0)), p0


def roundrect_ratio(pad):
    """A roundrect pad's corner radius as a fraction of its shorter side."""
    return num(pad, "roundrect_rratio", ROUNDRECT_RRATIO)


def mask_margin(node, d):
    """A pad's or footprint's own solder_mask_margin, or None when it has none.  Up to format
    LEGACY_ZERO_MARGIN a margin of 0 means none: the pad takes its footprint's, the footprint the
    board's (parseFOOTPRINT, parsePAD: "In pre-9.0 files "0" meant inherit")."""
    m = num(node, "solder_mask_margin")
    return None if m == 0 and d.format <= LEGACY_ZERO_MARGIN else m


# ---- zones -------------------------------------------------------------------------------------
def stroked_fill_pen(node, d):
    """The pen a zone's stored fill is drawn with, 0 for none.  KiCad 5 and older stored a fill shrunk by
    half the zone's min_thickness and drew its outline with a pen of min_thickness; KiCad 6 to 8 write
    (filled_areas_thickness no) on a zone they filled, and files from format STROKED_FILL_UNTIL on are
    never stroked.  As KiCad does on reading such a file, a stroked fill grows by half the min_thickness,
    round at the corners (parseZONE: isStrokedFill and InflateWithLinkedHoles)."""
    flag_ = child(node, "filled_areas_thickness")
    stroked = d.format < STROKED_FILL_UNTIL
    if flag_ and len(flag_) > 1 and str(flag_[1]) in ("no", "false"):
        stroked = False
    if not stroked or child(node, "keepout"):
        return 0.0
    return num(node, "min_thickness", 0.0)


# ---- pads and vias -----------------------------------------------------------------------------
def zone_layer_connections(node):
    """(layers where a zone keeps the ring, whether zones count when the ring is tested).  KiCad 7+
    writes (zone_layer_connections "In1.Cu" ...) on a pad or via with remove_unused_layers: the zone
    filler's verdict, the layers where a zone connects to it.  KiCad then flashes the ring there and,
    on the other layers, only where a track, arc, via or pad of its net meets it, not a zone
    (pad.cpp / pcb_track.cpp FlashLayer, ZLO_FORCE_FLASHED).  An older file has no such list and
    any copper counts."""
    z = child(node, "zone_layer_connections")
    if z is None:
        return set(), True
    return {str(l) for l in z[1:] if not isinstance(l, list)}, False


def via_tenting(node, default):
    """{"F": tented?, "B": tented?} of a via: KiCad 10 (tenting (front yes) (back no)), KiCad 9
    (tenting front back) / (tenting none), the complete list; a via that does not say keeps `default`."""
    tent = dict(default)
    vt = child(node, "tenting")
    if vt is not None:
        words = atoms(vt)
        for side, key in (("F", "front"), ("B", "back")):
            c = child(vt, key)
            if c is not None:
                tent[side] = yes(c[1])
            elif words:
                tent[side] = key in words
    return tent


def board_tenting(setup):
    """(whether vias are tented when they don't say, {"F", "B"}, where that comes from): the board
    setup's (tenting front back) or (tenting (front yes) (back yes)) from KiCad 9, else KiCad 8's and
    older plot setting viasonmask (vias open in the mask when yes), else KiCad's default, tented."""
    ten = child(setup, "tenting")
    if ten is not None:
        out = {}
        for side, key in (("F", "front"), ("B", "back")):
            c = child(ten, key)
            out[side] = yes(c[1]) if c is not None and len(c) > 1 else key in atoms(ten)
        return out, "board setup (tenting)"
    pp = child(setup, "pcbplotparams")
    vom = child(pp, "viasonmask") if pp else None
    open_ = bool(vom) and yes(vom[1])
    return {"F": not open_, "B": not open_}, "plot setting viasonmask" if vom else "KiCad default (vias tented)"


def net_class_vias(tree, unescape):
    """What a via that gives no size or drill takes (KiCad 4/5 leave out what is at its net class's
    value): (the Default class's, {net: its class's}), each (size, drill, micro size, micro drill).
    A class takes what it leaves out from the board setup's via_size / via_drill, the setup from
    KiCad's defaults (PCB_VIA::GetDrillValue takes the net class's when the via has none).
    `unescape` reads the class's net names."""
    setup = child(tree, "setup") or []
    d = KICAD_DEFAULT_VIA
    board = (num(setup, "via_size", d[0]), num(setup, "via_drill", d[1]),
             num(setup, "uvia_size", d[2]), num(setup, "uvia_drill", d[3]))
    classes, default = {}, board
    for nc in children(tree, "net_class"):
        vals = (num(nc, "via_dia", board[0]), num(nc, "via_drill", board[1]),
                num(nc, "uvia_dia", board[2]), num(nc, "uvia_drill", board[3]))
        for a in children(nc, "add_net"):
            classes[unescape(str(a[1]))] = vals
        if len(nc) > 1 and str(nc[1]) == "Default":     # a net in no class is in Default
            default = vals
    return default, classes


def via_size(node):
    """A via's (size) and (drill), None for what it leaves to its net class (KiCad 4/5)."""
    return num(node, "size"), num(node, "drill")


def padstack_entries(node, copper):
    """KiCad 9+ (padstack (mode front_inner_back | custom) (layer "Inner" | "B.Cu" | "In1.Cu" ...)):
    [(copper layers, entry)] for the layers whose shape is not the front one; "Inner" is every
    inner layer."""
    ps = child(node, "padstack")
    out = []
    for entry in children(ps, "layer") if ps is not None else []:
        name = str(entry[1])
        out.append(([l for l in (copper[1:-1] if name == "Inner" else [name]) if l in copper and l != "F.Cu"], entry))
    return out


# ---- nets --------------------------------------------------------------------------------------
# KiCad's {token} escapes in net names (string_utils.cpp, UnescapeString)
NET_ESCAPES = {"dblquote": '"', "quote": "'", "lt": "<", "gt": ">", "backslash": "\\", "slash": "/", "bar": "|",
               "comma": ",", "colon": ":", "space": " ", "dollar": "$", "tab": "\t", "return": "\n", "brace": "{"}


def kicad_unescape(s):
    """A net name as KiCad shows it: KiCad 6+ stores characters a net name cannot hold as {slash},
    {colon}, ... (a label "A/B" on the root sheet is the net "/A{slash}B", shown "/A/B").  Markup -
    ~{overbar}, ^{super}, _{sub}, ${var} - and unknown tokens stay as written, as in KiCad."""
    if len(s) <= 2 or "{" not in s:
        return s
    out, i, n, prev = [], 0, len(s), ""
    while i < n:
        ch = s[i]
        if ch != "{":
            out.append(ch)
            prev, i = ch, i + 1
            continue
        depth, j = 1, i + 1
        while j < n:
            depth += {"{": 1, "}": -1}.get(s[j], 0)
            if depth <= 0:
                break
            j += 1
        token = s[i + 1:j]
        if j >= n:                                   # not closed
            out.append("{" + kicad_unescape(token))
        elif prev in "$~^_" and prev:
            out.append("{" + kicad_unescape(token) + "}")
        elif token in NET_ESCAPES:
            out.append(NET_ESCAPES[token])
        else:
            out.append("{" + kicad_unescape(token) + "}")
        prev, i = "}", j + 1
    return "".join(out)


def overbar_markup(text, d):
    """A text or net name as KiCad reads it: before format NEW_OVERBAR an overbar ran from one ~ to
    the next (or to a space, } or ) ), and ~~ was a ~; KiCad turns that into ~{...} on reading
    (string_utils.cpp ConvertToNewOverbarNotation)."""
    if d.format >= NEW_OVERBAR or "~" not in text or text == "~":
        return text
    out, inside, i, n = [], False, 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "~":
            nxt = text[i + 1] if i + 1 < n else ""
            if nxt == "~":
                if i + 2 < n and text[i + 2] == "{":
                    out.append("~~{}")          # the { after it must not start an overbar
                    i += 1
                else:
                    out.append("~")
                    i += 2
                continue
            if nxt == "{":
                return text                     # already the new notation
            out.append("}" if inside else "~{")
            inside = not inside
            i += 1
            continue
        if ch in " })" and inside:
            out.append("}")
            inside = False
        out.append(ch)
        i += 1
    return "".join(out) + ("}" if inside else "")


def net_table(tree, d):
    """{"3": "GND"} from the board's (net 3 "GND") entries (KiCad 9 and older; KiCad 10 writes none),
    with "" for a net with no name."""
    return {str(n[1]): kicad_unescape(overbar_markup(str(n[2]), d)) if len(n) > 2 else "" for n in children(tree, "net")}


def net_of(nets, node, d):
    """The name of an item's net, "" for none: (net 3) in KiCad 9 and older is a number in the net
    table; KiCad 10 writes the net's name itself."""
    n = child(node, "net")
    if not n or len(n) < 2:
        return ""
    key = str(n[1])
    if key in nets:
        return nets[key]
    return kicad_unescape(overbar_markup(key, d)) if key != "0" else ""


# ---- text --------------------------------------------------------------------------------------
LEGACY_TEXT_SIZE_MM = 1.524     # KiCad 4 leaves out a text size of 60 mils (parseEDA_TEXT)


def text_size(font_node):
    """(height, width) of a text's font; KiCad 4 wrote none for the 60 mil default."""
    size = child(font_node, "size")
    return (float(size[1]), float(size[2])) if size else (LEGACY_TEXT_SIZE_MM, LEGACY_TEXT_SIZE_MM)


def is_hidden(node):
    """A text's hide flag: (hide yes) from KiCad 8, a bare hide in the node or its (effects ...)
    before."""
    h_ = child(node, "hide")
    effects = child(node, "effects") or []
    return (yes(h_[1]) if h_ is not None and len(h_) > 1 else h_ is not None) \
        or "hide" in atoms(node) or "hide" in atoms(effects) \
        or (child(effects, "hide") is not None and yes((child(effects, "hide") + ["yes"])[1]))


def kept_upright(node):
    """Whether KiCad keeps a footprint text upright: unless the file says (unlocked yes), or before
    KiCad 8 a bare unlocked in its (at ...)."""
    if "unlocked" in [str(a) for a in atoms(child(node, "at"))]:
        return False
    unlocked = child(node, "unlocked")
    return unlocked is None or (len(unlocked) > 1 and not yes(unlocked[1]))


def is_knockout(node):
    """Knockout text, KiCad 7+: (layer "F.Cu" knockout)."""
    return "knockout" in [str(a) for a in atoms(child(node, "layer"))]


def footprint_text_fields(fp):
    """{FIELD: value} of a footprint's own fields: its (property "Name" "value") entries (KiCad 8+
    keeps reference and value there too) and, before KiCad 8, (fp_text reference|value "...")."""
    out = {}
    for prop in children(fp, "property"):
        if len(prop) > 2 and not isinstance(prop[2], list):
            out[str(prop[1]).upper()] = str(prop[2])
    for t in children(fp, "fp_text"):
        if len(t) > 2 and t[1] in ("reference", "value"):
            out[t[1].upper()] = str(t[2])
    return out


def render_cache_rings(node, text, angle):
    """The glyph polygons KiCad 7+ stores with a TrueType text, (render_cache "text" angle (polygon
    (pts outline) (pts hole) ...) ...), as [[outline, hole, ...] per polygon] of (x, y) in board
    coordinates.  None when there is none or it is stale - made for another text or angle - as KiCad
    then draws it anew (EDA_TEXT::GetRenderCache)."""
    rc = child(node, "render_cache")
    if rc is None or len(rc) < 3 or isinstance(rc[1], list) or str(rc[1]) != text:
        return None
    try:
        turned = (float(rc[2]) - angle + 180.0) % 360.0 - 180.0
    except (TypeError, ValueError):
        return None
    if abs(turned) > 1e-6:
        return None
    out = []
    for poly in children(rc, "polygon"):
        rings = [[(float(p[1]), float(p[2])) for p in pts[1:] if isinstance(p, list) and p[0] == "xy"]
                 for pts in children(poly, "pts")]
        out.append([r for r in rings if len(r) >= 3])
    return out
