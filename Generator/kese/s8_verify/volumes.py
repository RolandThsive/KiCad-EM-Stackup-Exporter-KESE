"""The volume check of stage 8 in simulation mode: by the divergence theorem every part's faces,
its slices and its mesh hold the same volume, and its prisms that less the opened pinch points."""

from kese.core.part_checks import volume_check
from parameters import P


def volumes_agree(model):
    """(ok, report lines): per part, the volume from its faces, its slices, its mesh and its prisms."""
    if model.mode != "simulation":
        return True, []
    scale = 1000.0 if model.units == "m" else 1.0
    prisms = model.prismset.by_part()
    listed = {part: i for i, part in enumerate(model.meshes)}       # the order the parts are listed everywhere
    ok, lines = True, []
    for part in sorted(model.boundaries, key=lambda part: listed.get(part, len(listed))):
        checked, (faces, slices, built) = model.checks.get(part) or (None, volume_check(model.boundaries[part], prisms[part]))
        mesh = float(checked.volume if checked else model.meshes[part].volume) * scale ** 3 if part in model.meshes else 0.0
        allowed = P.Verifier.VERIFY_VOLUME_TOLERANCE * max(slices, 1e-9) + 1e-9
        closed = abs(faces - slices) <= allowed and abs(mesh - slices) <= allowed
        whole = abs(built - slices) <= allowed + P.Verifier.VERIFY_OPENED_VOLUME_MM3
        ok &= closed and whole
        lines.append(f"  {part:36s} volume from faces {faces:.6f} mesh {mesh:.6f} slices {slices:.6f} "
                     f"prisms {built:.6f} mm3 closed={closed} whole={whole}")
    return ok, lines
