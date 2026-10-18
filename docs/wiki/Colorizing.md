# 12. Colorizing

Colours decide only the look of the GLB and OBJ files (and the colour tag of each STEP solid).
They never change geometry or the physical properties in `materials.json`. The Colorer
(`Generator/Colorer.py`) gives every part one material from `Parameters/Color_Parameters.py`.

<!-- Pictures wanted for this page (made by Roland):
     Color 1: the default palette, one swatch per MATERIALS entry.
     Color 2: the same board with a green, a black and a red stack-up mask colour. -->

## 12.1 Materials

Each entry of `Color.MATERIALS` is a colour as an sRGB hex string, an alpha 0 to 1, a metallic
factor 0 to 1 and a roughness 0 to 1 (the glTF PBR metallic-roughness model). Alpha below 1
writes a glTF `BLEND` material.

| Key | Used for | Default |
|---|---|---|
| `Board`, `Board_core`, `Board_prepreg` | dielectrics; `Board_core` / `Board_prepreg` by kind when `Run.DIELECTRIC_GROUPING = "layer"`, else `Board` | `#968A58` / `#968A58` / `#A89C66`, rough, not metallic |
| `Copper` | copper parts in simulation mode | `#CD803E`, metallic 0.9, roughness 0.35 |
| `Plating` | the `Plating` part (layer grouping) | as `Copper` |
| `Copper_exposed` | all copper and plating in visual mode | `#DEBA60`, metallic 1.0 |
| `Top Solder Mask`, `Bottom Solder Mask` | the mask parts | `#126830`, alpha 0.80 |
| `Top Mask over Copper`, `Bottom Mask over Copper` | the mask on top of copper, visual mode only | `#3F8F3A`, opaque |
| `Top Silkscreen`, `Bottom Silkscreen` | silkscreen | `#F0F0EC` |
| `Nickel`, `Gold`, `Tin`, `Silver`, `OSP` | finish metals, by the metal name | metallic greys, gold, tin |

How a part finds its key: a `board` part by its kind; `copper` and `plating` by role and mode;
`mask`, `mask_over_copper` and `silk` parts by their own part name; a `finish` part by its metal.
A part with no matching entry falls back to `Board`.

## 12.2 Colours From The Stack-Up

KiCad's Board Setup can name a colour for the mask and silkscreen layers
(`(layer "F.Mask" ... (color "Green"))`). With `Color.USE_STACKUP_COLORS = True` (the default)
those names are honoured through three tables:

| Table | Maps | Entries |
|---|---|---|
| `STACKUP_MASK_COLORS` | mask colour name to hex | green, red, blue, black, white, yellow, purple, matte green, matte black, matte blue, matte red |
| `STACKUP_SILK_COLORS` | silkscreen colour name to hex | white, black, yellow |
| `STACKUP_MASK_OVER_COPPER_COLORS` | mask colour name to the lighter "mask on copper" hex used in visual mode | the same mask colours |

Names are matched in lower case; a name not in the table keeps the `MATERIALS` colour. The
`six_layer` test board, for example, has a black mask in its stack-up and comes out with
`#121214` mask parts. Set `USE_STACKUP_COLORS = False` to always use `MATERIALS`.

## 12.3 Mode Differences

- **Simulation mode**: the mask is translucent (alpha 0.80) so the copper under it can be seen in
  a viewer. The mask on top of copper is part of the same mask solid and has the same colour.
- **Visual mode**: the mask is drawn opaque whatever its alpha (`Color.VISUAL_MASK_OPAQUE =
  True`), because the skin has nothing behind it; the mask over copper is its own part with the
  lighter "over copper" colour, so traces read through the mask as on a real board; all copper
  takes `Copper_exposed`.

## 12.4 Where The Colours Go

| File | How the colour is written |
|---|---|
| GLB | one PBR material per part: `baseColorFactor` (sRGB converted to linear, equation (12.1)), `metallicFactor`, `roughnessFactor`, `alphaMode: BLEND` when alpha < 1 |
| OBJ | an `.mtl` next to the `.obj` with `newmtl <part>`, `Kd r g b`, `d alpha` |
| STEP | the assembly colour of each solid (RGB and alpha) |
| STL | none (STL has no colour) |
| `materials.json` | `look: {color, alpha}` per part |
| `report.txt` | the material key, hex and alpha on every `parts` line |

glTF stores base colours in linear light, so each 8-bit sRGB channel of the hex colour is
converted with the standard sRGB transfer function before it is written to the GLB:

```math
c_{\mathrm{lin}} = \begin{cases} \dfrac{c}{12.92} & c \le 0.04045 \\ \left( \dfrac{c + 0.055}{1.055} \right)^{2.4} & c > 0.04045 \end{cases}, \qquad c = \frac{C_8}{255} \qquad (12.1)
```

| Symbol | Meaning |
|---|---|
| $`C_8`$ | one channel of the hex colour, 0 to 255 |
| $`c`$ | that channel as sRGB, 0 to 1 (also what the OBJ `.mtl` `Kd` line carries) |
| $`c_{\mathrm{lin}}`$ | the linear value in the GLB `baseColorFactor`, rounded to 5 decimals |

The fourth component of `baseColorFactor` is the alpha, unchanged.

## 12.5 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MATERIALS` | the table above | dict of `{color, alpha, metallic, roughness}` | Look of every part kind |
| `VISUAL_MASK_OPAQUE` | `True` | bool | Draw the mask opaque in visual mode |
| `USE_STACKUP_COLORS` | `True` | bool | Honour the colour names in the board's stack-up |
| `STACKUP_MASK_COLORS`, `STACKUP_SILK_COLORS` | tables above | name to hex | Stack-up colour names |
| `STACKUP_MASK_OVER_COPPER_COLORS` | table above | name to hex, or `None` | Visual-mode colour of the mask over copper per stack-up colour; `None` keeps the `MATERIALS` entry |

| Previous | Next |
|:---|---:|
| [Copper And Traces](Copper-And-Traces.md) | [Top And Bottom Copper Finishings](Copper-Finishings.md) |
