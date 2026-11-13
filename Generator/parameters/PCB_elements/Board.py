"""
parameters/PCB_elements/Board.py - the board: its laminate (the dielectric between the copper
layers), its outline, and the holes and machining that cut through every layer.

The board file is read first (KiCad: Board Setup > Physical Stackup, and Edge.Cuts).  The values
here fill in what the file leaves out, or replace it where a USE_STACKUP_* switch is False or
PLIES_BY_HAND lists a gap.  Values marked "generic" are common rigid-FR4 values; replace them with
your fabricator's datasheet numbers for lab work.

Whether the laminate is built, and whether its plies are fused or separate, is in Stackup.py:
the lines "board" (plies fused), "prepreg_plies" and "cores" (plies separate), and
"resin_between_traces" (both).

Sections, as in every element's file:  1 Parts  2 Thickness  3 Shape  4 Material (for the solver)
5 Color (for the viewer)
"""

# ==================================================================================================
# 1. Parts
# ==================================================================================================
# Plies fused:    one solid for each gap between two copper layers     "Board_dielectric 1"
# Plies separate: one solid for each prepreg ply                       "Board_dielectric 1 ply 1"
#                 one solid for each core                              "Board_dielectric 2"
#                 one solid for the resin beside each inner copper     "Board_resin In1.Cu"

# Plies separate: neighbouring plies of one gap with the same material and values become one solid
JOIN_EQUAL_PLIES = False

# "layer"  - the solids listed above, as the stack-up being built says
# "merged" - the whole laminate as one solid ("Board"), whichever stack-up is built
DIELECTRIC_GROUPING = "layer"


# ==================================================================================================
# 2. Thickness
# ==================================================================================================
# --- The whole laminate ---
# Laminate thickness in mm, or None to take it from the board file:
#   with a stack-up   -> sum of its dielectric layers (+ inner copper), so the finished board
#                        (laminate + outer copper + mask) equals KiCad's board thickness
#   without one       -> KiCad's (general (thickness ...)) value less the outer copper and the two
#                        masks, so the finished board again equals KiCad's board thickness
# A number keeps the plies' proportions, scaled to it.
BOARD_THICKNESS_MM = None
DEFAULT_BOARD_THICKNESS_MM = 1.6        # finished board thickness when the file gives none (KiCad's default)

# When the file has no stack-up, how the laminate is divided between copper layers:
#   "even" - equal dielectric thickness between every pair of copper layers
DIELECTRIC_SPLIT = "even"

# Plies separate: a ply thinner than this (mm) is joined to its thicker neighbour, with a warning
PLY_MIN_THICKNESS_MM = 0.001

# --- Plies written by hand ---
# Empty: every ply comes from the board file.  To give a board other plies, add the board's file name
# (without .kicad_pcb) and, under it, each gap to change, named by its two copper layers.  A gap
# listed here takes these plies, top to bottom, instead of the file's; gaps not listed still come
# from the file, and other boards are not touched.  Each ply:
#   "type"                    "core" or "prepreg"
#   "thickness_mm"
#   "material"                a name, written to materials.json
#   "epsilon_r", "loss_tangent"
#   "frequency_hz", "model"   optional; left out, the defaults in Material below
# KESE checks the list before it builds anything: the two copper layers must be neighbours on that
# board, and every thickness above 0.
# The example is a whole four-layer board: its three gaps, from the top copper down to the bottom.
PLIES_BY_HAND = {
    # "14_stackup_full": {
    #     ("F.Cu", "In1.Cu"): [
    #         {"type": "prepreg", "thickness_mm": 0.100, "material": "1080", "epsilon_r": 3.8, "loss_tangent": 0.015},
    #         {"type": "prepreg", "thickness_mm": 0.120, "material": "2116", "epsilon_r": 4.1, "loss_tangent": 0.017},
    #     ],
    #     ("In1.Cu", "In2.Cu"): [
    #         {"type": "core",    "thickness_mm": 1.000, "material": "FR4 core", "epsilon_r": 4.6, "loss_tangent": 0.018},
    #     ],
    #     ("In2.Cu", "B.Cu"): [
    #         {"type": "prepreg", "thickness_mm": 0.120, "material": "2116", "epsilon_r": 4.1, "loss_tangent": 0.017},
    #         {"type": "prepreg", "thickness_mm": 0.100, "material": "1080", "epsilon_r": 3.8, "loss_tangent": 0.015},
    #     ],
    # },
}


# ==================================================================================================
# 3. Shape
# ==================================================================================================
# --- Outline ---
OUTLINE_LINE_SNAP_MM = 0.01             # loose Edge.Cuts line/arc ends closer than this are joined (KiCad: 0.01 mm)
OUTLINE_FALLBACK = "copper_hull"        # when there is no Edge.Cuts: "copper_hull" (convex hull of the copper + margin) or "error"
OUTLINE_FALLBACK_MARGIN_MM = 1.0
OUTLINE_DUPLICATE_AREA_MM2 = 1e-6       # two closed Edge.Cuts outlines differing by less than this area are one
OUTLINE_MIN_AREA_MM2 = 1e-9             # a closed Edge.Cuts outline of this area or less is left out (a line drawn
                                        # there and back, or a circle of no size)

# --- Holes and machining ---
INCLUDE_NON_PLATED_HOLES = True         # NPTH pads become holes through the board
# KiCad 10's extra drills of pads and vias
BACKDRILLS = True                       # backdrills and tertiary drills: the hole is drilled out, plating and
                                        # copper too, from their start layer through their must-cut layer
POST_MACHINING = True                   # counterbores and countersinks are cut from the board's face
# A countersink's cone is built as steps (the solids have vertical walls).  Each step's radius is the
# cone's at the middle of the step, and the steps are short enough to stray from the cone by at most
# this much; copper and inner layers are cut as KiCad cuts them, at the cone's radius at their face.
COUNTERSINK_STEP_TOLERANCE_MM = 0.025


# ==================================================================================================
# 4. Material (written to materials.json for the solver; it changes no geometry)
# ==================================================================================================
# --- Plies, where the board file gives none (all generic) ---
DEFAULT_DIELECTRIC_MATERIAL = "FR4"
DEFAULT_DIELECTRIC_TYPE = "core"        # "core" or "prepreg"
DEFAULT_EPSILON_R = 4.5                 # generic FR4 at 1 GHz (KiCad's default for a new dielectric)
DEFAULT_LOSS_TANGENT = 0.02             # generic FR4 at 1 GHz (KiCad's default for a new dielectric)
DEFAULT_SPEC_FREQUENCY_HZ = 1e9         # the frequency er and tan d are given at (KiCad's default)
# The board file's values win over the defaults when present
USE_STACKUP_EPSILON_R = True
USE_STACKUP_LOSS_TANGENT = True
USE_STACKUP_SPEC_FREQUENCY = True       # (spec_frequency ...), KiCad's development version (format 20260511 on)

# --- How er and tan d change with frequency ---
#   "constant"          - the same at every frequency: what KESE writes today, and KiCad's default
#   "djordjevic_sarkar" - the wideband model usual for glass-epoxy laminates, fitted to er and tan d
#                         at the spec frequency; materials.json gets the fitted parameters
#   "table"             - DIELECTRIC_TABLE, written as given
DIELECTRIC_MODEL = "constant"
USE_STACKUP_DIELECTRIC_MODEL = True     # (dielectric_model constant / djordjevic_sarkar), as above
DS_LOW_FREQUENCY_HZ = 1e3               # Djordjevic-Sarkar: lower corner frequency
DS_HIGH_FREQUENCY_HZ = 1e12             # Djordjevic-Sarkar: upper corner frequency
# "table": ((frequency Hz, er, tan d), ...) by rising frequency.  Empty: "table" is then an error.
#   e.g. ((1e8, 4.6, 0.016), (1e9, 4.5, 0.02), (1e10, 4.4, 0.022))
DIELECTRIC_TABLE = ()

# --- Plies fused: a gap whose plies differ ---
#   "first"  - the first ply's material, er and tan d (top to bottom), as KESE has always done
#   "series" - the plies in series, as a field straight across the gap sees them:
#              h / er = sum(h_p / er_p), and tan d weighted the same way
FUSED_PROPERTIES = "first"

# --- The resin between the traces of the inner copper ---
# Plies fused:    it is part of the board solid beside it and has that solid's values, as KESE has
#                 always done; the three values below are not used.
# Plies separate: it is its own solid ("Board_resin In1.Cu"), with the values below: the prepreg's
#                 resin without its glass.  None for er or tan d takes that value from the prepreg
#                 ply the resin flowed from.
RESIN_MATERIAL = "resin"
RESIN_EPSILON_R = 3.5                   # best guess for FR-4 epoxy without glass: published figures give er 3.0
RESIN_LOSS_TANGENT = 0.02               #   to 3.57 and tan d 0.021 (E-glass: 6.2 and 0.002); no resin maker's sheet


# ==================================================================================================
# 5. Color (GLB, OBJ and STEP)
# ==================================================================================================
# sRGB hex colour, alpha 0-1 (below 1 is see-through), metallic 0-1, and roughness 0-1: how matte it
# looks in a viewer.
CORE_COLOR = {"color": "#968A58", "alpha": 1.0, "metallic": 0.0, "roughness": 0.80}
PREPREG_COLOR = {"color": "#A89C66", "alpha": 1.0, "metallic": 0.0, "roughness": 0.80}
# Plies separate: the resin between the traces of the inner copper
RESIN_COLOR = {"color": "#B8AC78", "alpha": 1.0, "metallic": 0.0, "roughness": 0.80}
# The whole laminate as one solid (DIELECTRIC_GROUPING = "merged"), and a ply of no type
BOARD_COLOR = {"color": "#968A58", "alpha": 1.0, "metallic": 0.0, "roughness": 0.80}
