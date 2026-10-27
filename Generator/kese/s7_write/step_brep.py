"""The B-rep of one part as STEP entities: its vertices, straight edges, planes, faces and
shells, from its Topology (kese/s7_write/step_topology.py), in output units and orientation.
Entities are numbered in blocks: so many per vertex, per edge, per loop, and the number of any
one of them is a sum, never looked up.  The text is made and written a slice of rows at a time,
so that a part of millions of edges never has more than a slice of it as Python objects."""
import numpy as np

from kese.s7_write.step_writer import real, refs

ROWS_AT_A_TIME = 100_000


def write_brep(w, topo, M):
    """-> the ids of the MANIFOLD_SOLID_BREP entities written, one per shell."""
    M = np.asarray(M, dtype=float)
    xyz = topo.xyz @ M[:3, :3].T + M[:3, 3]
    point = w.reserve(2 * len(xyz)) + 2 * np.arange(len(xyz))      # CARTESIAN_POINT, then VERTEX_POINT
    up = w.reserve(2)                                                # DIRECTION and VECTOR, up along the walls
    edge_size = np.where(topo.vertical, 2, 4)                        # (DIRECTION, VECTOR,) LINE, EDGE_CURVE
    edge = w.reserve(int(edge_size.sum())) + np.cumsum(np.r_[0, edge_size[:-1]])
    edge_curve = edge + edge_size - 1
    plane_size = np.where(topo.plane_origin_vertex >= 0, 4, 5)       # PLANE, AXIS2_PLACEMENT_3D, 2 DIRECTION, (CARTESIAN_POINT)
    plane = w.reserve(int(plane_size.sum())) + np.cumsum(np.r_[0, plane_size[:-1]])
    loop_size = 2 + topo.loop_count                                  # FACE_BOUND, EDGE_LOOP, the ORIENTED_EDGEs
    loop = w.reserve(int(loop_size.sum())) + np.cumsum(np.r_[0, loop_size[:-1]])
    face = w.reserve(len(topo.face_plane)) + np.arange(len(topo.face_plane))
    shell = w.reserve(2 * topo.shells) + 2 * np.arange(topo.shells)  # CLOSED_SHELL, MANIFOLD_SOLID_BREP

    for rows in slices(len(xyz)):
        lines = []
        for i, (x, y, z) in zip(point[rows].tolist(), xyz[rows].tolist()):
            lines.append(f"#{i} = CARTESIAN_POINT('',({real(x)},{real(y)},{real(z)}));")
            lines.append(f"#{i + 1} = VERTEX_POINT('',#{i});")
        w.write(lines)
    ux, uy, uz = map(real, direction([0.0, 0.0, 1.0], M)[0])
    w.write([f"#{up} = DIRECTION('',({ux},{uy},{uz}));", f"#{up + 1} = VECTOR('',#{up},1.);"])

    for rows in slices(len(edge)):
        lines = []
        a, b = topo.edge_start[rows], topo.edge_end[rows]
        along = unit(xyz[b] - xyz[a])
        for e, vertical, pa, pb, (dx, dy, dz) in zip(edge[rows].tolist(), topo.vertical[rows].tolist(),
                                                     point[a].tolist(), point[b].tolist(), along.tolist()):
            if vertical:
                lines.append(f"#{e} = LINE('',#{pa},#{up + 1});")
                lines.append(f"#{e + 1} = EDGE_CURVE('',#{pa + 1},#{pb + 1},#{e},.T.);")
            else:
                lines.append(f"#{e} = DIRECTION('',({real(dx)},{real(dy)},{real(dz)}));")
                lines.append(f"#{e + 1} = VECTOR('',#{e},1.);")
                lines.append(f"#{e + 2} = LINE('',#{pa},#{e + 1});")
                lines.append(f"#{e + 3} = EDGE_CURVE('',#{pa + 1},#{pb + 1},#{e + 2},.T.);")
        w.write(lines)

    for rows in slices(len(plane)):
        lines = []
        origin = topo.plane_origin[rows] @ M[:3, :3].T + M[:3, 3]
        axis, ref = direction(topo.plane_axis[rows], M), direction(topo.plane_ref[rows], M)
        at = topo.plane_origin_vertex[rows]
        origin_id = np.where(at >= 0, point[np.maximum(at, 0)], plane[rows] + 4)
        for p, o, own, (ox, oy, oz), (ax, ay, az), (rx, ry, rz) in zip(
                plane[rows].tolist(), origin_id.tolist(), (at < 0).tolist(), origin.tolist(), axis.tolist(), ref.tolist()):
            if own:
                lines.append(f"#{o} = CARTESIAN_POINT('',({real(ox)},{real(oy)},{real(oz)}));")
            lines.append(f"#{p} = PLANE('',#{p + 1});")
            lines.append(f"#{p + 1} = AXIS2_PLACEMENT_3D('',#{o},#{p + 2},#{p + 3});")
            lines.append(f"#{p + 2} = DIRECTION('',({real(ax)},{real(ay)},{real(az)}));")
            lines.append(f"#{p + 3} = DIRECTION('',({real(rx)},{real(ry)},{real(rz)}));")
        w.write(lines)

    oriented = np.repeat(loop + 2, topo.loop_count) + (np.arange(len(topo.use_edge)) - np.repeat(topo.loop_start, topo.loop_count))
    for rows in slices(len(oriented)):
        w.write([f"#{i} = ORIENTED_EDGE('',*,*,#{e},{'.T.' if forward else '.F.'});"
                 for i, e, forward in zip(oriented[rows].tolist(), edge_curve[topo.use_edge[rows]].tolist(),
                                          topo.use_forward[rows].tolist())])
    outer = np.zeros(len(loop), dtype=bool)
    outer[topo.face_loop_start] = True
    for rows in slices(len(loop)):
        lines = []
        for i, n, is_outer in zip(loop[rows].tolist(), topo.loop_count[rows].tolist(), outer[rows].tolist()):
            lines.append(f"#{i} = {'FACE_OUTER_BOUND' if is_outer else 'FACE_BOUND'}('',#{i + 1},.T.);")
            lines.append(f"#{i + 1} = EDGE_LOOP('',{refs(range(i + 2, i + 2 + n))});")
        w.write(lines)
    for rows in slices(len(face)):
        w.write([f"#{f} = ADVANCED_FACE('',{refs(loop[first:first + n])},#{p},{'.T.' if same else '.F.'});"
                 for f, first, n, p, same in zip(face[rows].tolist(), topo.face_loop_start[rows].tolist(),
                                                 topo.face_loop_count[rows].tolist(), plane[topo.face_plane[rows]].tolist(),
                                                 topo.face_same_sense[rows].tolist())])
    order = np.argsort(topo.face_shell, kind="stable")
    cut = np.r_[0, np.cumsum(np.bincount(topo.face_shell, minlength=topo.shells))]
    for k, s in enumerate(shell.tolist()):
        w.write([f"#{s} = CLOSED_SHELL('',{refs(face[order[cut[k]:cut[k + 1]]])});",
                 f"#{s + 1} = MANIFOLD_SOLID_BREP('',#{s});"])
    return (shell + 1).tolist()


def slices(n):
    """The rows 0 to n, ROWS_AT_A_TIME at a time."""
    return (slice(k, k + ROWS_AT_A_TIME) for k in range(0, n, ROWS_AT_A_TIME))


def unit(v):
    """The rows of v, each scaled to length one."""
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def direction(d, M):
    """Directions (rows) in board coordinates -> in the output orientation, of length one."""
    return unit(np.atleast_2d(np.asarray(d, dtype=float)) @ M[:3, :3].T)
