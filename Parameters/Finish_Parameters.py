"""
Finish_Parameters.py - the surface finish on copper left bare by the solder mask.

Off by default so the geometry matches KiCad; turn on for an as-fabricated model.
"""

FINISH_ENABLED = True

# "file" - take the type from the stackup's (copper_finish "...") field, else FINISH_DEFAULT_TYPE
# or one of the keys of FINISH_TYPES
FINISH_TYPE = "file"
FINISH_DEFAULT_TYPE = "ENIG"

# Layers of each finish, bottom to top, in mm.  Each becomes its own solid on the exposed copper.
FINISH_TYPES = {
    "ENIG": [("Nickel", 0.005), ("Gold", 0.00008)],
    "HASL": [("Tin", 0.010)],
    "HASL_LF": [("Tin", 0.010)],
    "OSP": [("OSP", 0.0003)],
    "ImmersionSilver": [("Silver", 0.0002)],
    "ImmersionTin": [("Tin", 0.001)],
    "HardGold": [("Nickel", 0.005), ("Gold", 0.001)],
}

# Electrical properties per finish metal, for materials.json
FINISH_CONDUCTIVITY_S_PER_M = {
    "Nickel": 1.4e7, "Gold": 4.1e7, "Tin": 9.1e6, "Silver": 6.3e7, "OSP": 0.0,
}
