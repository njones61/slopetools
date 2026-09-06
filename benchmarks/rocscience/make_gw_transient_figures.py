"""Render the comparison figures for the transient Groundwater corpus in
docs/verification/rocscience_groundwater.md.

  gw015.png  Terzaghi 1-D consolidation — ue/u0 vs depth, double & single drainage
  gw016.png  Pyrah two-layer consolidation — ue/u0 vs depth, uniform / A-B / B-A
  gw017.png  toe-drain dam — XSLOPE's steady total-head field (a field render)
  gw018.png  earth-fill dam — toe-slope total head vs RS2 Fig 20.5
  gw019.png  lagoon — pressure head along the top boundary vs RS2 Fig 21.9
  gw020.png  layered slope — total head down the query line vs both Fig 22.7 series
  gw021.png  Ferris confined aquifer — head rise vs distance at 600 hr, two ICs

All but gw017 are LINE plots (a profile vs depth/distance/x), the native form of
the published figures, so the field-plot frame spec (equal aspect / colorbars)
does not apply.  Their legends follow one rule: every drawn series has an entry
naming its SOURCE and its time or case in the series' own color, and the legend
sits in reserved space under the axes, sized from its own rendered height
(``_legend_below``), so it never covers data.

The published sources are named as the manuals name them.  The closed-form rows
(GW15, GW16, GW21) compare against Terzaghi, a recomputed Pyrah series and Ferris'
erfc solution.  The vendor rows (GW18, GW19, GW20) compare against the RS2
groundwater manual's own figures, whose legends label RS2's solve "Phase 2" and
the published reference curve "Analytical" (Ref [1], Fredlund & Rahardjo 1993).

Run from the repo root:  python benchmarks/rocscience/make_gw_transient_figures.py
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

import build_groundwater as B

SRC = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'verification',
                   'files', 'rocscience_gw')
OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'verification', 'images')

_COLORS = ['#1f77b4', '#d62728', '#2ca02c', '#9467bd', '#ff7f0e']


def _legend_below(fig, handles, ncol, title=None, labels=None, top=1.0):
    """Put the legend in reserved space under the axes, never over the data.

    The reserve is measured from the legend's own rendered height, so a
    two-row legend and a four-row legend both clear the axes without a
    hand-tuned margin; the column count is capped so the legend never runs
    past the figure's width.  ``top`` leaves room for a suptitle.
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
        return _legend_below(fig, handles, max(1, ncol // 2), title, labels, top)
    fig.tight_layout(rect=(0, bb.height + 0.02, 1, top))
    return leg


def _line(color, label, ls='-', lw=1.8):
    return Line2D([], [], color=color, ls=ls, lw=lw, label=label)


def _marker(color, label, marker='s', ms=5):
    return Line2D([], [], marker=marker, color=color, ls='none', mfc='white',
                  mew=1.3, ms=ms, label=label)


def _solve(stem, target_size, frac=None):
    sd = load_slope_data(os.path.join(SRC, f'{stem}.xlsx'))
    ts = build_tseep_data(sd)
    mesh = build_mesh_from_polygons(get_material_polygons(sd), target_size, 'tri3')
    seep = build_seep_data(mesh, sd)
    kw = {'verbose': False}
    if frac is not None:
        kw['max_head_change_frac'] = frac
    with contextlib.redirect_stdout(io.StringIO()):
        sol = run_transient_seepage(seep, ts, **kw)
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


def fig_gw15():
    cv = B._GW15_K / B._gw15_ss()
    ys = np.linspace(0.02, 0.98, 200)
    ys_s = np.linspace(0.1, 0.9, 9)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.6), sharey=True)
    tvs = []
    for ax, (stem, H, saves, Zof, title) in zip(axes, [
            ('gw015a', 0.5, B._GW15_SAVES['a'], lambda y: 2 * (1 - y),
             'Case 1 — double drainage (H = 0.5 m),  t = 250 / 500 / 1000 s'),
            ('gw015b', 1.0, B._GW15_SAVES['b'], lambda y: 1 - y,
             'Case 2 — single drainage (H = 1.0 m),  t = 1000 / 2000 / 4000 s')]):
        nodes, sol = _solve(stem, 0.02)
        tvs = [cv * t / (H * H) for t in saves]     # the same triple for both cases
        for c, t, Tv in zip(_COLORS, saves, tvs):
            ax.plot(B.terzaghi_ue(Zof(ys), Tv), ys, '-', color=c, lw=1.6)
            h = np.asarray(sol['frames'][transient_frame_index(sol, t)]['head'])
            ue = np.array([(_sample(nodes, h, 0.125, y) - B._H_REF) / B._GW15_U0
                           for y in ys_s])
            ax.plot(ue, ys_s, 'o', color=c, ms=5, mfc='white', mew=1.3)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel('excess pore pressure  $u_e/u_0$')
        ax.grid(alpha=0.3)
        ax.set_xlim(-0.02, 1.02)
    axes[0].set_ylabel('elevation  y  (m)   [drained top at y = 1]')
    handles = []
    for c, Tv in zip(_COLORS, tvs):
        handles.append(_line(c, f'Terzaghi Eq 17.3, $T_v$ = {Tv:.2f}', lw=1.6))
        handles.append(_marker(c, f'XSLOPE, $T_v$ = {Tv:.2f}', marker='o'))
    fig.suptitle('GW15 — Terzaghi 1-D consolidation, closed form vs XSLOPE',
                 fontsize=11)
    _legend_below(fig, handles, ncol=3, top=0.94)
    fig.savefig(os.path.join(OUT, 'gw015.png'), dpi=150)
    plt.close(fig)
    return 'gw015.png'


def fig_gw16():
    ys = np.linspace(0.001, 0.999, 400)
    ys_s = np.linspace(0.08, 0.92, 11)
    saves = B._GW16_SAVES
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 5), sharey=True)
    specs = [
        ('gw016a', 'Case 1 — uniform Soil A', None),
        ('gw016b', 'Case 2 — A (top) / B (bottom)', (B._GW16_A, B._GW16_B)),
        ('gw016c', 'Case 3 — B (top) / A (bottom)', (B._GW16_B, B._GW16_A)),
    ]
    for ax, (stem, title, layers) in zip(axes, specs):
        nodes, sol = _solve(stem, 0.02, frac=B._GW16_FRAC)
        if layers is None:
            ana = lambda yy, t: B.terzaghi_ue(1 - yy, t)
        else:
            top, bottom = layers
            betas = B._pyrah_betas(bottom[0], top[0])
            ana = (lambda yy, t, top=top, bottom=bottom, betas=betas:
                   B.pyrah_ue(yy, t, bottom[0], top[0], bottom[1], top[1],
                              betas=betas, u0=1.0))
            ax.axhline(0.5, color='0.6', ls='--', lw=1)
        for c, t in zip(_COLORS, saves):
            ax.plot(ana(ys, t), ys, '-', color=c, lw=1.6)
            h = np.asarray(sol['frames'][transient_frame_index(sol, t)]['head'])
            ue = np.array([(_sample(nodes, h, 0.25, y) - B._H_REF) / B._GW16_U0
                           for y in ys_s])
            ax.plot(ue, ys_s, 'o', color=c, ms=5, mfc='white', mew=1.3)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel('excess pore pressure  $u_e/u_0$')
        ax.grid(alpha=0.3)
        ax.set_xlim(-0.02, 1.02)
    axes[0].set_ylabel('elevation  y  (m)   [drained top at y = 1]')
    handles = []
    for c, t in zip(_COLORS, saves):
        handles.append(_line(c, f'Series solution, t = {t:g}  ($c_v$ = 1)', lw=1.6))
        handles.append(_marker(c, f'XSLOPE, t = {t:g}', marker='o'))
    fig.suptitle('GW16 — Pyrah two-layer consolidation, recomputed series vs XSLOPE',
                 fontsize=11)
    _legend_below(fig, handles, ncol=3, top=0.94)
    fig.savefig(os.path.join(OUT, 'gw016.png'), dpi=150)
    plt.close(fig)
    return 'gw016.png'


def fig_gw21():
    D = B._gw21_D()
    xs = np.linspace(0, 100, 300)
    xs_s = np.array([10, 20, 30, 40, 50, 60, 70.])
    fig, ax = plt.subplots(figsize=(8, 5.4))
    cases = [('gw021a', 0.0, 'case 1 (IC = 0, step to 5 ft)'),
             ('gw021b', 5.0, 'case 2 (IC = 5 ft, step to 10 ft)')]
    for c, (stem, ic, lbl) in zip(_COLORS, cases):
        nodes, sol = _solve(stem, 0.8)
        ax.plot(xs, ic + B.ferris_dh(xs, B._GW21_T, D, B._GW21_DH), '-',
                color=c, lw=1.8)
        h = np.asarray(sol['frames'][transient_frame_index(sol, B._GW21_T)]['head'])
        hv = np.array([_sample(nodes, h, x, 2.5) - B._H_REF for x in xs_s])
        ax.plot(xs_s, hv, 'o', color=c, ms=6, mfc='white', mew=1.4)
    ax.set_xlabel('distance from stepped face,  x  (ft)')
    ax.set_ylabel('head above datum  (ft)')
    ax.set_title('GW21 — Ferris confined aquifer at t = 600 hr, erfc vs XSLOPE',
                 fontsize=11)
    ax.grid(alpha=0.3)
    handles = []
    for c, (_stem, _ic, lbl) in zip(_COLORS, cases):
        handles.append(_line(c, f'Ferris erfc, {lbl}'))
        handles.append(_marker(c, f'XSLOPE, {lbl}', marker='o', ms=6))
    _legend_below(fig, handles, ncol=2)
    fig.savefig(os.path.join(OUT, 'gw021.png'), dpi=150)
    plt.close(fig)
    return 'gw021.png'


# Digitized RS2 markers ("Phase 2" in the chart's own legend) from the RS2
# groundwater manual's Fig 20.5, total head along the downstream (toe) slope at the
# two published stage times.  Read at 500 dpi off the chart's own 2 m x / 1 m head
# gridlines, at every labelled x station.  The Slide2 manual publishes the same
# comparison as its Fig 18.5, with its own markers on the same curve.
_GW18_FIG205 = {
    0.6: ([28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48],
          [2.887, 2.775, 2.687, 2.560, 2.448, 2.323, 2.177, 2.047, 1.882,
           1.680, 1.406]),
    19656: ([28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48],
            [8.330, 8.001, 7.639, 7.238, 6.794, 6.286, 5.683, 4.970, 4.019,
             3.014, 2.009]),
}


# Digitized RS2 ("Phase 2") markers from the groundwater manual's Fig 21.9, pressure
# head along the top boundary at the four report times. Calibrated against two values
# the model fixes: the far-field markers read -5.000 (the initial water table, 5 m
# below the top boundary) and the lagoon markers +0.996 (the 1 m of ponded water), so
# the read-off is good to ~0.005 m. Entries missing at a time are markers hidden under
# a later-drawn series, not missing data.
_GW19_FIG219 = {
    73.0: ([3, 4, 5, 6], [-3.328, -5.098, -5.005, -4.998]),
    416.0: ([3, 4, 5, 6, 7, 8, 9],
            [-1.856, -3.225, -4.124, -4.770, -4.952, -4.984, -4.995]),
    792.0: ([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [-1.544, -2.685, -3.427, -4.039, -4.508, -4.751, -4.892, -4.963,
             -4.977, -4.984, -4.987, -4.991, -4.998, -4.999, -4.999, -4.998,
             -4.999]),
    11340.0: ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
              [0.996, 0.996, 0.996, -0.478, -1.072, -1.473, -1.786, -2.064,
               -2.308, -2.547, -2.763, -2.980, -3.183, -3.382, -3.574, -3.755,
               -3.925, -4.053, -4.136, -4.178]),
}

# The RS2 groundwater manual's Fig 22.7 carries TWO published series, named in its
# own legend: square markers "Phase 2" (RS2's own solve) and lines "Analytical"
# (Ref [1], Fredlund & Rahardjo 1993). Both are digitized here, total head down the
# manual's own query line (Fig 22.6: vertical, at x = 1.6, the crest break). The
# chart's depth axis is measured from the crest, so y = 1.0 - depth. Calibration
# check: the 4.6 s markers at the base read 0.302-0.305 against the model's initial
# total head of 0.300.
_GW20_FIG227_Y = [1.0, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50,
                  0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05, 0.00]
_GW20_FIG227 = {
    4.6: [0.3915, 0.3846, 0.3805, 0.3750, 0.3720, 0.3695, 0.3650, 0.3320, 0.3080,
          0.3060, 0.3060, 0.3050, 0.3050, 0.3050, 0.3030, 0.3031, 0.3030, 0.3030,
          0.3020, 0.3020, 0.3020],
    31.0: [0.6050, 0.5991, 0.5940, 0.5880, 0.5840, 0.5815, 0.5770, 0.4949, 0.4180,
           0.4150, 0.4120, 0.4090, 0.4080, 0.4050, 0.4040, 0.4025, 0.4025, 0.4010,
           0.3999, 0.4000, 0.4000],
    208.0: [0.8620, 0.8555, 0.8500, 0.8445, 0.8401, 0.8360, 0.8320, 0.7300, 0.6280,
            0.6240, 0.6210, 0.6170, 0.6149, 0.6120, 0.6100, 0.6102, 0.6060, 0.6060,
            0.6051, 0.6050, 0.6050],
}
_GW20_QUERY_X = 1.6                       # the manual's own query line (Fig 22.6)

# Fig 22.7's "Analytical" lines — Ref [1] (Fredlund & Rahardjo 1993) — at the same
# 21 stations, read at 400 dpi off the chart's own 0.1 m gridlines with the marker
# columns skipped so the line is not averaged with the markers drawn on it. The
# Slide2 manual reprints the same reference curves as its Fig 20.7.
_GW20_FIG227_REF1 = {
    4.6: [0.462, 0.423, 0.394, 0.379, 0.367, 0.359, 0.353, 0.322, 0.308, 0.308,
          0.308, 0.308, 0.307, 0.306, 0.306, 0.306, 0.306, 0.306, 0.306, 0.306,
          0.306],
    31.0: [0.652, 0.640, 0.639, 0.630, 0.629, 0.620, 0.607, 0.543, 0.482, 0.471,
           0.471, 0.471, 0.471, 0.470, 0.461, 0.459, 0.459, 0.459, 0.459, 0.459,
           0.459],
    208.0: [0.877, 0.877, 0.871, 0.868, 0.861, 0.859, 0.844, 0.754, 0.659, 0.641,
            0.640, 0.630, 0.628, 0.628, 0.628, 0.618, 0.617, 0.617, 0.617, 0.617,
            0.617],
}

# GW18's own steady frame (a third save time on gw018.xlsx): the toe-slope profile is
# within 0.003 m of it by 50000 h, and Fig 20.5's 19656 h curve is already steady.
_GW18_STEADY = 60000.0


def _toe_y(x):
    return 12.0 - (x - 28.0) / 2.0          # downstream 2:1 face, x in [28,52]


def fig_gw18():
    """Toe-slope total head vs x: XSLOPE (solid, dense sampling of the downstream
    face) against the digitized Fig 20.5 profile (markers), at the vendor's own two
    stage times, plus XSLOPE's own steady profile (dashed) — which both codes have
    essentially reached by 19656 h."""
    nodes, sol = _solve('gw018', 1.5, frac=0.25)
    xs = np.linspace(28.0, 52.0, 120)
    fig, ax = plt.subplots(figsize=(8.5, 5.8))
    handles = []
    for c, (t_solve, t_pub, lbl) in zip(_COLORS, [
            (0.6, 0.6, 't = 0.6 h'),
            (19656.0, 19656, 't = 19656 h')]):
        h = np.asarray(sol['frames'][transient_frame_index(sol, t_solve)]['head'])
        th = np.array([_sample(nodes, h, x, _toe_y(x)) for x in xs])
        ax.plot(xs, th, '-', color=c, lw=1.8)
        px, ph = _GW18_FIG205[t_pub]
        ax.plot(px, ph, 's', color=c, ms=5, mfc='white', mew=1.3)
        handles.append(_line(c, f'XSLOPE, {lbl}'))
        handles.append(_marker(c, f'RS2 Fig 20.5, {lbl}'))
    hs = np.asarray(sol['frames'][transient_frame_index(sol, _GW18_STEADY)]['head'])
    ax.plot(xs, np.array([_sample(nodes, hs, x, _toe_y(x)) for x in xs]), '--',
            color=_COLORS[2], lw=1.6)
    handles.append(_line(_COLORS[2], 'XSLOPE, steady (t = 60000 h)', ls='--', lw=1.6))
    ax.set_xlabel('x coordinate along toe slope  (m)')
    ax.set_ylabel('total head  (m)')
    ax.set_title('GW18 — toe-slope total head, XSLOPE against RS2 Fig 20.5',
                 fontsize=11)
    ax.set_xlim(25, 55)
    ax.set_ylim(0, 9)
    ax.grid(alpha=0.3)
    _legend_below(fig, handles, ncol=3)
    fig.savefig(os.path.join(OUT, 'gw018.png'), dpi=150)
    plt.close(fig)
    return 'gw018.png'


def fig_gw17():
    """XSLOPE's STEADY total-head field for the toe-drain dam, rendered
    through the package's own plot_seep_solution — the visual analog of the
    published Fig 19-5 total-head contours (reservoir 10 drawn down to the toe drain
    at head 0).

    The single field render in this transient panel, drawn with the final display
    conventions: the automatic two-line "Seepage Solution — t = 200000 hr" title rides
    (no manual override), the series-driven reservoir / toe-drain BC water levels are
    shown for the frame (show_bc_levels), and no flow lines are drawn (a transient
    storage-release frame has no flow net). Single frame → auto colour scale."""
    from xslope.plot_seep import plot_seep_solution
    sd = load_slope_data(os.path.join(SRC, 'gw017.xlsx'))
    ts = build_tseep_data(sd)
    mesh = build_mesh_from_polygons(get_material_polygons(sd), 1.0, 'tri3')
    seep = build_seep_data(mesh, sd)
    with contextlib.redirect_stdout(io.StringIO()):
        sol = run_transient_seepage(seep, ts, verbose=False, max_head_change_frac=0.25)
    fr = sol['frames'][transient_frame_index(sol, 200000.0)]
    frame_solution = {
        # 'time' rides so the title reads "Seepage Solution — t = 500 hr" (auto).
        'time': fr['time'],
        'head': np.asarray(fr['head']), 'u': np.asarray(fr['u']),
        # No stream function is stored for a transient frame (no flow net); this
        # figure draws flowlines=False anyway.
        'phi': None, 'flowrate': fr.get('inflow'),
        'inflow': fr.get('inflow'), 'outflow': fr.get('outflow'),
        'unconfined': True,
    }
    fig = plt.figure(figsize=(9.0, 4.0))
    with contextlib.redirect_stdout(io.StringIO()):
        plot_seep_solution(seep, frame_solution, fig=fig, show_title=True,
                           fill_contours=True, phreatic=True, flowlines=False,
                           show_bc_levels=True, mesh=False)
    fig.savefig(os.path.join(OUT, 'gw017.png'), dpi=150)
    plt.close(fig)
    return 'gw017.png'


def fig_gw19():
    """Pressure head along the top boundary (y = 10) vs x at the four report times:
    XSLOPE (lines) against the digitized Fig 21.9 RS2 markers (points). The
    lagoon-leak pressure mound spreads from the centerline (x = 0) toward the far
    field as the lined pond fills; the lagoon footprint (x in [0,2]) is shaded."""
    nodes, sol = _solve('gw019', 0.8, frac=0.25)
    times = [73.0, 416.0, 792.0, 11340.0]
    xs = np.linspace(0.0, 19.0, 160)
    fig, ax = plt.subplots(figsize=(8.5, 6.0))
    handles = []
    for c, t in zip(_COLORS, times):
        h = np.asarray(sol['frames'][transient_frame_index(sol, t)]['head'])
        ph = np.array([_sample(nodes, h, x, 10.0) - 10.0 for x in xs])
        ax.plot(xs, ph, '-', color=c, lw=1.8)
        px, pp = _GW19_FIG219[t]
        ax.plot(px, pp, 's', color=c, ms=4.5, mfc='white', mew=1.2)
        handles.append(_line(c, f'XSLOPE, t = {t:g} min'))
        handles.append(_marker(c, f'RS2 Fig 21.9, t = {t:g} min', ms=4.5))
    ax.axvspan(0.0, 2.0, color='0.85', zorder=0)
    ax.text(1.0, 0.9, 'lagoon', ha='center', va='top', fontsize=8,
            transform=ax.get_xaxis_transform())
    ax.set_xlabel('x along top boundary  (m)   [centerline at x = 0]')
    ax.set_ylabel('pressure head  (m)')
    ax.set_title('GW19 — pressure head along the top boundary, XSLOPE against '
                 'RS2 Fig 21.9', fontsize=10.5)
    ax.set_xlim(0, 19)
    ax.grid(alpha=0.3)
    _legend_below(fig, handles, ncol=4)
    fig.savefig(os.path.join(OUT, 'gw019.png'), dpi=150)
    plt.close(fig)
    return 'gw019.png'


def fig_gw20():
    """Total head down the manual's own query line (Fig 22.6: vertical at x = 1.6,
    the crest break) vs elevation at the three report times, against BOTH series
    Fig 22.7 publishes: RS2's own markers and the Ref [1] curve the manual compares
    itself with. As rainfall switches on the perched mound builds above the low-k
    fine lens (shaded, y in [0.6,0.7]) and the water table rises from its initial
    el 0.3. XSLOPE lies between the two published series at every frame."""
    nodes, sol = _solve('gw020', 0.04, frac=0.25)
    times = [4.6, 31.0, 208.0]
    ys = np.linspace(0.0, 1.0, 160)
    fig, ax = plt.subplots(figsize=(7.8, 6.4))
    handles = []
    for c, t in zip(_COLORS, times):
        h = np.asarray(sol['frames'][transient_frame_index(sol, t)]['head'])
        th = np.array([_sample(nodes, h, _GW20_QUERY_X, yy) for yy in ys])
        ax.plot(th, ys, '-', color=c, lw=1.8)
        ax.plot(_GW20_FIG227[t], _GW20_FIG227_Y, 's', color=c, ms=4.5,
                mfc='white', mew=1.2)
        ax.plot(_GW20_FIG227_REF1[t], _GW20_FIG227_Y, ':', color=c, lw=1.4)
        handles.append(_line(c, f'XSLOPE, t = {t:g} s'))
        handles.append(_marker(c, f'RS2 Fig 22.7, t = {t:g} s', ms=4.5))
        handles.append(_line(c, f'Ref [1] Fig 22.7, t = {t:g} s', ls=':', lw=1.4))
    ax.axhspan(0.6, 0.7, color='0.85', zorder=0)
    ax.text(0.02, 0.65, 'fine lens', ha='left', va='center', fontsize=8,
            transform=ax.get_yaxis_transform())
    ax.set_xlabel('total head  (m)')
    ax.set_ylabel('elevation  y  (m)   [query line at x = 1.6]')
    ax.set_title('GW20 — total head down the Fig 22.6 query line, XSLOPE against '
                 'both Fig 22.7 series', fontsize=10)
    ax.grid(alpha=0.3)
    _legend_below(fig, handles, ncol=3)
    fig.savefig(os.path.join(OUT, 'gw020.png'), dpi=150)
    plt.close(fig)
    return 'gw020.png'


if __name__ == '__main__':
    for fn in (fig_gw15, fig_gw16, fig_gw21, fig_gw18, fig_gw17, fig_gw19, fig_gw20):
        print('ok  ', fn(), flush=True)
