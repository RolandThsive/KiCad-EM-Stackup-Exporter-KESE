# 14. Colorizing

Colours decide only the look of the GLB and OBJ files (and the colour tag of each STEP solid).
They never change geometry or the physical properties in `materials.json`. Stage 5, materials
(`kese/s5_materials/materials.py`), gives every part one material. There is no file of colours:
each colour is a setting in the last section, "Color", of the file of the element it belongs to,
in `parameters/PCB_elements/`: `Board.py`, `Copper.py`, `Finish.py`, `SolderMask.py` and
`SilkScreen.py`.

## 14.1 Materials

Every colour setting is one dict of four values: `color`, an sRGB hex string, and the glTF PBR
values `alpha`, `metallic` and `roughness`. Alpha below 1 writes a glTF `BLEND` material.

```python
CORE_COLOR = {"color": "#968A58", "alpha": 1.0, "metallic": 0.0, "roughness": 0.80}
```

| Setting | Colour | Alpha | Metallic | Roughness | Material name | Used for |
|---|---|---|---|---|---|---|
| `Board.CORE_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/968A58.webp" width="12" height="12" align="absmiddle" alt=""> `#968A58` | 1.0 | 0.0 | 0.80 | `Board_core` | the cores |
| `Board.PREPREG_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/A89C66.webp" width="12" height="12" align="absmiddle" alt=""> `#A89C66` | 1.0 | 0.0 | 0.80 | `Board_prepreg` | the prepregs and their plies |
| `Board.RESIN_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/B8AC78.webp" width="12" height="12" align="absmiddle" alt=""> `#B8AC78` | 1.0 | 0.0 | 0.80 | `Board_resin` | the resin between the traces of the inner copper, with the plies separate |
| `Board.BOARD_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/968A58.webp" width="12" height="12" align="absmiddle" alt=""> `#968A58` | 1.0 | 0.0 | 0.80 | `Board` | the laminate with `Board.DIELECTRIC_GROUPING = "merged"`, and a ply of no type |
| `Copper.COPPER_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/CD803E.webp" width="12" height="12" align="absmiddle" alt=""> `#CD803E` | 1.0 | 0.9 | 0.35 | `Copper` | copper, simulation mode |
| `Copper.PLATING_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/CD803E.webp" width="12" height="12" align="absmiddle" alt=""> `#CD803E` | 1.0 | 0.9 | 0.35 | `Plating` | the `Plating` part (`Copper.COPPER_GROUPING = "layer"`) |
| `Copper.EXPOSED_COPPER_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/DEBA60.webp" width="12" height="12" align="absmiddle" alt=""> `#DEBA60` | 1.0 | 1.0 | 0.25 | `Copper_exposed` | all copper and plating, visual mode |
| `Copper.VIA_RESIN_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/D8CFA0.webp" width="12" height="12" align="absmiddle" alt=""> `#D8CFA0` | 1.0 | 0.0 | 0.60 | `Via Resin` | the resin of plugged and resin-filled vias (KiCad 10), both modes |
| `SolderMask.TOP_MASK_COLOR`, `SolderMask.BOTTOM_MASK_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/EBEBE6.webp" width="12" height="12" align="absmiddle" alt=""> `#EBEBE6` white | 0.80 | 0.0 | 0.30 | `Top Solder Mask`, `Bottom Solder Mask` | the mask parts |
| `SolderMask.TOP_MASK_OVER_COPPER_COLOR`, `SolderMask.BOTTOM_MASK_OVER_COPPER_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/F2EFD8.webp" width="12" height="12" align="absmiddle" alt=""> `#F2EFD8` | 1.0 | 0.0 | 0.30 | `Top Mask over Copper`, `Bottom Mask over Copper` | the mask on copper, visual mode only |
| `SilkScreen.TOP_SILK_COLOR`, `SilkScreen.BOTTOM_SILK_COLOR` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/141414.webp" width="12" height="12" align="absmiddle" alt=""> `#141414` black | 1.0 | 0.0 | 0.75 | `Top Silkscreen`, `Bottom Silkscreen` | silkscreen |
| `Finish.FINISH_COLORS["Nickel"]` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/B8B8B0.webp" width="12" height="12" align="absmiddle" alt=""> `#B8B8B0` | 1.0 | 1.0 | 0.40 | `Nickel` | finish |
| `Finish.FINISH_COLORS["Gold"]` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/E6C15A.webp" width="12" height="12" align="absmiddle" alt=""> `#E6C15A` | 1.0 | 1.0 | 0.20 | `Gold` | finish |
| `Finish.FINISH_COLORS["Tin"]` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/C9C9C9.webp" width="12" height="12" align="absmiddle" alt=""> `#C9C9C9` | 1.0 | 1.0 | 0.45 | `Tin` | finish |
| `Finish.FINISH_COLORS["Silver"]` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/E4E4E0.webp" width="12" height="12" align="absmiddle" alt=""> `#E4E4E0` | 1.0 | 1.0 | 0.25 | `Silver` | finish |
| `Finish.FINISH_COLORS["Palladium"]` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/DFDAD4.webp" width="12" height="12" align="absmiddle" alt=""> `#DFDAD4` | 1.0 | 1.0 | 0.30 | `Palladium` | finish |
| `Finish.FINISH_COLORS["OSP"]` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/D9955A.webp" width="12" height="12" align="absmiddle" alt=""> `#D9955A` | 1.0 | 0.8 | 0.35 | `OSP` | finish |

The material name is what the GLB, `materials.json` and `report.txt` call the look. How a part
finds its setting (`_key()` in `kese/s5_materials/materials.py`):

| Part role | Material name |
|---|---|
| `board` | `Board_<kind>` (`Board_core`, `Board_prepreg`, `Board_resin`) with `"layer"` grouping, else `Board` |
| `copper`, `plating` | `Copper_exposed` in visual mode, else `Copper` / `Plating` |
| `via_resin` | `Via Resin` |
| `mask`, `mask_over_copper`, `silk` | the part's own name, e.g. `Top Solder Mask` |
| `finish` | its metal, e.g. `Gold` |

A laminate solid of a kind with no setting of its own, and a finish metal that
`Finish.FINISH_COLORS` does not hold, take `Board.BOARD_COLOR`. With the plies fused the resin
beside the inner copper is a part of its prepreg's solid and has that solid's colour;
`Board_resin` is a part of its own with the plies separate (`Stackup.FUSION_BUILD = "PLIES_SEPARATE"`, the default)
([Board](Board.md#122-resin-between-the-traces-of-the-inner-copper)).

One setting of a colour is changed for one run with `--set` and the whole dict:

```bash
python run_KESE.py board.kicad_pcb --set 'Copper.COPPER_COLOR={"color": "#B87333", "alpha": 1.0, "metallic": 0.9, "roughness": 0.35}'
```

Before the parameters were sorted by element, all of these were entries of one dict,
`Color.MATERIALS`, in `parameters/color.py`. That file is not read any more and
`--set Color.MATERIALS=...` stops the run with the list of the settings that took its place; the
other settings of the old `Color` module are still understood under their old names, with a note
in `report.txt` ([Parameter Reference](Parameter-Reference.md)).

## 14.2 Colours From The Stack-Up

KiCad's Board Setup gives the mask and silkscreen layers a colour: one of its names (Green, Red,
Blue, Purple, Black, White, Yellow), written as the name (`(layer "F.Mask" ... (color "Green"))`),
or one picked under "User defined", written as `#RRGGBBAA` with its opacity last
(`(color "#1B5E20D4")`). With `SolderMask.USE_STACKUP_MASK_COLOR = True` and
`SilkScreen.USE_STACKUP_SILK_COLOR = True` (the defaults) a name, in lower case, is looked up in
three tables: two in `SolderMask.py` and one in `SilkScreen.py`. A name the mask or silkscreen
table does not have keeps the colour setting of its part, and `report.txt` warns about it.

| Name | `SolderMask.STACKUP_MASK_COLORS` | `SolderMask.STACKUP_MASK_OVER_COPPER_COLORS` (visual mode) | `SilkScreen.STACKUP_SILK_COLORS` |
|---|---|---|---|
| `green` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/126830.webp" width="12" height="12" align="absmiddle" alt=""> `#126830` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/3F8F3A.webp" width="12" height="12" align="absmiddle" alt=""> `#3F8F3A` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/126830.webp" width="12" height="12" align="absmiddle" alt=""> `#126830` |
| `red` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/A01414.webp" width="12" height="12" align="absmiddle" alt=""> `#A01414` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/C8503C.webp" width="12" height="12" align="absmiddle" alt=""> `#C8503C` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/A01414.webp" width="12" height="12" align="absmiddle" alt=""> `#A01414` |
| `blue` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/14328C.webp" width="12" height="12" align="absmiddle" alt=""> `#14328C` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/3C5AB4.webp" width="12" height="12" align="absmiddle" alt=""> `#3C5AB4` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/14328C.webp" width="12" height="12" align="absmiddle" alt=""> `#14328C` |
| `purple` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/501E6E.webp" width="12" height="12" align="absmiddle" alt=""> `#501E6E` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/7A4696.webp" width="12" height="12" align="absmiddle" alt=""> `#7A4696` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/501E6E.webp" width="12" height="12" align="absmiddle" alt=""> `#501E6E` |
| `black` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/121214.webp" width="12" height="12" align="absmiddle" alt=""> `#121214` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/2E2E30.webp" width="12" height="12" align="absmiddle" alt=""> `#2E2E30` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/141414.webp" width="12" height="12" align="absmiddle" alt=""> `#141414` |
| `white` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/EBEBE6.webp" width="12" height="12" align="absmiddle" alt=""> `#EBEBE6` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/F2EFD8.webp" width="12" height="12" align="absmiddle" alt=""> `#F2EFD8` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/F0F0EC.webp" width="12" height="12" align="absmiddle" alt=""> `#F0F0EC` |
| `yellow` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/D2B414.webp" width="12" height="12" align="absmiddle" alt=""> `#D2B414` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/E6CC50.webp" width="12" height="12" align="absmiddle" alt=""> `#E6CC50` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/E6C828.webp" width="12" height="12" align="absmiddle" alt=""> `#E6C828` |
| `matte green` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/1E5A2D.webp" width="12" height="12" align="absmiddle" alt=""> `#1E5A2D` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/4A7D4A.webp" width="12" height="12" align="absmiddle" alt=""> `#4A7D4A` | |
| `matte black` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/191919.webp" width="12" height="12" align="absmiddle" alt=""> `#191919` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/343434.webp" width="12" height="12" align="absmiddle" alt=""> `#343434` | |
| `matte blue` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/19326E.webp" width="12" height="12" align="absmiddle" alt=""> `#19326E` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/3C5A96.webp" width="12" height="12" align="absmiddle" alt=""> `#3C5A96` | |
| `matte red` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/8C1919.webp" width="12" height="12" align="absmiddle" alt=""> `#8C1919` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/AA4646.webp" width="12" height="12" align="absmiddle" alt=""> `#AA4646` | |

The `six_layer` test board, for example, has a black mask in its stack-up, so its mask parts come
out
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/121214.webp" width="12" height="12" align="absmiddle" alt=""> `#121214`.
Set `SolderMask.USE_STACKUP_MASK_COLOR = False` to always use `TOP_MASK_COLOR` and
`BOTTOM_MASK_COLOR`, and `SilkScreen.USE_STACKUP_SILK_COLOR = False` to always use `TOP_SILK_COLOR`
and `BOTTOM_SILK_COLOR`. The two switches are apart, so a board can keep its mask colour and take
the silkscreen colour of the file.

A user-defined colour is used as it is, for the mask and the silkscreen alike. Its opacity is not:
the mask keeps the alpha of its colour setting, 0.8 in simulation mode and opaque in visual mode, as with
a named colour. In visual mode the mask over copper takes the colour mixed part of the way toward
white, each channel

```math
c' = c + L \cdot (255 - c) \qquad (14.1)
```

| Symbol | Meaning |
|---|---|
| $`c`$ | one channel of the user-defined colour, 0 to 255 |
| $`c'`$ | the same channel over copper, rounded |
| $`L`$ | `SolderMask.USER_MASK_OVER_COPPER_LIGHTEN`, 0.15 by default |

With $`L = 0.15`$, `#1B5E20D4` gives <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/1B5E20.webp" width="12" height="12" align="absmiddle" alt=""> `#1B5E20` for the mask and <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/3D7641.webp" width="12" height="12" align="absmiddle" alt=""> `#3D7641` over copper.

![The board featureTest/17_mask_silk from the top in a simulation-mode GLB, once for every mask colour name in the table and once with none set, each labelled with its name and hex value](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Solder-Masks/mask_1_colors_simulation.webp)

![The same board once for every silkscreen colour: white and yellow silk on black mask, and black, not set, green, red, blue and purple silk on white mask](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Silkscreens/silk_1_colors_simulation.webp)

## 14.3 Mode Differences

- **Simulation mode**: the mask is translucent (alpha 0.80) so the copper under it can be seen in
  a viewer. The mask on top of copper is part of the same mask solid and has the same colour.
- **Visual mode**: the mask is drawn opaque whatever its alpha (`SolderMask.VISUAL_MASK_OPAQUE =
  True`), because the skin has nothing behind it; the mask over copper is its own part with the
  lighter "over copper" colour, so traces read through the mask as on a real board; all copper
  takes `Copper.EXPOSED_COPPER_COLOR`.

![The mask colour gallery again in a visual-mode GLB: the mask opaque, and the mask on the copper in its lighter colour, so the tracks read through it](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Solder-Masks/mask_2_colors_visual.webp)

## 14.4 Where The Colours Go

| File | How the colour is written |
|---|---|
| GLB | a PBR material with the part's material name (14.1), shared by parts with the same name and look (every `Copper_<net>` uses one `Copper` material; the top and bottom mask and silkscreen each keep their own): `baseColorFactor` (sRGB converted to linear, below), `metallicFactor`, `roughnessFactor`, `alphaMode: BLEND` when alpha < 1 |
| OBJ | an `.mtl` next to the `.obj` with `newmtl <part>` (the part name with spaces and other characters replaced by `_`, e.g. `Top_Solder_Mask`), `Kd r g b`, `d alpha` |
| STEP | the assembly colour of each solid (RGB and alpha) |
| STL | none (STL has no colour) |
| `materials.json` | `look: {color, alpha}` per part |
| `report.txt` | the material name, hex and alpha on every `parts` line |

glTF stores base colours in linear light, so `kese/s7_write/glb.py` converts each 8-bit sRGB
channel before it writes the GLB:

```python
def _srgb_to_linear(rgb):                    # rgb: the hex colour as three 0-255 values
    s = np.asarray(rgb, dtype=float) / 255
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)

factor = np.array([*np.round(_srgb_to_linear(mat["rgb"]), 5), round(float(mat["alpha"]), 4)])
```

The GLB writer then stores the factor in 8 bits, so the GLB holds the nearest step of 1/255:
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Colorizing/ColorSwatches/968A58.webp" width="12" height="12" align="absmiddle" alt=""> `#968A58`
is written as 0.30588, 0.25490, 0.09804 rather than 0.30499, 0.25415, 0.09759. The alpha is
stored in the same 1/255 steps (0.80 stays 0.80; 0.85 would become 0.85098). The OBJ `Kd` line
carries the sRGB values as they are, `s` above.

## 14.5 Settings

The colours themselves are the settings of 14.1. The rest, by file:

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SolderMask.VISUAL_MASK_OPAQUE` | `True` | bool | Draw the mask opaque in visual mode |
| `SolderMask.USE_STACKUP_MASK_COLOR` | `True` | bool | Honour the mask colour in the board's stack-up, named or user-defined |
| `SolderMask.STACKUP_MASK_COLORS` | table above | name to hex | Stack-up colour names of the mask |
| `SolderMask.STACKUP_MASK_OVER_COPPER_COLORS` | table above | name to hex or `None` per entry | Visual-mode colour of the mask over copper per stack-up colour; an entry set to `None` keeps `TOP_MASK_OVER_COPPER_COLOR` or `BOTTOM_MASK_OVER_COPPER_COLOR` (the table itself must stay a dict) |
| `SolderMask.USER_MASK_OVER_COPPER_LIGHTEN` | `0.15` | 0 to 1 | With a user-defined mask colour, how far the visual-mode mask over copper is mixed toward white (0 the same colour, 1 white) |
| `SilkScreen.USE_STACKUP_SILK_COLOR` | `True` | bool | Honour the silkscreen colour in the board's stack-up, named or user-defined |
| `SilkScreen.STACKUP_SILK_COLORS` | table above | name to hex | Stack-up colour names of the silkscreen |

The old name `Color.USE_STACKUP_COLORS` sets both `USE_STACKUP_MASK_COLOR` and
`USE_STACKUP_SILK_COLOR`.

| Previous | Next |
|:---|---:|
| [Copper And Traces](Copper-And-Traces.md) | [Finish](Finish.md) |
