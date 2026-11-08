"""The arithmetic of triangle meshes (kese/core/mesh.py): unit vectors, face normals and angles,
transforms and shared edges, written in trimesh 4/5's order of operations, bit for bit."""
import numpy as np

ZERO = float(np.finfo(np.float64).resolution * 100)    # a length below this is no length


def unitize(vectors, check_valid=False):
    """Every row scaled to length 1 (a row of no length is left as it is, scaled by its length);
    with check_valid, (the rows of some length, unitized, and which rows they are)."""
    vectors = np.asanyarray(vectors)
    norm = np.sqrt(np.dot(vectors * vectors, [1.0] * vectors.shape[1]))
    valid = norm > ZERO
    norm[valid] **= -1
    unit = vectors * norm.reshape((-1, 1))
    return (unit[valid], valid) if check_valid else unit


def diagonal_dot(a, b):
    """The dot product of every row of a with the same row of b."""
    a = np.asanyarray(a)
    return np.dot(a * b, [1.0] * a.shape[1])


def crosses(triangles):
    """The cross product of the first two edges of every triangle (n, 3, 3)."""
    vectors = triangles[:, 1:, :] - triangles[:, :2, :]
    return np.cross(vectors[:, 0], vectors[:, 1])


def face_normals(triangles, cross):
    """The unit normal of every triangle, [0, 0, 0] for one of no area."""
    unit, valid = unitize(cross, check_valid=True)
    if valid.all():
        return unit
    padded = np.zeros((len(triangles), 3), dtype=np.float64)
    padded[valid] = unit
    return padded


def angles(triangles, zero_angle):
    """The angle at each corner of every triangle, all three 0 where one is under zero_angle."""
    u = unitize(triangles[:, 1] - triangles[:, 0])
    v = unitize(triangles[:, 2] - triangles[:, 0])
    w = unitize(triangles[:, 2] - triangles[:, 1])
    result = np.zeros((len(triangles), 3), dtype=np.float64)
    result[:, 0] = np.arccos(np.clip(diagonal_dot(u, v), -1, 1))
    result[:, 1] = np.arccos(np.clip(diagonal_dot(-u, w), -1, 1))
    result[:, 2] = np.pi - result[:, 0] - result[:, 1]
    result[(result < zero_angle).any(axis=1), :] = 0.0
    return result


def transform_points(points, matrix):
    """Points (n, 3) through a 4x4 matrix."""
    points = np.asanyarray(points, dtype=np.float64)
    if len(points) == 0:
        return points.copy()
    matrix = np.asanyarray(matrix, dtype=np.float64)
    if np.abs(matrix - np.eye(4)).max() < 1e-8:
        return np.ascontiguousarray(points.copy())
    stack = np.column_stack((points, np.ones(len(points))))
    return np.dot(matrix, stack.T).T[:, :3]


def nearly_equal(a, b, atol):
    """trimesh's util.allclose: the spread of a - b under atol."""
    return bool(float(np.ptp(np.asarray(a) - np.asarray(b))) < atol)


def edges(faces):
    """(the three edges of every face in order, the face of each edge)."""
    faces = np.asanyarray(faces, np.int64)
    return faces[:, [0, 1, 1, 2, 2, 0]].reshape((-1, 2)), np.repeat(np.arange(len(faces)), 3)


def edge_pairs(sorted_edges):
    """(k, 2): the rows of the edges (each sorted) that occur exactly twice, the two rows of each."""
    if not len(sorted_edges):
        return np.zeros((0, 2), dtype=np.int64)
    key = sorted_edges[:, 0] * (int(sorted_edges.max()) + 1) + sorted_edges[:, 1]
    order = np.argsort(key, kind="stable")
    k = key[order]
    start = np.flatnonzero(np.r_[True, k[1:] != k[:-1]])
    count = np.diff(np.r_[start, len(k)])
    two = start[count == 2]
    return np.column_stack((order[two], order[two + 1]))


def volume(triangles, cross):
    """The volume a closed, outward wound surface holds (the divergence theorem)."""
    f1 = triangles[:, 0, :] + triangles[:, 1, :] + triangles[:, 2, :]
    return (cross[:, 0] * f1[:, 0]).sum() / 6.0
