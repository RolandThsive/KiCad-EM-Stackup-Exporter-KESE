# 39. OpenEMS Implementation Accuracy

Where the openEMS bridge's errors come from, how big each one measured on O01, and what the bridge
leaves out of the physics. Every number here is from O01's runs on the `OpenEMS_Integration` branch
(`Examples/O01_microstrip/results*.json`).

## 39.1 The Error Budget On O01

Each line changes one thing and keeps the rest. The differences are at 1 GHz unless a range is given.

| Source | Test | εeff from S21 | Z0 |
|---|---|---|---|
| Spacing at the copper's edges | h 0.2 mm against 0.1 mm | 0.01 % (0.02 % at 4 GHz) | 0.5 % |
| Cells through the core | 6 against 12 | 0.02 % (0.03 % at 4 GHz) | 0.06 % |
| The engine | CPU engine against the default engine | 0.003 % (none from 2 to 4 GHz) | 0.005 % |
| The pulse and the stop | cosine pulse to −40 dB against the DC-free pulse to −50 dB | 0.07 % at 1 GHz, none from 2 to 4 GHz | 0.03 % |
| A rerun of the same case | the CPU engine's threads can stop it a step apart | 0.01 % | 0.01 % |
| **openEMS against the closed forms** | Kirschning–Jansen, Hammerstad–Jensen | **+1.4 % (+0.7 % at 4 GHz)** | **+1.7 %** |
| The closed forms' own accuracy | their authors' figures | 0.2 % static, 0.6 % with dispersion | about 1 % |

The mesh, the engine and the stop together move the numbers by less than a tenth of the gap to the
closed forms, so the gap is not a matter of resolution. It is larger than the formulas' own error,
so it belongs to the model. Both numbers come out a little high, as they would for a strip slightly
thinner than its 35 µm: the copper is one cell thick in z, and Hammerstad and Jensen's correction
for a strip's thickness is an approximation of its own. That reading is the most likely one, not a
proven one: no run with several cells through the copper has been made yet.

## 39.2 Two Ways To εeff

| f | εeff from S21's phase | εeff from port 1's probes | Difference |
|---|---|---|---|
| 1 GHz | 3.364 | 3.415 | +1.5 % |
| 2 GHz | 3.376 | 3.414 | +1.1 % |
| 3 GHz | 3.395 | 3.439 | +1.3 % |
| 4 GHz | 3.421 | 3.441 | +0.6 % |

A port finds the propagation constant from three probes 1.8 mm apart, 6 mm from its feed; S21's
phase is taken over the 38 mm between the two ports' measurement planes. The longer base is the
better measurement, so quote εeff from S21. The port's own value is still the only one a single port
gives, and Z0 comes from the same probes.

## 39.3 What The Bridge Leaves Out

| What | In the bridge | What it does to the numbers |
|---|---|---|
| Conductor loss and skin effect | the copper is PEC (no loss, current on its surface only) | S21 holds the dielectric's loss and radiation only. A line's real loss at GHz is larger by the copper's share; see [Elmer vs openEMS](Elmer-vs-OpenEMS.md#423-which-one-for-what) |
| The dielectric's loss against frequency | a conductivity κ = 2π f0 ε₀ εr tan δ, exact at f0 | tan δ is right at f0 only and falls as f0/f elsewhere: on O01, tan δ 0.02 at 3 GHz is 0.06 at 1 GHz and 0.015 at 4 GHz, so the line loses about the same 0.34 dB at every frequency. FR-4's measured tan δ stays nearly constant over a wide band [1], so the real line's dielectric loss grows with frequency. The S21 check uses the bridge's law, so it checks openEMS's sums, not FR-4 |
| εr against frequency | one εr for the whole band | a real dielectric's εr is not constant over a wide band either; give the εr at the band's centre |
| Radiation | open MUR boundaries, 15 mm of air | radiation from the line's ends and the ports shows as extra loss in S21: 0.02 to 0.03 dB above the dielectric's loss from 2 to 4 GHz on O01 |
| The copper's shape | staircased onto the rectilinear mesh, one cell thick | round ends and arcs become steps; straight edges get the thirds rule's lines ([OpenEMS Implementation Troubleshooting](OpenEMS-Implementation-Troubleshooting.md#411-wrong-numbers-that-look-right)) |

## 39.4 What To Trust

| Quantity | On a board like O01 |
|---|---|
| Z0 | within about 2 % (+1.7 % on O01) |
| εeff from S21 | within about 1.5 % (+0.7 to +1.4 % on O01) |
| εeff from a port's probes | within about 3 % (+1.3 to +2.9 % on O01) |
| S21 of a matched line | the dielectric's loss as modelled (39.3) to 0.002 dB at 1 GHz, plus radiation above 2 GHz |
| S11 | the reflection of the ports and the line: −31 to −53 dB on O01 |

These hold for what O01 has proved, a straight microstrip. A board with couplings, resonances or
radiation of its own needs its own mesh study: run it again with `--h-edge` halved and with
`--dielectric-cells` doubled ([OpenEMS Implementation Simulating Your Own Board](OpenEMS-Implementation-Simulating-Your-Own-Board.md#365-the-command-line)),
and quote the numbers only when they stop moving.

A wideband dielectric of constant loss tangent, such as Djordjevic and Sarkar's model [1], would need
openEMS's dispersive materials (several Debye terms fitted to it); the bridge does not do that yet.

## 39.5 References

1. A. R. Djordjevic, R. M. Biljić, V. D. Likar-Smiljanić and T. K. Sarkar, *Wideband frequency-domain
   characterization of FR-4 and time-domain causality*, IEEE Transactions on Electromagnetic
   Compatibility 43 (4), 662–667, 2001, doi:10.1109/15.974647 (read from its abstract and index
   record; KiCad implements the same model, `DIELECTRIC_DJORDJEVIC_SARKAR`)

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Test Board Results](OpenEMS-Implementation-Test-Board-Results.md) | [OpenEMS Implementation Hardware](OpenEMS-Implementation-Hardware.md) |
