"""
parameters/board.py - the laminate: thickness, dielectrics, outline and holes.

Values marked "typical" are common rigid-FR4 production values; replace them with your
fabricator's datasheet numbers for lab work.
"""

# Laminate thickness in mm, or None to take it from the board file:
#   with a stackup   -> sum of the stackup's dielectric layers (+ inner copper), so the finished
#                       board (laminate + outer copper + mask) equals KiCad's board thickness
#   without stackup  -> KiCad's (general (thickness ...)) value
BOARD_THICKNESS_MM = None

# When the file has no stackup, how the laminate is divided between copper layers:
#   "even" - equal dielectric thickness between every pair of copper layers
DIELECTRIC_SPLIT = "even"

# Dielectric material when the stackup gives none
DEFAULT_DIELECTRIC_MATERIAL = "FR4"
DEFAULT_DIELECTRIC_TYPE = "core"        # "core" or "prepreg"
DEFAULT_EPSILON_R = 4.5                 # typical FR4 at 1 GHz
DEFAULT_LOSS_TANGENT = 0.02             # typical FR4 at 1 GHz
# Stackup values win over the defaults when present
USE_STACKUP_EPSILON_R = True
USE_STACKUP_LOSS_TANGENT = True

# Resin of the prepreg/core fills the space between inner copper traces (true for pressed laminates)
RESIN_FILL_BETWEEN_INNER_COPPER = True

# Holes
INCLUDE_NON_PLATED_HOLES = True         # NPTH pads become holes through the board

# Board outline
OUTLINE_LINE_SNAP_MM = 1e-5             # Edge.Cuts line/arc end points closer than this are joined
OUTLINE_FALLBACK = "copper_hull"        # when there is no Edge.Cuts: "copper_hull" (convex hull of the copper + margin) or "error"
OUTLINE_FALLBACK_MARGIN_MM = 1.0
