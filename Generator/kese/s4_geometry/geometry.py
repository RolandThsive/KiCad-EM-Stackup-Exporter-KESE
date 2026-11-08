"""Stage 4 - geometry: the resolved regions -> a PrismSet, flat regions between two heights for
the laminate, copper, plating, via fills, solder mask, silkscreen and finish."""
from kese.core import shapes2d as sh
from kese.model.prisms import PrismSet
from kese.s4_geometry import copper, finish, finish_shells, laminate, plating, silkscreen, solder_mask, via_fill
from kese.s4_geometry.switches import enabled, switched_off


def run(regions, job):
    with job.stage("geometry", "geometry (prisms for laminate, copper, mask, silk)"):
        return geometry(regions, job.mode)


def geometry(regions, mode):
    """Regions -> PrismSet, in the heights stage 3 set (s3_resolve/heights.py)."""
    ps = PrismSet(regions=regions)
    laminate.build(regions, ps)
    copper.build(regions, ps)
    plating.build(regions, ps)
    via_fill.build(regions, ps)
    solder_mask.build(regions, ps, mode)
    silkscreen.build(regions, ps)
    finish.build(regions, ps)
    finish_shells.build(regions, ps)
    ps.free_levels = free_levels(regions, ps)
    return leave_out_disabled(ps)


def free_levels(r, ps):
    """The heights only post machining and via plugs bring (KiCad 10): the steps of the cuts in the
    laminate and the barrels, and the plugs' ends, but no copper layer's or dielectric's own heights.
    A wall runs on across them where nothing stops it (kese/core/tall_walls.py)."""
    st, d = r.stackup, sh.G().HEIGHT_DIGITS
    cut = {z for into in (r.slab_cuts, r.band_cuts) for cuts in into.values() for z0, z1, _ in cuts for z in (z0, z1)}
    cut |= {z for _, z0, z1, *_ in r.barrel_pieces for z in (z0, z1)}
    cut |= {z for p in ps.prisms if p.role == "via_resin" for z in (p.z0, p.z1)}
    own = {z for band in st.band.values() for z in band}
    return frozenset(round(z, d) for z in cut) - {round(z, d) for z in own}


def leave_out_disabled(ps):
    """Drop the prisms of every part switched off.  Everything is built first, so what stays is
    exactly as it would be with every switch on (the mask still steps over copper left out)."""
    off = switched_off()
    if off:
        ps.prisms = [p for p in ps.prisms if enabled(p.role)]
        ps.notes.append(f"left out of every file: {', '.join(off)} = False")
    return ps
