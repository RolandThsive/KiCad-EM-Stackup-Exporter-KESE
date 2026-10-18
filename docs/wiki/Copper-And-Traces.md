# 11. Copper And Traces

Copper is what the model is for: one closed solid per net, with every layer's traces, pads and
zone fills joined to its vias and plated holes. `Generator/BoardBreakdown.py` collects and
resolves the copper per layer and net; `Generator/Geometry/Copper.py` turns it into prisms; the
settings are in `Parameters/Copper_Parameters.py`.

<!-- Pictures wanted for this page (made by Roland):
     Copper 1: one net's solid alone (traces on two layers joined by vias).
     Copper 2: a via in cross-section: drill, plated wall, annular rings, the outer copper capping
               the barrel, an inner layer drilled through.
     Copper 3: the etch-factor trapezoid at ETCH_FACTOR 0 and 0.5, ETCH_STEPS 4.
     Copper 4: a castellated edge and an edge-plated board edge. -->

## 11.1 What Makes Copper

Per copper layer, these items are collected with their net:

| Item | Shape |
|---|---|
| `segment` (track) | the centre line thickened by the track width, round ends |
| `arc` (arc track) | the arc flattened to `Geometry.ARC_STEP_DEG` steps, thickened |
| `via` | a disc of the via's size on **every** layer it spans (see 11.3) |
| `pad` | the pad shape (circle, rect, oval, roundrect, trapezoid, custom with anchor and primitives) at its position and angle, with the drill offset, on each copper layer the pad lists (`*.Cu`, `F&B.Cu` expanded) |
| `zone` fill | the `filled_polygon` polygons stored in the file |
| `gr_*` / `fp_*` graphics on a copper layer | lines and arcs thickened by their stroke width; filled shapes filled; unfilled closed shapes as their outline stroke |
| text on a copper layer | the stroke-font glyphs, as on silkscreen |

Then, per layer and per net: union, clip to the outline, subtract the holes, simplify by
`Geometry.SIMPLIFY_TOLERANCE_MM` (0.5 µm), move to the board frame and snap to the grid.

> [!WARNING]
> **Zones must be filled in KiCad.** KESE takes the fill polygons KiCad stores in the file,
> which exist only after the zones have been filled (press **B**) and the file saved. A zone with
> no stored fill produces **no copper**; the run warns and `report.txt` counts it under
> `zones with no fill (unfilled - press B in KiCad and save)`. Keep-out and rule areas are
> listed separately and are not an error.

### 11.1.1 Nets

In KiCad 6 to 9 an item carries a net **number** that is looked up in the file's net table; KiCad
10 writes the net **name** directly, and KESE reads both. Copper with no net (board graphics,
unconnected pads, net 0) is named `Copper.NO_NET_NAME`, `no_net` by default, so it becomes
`Copper_no_net`.

Copper of different nets never overlaps on a real board. If the file has an overlap (two nets'
shapes drawn on top of each other), the net that was resolved first keeps the shared area, so the
solids stay disjoint.

## 11.2 Grouping And Part Names

| `Run.COPPER_GROUPING` | Part per | Name | Plating |
|---|---|---|---|
| `"net"` (default) | net | `Copper_<net>` | inside the net's part |
| `"layer"` | layer | `Copper_F.Cu`, `Copper_In1.Cu`, ... | separate `Plating` part |
| `"merged"` | all copper | `Copper` | inside it |

With `"net"` grouping the whole net is one closed body: every layer's copper, every annular ring
and every barrel. That is what a solver needs to assign one port or one conductor to a net.

## 11.3 Vias And Plated Holes

A via contributes:

- a round **pad** (annular ring) of the via's size on every copper layer from its start layer to
  its end layer (through vias on all layers; blind, buried and micro vias on the layers they
  span);
- a **hole** of the via's drill through the same span;
- a plated **barrel**: the ring between the drill and the drill shrunk by `Copper.VIA_WALL_MM`
  (25 µm by default), running between the copper layers it joins.

A through-hole pad contributes its pad shape on the listed layers and a barrel with
`Copper.PTH_WALL_MM`. Oval (slot) drills become slot-shaped barrels.

How the barrel meets the layers (so that the solids only touch):

- **Outer layers cap the barrel.** The outer copper is cut by the *bore* (drill minus wall), so
  the annular ring's copper covers the top of the barrel like a lid. The barrel runs from the
  bottom of `F.Cu` to the top of `B.Cu`.
- **Inner layers are drilled through.** Inner copper is cut by the full *drill*, and the barrel
  continues through the inner layer's band. The inner ring touches the barrel from the side.

Barrels of the same span and net are one region; with `"net"` grouping they go into the net's
part, with `"layer"` grouping into `Plating`.

### 11.3.1 Remove Unused Layers

KiCad's via option "remove unused layers" drops the annular rings on layers where nothing
connects. With `Copper.HONOUR_REMOVE_UNUSED_LAYERS = True` (the default), KESE keeps a via's
ring on such a layer only when other copper of the board already touches it there; the start
and end layers are kept when the via says `keep_end_layers`. `report.txt` counts the rings
removed under `via rings removed on unconnected layers`.

### 11.3.2 Via Tenting

Tenting decides whether the solder mask covers the via (the mask has no opening over it) or is
open. `Copper.VIA_TENTING`:

| Value | Meaning |
|---|---|
| `"file"` (default) | follow the board: KiCad 9 / 10 `(tenting ...)` in Board Setup and per via, else the older plot setting `viasonmask`, else KiCad's default (tented) |
| `"tented"` | mask over every via |
| `"open"` | mask open over every via, with the pad-to-mask clearance |

`report.txt` states the source on the `vias:` line (`board setup (tenting)`, `plot setting
viasonmask`, `KiCad default (vias tented)`).

## 11.4 Copper Thickness And Plating

| Layer | Thickness |
|---|---|
| outer (`F.Cu`, `B.Cu`) | foil (`Copper.DEFAULT_OUTER_FOIL_MM` or the stack-up) + `Copper.OUTER_PLATING_ADDED_MM` |
| inner | foil (`Copper.DEFAULT_INNER_FOIL_MM` or the stack-up) |

`OUTER_PLATING_ADDED_MM` is the copper that electroplating adds to the outer layers during hole
plating ("finished copper"), typically 20 µm. It is 0 by default so that the geometry matches
KiCad; set it for an as-fabricated model. Each copper part records `foil_mm` and
`plating_added_mm` in `materials.json`.

## 11.5 Etch Factor

Real traces are trapezoids: etching undercuts the resist, so a trace is narrower at its free
face than at its foot. `Copper.ETCH_FACTOR` (0 by default, a rectangle as in KiCad) leans each
side wall in by `ETCH_FACTOR × copper thickness` over the copper height. The trapezoid is built as
`Copper.ETCH_STEPS` stacked slices (4 by default), each inset a little more than the one below.

- On `F.Cu` the foot is at the bottom (on the laminate), on `B.Cu` at the top.
- Inner layers are etched only with `Copper.ETCH_APPLY_TO_INNER_LAYERS = True`; their foot faces
  the board centre (the core side).

An etch factor of 0.5 with 35 µm copper makes each wall lean in by 17.5 µm across the height.

## 11.6 Castellated Holes

A castellation is a plated hole that the board edge cuts through (module edge connectors). KiCad
has no per-pad flag; KESE finds them as plated holes whose drill crosses `Edge.Cuts`. Then
`Copper.CASTELLATION`:

| Value | Meaning |
|---|---|
| `"auto"` (default) | every plated hole crossing the outline is a castellation: the drill notches the edge and its plating is a part-barrel on the notch wall, joined to the hole's net, with wall `Copper.CASTELLATION_WALL_MM` |
| `"file"` | as `"auto"`, but only when the stack-up says `(castellated_pads yes)`; otherwise a note in `report.txt` says how to turn it on |
| `"off"` | holes crossing the edge are not plated at all |

The XIAO example has 14 castellated holes; `report.txt` counts them under `castellated holes
(plated holes cut by the board edge)`.

## 11.7 Edge Plating

Edge plating is copper on the routed board edge (edge-card connectors, RF shielding).
`Copper.EDGE_PLATING`: `"file"` (default) follows the stack-up's `(edge_plating yes)`, `"yes"` and
`"no"` force it. When on:

- a band `Copper.EDGE_PLATING_WALL_MM` wide just inside the outline becomes copper from the
  bottom of `B.Cu` to the top of `F.Cu`, interrupted by every hole and castellation that crosses
  the edge;
- the band takes the laminate's place at the edge, like a barrel in its drill;
- the band belongs to one net, `Copper.EDGE_PLATING_NET`: `"auto"` picks the named net with the
  most copper touching the band (or `no_net`), or give a net name such as `"GND"`;
- copper of **other** nets inside the band is moved to the edge net, since edge plating shorts
  everything that reaches the edge; `report.txt` lists what was moved.

## 11.8 Electrical Properties

Every copper and plating part carries `conductivity_S_per_m` (`Copper.COPPER_CONDUCTIVITY_S_PER_M`,
5.8 × 10⁷ S/m) and `surface_roughness_um` (`Copper.COPPER_SURFACE_ROUGHNESS_UM`, 0 = ignore; a
solver setting, not geometry) in `materials.json`. See
[Material Properties](Material-Properties.md).

## 11.9 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `DEFAULT_OUTER_FOIL_MM`, `DEFAULT_INNER_FOIL_MM` | `0.035`, `0.035` | mm > 0 | Foil thickness when the stack-up gives none (1 oz = 0.035, 0.5 oz = 0.0175) |
| `USE_STACKUP_COPPER_THICKNESS` | `True` | bool | Stack-up copper thickness wins when present |
| `OUTER_PLATING_ADDED_MM` | `0.0` | mm ≥ 0 | Plating added to the outer layers (typical 0.020) |
| `VIA_WALL_MM`, `PTH_WALL_MM` | `0.025`, `0.025` | mm > 0 | Plated wall of vias and through-hole pads (typical 0.020 to 0.025) |
| `ETCH_FACTOR` | `0.0` | ≥ 0 | Side-wall lean per unit of copper thickness; 0 = rectangular |
| `ETCH_STEPS` | `4` | int ≥ 1 | Slices per trapezoid |
| `ETCH_APPLY_TO_INNER_LAYERS` | `False` | bool | Etch the inner layers too |
| `CASTELLATION` | `"auto"` | `"auto"` / `"file"` / `"off"` | How plated holes crossing the edge are treated |
| `CASTELLATION_WALL_MM` | `0.025` | mm > 0 | Plated wall of a castellation |
| `EDGE_PLATING` | `"file"` | `"file"` / `"yes"` / `"no"` | Copper on the board edge |
| `EDGE_PLATING_WALL_MM` | `0.025` | mm > 0 | Width of the edge band |
| `EDGE_PLATING_NET` | `"auto"` | `"auto"` or a net name | Which net the edge copper belongs to |
| `VIA_TENTING` | `"file"` | `"file"` / `"tented"` / `"open"` | Mask over vias |
| `HONOUR_REMOVE_UNUSED_LAYERS` | `True` | bool | Drop via rings on layers nothing connects to |
| `COPPER_CONDUCTIVITY_S_PER_M` | `5.8e7` | S/m | Written to `materials.json` |
| `COPPER_SURFACE_ROUGHNESS_UM` | `0.0` | µm ≥ 0 | Written to `materials.json`; 0 = ignore |
| `NO_NET_NAME` | `"no_net"` | text | Name of copper that belongs to no net |

| Previous | Next |
|:---|---:|
| [Board](Board.md) | [Colorizing](Colorizing.md) |
