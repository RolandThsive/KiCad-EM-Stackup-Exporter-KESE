"""Footprint courtyards (F.CrtYd, B.CrtYd), for what KESE needs them for: KiCad 10 cuts the hatch of
a hatched drawing back from the courtyard of every other footprint on the drawing's side
(PCB_SHAPE::getHatchingKnockouts), the courtyard built as FOOTPRINT::BuildCourtyardCaches builds it."""
import functools

import shapely

from kese.core.outlines import faces, nested
from kese.s2_collect.hatch import Knockout

LAYERS = ("F.CrtYd", "B.CrtYd")
CHAIN_MM = 0.02          # courtyard line ends this close are chained into one outline (chainingEpsilon)
SHRINK_MM = 0.005        # the courtyard is shrunk this much (its maxError), so courtyards that touch do not overlap


def add_courtyards(ctx, drawn, fp):
    """drawn: {courtyard layer: [(centre-line geometry, closed?)]} of one footprint's drawings, board
    frame (drawings.graphic) -> a Knockout of kind "courtyard" on that layer, built when first used."""
    for layer, parts in drawn.items():
        box = shapely.total_bounds([g for g, _ in parts])
        ctx.knockouts.append(Knockout(layer, fp, "courtyard", tuple(box), once(parts)))


def once(parts):
    """margin -> the courtyard of `parts`, made on the first call: it knocks out no more for a margin."""
    built = functools.cache(lambda: courtyard(parts))
    return lambda _margin: built()


def courtyard(parts):
    """The area a footprint's drawings on one courtyard layer enclose (ConvertOutlineToPolygon):
    closed shapes as they are, lines and arcs chained where their ends lie within CHAIN_MM, an
    outline inside another a hole in it; shrunk by SHRINK_MM.  Lines that close nothing give nothing."""
    rings = [p for g, closed in parts if closed for p in shapely.get_parts(g) if p.geom_type == "Polygon"]
    lines = [g for g, closed in parts if not closed and not g.is_empty]
    if lines:
        rings += faces(lines, CHAIN_MM)[0]
    area = nested([r for r in rings if r.is_valid and r.area > 0])
    return area.buffer(-SHRINK_MM, join_style="mitre", mitre_limit=2.0)
