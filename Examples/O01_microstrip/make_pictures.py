"""O01's pictures for the wiki, from openEMS's own output: nothing here is drawn by hand.

    python make_pictures.py [--out DIR]

Needs results.json (and results_h0.1.json, results_h0.2_z12.json when present) and the field dump of
`python simulation.py --dump` in case/h0.2_dump/. Writes lossless WebP files into DIR (default pictures/):

    oemsresults_1_eps_eff.webp   eps_eff against frequency: from S21, from port 1's probes, Kirschning-Jansen
    oemsresults_2_z0.webp        Z0 against frequency: port 1's probes and Hammerstad-Jensen
    oemsresults_3_field.webp     an animation of Ez halfway through the core as the pulse runs down the line
"""
from __future__ import annotations

import argparse
import json
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
    ax.plot(f, ref['eps_eff'], color=INK2, lw=2, ls='--', label='Kirschning–Jansen')
    ax.plot(f, e_s21, color=BLUE, lw=2, label='openEMS, from S21')
    ax.plot(f, e_port, color=ORANGE, lw=2, label="openEMS, port 1's probes")
    fine = HERE / 'results_h0.1.json'
    if fine.exists():
        e_fine = json.loads(fine.read_text())['data']['eps_eff_from_S21']
        ax.plot(f, e_fine, color=AQUA, lw=0, marker='o', ms=3.5, markevery=4,
                label='openEMS, from S21, h 0.1 mm')
    style(ax, 'frequency (GHz)', 'εeff')
    ax.set_title('O01: effective permittivity of the 2.9 mm line on 1.53 mm FR-4', color=INK, fontsize=10.5,
                 loc='left')
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
    ax.set_title('O01: characteristic impedance', color=INK, fontsize=10.5, loc='left')
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc='upper left')
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=str(HERE / 'pictures'))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    charts(out)
    if (HERE / 'case' / 'h0.2_dump' / 'Et_core.h5').exists():
        field(out)
    else:
        print('no field dump: run python simulation.py --dump first')


if __name__ == '__main__':
    main()
