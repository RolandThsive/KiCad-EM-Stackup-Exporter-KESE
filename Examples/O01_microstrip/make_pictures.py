"""O01's pictures for the wiki, from openEMS's own output: nothing here is drawn by hand.

    python make_pictures.py [--out DIR]

Needs results.json (and results_h0.1.json, results_h0.2_z12.json when present) and the field dump of
`python simulation.py --dump` in case/h0.2_dump/. Writes lossless WebP files into DIR (default pictures/):

    oemsresults_1_eps_eff.webp   eps_eff against frequency: from S21, from port 1's probes, Kirschning-Jansen
    oemsresults_2_z0.webp        Z0 against frequency: port 1's probes and Hammerstad-Jensen
    oemsresults_3_field.webp     an animation of Ez halfway through the core as the pulse runs down the line
    oemsresults_4_section.webp   E and H across the line at 3 GHz: what the line's wave looks like inside
                                 (needs the dumps of `python simulation.py --section`, in case/h0.2_section/)
    oemsresults_5_power.webp     where the power sent into port 1 goes: arrives at port 2, lost, reflected
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

INK, INK2, GRID, SURFACE = '#0b0b0b', '#52514e', '#e4e3df', '#fcfcfb'
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'


def style(ax, xlabel, ylabel):
    ax.set_facecolor(SURFACE)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_xlabel(xlabel, color=INK2, fontsize=10)
    ax.set_ylabel(ylabel, color=INK2, fontsize=10)


def save(fig, path):
    fig.savefig(path, format='webp', dpi=200, facecolor=SURFACE, pil_kwargs=dict(lossless=True))
    print('wrote', path)


def charts(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    r = json.loads((HERE / 'results.json').read_text())
    f = np.asarray(r['data']['frequency_hz']) / 1e9
    ref = r['references']
    e_s21 = np.asarray(r['data']['eps_eff_from_S21'])
    e_port = np.asarray(r['data']['lines']['1']['eps_eff'])
    z_port = np.asarray([v[0] for v in r['data']['lines']['1']['Z_line_ohm']])

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    fig.patch.set_facecolor(SURFACE)
    ax.plot(f, ref['eps_eff'], color=INK2, lw=2, ls='--', label='Kirschning–Jansen (the textbook formula)')
    ax.plot(f, e_s21, color=BLUE, lw=2, label="openEMS, from S21's phase over 38 mm")
    ax.plot(f, e_port, color=ORANGE, lw=2, label="openEMS, port 1's probes (1.8 mm apart: less exact)")
    fine = HERE / 'results_h0.1.json'
    if fine.exists():
        e_fine = json.loads(fine.read_text())['data']['eps_eff_from_S21']
        ax.plot(f, e_fine, color=AQUA, lw=0, marker='o', ms=3.5, markevery=4,
                label='openEMS, from S21, h 0.1 mm')
    style(ax, 'frequency (GHz)', 'εeff')
    ax.set_title('O01: εeff, which sets how fast the signal runs along the line', color=INK, fontsize=10.5,
                 loc='left')
    k3 = int(np.argmin(abs(f - 3.0)))
    v = 1 / np.sqrt(e_s21[k3])
    ax.text(0.98, 0.04, f'at 3 GHz εeff = {e_s21[k3]:.2f}: the signal runs at c/√εeff = {v:.2f} c, '
            f'{v * 299.79:.0f} mm a nanosecond\n(air would give εeff 1, the FR-4 alone 4.4: the field is partly '
            'in the air above the strip)', transform=ax.transAxes, ha='right', va='bottom', fontsize=7.5, color=INK2)
    ax.set_ylim(3.30, 3.56)
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc='upper left')
    fig.tight_layout()
    save(fig, out / 'oemsresults_1_eps_eff.webp')
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    fig.patch.set_facecolor(SURFACE)
    ax.axhline(ref['Z0_ohm'], color=INK2, lw=2, ls='--', label='Hammerstad–Jensen (static)')
    ax.plot(f, z_port, color=BLUE, lw=2, label="openEMS, port 1's probes")
    style(ax, 'frequency (GHz)', 'Z0 (Ω)')
    ax.set_ylim(48, 53)
    ax.set_title('O01: Z0, the line\'s impedance (the line was drawn for 50 Ω)', color=INK, fontsize=10.5,
                 loc='left')
    z1 = z_port[int(np.argmin(abs(f - 1.0)))]
    ax.annotate(f'{z1:.1f} Ω at 1 GHz, {100 * (z1 / ref["Z0_ohm"] - 1):+.1f} % from the formula',
                xy=(1.0, z1), xytext=(1.25, 52.25), fontsize=8, color=INK2,
                arrowprops=dict(arrowstyle='-', color=INK2, lw=0.8))
    ax.text(0.02, 0.04, 'the formula is the static Z0; a real line\'s Z0 rises a little\nwith frequency, as more of '
            'the field draws into the FR-4', transform=ax.transAxes, ha='left', va='bottom', fontsize=7.5, color=INK2)
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc='lower right')
    fig.tight_layout()
    save(fig, out / 'oemsresults_2_z0.webp')
    plt.close(fig)


def field(out, step=1):
    """Ez in the plane halfway through the core, every dumped sample, on openEMS's own mesh."""
    import h5py
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from PIL import Image
    r = json.loads((HERE / 'results.json').read_text())
    s = r['settings']
    h5 = h5py.File(HERE / 'case' / 'h0.2_dump' / 'Et_core.h5', 'r')
    x = np.asarray(h5['Mesh/x']) * 1e3       # m to mm when openEMS writes metres
    y = np.asarray(h5['Mesh/y']) * 1e3
    if np.ptp(x) > 1e4:                       # already in mm (drawing units)
        x, y = x / 1e3, y / 1e3
    td = h5['FieldData/TD']
    keys = sorted(td.keys())[::step]
    ez = [np.asarray(td[k])[2, :, :, 0].T for k in keys]
    times = [float(td[k].attrs['time'][0]) for k in keys]
    vmax = np.percentile(np.abs(np.concatenate([e.ravel() for e in ez])), 99.5)
    cmap = LinearSegmentedColormap.from_list('div', [BLUE, '#e9e8e4', ORANGE])
    cx, cy = 100.0, -100.0
    L, W, w = s['length_mm'], 30.0, s['width_mm']
    frames = []
    for e, t in zip(ez, times):
        fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=150)
        fig.patch.set_facecolor(SURFACE)
        pm = ax.pcolormesh(x, y, e / vmax, cmap=cmap, vmin=-1, vmax=1, shading='nearest', rasterized=True)
        cb = fig.colorbar(pm, ax=ax, fraction=0.035, pad=0.02, ticks=[-1, 0, 1])
        cb.ax.tick_params(colors=INK2, labelsize=8)
        cb.set_label('Ez, relative', color=INK2, fontsize=8)
        cb.outline.set_visible(False)
        ax.plot([cx - L / 2, cx + L / 2, cx + L / 2, cx - L / 2, cx - L / 2],
                [cy - W / 2, cy - W / 2, cy + W / 2, cy + W / 2, cy - W / 2], color=INK, lw=1.6)
        ax.plot([cx - L / 2, cx + L / 2], [cy - w / 2] * 2, color=INK2, lw=0.8, ls=':')
        ax.plot([cx - L / 2, cx + L / 2], [cy + w / 2] * 2, color=INK2, lw=0.8, ls=':')
        ax.set_aspect('equal')
        ax.set_xlim(x[0], x[-1])
        ax.set_ylim(y[0], y[-1])
        ax.set_xlabel('x (mm)', color=INK2, fontsize=9)
        ax.set_ylabel('y (mm)', color=INK2, fontsize=9)
        ax.tick_params(colors=INK2, labelsize=8)
        ax.set_title(f'O01: Ez halfway through the core, t = {t * 1e12:4.0f} ps (board edge black, strip dotted)',
                     color=INK, fontsize=9, loc='left')
        fig.tight_layout()
        fig.canvas.draw()
        frames.append(Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()))
        plt.close(fig)
    path = out / 'oemsresults_3_field.webp'
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=90, loop=0, lossless=True)
    print('wrote', path, f'({len(frames)} frames)')


def power(out):
    """Where the power sent into port 1 goes, from S11 and S21: |S21|^2 arrives at port 2, |S11|^2 comes back, the
    rest is lost on the way (heat in the FR-4, a little radiation)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    r = json.loads((HERE / 'results.json').read_text())
    f = np.asarray(r['data']['frequency_hz']) / 1e9
    s11 = np.array([complex(*v) for v in r['data']['S']['S11']])
    s21 = np.array([complex(*v) for v in r['data']['S']['S21']])
    expect = 100 * 10 ** (-np.asarray(r['references']['dielectric_loss_db']) / 10)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    fig.patch.set_facecolor(SURFACE)
    rows = [1.0, 2.0, 3.0, 4.0]
    for i, fr in enumerate(rows):
        k = int(np.argmin(abs(f - fr)))
        arrive, back = 100 * abs(s21[k]) ** 2, 100 * abs(s11[k]) ** 2
        lost = 100 - arrive - back
        yy = len(rows) - 1 - i
        ax.barh(yy, arrive, color=BLUE, height=0.56, edgecolor=SURFACE, linewidth=2)
        ax.barh(yy, lost, left=arrive, color=ORANGE, height=0.56, edgecolor=SURFACE, linewidth=2)
        ax.text(arrive / 2, yy, f'{arrive:.1f} % arrives at port 2', ha='center', va='center', color='white',
                fontsize=8.5)
        back_t = 'under 0.001 %' if back < 0.001 else f'{back:.2g} %'
        ax.text(101.5, yy, f'{lost:.1f} % lost on the way\n{back_t} reflected', ha='left', va='center',
                color=INK2, fontsize=7.5)
        ax.plot([expect[k]] * 2, [yy - 0.36, yy + 0.36], color=INK, lw=1.4)
    ax.text(expect[0], len(rows) - 0.42, 'expected from the FR-4\'s loss alone', ha='right', va='bottom',
            fontsize=7.5, color=INK)
    ax.set_yticks(range(len(rows)), [f'{fr:g} GHz' for fr in reversed(rows)])
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(rows) - 0.1)
    style(ax, 'share of the power sent into port 1 (%)', '')
    ax.grid(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.set_title('O01: where the power goes on the 38 mm between the two measurement planes', color=INK,
                 fontsize=10.5, loc='left')
    fig.subplots_adjust(left=0.1, right=0.76, top=0.88, bottom=0.16)
    save(fig, out / 'oemsresults_5_power.webp')
    plt.close(fig)


def section(out):
    """E and H across the line at 3 GHz, halfway along it, from openEMS's frequency-domain dumps: a snapshot at the
    phase where E is strongest. Colour: the field's strength; arrows (E) and lines (H): its direction."""
    import h5py
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.patches import Rectangle
    from scipy.interpolate import RegularGridInterpolator
    if str(HERE.parent.parent) not in sys.path:
        sys.path.insert(0, str(HERE.parent.parent))
    from bridge import fdtd as F
    r = json.loads((HERE / 'results.json').read_text())
    s = r['settings']
    parts, _m = F.load(F.kese_export(HERE / s['board'], HERE / 'case' / 'kese', log=lambda *a: None))
    board = next(p for p in parts if p.role == 'board')
    trace = next(p for p in parts if p.net == 'RF')
    gnd = next(p for p in parts if p.role == 'copper' and p.net != 'RF')
    yc = F.kicad_to_model(*s['centre_kicad'])[1]
    w = s['width_mm']

    def load(name):
        h = h5py.File(HERE / 'case' / 'h0.2_section' / f'{name}.h5', 'r')
        y = np.asarray(h['Mesh/y']) * 1e3 - yc
        z = np.asarray(h['Mesh/z']) * 1e3
        k = [n for n in h['FieldData/FD'] if abs(h['FieldData/FD'][n].attrs['frequency'] - 3e9) < 1][0]
        return y, z, np.asarray(h['FieldData/FD'][k])[:, 0, :, :]          # (3, ny, nz)
    y, z, E = load('Ef_section')
    _y, _z, H = load('Hf_section')
    phis = np.linspace(0, np.pi, 90)
    phi = phis[int(np.argmax([(np.real(E * np.exp(-1j * p)) ** 2).sum() for p in phis]))]
    Er, Hr = np.real(E * np.exp(-1j * phi)), np.real(H * np.exp(-1j * phi))
    under = (abs(y)[:, None] < w / 4) & (z[None, :] > board.z[0]) & (z[None, :] < board.z[1])
    if Er[2][under].mean() > 0:                  # the snapshot half a period on, where E points from strip to ground
        Er, Hr = -Er, -Hr
    Ylim, Zlim = (-7.0, 7.0), (gnd.z[0] - 0.6, trace.z[1] + 3.2)
    yu = np.linspace(*Ylim, 281)
    zu = np.linspace(*Zlim, 141)
    YY, ZZ = np.meshgrid(yu, zu)
    pts = np.stack([YY.ravel(), ZZ.ravel()], axis=1)

    def grid(a):
        return RegularGridInterpolator((y, z), a, bounds_error=False, fill_value=0.0)(pts).reshape(YY.shape)
    inside = (ZZ < gnd.z[1]) | ((ZZ > trace.z[0]) & (ZZ < trace.z[1]) & (abs(YY) < w / 2))   # copper: no field
    cmaps = (LinearSegmentedColormap.from_list('e', ['#fcfcfb', '#cfe0f5', BLUE, '#0d3a75']),
             LinearSegmentedColormap.from_list('h', ['#fcfcfb', '#fbd9c9', ORANGE, '#8a3313']))
    fig, axes = plt.subplots(2, 1, figsize=(6.6, 5.4), sharex=True)
    fig.patch.set_facecolor(SURFACE)
    for ax, F3, name, cmap in ((axes[0], Er, 'E', cmaps[0]), (axes[1], Hr, 'H', cmaps[1])):
        fy, fz = grid(F3[1]), grid(F3[2])
        mag = np.hypot(fy, fz)
        mag[inside] = np.nan
        fy[inside], fz[inside] = 0.0, 0.0
        vmax = np.nanpercentile(mag, 99.0)
        ax.pcolormesh(yu, zu, mag / vmax, cmap=cmap, vmin=0, vmax=1, shading='gouraud', rasterized=True)
        if name == 'E':
            sy, sz = slice(6, None, 14), slice(4, None, 9)
            ny_, nz_ = fy[sz, sy], fz[sz, sy]
            nn = np.hypot(ny_, nz_)
            ok = nn > 0.03 * vmax
            ln = np.clip(nn / vmax, 0, 1) ** 0.4 / np.maximum(nn, 1e-30)      # longer where stronger
            ax.quiver(YY[sz, sy][ok], ZZ[sz, sy][ok], (ny_ * ln)[ok], (nz_ * ln)[ok], color=INK, scale=40,
                      width=0.0028, headwidth=4, headlength=4.5, headaxislength=4)
        else:
            ax.streamplot(yu, zu, fy, fz, color=INK, density=(1.4, 0.9), linewidth=0.7, arrowsize=0.7)
        ax.add_patch(Rectangle((Ylim[0], board.z[0]), Ylim[1] - Ylim[0], board.z[1] - board.z[0], fill=False,
                               ls='--', lw=0.8, ec=INK2))
        ax.add_patch(Rectangle((-w / 2, trace.z[0]), w, trace.z[1] - trace.z[0] + 0.06, color='#d62828', zorder=5))
        ax.add_patch(Rectangle((Ylim[0], gnd.z[0] - 0.06), Ylim[1] - Ylim[0], gnd.z[1] - gnd.z[0] + 0.06,
                               color='#1e64c8', zorder=5))
        ax.set_aspect('equal')
        ax.set_xlim(*Ylim)
        ax.set_ylim(*Zlim)
        ax.set_facecolor(SURFACE)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.tick_params(colors=INK2, labelsize=8)
        ax.set_ylabel('z (mm)', color=INK2, fontsize=9)
        box = dict(boxstyle='round,pad=0.15', fc=SURFACE, ec='none', alpha=0.85)
        ax.text(Ylim[0] + 0.2, (board.z[0] + board.z[1]) / 2, 'FR-4', color=INK2, fontsize=8, va='center', bbox=box,
                zorder=6)
        ax.text(Ylim[0] + 0.2, trace.z[1] + 2.6, 'air', color=INK2, fontsize=8, va='center', bbox=box, zorder=6)
    axes[0].set_title('E, the electric field: from the strip down to the ground, mostly inside the FR-4',
                      color=INK, fontsize=9.5, loc='left')
    axes[1].set_title('H, the magnetic field: lines that circle the strip', color=INK, fontsize=9.5, loc='left')
    axes[1].set_xlabel('across the line (mm); the strip (red) is 2.9 mm wide, the ground (blue) runs under the '
                       'whole board', color=INK2, fontsize=8.5)
    fig.suptitle('O01 at 3 GHz, from openEMS: the wave\'s field across the line, halfway along it', color=INK,
                 fontsize=10.5, x=0.02, ha='left')
    fig.text(0.02, 0.005, 'Colour: the field\'s strength (darker is stronger), each panel against its own peak. '
             'A snapshot at the moment E is strongest.', color=INK2, fontsize=7.5)
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    save(fig, out / 'oemsresults_4_section.webp')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(HERE / 'pictures'))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    charts(out)
    power(out)
    if (HERE / 'case' / 'h0.2_section' / 'Ef_section.h5').exists():
        section(out)
    else:
        print('no section dumps: run python simulation.py --section first')
    if (HERE / 'case' / 'h0.2_dump' / 'Et_core.h5').exists():
        field(out)
    else:
        print('no field dump: run python simulation.py --dump first')


if __name__ == '__main__':
    main()
