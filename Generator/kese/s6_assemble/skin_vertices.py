"""The visual mode's flat faces given the vertices that lie on their edges, as its walls are
(kese/core/vertices.py walls_split_at_vertices), so that a face and the wall beside it meet along
the same edges (skin_faces.py)."""
from kese.core.vertices import share_vertices


def flats_sharing_vertices(flats, slices, levels):
    """Every part's flat faces with each vertex of the faces at their height and the heights next to it,
    and of every part's material just below and above, that lies on one of their edges (near_edge()), as
    the walls between those heights are split at them (walls_split_at_vertices): a face then meets the
    wall beside it along the same edges.  Else a silkscreen's wall bent at a vertex of the mask's face
    half a grid step off the ink's edge left a crack 50 nm wide between the ink's face and the wall."""
    at = {z: k for k, z in enumerate(levels)}
    by_height = {}
    for part, faces in flats.items():
        for i, (z, _, _) in enumerate(faces):
            by_height.setdefault(z, []).append((part, i))
    out = {part: list(faces) for part, faces in flats.items()}
    for z, faces in by_height.items():
        k = at[z]
        sources = [s[j] for s in slices.values() for j in (k - 1, k) if 0 <= j < len(s) and not s[j].is_empty]
        sources += [flats[part][i][1] for h in levels[max(k - 1, 0):k + 2] if h != z for part, i in by_height.get(h, [])]
        new, changed = share_vertices([flats[part][i][1] for part, i in faces], sources)
        for n in changed:
            part, i = faces[n]
            out[part][i] = (z, new[n], flats[part][i][2])
    return out
