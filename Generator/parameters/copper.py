"""
parameters/copper.py - copper foils, plating, vias and the finished copper geometry.

Values marked "typical" are common rigid-FR4 production values; replace them with your
fabricator's datasheet numbers for lab work.
"""

# Copper grouping in "simulation" mode:
#   "net"    - one solid per net (all its layers and vias joined)  <- what EM ports need
#   "layer"  - one solid per copper layer, plating separate
#   "merged" - all copper in one solid
COPPER_GROUPING = "net"

# Build the copper (layers and the plated barrels of holes and vias) and write it to every output file.
COPPER_ENABLED = True

# WARNING - copper zones (ground planes, fills): KESE takes the fill polygons that KiCad stores in
# the board file. KiCad only writes them after the zones have been filled (press B) and the file
# saved. A zone with no stored fill is IGNORED entirely - no copper is made for it and report.txt
# counts it under "zones with no fill". Fill the zones in KiCad and save before exporting.

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
ETCH_UNETCHED_REACH = 1.5               # copper within this x the inset of a hole wall or board edge keeps its outline

# A hole in one net's copper narrower than this on average (2 x area / perimeter) is no hole: it is
# filled (the gap KiCad leaves between a zone fill and a pad it meets, a hair wide)
HAIRLINE_HOLE_MM = 1e-3

# Castellated holes: plated holes that the board edge cuts through (module edge connectors).
# KiCad has a per-pad "Castellated pad" fabrication property, but KESE does not read it: here a
# castellation is a plated hole whose drill crosses Edge.Cuts.
#   "auto" - every plated hole crossing the outline is a castellation: the drill notches the
#            edge and its plating is a part-barrel on the notch wall, joined to the hole's net
#   "file" - as "auto", but only when the board's stackup says (castellated_pads yes)
#   "off"  - holes crossing the edge are not plated at all (the notch stays bare)
CASTELLATION = "auto"
CASTELLATION_WALL_MM = 0.025            # plated wall thickness of a castellation (typical 0.020-0.025)

# Edge plating: copper on the whole routed board edge (edge-card connectors, RF shielding)
#   "file" - follow the board's stackup flag (edge_plating yes), "yes", "no"
# The plating is a band EDGE_PLATING_WALL_MM wide inside the outline, from the bottom of B.Cu
# to the top of F.Cu, interrupted by every hole and castellation that crosses the edge.
EDGE_PLATING = "file"
EDGE_PLATING_WALL_MM = 0.025
# Which net the edge copper belongs to:
#   "auto" - the named net with the most copper touching the edge band (NO_NET_NAME if none)
#   a net name, e.g. "GND"
# Copper of any other net inside the band is given to the edge net (edge plating shorts
# everything that reaches the edge); report.txt lists what was moved.
EDGE_PLATING_NET = "auto"

# Via tenting (mask over the via):
#   "file"   - follow the board file (KiCad 9/10 tenting settings, older plot setting, else tented)
#   "tented" - cover every via with mask
#   "open"   - open the mask over every via
VIA_TENTING = "file"

# KiCad 10's via protection (IPC-4761): covering, plugging, filling and capping, as the via says or,
# where it leaves them to the board, as the board's setup says.
#   "file" - as the board file says
#   "off"  - every via stays open, as before KiCad 10 (report.txt counts them under "skipped")
# Covering closes the hole under the solder mask on its side: the mask spans the hole.  Capping
# plates over the filled hole: the outer copper is not cut by it.  An end that a backdrill, counterbore
# or countersink opens stays open.
VIA_PROTECTION = "file"
# What a filled via (IPC-4761 Types V to VII) is filled with, the whole hole inside the plating.
# KiCad's documentation calls the fill conductive, "typically copper or conductive paste":
#   "copper" - copper, part of the via's net (and the outer copper is not cut by the hole)
#   "resin"  - the resin below (a non-conductive fill), flush with the outer copper
VIA_FILL = "copper"
# How far the resin of a plugged via (Types III and IV) goes into the hole from its side, as a share
# of the hole's length.  IPC-4761 says only "partial penetration", so 0.5 is KESE's choice: plugged
# from both sides, the two plugs meet.
VIA_PLUG_DEPTH_FRACTION = 0.5
# The resin of plugged and resin-filled vias: San-Ei Kagaku PHP-900 IR-6P, a permanent hole plugging
# ink, from its technical specifications (sold by Umicore): Dk 4.4 and Df 0.02 at 1 GHz (ASTM D2520).
VIA_RESIN_EPSILON_R = 4.4
VIA_RESIN_LOSS_TANGENT = 0.02
# Build the resin of plugged and resin-filled vias and write it to every output file.
VIA_RESIN_ENABLED = True

# KiCad's "remove unused layers" on vias and through-hole pads: drop annular rings on layers nothing connects to
HONOUR_REMOVE_UNUSED_LAYERS = True

# Electrical properties (written to materials.json for the solver)
COPPER_CONDUCTIVITY_S_PER_M = 5.8e7
COPPER_SURFACE_ROUGHNESS_UM = 0.0       # 0 = ignore; e.g. 1.5 for standard foil (solver setting, not geometry)

# Name used for copper that belongs to no net (board graphics, unconnected pads)
NO_NET_NAME = "no_net"
