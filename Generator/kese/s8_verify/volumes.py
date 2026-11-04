"""The volume check of stage 8 in simulation mode: by the divergence theorem every part's faces,
its slices and its mesh hold the same volume, and its prisms that less the opened pinch points."""

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
        boundary = model.boundaries[part]
        faces, slices = boundary.volume(), boundary.volume_of_slices()
        mesh = float(model.meshes[part].volume) * scale ** 3 if part in model.meshes else 0.0
        built = sum(p.region.area * (p.z1 - p.z0) for p in prisms[part])
        allowed = P.Run.VERIFY_VOLUME_TOLERANCE * max(slices, 1e-9) + 1e-9
        closed = abs(faces - slices) <= allowed and abs(mesh - slices) <= allowed
        whole = abs(built - slices) <= allowed + P.Run.VERIFY_OPENED_VOLUME_MM3
        ok &= closed and whole
        lines.append(f"  {part:36s} volume from faces {faces:.6f} mesh {mesh:.6f} slices {slices:.6f} "
                     f"prisms {built:.6f} mm3 closed={closed} whole={whole}")
    return ok, lines
