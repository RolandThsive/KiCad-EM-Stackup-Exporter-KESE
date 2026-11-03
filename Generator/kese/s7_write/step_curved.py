"""A part's Topology with true circles (Run.STEP_EXACT_ARCS): where the outline runs through points
that lie on one circle, at every height it is at, the chords become one arc edge per height and the
walls standing on them one cylindrical face per slice; the vertices inside the arc go.

A point can be inside an arc only where the outline passes it the same way at every height (its two
neighbours are the same two points at every height, as along a hole, a pad or a round outline): then
removing it leaves every face around it closed.  The outline's chains of such points are searched
for arcs (step_outline, step_arcs), the arcs that could cross another edge at their heights are
dropped (step_clear), and the faces are rebuilt (rebuilt).  In board mm."""
from dataclasses import replace

import numpy as np

from kese.s7_write.step_clear import clear
from kese.s7_write.step_outline import arcs_of, outline_of
from parameters import P


def with_arcs(topo):
    """Topology -> the same solids with arcs and cylinders, or the Topology itself when nothing on
    it is an arc or it is not closed."""
    if topo.edges_not_used_twice or not len(topo.edge_start):
        return topo
    o = outline_of(topo)
    pieces = arcs_of(o) if o is not None else []
    pieces = clear(o, pieces, P.Geometry.SNAP_GRID_MM) if pieces else []
    return rebuilt(topo, o, pieces) if pieces else topo


def rebuilt(topo, o, pieces):
    """The Topology with every arc's chords one arc edge per height and the walls on them one
    cylindrical face per slice.  Kept vertices, edges, planes and faces stay in their order; the
    arc edges and the cylindrical faces follow."""
    nlev, npc = len(o.levels), len(pieces)
    piece_u, piece_w = np.empty(npc, dtype=np.int64), np.empty(npc, dtype=np.int64)
    piece_circle, piece_ccw = np.empty(npc, dtype=np.int64), np.empty(npc, dtype=bool)
    seg_piece, seg_pos, seg_from = (np.full(len(o.seg_a), -1) for _ in range(3))
    removed = np.zeros(len(o.xy), dtype=bool)
    for m, (k, i, j, ci, ccw) in enumerate(pieces):
        pts, segs, _ = o.chains[k]
        piece_u[m], piece_w[m], piece_circle[m], piece_ccw[m] = pts[i], pts[j], ci, ccw
        seg_piece[segs[i:j]] = m
        seg_pos[segs[i:j]] = np.arange(j - i)
        seg_from[segs[i:j]] = pts[i:j]
        removed[pts[i + 1:j]] = True
    piece_len = np.bincount(seg_piece[seg_piece >= 0], minlength=npc)

    keep_v = ~removed[o.pt]
    vmap = np.cumsum(keep_v) - 1
    vkey = o.pt * nlev + o.lev
    vorder = np.argsort(vkey)

    def vertex_at(p, lv):
        return vorder[np.searchsorted(vkey, p * nlev + lv, sorter=vorder)]

    # edges: a chord becomes the arc edge of its piece at its height
    E = len(topo.edge_start)
    eseg = o.edge_seg
    chord = (eseg >= 0) & (seg_piece[np.maximum(eseg, 0)] >= 0)
    drop = chord | (topo.vertical & removed[o.pt[topo.edge_start]])
    kept_e = np.flatnonzero(~drop)
    elev = o.lev[topo.edge_start]
    epiece = np.where(chord, seg_piece[np.maximum(eseg, 0)], -1)
    arc_keys, arc_of_chord = np.unique(epiece[chord] * nlev + elev[chord], return_inverse=True)
    arc_piece, arc_lev = arc_keys // nlev, arc_keys % nlev
    emap = np.full(E, -1)
    emap[kept_e] = np.arange(len(kept_e))
    emap[np.flatnonzero(chord)] = len(kept_e) + arc_of_chord
    along = np.zeros(E, dtype=bool)                  # a chord runs from its start along its arc
    along[chord] = o.pt[topo.edge_start[chord]] == seg_from[eseg[chord]]
    edge_start = np.r_[vmap[topo.edge_start[kept_e]], vmap[vertex_at(piece_u[arc_piece], arc_lev)]]
    edge_end = np.r_[vmap[topo.edge_end[kept_e]], vmap[vertex_at(piece_w[arc_piece], arc_lev)]]
    vertical = np.r_[topo.vertical[kept_e], np.zeros(len(arc_keys), dtype=bool)]
    edge_circle = np.r_[np.full(len(kept_e), -1), piece_circle[arc_piece]]
    edge_ccw = np.r_[np.zeros(len(kept_e), dtype=bool), piece_ccw[arc_piece]]

    # faces: a wall on a chord goes into its piece's cylinder at its slice
    L = len(topo.loop_count)
    first_use = topo.loop_start[topo.face_loop_start]
    four = (topo.face_loop_count == 1) & (topo.loop_count[topo.face_loop_start] == 4)
    fu = np.where(four, first_use, 0)
    wall = four & topo.vertical[topo.use_edge[fu + 1]] & topo.vertical[topo.use_edge[np.minimum(fu + 3, len(topo.use_edge) - 1)]]
    merged = wall & chord[topo.use_edge[fu]]
    kept_f = np.flatnonzero(~merged)
    use_loop = np.repeat(np.arange(L), topo.loop_count)
    loop_face = np.repeat(np.arange(len(topo.face_loop_count)), topo.face_loop_count)
    keep_use = ~merged[loop_face[use_loop]]
    ue = topo.use_edge
    new_edge = emap[ue]
    new_fwd = np.where(chord[ue], topo.use_forward == along[ue], topo.use_forward)
    prev = np.arange(len(ue)) - 1
    prev[topo.loop_start] = topo.loop_start + topo.loop_count - 1
    keep_use &= ~(chord[ue] & (new_edge == new_edge[prev]))     # one use per run of chords of one arc
    if (new_edge[keep_use] < 0).any():
        raise AssertionError("a kept face uses an edge that went")
    kept_loops = np.flatnonzero(~merged[loop_face])
    loop_count = np.bincount(use_loop[keep_use], minlength=L)[kept_loops]

    mw = np.flatnonzero(merged)
    fu_mw = first_use[mw]
    bottom, up_end, top, down_start = (topo.use_edge[fu_mw + k] for k in range(4))
    group_key, group = np.unique(emap[bottom], return_inverse=True)
    go = topo.use_forward[fu_mw] == along[bottom]                # the wall runs along its arc
    mp = seg_piece[eseg[bottom]]
    pos = seg_pos[eseg[bottom]]
    is_end = np.where(go, pos == piece_len[mp] - 1, pos == 0)
    is_start = np.where(go, pos == 0, pos == piece_len[mp] - 1)
    G = len(group_key)
    count = np.bincount(group, minlength=G)
    gpiece = np.zeros(G, dtype=np.int64)
    gpiece[group] = mp
    if (count != piece_len[gpiece]).any() or (np.bincount(group[is_end], minlength=G) != 1).any() \
            or (np.bincount(group[is_start], minlength=G) != 1).any():
        raise AssertionError("the walls on an arc do not close")
    end_wall, start_wall = np.zeros(G, dtype=np.int64), np.zeros(G, dtype=np.int64)
    end_wall[group[is_end]] = np.flatnonzero(is_end)
    start_wall[group[is_start]] = np.flatnonzero(is_start)
    ggo = np.zeros(G, dtype=bool)
    ggo[group] = go
    gtop = np.zeros(G, dtype=np.int64)
    gtop[group] = emap[top]
    # a cylinder's loop: along its bottom arc, up at the arc's end, back along its top arc, down at its start
    cyl_use_edge = np.stack([group_key, emap[up_end[end_wall]], gtop, emap[down_start[start_wall]]], axis=1)
    cyl_use_fwd = np.stack([ggo, topo.use_forward[fu_mw[end_wall] + 1], ~ggo,
                            topo.use_forward[fu_mw[start_wall] + 3]], axis=1)
    glev = o.lev[topo.edge_start[bottom[end_wall]]]
    cyl_keys, cyl_of_group = np.unique(piece_circle[gpiece] * nlev + glev, return_inverse=True)
    gshell = np.zeros(G, dtype=np.int64)
    gshell[group] = topo.face_shell[mw]

    used_plane = np.zeros(len(topo.plane_origin), dtype=bool)
    used_plane[topo.face_plane[kept_f]] = True
    pmap = np.cumsum(used_plane) - 1
    origin_vertex = topo.plane_origin_vertex[used_plane]
    if removed[o.pt[origin_vertex[origin_vertex >= 0]]].any():
        raise AssertionError("a plane starts at a vertex that went")
    origin_vertex = np.where(origin_vertex >= 0, vmap[np.maximum(origin_vertex, 0)], -1)
    return replace(
        topo, xyz=topo.xyz[keep_v], edge_start=edge_start, edge_end=edge_end, vertical=vertical,
        use_edge=np.r_[new_edge[keep_use], cyl_use_edge.ravel()],
        use_forward=np.r_[new_fwd[keep_use], cyl_use_fwd.ravel()],
        loop_start=np.cumsum(np.r_[0, loop_count, np.full(G, 4)])[:-1],
        loop_count=np.r_[loop_count, np.full(G, 4)],
        face_loop_start=np.r_[np.cumsum(np.r_[0, topo.face_loop_count[kept_f]])[:-1], len(kept_loops) + np.arange(G)],
        face_loop_count=np.r_[topo.face_loop_count[kept_f], np.ones(G, dtype=np.int64)],
        face_plane=np.r_[pmap[topo.face_plane[kept_f]], np.full(G, -1)],
        face_same_sense=np.r_[topo.face_same_sense[kept_f], piece_ccw[gpiece] == ggo],
        plane_origin=topo.plane_origin[used_plane], plane_axis=topo.plane_axis[used_plane],
        plane_ref=topo.plane_ref[used_plane], plane_origin_vertex=origin_vertex,
        face_shell=np.r_[topo.face_shell[kept_f], gshell],
        edge_circle=edge_circle, edge_ccw=edge_ccw,
        face_cylinder=np.r_[np.full(len(kept_f), -1), cyl_of_group],
        circle_xy=np.array([c for c, _ in o.circles]), circle_r=np.array([r for _, r in o.circles]),
        cylinder_circle=cyl_keys // nlev, cylinder_z=o.levels[cyl_keys % nlev])
