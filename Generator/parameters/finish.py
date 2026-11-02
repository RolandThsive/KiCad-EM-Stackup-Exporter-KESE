"""
parameters/finish.py - the surface finish on copper left bare by the solder mask.

Off by default so the geometry matches KiCad; turn on for an as-fabricated model.
"""

FINISH_ENABLED = False

# "file" - take the type from the stackup's (copper_finish "...") field, else FINISH_DEFAULT_TYPE
# or one of the keys of FINISH_TYPES
FINISH_TYPE = "file"
FINISH_DEFAULT_TYPE = "ENIG"

# Finish parts:
#   "metal" - one part per side and metal: "Top Finish Nickel", "Top Finish Gold", ...
#   "net"   - one part per side, metal and net: "Top Finish Gold_GND", so a net's copper, nickel
#             and gold can be picked together in the solver (Copper_GND, Top Finish Nickel_GND, ...)
FINISH_GROUPING = "metal"

# The finish on the plated board edge (Copper.EDGE_PLATING) and inside the plated castellations.
# Plated edges are routed and plated before the finish goes on, so the finish covers the edge wall
# as it covers the top and bottom copper (ENIG is the usual finish there).  Each metal is a shell
# round the edge copper, in the air beside it, from the bottom of B.Cu to the top of F.Cu; where the
# top or bottom copper at the edge is bare (no mask), the shell wraps over the corner and meets the
# Top / Bottom Finish, so the edge copper is covered without a gap.  Part "Edge Finish <metal>".
#   FINISH_ON_EDGE_PLATING - the plated board edge
#   FINISH_ON_CASTELLATIONS - the part-barrels of the castellated holes (and their cut ends)
FINISH_ON_EDGE_PLATING = True
FINISH_ON_CASTELLATIONS = True

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

# KiCad's copper_finish names (board setup > physical stackup) -> keys of FINISH_TYPES.
# Matching ignores case, spaces, '-' and '_'.  "None" means no finish at all (nothing is built).
FINISH_NAME_ALIASES = {
    "HAL SnPb": "HASL", "HAL lead-free": "HASL_LF", "Hard gold": "HardGold",
    "Immersion tin": "ImmersionTin", "Immersion silver": "ImmersionSilver", "HT_OSP": "OSP",
}

# Electrical properties per finish metal, for materials.json
FINISH_CONDUCTIVITY_S_PER_M = {
    "Nickel": 1.4e7, "Gold": 4.1e7, "Palladium": 9.5e6, "Tin": 9.1e6, "Silver": 6.3e7, "OSP": 0.0,
}
