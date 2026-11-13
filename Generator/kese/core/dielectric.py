"""How a dielectric's er and tan d change with frequency: the "dielectric_model" entry a laminate
part gets in materials.json (Board.DIELECTRIC_MODEL, or the board file's (dielectric_model ...)).

The Djordjevic-Sarkar model is the wideband model usual for glass-epoxy laminates (Djordjevic,
Biljic, Likar-Smiljanic and Sarkar, IEEE Trans. EMC 43(4), 2001):

    er(f) = epsilon_inf + delta_epsilon / ln(f_high / f_low) * ln((f_high + j f) / (f_low + j f))

Its real part is er and its imaginary part -er * tan d.  It is fitted to one er and tan d at the
spec frequency, as KiCad fits it (common/transline_calculations/dielectric_djordjevic_sarkar.cpp),
between the corner frequencies Board.DS_LOW_FREQUENCY_HZ and Board.DS_HIGH_FREQUENCY_HZ."""
import cmath
import math

from parameters import P


def ds_fits(f_spec, f_low, f_high):
    """Whether the model can be fitted: the corners in order, the spec frequency between them."""
    return 0 < f_low < f_high and f_low <= f_spec <= f_high


def ds_fit(epsilon_r, loss_tangent, f_spec, f_low, f_high):
    """(epsilon_inf, delta_epsilon) of the model that has epsilon_r and loss_tangent at f_spec."""
    if loss_tangent == 0:
        return float(epsilon_r), 0.0
    k = cmath.log((f_high + 1j * f_spec) / (f_low + 1j * f_spec))
    m = -loss_tangent * epsilon_r / k.imag
    return epsilon_r * (1 + loss_tangent * k.real / k.imag), m * math.log(f_high / f_low)


def ds_at(epsilon_inf, delta_epsilon, f, f_low, f_high):
    """(er, tan d) of the model at frequency f."""
    e = epsilon_inf + delta_epsilon / math.log(f_high / f_low) * cmath.log((f_high + 1j * f) / (f_low + 1j * f))
    return e.real, -e.imag / e.real


def model_props(model, epsilon_r, loss_tangent, f_spec):
    """The "dielectric_model" entry of materials.json for one solid: the model's name, and what a
    solver needs to use it."""
    B = P.Board
    low, high = B.DS_LOW_FREQUENCY_HZ, B.DS_HIGH_FREQUENCY_HZ
    if model == "djordjevic_sarkar" and ds_fits(f_spec, low, high):
        epsilon_inf, delta = ds_fit(epsilon_r, loss_tangent, f_spec, low, high)
        return {"model": model, "spec_frequency_hz": f_spec, "low_frequency_hz": low, "high_frequency_hz": high,
                "epsilon_inf": round(epsilon_inf, 6), "delta_epsilon": round(delta, 6)}
    if model == "table":
        return {"model": model, "table": [list(row) for row in B.DIELECTRIC_TABLE]}
    return {"model": "constant"}


def check_models(dielectrics, log):
    """A ply whose model cannot be written as asked is written with constant values, with a warning:
    a Djordjevic-Sarkar model that cannot be fitted (its spec frequency is not between the corner
    frequencies), as KiCad falls back, and a table where Board.DIELECTRIC_TABLE is empty."""
    B = P.Board
    for d in dielectrics:
        for ply in d.plies:
            if ply.model == "djordjevic_sarkar" and not ds_fits(ply.frequency_hz, B.DS_LOW_FREQUENCY_HZ, B.DS_HIGH_FREQUENCY_HZ):
                log(f"warning: {ply.name}: the Djordjevic-Sarkar model needs its spec frequency ({ply.frequency_hz:g} Hz) "
                    f"between Board.DS_LOW_FREQUENCY_HZ ({B.DS_LOW_FREQUENCY_HZ:g}) and Board.DS_HIGH_FREQUENCY_HZ "
                    f"({B.DS_HIGH_FREQUENCY_HZ:g}): written with constant values")
                ply.model = "constant"
            if ply.model == "table" and not B.DIELECTRIC_TABLE:
                log(f"warning: {ply.name}: its dielectric model is \"table\" but Board.DIELECTRIC_TABLE is empty: "
                    "written with constant values")
                ply.model = "constant"
        d.model = d.plies[0].model
