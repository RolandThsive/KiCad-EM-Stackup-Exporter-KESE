The Examples page's pictures of the three example boards of Generator/Input/, one folder per
board: rf_module/, hdi_module/ and pcie_card/. The page shows them by their raw URL on main
(https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Examples/<board>/<name>),
so they show in the wiki only after they are on main. The same boards drawn straight from above
and below, for the Time Distribution page, are in ../Time-Distribution/<board>/, and the turning
RF module of the main README is in ../README/rf_module/; they are drawn the same way.

Each picture is the board's GLB drawn with three.js, saved as a lossless WebP; an animation is an
animated WebP. The name says what it shows, and from which mode where that matters:
top_visual.webp is the top of the visual-mode GLB, layers_apart_simulation.webp the
simulation-mode GLB with its layers drawn apart. top_straight_visual.webp and
bottom_straight_visual.webp are the visual-mode GLB with the mask and silkscreen on, drawn
straight from above and from below by an orthographic camera; the bottom is mirrored left to
right, as KiCad shows the board flipped.
