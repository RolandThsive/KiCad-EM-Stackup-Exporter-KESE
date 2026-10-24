"""Stage 3 - resolve: the collected items -> 2D regions in the board frame (mm, Y up, origin per
Run.ORIGIN), snapped to the grid, with the holes applied per layer span."""
from kese.model.regions import Regions
from kese.s3_resolve.copper import copper_layers, join_nets
from kese.s3_resolve.edge_plating import edge_plating
from kese.s3_resolve.frame import place
from kese.s3_resolve.holes import band_laminate, barrels, castellate, exact_circles, slabs
from kese.s3_resolve.mask import mask_openings, mask_regions
from kese.s3_resolve.outline import outline_from
from kese.s3_resolve.silk import clip_silk


def run(items, job):
    with job.stage("resolve", "resolve (regions per layer and net, holes applied)"):
        return resolve(items, job.note)


def resolve(items, log):
    """Items -> Regions.  The order matters: edge plating changes the copper and the laminate,
    and everything after it builds on the result."""
    outline_k = outline_from(items, log)          # KiCad frame
    r = Regions(items=items, layers=items.layers, stackup=items.stackup)
    place(r, outline_k)
    castellate(items, outline_k)
    slabs(r, items)
    copper_layers(r, items, outline_k)
    edge_plating(r, items, log)
    join_nets(r)
    band_laminate(r, items)
    barrels(r, items, outline_k)
    exact_circles(r, items)
    openings = mask_openings(r, items, outline_k)
    mask_regions(r)
    clip_silk(r, items, outline_k, openings)
    return r
