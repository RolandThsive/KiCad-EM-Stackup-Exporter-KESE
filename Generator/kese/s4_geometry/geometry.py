"""Stage 4 - geometry: the resolved regions -> a PrismSet, flat regions between two heights for
the laminate, copper, plating, solder mask, silkscreen and finish."""
from kese.model.prisms import PrismSet
from kese.s4_geometry import copper, finish, finish_shells, laminate, plating, silkscreen, solder_mask
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
    finish_shells.build(regions, ps)
    return leave_out_disabled(ps)


# which switch keeps each role in the model (FINISH_ENABLED also decides whether finish.build makes any)
ENABLED_BY = {"board": ("Board", "BOARD_ENABLED"), "copper": ("Copper", "COPPER_ENABLED"),
              "plating": ("Copper", "COPPER_ENABLED"), "finish": ("Finish", "FINISH_ENABLED"),
              "mask": ("SolderMask", "SOLDER_MASK_ENABLED"), "mask_over_copper": ("SolderMask", "SOLDER_MASK_ENABLED"),
              "silk": ("Silkscreen", "SILKSCREEN_ENABLED")}


def enabled(role):
    module, name = ENABLED_BY[role]
    return getattr(getattr(P, module), name)


def leave_out_disabled(ps):
    """Drop the prisms of every role switched off.  Everything is built first, so what stays is
    exactly as it would be with every switch on (the mask still steps over the copper left out)."""
    off = sorted({f"{m}.{n}" for r, (m, n) in ENABLED_BY.items() if r != "finish" and not enabled(r)})
    if off:
        ps.prisms = [p for p in ps.prisms if enabled(p.role)]
        ps.notes.append(f"left out of every file: {', '.join(off)} = False")
    return ps
