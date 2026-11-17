"""KESE's export of a board, and the heights of its copper layers read from it.

KESE stays a geometry exporter: the bridge runs it as a program (run_KESE.py, from the path in KESE_PATH or the
branch's 3D_Geometry folder) and reads the materials.json it writes. FastHenry takes its conductors from the board
file's tracks (kicad.py); what it takes from KESE is the stack-up: where each copper layer sits and how thick it is,
as KESE builds it from the board's own stack-up.

KESE writes a board with F.Cu toward +z and z = 0 in the middle of the board. The bridge's model coordinates: x and
y as KESE's (KiCad's, y up), z shifted so that the stator's F.Cu top face is z = 0.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# KESE's solder mask as the coil boards' brief asks: 20 um over copper and laminate, vias tented. The mask is an
# insulator with mu_r 1, air to a magneto-quasi-static solve; it is kept so the export is the same for any solver.
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
    raise FileNotFoundError("KESE not found: copy main's Generator into 3D_Geometry (see its README) "
                            'or set KESE_PATH to run_KESE.py')


def kese_version():
    try:
        r = subprocess.run([sys.executable, str(kese_script()), '--version'], capture_output=True, text=True)
        return r.stdout.strip() or r.stderr.strip()
    except Exception as e:              # noqa: BLE001
        return f'unknown ({e})'


def run_kese(board, out, mask=True, log=print):
    """Export one .kicad_pcb with KESE's solver preset (--for elmer: solids and materials.json) plus STEP and STL.
    Returns the folder with materials.json."""
    cmd = [sys.executable, str(kese_script()), str(board), '--for', 'elmer', '--format', 'step', 'stl',
           '--out', str(out)]
    for s in (MASK_SETTINGS if mask else []):
        cmd += ['--set', s]
    log('KESE: ' + ' '.join(Path(c).name if i == 1 else c for i, c in enumerate(cmd)))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f'KESE failed on {board}:\n{r.stdout}\n{r.stderr}')
    found = sorted(Path(out).glob(f'{Path(board).stem}/simulation_*/materials.json'))
    if not found:
        raise RuntimeError(f'KESE wrote no materials.json for {board}')
    return found[-1].parent


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def kese_geometry(board, folder, mask=True, log=print):
    """KESE's export of a board kept in folder/<board name>: materials.json, the STL solids, the STEP and KESE's
    report and parameters, meant to be committed beside the board. source.json there records the board file's hash,
    KESE's version and the settings; the board is exported again only when its file changes. Returns that folder."""
    board = Path(board)
    dst = Path(folder) / board.stem
    rec = dst / 'source.json'
    if rec.exists() and (dst / 'materials.json').exists() and \
            json.loads(rec.read_text()).get('board_hash') == file_hash(board):
        log(f'KESE geometry reused: {dst}')
        return dst
    with tempfile.TemporaryDirectory() as tmp:
        src = run_kese(board, Path(tmp), mask=mask, log=log)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    (dst / 'source.json').write_text(json.dumps(dict(
        board=board.name, board_hash=file_hash(board), hash="the first 16 hex digits of the file's SHA-256",
        kese=kese_version(), preset='elmer', formats=['step', 'stl'],
        settings=MASK_SETTINGS if mask else []), indent=1) + '\n')
    return dst


def copper_layers(export):
    """Each copper layer's z range in KESE's coordinates, {layer: (z_bottom, z_top)}, from materials.json: a
    dielectric part says which two layers it lies between, and each copper layer's thickness is in the copper
    parts' properties."""
    mats = json.loads((Path(export) / 'materials.json').read_text())
    thick, between = {}, []
    for info in mats['parts'].values():
        p = info.get('properties', {})
        if info['role'] == 'copper':
            for lay in p.get('layers', []) or [dict(layer=info.get('layer'), thickness_mm=p.get('thickness_mm'))]:
                if lay.get('layer') and lay.get('thickness_mm'):
                    thick[lay['layer']] = float(lay['thickness_mm'])
        elif info['role'] == 'board' and p.get('between'):
            between.append((tuple(p['between']), info['z_range_mm']))
    out = {}
    for (upper, lower), (z0, z1) in between:            # 'between': [the layer above, the layer below]
        if upper in thick:                              # a layer with no copper on it has no thickness here
            out.setdefault(upper, (z1, z1 + thick[upper]))
        if lower in thick:
            out.setdefault(lower, (z0 - thick[lower], z0))
    if not out:                                         # a one-layer board: the copper part's own range
        for info in mats['parts'].values():
            if info['role'] == 'copper':
                out[info['layer']] = tuple(info['z_range_mm'])
    return out


def versions(exports=()):
    """The versions a result depends on. Where KESE is not installed (a board whose export is committed needs it
    not), KESE's version is the one that made the exports, from their source.json."""
    from . import fasthenry_case as C
    out = {'python': platform.python_version(), 'kese': kese_version(), 'fasthenry': C.fasthenry_version()}
    made = sorted({json.loads(Path(e, 'source.json').read_text()).get('kese', '') for e in exports
                   if Path(e, 'source.json').exists()} - {''})
    if made and out['kese'].startswith('unknown'):
        out['kese'] = ', '.join(made) + ' (made the export; not installed where this ran)'
    for mod in ('numpy', 'shapely'):
        try:
            out[mod] = __import__(mod).__version__
        except Exception:                # noqa: BLE001
            pass
    return out
