"""
SolderMask_Parameters.py - the solder mask (LPI) on both faces.

KiCad's mask layers are NEGATIVE: whatever is drawn on F.Mask / B.Mask, plus every pad and
every untented via, is an OPENING.  The mask solid is  outline - openings - holes.
"""

# Thickness in mm.  LPI mask is thinner on top of copper than over bare laminate.
# Typical production: 0.010-0.015 over copper, 0.020-0.030 over laminate.
# KiCad's stackup gives one value; it is used for both unless USE_STACKUP_MASK_THICKNESS is False.
MASK_OVER_LAMINATE_MM = 0.010
MASK_OVER_COPPER_MM = 0.010
USE_STACKUP_MASK_THICKNESS = True

# The mask (and the silkscreen on it) stop this far short of the board edge (fabs pull both back
# from routed edges).
# It also keeps <model-viewer> from hiding a translucent mask as a "baked shadow".
MASK_EDGE_PULLBACK_MM = 0.005

# Pad-to-mask clearance in mm, or None to follow the board file (pad / footprint / board setup)
PAD_TO_MASK_CLEARANCE_MM = None

# Curve quality of the little walls where the mask climbs over a trace (segments per quarter circle)
MASK_WALL_QUAD_SEGS = 4
