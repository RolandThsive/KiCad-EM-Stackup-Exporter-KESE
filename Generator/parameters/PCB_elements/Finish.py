"""
parameters/PCB_elements/Finish.py - the surface finish on copper left bare by the solder mask.

Whether the finish is built is in Stackup.py: the lines "top_finish" and "bottom_finish" (the
finish on the two faces) and "hole_finish" (the finish inside the plated holes and on the
board's edge).

Sections, as in every element's file:  1 Parts  2 Thickness  3 Shape  4 Material (for the solver)
5 Color (for the viewer)
"""

# ==================================================================================================
# 1. Parts
# ==================================================================================================
# "file" takes the type from the board file (KiCad: Board Setup > Physical Stackup > Copper finish),
# or a key of FINISH_TYPES gives every board that finish.  With "file" a board file whose finish is
# "None" gets no finish, and the run stops with an error, before any work, when the board file names
# no finish (it has no stack-up, or the field is left empty) or one KESE does not know: set the
# finish in KiCad, or name one here (on the command line: --set Finish.FINISH_TYPE=ENIG), or leave
# the finish out (--set Stackup.finish=False).
FINISH_TYPE = "file"

# KiCad's copper_finish names (board setup > physical stackup) -> keys of FINISH_TYPES.
# Matching ignores case, spaces, '-' and '_'.  "None" means no finish at all (nothing is built).
FINISH_NAME_ALIASES = {
    "HAL SnPb": "HASL", "HAL lead-free": "HASL_LF", "Hard gold": "HardGold",
    "Immersion tin": "ImmersionTin", "Immersion silver": "ImmersionSilver", "HT_OSP": "OSP",
}

# Finish parts:
#   "metal" - one part per side and metal: "Top Finish Nickel", "Top Finish Gold", ...
#   "net"   - one part per side, metal and net: "Top Finish Gold_GND", so a net's copper, nickel
#             and gold can be picked together in the solver (Copper_GND, Top Finish Nickel_GND, ...)
FINISH_GROUPING = "metal"


# ==================================================================================================
# 2. Thickness
# ==================================================================================================
# Layers of each finish, bottom to top, in mm.  Each becomes its own solid on the exposed copper.
FINISH_TYPES = {
    "ENIG": [("Nickel", 0.005), ("Gold", 0.00008)],
    "ENEPIG": [("Nickel", 0.005), ("Palladium", 0.0001), ("Gold", 0.00005)],
    "HASL": [("Tin", 0.010)],
    "HASL_LF": [("Tin", 0.010)],
    "OSP": [("OSP", 0.0003)],
    "ImmersionSilver": [("Silver", 0.0002)],
    "ImmersionTin": [("Tin", 0.001)],
    "HardGold": [("Nickel", 0.005), ("Gold", 0.001)],
}


# ==================================================================================================
# 3. Shape
# ==================================================================================================
# When the finish goes on, against the solder mask:
#   False - after the mask (the usual flow, solder mask over bare copper): only the copper in the
#           mask openings takes the finish, and ink kept in an opening keeps it off
#   True  - before the mask (e.g. full-body electroplated hard gold): all the outer copper takes the
#           finish, and the mask and the silkscreen lie on it, raised by its thickness over copper
FINISH_BEFORE_SOLDER_MASK = False

# The finish coats every bare copper face, as the baths do: the tops of the copper in the mask
# openings ("Top / Bottom Finish <metal>"), and also, built in:
#   - the copper's side walls where they meet the air: pads and traces in the openings, and copper
#     the board edge cuts on any layer (part of the side's finish on F.Cu / B.Cu, "Edge Finish
#     <metal>" on the inner layers)
#   - the plated board edge and the castellations, wrapping over onto the top and bottom finish
#     ("Edge Finish <metal>")
#   - inside the bore of every plated hole open at a face ("Hole Finish <metal>")

# How the finish follows the copper's sharp corners: the outer side of each finish layer (and of the
# copper the mask wraps, with FINISH_BEFORE_SOLDER_MASK) keeps the corner's point out to this many
# times the finish's thickness from the copper's corner, and is cut straight across there.  At 2.0 a
# corner of 60 degrees or more keeps its point (a square pad's corners stay square); a sharper one,
# such as the tip of a zone's spike, is cut.  1.0 cuts every corner at the finish's thickness;
# higher values let sharp tips reach further out.
FINISH_MITRE_LIMIT = 2.0


# ==================================================================================================
# 4. Material (written to materials.json for the solver; it changes no geometry)
# ==================================================================================================
# Conductivity of each finish metal, S/m (bulk values)
FINISH_CONDUCTIVITY_S_PER_M = {
    "Nickel": 1.4e7, "Gold": 4.1e7, "Palladium": 9.5e6, "Tin": 9.1e6, "Silver": 6.3e7, "OSP": 0.0,
}


# ==================================================================================================
# 5. Color (GLB, OBJ and STEP)
# ==================================================================================================
# sRGB hex colour, alpha 0-1 (below 1 is see-through), metallic 0-1, and roughness 0-1: how matte it
# looks in a viewer.  One per finish metal.
FINISH_COLORS = {
    "Nickel":    {"color": "#B8B8B0", "alpha": 1.0, "metallic": 1.0, "roughness": 0.40},
    "Gold":      {"color": "#E6C15A", "alpha": 1.0, "metallic": 1.0, "roughness": 0.20},
    "Tin":       {"color": "#C9C9C9", "alpha": 1.0, "metallic": 1.0, "roughness": 0.45},
    "Silver":    {"color": "#E4E4E0", "alpha": 1.0, "metallic": 1.0, "roughness": 0.25},
    # ENEPIG's palladium: sRGB (223, 218, 212), the base colour that published PBR tables of measured metals give it
    "Palladium": {"color": "#DFDAD4", "alpha": 1.0, "metallic": 1.0, "roughness": 0.30},
    "OSP":       {"color": "#D9955A", "alpha": 1.0, "metallic": 0.8, "roughness": 0.35},
}
