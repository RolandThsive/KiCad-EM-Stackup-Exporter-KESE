"""The openEMS bridge: KESE's STL export as a CSXCAD model, a mesh placed by the copper's edges, ports, a preflight
check of the grid and the ports, one FDTD run, and the S-parameters and line data read back.

KESE stays a geometry exporter: the bridge runs it as a program (run_KESE.py from $KESE_PATH or the branch's
3D_Geometry folder) with its `openems` preset and reads what it writes: one closed STL per net and per dielectric,
in mm, with y up (y_model = -y_kicad) and z = 0 in the middle of the board, and materials.json.

Four habits, taken from SPIKE (github.com/krishna-swaroop/SPIKE), are part of every run:
  * a preflight of the grid (largest cell against the shortest wavelength, the ratio of neighbouring cells) that
    stops a run that would be wrong before it starts;
  * a check that every port sits on copper of its own net, with its reference copper under it;
  * the hash of the simulation script and of the bridge in the results, so a number can be traced to its code;
  * only the S-parameters that were measured: one excited port gives one column, S_i1, and nothing else.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INSTALL = ROOT / 'Solver_OpenEMS' / 'install'
C0 = 299792458.0
EPS0 = 8.8541878128e-12


def kese_script():
    """run_KESE.py: $KESE_PATH (the file or its folder), else the branch's 3D_Geometry/run_KESE.py."""
    env = os.environ.get('KESE_PATH')
    cands = [Path(env)] if env else []
    cands.append(ROOT / '3D_Geometry')
    for c in cands:
        c = c / 'run_KESE.py' if c.is_dir() else c
        if c.is_file():
            return c
    raise FileNotFoundError("KESE not found: copy main's Generator into 3D_Geometry (see its README) "
                            "or set KESE_PATH to run_KESE.py")


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def kese_export(board, cache_root, extra=(), log=print):
    """KESE's openems export of a board, reused while the board file and the extra settings are unchanged."""
    board = Path(board)
    key = file_hash(board) + ('_' + hashlib.sha256(' '.join(extra).encode()).hexdigest()[:6] if extra else '')
    out = Path(cache_root) / f'{board.stem}_{key}'
    found = sorted(out.glob(f'{board.stem}/simulation_*/materials.json'))
    if found:
        log(f'KESE export reused: {found[-1].parent}')
        return found[-1].parent
    cmd = [sys.executable, str(kese_script()), str(board), '--for', 'openems', '--out', str(out)]
    for s in extra:
        cmd += ['--set', s]
    log('KESE: ' + ' '.join(Path(c).name if i == 1 else c for i, c in enumerate(cmd)))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f'KESE failed on {board}:\n{r.stdout}\n{r.stderr}')
    for line in r.stdout.splitlines():
        if 'Verifier' in line:
            log('KESE ' + line.strip())
    found = sorted(out.glob(f'{board.stem}/simulation_*/materials.json'))
    if not found:
        raise RuntimeError(f'KESE wrote no materials.json for {board}')
    return found[-1].parent


def kese_version():
    try:
        r = subprocess.run([sys.executable, str(kese_script()), '--version'], capture_output=True, text=True)
        return r.stdout.strip() or r.stderr.strip()
    except Exception as e:              # noqa: BLE001
        return f'unknown ({e})'


def versions():
    import platform
    out = {'python': platform.python_version(), 'kese': kese_version()}
    for mod in ('numpy', 'scipy', 'shapely', 'trimesh', 'openEMS', 'CSXCAD'):
        try:
            m = __import__(mod)
            out[mod] = getattr(m, '__version__', 'installed')
        except Exception:                # noqa: BLE001
            pass
    try:
        r = subprocess.run([str(INSTALL / 'bin' / 'openEMS'), '--version'], capture_output=True, text=True,
                           timeout=30)
        line = next((l for l in (r.stdout + r.stderr).splitlines() if 'Version' in l or 'openEMS' in l), '')
        out['openEMS_binary'] = line.strip() or 'unknown'
    except Exception:                    # noqa: BLE001
        out['openEMS_binary'] = 'unknown'
    return out


def code_hashes(*scripts):
    """The hash of each script given and of every file of the bridge: what a result was made with."""
    files = [Path(s) for s in scripts] + sorted(HERE.glob('*.py'))
    return {f.name: file_hash(f) for f in files}


@dataclass
class Part:
    name: str
    role: str                 # copper, board, mask
    net: str | None
    layer: str | None
    z: tuple                  # (z0, z1) in mm
    stl: Path
    props: dict
    polys: object = None      # shapely geometry: the section at mid height, in model xy (copper only)
    bounds: tuple = None      # (x0, y0, z0, x1, y1, z1) of its STL, mm


def load(export):
    """The parts of a KESE export, with each copper part's outline (its section at mid height)."""
    import shapely
    import trimesh
    export = Path(export)
    mats = json.loads((export / 'materials.json').read_text())
    parts = []
    for name, info in mats['parts'].items():
        stl = export / 'stl' / info['file_names']['stl']
        if not stl.exists():
            continue
        p = Part(name=name, role=info['role'], net=info.get('net'), layer=info.get('layer'),
                 z=tuple(info['z_range_mm']), stl=stl, props=info.get('properties', {}))
        mesh = trimesh.load(stl, force='mesh')
        p.bounds = tuple(float(v) for v in np.r_[mesh.bounds[0], mesh.bounds[1]])
        if p.role == 'copper':
            zs = sorted(set(np.round(mesh.vertices[:, 2], 6)))
            geoms = [section(mesh, (a + b) / 2) for a, b in zip(zs[:-1], zs[1:])]
            geoms = [g for g in geoms if g is not None]
            p.polys = shapely.unary_union(geoms) if geoms else None
        parts.append(p)
    return parts, mats


def section(mesh, z):
    """A closed triangle mesh's cross-section at height z, as shapely geometry (holes kept), or None."""
    import shapely
    import trimesh
    from shapely.geometry import Polygon
    lines = trimesh.intersections.mesh_plane(mesh, [0, 0, 1], [0, 0, z])
    if len(lines) == 0:
        return None
    segs = np.round(lines[:, :, :2], 6)
    segs = segs[np.any(segs[:, 0] != segs[:, 1], axis=1)]
    merged = shapely.line_merge(shapely.MultiLineString(list(segs)))
    polys = [Polygon(np.asarray(g.coords)) for g in shapely.get_parts(merged) if g.is_closed and len(g.coords) >= 4]
    polys = [q if q.is_valid else q.buffer(0) for q in polys]
    polys = [q for q in polys if not q.is_empty and q.area > 1e-12]
    if not polys:
        return None
    g = shapely.make_valid(shapely.symmetric_difference_all(polys))     # even-odd: holes stay holes
    g = shapely.unary_union([q for q in shapely.get_parts(g) if q.geom_type == 'Polygon'])
    return None if g.is_empty else g


def kicad_to_model(x, y):
    return x, -y


# ------------------------------------------------------------------------------------------------ mesh
def edge_lines(parts, h_edge, axis):
    """Mesh lines at the copper's straight edges along one axis (0: x, 1: y), by the thirds rule: a line h/3
    outside the metal and one 2h/3 inside, so the field's edge singularity falls between them."""
    out = []
    for p in parts:
        if p.role != 'copper' or p.polys is None:
            continue
        import shapely
        for poly in shapely.get_parts(p.polys):
            for ring in [poly.exterior] + list(poly.interiors):
                c = np.asarray(ring.coords)
                for a, b in zip(c[:-1], c[1:]):
                    if abs(a[axis] - b[axis]) > 1e-6:          # not an edge at constant x (y)
                        continue
                    if abs(a[1 - axis] - b[1 - axis]) < 4 * h_edge:   # a short stub: no thirds rule
                        out.append(a[axis])
                        continue
                    mid = (a + b) / 2
                    probe = mid.copy()
                    probe[axis] += 1e-4
                    inside_plus = poly.contains(shapely.Point(probe))
                    s = 1.0 if inside_plus else -1.0                  # the metal's side
                    out += [a[axis] - s * h_edge / 3, a[axis] + s * 2 * h_edge / 3]
    return out


def smooth(lines, max_res, ratio=1.4):
    from CSXCAD.SmoothMeshLines import SmoothMeshLines
    lines = np.unique(np.round(np.asarray(lines, float), 6))
    return np.asarray(SmoothMeshLines(lines, max_res, ratio))


@dataclass
class MeshSpec:
    f_max: float                       # Hz, the highest frequency of interest
    res_div: float = 20.0              # cells per wavelength in the densest material, at least
    h_edge: float = 0.2                # mm, the thirds-rule spacing at copper edges
    dielectric_cells: int = 4          # cells through each dielectric, at least
    copper_cells: int = 1              # cells through each copper layer
    ratio: float = 1.4                 # largest ratio of neighbouring cells
    air_mm: tuple = (10.0, 10.0, 10.0)  # air round the board in x, y, z (each side)
    extra: dict = field(default_factory=dict)   # axis -> extra lines (ports' planes)


def make_mesh(parts, spec, box=None):
    """The three axes' mesh lines (mm). box: (x0, x1, y0, y1, z0, z1) of the domain, else the parts' extent
    plus spec.air_mm."""
    eps = max([p.props.get('epsilon_r', 1.0) for p in parts if p.role != 'copper'] + [1.0])
    lam = C0 / spec.f_max / math.sqrt(eps) * 1e3
    max_res = lam / spec.res_div
    lam0 = C0 / spec.f_max * 1e3
    if box is None:
        import shapely
        g = shapely.unary_union([p.polys for p in parts if p.polys is not None])
        x0, y0, x1, y1 = g.bounds
        zs = [z for p in parts for z in p.z]
        ax, ay, az = spec.air_mm
        box = (x0 - ax, x1 + ax, y0 - ay, y1 + ay, min(zs) - az, max(zs) + az)
    lines = {}
    for axis in (0, 1):
        l = edge_lines(parts, spec.h_edge, axis) + list(box[2 * axis: 2 * axis + 2]) + list(spec.extra.get(axis, []))
        l = [v for v in l if box[2 * axis] - 1e-9 <= v <= box[2 * axis + 1] + 1e-9]
        lines[axis] = smooth(l, max_res, spec.ratio)
    # z: the copper's faces fixed (and copper_cells through each copper layer), the board graded from them up to
    # its thinnest dielectric over dielectric_cells, then the air grown by the same ratio out to the box
    zl = list(spec.extra.get(2, []))
    for p in parts:
        z0, z1 = p.z
        zl += list(np.linspace(z0, z1, (spec.copper_cells if p.role == 'copper' else 1) + 1))
    diel = [p.z[1] - p.z[0] for p in parts if p.role != 'copper']
    dz_board = min([max_res] + [d / spec.dielectric_cells for d in diel])
    board = smooth(zl, dz_board, spec.ratio)
    top = grow(board[-1], board[-1] - board[-2], box[5], spec.ratio, lam0 / spec.res_div)
    bot = grow(board[0], board[1] - board[0], box[4], spec.ratio, lam0 / spec.res_div)
    lines[2] = np.unique(np.round(np.r_[bot, board, top], 6))
    return lines, dict(max_res_mm=max_res, lambda_min_mm=lam, eps_max=eps, box=box)


def grow(z0, dz0, z_end, ratio, max_res):
    """Lines from z0 (not included) to z_end, each cell `ratio` times the last, from dz0, at most max_res; the
    last cell is stretched or merged so that the lines end at z_end exactly."""
    out, z, dz = [], z0, abs(dz0)
    s = 1.0 if z_end > z0 else -1.0
    while s * (z_end - z) > 1e-9:
        dz = min(dz * ratio, max_res)
        z = z + s * dz
        if s * (z_end - z) < 0.5 * dz:
            z = z_end
        out.append(z)
    if out:
        out[-1] = z_end
    return np.asarray(out)


# ------------------------------------------------------------------------------------------------ checks
def preflight(lines, parts, ports, spec, info, log=print):
    """Check the grid and the ports before running. Returns a list of (check, ok, detail); raises on a failure
    that would make the result wrong."""
    import shapely
    from shapely.geometry import box as sbox
    rows = []
    lam = info['lambda_min_mm']
    lam0 = C0 / spec.f_max * 1e3
    diel = [p.bounds for p in parts if p.role not in ('copper',) and p.bounds]
    for axis, name in enumerate('xyz'):
        d = np.diff(lines[axis])
        mid = 0.5 * (lines[axis][1:] + lines[axis][:-1])
        inside = np.zeros(len(d), bool)
        for b in diel:                      # cells within a dielectric's extent along this axis
            inside |= (mid > b[axis] - 1e-9) & (mid < b[axis + 3] + 1e-9)
        big_in = d[inside].max() if inside.any() else 0.0
        big_out = d[~inside].max() if (~inside).any() else 0.0
        if inside.any():
            rows.append((f'largest {name} cell in the dielectric under lambda/15', big_in <= lam / 15,
                         f'{big_in:.3f} mm, lambda_min {lam:.2f} mm (lambda/15 = {lam / 15:.3f})'))
        if (~inside).any():
            rows.append((f'largest {name} cell in the air under lambda0/15', big_out <= lam0 / 15,
                         f'{big_out:.3f} mm, lambda0 {lam0:.2f} mm (lambda0/15 = {lam0 / 15:.3f})'))
        r = np.maximum(d[1:] / d[:-1], d[:-1] / d[1:]).max() if len(d) > 1 else 1.0
        rows.append((f'neighbouring {name} cells within 2:1', r <= 2.0, f'largest ratio {r:.2f}'))
    cells = int(np.prod([len(l) - 1 for l in lines.values()]))
    rows.append(('cells', True, f'{cells:,} ({" x ".join(str(len(l) - 1) for l in lines.values())})'))
    for pt in ports:
        x0, x1 = sorted((pt.start[0], pt.stop[0]))
        y0, y1 = sorted((pt.start[1], pt.stop[1]))
        strip = sbox(x0, y0, x1, y1)
        cu = shapely.unary_union([p.polys for p in parts if p.role == 'copper' and p.net == pt.net
                                  and p.polys is not None])
        share = cu.intersection(strip).area / strip.area if not cu.is_empty else 0.0
        rows.append((f'port {pt.number} lies on copper of net {pt.net}', share >= 0.9,
                     f'{share * 100:.1f} % of the port strip is copper of {pt.net}'))
        ref = shapely.unary_union([p.polys for p in parts if p.role == 'copper' and p.net == pt.ref_net
                                   and p.polys is not None])
        share = ref.intersection(strip).area / strip.area if not ref.is_empty else 0.0
        rows.append((f'port {pt.number} has its reference copper ({pt.ref_net}) under it', share >= 0.99,
                     f'{share * 100:.1f} % covered'))
        w = y1 - y0 if pt.prop_dir == 'x' else x1 - x0
        across = lines[1] if pt.prop_dir == 'x' else lines[0]
        lo, hi = (y0, y1) if pt.prop_dir == 'x' else (x0, x1)
        n = int(((across > lo - 1e-9) & (across < hi + 1e-9)).sum()) - 1
        rows.append((f'port {pt.number}: at least 3 cells across its {w:.2f} mm strip', n >= 3, f'{n} cells'))
    for name, ok, detail in rows:
        log(f"preflight {'ok  ' if ok else 'FAIL'} {name}: {detail}")
    bad = [r for r in rows if not r[1]]
    if bad:
        raise RuntimeError('preflight failed: ' + '; '.join(f'{n} ({d})' for n, _, d in bad))
    return rows


# ------------------------------------------------------------------------------------------------ model
@dataclass
class MSLPortSpec:
    number: int
    net: str
    ref_net: str
    start: tuple              # (x, y, z) in model mm: x, y of one corner of the strip, z of the strip's underside
    stop: tuple               # (x, y, z): the opposite corner, z of the reference copper's top
    prop_dir: str = 'x'
    excite: float = 0.0       # 1 or -1 for the excited port: the sign points the feed into the line
    feed_shift: float = 0.0   # mm, from the port's start to the feed
    meas_shift: float = 0.0   # mm, from the port's start to its measurement plane
    feed_r: float = 50.0      # ohm, the resistor at the port's start: it ends the line
    strip_top: float = None   # z of the strip's top face: KESE's copper is thick, see thick_strip_probes()
    probe_pad: float = 0.0    # mm added to each side of the current probes across the strip


def build(parts, lines, ports, f0, fc, boundaries, end_criteria=1e-4, max_steps=200000, kappa_at=None):
    """The FDTD and CSX objects: the dielectrics with their eps_r and the loss of their tan delta at kappa_at Hz
    (default f0), copper as PEC from KESE's STL files, the mesh and the MSL ports. Returns (FDTD, CSX, ports)."""
    from CSXCAD import ContinuousStructure
    from openEMS import openEMS
    FDTD = openEMS(NrTS=max_steps, EndCriteria=end_criteria)
    FDTD.SetGaussExcite(f0, fc)
    FDTD.SetBoundaryCond(boundaries)
    CSX = ContinuousStructure()
    FDTD.SetCSX(CSX)
    grid = CSX.GetGrid()
    grid.SetDeltaUnit(1e-3)
    for axis, name in enumerate('xyz'):
        grid.SetLines(name, lines[axis])
    fk = kappa_at or f0
    pec = CSX.AddMetal('copper')
    for p in parts:
        if p.role == 'copper':
            prim = pec.AddPolyhedronReader(str(p.stl), priority=10)
            prim.ReadFile()
        else:
            er = p.props.get('epsilon_r', 1.0)
            td = p.props.get('loss_tangent', 0.0)
            mat = CSX.AddMaterial(p.name.replace(' ', '_'), epsilon=er, kappa=2 * math.pi * fk * EPS0 * er * td)
            prim = mat.AddPolyhedronReader(str(p.stl), priority=1)
            prim.ReadFile()
    port_objs = []
    for pt in ports:
        po = FDTD.AddMSLPort(pt.number, pec, list(pt.start), list(pt.stop), pt.prop_dir, 'z', excite=pt.excite,
                             FeedShift=pt.feed_shift, MeasPlaneShift=pt.meas_shift, Feed_R=pt.feed_r, priority=20)
        if pt.strip_top is not None:
            thick_strip_probes(po, pt)
        port_objs.append(po)
    return FDTD, CSX, port_objs


def thick_strip_probes(port, pt):
    """openEMS's MSL port measures the strip's current with a probe of no height at the strip's underside, made
    for a strip of no thickness. KESE's copper is a solid 35 um thick: such a probe's loop of H runs through the
    copper and misses the current on the strip's top and sides (on O01 it read Z0 50 % high). Each current probe
    is stretched here to enclose the whole strip: from its underside to its top, and probe_pad wider each side."""
    ax = 'xyz'.index(pt.prop_dir)
    across = 1 - ax if ax < 2 else 0
    lo = min(pt.start[across], pt.stop[across]) - pt.probe_pad
    hi = max(pt.start[across], pt.stop[across]) + pt.probe_pad
    n = 0
    for prop in port.port_props:
        if '_it_' not in prop.GetName() and not prop.GetName().startswith('port_it'):
            continue
        for i in range(prop.GetQtyPrimitives()):
            box = prop.GetPrimitive(i)
            a, b = np.array(box.GetStart(), float), np.array(box.GetStop(), float)
            a[across], b[across] = lo, hi
            a[2], b[2] = pt.start[2], pt.strip_top
            box.SetStart(list(a))
            box.SetStop(list(b))
            n += 1
    if n == 0:
        raise RuntimeError(f'port {pt.number}: no current probes found to stretch over the strip')


def run(FDTD, sim_path, threads=4, engine='cpu', log=print):
    """Run openEMS, quietly, in sim_path. Returns the seconds taken."""
    import time
    t0 = time.time()
    kw = dict(engine=engine) if engine else {}
    FDTD.Run(str(sim_path), cleanup=True, verbose=0, numThreads=threads, **kw)
    dt = time.time() - t0
    log(f'openEMS: {dt:.0f} s')
    return dt


def port_results(port_objs, sim_path, freqs, excited, ref_impedance=None):
    """S_i,excited for every port i (the one column the run measured), and each MSL port's line impedance and
    effective permittivity from its own probes. With ref_impedance None the S-parameters are referred to each
    port's own measured line impedance. Complex numbers as [re, im]."""
    for p in port_objs:
        p.CalcPort(str(sim_path), freqs, ref_impedance=ref_impedance)
    a = port_objs[excited - 1].uf_inc
    out = dict(frequency_hz=list(map(float, freqs)), S={}, lines={})
    for i, p in enumerate(port_objs, 1):
        s = p.uf_ref / a                 # every port's outgoing wave is its "reflected" one, in openEMS's terms
        out['S'][f'S{i}{excited}'] = [[float(v.real), float(v.imag)] for v in s]
        zl = p.uf_tot / p.if_tot if hasattr(p, 'if_tot') else None
        beta = getattr(p, 'beta', None)
        row = {}
        z_line = getattr(p, 'ZL', None) if ref_impedance is not None else getattr(p, 'Z_ref', None)
        if z_line is not None:
            row['Z_line_ohm'] = [[float(np.real(v)), float(np.imag(v))] for v in np.atleast_1d(z_line)]
        if beta is not None:
            w = 2 * np.pi * np.asarray(freqs)
            row['eps_eff'] = [float(v) for v in (np.real(beta) * C0 / w) ** 2]
        if zl is not None:
            row['Z_in_ohm'] = [[float(np.real(v)), float(np.imag(v))] for v in zl]
        if hasattr(p, 'prop_ny'):        # the measurement plane, after openEMS moved it onto a mesh line
            row['meas_plane_mm'] = float(p.start[p.prop_ny] + p.direction * p.measplane_shift)
        out['lines'][str(i)] = row
    return out
