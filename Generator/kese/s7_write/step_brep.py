"""The B-rep of one part as STEP entities from its Topology, in output units, numbered in blocks
(so many per vertex, edge, loop), written a slice of rows at a time to bound the memory: the file is
the same whatever the size of the slices.  Lines and planes share one DIRECTION per distinct
direction (kese/s7_write/step_directions.py): a board's edges run in few."""
import numpy as np

from kese.s7_write.step_directions import Directions, keys_of
from kese.s7_write.step_writer import real, reals, refs
from parameters import P


def write_brep(w, topo, M):
    """-> the ids of the MANIFOLD_SOLID_BREP entities written, one per shell."""
    M = np.asarray(M, dtype=float)
    xyz = topo.xyz @ M[:3, :3].T + M[:3, 3]
    point = w.reserve(2 * len(xyz)) + 2 * np.arange(len(xyz))      # CARTESIAN_POINT, then VERTEX_POINT
    up = w.reserve(2)                                                # DIRECTION and VECTOR, up along the walls
    arc = arcs_of(topo)
    edge_size = np.where(arc, 1, 2)                                  # (LINE,) EDGE_CURVE
    edge = w.reserve(int(edge_size.sum())) + np.cumsum(np.r_[0, edge_size[:-1]])
    edge_curve = edge + edge_size - 1
    plane_size = np.where(topo.plane_origin_vertex >= 0, 2, 3)       # PLANE, AXIS2_PLACEMENT_3D, (CARTESIAN_POINT)
    plane = w.reserve(int(plane_size.sum())) + np.cumsum(np.r_[0, plane_size[:-1]])
    loop_size = 2 + topo.loop_count                                  # FACE_BOUND, EDGE_LOOP, the ORIENTED_EDGEs
    loop = w.reserve(int(loop_size.sum())) + np.cumsum(np.r_[0, loop_size[:-1]])
    face = w.reserve(len(topo.face_plane)) + np.arange(len(topo.face_plane))
    shell = w.reserve(2 * topo.shells) + 2 * np.arange(topo.shells)  # CLOSED_SHELL, MANIFOLD_SOLID_BREP
    curves = None if topo.edge_circle is None else Curves(w, topo, M)
    directions = Directions(w)

    for rows in slices(len(xyz)):
        x = iter(reals(xyz[rows]))
        w.write([f"#{i} = CARTESIAN_POINT('',({a},{b},{c}));\n#{i + 1} = VERTEX_POINT('',#{i});"
                 for i, a, b, c in zip(point[rows].tolist(), x, x, x)])
    ux, uy, uz = map(real, direction([0.0, 0.0, 1.0], M)[0])
    w.write([f"#{up} = DIRECTION('',({ux},{uy},{uz}));", f"#{up + 1} = VECTOR('',#{up},1.);"])
    if curves:
        curves.write(w, up)

    sloped = ~arc & ~topo.vertical                                   # a line that does not run up a wall
    directions.write((along(topo, xyz, sloped, rows) for rows in slices(len(edge))), vectors=True)
    for rows in slices(len(edge)):
        a, b = topo.edge_start[rows], topo.edge_end[rows]
        vector = np.full(len(a), up + 1)                             # a wall's vertical edge runs up
        vector[sloped[rows]] = directions.vectors(along(topo, xyz, sloped, rows))
        circle = curves.edge_circle(rows) if curves else [None] * len(a)
        w.write([f"#{e} = EDGE_CURVE('',#{pa + 1},#{pb + 1},#{c[0]},{c[1]});" if c is not None else
                 f"#{e} = LINE('',#{pa},#{v});\n#{e + 1} = EDGE_CURVE('',#{pa + 1},#{pb + 1},#{e},.T.);"
                 for e, pa, pb, v, c in zip(edge[rows].tolist(), point[a].tolist(), point[b].tolist(), vector.tolist(), circle)])

    directions.write(direction(topo.plane_axis[rows], M) for rows in slices(len(plane)))
    directions.write(direction(topo.plane_ref[rows], M) for rows in slices(len(plane)))
    own = topo.plane_origin_vertex < 0                               # a plane through no vertex has its own origin
    origin_id = np.where(own, plane + 2, point[np.maximum(topo.plane_origin_vertex, 0)])
    for rows in slices(len(plane)):                                  # those origins first, then the planes
        x = iter(reals(topo.plane_origin[rows][own[rows]] @ M[:3, :3].T + M[:3, 3]))
        w.write([f"#{o} = CARTESIAN_POINT('',({a},{b},{c}));" for o, a, b, c in zip(origin_id[rows][own[rows]].tolist(), x, x, x)])
    for rows in slices(len(plane)):
        axis = directions.ids(direction(topo.plane_axis[rows], M))
        ref = directions.ids(direction(topo.plane_ref[rows], M))
        w.write([f"#{p} = PLANE('',#{p + 1});\n#{p + 1} = AXIS2_PLACEMENT_3D('',#{o},#{d},#{r});"
                 for p, o, d, r in zip(plane[rows].tolist(), origin_id[rows].tolist(), axis.tolist(), ref.tolist())])

    oriented = np.repeat(loop + 2, topo.loop_count) + (np.arange(len(topo.use_edge)) - np.repeat(topo.loop_start, topo.loop_count))
    for rows in slices(len(oriented)):
        w.write([f"#{i} = ORIENTED_EDGE('',*,*,#{e},{'.T.' if forward else '.F.'});"
                 for i, e, forward in zip(oriented[rows].tolist(), edge_curve[topo.use_edge[rows]].tolist(),
                                          topo.use_forward[rows].tolist())])
    outer = np.zeros(len(loop), dtype=bool)
    outer[topo.face_loop_start] = True
    for rows in slices(len(loop)):
        w.write([f"#{i} = {'FACE_OUTER_BOUND' if is_outer else 'FACE_BOUND'}('',#{i + 1},.T.);\n"
                 f"#{i + 1} = EDGE_LOOP('',{refs(range(i + 2, i + 2 + n))});"
                 for i, n, is_outer in zip(loop[rows].tolist(), topo.loop_count[rows].tolist(), outer[rows].tolist())])
    for rows in slices(len(face)):
        surface = plane[topo.face_plane[rows]] if curves is None else curves.surface(rows, plane)
        w.write([f"#{f} = ADVANCED_FACE('',{refs(loop[first:first + n])},#{p},{'.T.' if same else '.F.'});"
                 for f, first, n, p, same in zip(face[rows].tolist(), topo.face_loop_start[rows].tolist(),
                                                 topo.face_loop_count[rows].tolist(), surface.tolist(),
                                                 topo.face_same_sense[rows].tolist())])
    order = np.argsort(topo.face_shell, kind="stable")
    cut = np.r_[0, np.cumsum(np.bincount(topo.face_shell, minlength=topo.shells))]
    for k, s in enumerate(shell.tolist()):
        w.write([f"#{s} = CLOSED_SHELL('',{refs(face[order[cut[k]:cut[k + 1]]])});",
                 f"#{s + 1} = MANIFOLD_SOLID_BREP('',#{s});"])
    return (shell + 1).tolist()


def entity_count(topo, M):
    """How many entity numbers write_brep(w, topo, M) takes, found without writing them: so a big
    board's parts get their first numbers before their text is written (step_parts.py)."""
    M = np.asarray(M, dtype=float)
    xyz = topo.xyz @ M[:3, :3].T + M[:3, 3]
    arc = arcs_of(topo)
    count = (2 * len(xyz) + 2 + int(np.where(arc, 1, 2).sum()) + int(np.where(topo.plane_origin_vertex >= 0, 2, 3).sum())
             + int((2 + topo.loop_count).sum()) + len(topo.face_plane) + 2 * topo.shells)
    if topo.edge_circle is not None:
        count += 1 + 4 * len(circle_places(topo)[1])                  # Curves: the x DIRECTION, 4 per placement
    sloped = ~arc & ~topo.vertical
    lines = keys_of(along(topo, xyz, sloped, rows) for rows in slices(len(arc)))     # a DIRECTION and a VECTOR each
    axes = keys_of(direction(topo.plane_axis[rows], M) for rows in slices(len(topo.plane_axis)))
    refs = keys_of(direction(topo.plane_ref[rows], M) for rows in slices(len(topo.plane_ref)))
    return count + 2 * len(lines) + len(axes - lines) + len(refs - lines - axes)


def arcs_of(topo):
    """Per edge: whether it is an arc (of a circle), not a line."""
    return np.zeros(len(topo.edge_start), dtype=bool) if topo.edge_circle is None else topo.edge_circle >= 0


def along(topo, xyz, sloped, rows):
    """The direction of each sloped edge (`sloped`) of the rows, in the output frame (`xyz`)."""
    a, b = topo.edge_start[rows][sloped[rows]], topo.edge_end[rows][sloped[rows]]
    return unit(xyz[b] - xyz[a])


def circle_places(topo):
    """The arc edges, the distinct (circle, height) placements of their circles and of the cylinders,
    and the placement of each (the arcs' first, then the cylinders')."""
    e = np.flatnonzero(topo.edge_circle >= 0)
    keys = np.r_[topo.edge_circle[e], topo.cylinder_circle], np.r_[topo.xyz[topo.edge_start[e], 2], topo.cylinder_z]
    uniq, at = np.unique(np.stack(keys, axis=1), axis=0, return_inverse=True)
    return e, uniq, at.ravel()


class Curves:
    """The circles of a Topology with arcs: one placement per circle and height (CARTESIAN_POINT at
    the centre, AXIS2_PLACEMENT_3D with the axis up and x as its reference), which the CIRCLE of the
    arc edges and the CYLINDRICAL_SURFACE of the walls at that height share."""

    def __init__(self, w, topo, M):
        self.topo, self.M = topo, M
        e, uniq, at = circle_places(topo)
        self.place_circle, self.place_z = uniq[:, 0].astype(np.int64), uniq[:, 1]
        self.edge_place = np.full(len(topo.edge_start), -1)
        self.edge_place[e] = at[:len(e)]
        self.cylinder_place = at[len(e):]
        self.has_circle = np.zeros(len(uniq), dtype=bool)
        self.has_circle[at[:len(e)]] = True
        self.has_cylinder = np.zeros(len(uniq), dtype=bool)
        self.has_cylinder[self.cylinder_place] = True
        self.xref = w.reserve(1)
        self.place = w.reserve(4 * len(uniq)) + 4 * np.arange(len(uniq))
        self.flip = np.linalg.det(M[:3, :3]) < 0        # a mirror turns counter-clockwise round

    def write(self, w, up):
        """The placements, circles and cylinders (`up`: the DIRECTION of the axis)."""
        M = self.M
        rx, ry, rz = map(real, direction([1.0, 0.0, 0.0], M)[0])
        lines = [f"#{self.xref} = DIRECTION('',({rx},{ry},{rz}));"]
        scale = float(np.linalg.norm(M[:3, :3] @ [0.0, 0.0, 1.0]))
        c = self.topo.circle_xy[self.place_circle]
        centre = np.c_[c, self.place_z] @ M[:3, :3].T + M[:3, 3]
        radius = self.topo.circle_r[self.place_circle] * scale
        for p, (x, y, z), r, circle, cylinder in zip(self.place.tolist(), centre.tolist(), radius.tolist(),
                                                    self.has_circle.tolist(), self.has_cylinder.tolist()):
            lines.append(f"#{p} = CARTESIAN_POINT('',({real(x)},{real(y)},{real(z)}));")
            lines.append(f"#{p + 1} = AXIS2_PLACEMENT_3D('',#{p},#{up},#{self.xref});")
            if circle:
                lines.append(f"#{p + 2} = CIRCLE('',#{p + 1},{real(r)});")
            if cylinder:
                lines.append(f"#{p + 3} = CYLINDRICAL_SURFACE('',#{p + 1},{real(r)});")
        for rows in slices(len(lines)):
            w.write(lines[rows])

    def edge_circle(self, rows):
        """Per edge of the rows: (the CIRCLE's id, the edge's sense along it) for an arc, else None."""
        at = self.edge_place[rows]
        ccw = self.topo.edge_ccw[rows] ^ self.flip
        return [None if a < 0 else (int(self.place[a]) + 2, ".T." if s else ".F.") for a, s in zip(at.tolist(), ccw.tolist())]

    def surface(self, rows, plane):
        """The surface of every face of the rows: its PLANE or its CYLINDRICAL_SURFACE."""
        cyl = self.topo.face_cylinder[rows]
        return np.where(cyl >= 0, self.place[self.cylinder_place[np.maximum(cyl, 0)]] + 3,
                        plane[np.maximum(self.topo.face_plane[rows], 0)])


def slices(n):
    """The rows 0 to n, Parallel.STEP_ROWS_AT_A_TIME at a time."""
    step = P.Parallel.STEP_ROWS_AT_A_TIME
    return (slice(k, k + step) for k in range(0, n, step))


def unit(v):
    """The rows of v, each scaled to length one."""
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def direction(d, M):
    """Directions (rows) in board coordinates -> in the output orientation, of length one."""
    return unit(np.atleast_2d(np.asarray(d, dtype=float)) @ M[:3, :3].T)
