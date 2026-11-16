# O01 Results

Run on the 4-core, 15 GB test machine (Ubuntu 24.04) with openEMS-Project master `e4cd015`
(openEMS `fc00235`, CSXCAD `fdff4b5`), KESE 3.4.0, on 16 November 2026. Every number below is in
`results.json` (and the `results_*.json` beside it for the other meshes and the other engine),
with the preflight's lines, the versions and the hashes of the code that made it.

## Expected Against What Came Out

The standard mesh (`results.json`, h 0.2 mm at the copper's edges, 411,424 cells, 79 s, 0.15 GB):

| f | Z0, openEMS | Z0, Hammerstad–Jensen | εeff from S21 | εeff, Kirschning–Jansen | Difference | εeff from port 1's probes | S21 | S21 from the dielectric's loss alone | S11 |
|---|---|---|---|---|---|---|---|---|---|
| 1 GHz | 50.71 Ω | 49.83 Ω | 3.367 | 3.318 | +1.5 % | 3.410 | −0.344 dB | −0.342 dB | −53.3 dB |
| 2 GHz | 50.95 Ω | 49.83 Ω | 3.376 | 3.341 | +1.1 % | 3.414 | −0.360 dB | −0.344 dB | −37.3 dB |
| 3 GHz | 51.31 Ω | 49.83 Ω | 3.395 | 3.368 | +0.8 % | 3.439 | −0.368 dB | −0.347 dB | −31.2 dB |
| 4 GHz | 51.70 Ω | 49.83 Ω | 3.421 | 3.397 | +0.7 % | 3.441 | −0.376 dB | −0.349 dB | −31.0 dB |

| Quantity | The reference's own accuracy | openEMS against it |
|---|---|---|
| Z0 at 1 GHz | Hammerstad–Jensen: within 1 % for a strip of no thickness [1]; the correction for the strip's thickness is an approximation of its own | +1.8 % |
| εeff from S21, 1 to 4 GHz | Hammerstad–Jensen's static εeff within 0.2 % [2], Kirschning–Jansen's dispersion within 0.6 % [3] | +0.7 to +1.5 % |
| εeff from the port's probes | as above | +1.3 to +2.8 % |
| S21 at 1 GHz | the dielectric's loss alone, Pozar, section 3.8 | 0.002 dB more loss |
| S11 | a line ended in about its own impedance | −31 to −53 dB |
| Preflight | | all 16 lines pass |

openEMS agrees with the closed-form references within 2 % everywhere. The 1 to 2 % that is left is
above the formulas' own accuracy, so it belongs to the FDTD model: the staircased strip and the
cells through the core (see the mesh study).

What is left over:

* **Z0 rises with frequency**, 50.7 to 51.7 Ω. Hammerstad and Jensen's Z0 is the static one; a
  microstrip's impedance does rise with frequency as the field draws into the substrate, and the
  1 GHz value (+1.8 %) is the fair comparison.
* **S21 loses a little more than the dielectric** above 2 GHz (0.02 to 0.03 dB). The copper is PEC
  here, so the rest is radiation from the line's ends and the ports, which grows with frequency, and
  the mismatch (0.004 dB at −31 dB).
* **εeff from the port's probes is 1.2 % above the one from S21.** The port takes a derivative over
  three probes 1.8 mm apart, 6 mm from its feed; S21's phase is taken over 38 mm. The S21 value is
  the one to quote.

## The Mesh Study

| Mesh | Cells | Time | Z0 at 1 GHz | εeff from S21 at 1 GHz | εeff from S21 at 4 GHz |
|---|---|---|---|---|---|
| h 0.2 mm, 6 cells through the core (standard) | 411,424 | 79 s | 50.71 Ω | 3.3668 | 3.4212 |
| h 0.1 mm at the copper's edges | 504,896 | 299 s | 50.48 Ω | 3.3661 | 3.4207 |
| largest cell in the core 0.13 mm instead of 0.25 (`--dielectric-cells 12`) | 438,256 | 108 s | 50.73 Ω | 3.3661 | 3.4202 |

Halving the spacing at the copper's edges moves εeff by 0.02 % and Z0 by 0.5 %; halving the cells
through the core moves εeff by 0.02 % and Z0 by 0.04 %. The mesh is converged well inside the 1 to 2 %
that separates openEMS from the closed-form references. Both differences point the same way, Z0 and
εeff a little high, as for a strip slightly thinner than 35 µm: the copper is one cell thick, and
the thickness correction in Hammerstad and Jensen's formulas is itself approximate. A rerun of the
same case gives the same numbers to 0.01 % (the CPU engine's threads can stop it a step apart).

## The Engines

openEMS's new CPU engine (`engine='cpu'`, marked experimental) and its default engine, on the same
mesh, give εeff and Z0 equal to four digits at every frequency (`results_h0.2_default.json`). The
CPU engine took 79 s, the default one 93 s, with an Elmer run sharing the machine for both.

## Bugs This Board Found

Each of these gave a wrong number that looked plausible, and each is fixed in the bridge.

| What it read | Cause | Fix |
|---|---|---|
| Z0 76 Ω | openEMS's microstrip port measures current with a probe of no height at the strip's underside, made for a strip of no thickness; KESE's copper is 35 µm thick, so the probe's loop of H ran through the copper and missed the current on its top and sides | `thick_strip_probes()` stretches each current probe round the whole strip |
| S21 −34 dB | S21 was taken from port 2's incident wave, which in openEMS's terms is the one going into the line | S_i1 is every port's outgoing (`uf_ref`) wave over port 1's incident one |
| εeff 3.72, 11 % high | the thirds rule was the wrong way round: h/3 outside the metal and 2h/3 inside, so the copper snapped onto the outer line through a half-covered cell. A microstrip in vacuum then read εeff 1.07 to 1.16 where it must read 1, with KESE's STL copper and with plain boxes alike; a parallel-plate line in vacuum read exactly c | h/3 inside the metal and 2h/3 outside, as openEMS's own tutorials have it (`MSL_NotchFilter.py`); the shielded vacuum strip then reads 0.99 to 1.03 |
| a ratio of 2.00 failing the 2:1 check | the port's plane on the board's edge, between the two thirds-rule lines, makes two cells of exactly 1:2, and the lines' rounding to 1 nm put the ratio a hair over 2 | the check passes 2.00 as printed |

The εeff hunt ruled out, one run each: the engine (CPU and default agree), the substrate (an air
substrate read 1.12), KESE's STL import (boxes read the same), the boundaries (PML read the same as
MUR), the feed's near field (moving the planes 25 mm in still read 1.08) and openEMS's time base
(the parallel plate).

## References

1. RF Essentials, *What is the Hammerstad–Jensen model and when is it accurate for microstrip impedance?*,
   https://rfessentials.com/rf-knowledge-base/what-is-the-hammerstad-jensen-model-and-when-is-it-accurate-for-microstrip-imped/
2. Qucs technical documentation, *Microstrip line: quasi-static characteristic impedance and effective permittivity*,
   https://qucs.sourceforge.net/tech/node75.html (E. Hammerstad and Ø. Jensen, *Accurate Models for Microstrip
   Computer-Aided Design*, IEEE MTT-S 1980)
3. Qucs technical documentation, *Microstrip line: dispersion*, https://qucs.github.io/tech/node77.html (M. Kirschning and R. H. Jansen, *Accurate model for effective dielectric
   constant of microstrip with validity up to millimetre-wave frequencies*, Electronics Letters 18, 1982)
4. D. M. Pozar, *Microwave Engineering*, 4th ed., section 3.8 (microstrip): the dielectric loss, the homogeneous line's loss times the filling factor εr(εeff − 1) / (εeff(εr − 1)).
5. openEMS, `python/Tutorials/MSL_NotchFilter.py`: the thirds rule, `third_mesh = [2*res/3, -res/3]/4` added
   outward from each strip edge.

