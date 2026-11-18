"""KESE's export as the bridge's parts: run KESE on a board, read its solids and materials.json, place them.

KESE stays a geometry exporter: the bridge runs it as a program (run_KESE.py, from the path in KESE_PATH or the
branch's 3D_Geometry folder) and reads what it writes. Nothing here changes KESE.

KESE writes a board with y up (y_model = -y_kicad), F.Cu toward +z and z = 0 in the middle of the board.
The bridge's model coordinates (the brief's): x and y as KESE's, z shifted so the stator's F.Cu top is z = 0.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

from .mesh25d import Part

HERE = Path(__file__).resolve().parent
PRIORITY = {'copper': 3, 'bridge': 3, 'mask': 2, 'board': 1}

# KESE's solder mask as the coil boards' brief asks: 20 um over copper and laminate, vias tented
MASK_SETTINGS = ['Stackup.solder_mask=True', 'SolderMask.USE_STACKUP_MASK_THICKNESS=False',
                 'SolderMask.MASK_OVER_COPPER_MM=0.020', 'SolderMask.MASK_OVER_LAMINATE_MM=0.020',
                 'SolderMask.VIA_TENTING=tented']


def kese_script():
    """run_KESE.py: $KESE_PATH (the file or its folder), else the branch's 3D_Geometry/run_KESE.py."""
    env = os.environ.get('KESE_PATH')
    cands = [Path(env)] if env else []
    cands.append(HERE.parent / '3D_Geometry')
    for c in cands:
        c = c / 'run_KESE.py' if c.is_dir() else c
        if c.is_file():
            return c
    raise FileNotFoundError('KESE not found: copy main\'s Generator into 3D_Geometry (see its README) '
                            'or set KESE_PATH to run_KESE.py')


def run_kese(board, out, mask=True, extra=(), log=print):
    """Export one .kicad_pcb with KESE's solver preset (--for elmer: solids and materials.json) plus STEP and STL.
    Returns the folder with materials.json."""
    cmd = [sys.executable, str(kese_script()), str(board), '--for', 'elmer', '--format', 'step', 'stl',
           '--out', str(out)]
    for s in (MASK_SETTINGS if mask else []) + list(extra):
        cmd += ['--set', s]
    log('KESE: ' + ' '.join(Path(c).name if i == 1 else c for i, c in enumerate(cmd)))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f'KESE failed on {board}:\n{r.stdout}\n{r.stderr}')
    for line in r.stdout.splitlines():
        if 'Verifier' in line:
            log('KESE ' + line.strip())
    found = sorted(Path(out).glob(f'{Path(board).stem}/simulation_*/materials.json'))
    if not found:
        raise RuntimeError(f'KESE wrote no materials.json for {board}')
    return found[-1].parent


def kese_version():
    try:
        r = subprocess.run([sys.executable, str(kese_script()), '--version'], capture_output=True, text=True)
        return r.stdout.strip() or r.stderr.strip()
    except Exception as e:              # noqa: BLE001
        return f'unknown ({e})'


def load_parts(export_dir, z_shift=0.0, flip=False, rotate_deg=0.0, axis=None, prefix='',
               body_of=None, drop_roles=()):
    """KESE's solids as Parts in model coordinates.
    z_shift: added to z (after flip). flip: z -> -z, the board turned copper side down without mirroring its
    pattern (a rotor). rotate_deg: turned about `axis`, (x, y) in model coordinates, by this angle in KiCad's sense
    (KiCad's y is down, so it is -rotate_deg in these y-up coordinates); the caller says where the axis is.
    body_of(name, info) -> the body name (default by role / net)."""
    if rotate_deg and axis is None:
        raise ValueError('load_parts: rotate_deg needs the axis it turns about')
    import trimesh
    export_dir = Path(export_dir)
    mats = json.loads((export_dir / 'materials.json').read_text())
    parts = []
    for name, info in mats['parts'].items():
        role = info['role']
        if role in drop_roles:
            continue
        mesh = trimesh.load(export_dir / 'stl' / info['file_names']['stl'], force='mesh')
        v = mesh.vertices.copy()
        if flip:
            v[:, 2] = -v[:, 2]
        v[:, 2] += z_shift
        if rotate_deg:
            a = np.radians(-rotate_deg)
            x, y = v[:, 0] - axis[0], v[:, 1] - axis[1]
            v[:, 0] = axis[0] + x * np.cos(a) - y * np.sin(a)
            v[:, 1] = axis[1] + x * np.sin(a) + y * np.cos(a)
        f = mesh.faces[:, ::-1] if flip else mesh.faces
        mesh = trimesh.Trimesh(v, f, process=False)
        if body_of:
            body = body_of(name, info)
        elif role == 'copper':
            body = prefix + str(info.get('net') or name)
        elif role == 'mask':
            body = prefix + 'MASK'
        else:
            body = prefix + 'FR4'
        parts.append(Part(name=prefix + name, body=body, role=role, mesh=mesh, priority=PRIORITY.get(role, 0)))
    return parts, mats


def copper_top(mats, layer='F.Cu'):
    """The z of the top of a copper layer in KESE's coordinates."""
    for info in mats['parts'].values():
        if info['role'] == 'copper' and info.get('layer') == layer:
            for l in info['properties'].get('layers', []):
                if l['layer'] == layer:
                    return float(info['z_range_mm'][1])
    zs = [info['z_range_mm'][1] for info in mats['parts'].values() if info['role'] == 'copper']
    return float(max(zs))
