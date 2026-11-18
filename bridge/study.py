"""KESE's export of a board, kept or cached, and the versions a result depends on."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import geometry as G
from . import palace_case as C


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def kese_export(board, cache_root, mask=True, log=print):
    """KESE's export of a board, reused while the board file is unchanged. Returns the folder with materials.json."""
    board = Path(board)
    out = Path(cache_root) / f'{board.stem}_{file_hash(board)}'
    found = sorted(out.glob(f'{board.stem}/simulation_*/materials.json'))
    if found:
        log(f'KESE export reused: {found[-1].parent}')
        return found[-1].parent
    return G.run_kese(board, out, mask=mask, log=log)


def kese_geometry(board, folder, mask=True, log=print):
    """KESE's export of a board kept in folder/<board name>: materials.json, the STL solids, the STEP and KESE's
    report and parameters, meant to be committed beside the board. source.json there records the board file's hash,
    KESE's version and the settings; the board is exported again only when its file changes. Returns that folder."""
    import shutil
    import tempfile
    board = Path(board)
    dst = Path(folder) / board.stem
    rec = dst / 'source.json'
    h = file_hash(board)
    if rec.exists() and (dst / 'materials.json').exists() and json.loads(rec.read_text()).get('board_hash') == h:
        log(f'KESE geometry reused: {dst}')
        return dst
    with tempfile.TemporaryDirectory() as tmp:
        src = G.run_kese(board, Path(tmp), mask=mask, log=log)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    write_source(dst, board, mask)
    return dst


def write_source(dst, board, mask=True):
    """source.json in a kept KESE export: which board file (by its hash), KESE's version and the settings used."""
    Path(dst, 'source.json').write_text(json.dumps(dict(
        board=Path(board).name, board_hash=file_hash(board), hash='the first 16 hex digits of the file\'s SHA-256',
        kese=G.kese_version(), preset='elmer', formats=['step', 'stl'],
        settings=G.MASK_SETTINGS if mask else []), indent=1) + '\n')


def versions(exports=()):
    """The versions a result depends on. KESE's is read from the exports' source.json where they are kept, so a
    result names the KESE that made its geometry even where KESE is not installed."""
    import platform
    out = {'python': platform.python_version()}
    kese = None
    for e in exports:
        rec = Path(e) / 'source.json'
        if rec.exists():
            kese = json.loads(rec.read_text()).get('kese')
    out['kese'] = (f'{kese} (made the export)' if kese else G.kese_version())
    out['palace'] = C.version()
    for mod in ('numpy', 'scipy', 'shapely', 'trimesh', 'mapbox_earcut'):
        try:
            out[mod] = __import__(mod).__version__
        except Exception:                # noqa: BLE001
            pass
    try:
        import gmsh
        out['gmsh'] = gmsh.__version__
    except Exception:                    # noqa: BLE001
        pass
    return out
