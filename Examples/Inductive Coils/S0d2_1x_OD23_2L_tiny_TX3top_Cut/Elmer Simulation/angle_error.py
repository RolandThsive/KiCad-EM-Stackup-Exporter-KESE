"""The angle error of a SIN and COS pair: how far the angle a decoder reads from the two curves is from the true rotor
angle. simulation.py calls it after every solve and writes the result into ../Results/SINCOS_Results.md; run on its own
it prints every air gap's errors and rewrites that page. Each air gap's results sit in their own folder in ../Results,
named for the gap with the point written as d: 1mm_AirGap, 0d5mm_AirGap.

    python angle_error.py                      every gap's results in ../Results, then the page rewritten
    python angle_error.py ../Results/1mm_AirGap/results_gap1mm.json

How it is worked out, for the angles solved so far:

  1. Each channel gets its best sine over the rotor's period: M(t) = offset + amplitude x sin(t + phase), t the rotor
     angle scaled so that one period of the rotor is 360 degrees (electrical degrees).
  2. Each channel's offset is taken out and it is divided by its amplitude, so both swing between -1 and +1. This is
     what a decoder chip's offset and gain calibration does.
  3. The angle is read back as atan2(SIN, COS), COS's sign taken so that it is the cosine to SIN's sine.
  4. The error at each angle is that reading less the true angle, less the average of all of them (a fixed offset
     only moves where zero is). The rms and the worst of them are the angle error.

The phase between the two fits is given too: 90 degrees is perfect quadrature, and a decoder that only calibrates
offset and gain sees any difference from 90 as error. The fit uses the same points as the error, so with few angles the
error is a measure of how far the solves are from a perfect sine and cosine pair, not of the sensor's harmonics.
This script is GPL-3.0 as the bridge.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
METHOD = ("Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each "
          "channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a "
          "decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at "
          "each angle is that reading less the true angle, less the average of all of them, since a fixed offset "
          "only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points "
          "as the error, so it measures how far the solves are from a perfect sine and cosine pair. "
          "[`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.")


def gap_folder(gap):
    """The folder of one air gap's results inside Results/: 1mm_AirGap, 0d5mm_AirGap (the point written as d)."""
    return f'{gap:g}mm_AirGap'.replace('.', 'd')


def results_files(results):
    """Every air gap's results file in Results/ (the default mesh and solver), as (gap, path), the largest gap first."""
    out = []
    for p in Path(results).glob('*_AirGap/results_gap*mm.json'):
        m = re.fullmatch(r'results_gap([0-9.]+)mm\.json', p.name)
        if m:
            out.append((float(m.group(1)), p))
    return sorted(out, key=lambda x: -x[0])


def sine_fit(angles, values, period=360.0):
    """The best fit offset + amplitude x sin(t + phase), t the angle scaled to 360 over `period`: offset, amplitude,
    phase (degrees) and the rms of what is left (None with three points or fewer, which a sine always passes)."""
    t = np.radians(np.asarray(angles, float) * 360.0 / period)
    y = np.asarray(values, float)
    A = np.c_[np.ones_like(t), np.sin(t), np.cos(t)]
    (a, b, c), *_ = np.linalg.lstsq(A, y, rcond=None)
    rest = y - A @ np.array([a, b, c])
    return dict(offset=float(a), amplitude=math.hypot(b, c), phase_deg=math.degrees(math.atan2(c, b)),
                rms_left=float(np.sqrt(np.mean(rest ** 2))) if len(y) > 3 else None)


def angle_error(angles, msin, mcos, period=360.0):
    """The error at each angle, in electrical degrees, with its rms and peak and the phase between SIN and COS, or
    None with fewer than five angles (a sine and cosine pair has six unknowns)."""
    if len(angles) < 5:
        return None
    fs, fc = sine_fit(angles, msin, period), sine_fit(angles, mcos, period)
    u = np.radians(np.asarray(angles, float) * 360.0 / period + fs['phase_deg'])
    s = (np.asarray(msin, float) - fs['offset']) / fs['amplitude']            # sin(u)
    c = (np.asarray(mcos, float) - fc['offset']) / fc['amplitude']            # sin(u + d), d near +90 or -90
    d = math.radians(fc['phase_deg'] - fs['phase_deg'])
    e = np.angle(np.exp(1j * (np.arctan2(s, math.copysign(1.0, math.sin(d)) * c) - u)))
    e = np.degrees(np.angle(np.exp(1j * (e - np.angle(np.mean(np.exp(1j * e)))))))
    return dict(per_angle={float(a): float(x) for a, x in zip(angles, e, strict=True)},
                rms=float(np.sqrt(np.mean(e ** 2))), peak=float(np.abs(e).max()),
                sin_to_cos_deg=abs((math.degrees(d) + 180) % 360 - 180), points=len(e),
                mechanical_per_electrical=period / 360.0)


def from_results(path, period=360.0):
    """The angles and the two curves (nH) of a results file, and their angle error."""
    res = json.loads(Path(path).read_text())
    runs = sorted((r for r in res['runs'] if r['rotor_deg'] != 'away'), key=lambda r: r['rotor_deg'])
    ang = [r['rotor_deg'] for r in runs]
    ms = [r['solve']['coils']['SIN']['M'] * 1e9 for r in runs]
    mc = [r['solve']['coils']['COS']['M'] * 1e9 for r in runs]
    return ang, ms, mc, angle_error(ang, ms, mc, period)


def main():
    spec = json.loads((HERE / 'test_spec.json').read_text())
    period = spec['sets'][0].get('rotor_period_mech_deg', 360.0)
    files = [Path(p) for p in sys.argv[1:]] or [p for _, p in results_files(HERE.parent / 'Results')]
    for f in files:
        ang, _, _, err = from_results(f, period)
        print(f'{f.name}: {len(ang)} angles')
        if not err:
            print('  fewer than five angles: no angle error yet')
            continue
        for a, x in err['per_angle'].items():
            print(f'  {a:7g} deg  {x:+6.2f} deg')
        print(f"  rms {err['rms']:.2f} deg, peak {err['peak']:.2f} deg (electrical); SIN to COS "
              f"{err['sin_to_cos_deg']:.2f} deg")
    if not sys.argv[1:]:
        sys.argv = sys.argv[:1]
        import simulation                                      # the page is simulation.py's; it calls back here
        simulation.report()


if __name__ == '__main__':
    main()
