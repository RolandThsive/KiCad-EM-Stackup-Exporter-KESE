"""Stage 4 - geometry: the resolved regions -> a PrismSet, flat regions between two heights for
the laminate, copper, plating, solder mask, silkscreen and finish."""
from kese.model.prisms import PrismSet
from kese.s4_geometry import copper, finish, finish_shells, laminate, plating, silkscreen, solder_mask
from kese.s4_geometry.heights import copper_bands
from kese.s4_geometry.switches import enabled, switched_off
from parameters import P


def run(regions, job):
    with job.stage("geometry", "geometry (prisms for laminate, copper, mask, silk)"):
        return geometry(regions, job.mode)


def geometry(regions, mode):
    """Regions -> PrismSet.  Sets the copper bands of the stackup first: finished outer copper
    is foil + plating."""
    st = regions.stackup
    copper_bands(st, {l: st.copper_thickness[l] + P.Copper.OUTER_PLATING_ADDED_MM for l in ("F.Cu", "B.Cu")})
    ps = PrismSet(regions=regions)
    laminate.build(regions, ps)
    copper.build(regions, ps)
    plating.build(regions, ps)
    solder_mask.build(regions, ps, mode)
    silkscreen.build(regions, ps)
    finish.build(regions, ps)
    finish_shells.build(regions, ps)
    return leave_out_disabled(ps)


def leave_out_disabled(ps):
    """Drop the prisms of every part switched off.  Everything is built first, so what stays is
    exactly as it would be with every switch on (the mask still steps over copper left out)."""
    off = switched_off()
    if off:
        ps.prisms = [p for p in ps.prisms if enabled(p.role)]
        ps.notes.append(f"left out of every file: {', '.join(off)} = False")
    return ps
