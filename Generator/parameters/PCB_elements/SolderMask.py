"""
parameters/PCB_elements/SolderMask.py - the solder mask (LPI) on both faces.

KiCad's mask layers are NEGATIVE: whatever is drawn on F.Mask / B.Mask, plus every pad and
every untented via, is an OPENING.  The mask solid is  outline - openings - holes.

Whether the solder mask is built is in Stackup.py: the lines "top_solder_mask" and
"bottom_solder_mask".

Sections, as in every element's file:  1 Parts  2 Thickness  3 Shape  4 Material (for the solver)
5 Color (for the viewer)
"""

# ==================================================================================================
# 1. Parts
# ==================================================================================================
# "Top Solder Mask" and "Bottom Solder Mask", and in visual mode "Top Mask over Copper" and
# "Bottom Mask over Copper".  No setting here: Stackup.py says whether they are built.  Its two
# solder mask lines are False by default: the mask is many more solids, which make STEP files much
# bigger and slower to open, and most EM work leaves it out.


# ==================================================================================================
# 2. Thickness
# ==================================================================================================
# Thickness in mm.  LPI mask is thinner on top of copper than over bare laminate.
# Typical production: 0.010-0.015 over copper, 0.020-0.030 over laminate.
# The board file gives one value; it is used for both unless USE_STACKUP_MASK_THICKNESS is False.
MASK_OVER_LAMINATE_MM = 0.010
MASK_OVER_COPPER_MM = 0.010
USE_STACKUP_MASK_THICKNESS = True


# ==================================================================================================
# 3. Shape
# ==================================================================================================
# Via tenting (mask over the via):
#   "file"   - follow the board file (KiCad 9/10 tenting settings, older plot setting, else tented)
#   "tented" - cover every via with mask
#   "open"   - open the mask over every via
VIA_TENTING = "file"

# The mask (and the silkscreen on it) stop this far short of the board edge (fabs pull both back
# from routed edges).
# It also keeps <model-viewer> from hiding a translucent mask as a "baked shadow".
MASK_EDGE_PULLBACK_MM = 0.005

# Pad-to-mask clearance in mm, or None to follow the board file (pad / footprint / board setup)
PAD_TO_MASK_CLEARANCE_MM = None

# Solder mask minimum web width in mm, or None to follow the board file (setup (solder_mask_min_width)).
# As KiCad plots the mask (and the fab makes it), openings closer than this are joined: no strip of
# mask narrower than this stays between them.  0 = keep every web.
MASK_MIN_WIDTH_MM = None
MASK_WEB_HAIRLINE_MM = 1e-3             # a web the minimum width adds that is narrower than twice this is dropped

# A piece of mask on top of copper narrower than twice this is left out: where an opening's outline
# follows the copper's (a pad with no mask margin) with other points along its curves, or a grid step
# off, the mask on the copper keeps slivers far thinner than a micrometre that no fab makes.  The finish
# covers them instead.
MASK_OVER_COPPER_HAIRLINE_MM = 1e-3

# A mask opening narrower than twice this everywhere is left out, the mask kept over it: an opening of a
# pad a micrometre across (some boards place hundreds, as markers) is no opening a fab makes, and the
# mask's edges around such a speck at a pad's corner come out a few tenths of a micrometre into the copper.
MASK_OPENING_HAIRLINE_MM = 1e-3

# Curve quality of the little walls where the mask climbs over a trace (segments per quarter circle)
MASK_WALL_QUAD_SEGS = 4


# ==================================================================================================
# 4. Material (written to materials.json for the solver; it changes no geometry)
# ==================================================================================================
MASK_MATERIAL = "LPI"                   # liquid photoimageable mask
MASK_EPSILON_R = 3.8                    # generic LPI mask: JLCPCB gives 3.8, OSH Park 3.9 (KiCad's own default is 3.3)
MASK_LOSS_TANGENT = 0.03                # generic LPI mask: Taiyo PSR-4000BN 0.029 at 1 MHz, OSH Park 0.033
USE_STACKUP_MASK_MATERIAL = True        # each mask layer's (material), (epsilon_r), (loss_tangent) in the file win


# ==================================================================================================
# 5. Color (GLB, OBJ and STEP)
# ==================================================================================================
# sRGB hex colour, alpha 0-1 (below 1 is see-through), metallic 0-1, and roughness 0-1: how matte it
# looks in a viewer.
TOP_MASK_COLOR = {"color": "#EBEBE6", "alpha": 0.80, "metallic": 0.0, "roughness": 0.30}
BOTTOM_MASK_COLOR = {"color": "#EBEBE6", "alpha": 0.80, "metallic": 0.0, "roughness": 0.30}
# Visual mode: the mask where it lies on top of copper (traces read through real mask)
TOP_MASK_OVER_COPPER_COLOR = {"color": "#F2EFD8", "alpha": 1.0, "metallic": 0.0, "roughness": 0.30}
BOTTOM_MASK_OVER_COPPER_COLOR = {"color": "#F2EFD8", "alpha": 1.0, "metallic": 0.0, "roughness": 0.30}

# In "visual" mode the mask is opaque regardless of the alpha above (it is a surface, not a solid)
VISUAL_MASK_OPAQUE = True

# Honour the mask colour named in the board file ((layer "F.Mask" ... (color "Green"))) using the
# tables below; False = always the colours above.
USE_STACKUP_MASK_COLOR = True
STACKUP_MASK_COLORS = {
    "green": "#126830", "red": "#A01414", "blue": "#14328C", "black": "#121214", "white": "#EBEBE6",
    "yellow": "#D2B414", "purple": "#501E6E", "matte green": "#1E5A2D", "matte black": "#191919",
    "matte blue": "#19326E", "matte red": "#8C1919",
}
# When the board file's mask colour is used in visual mode, the mask-over-copper colour is this one
# instead; a colour name missing here keeps the colour above.
STACKUP_MASK_OVER_COPPER_COLORS = {
    "green": "#3F8F3A", "red": "#C8503C", "blue": "#3C5AB4", "black": "#2E2E30", "white": "#F2EFD8",
    "yellow": "#E6CC50", "purple": "#7A4696", "matte green": "#4A7D4A", "matte black": "#343434",
    "matte blue": "#3C5A96", "matte red": "#AA4646",
}
# A user-defined colour in the board file (Board Setup's "User defined", written as #RRGGBBAA) is used as it is,
# with the alpha above; in visual mode the mask over copper is that colour mixed this much of the way
# toward white (0 = the same colour, 1 = white)
USER_MASK_OVER_COPPER_LIGHTEN = 0.15
