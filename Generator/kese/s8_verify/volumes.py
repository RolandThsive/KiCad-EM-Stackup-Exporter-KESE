"""The volume check of stage 8 in simulation mode: by the divergence theorem every part's faces,
its slices and its mesh hold the same volume, and its prisms that less what opening pinch points and
sharing vertices moves: in all, or else in every piece (kese/core/part_checks.py)."""
from kese.core.part_checks import allowed, volume_check, whole


def volumes_agree(model):
    """(ok, report lines): per part, the volume from its faces, its slices, its mesh and its prisms,
    and where those last two differ by more than a part may, piece by piece."""
    if model.mode != "simulation":
        return True, []
    scale = 1000.0 if model.units == "m" else 1.0
    prisms = model.prismset.by_part()
    listed = {part: i for i, part in enumerate(model.meshes)}       # the order the parts are listed everywhere
    ok, lines = True, []
    for part in sorted(model.boundaries, key=lambda part: listed.get(part, len(listed))):
        checked, volumes = model.checks.get(part) or (None, volume_check(model.boundaries[part], prisms[part]))
        faces, slices, built, pieces = volumes
        mesh = float(checked.volume if checked else model.meshes[part].volume) * scale ** 3 if part in model.meshes else 0.0
        closed = bool(abs(faces - slices) <= allowed(slices) and abs(mesh - slices) <= allowed(slices))
        ok &= closed and whole(volumes)
        lines.append(f"  {part:36s} volume from faces {faces:.6f} mesh {mesh:.6f} slices {slices:.6f} "
                     f"prisms {built:.6f} mm3 closed={closed} whole={whole(volumes)}")
        if pieces:
            x, y, z0, z1 = pieces.at
            lines.append(f"  {'':36s} piece by piece: {pieces.pieces} pieces, {pieces.gone} gone, worst {pieces.worst:+.3e} "
                         f"of {pieces.volume:.3e} mm3 at x {x:.3f} y {y:.3f} z {z0:+.4f} .. {z1:+.4f} mm")
    return ok, lines
