The pictures in the web tool's tips (WebUI/tips.json "pictures").  build_site.py copies them to the site's
WebUI/tooltips/ folder; a tip loads its picture only when it opens.

Each one is a single panel cut from a wiki picture in docs/images, at most 680 px on its longer side (twice the
tip's width), saved as WebP at quality 82.  The box is in the source picture's pixels (left, top, right, bottom).
A remade picture keeps its file name, so tips.json needs no change; update its w and h there if its size changes.

Nineteen are drawn for the tip instead ("drawn" below), where the wiki picture's text or colours were too small to read
at tip size: text 20 to 24 px (10 to 12 px in the tip), KESE's own colours (parameters/color.py), silkscreen in
KiCad's stroke font.
Their SVG sources are in drawn/; each is rendered at its own size (684 px wide) and saved as WebP at quality 82.

modes.webp  684x236     6 KB  drawn for the tip: drawn/modes.svg (the two modes, cut through)
modes_visual.webp  680x463    15 KB  from modes_1_simulation_visual.webp, box (1077, 178, 2116, 885)
frames.webp  684x286     6 KB  drawn for the tip: drawn/frames.svg (the two origins)
orient.webp  684x312     7 KB  drawn for the tip: drawn/orient.svg (the two orientations)
stackup.webp  684x296    12 KB  drawn for the tip: drawn/stackup.svg (a 4-layer stack-up)
dielectrics.webp  684x286     9 KB  drawn for the tip: drawn/dielectrics.svg (the two Dielectric Grouping choices)
resin.webp  680x195     6 KB  from copper_5_thickness.webp, box (1101, 725, 2114, 1015)
npth.webp  680x456    14 KB  from board_1_outline.webp, box (1080, 1771, 2116, 2466)
outline.webp  684x286     8 KB  drawn for the tip: drawn/outline.svg (ends joined and left open)
net_solid.webp  684x214     7 KB  drawn for the tip: drawn/net_solid.svg (the three groupings)
foil.webp  680x195     4 KB  from copper_5_thickness.webp, box (26, 725, 1039, 1015)
plating.webp  684x282    11 KB  drawn for the tip: drawn/plating.svg (Outer Plating Added 0 and 0.020 mm)
pth_wall.webp  680x253     6 KB  from copper_6_plating.webp, box (26, 209, 1060, 594)
via.webp  684x286     7 KB  drawn for the tip: drawn/via.svg (drill, bore and wall)
etch.webp  684x250     4 KB  drawn for the tip: drawn/etch.svg (Etch Factor 0 and 0.5)
castell.webp  684x288     8 KB  drawn for the tip: drawn/castell.svg (a plated and a bare notch)
castell_wall.webp  680x432     9 KB  from copper_7_castellation.webp, box (0, 1127, 1265, 1931)
edge.webp  684x296     8 KB  drawn for the tip: drawn/edge.svg (a plated and a bare edge)
edge_wall.webp  585x680    14 KB  from copper_8_edge_plating.webp, box (1379, 119, 2054, 904)
edge_net.webp  684x306    11 KB  drawn for the tip: drawn/edge_net.svg (the band's net)
tenting.webp  680x465    16 KB  from mask_6_over_holes.webp, box (968, 95, 2116, 880)
mask.webp  680x432    19 KB  from mask_3_conformal.webp, box (968, 95, 2116, 825)
mask_thick.webp  680x414    11 KB  from mask_4_thickness.webp, box (24, 1087, 1060, 1717)
pullback.webp  680x386    10 KB  from mask_5_edge_pullback.webp, box (968, 927, 2116, 1579)
mask_colors.webp  684x366    17 KB  drawn for the tip: drawn/mask_colors.svg (KESE's mask colours, a trace and gold pads)
silk_colors.webp  684x366    27 KB  drawn for the tip: drawn/silk_colors.svg (KESE's colours and KiCad's stroke font)
silk_height.webp  684x294     8 KB  drawn for the tip: drawn/silk_height.svg (the ink on the mask)
silk_copper.webp  680x483    14 KB  from silk_4_mask_subtract.webp, box (24, 143, 1141, 937)
silk_text.webp  684x284     8 KB  drawn for the tip: drawn/silk_text.svg (the line pitch)
silk_join.webp  684x270     9 KB  drawn for the tip: drawn/silk_join.svg (1, 2 and 4 segments per quarter circle)
finish_where.webp  684x278     9 KB  drawn for the tip: drawn/finish_where.svg (the finish on and off)
finish_enig.webp  680x379    16 KB  from finish_2_enig.webp, box (26, 200, 1063, 778)
stage6.webp  680x205    14 KB  from wp_2_solid.webp, box (26, 162, 2116, 792)
checked.webp  675x632    30 KB  from wp_2_solid.webp, box (1441, 837, 2116, 1469)
