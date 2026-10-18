"""
Silkscreen_Parameters.py - legend ink and text rendering.
"""

# Ink thickness in mm (typical 0.010-0.020)
SILK_THICKNESS_MM = 0.010

# Silkscreen where the solder mask is open (pads, exposed copper, bare laminate in openings):
#   False - no ink wherever there is no mask (what fabricators do: silk is clipped off the pads)
#   True  - keep the ink there too, as drawn in KiCad
SILKSCREEN_OVER_COPPER = False

# Font.  None -> KiCad's own stroke font (Parameters/Fonts/kicad_newstroke.json.gz).
# A path (relative to Parameters/Fonts) to a custom font: this project's stroke-font JSON,
# or a Hershey .jhf file.  If the file is missing the default is used and the report says so.
FONT_FILE = None

# Text in a TrueType face (KiCad 7+ (font (face "...")) is drawn with the stroke font above.
DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT = True

# KiCad text metrics (from KiCad's font code; change only to match a different font)
INTERLINE_PITCH = 1.68                  # line pitch as a multiple of the text height
INTERLINE_LEGACY_FACTOR = 0.9583        # KiCad's correction for stroke fonts
INTER_CHAR_SPACING = 0.2                # extra advance between glyphs, as a fraction of text width
ITALIC_TILT = 0.125                     # x shift per unit of y for italic text
BOLD_THICKNESS_RATIO = 0.2              # bold text stroke = this x text height when the file gives none
NORMAL_THICKNESS_RATIO = 0.15           # normal text stroke = this x text height when the file gives none
TEXT_STROKE_QUAD_SEGS = 4               # roundness of stroke ends

# Draw text that the file marks hidden (reference/value with (hide yes))
DRAW_HIDDEN_TEXT = False

# Silkscreen items on these layers are drawn.  Others (Fab, Courtyard, User) are listed as skipped.
SILK_LAYERS = ["F.SilkS", "B.SilkS"]
