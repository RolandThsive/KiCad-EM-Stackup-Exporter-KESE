"""Textbook values the examples check Palace against. Not part of the bridge: the bridge only turns a board into a
Palace model and reads it back; what a result is compared with belongs to each example."""
import math

MU0 = 1.25663706212e-6               # H/m, CODATA 2018


def ring_inductance(radius_mm, gmd_mm):
    """A circular loop's inductance from the geometric mean distance of its cross-section (Grover):
    mu0 R (ln(8R / g) - 2)."""
    return MU0 * radius_mm * 1e-3 * (math.log(8 * radius_mm / gmd_mm) - 2)


def arc_mutual(r1_mm, r2_mm, d_mm, theta):
    """The mutual partial inductance of two coaxial circular arcs of radii r1 and r2 over the same angle theta
    (radians), in planes d apart, by Neumann's double integral:
    mu0 r1 r2 / 4 pi  int int cos(p1 - p2) / sqrt(r1^2 + r2^2 - 2 r1 r2 cos(p1 - p2) + d^2) dp1 dp2, both over
    [0, theta]. For theta = 2 pi it is Maxwell's formula for two coaxial rings."""
    from scipy import integrate
    a, b, d = r1_mm * 1e-3, r2_mm * 1e-3, d_mm * 1e-3

    def f(u):                       # the double integral as one over u = p1 - p2, weighted by (theta - |u|)
        return (theta - abs(u)) * math.cos(u) / math.sqrt(a * a + b * b - 2 * a * b * math.cos(u) + d * d)
    v, _ = integrate.quad(f, -theta, theta, points=[0.0], limit=400, epsabs=1e-14)
    return MU0 * a * b / (4 * math.pi) * v


def arc_inductance(radius_mm, theta, gmd_mm):
    """The partial inductance of a circular arc of angle theta (radians), by the GMD method: a conductor's
    self-inductance is the mutual inductance of two filaments its cross-section's geometric mean distance g apart,
    here two coaxial arcs g apart (arc_mutual). For theta = 2 pi it is Maxwell's formula for two coaxial rings g
    apart, which is Grover's ring formula to O(g^2 / R^2)."""
    return arc_mutual(radius_mm, radius_mm, gmd_mm, theta)
