"""
parameters/PCB_elements/SilkScreen.py - the silkscreen: legend ink and text rendering.

Whether the silkscreen is built is in Stackup.py: the lines "top_silkscreen" and
"bottom_silkscreen".

Sections, as in every element's file:  1 Parts  2 Thickness  3 Shape  4 Material (for the solver)
5 Color (for the viewer)
"""

# ==================================================================================================
# 1. Parts
# ==================================================================================================
# "Top Silkscreen" and "Bottom Silkscreen".  Stackup.py says whether they are built; its two
# silkscreen lines are False by default, like the solder mask's.

# Silkscreen items on these layers are drawn.  Others (Fab, Courtyard, User) are listed as skipped.
SILK_LAYERS = ["F.SilkS", "B.SilkS"]

# Draw text that the file marks hidden (reference/value with (hide yes))
DRAW_HIDDEN_TEXT = False


# ==================================================================================================
# 2. Thickness
# ==================================================================================================
# Ink thickness in mm (typical 0.010-0.020)
SILK_THICKNESS_MM = 0.010


# ==================================================================================================
# 3. Shape
# ==================================================================================================
# Silkscreen where the solder mask is open (pads, exposed copper, bare laminate in openings):
#   False - no ink wherever there is no mask (what fabricators do: silk is clipped off the pads)
#   True  - keep the ink there too, as drawn in KiCad
SILKSCREEN_OVER_COPPER = False

# Font.  None -> KiCad's own stroke font (kese/assets/fonts/kicad_newstroke.json.gz).
# A path (relative to kese/assets/fonts) to a custom font: this project's stroke-font JSON,
# or a Hershey .jhf file.  If the file is missing the default is used and the report says so.
FONT_FILE = None

# Text in a TrueType face (KiCad 7+ (font (face "..."))) is drawn from the letters KiCad saves with it
# (its render cache), so no font file is needed.  Text with no cache, or one made for other words or
# another angle, is drawn with the stroke font above when True (with a warning), and left out when False.
DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT = True

# KiCad text metrics (from KiCad's font code; change only to match a different font)
INTERLINE_PITCH = 1.68                  # line pitch as a multiple of the text height
INTERLINE_LEGACY_FACTOR = 0.9583        # KiCad's correction for stroke fonts
ITALIC_TILT = 0.125                     # x shift per unit of y for italic text
BOLD_THICKNESS_RATIO = 0.2              # bold text stroke = this x text width when the file gives none
NORMAL_THICKNESS_RATIO = 0.125          # normal text stroke = this x text width when the file gives none
MAX_PEN_RATIO = 0.25                    # a stroke is at most this x the text's smaller size (ClampTextPenSize)
TEXT_STROKE_QUAD_SEGS = 4               # roundness of stroke ends


# ==================================================================================================
# 4. Material (written to materials.json for the solver; it changes no geometry)
# ==================================================================================================
# The board file gives no material for silkscreen (KiCad's own default er is 1.0, as if it were air).
SILK_MATERIAL = "epoxy ink"
SILK_EPSILON_R = 5.0                    # best guess for white ink: its pigment lifts er above the mask's 3.8
SILK_LOSS_TANGENT = 0.03                # best guess: the solder mask's value
# Neither is a maker's figure: no legend ink data sheet with er and tan d has been read yet.


# ==================================================================================================
# 5. Color (GLB, OBJ and STEP)
# ==================================================================================================
# sRGB hex colour, alpha 0-1 (below 1 is see-through), metallic 0-1, and roughness 0-1: how matte it
# looks in a viewer.
TOP_SILK_COLOR = {"color": "#141414", "alpha": 1.0, "metallic": 0.0, "roughness": 0.75}
BOTTOM_SILK_COLOR = {"color": "#141414", "alpha": 1.0, "metallic": 0.0, "roughness": 0.75}

# Honour the silkscreen colour named in the board file ((layer "F.SilkS" ... (color "White")))
# using the table below; a user-defined #RRGGBBAA colour is used as it is.  False = always the colours above.
USE_STACKUP_SILK_COLOR = True
STACKUP_SILK_COLORS = {
    "white": "#F0F0EC", "black": "#141414", "yellow": "#E6C828",
    "green": "#126830", "red": "#A01414", "blue": "#14328C", "purple": "#501E6E",
}
