"""The hand values for each coil board's TX coil: what can be worked out from the copper alone, with no field solver.

    python scripts/theory.py                       reads each board from origin/FastHenry_Integration (git fetch first)
    python scripts/theory.py --check               also checks the method on the E01 loop against its textbook value

For each board it follows the TX copper in Boards/Stator.kicad_pcb from one terminal end to the other (the traces of
the TX net and the via that joins the two layers), and works out:

  L_dc   Neumann's double integral over that path, with the geometric mean distance (GMD) of a trace's rectangle,
         g = 0.2235 (w + t) (Grover), standing in for its width and thickness: the TX coil's inductance at DC, with
         the rotor away. Because a coil's inductance can only fall as the frequency rises or as copper comes near
         (the rotor's eddy currents), it is also the most the TX inductance can be at any air gap at 3.5 MHz.
  L_hf   the same with the current all at the copper's surface, as at high frequency: g is then the rectangle's
         logarithmic capacity (a boundary-element solve of the cross-section). With the rotor away, the TX inductance
         at 3.5 MHz lies between L_hf and L_dc, since the skin depth there equals the copper's thickness.
  R_dc   the copper's DC resistance, length / (sigma w t), summed over the traces: the least the TX resistance can be
         at any frequency and air gap (any other current pattern, and any eddy current in the rotor, loses more).

Both inductances are the open path's (partial) inductance, between the two stacked ends, as E01's reference is.
Writes data/theory.csv. GPL-3.0.
"""
from __future__ import annotations

import argparse
import math
import re
import resource
import time
from pathlib import Path

import numpy as np

import collect

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'
MU0 = 1.25663706212e-6               # H/m, CODATA 2018
NEAR_MM = 2.0                        # pieces closer than this along the copper are one conductor (GMD kernel)
GAUSS = 4                            # Gauss points along each piece


def items(text, kind):
    """Each (kind ...) item of a .kicad_pcb, as its text with balanced brackets."""
    out, i = [], 0
    while True:
        i = text.find(f'({kind} ', i)
        if i < 0:
            return out
        depth, j = 0, i
        while True:
            c = text[j]
            depth += (c == '(') - (c == ')')
            j += 1
            if depth == 0:
                break
        out.append(text[i:j])
        i = j


def field(item, name, n=1):
    m = re.search(rf'\({name}((?:\s+[^\s()]+){{{n}}})\)', item)
    return m.group(1).split() if m else None


def tx_path(text, net_name='TX', layer_z=None):
    """The TX copper as an ordered list of straight pieces (a, b, width, kind), from one free end to the other.
    Arcs are split into chords of at most 0.5 degrees. layer_z maps a copper layer to its centre's height (mm)."""
    nets = {m.group(2): m.group(1) for m in re.finditer(r'\(net (\d+) "([^"]*)"\)', text)}
    net = nets[net_name]
    edges = []

    def node(x, y, layer):
        return (round(float(x), 4), round(float(y), 4), layer)

    for it in items(text, 'segment') + items(text, 'arc'):
        if (field(it, 'net') or [None])[0] != net:
            continue
        layer = field(it, 'layer')[0].strip('"')
        w = float(field(it, 'width')[0])
        p0, p1 = [float(v) for v in field(it, 'start', 2)], [float(v) for v in field(it, 'end', 2)]
        pts = arc_points(p0, [float(v) for v in field(it, 'mid', 2)], p1) if it.startswith('(arc') else [p0, p1]
        edges.append((node(*p0, layer), node(*p1, layer), pts, layer, w))
    vias = []
    for it in items(text, 'via'):
        if (field(it, 'net') or [None])[0] != net:
            continue
        x, y = [float(v) for v in field(it, 'at', 2)]
        l1, l2 = [s.strip('"') for s in field(it, 'layers', 2)]
        vias.append((node(x, y, l1), node(x, y, l2), float(field(it, 'drill')[0])))
    adj = {}
    for k, e in enumerate(edges):
        adj.setdefault(e[0], []).append(('e', k))
        adj.setdefault(e[1], []).append(('e', k))
    for k, v in enumerate(vias):
        adj.setdefault(v[0], []).append(('v', k))
        adj.setdefault(v[1], []).append(('v', k))
    ends = [n for n, a in adj.items() if len(a) == 1]
    if len(ends) != 2 or any(len(a) > 2 for a in adj.values()):
        raise ValueError(f'the {net_name} copper is not one path: {len(ends)} free ends')
    start = sorted(ends, key=lambda n: (n[2] != 'F.Cu', n))[0]
    pieces, used, at = [], set(), start
    while True:
        nxt = [t for t in adj[at] if t not in used]
        if not nxt:
            break
        t = nxt[0]
        used.add(t)
        if t[0] == 'v':
            a, b, drill = vias[t[1]]
            far = b if at == a else a
            pieces.append(((at[0], at[1], layer_z[at[2]]), (far[0], far[1], layer_z[far[2]]), drill, 'via'))
            at = far
            continue
        n0, n1, pts, layer, w = edges[t[1]]
        far = n1 if at == n0 else n0
        if at != n0:
            pts = pts[::-1]
        z = layer_z[layer]
        for a, b in zip(pts[:-1], pts[1:]):
            pieces.append(((a[0], a[1], z), (b[0], b[1], z), w, 'trace'))
        at = far
    if at not in ends or at == start:
        raise ValueError('the walk along the copper did not reach the other end')
    return pieces


def arc_points(p0, pm, p1, max_deg=0.5):
    """Points along the circle through p0, pm, p1, from p0 to p1 through pm."""
    (x1, y1), (x2, y2), (x3, y3) = p0, pm, p1
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    ux = ((x1 * x1 + y1 * y1) * (y2 - y3) + (x2 * x2 + y2 * y2) * (y3 - y1) + (x3 * x3 + y3 * y3) * (y1 - y2)) / d
    uy = ((x1 * x1 + y1 * y1) * (x3 - x2) + (x2 * x2 + y2 * y2) * (x1 - x3) + (x3 * x3 + y3 * y3) * (x2 - x1)) / d
    r = math.hypot(x1 - ux, y1 - uy)
    a0, am, a1 = (math.atan2(p[1] - uy, p[0] - ux) for p in (p0, pm, p1))
    sweep = (a1 - a0) % (2 * math.pi)
    if (am - a0) % (2 * math.pi) > sweep:          # pm is not on the counter-clockwise way: go clockwise
        sweep -= 2 * math.pi
    n = max(2, math.ceil(abs(math.degrees(sweep)) / max_deg))
    return [(ux + r * math.cos(a0 + sweep * k / n), uy + r * math.sin(a0 + sweep * k / n)) for k in range(n + 1)]


def section(w, t, mode):
    """A trace's w x t cross-section, as the kernel sees it: its GMD g (mm) and the variances (mm^2) of where its
    current flows across the width and through the thickness.
      dc     the current spread evenly: g = 0.2235 (w + t) (Grover), variances w^2 / 12 and t^2 / 12;
      hf     the current pushed to the surface, as at high frequency: it then lies as charge does on a conductor, and
             g is the rectangle's logarithmic capacity (0.25 w for a thin strip, 0.5902 a for a square of side a),
             worked out here by a boundary-element solve of 2000 panels with the variances of that current;
      strip  E01's high-frequency reference: a strip of no thickness, g = w / 4."""
    if mode == 'dc':
        return 0.2235 * (w + t), w * w / 12, t * t / 12
    if mode == 'strip':
        return w / 4, w * w / 8, 0.0
    corners = [(-w / 2, -t / 2), (w / 2, -t / 2), (w / 2, t / 2), (-w / 2, t / 2)]
    p0, p1 = [], []
    for k in range(4):
        a, b = np.array(corners[k]), np.array(corners[(k + 1) % 4])
        nk = max(8, int(2000 * np.linalg.norm(b - a) / (2 * (w + t))))
        u = (1 - np.cos(np.linspace(0, math.pi, nk + 1))) / 2          # panels closer together at the corners
        p0 += [a + (b - a) * x for x in u[:-1]]
        p1 += [a + (b - a) * x for x in u[1:]]
    p0, p1 = np.array(p0), np.array(p1)
    c, h = (p0 + p1) / 2, np.linalg.norm(p1 - p0, axis=1)
    d = np.linalg.norm(c[:, None] - c[None], axis=2)
    np.fill_diagonal(d, 1.0)
    G = np.log(d) * h[None]
    np.fill_diagonal(G, h * (np.log(h / 2) - 1))                         # a panel's own ln r, integrated exactly
    n = len(h)
    A = np.zeros((n + 1, n + 1))
    A[:n, :n], A[:n, n], A[n, :n] = G, -1.0, h
    rhs = np.zeros(n + 1)
    rhs[n] = 1.0
    x = np.linalg.solve(A, rhs)                                          # charge q (total 1) at one potential V
    q = x[:n] * h
    return math.exp(x[n]), float(np.sum(q * c[:, 0] ** 2)), float(np.sum(q * c[:, 1] ** 2))


def quadrature(pieces, t_mm, mode, h_mm):
    """Gauss points along the path: position (m), tangent times weight (m), GMD (m), arc length (m), the unit
    vector across the trace's width, and the current's variances across the width and through the thickness (m^2)."""
    xg, wg = np.polynomial.legendre.leggauss(GAUSS)
    pos, dl, gmd, s, across, var = [], [], [], [], [], []
    sections = {}
    s0 = 0.0
    for a, b, w, kind in pieces:
        a, b = np.array(a) * 1e-3, np.array(b) * 1e-3
        length = float(np.linalg.norm(b - a))
        if length == 0:
            continue
        u = (b - a) / length
        if kind == 'via':
            g, vw, vt = w / 2, 0.0, 0.0                 # a plated barrel: a thin tube's GMD is its radius
            side = np.zeros(3)
        else:
            if w not in sections:
                sections[w] = section(w, t_mm, mode)
            g, vw, vt = sections[w]
            side = np.array([-u[1], u[0], 0.0])
        n = max(1, math.ceil(length / (h_mm * 1e-3)))
        for k in range(n):
            for xi, wi in zip(xg, wg):
                f = (k + (xi + 1) / 2) / n
                pos.append(a + (b - a) * f)
                dl.append(u * wi / 2 * length / n)
                gmd.append(g * 1e-3)
                s.append(s0 + f * length)
                across.append(side)
                var.append((vw * 1e-6, vt * 1e-6))
        s0 += length
    return (np.array(pos), np.array(dl), np.array(gmd), np.array(s), np.array(across), np.array(var))


def neumann(pieces, t_mm, mode='dc', h_mm=None):
    """Neumann's double integral over the path, mu0 / 4 pi  sum sum dl_i . dl_j K_ij, by Gauss points GAUSS to a
    piece of at most h_mm (a quarter of the trace width). Between points less than NEAR_MM apart along the copper,
    on the same trace, K = 1 / sqrt(r^2 + g_i g_j): the GMD method, a conductor's self-inductance being the mutual
    inductance of two filaments g apart. Farther along, between what are then two separate stretches of copper,
    K is 1 / r averaged over both cross-sections, to second order:
    1/r + (3 (r_w^2 U_w + r_z^2 U_z) - r^2 (U_w + U_z)) / (2 r^5), with r_w and r_z the parts of r across the
    width and through the thickness and U the summed variances of where the two currents flow."""
    if h_mm is None:
        h_mm = min(p[2] for p in pieces if p[3] == 'trace') * 0.25
    pos, dl, gmd, s, across, var = quadrature(pieces, t_mm, mode, h_mm)
    total, n, chunk = 0.0, len(pos), 1200
    for i0 in range(0, n, chunk):
        i1 = min(n, i0 + chunk)
        d = pos[i0:i1, None, :] - pos[None, :, :]
        r2 = np.einsum('ijk,ijk->ij', d, d)
        near = np.abs(s[i0:i1, None] - s[None, :]) < NEAR_MM * 1e-3
        rf = np.where(near, 1.0, r2)                    # the far kernel only where far (keeps it finite elsewhere)
        rw2 = np.einsum('ijk,ik->ij', d, across[i0:i1]) ** 2
        rz2 = d[..., 2] ** 2
        uw = var[i0:i1, None, 0] + var[None, :, 0]
        uz = var[i0:i1, None, 1] + var[None, :, 1]
        far = 1 / np.sqrt(rf) + (3 * (rw2 * uw + rz2 * uz) - rf * (uw + uz)) / (2 * rf ** 2.5)
        k = np.where(near, 1 / np.sqrt(r2 + gmd[i0:i1, None] * gmd[None, :]), far)
        total += float(np.sum((dl[i0:i1] @ dl.T) * k))
    return MU0 / (4 * math.pi) * total


def resistance(pieces, t_mm, sigma):
    """DC resistance of the traces, length / (sigma w t) each (the via's barrel adds well under a milliohm)."""
    r = 0.0
    for a, b, w, kind in pieces:
        if kind == 'trace':
            r += math.dist(a, b) * 1e-3 / (sigma * w * 1e-3 * t_mm * 1e-3)
    return r


def stackup(materials):
    """Copper thickness (mm), conductivity and each layer's centre height (mm) from KESE's materials.json."""
    cu = [p for p in materials['parts'].values() if p['role'] == 'copper']
    t = cu[0]['properties']['thickness_mm']
    sigma = cu[0]['properties']['conductivity_S_per_m']
    z0 = min(p['z_range_mm'][0] for p in cu)
    z1 = max(p['z_range_mm'][1] for p in cu)
    return t, sigma, {'F.Cu': z1 - t / 2, 'B.Cu': z0 + t / 2}


def board_theory(src, b):
    base = f'Examples/Inductive Coils/{b}'
    text = src.read(f'{base}/Boards/Stator.kicad_pcb')
    mats = src.json(f'{base}/3D_Geometry/Stator/materials.json')
    params = src.read(f'{base}/Boards/Parameters.txt') or ''
    if not text or not mats:
        return None
    t0 = time.time()
    t, sigma, z = stackup(mats)
    pieces = tx_path(text, 'TX', z)
    traces = [p for p in pieces if p[3] == 'trace']
    w = traces[0][2]
    length = sum(math.dist(p[0], p[1]) for p in traces)
    via = [p for p in pieces if p[3] == 'via']
    l_dc, l_hf = neumann(pieces, t, 'dc') * 1e9, neumann(pieces, t, 'hf') * 1e9
    period = re.search(r'spatial period at mid radius ([\d.]+) mm', params)
    return dict(board=b, L_dc_nH=l_dc, L_hf_nH=l_hf, R_dc_mohm=resistance(pieces, t, sigma) * 1e3, length_mm=length,
                width_mm=w, copper_mm=t, gmd_dc_mm=0.2235 * (w + t), gmd_hf_mm=section(w, t, 'hf')[0],
                layer_gap_mm=z['F.Cu'] - z['B.Cu'], vias=len(via), via_drill_mm=via[0][2] if via else None,
                sigma_S_per_m=sigma, skin_depth_um=1e6 / math.sqrt(math.pi * 3.5e6 * MU0 * sigma),
                period_mm=float(period.group(1)) if period else None, seconds=time.time() - t0,
                peak_memory_gb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 ** 2,
                source=src.ref or src.folder)


def check_e01(src):
    """The method on E01's open circular loop (two arcs between the round ends' centres), against its reference:
    references.arc_inductance's Neumann integral over the exact arc (collect.REFERENCES)."""
    base = 'Examples/E01_circular_loop'
    text = src.read(f'{base}/E01_circular_loop.kicad_pcb')
    mats = src.json(f'{base}/3D_Geometry/E01_circular_loop/materials.json')
    t, sigma, z = stackup(mats)
    pieces = tx_path(text, 'LOOP', z)
    l_dc, l_hf, l_strip = (neumann(pieces, t, m) * 1e9 for m in ('dc', 'hf', 'strip'))
    ref_dc, ref_hf = collect.REFERENCES[('E01_circular_loop', 'dc')], collect.REFERENCES[('E01_circular_loop', 'hf')]
    return dict(L_dc_nH=l_dc, ref_dc_nH=ref_dc, dc_off_pct=100 * (l_dc / ref_dc - 1), L_strip_nH=l_strip,
                ref_strip_nH=ref_hf, strip_off_pct=100 * (l_strip / ref_hf - 1), L_hf_nH=l_hf,
                gmd_hf_mm=section(0.5, t, 'hf')[0], t_mm=t)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--repo', default=str(collect.ROOT))
    ap.add_argument('--remote', default='origin')
    ap.add_argument('--dir', default=None, help='read the boards from this folder (a checkout) instead of git')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    branch = collect.SOLVERS[collect.REF]
    src = collect.Source(collect.REF, folder=a.dir, ref=f'{a.remote}/{branch}', repo=a.repo)
    if a.check:
        e = check_e01(src)
        print('E01', e)
        collect.write(DATA / 'theory_e01.csv', [e])
    rows = []
    for b in collect.BOARDS:
        r = board_theory(src, b)
        if r:
            rows.append(r)
            print(f"{b}: L_dc {r['L_dc_nH']:.2f} nH, L_hf {r['L_hf_nH']:.2f} nH, R_dc {r['R_dc_mohm']:.1f} mohm, "
                  f"{r['length_mm']:.1f} mm of copper")
    DATA.mkdir(exist_ok=True)
    collect.write(DATA / 'theory.csv', rows)


if __name__ == '__main__':
    main()
