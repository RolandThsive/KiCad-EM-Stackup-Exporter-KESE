# 14. Silkscreens

The silkscreen is the legend ink printed on top of the solder mask: reference designators,
values, logos and outlines. `Generator/Geometry/Silkscreen.py` builds it,
`Generator/Geometry/Text.py` renders the text; the settings are in
`Parameters/Silkscreen_Parameters.py`.

<!-- Pictures wanted for this page (made by Roland):
     Silk 1: a reference designator rendered by KESE next to KiCad's own rendering of the same text.
     Silk 2: a cross-section of ink climbing the mask step beside a trace.
     Silk 3: silk clipped off a pad opening (SILKSCREEN_OVER_COPPER False) versus kept (True). -->

## 14.1 What Is Drawn

Items on the layers in `Silkscreen.SILK_LAYERS` (`F.SilkS` and `B.SilkS` by default):

| Item | Shape |
|---|---|
| graphics (`gr_line`, `gr_arc`, `gr_circle`, `gr_rect`, `gr_poly`, `gr_curve`, and the `fp_*` versions inside footprints) | the stroke thickened by its width; filled shapes filled |
| text (`gr_text`, `fp_text`, footprint `property` fields such as Reference and Value) | glyphs of the stroke font, laid out as KiCad lays them out |
| zone fills on a silk layer | the stored polygons |

Items on `F.Fab`, `B.Fab`, courtyard and user layers are not physical and are counted under
`skipped` in `report.txt`. Text boxes and dimensions are not modelled (also counted).

Everything is clipped to the outline, pulled back from the edge by the same
`SolderMask.MASK_EDGE_PULLBACK_MM` as the mask, and cut away over open hole bores. Then, with
`Silkscreen.SILKSCREEN_OVER_COPPER = False` (the default), the ink is removed wherever the mask
is open (pads, exposed copper, bare laminate in openings), which is what fabricators do: silk is
clipped off the pads. With `True` the ink is kept there as drawn in KiCad.

## 14.2 Text Rendering

KESE ships KiCad's own stroke font, **newstroke**, converted to a JSON file
(`Parameters/Fonts/kicad_newstroke.json.gz`, with its notice in `LICENSE_fonts.txt`). Text is laid
out following KiCad's `STROKE_FONT` and `drawMultilineText` code:

- glyph advance from the glyph width plus `INTER_CHAR_SPACING` × text width;
- line pitch `INTERLINE_PITCH` × text height × `INTERLINE_LEGACY_FACTOR`;
- horizontal and vertical justification with KiCad's offsets, mirrored text for the back side;
- italic as a shear of `ITALIC_TILT`;
- stroke thickness from the file, else `BOLD_THICKNESS_RATIO` or `NORMAL_THICKNESS_RATIO` × height;
- round stroke ends with `TEXT_STROKE_QUAD_SEGS` segments per quarter circle;
- `${REFERENCE}`, `${VALUE}` and other footprint fields substituted;
- `\n` line breaks.

Text in a TrueType face (KiCad 7+ `(font (face "..."))`) is drawn with the stroke font when
`DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT = True` (the default) and counted in `report.txt`; with
`False` it is skipped. Text the file marks hidden (`(hide yes)`) is skipped unless
`DRAW_HIDDEN_TEXT = True`.

A custom font can replace newstroke: set `FONT_FILE` to a file in `Parameters/Fonts/`, either in
this project's stroke-font JSON format or a Hershey `.jhf` file. If the file is missing, newstroke
is used and `report.txt` says so on its `font:` note.

## 14.3 Ink Geometry

The ink is `SILK_THICKNESS_MM` thick (10 µm by default) and follows the mask surface, which is
flat over laminate and raised over copper (by the copper thickness plus the mask-over-copper
thickness):

| Where | z range (top side, from the laminate face) |
|---|---|
| on the mask over laminate | mask thickness to mask thickness + ink |
| on the mask over copper | copper + mask over copper to that + ink |
| the step beside a trace, where the mask climbs | a wall from the mask surface to the raised surface + ink |
| where the ink leaves the mask (only with `SILKSCREEN_OVER_COPPER = True`) | it steps down the mask edge and lies on the laminate or on bare copper |

Each side is one part, `Top Silkscreen` or `Bottom Silkscreen`, with `side` and `thickness_mm`
in `materials.json`.

## 14.4 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILK_THICKNESS_MM` | `0.010` | mm > 0 | Ink thickness (typical 0.010 to 0.020) |
| `SILKSCREEN_OVER_COPPER` | `False` | bool | Keep ink where the mask is open |
| `FONT_FILE` | `None` | None or a file name in `Parameters/Fonts/` | Custom font; `None` = KiCad newstroke |
| `DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT` | `True` | bool | Draw TrueType-face text with the stroke font |
| `INTERLINE_PITCH`, `INTERLINE_LEGACY_FACTOR` | `1.68`, `0.9583` | > 0 | KiCad's line pitch and stroke-font correction |
| `INTER_CHAR_SPACING` | `0.2` | ≥ 0 | Extra advance between glyphs, fraction of text width |
| `ITALIC_TILT` | `0.125` | ≥ 0 | x shift per unit of y for italic text |
| `BOLD_THICKNESS_RATIO`, `NORMAL_THICKNESS_RATIO` | `0.2`, `0.15` | > 0 | Stroke = ratio × text height when the file gives none |
| `TEXT_STROKE_QUAD_SEGS` | `4` | int ≥ 1 | Roundness of stroke ends |
| `DRAW_HIDDEN_TEXT` | `False` | bool | Draw text marked hidden |
| `SILK_LAYERS` | `["F.SilkS", "B.SilkS"]` | list of layer names | Layers drawn as silkscreen |

| Previous | Next |
|:---|---:|
| [Top And Bottom Copper Finishings](Copper-Finishings.md) | [Solder Masks](Solder-Masks.md) |
