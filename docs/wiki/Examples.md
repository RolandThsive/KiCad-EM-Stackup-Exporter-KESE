# 5. Examples

`Generator/Input/` holds three example boards. Each is a whole design, not a test of one feature:
a stack-up set in Board Setup, footprints, filled zones, silkscreen on both sides and a solder
mask colour of its own, saved by KiCad 7. Between them they use most of what KESE reads.
`python run_KESE.py` with no arguments exports all three.

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/top_visual.webp" width="32%" alt="The RF sensor module in visual mode: blue mask, white silkscreen and a plated edge">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/top_visual.webp" width="32%" alt="The HDI radio module in visual mode: black mask, a meander antenna and castellated pads on three sides">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/top_visual.webp" width="32%" alt="The PCIe x1 card in visual mode: green mask, and gold fingers on its tongue">
</p>

| | [RF sensor module](#51-rf-sensor-module) | [HDI radio module](#52-hdi-radio-module) | [PCIe x1 card](#53-pcie-x1-card) |
|---|---|---|---|
| File in `Input/` | `rf_module.kicad_pcb` | `hdi_module.kicad_pcb` | `pcie_card.kicad_pcb` |
| Outline | 64 × 44 mm, a cut-out | 22 × 30 mm | 80 × 64.4 mm with the fingers' tongue, a slot |
| Thickness | 1.6 mm | 0.925 mm | 1.57 mm |
| Copper layers | 4 | 6, built 1+4+1 | 4 |
| Dielectrics | FR4: two prepregs of 0.2 mm, a core of 1.095 mm | prepregs 1067 and 1080, two IT-180A cores | two 2116 prepregs, an FR4 core of 1.01 mm |
| Vias | 307 through | 71 micro, 34 blind and buried, 45 through | 239 through |
| Board edge | plated all round and in the cut-out | 43 castellated pads | 36 gold fingers |
| Mask, silkscreen, finish | blue, white, ENIG | black, white, immersion silver | green, white, hard gold |
| Simulation GLB with `--verify` | 42 parts, 887,012 triangles; 21 s, 29.9 MB | 60 parts, 499,544 triangles; 14 s, 17.0 MB | 59 parts, 942,340 triangles; 19 s, 32.1 MB |
| Visual GLB with `--verify` | 20 s, 17.1 MB | 15 s, 8.8 MB | 21 s, 18.3 MB |

The times are the ones the run prints, with the default parameters on one Linux machine with 4
cores; [Project Capabilities](Project-Capabilities.md#45-tested-sizes) adds the STEP files. The
same three files are in `featureTest/` as `21_rf_module`, `22_hdi_module` and `23_pcie_card`, so
the regression suite checks every part of each in both modes.

The pictures on this page are the boards' GLB files drawn with three.js. They were exported with
`--set Run.COPPER_GROUPING=layer`, so that the copper of each layer is one part and the layers
can be drawn apart; with the default grouping, one part per net, the boards look the same.

## 5.1 RF Sensor Module

`Input/rf_module.kicad_pcb`: a 4-layer sensor board with a radio. A QFN-32 microcontroller with
its crystal, a 6-pad SWD connector and a SOIC-8 flash; a QFN-20 radio on an SPI bus, whose 50 Ω
line runs through a matching network to a coax connector between rows of stitching vias; an LDO
fed from a 6-pin header, three LEDs, test points on both sides and plated mounting holes. GND fills
F.Cu, In1.Cu and B.Cu, and In2.Cu is split into +3V3 and +5V.

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/turning_visual_and_simulation.webp" width="70%" alt="The RF module stood on its side and turning, so that its top and its bottom come round in turn: above in visual mode, the opaque blue mask with the tracks reading through it in a lighter blue, the bare copper and the plated edge in gold; below in simulation mode, the mask translucent over the copper and the plated edge in copper colour">
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/top_visual.webp" width="49%" alt="The top in visual mode: the blue mask with the tracks reading through it, the white silkscreen, the bare copper of the pads, test points and mounting holes, the GND border along the rounded outline and around the cut-out with its fence of vias, and the plated edge">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/bottom_visual.webp" width="49%" alt="The bottom in visual mode: the KESE logo, the outline of the CR1220 coin cell BT1, the pads of the I2C and UART lines, the GND border and the plated walls of the edge and the cut-out">
</p>

What this board shows:

- **A plated edge.** The stack-up says `(edge_plating yes)`, so with `Copper.EDGE_PLATING = "file"`
  (the default) the routed edge is copper all round, and so are the walls of the 13 × 6 mm
  cut-out. The edge copper belongs to GND, the net with the most copper at the edge, and meets
  the GND border on every copper layer: 1.2 mm wide along the outline and 1.0 mm around the
  cut-out, the mask open over it, with a fence of GND vias in it. See
  [Edge Plating](Copper-And-Traces.md#117-edge-plating).
- **Its own stack-up.** Every height comes from Board Setup: 35 µm outer and 17.5 µm inner
  copper, two FR4 prepregs and a core, a 1.6 mm board and a 10 µm mask. From `report.txt`:

  ```text
  stack-up
    copper layers: F.Cu, In1.Cu, In2.Cu, B.Cu
    laminate 1.5300 mm (stackup dielectrics (+ inner copper); board total in file 1.6 mm)
    F.Cu     z +0.7650 .. +0.8000 mm  (foil 0.035 mm)
    In1.Cu   z +0.5475 .. +0.5650 mm  (foil 0.0175 mm)
    In2.Cu   z -0.5650 .. -0.5475 mm  (foil 0.0175 mm)
    B.Cu     z -0.8000 .. -0.7650 mm  (foil 0.035 mm)
    dielectric 1             prepreg  FR4        0.2000 mm  er 4.5  tan d 0.02   z +0.5650 .. +0.7650
    dielectric 2             core     FR4        1.0950 mm  er 4.5  tan d 0.02   z -0.5475 .. +0.5475
    dielectric 3             prepreg  FR4        0.2000 mm  er 4.5  tan d 0.02   z -0.7650 .. -0.5650
  ```

- **Colours from the stack-up.** The mask is KiCad's "Blue" and the silkscreen "White", so the mask
  parts come out
  <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/14328C.webp" width="12" height="12" align="absmiddle" alt=""> `#14328C`,
  over copper in visual mode
  <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/3C5AB4.webp" width="12" height="12" align="absmiddle" alt=""> `#3C5AB4`,
  and the silkscreen
  <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/F0F0EC.webp" width="12" height="12" align="absmiddle" alt=""> `#F0F0EC`
  ([Colorizing](Colorizing.md#122-colours-from-the-stack-up)).
- **One part per net.** 35 copper parts. `Copper_GND` is one closed solid made of the three
  planes, the border, the via fence, the plated edge and the barrels of its vias. The 50 Ω line is
  `Copper_RF` from the radio to L1 and `Copper_RF2` from L1 to the coax connector, each joined to
  its pads.
- **The logo in three materials.** On the back the KESE logo of `docs/logo/` is bare copper,
  copper under the mask, and silkscreen. In visual mode the bare copper takes the exposed copper
  colour and the copper under the mask reads through it in the lighter blue.
- **Keep-outs and finish.** Three rule areas are counted under `skipped` and make no copper, as
  intended. The stack-up's finish is ENIG; the finish is off by default, and
  `--set Finish.FINISH_ENABLED=True` adds the nickel and the gold on the bare copper
  ([ENIG](Copper-Finishings.md#1331-enig)).

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/logo.webp" width="61%" alt="The logo on the back close up in visual mode: the K mark and the name, beside the plated wall of the cut-out">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/logo_zoom.webp" width="37%" alt="The K mark closer still: the stem in white silkscreen, one arm in bare copper, the other arm in copper under the mask, a lighter blue than the mask around it">
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/layers_apart_simulation.webp" width="49%" alt="The board in simulation mode with its layers drawn apart, from the top: the top mask and silkscreen, F.Cu, the first prepreg, In1.Cu, the core with the via barrels and the plated edge, In2.Cu with its +3V3 and +5V halves, the second prepreg, B.Cu, and the bottom mask and silkscreen, each one closed solid">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/rf_module/layers_apart_visual.webp" width="49%" alt="The same in visual mode, where the file holds only the faces that can be seen: the top mask and silkscreen, the bare copper of F.Cu, the walls of the via bores and the plated edge; the faces of the bottom side look down, away from the camera, and the inner copper layers leave almost nothing">
</p>

<p align="center"><sub><b>Left:</b> simulation mode, every layer a closed solid. <b>Right:</b> visual mode, only the faces you can see.</sub></p>

| Part (simulation mode) | Triangles |
|---|---|
| `Copper_GND`: the planes, the border, the via fence, the plated edge | 333,000 |
| `Copper_+3V3` and `Copper_+5V`: the two halves of In2.Cu, with their tracks and pads | 50,596 |
| the other 33 copper parts | 30,872 |
| `Board_dielectric 1` to `3` | 186,452 |
| `Top Solder Mask`, `Bottom Solder Mask` | 229,814 |
| `Top Silkscreen`, `Bottom Silkscreen` | 56,278 |

## 5.2 HDI Radio Module

`Input/hdi_module.kicad_pcb`: a 6-layer radio module, built 1+4+1, one layer of microvias on each
side of a 4-layer core. A 64-ball BGA with a microvia in the pad of each inner ball and its
supplies on staggered buried vias, fanned out on In1.Cu to 43 castellated pads on three sides; a
USON-8 flash, a 2016 crystal, a buck converter making +1V1, and a matching network feeding a
meander antenna in a keep-out, its line referenced to In2.Cu through a cut in In1.Cu. GND on
In2.Cu, +3V3 on In3.Cu and a +1V1 island on In4.Cu; on the back an exposed GND pad, test pads
reached on In4.Cu, the pin numbers and the logo.

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/top_visual.webp" width="49%" alt="The HDI module from above in visual mode: the black mask, the meander antenna reading through it at the top, the BGA's pads, the flash U2 and the crystal Y1, and the castellated pads down both sides and along the bottom">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/bottom_visual.webp" width="49%" alt="The bottom in visual mode: the exposed GND pad, the logo, the pin numbers 1 to 43 beside the castellated pads, and the test pads TX, RX, BOOT, 3V3, EN and GND">
</p>

What this board shows:

- **Four kinds of via.** 71 microvias, from each outer layer to the layer under it; 34 blind and
  buried vias, buried from In1.Cu to In4.Cu and blind from an outer layer to In2.Cu or In3.Cu; and
  45 through vias. A via has its ring on the layers it spans and its barrel only between them
  ([Vias And Plated Holes](Copper-And-Traces.md#113-vias-and-plated-holes)).
- **Named laminates.** The dielectrics carry the glass styles and materials of the stack-up, each
  with its own εr and tanδ, and each becomes its own part, `Board_dielectric 1` to `5`, with those
  values in `materials.json` ([Material Properties](Material-Properties.md)):

  ```text
  dielectric 1             prepreg  1067       0.0650 mm  er 3.9  tan d 0.015   z +0.3525 .. +0.4175
  dielectric 2             core     IT-180A    0.2000 mm  er 4.3  tan d 0.016   z +0.1350 .. +0.3350
  dielectric 3             prepreg  1080       0.2000 mm  er 4.0  tan d 0.016   z -0.1000 .. +0.1000
  dielectric 4             core     IT-180A    0.2000 mm  er 4.3  tan d 0.016   z -0.3350 .. -0.1350
  dielectric 5             prepreg  1067       0.0650 mm  er 3.9  tan d 0.015   z -0.4175 .. -0.3525
  ```

- **Castellated pads.** The 43 plated holes that the board edge cuts through are castellations:
  each drill notches the edge, and its plating is a part-barrel on the notch wall, joined to the
  pad's net (`Copper.CASTELLATION = "auto"`; the file also says `(castellated_pads yes)`). See
  [Castellated Holes](Copper-And-Traces.md#116-castellated-holes).
- **Keep-outs.** The antenna's keep-out on every layer and the cut in In1.Cu under its line are
  rule areas: six of them, counted under `skipped`, and no copper inside them.
- **Black mask.** The stack-up's "Black" gives
  <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/121214.webp" width="12" height="12" align="absmiddle" alt=""> `#121214`,
  and over copper in visual mode
  <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/ColorSwatches/2E2E30.webp" width="12" height="12" align="absmiddle" alt=""> `#2E2E30`.
  The finish is immersion silver, built only with `Finish.FINISH_ENABLED = True`
  ([ImmersionSilver](Copper-Finishings.md#1336-immersionsilver)).

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/top_closeup.webp" width="51%" alt="The top close up in visual mode: the BGA's ball pads, a microvia in each inner pad, the flash U2, the crystal Y1 and the feed of the antenna">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/top_simulation.webp" width="47%" alt="The top in simulation mode: the black mask translucent over the copper, so the planes, the BGA's fan-out and the antenna show through it">
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/layers_apart_simulation.webp" width="49%" alt="The module in simulation mode with its layers drawn apart: the masks, the six copper layers and the five dielectrics, each one closed solid, the via barrels between the layers they join">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/layers_apart_visual.webp" width="49%" alt="The same in visual mode: the top mask and silkscreen, the bare copper of F.Cu with the castellated pads, and the walls of the via bores at the heights of their own layers; the inner copper layers leave almost nothing">
</p>

<p align="center"><sub><b>Left:</b> simulation mode, every layer a closed solid. <b>Right:</b> visual mode, only the faces you can see.</sub></p>

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/hdi_module/logo.webp" width="70%" alt="The bottom close up in visual mode: the logo beside the exposed GND pad, and the castellated pads with their pin numbers">
</p>

## 5.3 PCIe x1 Card

`Input/pcie_card.kicad_pcb`: a 4-layer PCIe x1 gigabit Ethernet card that powers its port (PoE),
within a low-profile card's size (PCI Express CEM Rev 2.0: at most 68.90 mm from the bottom of the
fingers to the top, and 167.65 mm long). A QFN-48 controller with its crystal, EEPROM and +1V0
LDO; the PCIe lane and clock pairs length matched by meanders, with AC coupling capacitors on the
card's transmit pair; an RJ45 jack with magnetics at the bracket, a 12 V fan header and an SMBus
temperature sensor. Across a 2 mm band kept clear on every copper layer, and a slot, the PoE side:
48 V in through a fuse to a PSE controller switching the port through a MOSFET, its own PGND and
+48V planes, and optocouplers across the slot. GND on F.Cu, In1.Cu and B.Cu, +3V3 and a +1V0
island on In2.Cu. Where finger B1 sits from the bracket and the outline next to the bracket are
estimates.

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/top_visual.webp" width="49%" alt="The PCIe card from above in visual mode: the green mask, the controller, the RJ45 footprint, the PoE side behind its dashed isolation line and slot, the logo, and the gold fingers on the tongue">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/bottom_visual.webp" width="49%" alt="The bottom in visual mode: the A side of the fingers, the tracks reading through the mask and the name in silkscreen">
</p>

What this board shows:

- **Gold fingers.** 18 fingers a side at a 1.00 mm pitch, side B on F.Cu and side A on B.Cu, on a
  tongue with its key and its corners chamfered 0.5 mm at 45°. PRSNT1# and PRSNT2# are 1 mm shorter
  and joined by a single trace, no plane runs under the fingers, and the mask is open over all of
  them. Each finger is a pad of its net, so the lane pairs, `+12V`, `+3V3` and GND end in the
  fingers.
- **Hard gold.** The stack-up's finish is hard gold. With `--set Finish.FINISH_ENABLED=True` it
  covers all the exposed copper, fingers and pads alike, since KiCad gives a board one finish
  ([HardGold](Copper-Finishings.md#1338-hardgold)).
- **The bevel is not modelled.** Board Setup's `(edge_connector bevelled)` asks the fabricator to
  bevel the fingers' edge. KESE does not read it, so the card's edge stays square.
- **An isolation barrier.** A rule area 2 mm wide keeps every copper layer clear between the logic
  side and the PoE side, and an 18 × 1.2 mm slot is milled through under it. The slot cuts every
  layer, so `Copper_PGND` and `Copper_+48V` stay apart from the logic side's parts.
- **Planes per net.** `Copper_GND` (187,288 triangles), `Copper_PGND` (71,564), `Copper_+3V3`
  (37,072) and `Copper_+48V` (17,888) are the biggest of the 52 copper parts.
- **Non-plated holes.** The bracket's two screw holes and the jack's two pegs are non-plated: their
  walls are bare laminate, with no plating and no ring.

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/fingers_closeup.webp" width="55%" alt="The tongue close up in visual mode: the B side fingers from B1, the key between them, and the chamfered corners of the tongue">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/isolation_closeup.webp" width="43%" alt="The isolation barrier close up in visual mode: the slot, the dashed line in silkscreen, the 2 mm band with no copper, the PSE controller U3, the MOSFET Q1 and the 48 V input">
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/layers_apart_simulation.webp" width="49%" alt="The card in simulation mode with its layers drawn apart: the masks, the four copper layers and the three dielectrics, each one closed solid; the PoE planes and the logic planes on each layer are apart across the band and the slot">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/layers_apart_visual.webp" width="49%" alt="The same in visual mode: the top mask and silkscreen, the bare copper of F.Cu with the fingers, and the walls of the via bores and the slot; the inner copper layers leave nothing">
</p>

<p align="center"><sub><b>Left:</b> simulation mode, every layer a closed solid. <b>Right:</b> visual mode, only the faces you can see.</sub></p>

<p align="center">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/top_simulation.webp" width="43%" alt="The top in simulation mode: the green mask translucent over the copper, the planes stopping at the isolation band">
<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/example_images/pcie_card/logo.webp" width="55%" alt="The logo on the front close up in visual mode: the K mark, the name, PoE+ GIGABIT NIC, PCIe x1, REV A, and a box for the serial number">
</p>

## 5.4 Exporting The Examples

```bash
cd Generator
python run_KESE.py                                                             # all three: simulation, GLB in metres, centred
python run_KESE.py Input/rf_module.kicad_pcb --for hfss                        # STEP in mm with KiCad's origin
python run_KESE.py Input/hdi_module.kicad_pcb --for viewer                     # visual mode for <model-viewer>
python run_KESE.py Input/pcie_card.kicad_pcb --set Finish.FINISH_ENABLED=True  # with the hard gold
python run_KESE.py Input/rf_module.kicad_pcb --set Run.COPPER_GROUPING=layer   # a copper part per layer
```

STEP files of these boards are large, 125 to 225 MB in mm, since every curve is written as flat
faces: see [Project Capabilities](Project-Capabilities.md#45-tested-sizes).

| Previous | Next |
|:---|---:|
| [Project Capabilities](Project-Capabilities.md) | [Working Principle](Working-Principle.md) |
