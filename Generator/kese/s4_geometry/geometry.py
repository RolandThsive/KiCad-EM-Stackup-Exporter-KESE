"""Stage 4 - geometry: the resolved regions -> a PrismSet, flat regions between two heights for
the laminate, copper, plating, solder mask, silkscreen and finish."""
from kese.model.prisms import PrismSet
from kese.s4_geometry import copper, finish, laminate, plating, silkscreen, solder_mask
from kese.s4_geometry.heights import copper_bands
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
    return ps
