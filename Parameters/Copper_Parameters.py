"""
Copper_Parameters.py - copper foils, plating, vias and the finished copper geometry.

Values marked "typical" are common rigid-FR4 production values; replace them with your
fabricator's datasheet numbers for lab work.
"""

# Base foil thickness in mm when the stackup gives none (1 oz = 0.035 mm, 0.5 oz = 0.0175 mm)
DEFAULT_OUTER_FOIL_MM = 0.035
DEFAULT_INNER_FOIL_MM = 0.035
USE_STACKUP_COPPER_THICKNESS = True     # stackup (layer "F.Cu" (thickness ...)) wins when present

# Electroplating adds copper to the OUTER layers during hole plating (the "finished copper").
# Finished outer copper = foil + this value.  Typical 0.020 mm.  0 = foil only (what KiCad models).
OUTER_PLATING_ADDED_MM = 0.0

# Hole wall plating
VIA_WALL_MM = 0.025                     # plated wall thickness of vias (typical 0.020-0.025)
PTH_WALL_MM = 0.025                     # plated wall thickness of through-hole pads

# Etch factor: real traces are trapezoids, narrower at the top than at the foot.
#   0.0  -> rectangular cross-section (default, matches KiCad)
#   e.g. 0.5 -> each side wall leans in by 0.5 x copper thickness over the copper height
ETCH_FACTOR = 0.0
ETCH_STEPS = 4                          # the trapezoid is built as this many stacked slices
ETCH_APPLY_TO_INNER_LAYERS = False      # inner copper is etched from the core side; foot toward the board centre

# Via tenting (mask over the via):
#   "file"   - follow the board file (KiCad 9/10 tenting settings, older plot setting, else tented)
#   "tented" - cover every via with mask
#   "open"   - open the mask over every via
VIA_TENTING = "file"

# KiCad's "remove unused layers" on vias: drop annular rings on layers nothing connects to
HONOUR_REMOVE_UNUSED_LAYERS = True

# Electrical properties (written to materials.json for the solver)
COPPER_CONDUCTIVITY_S_PER_M = 5.8e7
COPPER_SURFACE_ROUGHNESS_UM = 0.0       # 0 = ignore; e.g. 1.5 for standard foil (solver setting, not geometry)

# Name used for copper that belongs to no net (board graphics, unconnected pads)
NO_NET_NAME = "no_net"
