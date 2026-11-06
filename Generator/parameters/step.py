"""
parameters/step.py - the STEP files: true arcs and cylinders, and what counts as an arc.

Every value here is recorded in parameters.txt next to each output.  The file's units are
Run.UNITS; STEP is written only when Run.FILE_FORMAT holds "step".  How many rows the writer turns
into text at once is Parallel.STEP_ROWS_AT_A_TIME.
"""

# Every part is written as the closed solid stage 6 built, one body per connected piece, with its
# flat faces and walls as they are (curves are polygons, as in the meshes), unless STEP_EXACT_ARCS.
#
# STEP_EXACT_ARCS - write circles and arcs as true curves (KESE's own STEP writer, no CAD kernel).
#   Where the outline of a part runs through vertices that lie on one circle (holes, vias, round
#   pads, track ends, arc tracks, round outlines), their chords become one CIRCLE edge and the walls
#   on them one CYLINDRICAL_SURFACE face, at every height alike, except where another edge at that
#   height passes closer to the vertices than the arc bulges out from them (a sliver of a few µm),
#   which the arc would cross.  Smaller files and true cylinders for CAD and EM solvers; every
#   other edge stays a line and every other face a plane.  Meshes (GLB / STL / OBJ) are unchanged.
STEP_EXACT_ARCS = True
STEP_ARC_FIT_TOLERANCE_MM = 0.0002     # vertices within this of one circle form an arc (2 x the snap grid)
STEP_ARC_MIN_POINTS = 5                # at least this many vertices in a run
STEP_ARC_MIN_SWEEP_DEG = 10.0          # and turning at least this far
STEP_ARC_MAX_TURN_DEG = 30.0           # but at most this far at one vertex: a polygon with fewer than 12
                                       # sides (an octagonal pad, a square) is a polygon, not a circle
STEP_ARC_TURN_RATIO_MAX = 1.3          # and evenly: no chord spans more than this many times the median
STEP_ARC_TURN_RATIO_MIN = 0.7          # chord's angle about the centre, and none but the first and last
                                       # less than this many times (those two may be shorter, where a
                                       # boolean cut the arc)
STEP_ARC_MAX_SWEEP_DEG = 181.0         # a longer arc is cut in pieces at vertices spread evenly; a whole
                                       # circle is two arcs on one circle, or more below 180
#
# Which parts are made, in every format and mode alike, is set by one switch per kind of part:
#   Board.BOARD_ENABLED, Copper.COPPER_ENABLED (copper and plated barrels), Finish.FINISH_ENABLED,
#   SolderMask.SOLDER_MASK_ENABLED, Silkscreen.SILKSCREEN_ENABLED; mask and silk are off by default.
#   STEP with mask and silk is bigger (the PCIe card in Input/, in mm: 151 MB and 1,024 solids written
#   in 2.9 s, against 81 MB and 788 solids in 1.9 s without them).
