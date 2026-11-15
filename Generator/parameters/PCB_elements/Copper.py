"""
parameters/PCB_elements/Copper.py - the copper: the top, inner and bottom copper layers, the plated
holes, the vias and the plated board edge.

Values marked "typical" are common rigid-FR4 production values; replace them with your
fabricator's datasheet numbers for lab work.

Whether the copper is built is in Stackup.py: the lines "top_copper", "inner_copper" and
"bottom_copper" (sections 2 to 4), "plated_holes" (section 5: the plated walls of the holes, the
copper in filled vias and the plated edge) and "via_resin" (the resin in plugged and resin-filled
vias).

Sections:  1 All copper  2 Top copper  3 Inner copper  4 Bottom copper
           5 Plated holes, vias and the board edge  6 Material (for the solver)  7 Color (for the viewer)
"""

# ==================================================================================================
# 1. All copper
# ==================================================================================================
# Copper grouping in "simulation" mode:
#   "net"    - one solid per net (all its layers and vias joined)  <- what EM ports need
#   "layer"  - one solid per copper layer, plating separate
#   "merged" - all copper in one solid
COPPER_GROUPING = "net"

# Name used for copper that belongs to no net (board graphics, unconnected pads)
NO_NET_NAME = "no_net"

# WARNING - copper zones (ground planes, fills): KESE takes the fill polygons that KiCad stores in
# the board file. KiCad only writes them after the zones have been filled (press B) and the file
# saved. A zone with no stored fill is IGNORED entirely - no copper is made for it and report.txt
# counts it under "zones with no fill". Fill the zones in KiCad and save before exporting.

# The foil thickness of a layer comes from the board file ((layer "F.Cu" (thickness ...))) when it
# gives one; the DEFAULT_*_FOIL_MM values of sections 2 to 4 are used when it gives none.  False:
# always the values of sections 2 to 4.
USE_STACKUP_COPPER_THICKNESS = True

# Etch factor (TOP_, INNER_ and BOTTOM_ETCH_FACTOR below): real traces are trapezoids, narrower at
# the free face than at the foot.
#   0.0  -> rectangular cross-section (default, matches KiCad)
#   e.g. 0.5 -> each side wall leans in by 0.5 x copper thickness over the copper height
ETCH_STEPS = 4                          # the trapezoid is built as this many stacked slices
ETCH_UNETCHED_REACH = 1.5               # copper within this x the inset of a hole wall or board edge keeps its outline

# A hole in one net's copper narrower than this on average (2 x area / perimeter) is no hole: it is
# filled (the gap KiCad leaves between a zone fill and a pad it meets, a hair wide)
HAIRLINE_HOLE_MM = 1e-3

# KiCad's "remove unused layers" on vias and through-hole pads: drop annular rings on layers nothing connects to
HONOUR_REMOVE_UNUSED_LAYERS = True


# ==================================================================================================
# 2. Top copper (F.Cu)
# ==================================================================================================
# Base foil thickness in mm when the board file gives none (1 oz = 0.035 mm, 0.5 oz = 0.0175 mm)
DEFAULT_TOP_FOIL_MM = 0.035

# Electroplating adds copper to the outer layers during hole plating (the "finished copper").
# Finished top copper = foil + this value.  Typical 0.020 mm.  0 = foil only (what KiCad models).
TOP_PLATING_ADDED_MM = 0.0

# Etch factor of the top copper, as in section 1; its foot is on the laminate.
TOP_ETCH_FACTOR = 0.0


# ==================================================================================================
# 3. Inner copper (In1.Cu, In2.Cu, ...)
# ==================================================================================================
# Base foil thickness in mm when the board file gives none.  Inner copper gets no plating.
DEFAULT_INNER_FOIL_MM = 0.035

# Etch factor of the inner copper, as in section 1.  Inner copper is etched on its core: its foot is
# on the side toward the board's centre.
INNER_ETCH_FACTOR = 0.0


# ==================================================================================================
# 4. Bottom copper (B.Cu)
# ==================================================================================================
# Base foil thickness in mm when the board file gives none
DEFAULT_BOTTOM_FOIL_MM = 0.035

# Finished bottom copper = foil + this value, as for the top copper
BOTTOM_PLATING_ADDED_MM = 0.0

# Etch factor of the bottom copper, as in section 1; its foot is on the laminate.
BOTTOM_ETCH_FACTOR = 0.0


# ==================================================================================================
# 5. Plated holes, vias and the board edge
# ==================================================================================================
# Hole wall plating
VIA_WALL_MM = 0.025                     # plated wall thickness of vias (typical 0.020-0.025)
PTH_WALL_MM = 0.025                     # plated wall thickness of through-hole pads

# Castellated holes: plated holes that the board edge cuts through (module edge connectors).
# KiCad has a per-pad "Castellated pad" fabrication property, but KESE does not read it: here a
# castellation is a plated hole whose drill crosses Edge.Cuts.
#   "auto" - every plated hole crossing the outline is a castellation: the drill notches the
#            edge and its plating is a part-barrel on the notch wall, joined to the hole's net
#   "file" - as "auto", but only when the board file says (castellated_pads yes)
#   "off"  - holes crossing the edge are not plated at all (the notch stays bare)
CASTELLATION = "auto"
CASTELLATION_WALL_MM = 0.025            # plated wall thickness of a castellation (typical 0.020-0.025)

# Edge plating: copper on the whole routed board edge (edge-card connectors, RF shielding)
#   "file" - follow the board file's flag (edge_plating yes), "yes", "no"
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
#   "resin"  - the via resin (a non-conductive fill), flush with the outer copper
VIA_FILL = "copper"
# How far the resin of a plugged via (Types III and IV) goes into the hole from its side, as a share
# of the hole's length.  IPC-4761 says only "partial penetration", so 0.5 is KESE's choice: plugged
# from both sides, the two plugs meet.
VIA_PLUG_DEPTH_FRACTION = 0.5


# ==================================================================================================
# 6. Material (written to materials.json for the solver; it changes no geometry)
# ==================================================================================================
# --- Copper: foils, plating, barrels, castellations and edge plating ---
COPPER_MATERIAL = "copper"
COPPER_CONDUCTIVITY_S_PER_M = 5.8e7     # annealed copper at 20 C
# Surface roughness, for the solver's conductor loss.  Each copper layer has two faces: the treated
# face, pressed into the dielectric the foil was laminated on (the lower face of the top copper, the
# upper face of the bottom copper, the face of an inner layer that lies on its core), and the other
# face.
#   "huray"      - the "snowball" model: nodule radius and surface ratio per face
#   "hammerstad" - one RMS height per face
#   "none"       - smooth (KESE up to version 3.3): the conductor loss comes out too low above about 1 GHz
# The Huray values below are the ones Ansys's tools start with on every face (the layer defaults of
# PyEDB: nodule radius 0.5 um, Hall-Huray surface ratio 2.9).  They describe no particular foil:
# replace them with your foil's values for lab work.
COPPER_ROUGHNESS_MODEL = "huray"
COPPER_HURAY_RADIUS_TREATED_UM = 0.5    # "huray": nodule radius
COPPER_HURAY_RADIUS_OTHER_UM = 0.5
COPPER_HURAY_SURFACE_RATIO_TREATED = 2.9  # "huray": nodule surface over flat surface (Hall-Huray surface ratio)
COPPER_HURAY_SURFACE_RATIO_OTHER = 2.9
COPPER_ROUGHNESS_RMS_TREATED_UM = 0.0   # "hammerstad": RMS height.  Foil makers quote Rz (peak to valley), which
COPPER_ROUGHNESS_RMS_OTHER_UM = 0.0     #   is larger: standard foil 3 to 6 um, RTF 1 to 1.5, VLP and HVLP 0.3 to 1 (JLCPCB)

# --- Via resin: plugged and resin-filled vias ---
# San-Ei Kagaku PHP-900 IR-6P, a permanent hole plugging ink, from its technical specifications
# (sold by Umicore): Dk 4.4 and Df 0.02 at 1 GHz (ASTM D2520).
VIA_RESIN_MATERIAL = "via resin"
VIA_RESIN_EPSILON_R = 4.4
VIA_RESIN_LOSS_TANGENT = 0.02


# ==================================================================================================
# 7. Color (GLB, OBJ and STEP)
# ==================================================================================================
# sRGB hex colour, alpha 0-1 (below 1 is see-through), metallic 0-1, and roughness 0-1: how matte it
# looks in a viewer (not the copper's surface roughness above).  A net's copper is one solid across
# its layers, so the top, inner and bottom copper share one colour.
COPPER_COLOR = {"color": "#CD803E", "alpha": 1.0, "metallic": 0.9, "roughness": 0.35}
# The plated walls of the holes, where they are a part of their own (COPPER_GROUPING = "layer")
PLATING_COLOR = {"color": "#CD803E", "alpha": 1.0, "metallic": 0.9, "roughness": 0.35}
# Visual mode: all the copper that shows
EXPOSED_COPPER_COLOR = {"color": "#DEBA60", "alpha": 1.0, "metallic": 1.0, "roughness": 0.25}
VIA_RESIN_COLOR = {"color": "#D8CFA0", "alpha": 1.0, "metallic": 0.0, "roughness": 0.60}
