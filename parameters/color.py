"""
parameters/color.py - the look of every part, for glb / obj output.

Each material: colour as an sRGB hex string, alpha 0-1, metallic 0-1, roughness 0-1.
alpha < 1 writes a glTF BLEND material.  Properties for solvers (er, conductivity...)
live in parameters/board.py, copper.py and finish.py, not here.
"""

MATERIALS = {
    # dielectric laminate
    "Board":              {"color": "#968A58", "alpha": 1.0,  "metallic": 0.0, "roughness": 0.80},
    "Board_core":         {"color": "#968A58", "alpha": 1.0,  "metallic": 0.0, "roughness": 0.80},
    "Board_prepreg":      {"color": "#A89C66", "alpha": 1.0,  "metallic": 0.0, "roughness": 0.80},
    # copper
    "Copper":             {"color": "#CD803E", "alpha": 1.0,  "metallic": 0.9, "roughness": 0.35},
    "Copper_exposed":     {"color": "#DEBA60", "alpha": 1.0,  "metallic": 1.0, "roughness": 0.25},
    "Plating":            {"color": "#CD803E", "alpha": 1.0,  "metallic": 0.9, "roughness": 0.35},
    # solder mask
    "Top Solder Mask":    {"color": "#126830", "alpha": 0.80, "metallic": 0.0, "roughness": 0.30},
    "Bottom Solder Mask": {"color": "#126830", "alpha": 0.80, "metallic": 0.0, "roughness": 0.30},
    # visual mode: the mask where it lies on top of copper (traces read through real mask)
    "Top Mask over Copper":    {"color": "#3F8F3A", "alpha": 1.0, "metallic": 0.0, "roughness": 0.30},
    "Bottom Mask over Copper": {"color": "#3F8F3A", "alpha": 1.0, "metallic": 0.0, "roughness": 0.30},
    # silkscreen
    "Top Silkscreen":     {"color": "#F0F0EC", "alpha": 1.0,  "metallic": 0.0, "roughness": 0.75},
    "Bottom Silkscreen":  {"color": "#F0F0EC", "alpha": 1.0,  "metallic": 0.0, "roughness": 0.75},
    # surface finish metals
    "Nickel":             {"color": "#B8B8B0", "alpha": 1.0,  "metallic": 1.0, "roughness": 0.40},
    "Gold":               {"color": "#E6C15A", "alpha": 1.0,  "metallic": 1.0, "roughness": 0.20},
    "Tin":                {"color": "#C9C9C9", "alpha": 1.0,  "metallic": 1.0, "roughness": 0.45},
    "Silver":             {"color": "#E4E4E0", "alpha": 1.0,  "metallic": 1.0, "roughness": 0.25},
    # ENEPIG's palladium: sRGB (223, 218, 212), the base colour in Adobe's Substance metal references
    "Palladium":          {"color": "#DFDAD4", "alpha": 1.0,  "metallic": 1.0, "roughness": 0.30},
    "OSP":                {"color": "#D9955A", "alpha": 1.0,  "metallic": 0.8, "roughness": 0.35},
}

# In "visual" mode the mask is opaque regardless of the alpha above (it is a surface, not a solid)
VISUAL_MASK_OPAQUE = True

# Honour the colour names in the board's stackup ((layer "F.Mask" ... (color "Green"))) using the
# tables below; False = always use MATERIALS.
USE_STACKUP_COLORS = True

STACKUP_MASK_COLORS = {
    "green": "#126830", "red": "#A01414", "blue": "#14328C", "black": "#121214", "white": "#EBEBE6",
    "yellow": "#D2B414", "purple": "#501E6E", "matte green": "#1E5A2D", "matte black": "#191919",
    "matte blue": "#19326E", "matte red": "#8C1919",
}
STACKUP_SILK_COLORS = {
    "white": "#F0F0EC", "black": "#141414", "yellow": "#E6C828",
}
# When the stackup mask colour is used in visual mode, the mask-over-copper colour is this one
# instead; set to None to keep the MATERIALS entry.
STACKUP_MASK_OVER_COPPER_COLORS = {
    "green": "#3F8F3A", "red": "#C8503C", "blue": "#3C5AB4", "black": "#2E2E30", "white": "#F2EFD8",
    "yellow": "#E6CC50", "purple": "#7A4696", "matte green": "#4A7D4A", "matte black": "#343434",
    "matte blue": "#3C5A96", "matte red": "#AA4646",
}
