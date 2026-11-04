"""
parameters/finish.py - the surface finish on copper left bare by the solder mask.
"""

# Build the surface finish and write it to every output file.  False leaves the bare copper as
# KiCad draws it.
FINISH_ENABLED = True

# A key of FINISH_TYPES, or "file" to take the type from the board's stack-up (Board Setup >
# Physical Stackup > Copper finish).  With "file" the run stops with an error when the board names
# no finish (no stack-up, or the field left empty) or one KESE does not know: change FINISH_TYPE
# or set the finish in KiCad.  A stack-up whose finish is "None" gets no finish.
FINISH_TYPE = "ENIG"

# Finish parts:
#   "metal" - one part per side and metal: "Top Finish Nickel", "Top Finish Gold", ...
#   "net"   - one part per side, metal and net: "Top Finish Gold_GND", so a net's copper, nickel
#             and gold can be picked together in the solver (Copper_GND, Top Finish Nickel_GND, ...)
FINISH_GROUPING = "metal"

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
