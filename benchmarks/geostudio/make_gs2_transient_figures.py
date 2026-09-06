"""Render the isochrone comparison figures for the SEEP/W transient corpus
(SEEPW-T01 consolidation, SEEPW-T02 infiltration) in
docs/verification/geostudio.md, "Transient seepage (SEEP/W)".

Both are LINE profiles (the native form of the published figures), so the
field-plot frame spec (equal aspect / colorbars) does not apply; each panel
shares axes and a uniform margin, following the GW transient figures.

  gs2_cons.png   Terzaghi excess PWP vs elevation at t = 150/604/1460 s
                 -- closed form (lines), XSLOPE (open markers), SEEP/W (dots)
  gs2_infil.png  pressure head vs elevation at t = 46 800 s
                 -- SEEP/W node.csv oracle (line), XSLOPE (open markers)
  gs2_rdd_fs.png T03 factor of safety vs time, both drawdown rates
                 -- XSLOPE (line), SLOPE/W slip_surface.csv minimum (open markers)

The SEEP/W profiles are the vendor .gsz node.csv results, DISTILLED to plain
arrays here (downsampled); the .gsz itself is never committed.

Run from the repo root:
  PYTHONPATH=. python3 benchmarks/geostudio/make_gs2_transient_figures.py
"""

import io
import os
import sys
import contextlib
import warnings

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from xslope.fileio import load_slope_data
from xslope.mesh import get_material_polygons, build_mesh_from_polygons
from xslope.seep import (build_seep_data, build_tseep_data,
                         run_transient_seepage, transient_frame_index)

import build_gs2_cons as C
import build_gs2_infil as I
import build_gs2_rdd as R
import build_gs2_heap as HP
import build_gs2_pond as PD

SRC = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'verification',
                   'files', 'geostudio')
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'verification', 'images')

_COLORS = ['#1f77b4', '#d62728', '#2ca02c']

# --- SEEP/W node.csv oracle, distilled (downsampled) from the vendor .gsz -----
# T01 excess PWP (kPa) at y = 0..0.05 (11 pts), t = 150/604/1460 s
_SW_CONS_Y = np.arange(0.0, 0.0501, 0.005)
_SW_CONS = {
    150.0: [0.0, 5.366, 8.235, 9.374, 9.766, 9.859, 9.766, 9.374, 8.235, 5.366, 0.0],
    604.0: [0.0, 2.736, 5.022, 6.635, 7.564, 7.864, 7.564, 6.635, 5.022, 2.736, 0.0],
    1460.0: [0.0, 1.516, 2.860, 3.899, 4.549, 4.770, 4.549, 3.899, 2.860, 1.516, 0.0],
}
# T02 pressure head (m) at y = 0..1 (21 pts), t = 46 800 s
_SW_INF_Y = np.arange(0.0, 1.001, 0.05)
_SW_INF_PSI = [-7.9976, -7.9991, -7.9998, -8.0, -8.0, -8.0, -7.9997, -7.4188,
               -1.6328, -0.7241, -0.4171, -0.2599, -0.1656, -0.1047, -0.0642,
               -0.0372, -0.0197, -0.0090, -0.0033, -0.0011, 0.0]


def _legend_below(fig, handles, ncol, title=None, labels=None):
    """Put the legend in reserved space under the axes, never over the data.

    The reserve is measured from the legend's own rendered height, so a
    two-row legend and a four-row legend both clear the axes without a
    hand-tuned margin; the column count is capped so the legend never runs
    past the figure's width.
    """
    kw = dict(loc='lower center', ncol=ncol, fontsize=8.5, frameon=False)
    if title:
        kw['title'] = title
    leg = fig.legend(handles, labels, **kw) if labels is not None \
        else fig.legend(handles=handles, **kw)
    fig.canvas.draw()
    bb = leg.get_window_extent().transformed(fig.transFigure.inverted())
    if bb.width > 0.98:               # too wide: halve the columns and re-measure
        leg.remove()
        return _legend_below(fig, handles, max(1, ncol // 2), title, labels)
    fig.tight_layout(rect=(0, bb.height + 0.02, 1, 1))
    return leg


def _solve(stem, target_size, frac, refine=None):
    sd = load_slope_data(os.path.join(SRC, f'{stem}.xlsx'))
    ts = build_tseep_data(sd)
    kw = {} if refine is None else {'refine_factor': float(refine)}
    mesh = build_mesh_from_polygons(get_material_polygons(sd), target_size, 'tri3',
                                    **kw)
    seep = build_seep_data(mesh, sd)
    with contextlib.redirect_stdout(io.StringIO()):
        sol = run_transient_seepage(seep, ts, max_head_change_frac=frac, verbose=False)
    _sample.mesh = seep          # the sampler interpolates inside this mesh
    return seep['nodes'], sol


def _sample(nodes, h, xq, yq):
    """The finite-element field at (xq, yq): interpolated inside the element that
    contains the point, with the shape functions the solver used. A point that
    sits on the mesh boundary and misses every element by round-off takes the
    nearest node's value, which on a boundary is exact."""
    from xslope.mesh import interpolate_at_point
    mesh = _sample.mesh
    val, found = interpolate_at_point(mesh['nodes'], mesh['elements'],
                                      mesh['element_types'], np.asarray(h),
                                      (float(xq), float(yq)),
                                      return_found=True, signed=True)
    if found:
        return float(val)
    d2 = (nodes[:, 0] - xq) ** 2 + (nodes[:, 1] - yq) ** 2
    return float(np.asarray(h)[int(np.argmin(d2))])


def fig_cons():
    cv = C._cv()
    ys = np.linspace(0.0, 0.05, 200)
    ys_s = np.linspace(0.004, 0.046, 11)
    nodes, sol = _solve('gs2_cons', 0.001, 0.02)
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for c, t in zip(_COLORS, C._SAVES):
        Tv = cv * t / (C._H * C._H)
        ax.plot(C._U0 * C.terzaghi_ue(ys / C._H, Tv), ys, '-', color=c, lw=1.7,
                label=f't = {t:g} s  ($T_v$ = {Tv:.2f})')
        ax.plot(_SW_CONS[t], _SW_CONS_Y, '.', color=c, ms=7)
        h = np.asarray(sol['frames'][transient_frame_index(sol, t)]['head'])
        ue = np.array([C._GW * (_sample(nodes, h, C._WIDTH / 2, y) - C._H_REF)
                       for y in ys_s])
        ax.plot(ue, ys_s, 'o', color=c, ms=5.5, mfc='white', mew=1.3)
    ax.set_xlabel('excess pore-water pressure  $u_e$  (kPa)')
    ax.set_ylabel('elevation  y  (m)   [drained at y = 0 and y = 0.05]')
    ax.set_title('SEEPW-T01 — Terzaghi 1-D consolidation (double drainage)',
                 fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_xlim(-0.3, 10.3)
    handles = ax.get_legend_handles_labels()[0]
    handles += [Line2D([], [], marker='o', color='0.3', ls='none', mfc='white',
                       mew=1.3, ms=6, label='XSLOPE'),
                Line2D([], [], marker='.', color='0.3', ls='none', ms=8, label='SEEP/W')]
    _legend_below(fig, handles, ncol=5, title='Terzaghi Eq 17.3 (lines)')
    fig.savefig(os.path.join(OUT, 'gs2_cons.png'), dpi=150)
    plt.close(fig)
    return 'gs2_cons.png'


def fig_infil():
    ys_s = np.linspace(0.05, 0.98, 20)
    nodes, sol = _solve('gs2_infil', 0.01, 0.01)
    h = np.asarray(sol['frames'][transient_frame_index(sol, I._SAVE)]['head'])
    psi = np.array([_sample(nodes, h, I._WIDTH / 2, y) - y for y in ys_s])
    fig, ax = plt.subplots(figsize=(6.5, 6))
    ax.plot(_SW_INF_PSI, _SW_INF_Y, '-', color='#1f77b4', lw=1.8,
            label='SEEP/W (node.csv oracle)')
    ax.plot(psi, ys_s, 'o', color='#d62728', ms=5.5, mfc='white', mew=1.3,
            label='XSLOPE')
    ax.axvline(0.0, color='0.6', ls='--', lw=0.9)
    ax.set_xlabel('pressure head  $\\psi$  (m)')
    ax.set_ylabel('elevation  y  (m)   [ponded at y = 1]')
    ax.set_title('SEEPW-T02 — infiltration into dry soil, t = 46 800 s',
                 fontsize=11)
    ax.grid(alpha=0.3)
    _legend_below(fig, ax.get_legend_handles_labels()[0], ncol=2)
    fig.savefig(os.path.join(OUT, 'gs2_infil.png'), dpi=150)
    plt.close(fig)
    return 'gs2_infil.png'


# --- SEEPW-T03 rapid drawdown: SEEP/W node.csv oracle, distilled -------------
# total head (m) at interior stations (20,5),(25,5),(30,3),(35,2) at the vendor
# save times, for the instantaneous and slow drawdown cases (the .gsz is never
# committed).
_RDD_T = [0, 21600, 54259, 103638, 178298, 291181, 461858, 719916, 1110093,
          1700031, 2592000]
_RDD_STATIONS = [(20, 5), (25, 5), (30, 3), (35, 2)]
# Derived from the vendor .gsz exactly as the page's reference column states: total
# head h = y + u/gamma_w built from each step's node.csv on mesh_1.ply, sampled at the
# station by inverse-squared distance over the four nearest nodes -- the same probe the
# runner reads XSLOPE's field with. Mapping check: the 19 upstream-face nodes read
# h = 8.000000 and the 11 drain nodes h = 0.000000, the vendor's own Dirichlet values.
_SW_RDD = {
    'inst': {
        (20, 5): [7.280, 6.766, 6.355, 6.051, 5.785, 5.520, 5.235, 4.923, 4.581, 4.210, 3.808],
        (25, 5): [6.258, 6.161, 6.003, 5.831, 5.650, 5.447, 5.209, 4.927, 4.602, 4.239, 3.838],
        (30, 3): [5.008, 4.981, 4.915, 4.828, 4.725, 4.597, 4.433, 4.221, 3.956, 3.635, 3.262],
        (35, 2): [3.424, 3.419, 3.402, 3.372, 3.327, 3.262, 3.165, 3.030, 2.847, 2.614, 2.331]},
    'slow': {
        (20, 5): [7.280, 7.136, 6.867, 6.509, 6.111, 5.714, 5.359, 5.008, 4.640, 4.252, 3.838],
        (25, 5): [6.258, 6.233, 6.158, 6.018, 5.817, 5.571, 5.301, 4.998, 4.655, 4.277, 3.866],
        (30, 3): [5.008, 5.002, 4.975, 4.914, 4.812, 4.671, 4.493, 4.272, 3.998, 3.669, 3.288],
        (35, 2): [3.424, 3.423, 3.416, 3.398, 3.360, 3.296, 3.199, 3.061, 2.875, 2.637, 2.350]}}
_RDD_COLORS = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd']


def fig_rdd():
    from xslope.seep import transient_frame_index
    day = 86400.0
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    for ax, (stem, key, title) in zip(axes, [
            ('gs2_rdd_inst', 'inst', 'Instantaneous drawdown (8 m → 0 at t = 0)'),
            ('gs2_rdd_slow', 'slow', 'Slow drawdown (8 → 0 m over 5 d)')]):
        nodes, sol = _solve(stem, 0.7, 0.05)
        tt = np.array([f['time'] for f in sol['frames']])
        for c, st in zip(_RDD_COLORS, _RDD_STATIONS):
            hx = []
            for f in sol['frames']:
                h = np.asarray(f['head'])
                hx.append(_sample(nodes, h, st[0], st[1]))
            ax.plot(tt / day, hx, '-', color=c, lw=1.6,
                    label=f'({st[0]}, {st[1]})')
            ax.plot(np.array(_RDD_T) / day, _SW_RDD[key][st], 'o', color=c,
                    ms=5, mfc='white', mew=1.2)
        ax.set_xlabel('time  (days)')
        ax.set_title(title, fontsize=10.5)
        ax.grid(alpha=0.3)
        ax.set_xlim(-1, 31)
    axes[0].set_ylabel('total head  h  (m)   at interior stations')
    handles = []
    for c, st in zip(_RDD_COLORS, _RDD_STATIONS):
        handles.append(Line2D([], [], color=c, lw=1.6,
                              label=f'XSLOPE at ({st[0]}, {st[1]})'))
        handles.append(Line2D([], [], marker='o', color=c, ls='none', mfc='white',
                              mew=1.2, ms=5, label=f'SEEP/W at ({st[0]}, {st[1]})'))
    fig.legend(handles=handles, loc='lower center', ncol=len(_RDD_STATIONS),
               fontsize=9, frameon=False)
    fig.suptitle('SEEPW-T03 — reservoir drawdown: interior total head vs time',
                 fontsize=12)
    fig.tight_layout(rect=(0, 0.10, 1, 0.96))
    fig.savefig(os.path.join(OUT, 'gs2_rdd.png'), dpi=150)
    plt.close(fig)
    return 'gs2_rdd.png'


# --- SEEPW-T03 stability: SLOPE/W factor of safety at every saved step -------
# The example's published answer (its Figures 9 and 11), taken from the vendor's
# own solved slip_surface.csv rather than read off the figure: the minimum over
# the 396 trial surfaces of the entry-and-exit search at each of the 11 steps, for
# each drawdown rate. Spencer both sides.
_SW_RDD_FS = {
    'inst': [1.6721, 0.8288, 0.9648, 1.0092, 1.0390, 1.0654, 1.0938, 1.1238,
             1.1567, 1.1939, 1.2336],
    'slow': [1.6721, 1.5786, 1.4801, 1.3656, 1.2356, 1.1072, 1.0781, 1.1142,
             1.1507, 1.1898, 1.2307]}


def fig_rdd_fs():
    """Factor of safety versus time, XSLOPE against SLOPE/W, both drawdown rates.

    One Spencer search per saved frame -- xslope.sensitivity.fs_vs_time over the
    march the seepage panels of gs2_rdd.png verify -- against the vendor's solved
    minimum at the same instant. The two runs take about a minute together.
    """
    from xslope.sensitivity import fs_vs_time
    day = 86400.0
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    for ax, (stem, key, title) in zip(axes, [
            ('gs2_rdd_inst', 'inst', 'Instantaneous drawdown (8 m → 0 at t = 0)'),
            ('gs2_rdd_slow', 'slow', 'Slow drawdown (8 → 0 m over 5 d)')]):
        sd = load_slope_data(os.path.join(SRC, f'{stem}.xlsx'))
        mesh = build_mesh_from_polygons(get_material_polygons(sd), 0.7, 'tri3')
        sd['mesh'] = mesh
        with contextlib.redirect_stdout(io.StringIO()):
            sol = run_transient_seepage(build_seep_data(mesh, sd),
                                        build_tseep_data(sd),
                                        max_head_change_frac=0.05, verbose=False)
            ok, res = fs_vs_time(sd, sol, times=_RDD_T, methods=('spencer',),
                                 num_slices=40)
        if not ok:
            raise RuntimeError(f'{stem}: {res}')
        df = res['df']
        ax.plot(np.array(_RDD_T) / day, df['fs'].to_numpy(), '-',
                color=_RDD_COLORS[0], lw=1.6)
        ax.plot(np.array(_RDD_T) / day, _SW_RDD_FS[key], 'o',
                color=_RDD_COLORS[0], ms=5, mfc='white', mew=1.2)
        ax.axhline(1.0, color='0.55', ls='--', lw=0.9)
        ax.set_xlabel('time  (days)')
        ax.set_title(title, fontsize=10.5)
        ax.grid(alpha=0.3)
        ax.set_xlim(-1, 31)
    axes[0].set_ylabel('factor of safety  (Spencer)')
    axes[0].legend(handles=[
        Line2D([], [], color=_RDD_COLORS[0], ls='-', label='XSLOPE'),
        Line2D([], [], marker='o', color=_RDD_COLORS[0], ls='none', mfc='white',
               mew=1.2, ms=6, label='SLOPE/W (slip_surface.csv)'),
        Line2D([], [], color='0.55', ls='--', label='FS = 1')],
        loc='lower right', fontsize=8.5)
    fig.suptitle('SEEPW-T03 — reservoir drawdown: factor of safety vs time',
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(os.path.join(OUT, 'gs2_rdd_fs.png'), dpi=150)
    plt.close(fig)
    return 'gs2_rdd_fs.png'


# --- SEEPW-T05 mineral heap leaching: SEEP/W node.csv oracle, distilled ------
# pressure head (m) vs elevation (y = 0..8, step 0.5) at t = 0/13527/67383/345600 s
# (the .gsz is never committed).
_HEAP_Y = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5,
           7.0, 7.5, 8.0]
_SW_HEAP = {
    0.0: [0.0, -0.4305, -0.6866, -0.7643, -0.7798, -0.7825, -0.783, -0.7831,
          -0.7831, -0.7831, -0.7831, -0.7831, -0.7831, -0.783, -0.7831, -0.7832, -0.7838],
    13527.0: [0.0, -0.4305, -0.6866, -0.7643, -0.7798, -0.7825, -0.783, -0.7831,
              -0.7831, -0.7831, -0.7831, -0.7831, -0.7831, -0.783, -0.7809, -0.671, -0.2742],
    67383.0: [0.0, -0.4305, -0.6866, -0.7643, -0.7798, -0.7825, -0.783, -0.7831,
              -0.7831, -0.783, -0.7821, -0.7732, -0.7053, -0.4898, -0.2883, -0.2001, -0.1714],
    345600.0: [0.0, -0.2926, -0.3584, -0.3146, -0.2614, -0.2214, -0.1952, -0.1794,
               -0.1704, -0.1658, -0.1637, -0.1631, -0.1631, -0.1632, -0.1632, -0.1629, -0.1625],
}
_HEAP_COLORS = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd']


def fig_heap():
    times = [0.0, 13527.0, 67383.0, 345600.0]
    ys_s = np.linspace(0.3, 7.8, 16)
    nodes, sol = _solve('gs2_heap', HP._TARGET, 0.05)
    fig, ax = plt.subplots(figsize=(6.8, 6))
    for c, t in zip(_HEAP_COLORS, times):
        ax.plot(_SW_HEAP[t], _HEAP_Y, '-', color=c, lw=1.6,
                label=f't = {t:g} s')
        h = np.asarray(sol['frames'][transient_frame_index(sol, t)]['head'])
        psi = np.array([_sample(nodes, h, HP._WIDTH / 2, y) - y for y in ys_s])
        ax.plot(psi, ys_s, 'o', color=c, ms=5, mfc='white', mew=1.2)
    ax.axvline(0.0, color='0.6', ls='--', lw=0.9)
    ax.set_xlabel('pressure head  $\\psi$  (m)')
    ax.set_ylabel('elevation  y  (m)   [flux top y = 8, drained base y = 0]')
    ax.set_title('SEEPW-T05 — leach column, irrigation stepped low → high',
                 fontsize=11)
    ax.grid(alpha=0.3)
    handles = ([Line2D([], [], marker='o', color=c, ls='none', mfc='white', mew=1.2,
                       ms=6, label=f'XSLOPE, t = {t:g} s')
                for c, t in zip(_HEAP_COLORS, times)]
               + [Line2D([], [], color=c, lw=1.6, label=f'SEEP/W, t = {t:g} s')
                  for c, t in zip(_HEAP_COLORS, times)])
    _legend_below(fig, handles, ncol=4)
    fig.savefig(os.path.join(OUT, 'gs2_heap.png'), dpi=150)
    plt.close(fig)
    return 'gs2_heap.png'


# --- SEEPW-T04 pond leakage: SEEP/W node.csv oracle, distilled ---------------
# total head (m) at interior stations vs the vendor save times (.gsz not committed)
_POND_T = [0.0, 291469.0, 700647.0, 1275073.0, 2081483.0, 3213564.0, 4802838.0,
           7033946.0, 10166092.0, 14563164.0, 20736000.0]
_POND_STATIONS = [(5, 2), (10, 3), (15, 4), (3, 5)]
# Re-derived from the vendor .gsz the same way as _SW_RDD above: h = y + u/gamma_w
# from each saved step's node.csv on mesh_1.ply, sampled by inverse-squared distance
# over the four nearest nodes.
_SW_POND = {
    (5, 2): [4.000, 4.000, 4.000, 4.003, 4.133, 4.568, 5.073, 5.546, 5.953, 6.266, 6.463],
    (10, 3): [4.000, 4.000, 4.000, 4.001, 4.042, 4.262, 4.630, 5.039, 5.416, 5.712, 5.900],
    (15, 4): [4.000, 4.000, 4.000, 4.000, 4.012, 4.103, 4.311, 4.589, 4.870, 5.095, 5.238],
    (3, 5): [4.000, 4.000, 4.000, 4.006, 4.251, 4.872, 5.436, 5.917, 6.319, 6.627, 6.821],
}
_POND_COLORS = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd']


def fig_pond():
    day = 86400.0
    nodes, sol = _solve('gs2_pond', PD._TARGET, 0.05, refine=PD._REFINE)
    tt = np.array([f['time'] for f in sol['frames']])
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for c, st in zip(_POND_COLORS, _POND_STATIONS):
        hx = [_sample(nodes, np.asarray(f['head']), st[0], st[1])
              for f in sol['frames']]
        ax.plot(tt / day, hx, '-', color=c, lw=1.6, label=f'({st[0]}, {st[1]})')
        ax.plot(np.array(_POND_T) / day, _SW_POND[st], 'o', color=c, ms=5,
                mfc='white', mew=1.2)
    ax.set_xlabel('time  (days)')
    ax.set_ylabel('total head  h  (m)   at interior stations')
    ax.set_title('SEEPW-T04 — clay-lined pond leakage: water-table rise vs time',
                 fontsize=11)
    ax.grid(alpha=0.3)
    handles = ([Line2D([], [], color=c, lw=1.6, label=f'XSLOPE at ({st[0]}, {st[1]})')
                for c, st in zip(_POND_COLORS, _POND_STATIONS)]
               + [Line2D([], [], marker='o', color=c, ls='none', mfc='white', mew=1.2,
                         ms=6, label=f'SEEP/W at ({st[0]}, {st[1]})')
                  for c, st in zip(_POND_COLORS, _POND_STATIONS)])
    _legend_below(fig, handles, ncol=4, title='station (x, y)')
    fig.savefig(os.path.join(OUT, 'gs2_pond.png'), dpi=150)
    plt.close(fig)
    return 'gs2_pond.png'


# Only the two-dimensional sections get an inputs figure. The column problems
# (T01, T02, T05, T07) are one-dimensional: a section plot of a column is a
# needle, and their geometry and boundary conditions are stated in the text.
_INPUT_STEMS = (('gs2_rdd_inst', 'SEEPW-T03 — dam (both drawdown rates)'),
                ('gs2_pond', 'SEEPW-T04 — clay-lined pond'))


def fig_inputs():
    """One inputs figure per transient workbook: the section, its materials and
    the seepage boundary conditions the march is run under, framed on the
    domain like every other engine-section inputs plot."""
    from xslope.plot import plot_inputs
    names = []
    for stem, label in _INPUT_STEMS:
        path = os.path.join(SRC, f'{stem}.xlsx')
        if not os.path.exists(path):
            continue
        sd = load_slope_data(path)
        with contextlib.redirect_stdout(io.StringIO()):
            fig = plot_inputs(sd, mode='seep', frame='content', show_mesh=False,
                              title=f'{label}: inputs and seepage boundary conditions')
        name = f'{stem}_inputs.png'
        fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches='tight')
        plt.close(fig)
        names.append(name)
    return ', '.join(names)


if __name__ == '__main__':
    for fn in (fig_inputs, fig_cons, fig_infil, fig_rdd, fig_rdd_fs, fig_heap, fig_pond):
        print('ok  ', fn(), flush=True)
