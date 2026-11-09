Pictures of the feature test boards of featureTest/, one folder per board, named after its
.kicad_pcb file. The wiki's Feature Test Collection page shows them by their raw URL on main
(https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Feature-Test-Collection/<board>/<name>),
so they show in the wiki only after they are on main. The timing charts on that page are beside
these folders: feature_<board>.webp for each board, and feature_0_all_boards.webp for all of them.

Each picture is the board's visual-mode GLB drawn with three.js through an orthographic camera,
saved as a lossless WebP: top_straight_visual.webp looks straight down at the top, bottom_straight_visual.webp
straight up at the bottom, as the board is seen when turned over left to right. Boards whose
stack-up names no mask colour are drawn with a green mask and white silkscreen
(Color.STACKUP_MASK_COLORS["green"], STACKUP_SILK_COLORS["white"]); the others in their own
colours.
