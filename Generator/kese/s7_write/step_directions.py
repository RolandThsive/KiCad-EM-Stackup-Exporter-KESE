"""The DIRECTION entities of one part's B-rep (kese/s7_write/step_brep.py): one per distinct
direction, which the lines and planes along it share, and one VECTOR of length one along it for the
lines.  All of them are written before the entities that refer to them, in sorted order, so that
the file does not depend on the slices the rows are written in (Parallel.STEP_ROWS_AT_A_TIME)."""
import numpy as np

from kese.s7_write.step_writer import real

DIRECTION_DIGITS = 12             # directions closer than this are one DIRECTION (a 1e-12 turn)


class Directions:
    """One DIRECTION per distinct direction of a part (rounded to DIRECTION_DIGITS), and one VECTOR
    of length one along it for the lines that need it.  write() writes those of all the rows at
    once, in sorted order, before the entities that refer to them: so the ids and the order of the
    file do not depend on how the rows are cut into slices."""

    def __init__(self, w):
        self.w, self.direction, self.vector = w, {}, {}

    def write(self, slices_of_d, vectors=False):
        """Write the DIRECTION (and with `vectors` the VECTOR) of every distinct direction among the
        rows of the slices (unit vectors, output frame) not written yet."""
        lines = []
        for key in sorted(keys_of(slices_of_d)):
            i = self.direction.get(key)
            if i is None:
                i = self.direction[key] = self.w.reserve(1)
                lines.append(f"#{i} = DIRECTION('',({','.join(real(v) for v in key)}));")
            if vectors and key not in self.vector:
                v = self.vector[key] = self.w.reserve(1)
                lines.append(f"#{v} = VECTOR('',#{i},1.);")
        if lines:
            self.w.write(lines)

    def ids(self, d):
        """The DIRECTION of every row of d, written already."""
        return self._look_up(d, self.direction)

    def vectors(self, d):
        """The VECTOR (length one) along every row of d, written already."""
        return self._look_up(d, self.vector)

    @staticmethod
    def _look_up(d, table):
        if not len(d):
            return np.empty(0, dtype=np.int64)
        uniq, back = np.unique(rounded(d), axis=0, return_inverse=True)
        return np.asarray([table[key] for key in map(tuple, uniq.tolist())], dtype=np.int64)[back.ravel()]


def keys_of(slices_of_d):
    """The distinct directions among the rows of the slices, as the keys of their DIRECTIONs."""
    keys = set()
    for d in slices_of_d:
        if len(d):
            keys.update(map(tuple, np.unique(rounded(d), axis=0).tolist()))
    return keys


def rounded(d):
    """Directions rounded to DIRECTION_DIGITS, the key of one DIRECTION (+ 0.0: no -0.)."""
    return np.round(d, DIRECTION_DIGITS) + 0.0
