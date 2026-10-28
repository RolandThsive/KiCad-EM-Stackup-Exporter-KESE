The colour boxes the wiki (docs/wiki/) shows in front of a hex colour code, one per colour of
Generator/parameters/color.py, named by the colour: CD803E.png is #CD803E.

GitHub shows its own colour preview for a `#hex` code only in issues, pull requests and
discussions, not on wiki pages, so each box is a small picture: 24 x 24 px, shown at 12 x 12.
In a page, by its raw URL on main (it shows in the wiki only after it is on main):

<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/CD803E.png" width="12" height="12" align="absmiddle" alt=""> `#CD803E`

After a colour in parameters/color.py changes, make the boxes again (from Generator/):

python tools/make_swatches.py
