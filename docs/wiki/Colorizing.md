# 12. Colorizing

Colours decide only the look of the GLB and OBJ files (and the colour tag of each STEP solid).
They never change geometry or the physical properties in `materials.json`. Stage 5, materials
(`kese/s5_materials/materials.py`), gives every part one material from `parameters/color.py`.

## 12.1 Materials

`Color.MATERIALS`: one entry per key, a colour as an sRGB hex string and the glTF PBR values.
Alpha below 1 writes a glTF `BLEND` material.

| Key | Colour | Alpha | Metallic | Roughness | Used for |
|---|---|---|---|---|---|
| `Board` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/968A58.webp" width="12" height="12" align="absmiddle" alt=""> `#968A58` | 1.0 | 0.0 | 0.80 | the laminate with `Run.DIELECTRIC_GROUPING = "merged"` |
| `Board_core` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/968A58.webp" width="12" height="12" align="absmiddle" alt=""> `#968A58` | 1.0 | 0.0 | 0.80 | cores, with `"layer"` grouping |
| `Board_prepreg` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/A89C66.webp" width="12" height="12" align="absmiddle" alt=""> `#A89C66` | 1.0 | 0.0 | 0.80 | prepregs, with `"layer"` grouping |
| `Copper` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/CD803E.webp" width="12" height="12" align="absmiddle" alt=""> `#CD803E` | 1.0 | 0.9 | 0.35 | copper, simulation mode |
| `Plating` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/CD803E.webp" width="12" height="12" align="absmiddle" alt=""> `#CD803E` | 1.0 | 0.9 | 0.35 | the `Plating` part (`Run.COPPER_GROUPING = "layer"`) |
| `Copper_exposed` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/DEBA60.webp" width="12" height="12" align="absmiddle" alt=""> `#DEBA60` | 1.0 | 1.0 | 0.25 | all copper and plating, visual mode |
| `Top Solder Mask`, `Bottom Solder Mask` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/EBEBE6.webp" width="12" height="12" align="absmiddle" alt=""> `#EBEBE6` white | 0.80 | 0.0 | 0.30 | the mask parts |
| `Top Mask over Copper`, `Bottom Mask over Copper` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/F2EFD8.webp" width="12" height="12" align="absmiddle" alt=""> `#F2EFD8` | 1.0 | 0.0 | 0.30 | the mask on copper, visual mode only |
| `Top Silkscreen`, `Bottom Silkscreen` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/141414.webp" width="12" height="12" align="absmiddle" alt=""> `#141414` black | 1.0 | 0.0 | 0.75 | silkscreen |
| `Nickel` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/B8B8B0.webp" width="12" height="12" align="absmiddle" alt=""> `#B8B8B0` | 1.0 | 1.0 | 0.40 | finish |
| `Gold` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/E6C15A.webp" width="12" height="12" align="absmiddle" alt=""> `#E6C15A` | 1.0 | 1.0 | 0.20 | finish |
| `Tin` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/C9C9C9.webp" width="12" height="12" align="absmiddle" alt=""> `#C9C9C9` | 1.0 | 1.0 | 0.45 | finish |
| `Silver` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/E4E4E0.webp" width="12" height="12" align="absmiddle" alt=""> `#E4E4E0` | 1.0 | 1.0 | 0.25 | finish |
| `Palladium` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/DFDAD4.webp" width="12" height="12" align="absmiddle" alt=""> `#DFDAD4` | 1.0 | 1.0 | 0.30 | finish |
| `OSP` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/D9955A.webp" width="12" height="12" align="absmiddle" alt=""> `#D9955A` | 1.0 | 0.8 | 0.35 | finish |

How a part finds its key (`_key()` in `kese/s5_materials/materials.py`):

| Part role | Key |
|---|---|
| `board` | `Board_<kind>` (`Board_core`, `Board_prepreg`) with `"layer"` grouping, else `Board` |
| `copper`, `plating` | `Copper_exposed` in visual mode, else `Copper` / `Plating` |
| `mask`, `mask_over_copper`, `silk` | the part's own name, e.g. `Top Solder Mask` |
| `finish` | its metal, e.g. `Gold` |

A key with no entry in `MATERIALS` takes the `Board` entry.

## 12.2 Colours From The Stack-Up

KiCad's Board Setup gives the mask and silkscreen layers a colour: one of its names (Green, Red,
Blue, Purple, Black, White, Yellow), written as the name (`(layer "F.Mask" ... (color "Green"))`),
or one picked under "User defined", written as `#RRGGBBAA` with its opacity last
(`(color "#1B5E20D4")`). With `Color.USE_STACKUP_COLORS = True` (the default) a name, in lower
case, is looked up in three tables. A name the mask or silkscreen table does not have keeps the
`MATERIALS` colour, and `report.txt` warns about it.

| Name | `STACKUP_MASK_COLORS` | `STACKUP_MASK_OVER_COPPER_COLORS` (visual mode) | `STACKUP_SILK_COLORS` |
|---|---|---|---|
| `green` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/126830.webp" width="12" height="12" align="absmiddle" alt=""> `#126830` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/3F8F3A.webp" width="12" height="12" align="absmiddle" alt=""> `#3F8F3A` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/126830.webp" width="12" height="12" align="absmiddle" alt=""> `#126830` |
| `red` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/A01414.webp" width="12" height="12" align="absmiddle" alt=""> `#A01414` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/C8503C.webp" width="12" height="12" align="absmiddle" alt=""> `#C8503C` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/A01414.webp" width="12" height="12" align="absmiddle" alt=""> `#A01414` |
| `blue` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/14328C.webp" width="12" height="12" align="absmiddle" alt=""> `#14328C` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/3C5AB4.webp" width="12" height="12" align="absmiddle" alt=""> `#3C5AB4` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/14328C.webp" width="12" height="12" align="absmiddle" alt=""> `#14328C` |
| `purple` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/501E6E.webp" width="12" height="12" align="absmiddle" alt=""> `#501E6E` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/7A4696.webp" width="12" height="12" align="absmiddle" alt=""> `#7A4696` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/501E6E.webp" width="12" height="12" align="absmiddle" alt=""> `#501E6E` |
| `black` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/121214.webp" width="12" height="12" align="absmiddle" alt=""> `#121214` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/2E2E30.webp" width="12" height="12" align="absmiddle" alt=""> `#2E2E30` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/141414.webp" width="12" height="12" align="absmiddle" alt=""> `#141414` |
| `white` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/EBEBE6.webp" width="12" height="12" align="absmiddle" alt=""> `#EBEBE6` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/F2EFD8.webp" width="12" height="12" align="absmiddle" alt=""> `#F2EFD8` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/F0F0EC.webp" width="12" height="12" align="absmiddle" alt=""> `#F0F0EC` |
| `yellow` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/D2B414.webp" width="12" height="12" align="absmiddle" alt=""> `#D2B414` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/E6CC50.webp" width="12" height="12" align="absmiddle" alt=""> `#E6CC50` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/E6C828.webp" width="12" height="12" align="absmiddle" alt=""> `#E6C828` |
| `matte green` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/1E5A2D.webp" width="12" height="12" align="absmiddle" alt=""> `#1E5A2D` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/4A7D4A.webp" width="12" height="12" align="absmiddle" alt=""> `#4A7D4A` | |
| `matte black` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/191919.webp" width="12" height="12" align="absmiddle" alt=""> `#191919` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/343434.webp" width="12" height="12" align="absmiddle" alt=""> `#343434` | |
| `matte blue` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/19326E.webp" width="12" height="12" align="absmiddle" alt=""> `#19326E` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/3C5A96.webp" width="12" height="12" align="absmiddle" alt=""> `#3C5A96` | |
| `matte red` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/8C1919.webp" width="12" height="12" align="absmiddle" alt=""> `#8C1919` | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/AA4646.webp" width="12" height="12" align="absmiddle" alt=""> `#AA4646` | |

The `six_layer` test board, for example, has a black mask in its stack-up, so its mask parts come
out
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/121214.webp" width="12" height="12" align="absmiddle" alt=""> `#121214`.
Set `USE_STACKUP_COLORS = False` to always use `MATERIALS`.

A user-defined colour is used as it is, for the mask and the silkscreen alike. Its opacity is not:
the mask keeps the alpha of `MATERIALS`, 0.8 in simulation mode and opaque in visual mode, as with
a named colour. In visual mode the mask over copper takes the colour mixed part of the way toward
white, each channel

```math
c' = c + L \cdot (255 - c) \qquad (12.1)
```

| Symbol | Meaning |
|---|---|
| $`c`$ | one channel of the user-defined colour, 0 to 255 |
| $`c'`$ | the same channel over copper, rounded |
| $`L`$ | `USER_MASK_OVER_COPPER_LIGHTEN`, 0.15 by default |

With $`L = 0.15`$, `#1B5E20D4` gives <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/1B5E20.webp" width="12" height="12" align="absmiddle" alt=""> `#1B5E20` for the mask and <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/3D7641.webp" width="12" height="12" align="absmiddle" alt=""> `#3D7641` over copper.

![The board featureTest/17_mask_silk from the top in a simulation-mode GLB, once for every mask colour name in the table and once with none set, each labelled with its name and hex value](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/mask_1_colors_simulation.webp)

![The same board once for every silkscreen colour: white and yellow silk on black mask, and black, not set, green, red, blue and purple silk on white mask](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/silk_1_colors_simulation.webp)

## 12.3 Mode Differences

- **Simulation mode**: the mask is translucent (alpha 0.80) so the copper under it can be seen in
  a viewer. The mask on top of copper is part of the same mask solid and has the same colour.
- **Visual mode**: the mask is drawn opaque whatever its alpha (`Color.VISUAL_MASK_OPAQUE =
  True`), because the skin has nothing behind it; the mask over copper is its own part with the
  lighter "over copper" colour, so traces read through the mask as on a real board; all copper
  takes `Copper_exposed`.

![The mask colour gallery again in a visual-mode GLB: the mask opaque, and the mask on the copper in its lighter colour, so the tracks read through it](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/mask_2_colors_visual.webp)

## 12.4 Where The Colours Go

| File | How the colour is written |
|---|---|
| GLB | a PBR material named after the part's `MATERIALS` key, shared by parts with the same key and look (every `Copper_<net>` uses one `Copper` material; the top and bottom mask and silkscreen each keep their own): `baseColorFactor` (sRGB converted to linear, below), `metallicFactor`, `roughnessFactor`, `alphaMode: BLEND` when alpha < 1 |
| OBJ | an `.mtl` next to the `.obj` with `newmtl <part>` (the part name with spaces and other characters replaced by `_`, e.g. `Top_Solder_Mask`), `Kd r g b`, `d alpha` |
| STEP | the assembly colour of each solid (RGB and alpha) |
| STL | none (STL has no colour) |
| `materials.json` | `look: {color, alpha}` per part |
| `report.txt` | the material key, hex and alpha on every `parts` line |

glTF stores base colours in linear light, so `kese/s7_write/glb.py` converts each 8-bit sRGB
channel before it writes the GLB:

```python
def _srgb_to_linear(rgb):                    # rgb: the hex colour as three 0-255 values
    s = np.asarray(rgb, dtype=float) / 255
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)

factor = [*np.round(_srgb_to_linear(mat["rgb"]), 5), round(float(mat["alpha"]), 4)]
```

`trimesh` then stores the factor in 8 bits, so the GLB holds the nearest step of 1/255:
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/968A58.webp" width="12" height="12" align="absmiddle" alt=""> `#968A58`
is written as 0.30588, 0.25490, 0.09804 rather than 0.30499, 0.25415, 0.09759. The alpha is
stored in the same 1/255 steps (0.80 stays 0.80; 0.85 would become 0.85098). The OBJ `Kd` line
carries the sRGB values as they are, `s` above.

## 12.5 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MATERIALS` | the table above | dict of `{color, alpha, metallic, roughness}` | Look of every part kind |
| `VISUAL_MASK_OPAQUE` | `True` | bool | Draw the mask opaque in visual mode |
| `USE_STACKUP_COLORS` | `True` | bool | Honour the mask and silkscreen colours in the board's stack-up, named or user-defined |
| `STACKUP_MASK_COLORS`, `STACKUP_SILK_COLORS` | tables above | name to hex | Stack-up colour names |
| `STACKUP_MASK_OVER_COPPER_COLORS` | table above | name to hex or `None` per entry | Visual-mode colour of the mask over copper per stack-up colour; an entry set to `None` keeps the `MATERIALS` entry (the table itself must stay a dict) |
| `USER_MASK_OVER_COPPER_LIGHTEN` | `0.15` | 0 to 1 | With a user-defined mask colour, how far the visual-mode mask over copper is mixed toward white (0 the same colour, 1 white) |

| Previous | Next |
|:---|---:|
| [Copper And Traces](Copper-And-Traces.md) | [Top And Bottom Copper Finishings](Copper-Finishings.md) |
