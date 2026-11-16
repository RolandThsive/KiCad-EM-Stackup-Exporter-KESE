Pictures for the wiki (docs/wiki/) and the main README, one folder for each wiki page that shows
pictures, named as the page: the page's file name in docs/wiki/ without .md, which is also its
address in the wiki (Time-Distribution/ for Time-Distribution.md). README/ holds the main
README's. A picture two pages show is kept once, in the folder of the page it was made for:
Colorizing shows the colour pictures of Solder-Masks/ and Silkscreens/, and Examples the colour
boxes of Colorizing/ColorSwatches/.

Name them <page prefix>_<number>_<short name>.webp, for example copper_2_via_section.webp,
mask_1_openings.webp or readme_1_feature_test_boards.webp; the pictures of a board go in a folder
named after the board (Examples/rf_module/, Feature-Test-Collection/11_zones/). Every picture is
a lossless WebP, and an animation an animated WebP, such as start_1_simulation.webp. The wiki
refers to its pictures by their raw URL on main
(https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/<page>/<name>),
so they show in the wiki only after they are on main. The main README refers to its pictures by
their path in the repository.

One colour per copper layer or per net everywhere, true-to-scale line widths, 200 dpi,
board or outline edges as thick black lines.

The test boards of the Elmer and openEMS pages (Elmer-FEM-Test-Boards/, OpenEMS-Implementation-
Test-Boards/) are drawn in the Sinusoidal Coil Generator's own style instead: the coil boards by its
RepresentativeSVGMaker.py (the stator beside the rotor, Top red, Inner 1 green, Inner 2 yellow,
Bottom blue, copper under Top drawn wider so that it shows as an edge, the vias as dots), and E01,
E02 and O01 in the same colours, from above beside a section through the board, rendered at 2240
pixels wide.
