# 14. Silkscreens

The silkscreen is the legend ink printed on top of the solder mask: reference designators,
values, logos and outlines. `kese/s4_geometry/silkscreen.py` builds it from the ink that
`kese/s3_resolve/silk.py` clips off the pads, and `kese/core/font.py` renders the text; the
settings are in `parameters/silkscreen.py`.

<!-- Picture still wanted for this page:
     a reference designator rendered by KESE next to KiCad's own rendering of the same text (14.2). -->

![The same board eight times from the top in a simulation-mode GLB, once in each silkscreen colour: white and yellow silk on black mask, and black, not set, green, red, blue and purple silk on white mask, each labelled with its colour and hex value](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/silk_1_colors_simulation.png)

## 14.1 What Is Drawn

Items on the layers in `Silkscreen.SILK_LAYERS` (`F.SilkS` and `B.SilkS` by default):

| Item | Shape |
|---|---|
| graphics (`gr_line`, `gr_arc`, `gr_circle`, `gr_rect`, `gr_poly`, `gr_curve`, and the `fp_*` versions inside footprints) | the stroke thickened by its width; filled shapes filled |
| text (`gr_text`, `fp_text`, footprint `property` fields such as Reference and Value) | glyphs of the stroke font, laid out as KiCad lays them out |
| zone fills on a silk layer | the stored polygons |

Graphics on `F.Fab`, `B.Fab`, courtyard and user layers are not physical and are counted under
`skipped` in `report.txt`. Text on those layers (including the footprints' Value fields, which
usually sit on `F.Fab`) and hidden text are ignored without a count. Text is drawn only on
`F.SilkS` and `B.SilkS` (and copper and mask layers), even if another layer is added to
`SILK_LAYERS`; graphics follow `SILK_LAYERS`, each drawn on the top or bottom side by the first
letter of its layer name. Text boxes and dimensions on those layers are not
modelled and are counted under `skipped`.

Everything is clipped to the outline, pulled back from the edge by the same
`SolderMask.MASK_EDGE_PULLBACK_MM` as the mask, and cut away over open hole bores. Then, with
`Silkscreen.SILKSCREEN_OVER_COPPER = False` (the default), the ink is removed wherever the mask
is open (pads, exposed copper, bare laminate in openings), which is what fabricators do: silk is
clipped off the pads. With `True` the ink is kept there as drawn in KiCad.

![U1, J1 and the text OPEN on board 17b_silk_over_copper with SILKSCREEN_OVER_COPPER False and True: from the top with a numbered key, U1 at an angle, and a true-scale cut along U1's outline across pad 2](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/silk_4_mask_subtract.png)

## 14.2 Text Rendering

KESE ships KiCad's own stroke font, **newstroke**, converted to a JSON file
(`kese/assets/fonts/kicad_newstroke.json.gz`, with its notice in `LICENSE_fonts.txt`). Text is laid
out following KiCad's `STROKE_FONT` and `drawMultilineText` code (`kese/core/font.py`).

### 14.2.1 Layout Of One Line

Each character advances the pen by its glyph width; a line's width drops the spacing that the
last glyph carries:

```math
x_{j+1} = x_j + a_j W, \qquad a_j = \begin{cases} w_{g} & \text{a glyph } g \\ w_{\mathrm{sp}} & \text{a space} \\ 4 w_{\mathrm{sp}} & \text{a tab} \end{cases} \qquad (14.1)
```

```math
\lambda = x_{\mathrm{end}} - s_c W \qquad (14.2)
```

A stroke point $`(u, v)`$ of a glyph (in units of the text size, $`v`$ down) is placed at

```math
x = x_j + \left( u - \tau v \right) W, \qquad y = v H \qquad (14.3)
```

### 14.2.2 Lines And Justification

```math
p = H \cdot \pi_\ell \cdot \kappa_\ell \qquad (14.4)
```

```math
\hat{H} = 1.17 H + (n_\ell - 1) p \qquad (14.5)
```

```math
o_x = \frac{T}{1.52}, \qquad o_y = H - 0.052 T - \begin{cases} 0 & \text{top} \\ \hat{H} & \text{bottom} \\ \hat{H}/2 & \text{centre} \end{cases} \qquad (14.6)
```

```math
x_{\mathrm{start},i} = o_x + \begin{cases} 0 & \text{left} \\ -\left( \lambda_i + o_x \right) & \text{right} \\ -\lambda_i / 2 & \text{centre} \end{cases}, \qquad y_{\mathrm{start},i} = o_y + i p \qquad (14.7)
```

### 14.2.3 Placement And Stroke

Every local point $`(x, y)`$ is mirrored when the text is marked `(justify mirror)` in the file
($`x \to -x`$; KiCad sets this on back-side text), then rotated by the
text angle $`\theta`$ about the anchor $`(X_0, Y_0)`$, in KiCad's frame (Y down):

```math
X = X_0 + x \cos\theta + y \sin\theta, \qquad Y = Y_0 - x \sin\theta + y \cos\theta \qquad (14.8)
```

The strokes are then thickened to the stroke width:

```math
T = \begin{cases} T_{\mathrm{file}} & \text{if the file gives one} \\ \rho_b H & \text{bold} \\ \rho_n H & \text{normal} \end{cases}, \qquad \text{glyph region} = \bigcup \text{strokes} \oplus \frac{T}{2} \qquad (14.9)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`H`$, $`W`$ | text height and width | the file's `(size h w)` |
| $`x_j`$ | pen position before character $`j`$ ($`x_0 = 0`$) | |
| $`w_g`$, $`w_{\mathrm{sp}}`$ | width of glyph $`g`$ and of a space, in units of $`W`$ (from the font file) | |
| $`s_c`$ | inter-character spacing included in each glyph width | `Silkscreen.INTER_CHAR_SPACING` (0.2) |
| $`\lambda`$, $`\lambda_i`$ | width of a line, of line $`i`$ | |
| $`\tau`$ | italic tilt (0 for upright text) | `Silkscreen.ITALIC_TILT` (0.125) |
| $`p`$ | line pitch | |
| $`\pi_\ell`$, $`\kappa_\ell`$ | interline pitch and legacy factor | `Silkscreen.INTERLINE_PITCH` (1.68), `Silkscreen.INTERLINE_LEGACY_FACTOR` (0.9583) |
| $`n_\ell`$ | number of lines (`\n` breaks) | |
| $`\hat{H}`$ | block height | |
| $`o_x`$, $`o_y`$ | KiCad's stroke-font offsets | |
| $`T`$ | stroke width | the file's `(thickness ...)`, else `Silkscreen.BOLD_THICKNESS_RATIO` $`\rho_b`$ (0.2) or `Silkscreen.NORMAL_THICKNESS_RATIO` $`\rho_n`$ (0.15) |
| $`\theta`$, $`(X_0, Y_0)`$ | text angle and anchor | the file's `(at x y angle)` |

Stroke ends are round with `TEXT_STROKE_QUAD_SEGS` segments per quarter circle. `${REFERENCE}`,
`${VALUE}` and the other footprint fields are substituted before layout.

Text in a TrueType face (KiCad 7+ `(font (face "..."))`) is drawn with the stroke font when
`DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT = True` (the default) and counted in `report.txt`; with
`False` it is skipped. Text the file marks hidden (`(hide yes)`) is skipped unless
`DRAW_HIDDEN_TEXT = True`.

A custom font can replace newstroke: set `FONT_FILE` to a file in `kese/assets/fonts/`, either in
this project's stroke-font JSON format or a Hershey `.jhf` file. If the file is missing, newstroke
is used and `report.txt` says so on its `font:` note.

## 14.3 Ink Geometry

![Board 17b_silk_over_copper from the top with a dashed box where a silk line crosses a 0.5 mm track, and the boxed region cut along the silk line: the ink on the mask over the laminate, climbing the mask's wall, and on the mask over the track](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/silk_2_conformal.png)

![Board 17b_silk_over_copper cut along the silk lines across a 1 mm track at true scale with all seven layers labelled, and the top face at the track's edge close up with rulers for the height of every surface above the laminate](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/silk_3_height.png)

The ink follows the mask surface, which is flat over laminate and raised over copper. First the
silk region $`S`$ is split against the mask region $`M`$ of equation (15.1), then the part on the
mask is split against the raised mask over copper, $`K = C \oplus m_L`$:

```math
S^{\mathrm{off}} = S \setminus \left( M \oplus s \right), \qquad S^{\mathrm{on}} = S \cap M, \qquad S^{\mathrm{step}} = S \cap \left( \left( M \oplus s \right) \setminus M \right) \qquad (14.10)
```

```math
S^{\mathrm{flat}} = S^{\mathrm{on}} \setminus \left( K \oplus s \right), \qquad S^{\mathrm{top}} = S^{\mathrm{on}} \cap K, \qquad S^{\mathrm{wall}} = S^{\mathrm{on}} \cap \left( \left( K \oplus s \right) \setminus K \right) \qquad (14.11)
```

On the `F` side, with $`h = L/2`$ the laminate face, these are extruded over:

| Region | z range | Where |
|---|---|---|
| $`S^{\mathrm{flat}}`$ | $`[h + m_L,\ h + m_L + s]`$ | on the mask over laminate |
| $`S^{\mathrm{top}}`$ | $`[h + t + m_C,\ h + t + m_C + s]`$ | on the mask over copper |
| $`S^{\mathrm{wall}}`$ | $`[h + m_L,\ h + t + m_C + s]`$ | climbing the mask step beside a trace |
| $`S^{\mathrm{step}} \cap C`$ | $`[h + t,\ h + t + m_C + s]`$ | stepping down the edge of a mask opening onto copper |
| $`(S^{\mathrm{step}} \setminus C) \cap K`$ | $`[h,\ h + t + m_C + s]`$ | stepping down to the laminate from the raised mask beside copper |
| $`S^{\mathrm{step}} \setminus K`$ | $`[h,\ h + m_L + s]`$ | stepping down the edge of a mask opening onto the laminate |
| $`S^{\mathrm{off}} \setminus C`$ | $`[h,\ h + s]`$ | on bare laminate in an opening |
| $`S^{\mathrm{off}} \cap C`$ | $`[h + t,\ h + t + s]`$ | on bare copper in an opening |

The last five exist only with `SILKSCREEN_OVER_COPPER = True`; otherwise the ink was already
removed from every opening. On the `B` side every z is mirrored. Each piece of the step starts on
what lies under it, the copper or the laminate, and rises to the top of the ink on the mask beside
it.

> [!NOTE]
> With `SILKSCREEN_OVER_COPPER = True` the ink in an opening lies on the bare copper, and a
> surface finish (`Finish.FINISH_ENABLED = True`) is left out under it, as when the legend is
> printed before the finish. So the ink overlaps no other part with either setting.

| Symbol | Meaning | Parameter |
|---|---|---|
| $`S`$ | silk region after clipping to the outline, the edge pull-back and the bores | |
| $`M`$ | mask region, equation (15.1) | |
| $`C`$ | outer copper of that side, every net | |
| $`s`$ | ink thickness | `Silkscreen.SILK_THICKNESS_MM` (0.010) |
| $`m_L`$, $`m_C`$ | mask thickness over laminate and over copper | `SolderMask.MASK_OVER_LAMINATE_MM`, `SolderMask.MASK_OVER_COPPER_MM` |
| $`t`$ | finished outer copper thickness, equation (7.3) | |

Each side is one part, `Top Silkscreen` or `Bottom Silkscreen`, with `side` and `thickness_mm`
in `materials.json`.

## 14.4 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILK_THICKNESS_MM` | `0.010` | mm > 0 | Ink thickness (typical 0.010 to 0.020) |
| `SILKSCREEN_OVER_COPPER` | `False` | bool | Keep ink where the mask is open, on the pads and the bare laminate (the finish is left out under it); `False` clips it off as fabricators do |
| `FONT_FILE` | `None` | None or a file name in `kese/assets/fonts/` | Custom font; `None` = KiCad newstroke |
| `DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT` | `True` | bool | Draw TrueType-face text with the stroke font |
| `INTERLINE_PITCH`, `INTERLINE_LEGACY_FACTOR` | `1.68`, `0.9583` | > 0 | KiCad's line pitch and stroke-font correction |
| `INTER_CHAR_SPACING` | `0.2` | ≥ 0 | Spacing each glyph width includes, as a fraction of the text width; dropped from the line width, equation (14.2) |
| `ITALIC_TILT` | `0.125` | ≥ 0 | x shift per unit of y for italic text |
| `BOLD_THICKNESS_RATIO`, `NORMAL_THICKNESS_RATIO` | `0.2`, `0.15` | > 0 | Stroke = ratio × text height when the file gives none |
| `TEXT_STROKE_QUAD_SEGS` | `4` | int ≥ 1 | Roundness of stroke ends |
| `DRAW_HIDDEN_TEXT` | `False` | bool | Draw text marked hidden |
| `SILK_LAYERS` | `["F.SilkS", "B.SilkS"]` | list of `F.*` / `B.*` layer names | Layers drawn as silkscreen, on the side their first letter names; any other name stops the run with a `KeyError` when the board has graphics on that layer |

| Previous | Next |
|:---|---:|
| [Top And Bottom Copper Finishings](Copper-Finishings.md) | [Solder Masks](Solder-Masks.md) |
