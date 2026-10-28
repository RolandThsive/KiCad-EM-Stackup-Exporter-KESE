"""Stage 2 - collect: every item of the parsed board as a flat shape on its layer, with its net,
in KiCad's frame (mm, Y down).  This file walks the tree; there is one file per kind of item."""
from kese.core import font
from kese.core.sexp import child
from kese.model.items import Items
from kese.s2_collect.context import Context
from kese.s2_collect.drawings import GRAPHICS, add_drawing
from kese.s2_collect.footprints import add_footprint
from kese.s2_collect.left_out import UNKNOWN, warn
from kese.s2_collect.nets import read_nets
from kese.s2_collect.setup import read_setup
from kese.s2_collect.stackup import read_stackup
from kese.s2_collect.text import TEXT, add_text
from kese.s2_collect.tracks import add_track
from kese.s2_collect.vias import add_via, drop_unconnected_rings
from kese.s2_collect.zones import UNFILLED, add_zone

# items that are not part of the physical board, counted under skipped
NOT_PHYSICAL = ("image", "target", "group", "generated", "table", "barcode", "point", "grid_item", "drill_chart",
                "drill_map")
# the rest of a board file: settings, not items (KiCad 4 to KiCad's development version)
SETTINGS = {"version", "host", "generator", "generator_version", "general", "page", "paper", "title_block", "layers",
            "setup", "property", "net", "net_class", "net_chains", "variants", "constraint", "embedded_fonts",
            "embedded_files"}


def run(raw, job):
    with job.stage("collect", "collect (tracks, pads, zones, vias, drawings, text)"):
        return collect(raw, job.note)


def collect(raw, log):
    """RawBoard -> Items."""
    tree = raw.tree
    items = Items(raw=raw, name=raw.name, layers=raw.copper_layers, stackup=None)
    setup = child(tree, "setup") or []
    items.stackup = read_stackup(tree, raw.copper_layers, raw.file_thickness, log)
    read_setup(items, setup)
    read_nets(items, tree)
    ctx = Context(items)
    vias = []
    for node in tree[1:]:
        if not isinstance(node, list) or not node:
            continue
        k = node[0]
        if k in ("segment", "arc"):
            add_track(ctx, node)
        elif k == "via":
            vias.append(node)
        elif k == "zone":
            add_zone(ctx, node)
        elif k in GRAPHICS:
            add_drawing(ctx, node, lambda p: p)
        elif k in ("footprint", "module"):
            add_footprint(ctx, node)
        elif k in TEXT:
            add_text(ctx, node)
        elif k in NOT_PHYSICAL:
            items.skipped[f"{k} items"] += 1
        elif k not in SETTINGS:
            items.skipped[f"{k} {UNKNOWN}"] += 1
    for v in vias:
        add_via(ctx, v)
    drop_unconnected_rings(ctx)
    unfilled = items.skipped.get(UNFILLED, 0)
    if unfilled:
        log(f"warning: {unfilled} copper zone(s) have no fill stored in the file and are ignored "
            "(fill the zones in KiCad, press B, and save; see parameters/copper.py)")
    warn(items, log)
    _, note = font.load()
    items.notes.append(note)
    return items
