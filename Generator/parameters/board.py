"""
parameters/board.py - the laminate: thickness, dielectrics, outline and holes.

Values marked "typical" are common rigid-FR4 production values; replace them with your
fabricator's datasheet numbers for lab work.
"""

# Dielectric grouping in "simulation" mode:
#   "layer"  - one solid per stackup dielectric (core / prepreg), each with its own material
#   "merged" - the whole laminate as one solid
DIELECTRIC_GROUPING = "layer"

# Build the laminate (the "board" parts, one per dielectric) and write it to every output file.
BOARD_ENABLED = True

# Laminate thickness in mm, or None to take it from the board file:
#   with a stackup   -> sum of the stackup's dielectric layers (+ inner copper), so the finished
#                       board (laminate + outer copper + mask) equals KiCad's board thickness
#   without stackup  -> KiCad's (general (thickness ...)) value less the outer copper and the two
#                       masks, so the finished board again equals KiCad's board thickness
BOARD_THICKNESS_MM = None
DEFAULT_BOARD_THICKNESS_MM = 1.6        # finished board thickness when the file gives none (KiCad's default)

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
OUTLINE_LINE_SNAP_MM = 0.01             # loose Edge.Cuts line/arc ends closer than this are joined (KiCad: 0.01 mm)
OUTLINE_FALLBACK = "copper_hull"        # when there is no Edge.Cuts: "copper_hull" (convex hull of the copper + margin) or "error"
OUTLINE_FALLBACK_MARGIN_MM = 1.0
OUTLINE_DUPLICATE_AREA_MM2 = 1e-6       # two closed Edge.Cuts outlines differing by less than this area are one
