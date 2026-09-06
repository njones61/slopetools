"""Builders for the Rocscience Slide2 Groundwater verification corpus
(docs/verification/rocscience_groundwater.md).  Steady-state problems (GW#1-13)
plus the first transient tier (GW#15, #16, #21), built on the uncoupled
transient seepage solver that shipped 2026-07 (run_transient_seepage).

Unlike the LEM corpus, these tags run the seepage solver live (run_tests.py
type=seep / seep_head / tseep_head mesh and solve per run), so the committed
artifact is the xlsx alone - no mesh/solution sidecars.

Run from the repo root:  python benchmarks/rocscience/build_groundwater.py
  ... build_groundwater.py --locks   # print the transient (tseep_head) test tags
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from xslope.fileio import load_slope_data as _load_slope_data  # noqa: E402
from xslope.fileio import save_slope_data_to_xlsx as _write_xlsx  # noqa: E402
from benchmarks._xlsx_writer import emit_water_mode  # noqa: E402
sys.path.insert(0, os.path.dirname(__file__))
from vendor_tcut import apply_vendor_t_cut  # noqa: E402


_SIGMA_KEYS = ('sigma_gamma', 'sigma_c', 'sigma_phi',
               'sigma_cp', 'sigma_d', 'sigma_psi')


def load_slope_data(path):
    """Load the geometry donor, clearing its elastic constants and its sigmas.

    These builders copy a material dict out of ACADS_1A for its shape and then set
    the seepage properties they actually care about. E and nu are not among them —
    a GW row is never solved for stress — so the donor's constants (RS2-1's vendor
    pair) are leftovers from a different problem. They are cleared at the door, which
    is also what the earliest GW files record: E is unset on the ones built before
    the donor happened to acquire a value.

    The donor's reliability standard deviations ride along the same way: ACADS_1A is
    also the design/reliability sample, and s(g)=1.2 / s(c)=1.8 / s(f)=2.744 describe
    the ACADS soil, not a groundwater problem's. No GW row is probabilistic, but a
    copied sigma would still offer a bogus one-click ±range, so it is cleared here.
    """
    sd = _load_slope_data(path)
    # The donor is RS2-1 and declares an isotropic at-rest initial stress
    # (main!D16, K0 = 1) that RS2 solved its SSR under. It belongs to that
    # problem alone, so it is cleared here rather than riding into files whose
    # own analysis is authored without one (benchmarks/tag_k0.py).
    sd['k0'] = None
    for m in sd.get('materials', []):
        m['E'] = 0.0
        m['nu'] = 0.0
        for k in _SIGMA_KEYS:
            m[k] = 0.0
    return sd


def save_slope_data_to_xlsx(slope_data, path):
    """Write a groundwater input file. No GW row carries a vendor tensile cap (they
    are seepage-only), but these builders copy the material dict out of ACADS_1A —
    which does carry one — so the cap is cleared on the way out.

    Water loads go out in v22's automatic form (emit_water_mode): these models
    state their pool as a seepage head boundary, and the engine derives the
    surface load from it. gw005 is the recorded exception and sets
    water_loads='manual' with its reason."""
    apply_vendor_t_cut(slope_data.get('materials', []), path)
    return _write_xlsx(emit_water_mode(slope_data, os.path.basename(path)), path)


OUT = os.path.join(os.path.dirname(__file__), '..', '..',
                   'docs', 'verification', 'files', 'rocscience_gw')
ACADS_1A = os.path.join(os.path.dirname(__file__), '..', '..',
                        'docs', 'lem', 'files', 'xslope_acads_simple.xlsx')


# ---------------------------------------------------------------------------
# THE TIME BASE OF EACH STEADY CASE
#
# Every model here carries a conductivity, and a conductivity is a length over a
# TIME, so each file declares the base its k is written in (the 'main' sheet's Time
# selector).  The base is read off the vendor model, per case, never inherited from
# a sibling: RS2 stores k in whatever base the model's own ``TimeUnit`` names, and
# the set is not uniform -- ``#019``/``#020`` are hours and ``#021`` is minutes, and
# their k values are the m/hr and m/min numbers to match (see the transient tiers
# below, which already declare theirs).
#
# For the STEADY tier the vendor is unanimous.  Every one of ``groundwater #001``
# through ``#013`` declares ``TimeUnit: second`` and ``metric permeability:
# "meters/second"`` in its own ``.fea``, and each builder's k is that model's own
# ``SK`` / conductivity-table value at face value in that base -- #002's 1e-05,
# #009_01's 6.67e-06, #010's 1.1574e-05, #011's 1e-07, #012's 1e-05, #013's 0.001,
# and the m/s fluxes the manual prints for #001 (2.5e-6), #007 (2.1e-4) and #008
# (4.4444e-5).  So all thirteen declare ``sec``.
#
# GW9 dam 1 is the case worth naming, because the page reports its discharge in
# m3/(min*m): that is a CONVERSION for comparison with Bowles, who works the dam in
# m/min.  The file's own conductivity is the vendor's 6.67e-6 m/s, and the locked
# flowrate 2.3069e-05 is the per-second number the page's 1.384e-3 is sixty times.
# Its declared base is therefore ``sec``, like every other steady case; labelling it
# per minute would put a unit on the figure that its own printed Q contradicts.
# ---------------------------------------------------------------------------


def _circle_through(p1, p2, yn):
    """The circle through ground points p1, p2 whose lowest point sits at
    elevation yn - the standing starting-circle rule (enter near the crest,
    tangent near the base of the governing zone, daylight near the toe) made
    constructive.  These groundwater decks never search or lock a factor of
    safety (every tag here is seep/seep_head/tseep_head, none of which read
    the circles sheet), but a shipped first circle still has to slice, so
    each caller below solves for one through two real points on its own
    ground/top boundary rather than carrying a generic placeholder.

    Returns {'Xo','Yo','Depth','R'}; raises if no such real circle exists
    (both points must sit above yn)."""
    (x1, y1), (x2, y2) = p1, p2
    A, B = y1 - yn, y2 - yn
    if A <= 0 or B <= 0:
        raise ValueError(f'_circle_through: p1/p2 must sit above yn={yn}: {p1} {p2}')
    a = B - A
    b = 2.0 * (A * x2 - B * x1)
    c = B * x1 * x1 - A * x2 * x2 - A * B * (y2 - y1)
    roots = []
    if abs(a) < 1e-14:
        if abs(b) > 1e-14:
            roots = [-c / b]
    else:
        disc = b * b - 4 * a * c
        if disc < 0:
            raise ValueError(f'_circle_through: no real circle for {p1} {p2} yn={yn}')
        sq = math.sqrt(disc)
        roots = [(-b + sq) / (2 * a), (-b - sq) / (2 * a)]
    lo, hi = min(x1, x2), max(x1, x2)
    best = None
    for Xo in roots:
        Yo = ((Xo - x1) ** 2 + y1 * y1 - yn * yn) / (2.0 * A)
        R = Yo - yn
        if R <= 0:
            continue
        pen = 0.0 if lo <= Xo <= hi else min(abs(Xo - lo), abs(Xo - hi))
        if best is None or pen < best[0]:
            best = (pen, {'Xo': Xo, 'Yo': Yo, 'Depth': yn, 'R': R})
    if best is None:
        raise ValueError(f'_circle_through: no admissible root for {p1} {p2} yn={yn}')
    return best[1]


def _base_sd(k1=1e-5, kr0=1e-3, h0=-0.4, time_unit=None):
    """Seepage-only base model: one material with u='seep'; the LEM circle is
    a placeholder (these problems are never solved for a factor of safety).

    ``time_unit`` is the TIME BASE the case's conductivities are expressed against,
    and every caller states it rather than inheriting a default: a conductivity is
    length/time, so an undeclared base leaves the k column and the solved flowrate
    as bare numbers in the figures, the Studio material table and the results CSV.
    It is passed per case and never guessed -- the block comment above carries the
    evidence each case's base rests on.
    """
    sd = load_slope_data(ACADS_1A)
    m = dict(sd['materials'][0])
    m.update(name='Soil', c=1.0, phi=30.0, gamma=20.0, gamma_sat=20.0,
             option='mc', u='seep', k1=k1, k2=k1, alpha=0.0, kr0=kr0, h0=h0)
    sd['materials'] = [m]
    sd['gamma_water'] = 9.81
    sd['time_unit'] = time_unit
    sd['dloads'] = []
    sd['piezo_line'] = []
    sd['circular'] = True
    sd['non_circ'] = []
    sd['circles'] = [{'Xo': 5.0, 'Yo': 10.0, 'Depth': 0.0, 'R': 10.0}]
    return sd


def gw001():
    """GW#1: shallow unconfined flow with rainfall (Haar 1990; Dupuit). Flow
    between two parallel rivers 10 m apart with a rainfall recharge on the land
    surface, the manual's first specified-flux problem after the flux BC landed.
    Domain 10 x 5 m (vendor RS2 groundwater #001_01: base y=0 impermeable, ground
    surface y=5); river heads h1=3.75 on the left edge (0,0)-(0,3.75) and h2=3.0
    on the right (10,0)-(10,3.0), exactly as the RS2 nodal 'total head' cards;
    uniform rainfall P=2.5e-6 m/s on the top ('vert infilt' 2.5e-6), k=1e-5 m/s.
    The whole recharge mounds an INTERNAL free surface between the rivers - there
    is no daylighting seepage face, so the top edge is declared BOTH the flux and
    an exit face: it stays inactive (dry, the mound crest el ~4.6 sits below the
    y=5 surface) but switches the solver onto the unsaturated free-surface path,
    which the internal mound needs. Targets (Table 1.1): the free-surface crest
    (x_a, h_max) - Slide 4.06 / 4.49, Haar eqs 1.2-1.3 3.98 / 4.25. xslope reads
    x_a~=4.1, h_max~=4.61 (a touch above Slide, the same free-surface-family bias
    the SEEP2D cross-check documents); Q=P*L=2.5e-5 m3/s per m is exact by
    construction. The free surface is k- and unsat-model independent (mass balance
    sets it); the flowrate lock plus a mound-guarding head regression are taken."""
    sd = _base_sd(k1=1e-5, time_unit='sec')
    from shapely.geometry import Polygon
    sd['profile_lines'] = []
    sd['polygons'] = [{'mat_id': 0, 'polygon': Polygon(
        [(0.0, 0.0), (10.0, 0.0), (10.0, 5.0), (0.0, 5.0)])}]
    sd['max_depth'] = None
    # First circle: enters/daylights on the flat top near the two ends of the
    # domain (1.0, 5.0) - (9.0, 5.0), tangent at el 1.5. Unused by the flowrate/
    # head locks (seep tags never read circles), but must slice per the standing
    # rule; the placeholder {5,10,0,10} did not.
    sd['circles'] = [_circle_through((1.0, 5.0), (9.0, 5.0), 1.5)]
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 3.75, 'coords': [(0.0, 0.0), (0.0, 3.75)]},
            {'head': 3.0, 'coords': [(10.0, 0.0), (10.0, 3.0)]},
        ],
        'specified_fluxes': [
            {'flux': 2.5e-6, 'coords': [(0.0, 5.0), (10.0, 5.0)]},
        ],
        # Same polyline as the flux: an internal recharge mound has no daylight
        # face, so the top doubles as an (inactive) exit face to select the
        # unsaturated solver. It never activates - the mound crest is below y=5.
        'exit_face': [(0.0, 5.0), (10.0, 5.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw001.xlsx'))
    return 'gw001.xlsx'


def gw007():
    """GW#7: seepage within a layered slope (Rulon & Freeze sandbox, after
    Fredlund & Rahardjo 1993). A medium-sand slope with a thin fine-sand lens;
    the fine sand's ks (5.5e-5 m/s) is BELOW the applied rainfall (2.1e-4 m/s),
    so recharge perches on the lens and daylights as a seepage face - the classic
    perched-water-table result. Geometry from vendor RS2 groundwater #007 (a 2.4 x
    1.0 m box, 2:1 downstream slope from crest (1.6,1.0) to toe (0,0.2)); the fine
    lens is the y=0.6-0.7 band from the slope face to the right wall. Conductivity
    functions are the RS2 'Custom' curves (Fig 7.2), fit by Mualem-vG here: medium
    ks=0.0014 (vg_a=1.774, vg_n=2.328), fine ks=5.5e-5 (vg_a=1.672, vg_n=2.197).
    BCs from the RS2 cards: rainfall 2.1e-4 'vert infilt' on the crest top
    (1.6-2.4, y=1.0); tailwater 'total head' 0.3 on the submerged toe (0,0.2)-
    (0.2,0.3); the rest of the slope an exit (seepage) face; base and right wall
    no-flow. All published targets are chart curves (Fig 7.4 water table, 7.7/7.8
    head profiles) with no tabulated value, so - as the methodology note allows for
    GW6/GW7 - only the flowrate is locked (Q=q*L=1.68e-4, exact by construction),
    with a head regression guarding the field. xslope reproduces the stated water
    table (daylights at el 0.30 at the toe) and the perched zone above the lens."""
    sd = _base_sd(time_unit='sec')
    med = dict(sd['materials'][0])
    med.update(name='Medium sand', k1=0.0014, k2=0.0014, alpha=0.0,
               kr0=1e-3, h0=-0.4, unsat='vg', vg_a=1.7745, vg_n=2.3276)
    fin = dict(med)
    fin.update(name='Fine sand', k1=5.5e-5, k2=5.5e-5,
               unsat='vg', vg_a=1.6722, vg_n=2.1965)
    sd['materials'] = [med, fin]                # mat 0 = medium, mat 1 = fine lens
    from shapely.geometry import Polygon
    sd['profile_lines'] = []
    sd['polygons'] = [
        {'mat_id': 0, 'polygon': Polygon(
            [(0.0, 0.0), (2.4, 0.0), (2.4, 0.6), (0.8, 0.6), (0.0, 0.2)])},
        {'mat_id': 1, 'polygon': Polygon(
            [(0.8, 0.6), (2.4, 0.6), (2.4, 0.7), (1.0, 0.7)])},
        {'mat_id': 0, 'polygon': Polygon(
            [(1.0, 0.7), (2.4, 0.7), (2.4, 1.0), (1.6, 1.0)])},
    ]
    sd['max_depth'] = None
    # First circle: enters on the toe slope (0.24, 0.32) and daylights on the
    # crest (2.16, 1.0), tangent at el 0.096 near the base of the fine lens.
    sd['circles'] = [_circle_through((0.24, 0.32), (2.16, 1.0), 0.096)]
    sd['seepage_bc'] = {
        'specified_heads': [{'head': 0.3, 'coords': [(0.0, 0.2), (0.2, 0.3)]}],
        'specified_fluxes': [{'flux': 2.1e-4, 'coords': [(1.6, 1.0), (2.4, 1.0)]}],
        'exit_face': [(0.2, 0.3), (0.8, 0.6), (1.0, 0.7), (1.6, 1.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw007.xlsx'))
    return 'gw007.xlsx'


def gw002():
    """GW#2: confined potential flow around a cylinder (Streeter analytical;
    Desai & Kundu FE). Half-domain 8 x 4 m with a 24-segment semicircular
    notch (r=1 at (4,0)); heads 1.0 / 0.0 on the left/right edges (Fig 2.2,
    all dimensions printed); fully saturated -> confined solve. Targets:
    heads at the 5 printed points - xslope matches Slide within 0.0013 m
    everywhere and the closed form within its own idealization error.
    Homogeneous confined flow: the head field is k-independent."""
    sd = _base_sd(time_unit='sec')
    from shapely.geometry import Polygon
    arc = [(4.0 - math.cos(t), math.sin(t))
           for t in [math.pi * i / 24 for i in range(25)]]
    coords = ([(0.0, 0.0), (3.0, 0.0)] + arc[1:-1] + [(5.0, 0.0), (8.0, 0.0)])
    sd['profile_lines'] = []
    sd['polygons'] = [{'mat_id': 0,
                       'polygon': Polygon(coords + [(8.0, 4.0), (0.0, 4.0)])}]
    sd['max_depth'] = None
    # First circle: flat-top entry/daylight points (0.8, 4.0) - (7.2, 4.0),
    # tangent at el 1.2.
    sd['circles'] = [_circle_through((0.8, 4.0), (7.2, 4.0), 1.2)]
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 1.0, 'coords': [(0.0, 0.0), (0.0, 4.0)]},
            {'head': 0.0, 'coords': [(8.0, 0.0), (8.0, 4.0)]},
        ],
        'exit_face': [],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw002.xlsx'))
    return 'gw002.xlsx'


def gw003():
    """GW#3: confined flow under a dam foundation (Rushton & Redshaw). Soil
    block 40 x 10 m; head 5 on the ground x 0-8, head 0 on x 20-40, dam base
    x 8-20 impervious (no BC). Targets: head profiles along line 1-1 (y=-4)
    and line 2-2 (x=20) from Fig 3.5/3.6 - xslope within 0.08 m of the
    chart (Slide's markers coincide with Rushton & Redshaw's).

    k = 1e-7 m/s, the vendor model's own SK (#003.slw). The problem is confined
    and homogeneous, so the published head-profile targets are k-independent;
    only the self-locked flowrate scales with it."""
    sd = _base_sd(k1=1e-7, time_unit='sec')
    from shapely.geometry import Polygon
    sd['profile_lines'] = []
    sd['polygons'] = [{'mat_id': 0, 'polygon': Polygon(
        [(0.0, -10.0), (40.0, -10.0), (40.0, 0.0), (0.0, 0.0)])}]
    sd['max_depth'] = None
    # First circle: entry/daylight on the top edge (4.0, 0.0) - (36.0, 0.0),
    # tangent at el -7.0 near the base of the 10 m block.
    sd['circles'] = [_circle_through((4.0, 0.0), (36.0, 0.0), -7.0)]
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 5.0, 'coords': [(0.0, 0.0), (8.0, 0.0)]},
            {'head': 0.0, 'coords': [(20.0, 0.0), (40.0, 0.0)]},
        ],
        'exit_face': [],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw003.xlsx'))
    return 'gw003.xlsx'


def gw004():
    """GW#4: steady unconfined flow through an earth dam with a TRAPEZOIDAL
    toe drain (Kozeny basic parabola).

    Geometry is read off the vendor model ``groundwater #004.fez`` - the
    Slide model converted to RS2 - whose mesh boundary polygon is
    (0,0)-(10,5)-(12.5,5)-(23.4857,1.5016)-(21.9,0).  The dam is NOT closed
    by a vertical face: its downstream slope runs past the printed dimension
    chain to (23.4857, 1.5016) and then falls back down-left on the drain's
    inclined contact face to the toe at (21.9, 0).  Fig 4.1 shows the
    trapezoidal drain that face bounds, Fig 4.2's right-hand end shows the
    face itself carrying the seepage-face markers, and the printed
    10.00 + 2.50 + 9.50 = 22.00 chain measures to the BASE TOE, not to the
    rightmost point of the downstream slope.

    Boundary conditions likewise from the vendor file: total head 4 on the
    submerged upstream face (its nodal cards span x 0..8.019, y 0..4.009);
    a potential seepage face over the dry upstream face, the crest, the
    downstream slope AND the drain contact; and one node pinned to total
    head 0 at the drain toe (21.900, 0.000).  ks = 1e-7 m/s from the
    vendor's ``groundwater_material_properties`` (the free-surface shape is
    k-independent, so ks sets the flowrate lock only).

    The unsaturated law is an ASSUMPTION, not a transcription: the vendor
    material carries ``gw_mode 0 / stype General``, RS2's built-in Simple
    curve, whose parameters the file does not store.  A linear front with
    kr0 = 1e-3 at 0.25 m of suction stands in for it.

    Targets (Table 4.1): y1, the free-surface height directly above the
    drain toe, and x1, the horizontal offset from that toe to where the free
    surface meets the drain face.  RS2 publishes its own solve of THIS file
    (0.395 / 0.226), Slide publishes 0.442 / 0.227 for the same model, and
    Eq 4.1-4.2 give 0.4863 / 0.2431 for d = 16.2869 (Casagrande entry
    correction on the vendor's m = 8.0187, h = 4.0094, focus x = 21.900).
    The quantity is corner-singular - the free surface is nearly vertical
    where it enters the drain - so it needs a fine mesh: y1 reads 0.346 /
    0.377 / 0.394 / 0.401 / 0.404 / 0.407 at target_size 0.25 / 0.147 /
    0.09 / 0.06 / 0.045 / 0.03, and the tags run at 0.06."""
    from shapely.geometry import Polygon
    sd = _base_sd(k1=1e-7, h0=-0.25, time_unit='sec')
    sd['profile_lines'] = []
    sd['polygons'] = [{'mat_id': 0, 'polygon': Polygon(
        [(0.0, 0.0), (10.0, 5.0), (12.5, 5.0),
         (23.4857, 1.5016), (21.9, 0.0)])}]
    sd['max_depth'] = None
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 4.0, 'coords': [(0.0, 0.0), (8.0, 4.0)]},
            # the vendor's single head-0 node at the drain toe
            {'head': 0.0, 'coords': [(21.9, 0.0), (21.9, 0.0)]},
        ],
        'exit_face': [(8.0, 4.0), (10.0, 5.0), (12.5, 5.0),
                      (23.4857, 1.5016), (21.9, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw004.xlsx'))
    return 'gw004.xlsx'


def gw005():
    """GW#5: flow behind an embankment (after the FLAC manual, Coetzee et al.
    1995), the manual's two-material permeability-contrast problem.  Geometry,
    materials and boundary cards are read verbatim from the vendor RS2 model
    (``groundwater #005.fez``, linked from the manual's own section 5.5), so
    nothing here is digitized: external boundary (0,0)-(30,0)-(40,0)-(40,2)-
    (30,2)-(30,10)-(0,10)-(0,0) — a 30 x 10 m block with a 2 m downstream shelf
    out to x=40 — and two internal material boundaries at y=6 and y=4 spanning
    x=0..30, i.e. a 2 m low-k lens through the block.  Saturated conductivities
    are the manual's printed pair (1e-10 m/s host, 1e-13 m/s lens, a 1000x
    contrast); total head 10 m on the whole left face and 4 m on the x=30 step
    face (y 2..4) plus the x=40 end (y 0..2); every other edge is no-flow, and
    the vendor sets no seepage face anywhere.

    Both vendor k(psi) functions are two-point CONSTANT curves (kr = 1 at
    psi = -1000 and at +1000), so despite the section title the vendor model is a
    constant-conductivity linear problem; kr0=1.0 reproduces that exactly and
    the unsaturated law never enters.  The lens is 1000x tighter than the host,
    so it isolates the upper block, which stagnates near total head 10 while the
    head below it falls linearly 10 -> 4 across the 30 m.

    Published target: Figure 5-4, a pressure-head contour plate carrying a
    numeric key (0 -> 10 m in ten 1 m bands) — chart-only, no tabulated value,
    the same situation the methodology note covers for GW6/GW7 — so xslope's own
    flowrate and total-head field are locked and the Fig 5-4 comparison is
    documented in the page.  Two independent checks: the flow is essentially
    one-dimensional through the 4 m below the lens, so k*b*i = 1e-10*4*(6/30) =
    8.0e-11 m3/s per m, and xslope reads 8.19/8.17/8.14e-11 over a tri3 1.0 ->
    tri3 0.5 -> tri6 0.5 ladder (+1.8% at the finest, 0.6% spread); against the
    vendor, the solved pressure head lands inside Fig 5-4's own 1 m band at 46
    of 49 grid points, the three exceptions missing a band edge by 0.003, 0.008
    and 0.025 m.

    WATER LOADS STAY MANUAL — a recorded exception. Two pools at different levels
    (10 m upstream, 4 m on the shelf) meet at the vertical step face at x = 30, and
    a water surface is a function of position: it can hold one elevation at that
    station, not two, so the automatic derivation loads the whole step from the
    upstream level and floods the shelf. The derivation says so rather than doing it
    silently (water.derive_water_loads reports the face), and this model keeps its
    water loads typed in. No result is affected — the file's only locks are the
    seepage flowrate and head field, and seepage never reads a surface load."""
    from shapely.geometry import Polygon
    sd = _base_sd(k1=1e-10, time_unit='sec')
    host = sd['materials'][0]
    host.update(name='Material 1', k1=1e-10, k2=1e-10, alpha=0.0,
                kr0=1.0, h0=-0.4)          # kr0=1 -> the vendor's constant k(psi)
    lens = dict(host)
    lens.update(name='Material 2', k1=1e-13, k2=1e-13)
    sd['materials'] = [host, lens]
    sd['profile_lines'] = []
    sd['polygons'] = [
        {'mat_id': 0, 'polygon': Polygon([(0.0, 6.0), (30.0, 6.0),
                                          (30.0, 10.0), (0.0, 10.0)])},
        {'mat_id': 1, 'polygon': Polygon([(0.0, 4.0), (30.0, 4.0),
                                          (30.0, 6.0), (0.0, 6.0)])},
        {'mat_id': 0, 'polygon': Polygon([(0.0, 0.0), (40.0, 0.0), (40.0, 2.0),
                                          (30.0, 2.0), (30.0, 4.0), (0.0, 4.0)])},
    ]
    sd['max_depth'] = None
    # First circle: enters on the upper block's flat crest (4.0, 10.0) and
    # daylights on the shelf (36.0, 2.0), tangent at el 0.6 near the shelf.
    sd['circles'] = [_circle_through((4.0, 10.0), (36.0, 2.0), 0.6)]
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 10.0, 'coords': [(0.0, 0.0), (0.0, 10.0)]},
            {'head': 4.0, 'coords': [(30.0, 4.0), (30.0, 2.0)]},
            {'head': 4.0, 'coords': [(40.0, 2.0), (40.0, 0.0)]},
        ],
        'exit_face': [],
    }
    sd['water_loads'] = 'manual'      # the recorded exception; see the docstring
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw005.xlsx'))
    return 'gw005.xlsx'


def gw009a():
    """GW#9 dam 1: Bowles' homogeneous dam via Chapuis et al. (2001). Base
    100 m, crest 10 m at el 20 (upstream 2.5:1, downstream 2:1), reservoir
    head 18.5; ks = 6.67e-6 m/s with the manual's printed 8-point k-function
    fit by Mualem-van Genuchten (vg_a=0.2835, vg_n=2.765, log-space, max
    deviation ~1.5x mid-range). Q = 1.379e-3 m3/(min*m) vs Slide 1.378e-3,
    SEEP/W fine-mesh 1.37e-3, Bowles' flow nets 1.10-1.28e-3 (Bowles 1984,
    Example 9-2 / Fig E9-2a: direct 11.01e-4, flow-net 12.8e-4, k = 4e-4 m/min
    = 6.67e-6 m/s). Dam 2 (the toe-drain variant, Bowles Fig E9-2b) is
    gw009b()."""
    sd = _base_sd(k1=6.67e-6, time_unit='sec')
    m = sd['materials'][0]
    m.update(name='Dam fill', c=10.0, phi=30.0, kr0=0.0, h0=0.0,
             unsat='vg', vg_a=0.2835, vg_n=2.765)
    sd['profile_lines'] = [
        {'mat_id': 0, 'coords': [(0.0, 0.0), (50.0, 20.0), (60.0, 20.0),
                                 (100.0, 0.0)]},
    ]
    sd['max_depth'] = 0.0
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 18.5, 'coords': [(0.0, 0.0), (46.25, 18.5)]},
        ],
        'exit_face': [(60.0, 20.0), (100.0, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw009a.xlsx'))
    return 'gw009a.xlsx'


def gw009b():
    """GW#9 dam 2: Bowles' dam with a toe drain (Bowles 1984, Physical and
    Geotechnical Properties of Soils, 2nd ed., Example 9-2 / Fig E9-2b, p.248).
    40 m dam, 10 m crest, symmetric 2:1 faces (base 190 m, crest at el 45 per
    the Slide manual Fig 9.5 / Chapuis et al. 2001 Fig 5), reservoir head 40; a
    coarse toe drain fills the downstream-toe triangle (100,0)-(190,0)-
    (145,22.5). Body ks = 2e-7 m/s (Bowles prints k = 2e-5 cm/s on Fig E9-2b);
    drain ks = 1e-4 m/s; the body's unsaturated k(u) is the dam-1 Mualem-vG
    curve (vg_a=0.2835, vg_n=2.765).

    Q = 4.29e-6 m3/(s*m) vs Bowles' flow net 3.8e-6 (Fig E9-2b hand-check
    k*h*n_f/n_d = 2e-7 * 40 * 1.9/4) and Chapuis SEEP/W (2328 el) / Slide
    4.23e-6 - all three per SECOND per metre. Two published errata, resolved by
    the source: (1) the Chapuis Fig 5 caption's body k = 2.0e-6 m/s is a
    one-decade exponent slip (Bowles is 2e-7; the Slide Fig 9.6 chart draws
    ~2e-7); (2) the published Q, tabulated as m3/(min*m) beside dam 1, is
    m3/(s*m) in Bowles' own units line. The k=2e-6 caption over-reads Q by ~10x
    (linear in k); see the GW9 section."""
    from shapely.geometry import Polygon
    sd = _base_sd(k1=2e-7, time_unit='sec')
    body = sd['materials'][0]
    body.update(name='Dam fill', c=10.0, phi=30.0, k1=2e-7, k2=2e-7, alpha=0.0,
                kr0=0.0, h0=0.0, unsat='vg', vg_a=0.2835, vg_n=2.765)
    drain = dict(body)
    drain.update(name='Toe drain', k1=1e-4, k2=1e-4)
    sd['materials'] = [body, drain]                 # mat 0 = body, mat 1 = drain
    sd['profile_lines'] = []
    sd['polygons'] = [
        {'mat_id': 0, 'polygon': Polygon(
            [(0.0, 0.0), (90.0, 45.0), (100.0, 45.0), (145.0, 22.5),
             (100.0, 0.0)])},
        {'mat_id': 1, 'polygon': Polygon(
            [(100.0, 0.0), (145.0, 22.5), (190.0, 0.0)])},
    ]
    sd['max_depth'] = None
    sd['seepage_bc'] = {
        'specified_heads': [{'head': 40.0, 'coords': [(0.0, 0.0), (80.0, 40.0)]}],
        # toe drain daylights on the lower downstream slope; the whole
        # downstream face is the exit (seepage) face - flow concentrates in the
        # high-k drain, so the drain-only and full-slope faces give the same Q.
        'exit_face': [(100.0, 45.0), (145.0, 22.5), (190.0, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw009b.xlsx'))
    return 'gw009b.xlsx'


def gw010():
    """GW#10: Clement, Wise, Molz & Wen (1996) unconfined square domain with
    van Genuchten conductivity (vg_a=0.64, vg_n=4.65, ks=1.1574e-5 m/s):
    10 x 10 m block, head 10 on the left edge, tailwater 2 on the right,
    exit face above the tailwater, no-flow top and base. Q = 6.070e-5 vs
    Slide 6.066e-5 (+0.07%) / Clement 6.076e-5 (-0.1%); phreatic exit el
    4.87 vs Clement 4.8 / Slide 5.0 (the manual's "seepage face" column is
    the exit ELEVATION, not a face length). Only the tailwater-2 case has
    published numbers."""
    sd = _base_sd(time_unit='sec')
    sd['materials'][0].update(u='none', k1=1.1574e-5, k2=1.1574e-5, alpha=0.0,
                              unsat='vg', vg_a=0.64, vg_n=4.65,
                              kr0=0.001, h0=-1.0)
    sd['profile_lines'] = [{'mat_id': 0, 'coords': [(0.0, 10.0), (10.0, 10.0)]}]
    sd['max_depth'] = 0.0
    # First circle: flat-top entry/daylight (1.0, 10.0) - (9.0, 10.0),
    # tangent at el 7.0.
    sd['circles'] = [_circle_through((1.0, 10.0), (9.0, 10.0), 7.0)]
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 10.0, 'coords': [(0.0, 0.0), (0.0, 10.0)]},
            {'head': 2.0, 'coords': [(10.0, 0.0), (10.0, 2.0)]},
        ],
        'exit_face': [(10.0, 2.0), (10.0, 10.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw010.xlsx'))
    return 'gw010.xlsx'


def gw012():
    """GW#12: Vedernikov's trapezoidal ditch seeping into a deep drainage
    layer, half-model by symmetry: ground (0,40)-(15,40)-(25,50)-(100,50),
    head 50 on the ditch perimeter, head 0 on the base (the deep drain),
    symmetry/right edges no-flow. Q_half = 4.137e-4 vs Slide 4.093e-4
    (+1.1%) / Vedernikov k(B+AH)/2 = 4.0e-4 (+3.4%); flow-bulb half-width
    ~42 vs Slide 41 / theory 40. The detached bulb converges at
    max_iter=1500 (tag key), not the default 400."""
    sd = _base_sd(time_unit='sec')
    sd['materials'][0].update(u='none', k1=1e-5, k2=1e-5, alpha=0.0,
                              unsat='lf', kr0=0.001, h0=-1.0)
    sd['profile_lines'] = [{'mat_id': 0, 'coords': [(0.0, 40.0), (15.0, 40.0),
                                                    (25.0, 50.0), (100.0, 50.0)]}]
    sd['max_depth'] = 0.0
    # First circle: enters on the ditch bank (10.0, 40.0) and daylights on the
    # far flat (90.0, 50.0), tangent at el 12.0.
    sd['circles'] = [_circle_through((10.0, 40.0), (90.0, 50.0), 12.0)]
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 50.0, 'coords': [(0.0, 40.0), (15.0, 40.0), (25.0, 50.0)]},
            {'head': 0.0, 'coords': [(0.0, 0.0), (100.0, 0.0)]},
        ],
        'exit_face': [(25.0, 50.0), (100.0, 50.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw012.xlsx'))
    return 'gw012.xlsx'


def gw013():
    """GW#13: Vedernikov's triangular ditch into a deep drainage layer,
    half-model: apex (0,40) to (10,50), k=1e-3. Q_half = 2.087e-2 vs Slide
    2.050e-2 (+1.8%) / Vedernikov 2.0e-2 (+4.3%). max_iter=1500 as GW#12."""
    sd = _base_sd(time_unit='sec')
    sd['materials'][0].update(u='none', k1=1e-3, k2=1e-3, alpha=0.0,
                              unsat='lf', kr0=0.001, h0=-1.0)
    sd['profile_lines'] = [{'mat_id': 0, 'coords': [(0.0, 40.0), (10.0, 50.0),
                                                    (100.0, 50.0)]}]
    sd['max_depth'] = 0.0
    # First circle: flat-top entry/daylight (10.0, 50.0) - (90.0, 50.0),
    # tangent at el 15.0.
    sd['circles'] = [_circle_through((10.0, 50.0), (90.0, 50.0), 15.0)]
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 50.0, 'coords': [(0.0, 40.0), (10.0, 50.0)]},
            {'head': 0.0, 'coords': [(0.0, 0.0), (100.0, 0.0)]},
        ],
        'exit_face': [(10.0, 50.0), (100.0, 50.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw013.xlsx'))
    return 'gw013.xlsx'




def gw011():
    """GW#11 case 1: uniform earth/rock-fill dam with the Gardner
    kr = 1/(1 + a*psi^n) conductivity law, after Zhang, Xu & Chen (2001).
    Geometry from Fig 11.1 (p.45, printed dimensions): 45 m high, 17 m crest,
    upstream run 89.10 (1:1.98), downstream run 76.90 -> base 183.0 m. (The
    text's "1:1.171" downstream is a typo: 76.90/45 = 1.709, and the printed
    76.90 governs.) Reservoir at el 40 (upstream elevation head 40, downstream
    0); exit face on the whole downstream slope; impermeable base.
    Gardner a = 0.15, n = 6 exactly as printed on p.45. ks is not printed for
    the uniform dam and does not matter: the dam is homogeneous, so the free
    surface (the published target) is k-independent - 1e-7 m/s is the dam value
    from Table 11.1 (p.46) for the companion non-homogeneous case.
    Target: release point on the downstream face - Slide 19.397 m,
    ABAQUS/Zhang 19.64 m (p.46)."""
    sd = _base_sd(k1=1e-7, time_unit='sec')
    sd['materials'][0].update(name='Dam fill', kr0=0.0, h0=0.0,
                              unsat='gard', vg_a=0.15, vg_n=6.0)
    sd['profile_lines'] = [
        {'mat_id': 0, 'coords': [(0.0, 0.0), (89.10, 45.0), (106.10, 45.0),
                                 (183.0, 0.0)]},
    ]
    sd['max_depth'] = 0.0
    sd['seepage_bc'] = {
        'specified_heads': [
            {'head': 40.0, 'coords': [(0.0, 0.0), (79.20, 40.0)]},
        ],
        'exit_face': [(106.10, 45.0), (183.0, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw011.xlsx'))
    return 'gw011.xlsx'


# GW#6's conductivity function, shared by all five cases.
#
# The source is the vendor's own model file rather than the Fig 6.2 chart: every
# ``groundwater #006_0N.slw`` inside the RS2 Groundwater zip carries the custom
# function as a table, and case 1's is four points of pressure head (m) against
# conductivity (m/s) --
#
#     -15: 1e-11    -10: 1e-10    -1: 1e-07    -0: 1e-07
#
# so ks = 1e-7 m/s, air entry 1 m (9.81 kPa), then log-linear in suction: -1/3
# decade per metre to psi = 10 m, -1/5 decade per metre to psi = 15 m.  Case 2's
# table is the same shape scaled by 9, case 3's is the same function sampled at
# every metre (16 points) with its core 100x lower, and cases 4 and 5 repeat
# case 1's exactly.  Digitizing Fig 6.2 recovers the same curve to 0.007 decades
# rms, so the chart and the table agree; the table is used because it is exact.
#
# XSLOPE carries van Genuchten, Gardner and linear-front laws, not a table, so
# the function is fit.  These are the least-squares Mualem-vG parameters in
# log10(kr) over 0-8 m of suction -- the band the five solved fields occupy
# (their deepest suction is 6.7 m, on case 3) -- and they hold the table to
# 0.030 decades rms and 0.102 decades worst over that band.
_GW6_VG = dict(unsat='vg', vg_a=0.2452, vg_n=2.5739)


def gw006a():
    """GW#6 case 1: Fredlund & Rahardjo (1993) isotropic earth dam with a
    12 m horizontal drain (Fig 6.1: 12 m high, 4 m crest, symmetric 2:1
    faces, base 52 m; reservoir 10 m). Conductivity from the vendor table
    (see _GW6_VG): ks=1e-7 m/s, air entry 1 m, fit by Mualem-vG to 0.030
    decades rms over the suction band the solution occupies. Target:
    pressure head along line 1-1 (the crest centerline, x=26) from Fig 6.6,
    where Slide and F&R coincide. xslope reads +0.04 to +0.20 m above
    Slide's curve there, mesh- and fit-insensitive; locked at xslope's own
    values. Cases 2 (9:1 anisotropy), 3 (core), 4 (infiltration) and 5
    (seepage face) are gw006b/c/d/e."""
    sd = _base_sd(k1=1e-7, time_unit='sec')
    m = sd['materials'][0]
    m.update(name='Dam fill', c=10.0, phi=30.0, kr0=0.0, h0=0.0, **_GW6_VG)
    sd['profile_lines'] = [{'mat_id': 0, 'coords': [(0.0, 0.0), (24.0, 12.0),
                                                    (28.0, 12.0), (52.0, 0.0)]}]
    sd['max_depth'] = 0.0
    sd['seepage_bc'] = {
        'specified_heads': [{'head': 10.0, 'coords': [(0.0, 0.0), (20.0, 10.0)]}],
        'exit_face': [(40.0, 0.0), (52.0, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw006a.xlsx'))
    return 'gw006a.xlsx'


def gw006b():
    """GW#6 case 2: the case-1 dam made ANISOTROPIC — horizontal conductivity
    nine times the vertical. From the vendor RS2 model (groundwater #006_02.slw:
    ``condx: 1 condy: 0.111111`` with the saturated k-function scaled to 9e-7),
    the saturated conductivities are kh = 9e-7, kv = 1e-7 m/s (ratio 9), kangle 0.
    The unsaturated relative shape is identical to case 1 (the whole custom
    k-function is 9x case 1), so the case-1 Mualem-vG fit is reused. Same 12 m
    dam, 2:1 faces, 12 m toe drain, reservoir at 10 m.

    The extra horizontal conductivity spreads the flow and lowers the phreatic
    surface. Target: pressure head along line 1-1 (crest centerline x=26, Fig
    6.9). Here xslope reproduces the Slide/F&R curve almost exactly: pressure
    head 6.52 / 4.74 / 3.28 / 1.85 / 0.38 m at elevations 0 / 2 / 4 / 6 / 8 vs
    the chart's 6.5 / 4.7 / 3.2 / 1.85 / 0.4. Chart-only target (no tabulated
    value), so xslope's own flowrate and total-head field are locked."""
    sd = _base_sd(k1=9e-7, time_unit='sec')
    m = sd['materials'][0]
    m.update(name='Dam fill', c=10.0, phi=30.0, k1=9e-7, k2=1e-7, alpha=0.0,
             kr0=0.0, h0=0.0, **_GW6_VG)
    sd['profile_lines'] = [{'mat_id': 0, 'coords': [(0.0, 0.0), (24.0, 12.0),
                                                    (28.0, 12.0), (52.0, 0.0)]}]
    sd['max_depth'] = 0.0
    sd['seepage_bc'] = {
        'specified_heads': [{'head': 10.0, 'coords': [(0.0, 0.0), (20.0, 10.0)]}],
        'exit_face': [(40.0, 0.0), (52.0, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw006b.xlsx'))
    return 'gw006b.xlsx'


def gw006c():
    """GW#6 case 3: the case-1 dam with a low-permeability CORE plus the toe
    drain. From the vendor RS2 model (groundwater #006_03.slw + mesh material-2
    footprint) the core is a rectangular central block x in [24, 28] (the full
    crest width), y in [0, 10] (base up to 2 m below the crest), and its
    saturated k is 1e-9 m/s — exactly 100x lower than the 1e-7 shell, with the
    identical unsaturated relative shape (both custom functions are parallel).
    Same 12 m dam, 2:1 faces, 12 m toe drain, reservoir at 10 m.

    The domain is tiled by two non-overlapping polygons — one notched shell that
    wraps the core on three sides plus over its top, and the core rectangle
    itself — so the core is a true internal zone with no seam through the shell.
    (An earlier version cut the shell into three pieces around the core; the two
    extra seams were internal boundaries the mesher had to honour, dividing the
    shell for no physical reason.) The low-k core forces almost
    the entire hydraulic-head drop across its 4 m width (the crowded contours of
    Fig 6.13). Target: pressure head along line 1-1 (x=26, now inside the core,
    Fig 6.14). xslope reproduces the profile shape and sits at the high end of
    the published scatter, by up to +0.91 m at elevation 8 where the Slide and
    Ref[1] curves themselves diverge 0.9 m. This case reaches the deepest
    suction of the five (6.7 m), so it is the one the conductivity fit moves
    most. Chart-only target, so xslope's own flowrate and total-head field are
    locked. The vendor's case-3 table samples the same function as case 1 at
    every metre, and its core's is that function 100x lower, so both zones take
    the shared fit."""
    from shapely.geometry import Polygon
    sd = _base_sd(k1=1e-7, time_unit='sec')
    shell = sd['materials'][0]
    shell.update(name='Shell', c=10.0, phi=30.0, k1=1e-7, k2=1e-7, alpha=0.0,
                 kr0=0.0, h0=0.0, **_GW6_VG)
    core = dict(shell)
    core.update(name='Core', k1=1e-9, k2=1e-9)
    sd['materials'] = [shell, core]
    sd['profile_lines'] = []
    # The shell is the dam outline with the core's footprint notched out of its
    # base: along the base to the core's upstream face, up and over the core,
    # back down to the base, on to the downstream toe, then up the downstream
    # face, across the crest and down the upstream face.
    sd['polygons'] = [
        {'mat_id': 0, 'polygon': Polygon([(0.0, 0.0), (24.0, 0.0), (24.0, 10.0),
                                          (28.0, 10.0), (28.0, 0.0), (52.0, 0.0),
                                          (28.0, 12.0), (24.0, 12.0)])},
        {'mat_id': 1, 'polygon': Polygon([(24.0, 0.0), (28.0, 0.0),
                                          (28.0, 10.0), (24.0, 10.0)])},
    ]
    sd['max_depth'] = None
    sd['seepage_bc'] = {
        'specified_heads': [{'head': 10.0, 'coords': [(0.0, 0.0), (20.0, 10.0)]}],
        'exit_face': [(40.0, 0.0), (52.0, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw006c.xlsx'))
    return 'gw006c.xlsx'


def gw006e():
    """GW#6 case 5: the case-1 isotropic dam with a downstream SEEPAGE FACE
    instead of the horizontal toe drain — the "unknown boundary condition" that
    lets the phreatic surface daylight on the slope. From the vendor RS2 model
    (groundwater #006_05.slw) the seepage-face nodes cover the crest and the
    whole downstream face (22,11)->(50,1); there is no drain. Same 12 m dam,
    2:1 faces, reservoir at 10 m; isotropic k = 1e-7 (case-1 material).

    Without the drain the phreatic surface rides higher and exits on the
    downstream slope. Target: pressure head along line 1-1 (x=26, Fig 6.23).
    xslope reproduces the Slide/F&R curve almost exactly: pressure head 8.30 /
    6.35 / 4.41 / 2.45 / 0.50 m at elevations 0 / 2 / 4 / 6 / 8 vs the chart's
    8.4 / 6.4 / 4.5 / 2.5 / 0.55. Chart-only target, so xslope's own flowrate
    and total-head field are locked."""
    sd = _base_sd(k1=1e-7, time_unit='sec')
    m = sd['materials'][0]
    m.update(name='Dam fill', c=10.0, phi=30.0, k1=1e-7, k2=1e-7, alpha=0.0,
             kr0=0.0, h0=0.0, **_GW6_VG)
    sd['profile_lines'] = [{'mat_id': 0, 'coords': [(0.0, 0.0), (24.0, 12.0),
                                                    (28.0, 12.0), (52.0, 0.0)]}]
    sd['max_depth'] = 0.0
    sd['seepage_bc'] = {
        'specified_heads': [{'head': 10.0, 'coords': [(0.0, 0.0), (20.0, 10.0)]}],
        # no toe drain: the crest + whole downstream slope is the seepage face
        'exit_face': [(20.0, 10.0), (24.0, 12.0), (28.0, 12.0), (52.0, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw006e.xlsx'))
    return 'gw006e.xlsx'


def gw006d():
    """GW#6 case 4: the case-1 dam under steady-state INFILTRATION — rain
    falling on the exposed surface while the toe drain still runs. Same 12 m
    dam, 2:1 faces, 12 m toe drain, reservoir at 10 m, case-1 material.

    The vendor model (groundwater #006_04.slw) applies the infiltration as
    fourteen traction cards, each a VERTICAL flux of 1e-8 m/s, over the surface
    from (22, 11) up across the crest and down the downstream face to (50, 1) —
    one element short of the fixed-head node at each end. A vertical rain rate
    is not the same number as the normal flux XSLOPE's flux BC takes: on the
    2:1 faces the vendor's own cards carry qn = 1e-8 * cos(atan 0.5) = 8.9443e-9,
    and only across the horizontal crest is qn the full 1e-8. So the surface goes
    in as three blocks at the vendor's two rates, and the assembled inflow is the
    rain rate times the 28 m horizontal footprint, 2.800000e-7 m3/s per m, to
    seven figures. The face rate goes in exact rather than rounded — at
    8.94427191e-9 a two-figure 8.9e-9 would leave the boundary 0.6% light.

    The drain is XSLOPE's exit face, as on cases 1-3. The vendor writes it as a
    specified head of 0; in XSLOPE that would leave the model with no exit face
    at all, which selects the confined solver and drops the unsaturated law the
    problem is about.

    Target: pressure head along line 1-1 (x=26) from Fig 6.18, which prints
    Slide and Ref[1] markers at every metre of elevation. Infiltration lifts the
    profile 0.65 m above case 1 at the base and 1.33 m at the crest. xslope
    tracks the Slide markers to 0.19 m rms over the 13 stations, running above
    them by 0.18 m on average.
    Chart-only target, so xslope's own flowrate and total-head field are locked."""
    sd = _base_sd(k1=1e-7, time_unit='sec')
    m = sd['materials'][0]
    m.update(name='Dam fill', c=10.0, phi=30.0, k1=1e-7, k2=1e-7, alpha=0.0,
             kr0=0.0, h0=0.0, **_GW6_VG)
    sd['profile_lines'] = [{'mat_id': 0, 'coords': [(0.0, 0.0), (24.0, 12.0),
                                                    (28.0, 12.0), (52.0, 0.0)]}]
    sd['max_depth'] = 0.0
    q_vert = 1e-8                             # the vendor's rain rate
    q_face = q_vert * 2.0 / math.sqrt(5.0)    # its normal component on a 2:1 face
    sd['seepage_bc'] = {
        'specified_heads': [{'head': 10.0, 'coords': [(0.0, 0.0), (20.0, 10.0)]}],
        'specified_fluxes': [
            {'flux': q_face, 'coords': [(22.0, 11.0), (24.0, 12.0)]},
            {'flux': q_vert, 'coords': [(24.0, 12.0), (28.0, 12.0)]},
            {'flux': q_face, 'coords': [(28.0, 12.0), (50.0, 1.0)]},
        ],
        'exit_face': [(40.0, 0.0), (52.0, 0.0)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw006d.xlsx'))
    return 'gw006d.xlsx'


def gw008():
    """GW#8: flow through ditch-drained soils (Gureghian 1981), the corpus'
    first specified-flux (Neumann) problem. Fig 8.1 (p.34): half-drain
    spacing 1.0 m wide, 0.5 m deep to the impermeable base, two layers -
    Soil A is the LOWER 0.1 m (coarse) and Soil B the upper 0.4 m (fine).
    The water-free ditch is the left wall: exit face over its full height,
    so the invert node carries zero head when active (Slide draws the same
    thing as "seepage face" + "zero head" at the invert). Base and
    right-hand symmetry edge are no-flow, i.e. simply unspecified.

    MATERIAL AND FLUX VALUES COME FROM THE VENDOR MODEL, not from the
    printed tables, on two inputs where the two disagree:

    * Infiltration.  Both manuals' text prints 4.4e-6 m/s; the vendor model
      (``groundwater #008.fez``, 20 'vert infilt' edges over the whole top
      boundary) carries **4.4444e-5 m/s**.  The units of that card are fixed
      by two problems whose printed flux is not in dispute - #001_01 carries
      2.5e-6 (manual P = 2.5e-6 m/s) and #007 carries 2.1e-4 (manual
      2.1e-4 m/s) - so 'vert infilt' is the distributed flux in m/s.  The
      vendor value is also the clean one: 4.4444e-5 m/s = 0.16 m/hr and
      q/k_B = 0.400 exactly, where the printed value is clean in nothing.
      Decisive check: two-layer Dupuit at the symmetry divide gives a
      0.063 m mound from the printed flux and 0.240 m from the vendor's,
      and Figs 8.3/8.4 both draw the water table at ~0.25 m there.

    * Gardner a for Soil B.  Both manuals' Table 8.1 prints 2777.7; the
      vendor model carries **277.777**.  Discriminated on Fig 8.3's own
      labelled pressure-head contours (-0.10/-0.14/-0.17/-0.20 m, digitized
      at five stations): a = 277.777 reproduces all 14 station values to
      0.010 m rms / 0.019 m worst, while a = 2777.7 never gets below
      -0.16 m of suction, so it cannot draw the -0.17 or -0.20 contours the
      figure shows at all, and lands 0.030 m rms on the two it can.

    Saturated conductivities are likewise the vendor's exact 1.111111e-3
    (Soil A) and 1.111111e-4 m/s (Soil B) rather than the tables' rounded
    1.11e-3/1.11e-4; Soil A's Gardner pair (a = 1000, n = 4.5) and Soil B's
    n = 4.2 agree between print and model.

    Targets are chart-only (the manual prints no point value and no
    discharge): the Fig 8.3 pressure-head contours above the water table
    and the Fig 8.4 total-head contours plus its drawn water table."""
    sd = _base_sd(time_unit='sec')
    soil_b = dict(sd['materials'][0])
    soil_b.update(name='Soil B', k1=1.111111e-4, k2=1.111111e-4, alpha=0.0,
                  kr0=0.0, h0=0.0, unsat='gard', vg_a=277.777, vg_n=4.2)
    soil_a = dict(soil_b)
    soil_a.update(name='Soil A', k1=1.111111e-3, k2=1.111111e-3,
                  unsat='gard', vg_a=1000.0, vg_n=4.5)
    sd['materials'] = [soil_b, soil_a]          # mat 0 = upper, mat 1 = lower
    sd['profile_lines'] = [
        {'mat_id': 0, 'coords': [(0.0, 0.5), (1.0, 0.5)]},
        {'mat_id': 1, 'coords': [(0.0, 0.1), (1.0, 0.1)]},
    ]
    sd['max_depth'] = 0.0
    # First circle: this section is essentially flat (a 1 x 0.5 m ditch-drain
    # box, no slope) - the simplest circle that genuinely slices, flat-top
    # entry/daylight (0.1, 0.5) - (0.9, 0.5), tangent at el 0.15.
    sd['circles'] = [_circle_through((0.1, 0.5), (0.9, 0.5), 0.15)]
    sd['seepage_bc'] = {
        'specified_heads': [],
        'specified_fluxes': [
            {'flux': 4.4444e-5, 'coords': [(0.0, 0.5), (1.0, 0.5)]},
        ],
        'exit_face': [(0.0, 0.0), (0.0, 0.5)],
    }
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw008.xlsx'))
    return 'gw008.xlsx'


# ===========================================================================
# TRANSIENT TIER (GW#15, #16, #21) — the consolidation / transient-seepage
# problems, built on the uncoupled transient solver (run_transient_seepage,
# storage S = Ss = gamma_w*mv).  Each problem has a CLOSED-FORM (or recomputed
# series) target that the builder computes directly:
#   GW15  Terzaghi (1943) Eq 17.3, 1-D consolidation, single/double drainage
#   GW16  Pyrah (1996) two-layer consolidation (recomputed eigen-series)
#   GW21  Ferris (Tao & Xi 2006) erfc, transient flow in a confined aquifer
#
# All three are modelled as SATURATED columns/strips: the excess pore pressure
# (or aquifer head rise) is carried on a datum-offset total head H_REF so the
# pressure head stays positive everywhere and storage is Ss throughout (the
# variably-saturated solver then runs on the linear, saturated branch, which is
# exactly the diffusion equation dh/dt = (K/Ss) grad^2 h = cv grad^2 h).  The
# uniform non-steady initial condition is set with the repeated-time step-series
# idiom (value at t=0 -> the t=0 steady solve gives the uniform IC; the stepped
# value drives t>0), the same device the erfc acceptance lock uses — so no
# h_init tag key is needed and the tseep sheet alone carries the transient model.
# ===========================================================================

import numpy as np  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402

# GW15/16 share a datum offset that keeps the 1 m column saturated; GW21 uses its
# own (the aquifer is 5 ft thick).  The offset is physically inert (it cancels out
# of the excess head), it only selects the solver's saturated branch.
_H_REF = 100.0


def _tseep_base_sd(gamma_w, time_unit, unit_system='si'):
    """Seepage-only transient base: one placeholder material, no LEM circle used
    (these problems are never solved for a factor of safety).  Callers overwrite
    materials / polygons / seepage_bc / tseep."""
    sd = load_slope_data(ACADS_1A)
    sd['gamma_water'] = gamma_w
    sd['time_unit'] = time_unit
    sd['unit_system'] = unit_system
    sd['dloads'] = []
    sd['piezo_line'] = []
    sd['circular'] = True
    sd['non_circ'] = []
    sd['profile_lines'] = []
    sd['max_depth'] = None
    return sd


def _tseep_material(base_mat, name, k, ss, sy=0.1):
    m = dict(base_mat)
    m.update(name=name, c=1.0, phi=30.0, gamma=20.0, gamma_sat=20.0, option='mc',
             u='seep', k1=k, k2=k, alpha=0.0, kr0=1e-3, h0=-0.4, Ss=ss, Sy=sy)
    return m


# --- analytical targets -----------------------------------------------------

def terzaghi_ue(Z, Tv, nterms=500):
    """Terzaghi (1943) Eq 17.3 degree of dissipation ue/u0 at normalized depth Z
    (Z = z/H measured from a drained face; Z in [0,1] single drainage, [0,2]
    double) and time factor Tv = cv*t/H^2."""
    s = 0.0
    for m in range(nterms):
        M = (np.pi / 2.0) * (2 * m + 1)
        s += (2.0 / M) * np.sin(M * Z) * np.exp(-M * M * Tv)
    return s


def _pyrah_betas(kb, kt, nmax=400):
    """Spatial eigenvalues for two saturated layers of EQUAL thickness (0.5 each)
    with the SAME cv, drained top / impermeable bottom.  Continuity of head and of
    Darcy flux (k dZ/dz) at the interface reduces — because the two half-thicknesses
    are equal — to  kb*tan(beta/2)^2 = kt, i.e. tan(beta/2) = +/-sqrt(kt/kb)."""
    r = np.sqrt(kt / kb)
    a = np.arctan(r)
    betas = []
    for k in range(nmax):
        betas.append(2.0 * (a + k * np.pi))            # tan(beta/2) = +r
        betas.append(2.0 * ((np.pi - a) + k * np.pi))  # tan(beta/2) = -r
    return np.array(sorted(b for b in betas if b > 1e-9))


def pyrah_ue(y, t, kb, kt, mvb, mvt, betas=None, L=1.0, h1=0.5, u0=1.0):
    """Recomputed two-layer consolidation excess pore pressure ue(y,t) for a
    column with an impermeable base at y=0 and a drained top at y=L, interface at
    y=h1, both layers cv=1.  Bottom (y<h1) properties (kb,mvb); top (kt,mvt).
    Eigenfunctions Z(y): bottom A*cos(beta*y) with A=tan(beta*h1); top
    sin(beta*(L-y)).  Coefficients from the Ss-weighted (Ss=gamma_w*mv, gamma_w=1)
    projection of the uniform IC u0 — all integrals in closed form.  ue(y,t) =
    sum_n c_n Z_n(y) exp(-beta_n^2 t)."""
    if betas is None:
        betas = _pyrah_betas(kb, kt)
    y = np.asarray(y, dtype=float)
    ue = np.zeros_like(y)
    for b in betas:
        A = np.tan(b * h1)
        # closed-form integrals over the two layers (weight Ss = mv here)
        num = (mvb * u0 * A * np.sin(b * h1) / b
               + mvt * u0 * (1.0 - np.cos(b * (L - h1))) / b)
        den = (mvb * A * A * (h1 / 2.0 + np.sin(2 * b * h1) / (4 * b))
               + mvt * ((L - h1) / 2.0 - np.sin(2 * b * (L - h1)) / (4 * b)))
        cn = num / den
        Zy = np.where(y <= h1, A * np.cos(b * y), np.sin(b * (L - y)))
        ue = ue + cn * Zy * np.exp(-b * b * t)
    return ue


def ferris_dh(x, t, D, dH):
    """J.G. Ferris transient head rise in a semi-infinite confined aquifer
    (Tao & Xi 2006): dh(x,t) = dH*erfc( x / sqrt(4*D*t) ), D = T/S = k/(gamma_w*mv)."""
    from scipy.special import erfc
    return dH * erfc(np.asarray(x, dtype=float) / np.sqrt(4.0 * D * t))


# --- GW15: Terzaghi 1-D consolidation --------------------------------------

# k = cv*gamma_w*mv; the published target is dimensionless (ue/u0 vs Z at Tv), cv
# only sets the real-time scale.  Manual values: mv=0.01/kPa, gamma_w=9.81 ->
# Ss=0.0981/m, k=1e-5 m/s -> cv=k/Ss=1.019e-4 m2/s.
_GW15_MV = 0.01
_GW15_K = 1e-5
_GW15_U0 = 100.0
_GW15_SAVES = {'a': [250.0, 500.0, 1000.0], 'b': [1000.0, 2000.0, 4000.0]}


def _gw15_ss():
    return 9.81 * _GW15_MV


def _gw15_column(single_drainage):
    """Return (sd) for a 0.25 x 1.0 m saturated column, top always drained; the
    bottom drains too unless single_drainage (then it is impermeable = no BC)."""
    sd = _tseep_base_sd(gamma_w=9.81, time_unit='sec', unit_system='si')
    ss = _gw15_ss()
    sd['materials'] = [_tseep_material(sd['materials'][0], 'Soil', _GW15_K, ss)]
    sd['polygons'] = [{'mat_id': 0, 'polygon': Polygon(
        [(0.0, 0.0), (0.25, 0.0), (0.25, 1.0), (0.0, 1.0)])}]
    # First circle: this section is flat (a 0.25 x 1.0 m 1-D column, no
    # slope) - the simplest circle that genuinely slices, flat-top
    # entry/daylight (0.025, 1.0) - (0.225, 1.0), tangent at el 0.95.
    sd['circles'] = [_circle_through((0.025, 1.0), (0.225, 1.0), 0.95)]
    heads = [{'head': 'res', 'coords': [(0.0, 1.0), (0.25, 1.0)]}]  # top drain
    if not single_drainage:
        heads.append({'head': 'res', 'coords': [(0.0, 0.0), (0.25, 0.0)]})  # bottom
    sd['seepage_bc'] = {'specified_heads': heads, 'exit_face': []}
    return sd


def _gw15_tseep(saves):
    base = _H_REF + _GW15_U0
    dur = max(saves) * 1.001
    return {'times': [0.0, 0.0], 'series': {'res': [base, _H_REF]},
            'duration': dur, 'save_interval': None, 'stage_1': None,
            'stage_2': None, 'save_times': list(saves)}


def gw015a():
    """GW#15 case 1 (RS2 #17 Case 1): 1-D consolidation, DOUBLE drainage.  A 1 m
    saturated clay column (mv=0.01/kPa, k=1e-5 m/s -> cv=1.02e-4 m2/s) with a
    uniform initial excess pore pressure u0, draining at BOTH the top and the
    bottom (drainage path H=0.5 m).  Terzaghi Eq 17.3 (Fig 17-3) is the closed-form
    target.  Modelled saturated on a datum offset H_ref=100 m: the total head is
    held uniform at H_ref+u0 at t=0 (the t=0 steady solve sets the IC) and both
    faces step to H_ref for t>0, so the excess head h-H_ref = u0*ue/u0 follows
    Terzaghi with Z=2*(1-y) (double drainage)."""
    sd = _gw15_column(single_drainage=False)
    sd['tseep'] = _gw15_tseep(_GW15_SAVES['a'])
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw015a.xlsx'))
    return 'gw015a.xlsx'


def gw015b():
    """GW#15 case 2 (RS2 #17 Case 2): 1-D consolidation, SINGLE drainage.  Same
    column, draining at the top only with an impermeable base (drainage path
    H=1.0 m); Terzaghi Fig 17-5.  Z=1-y."""
    sd = _gw15_column(single_drainage=True)
    sd['tseep'] = _gw15_tseep(_GW15_SAVES['b'])
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw015b.xlsx'))
    return 'gw015b.xlsx'


# --- GW16: Pyrah two-layer consolidation -----------------------------------

# Table 18.1 (consistent units, gamma_w=1): Soil A k=1, mv=1 (cv=1); Soil B k=10,
# mv=10 (cv=1).  1 m column, x[0..0.5]; top drained, impermeable base; uniform IC
# u0=1000.  Both layers share cv=1, so the LAYERING (k/mv contrast at the
# interface), not a cv contrast, shapes the dissipation — Pyrah's (1996) point.
_GW16_U0 = 1000.0
_GW16_SAVES = [0.05, 0.2, 0.5]
_GW16_FRAC = 0.005          # small steps: two-layer interface error is temporal
# LAYER-ORDER CONVENTION: "A/B" is read upper/lower (A on top).  The eigen-series
# and the solver use the SAME assignment, so the lock is order-independent; only
# the match to Pyrah's Fig 18-3/4 depends on it — flagged in the docs.
_GW16_A = (1.0, 1.0)        # (k, mv)
_GW16_B = (10.0, 10.0)


def _gw16_base():
    sd = _tseep_base_sd(gamma_w=1.0, time_unit='sec', unit_system=None)
    # First circle: this section is flat (a 0.5 x 1.0 m 1-D column, no
    # slope) - the simplest circle that genuinely slices, flat-top
    # entry/daylight (0.05, 1.0) - (0.45, 1.0), tangent at el 0.85.
    sd['circles'] = [_circle_through((0.05, 1.0), (0.45, 1.0), 0.85)]
    sd['seepage_bc'] = {'specified_heads': [
        {'head': 'res', 'coords': [(0.0, 1.0), (0.5, 1.0)]}], 'exit_face': []}  # top drain
    base = _H_REF + _GW16_U0
    dur = max(_GW16_SAVES) * 1.001
    sd['tseep'] = {'times': [0.0, 0.0], 'series': {'res': [base, _H_REF]},
                   'duration': dur, 'save_interval': None, 'stage_1': None,
                   'stage_2': None, 'save_times': list(_GW16_SAVES)}
    return sd


def _box(y0, y1):
    return Polygon([(0.0, y0), (0.5, y0), (0.5, y1), (0.0, y1)])


def gw016a():
    """GW#16 case 1 (RS2 #18 Case 1): uniform Soil A (k=1, mv=1), single drainage.
    A one-material check that reduces to Terzaghi (Tv=t here, cv=1, H=1)."""
    sd = _gw16_base()
    m0 = sd['materials'][0]
    sd['materials'] = [_tseep_material(m0, 'Soil A', _GW16_A[0], _GW16_A[1])]
    sd['polygons'] = [{'mat_id': 0, 'polygon': _box(0.0, 1.0)}]
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw016a.xlsx'))
    return 'gw016a.xlsx'


def _gw16_layered(top, bottom, name_top, name_bottom, fname):
    sd = _gw16_base()
    m0 = sd['materials'][0]
    # mat 0 = bottom half [0,0.5]; mat 1 = top half [0.5,1]
    sd['materials'] = [
        _tseep_material(m0, name_bottom, bottom[0], bottom[1]),
        _tseep_material(m0, name_top, top[0], top[1])]
    sd['polygons'] = [
        {'mat_id': 0, 'polygon': _box(0.0, 0.5)},
        {'mat_id': 1, 'polygon': _box(0.5, 1.0)}]
    save_slope_data_to_xlsx(sd, os.path.join(OUT, fname))
    return fname


def gw016b():
    """GW#16 case 2 (RS2 #18 Case 2): two layers, Soil A over Soil B (A on top,
    the drained side; B below).  Recomputed two-layer eigen-series (Pyrah 1996,
    Fig 18-3) is the target."""
    return _gw16_layered(_GW16_A, _GW16_B, 'Soil A', 'Soil B', 'gw016b.xlsx')


def gw016c():
    """GW#16 case 3 (RS2 #18 Case 3): two layers, Soil B over Soil A (B on top,
    A below).  Pyrah Fig 18-4."""
    return _gw16_layered(_GW16_B, _GW16_A, 'Soil B', 'Soil A', 'gw016c.xlsx')


# --- GW21: Ferris confined aquifer -----------------------------------------

# 100 ft x 5 ft confined aquifer, fully saturated (imperial): k=4 ft/hr, mv=0.1,
# gamma_w=62.4 -> Ss=6.24/ft, D=T/S=k/Ss=0.641 ft2/hr.  Left face stepped +5 ft at
# t=0; results at 600 hr.  Case a IC=0, case b IC=5 ft.  Ferris erfc closed form.
_GW21_MV = 0.1
_GW21_K = 4.0
_GW21_GW = 62.4
_GW21_DH = 5.0
_GW21_T = 600.0


def _gw21_ss():
    return _GW21_GW * _GW21_MV


def _gw21_D():
    return _GW21_K / _gw21_ss()


def _gw21_build(ic_excess, fname):
    sd = _tseep_base_sd(gamma_w=_GW21_GW, time_unit='hr', unit_system='imperial')
    sd['materials'] = [_tseep_material(sd['materials'][0], 'Aquifer',
                                       _GW21_K, _gw21_ss())]
    sd['polygons'] = [{'mat_id': 0, 'polygon': Polygon(
        [(0.0, 0.0), (100.0, 0.0), (100.0, 5.0), (0.0, 5.0)])}]
    sd['circles'] = [{'Xo': 50.0, 'Yo': 10.0, 'Depth': 0.0, 'R': 10.0}]
    # left face is the only Dirichlet: series holds base at t=0 (uniform IC via the
    # t=0 steady solve) then steps +dH; the far/other boundaries are no-flow, which
    # matches the semi-infinite erfc far field at 600 hr (the front reaches ~40 ft).
    base = _H_REF + ic_excess
    sd['seepage_bc'] = {'specified_heads': [
        {'head': 'res', 'coords': [(0.0, 0.0), (0.0, 5.0)]}], 'exit_face': []}
    sd['tseep'] = {'times': [0.0, 0.0],
                   'series': {'res': [base, base + _GW21_DH]},
                   'duration': _GW21_T * 1.001, 'save_interval': None,
                   'stage_1': None, 'stage_2': None, 'save_times': [_GW21_T]}
    save_slope_data_to_xlsx(sd, os.path.join(OUT, fname))
    return fname


def gw021a():
    """GW#21 case 1 (RS2 #23 Case 1): transient flow in a fully confined aquifer,
    initial head 0.  The left boundary head is stepped up 5 ft at t=0; the head
    rise at 600 hr follows Ferris' erfc (Tao & Xi 2006)."""
    return _gw21_build(0.0, 'gw021a.xlsx')


def gw021b():
    """GW#21 case 2 (RS2 #23 Case 2): the same aquifer starting from a uniform 5 ft
    head (a prior steady state); the left boundary steps to 10 ft.  Ferris erfc
    about the 5 ft baseline (Fig 23-7)."""
    return _gw21_build(5.0, 'gw021b.xlsx')


# ===========================================================================
# DAM TRANSIENT TIER (GW#17, #18) — transient seepage through the Fredlund &
# Rahardjo (1993) earth-fill dam as the reservoir is quickly raised 4 m -> 10 m.
# Same 12 m dam as the steady GW#6 family (base 52 m, 4 m crest, symmetric 2:1
# faces, profile (0,0)-(24,12)-(28,12)-(52,0)), now with STORAGE (Ss = gamma_w*mv)
# and a moving reservoir face.  GW#18 has a free downstream seepage face (no
# drain); GW#17 adds a 12 m toe drain (a high-k strip held at total head 0).
#
# Unsaturated properties: each vendor model carries a "user defined groundwater
# function" with TWO independent tables - a conductivity curve k(suction) and a
# water-content curve theta(suction) - with suction in kPa and k in m/s.  They are
# transcribed separately, not derived from one another:
#
#   GW#18 (RS2 #020)   k: (0, 1e-7) (5, 1e-7) (100, 1e-10)   theta: (0, 0.7) (4000, 0.4)
#   GW#17 (RS2 #019)   k: (0, 1e-7) (15, 1e-7) (50, 5e-9)    theta: (0, 0.4) (100, 0.1)
#                         (100, 1e-10) (200, 1e-12)
#
# GW#18's retention curve spreads its 0.3 of water content over 4000 kPa - 408 m of
# head, a hundred times the scale of any van Genuchten fit to its conductivity curve
# - so its moisture capacity CANNOT be carried by the same (a, n) that carries kr.
# It is built on ``unsat='gard'`` instead, where XSLOPE takes kr from the Gardner
# power law and the drainage capacity from an independent linear band Sy/|h0|: a
# straight retention line over its own range is exactly what that band is, so
# Sy = 0.7 - 0.4 and h0 = -4000/gamma_w reproduce the vendor curve rather than fit
# it.  The Gardner fit to GW#18's own conductivity table is also the better of the
# two (0.120 vs 0.161 decades rms over 0-12 m of suction).
#
# GW#17's retention range is 100 kPa (10 m), the same order as its conductivity
# curve, so the van Genuchten capacity is close to the vendor's straight retention
# line rather than an order off it, and it keeps the vG model.  That was measured
# rather than assumed: rebuilding GW#17 on the ``gard`` split as well (S_y = 0.3
# over h0 = -10 m from its own (0, 0.4) -> (100, 0.1) water-content table, with a
# Gardner fit to its 5-point conductivity table) moves the 15 h h = 7 m front by
# less than 0.1 m and leaves the row's standing discrepancy where it is.
#
# The reservoir raise is the submerged-only Dirichlet reservoir series ('res' =
# 4 -> 10 stepped at t=0): the t=0 steady solve at reservoir 4 sets the initial
# condition, and every upstream node with y <= h(t) is held at h(t) while nodes
# above the water line become exit-face nodes.  tri3 mesh (the transient exit-face
# active set is tracked per corner; linear elements only).
#
# Units: both vendor models declare "metric permeability: meters/second" and
# "stage time units: hours", so a k printed in m/s is multiplied by 3600 ONCE to
# reach the m/hr the tseep schedule runs in.
# ===========================================================================

_DAM_KS_MHR = 1e-7 * 3600.0          # 3.6e-4 m/hr (vendor 1e-7 m/s, TimeUnit hour)
_DAM_PROFILE = [(0.0, 0.0), (24.0, 12.0), (28.0, 12.0), (52.0, 0.0)]


def _dam_res_series(saves, duration):
    """Reservoir head series: held at 4 m at t=0 (steady IC), stepped to 10 m for
    t>0 (the repeated-time step idiom).  ``saves`` are the transient report times."""
    return {'times': [0.0, 0.0], 'series': {'res': [4.0, 10.0]},
            'duration': duration, 'save_interval': None, 'stage_1': None,
            'stage_2': None, 'save_times': list(saves)}


def gw018():
    """GW#18 (RS2 #20): transient seepage through the earth-fill dam, NO drain.
    The reservoir is raised from 4 m to 10 m at t=0 and the phreatic surface rises
    through the 12 m dam, daylighting on the downstream (toe) slope (the free
    seepage face).  Storage Ss = gamma_w*mv = 9.81*0.002 = 0.01962 /m (the vendor
    model carries mv=0.002; the manual TEXT prints 0.003 -- the model value is used
    to reproduce RS2's own Fig 20.5 result).

    Both unsaturated curves come from '#020's user-defined groundwater function and
    neither is derived from the other (see the block comment above): Gardner
    a=0.040424, n=4.14868 fitted to its conductivity table, and the drainage band
    Sy = 0.7-0.4 = 0.3 over h0 = -4000/9.81 = -407.75 m reproducing its
    water-content table exactly.

    Target: total head sampled along the toe (downstream) slope at t=0.6 h (the
    early transient) and near-steady, compared with Ref[1] (Fredlund & Rahardjo)
    in Fig 20.5 -- a digitizable line profile.  Both frames are taken at the
    VENDOR's own stage times, 0.6 h and 19656 h."""
    sd = _tseep_base_sd(gamma_w=9.81, time_unit='hr', unit_system='si')
    m = _tseep_material(sd['materials'][0], 'Dam fill', _DAM_KS_MHR,
                        ss=9.81 * 0.002, sy=0.3)
    m.update(kr0=0.0, h0=-4000.0 / 9.81, unsat='gard',
             vg_a=0.040424, vg_n=4.14868)
    sd['materials'] = [m]
    sd['profile_lines'] = [{'mat_id': 0, 'coords': list(_DAM_PROFILE)}]
    sd['max_depth'] = 0.0
    sd['circles'] = [{'Xo': 26.0, 'Yo': 24.0, 'Depth': 0.0, 'R': 20.0}]
    sd['seepage_bc'] = {
        # upstream face: submerged-only reservoir series (4 -> 10 at t=0); nodes
        # above the water line auto-convert to exit-face nodes each step.
        'specified_heads': [{'head': 'res', 'kind': 'reservoir',
                             'coords': [(0.0, 0.0), (24.0, 12.0)]}],
        # crest + downstream slope: the free seepage (exit) face.
        'exit_face': [(24.0, 12.0), (28.0, 12.0), (52.0, 0.0)],
    }
    sd['tseep'] = _dam_res_series([0.6, 19656.0, 60000.0], 60000.0 * 1.001)
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw018.xlsx'))
    return 'gw018.xlsx'


def gw017():
    """GW#17 (RS2 #19): the same dam WITH a 12 m toe drain -- a 0.5 m deep, 12 m
    wide high-k strip under the downstream toe (x in [40,52], y in [-0.5,0]) held at
    total head 0 (the vendor's tx=0 drain nodes).  The drain draws the phreatic
    surface down so the downstream slope stays largely unsaturated; the flow
    concentrates into the drain.  Reservoir raised 4 m -> 10 m at t=0.  Storage
    Ss = gamma_w*mv = 10*0.003 = 0.03 /m (vendor '#019' fill mv=0.003, drain
    mv=0.002, pore_fluid_uw=10); Sy = 0.4-0.1 = 0.3 from its water-content table
    (0, 0.4) -> (100, 0.1).  Dam fill kr fit by Mualem-vG (vg_a=0.2324,
    vg_n=2.934) to its 5-point conductivity table; unlike GW#18 this model's
    retention range (100 kPa = 10 m) is the same order as its conductivity curve,
    so the vG moisture capacity is an adequate stand-in and the vG fit is twice as
    good as a Gardner one (0.055 vs 0.113 decades rms over 0-20 m of suction).
    The drain is a high-k strip at the vendor's SK = 0.01 m/s.

    Published targets are total-head + pressure-head CONTOURS at 15 hr and 16383 hr
    (Figs 19-4..19-7, vs FlexPDE + SEEP/W, Pentland et al. 2001) -- chart-only, no
    tabulated profile.  Both frames are taken at the VENDOR's own stage times, and
    XSLOPE's own solved heads at named points are locked as a regression guard."""
    sd = _tseep_base_sd(gamma_w=10.0, time_unit='hr', unit_system='si')
    fill = _tseep_material(sd['materials'][0], 'Dam fill', _DAM_KS_MHR,
                           ss=10.0 * 0.003, sy=0.3)
    fill.update(kr0=0.0, h0=0.0, unsat='vg', vg_a=0.2324, vg_n=2.934)
    drain = _tseep_material(sd['materials'][0], 'Toe drain', 0.01 * 3600.0,
                            ss=10.0 * 0.002, sy=0.3)
    drain.update(kr0=0.0, h0=0.0, unsat='vg', vg_a=0.2324, vg_n=2.934)
    sd['materials'] = [fill, drain]           # mat 0 = dam fill, mat 1 = toe drain
    sd['profile_lines'] = []
    sd['polygons'] = [
        {'mat_id': 0, 'polygon': Polygon(
            [(0.0, 0.0), (24.0, 12.0), (28.0, 12.0), (52.0, 0.0), (40.0, 0.0)])},
        {'mat_id': 1, 'polygon': Polygon(
            [(40.0, 0.0), (52.0, 0.0), (52.0, -0.5), (40.0, -0.5)])},
    ]
    sd['max_depth'] = None
    sd['circles'] = [{'Xo': 26.0, 'Yo': 24.0, 'Depth': 0.0, 'R': 20.0}]
    sd['seepage_bc'] = {
        'specified_heads': [
            # upstream reservoir series (submerged-only), 4 -> 10 at t=0
            {'head': 'res', 'kind': 'reservoir',
             'coords': [(0.0, 0.0), (24.0, 12.0)]},
            # toe drain outlet held at total head 0 (bottom + downstream edge)
            {'head': 0.0, 'coords': [(40.0, -0.5), (52.0, -0.5), (52.0, 0.0)]},
        ],
        # downstream slope is an (inactive, drain-drawn) seepage face
        'exit_face': [(24.0, 12.0), (28.0, 12.0), (52.0, 0.0)],
    }
    sd['tseep'] = _dam_res_series([15.0, 16383.0, 200000.0], 200000.0 * 1.001)
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw017.xlsx'))
    return 'gw017.xlsx'


# ===========================================================================
# LAGOON / LAYERED-SLOPE TRANSIENT TIER (GW#19, #20) — two more Fredlund &
# Rahardjo (1993) transient-seepage ports on the uncoupled solver.  GW#19 is a
# lined lagoon leaking into a two-layer aquifer as the pond is filled; GW#20 is
# the steady GW#7 Rulon & Freeze layered sandbox re-run transiently as rainfall
# switches on.  Both are chart-only targets (RS2 Figs 21.9 / 22.7 are digitizable
# line profiles + contours), so — as the GW#6/#7/#17 methodology note allows —
# XSLOPE's OWN solved heads are locked as a regression guard, with the published
# profile comparison reported beside them in the docs.
#
# Both are built on the GW#18 split (``unsat='gard'``): the vendor .slw carries a
# conductivity table k(psi) and a water-content table theta(psi) as INDEPENDENT
# curves, and the retention table in each of these two models is a straight line,
# which is exactly the linear drainage band Sy/|h0| that ``gard`` uses for the
# moisture capacity.  Reproducing it is what sets the transient timing: a van
# Genuchten capacity fitted to the CONDUCTIVITY curve instead concentrates the
# same Sy within ~1/alpha of saturation, which is where a perched mound builds,
# and the mound then fills several times too slowly (measured on GW#20: 0.155 m
# rms against RS2's 31 s query-line profile with the vG capacity, 0.012 m with
# the vendor's own retention line).
# ===========================================================================


def gw019():
    """GW#19 (RS2 #21): transient seepage BELOW A LAGOON.  A half-model (the lagoon
    centerline at x=0 is a no-flow symmetry plane), 19 m wide x 10 m deep, of a
    two-layer aquifer: a 1 m soil LINER across the top (y in [9,10], lower k) over
    9 m of SOIL (y in [0,9]).  A 2 m-wide lagoon (x in [0,2] at the surface y=10)
    is filled with 1 m of water at t=0 and leaks down through the liner.

    From the vendor RS2 model (groundwater #021 .slw): both materials m_v=0.002,
    porosity 0.7; soil Custom k(psi) k_s=6e-4 (down to 6e-6 by 10 m suction), liner
    k_s=3.54e-4 (same relative shape).  TimeUnit=minute, so k is m/min and the
    schedule is in minutes.  Storage S_s = gamma_w*m_v = 10*0.002 = 0.02 /m (the
    vendor model carries pore_fluid_uw=10), S_y = theta_s - theta_r = 0.7-0.5 = 0.2.

    Built on the GW#18 split (``unsat='gard'``, see the block comment above), which
    both vendor tables here support REPRODUCING rather than fitting:

      * conductivity -- the .slw table is three points in metres of head,
        kr(0)=1, kr(5 m)=0.1, kr(10 m)=0.01, identical in relative shape for the
        soil and the liner.  Gardner kr = 1/(1+a*psi^n) through the two non-trivial
        points is exact: n = ln(11)/ln(2) = 3.45943, a = 9/5^n = 0.034372.  (The
        Mualem-vG pair this replaces, vg_a=0.1734/vg_n=1.9124, was a fit -- it
        returns kr = 0.095 and 0.0128 at those two points.)
      * retention -- the .slw water-content table is TWO points in kPa,
        (0, 0.7) -> (100, 0.5), i.e. a straight line, which is exactly the linear
        drainage band Sy/|h0| that ``gard`` uses for capacity: Sy = 0.2 over
        h0 = -100/10 = -10 m.

    NOTE the two tables are written in DIFFERENT units in the .slw -- conductivity
    against head in metres, water content against pressure in kPa.  The sibling
    models make this unambiguous: '#020' and '#022' write conductivity abscissae of
    -10.1936799184506 / -0.509683995922528 / -3.05810397553517, which are 100 / 5 /
    30 kPa divided by their gamma_w = 9.81, while their water-content abscissae stay
    round (-4000, -100).  Here gamma_w = 10 exactly, so the converted conductivity
    heads come out round (-10, -5) and the distinction is easy to miss.  Both of
    this model's curves therefore span the SAME 10 m of head.

    The far field (right edge x=19, y in [0,5]) is held at total head 5 — the
    regional water table 5 m below the surface, which is also the initial condition:
    the t=0 steady solve at a lagoon head of 5 (equal to the far field) gives a
    uniform water table at el 5, then the lagoon steps to total head 11 (el 10 + 1 m
    ponded) for t>0 (the repeated-time step idiom, applied through the submerged-only
    series: at t=0 the lagoon nodes at y=10 sit above the head-5 water line and are
    inactive, at t>0 head 11 submerges and holds them).  The base, the centerline and
    the top away from the lagoon are no-flow.  Report times 73 / 416 / 792 / 11340 min
    (the vendor stage schedule).

    Published target: pressure head along the top boundary (Fig 21.9, vs Ref [1]
    Fredlund & Rahardjo) + pressure-head contours at the four times — chart-only, no
    tabulated value.  XSLOPE's own solved heads at interior stations are locked as a
    regression guard; the field reproduces the lagoon-leak mound spreading toward the
    far field."""
    sd = _tseep_base_sd(gamma_w=10.0, time_unit='min', unit_system='si')
    ss = 10.0 * 0.002
    _GARD = dict(kr0=0.0, h0=-10.0, unsat='gard', vg_a=0.034372, vg_n=3.45943)
    soil = _tseep_material(sd['materials'][0], 'Soil', 6.0e-4, ss=ss, sy=0.2)
    soil.update(**_GARD)
    liner = _tseep_material(sd['materials'][0], 'Liner', 3.54e-4, ss=ss, sy=0.2)
    liner.update(**_GARD)
    sd['materials'] = [soil, liner]              # mat 0 = soil, mat 1 = liner
    sd['profile_lines'] = []
    sd['polygons'] = [
        {'mat_id': 0, 'polygon': Polygon(
            [(0.0, 0.0), (19.0, 0.0), (19.0, 9.0), (0.0, 9.0)])},
        {'mat_id': 1, 'polygon': Polygon(
            [(0.0, 9.0), (19.0, 9.0), (19.0, 10.0), (0.0, 10.0)])},
    ]
    sd['max_depth'] = None
    # First circle: flat-top entry/daylight (1.9, 10.0) - (17.1, 10.0),
    # tangent at el 3.0 near the base of the 9 m soil layer.
    sd['circles'] = [_circle_through((1.9, 10.0), (17.1, 10.0), 3.0)]
    sd['seepage_bc'] = {
        'specified_heads': [
            # lagoon floor (x 0-2, y=10): ponded reservoir series, 5 -> 11 at t=0
            {'head': 'pond', 'kind': 'reservoir',
             'coords': [(0.0, 10.0), (2.0, 10.0)]},
            # far-field regional water table, right edge y in [0,5], total head 5
            {'head': 5.0, 'coords': [(19.0, 0.0), (19.0, 5.0)]},
        ],
        'exit_face': [],
    }
    dur = 11340.0 * 1.001
    sd['tseep'] = {'times': [0.0, 0.0], 'series': {'pond': [5.0, 11.0]},
                   'duration': dur, 'save_interval': None, 'stage_1': None,
                   'stage_2': None, 'save_times': [73.0, 416.0, 792.0, 11340.0]}
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw019.xlsx'))
    return 'gw019.xlsx'


def gw020():
    """GW#20 (RS2 #22): transient seepage in a LAYERED SLOPE — the steady GW#7
    Rulon & Freeze sandbox (2.4 x 1.0 m, a medium-sand slope with a thin fine-sand
    lens) re-run transiently as rainfall switches on at t=0.  Same geometry,
    materials and boundary layout as gw007(); the transient additions are storage
    (S_s = gamma_w*m_v) and a rainfall flux that is zero at t=0 and steps to the GW#7
    value 2.1e-4 m/s for t>0.

    The initial condition is the t=0 steady solve with NO infiltration: only the
    tailwater head 0.3 at the toe holds, so the water table sits at el 0.3 (0.1 m
    above the toe).  When rainfall (2.1e-4 m/s, above the fine sand's k_s=5.5e-5)
    switches on, water perches on the fine lens and the perched mound builds toward
    the GW#7 steady result.  Vendor stage schedule: report times 4.6 / 31 / 208 s
    (TimeUnit=second, k in m/s).

    Both unsaturated curves are transcribed from '#022's user-defined groundwater
    function, neither derived from the other (see the block comment above):

      * retention -- its water-content table is TWO points in kPa, (0, 0.7) ->
        (100, 0.5), a straight line, which is the linear drainage band ``gard``
        uses for capacity: S_y = 0.2 over h0 = -100/9.81 = -10.1937 m.  That band
        is 0.2/10.1937 = 0.01962 /m, and the elastic S_s = gamma_w*m_v =
        9.81*0.002 = 0.01962 /m matches it, so the capacity is the manual's own
        printed m_v = 0.002 /kPa on both sides of the phreatic surface.
      * conductivity -- its 4-point Custom table (abscissae in metres of head:
        -3.0581 / -1.3252 / -0.30581 / 0, i.e. 30 / 13 / 3 / 0 kPa) is fitted by
        Gardner kr = 1/(1 + a*psi^n): medium a=146.88069, n=4.45352, fine
        a=115.81091, n=4.18902.  Over the three tabulated points that fit is
        0.24 decades rms against 0.40 for the Mualem-vG pair GW#7 carries, and
        the two give the same steady field (0.003 vs 0.004 m rms against the
        Fig 22.7 208 s markers).

    Published target: total head along a query line (Fig 22.7, vs Ref [1]) +
    total-head contours at the three times — chart-only.  XSLOPE's own solved heads
    at interior stations (the developing perched zone) are locked as a regression
    guard, with the digitized Fig 22.7 comparison reported beside them."""
    sd = _tseep_base_sd(gamma_w=9.81, time_unit='sec', unit_system='si')
    ss = 9.81 * 0.002
    _H_RET = -100.0 / 9.81          # the water-content table's 100 kPa range
    med = _tseep_material(sd['materials'][0], 'Medium sand', 0.0014, ss=ss, sy=0.2)
    med.update(kr0=0.0, h0=_H_RET, unsat='gard', vg_a=146.88069, vg_n=4.45352)
    fin = _tseep_material(sd['materials'][0], 'Fine sand', 5.5e-5, ss=ss, sy=0.2)
    fin.update(kr0=0.0, h0=_H_RET, unsat='gard', vg_a=115.81091, vg_n=4.18902)
    sd['materials'] = [med, fin]                 # mat 0 = medium, mat 1 = fine lens
    sd['profile_lines'] = []
    sd['polygons'] = [
        {'mat_id': 0, 'polygon': Polygon(
            [(0.0, 0.0), (2.4, 0.0), (2.4, 0.6), (0.8, 0.6), (0.0, 0.2)])},
        {'mat_id': 1, 'polygon': Polygon(
            [(0.8, 0.6), (2.4, 0.6), (2.4, 0.7), (1.0, 0.7)])},
        {'mat_id': 0, 'polygon': Polygon(
            [(1.0, 0.7), (2.4, 0.7), (2.4, 1.0), (1.6, 1.0)])},
    ]
    sd['max_depth'] = None
    # Same slope face as gw007() (this is its transient re-run): entry on the
    # toe slope (0.24, 0.32), daylight on the crest (2.16, 1.0), tangent at
    # el 0.096 near the base of the fine lens.
    sd['circles'] = [_circle_through((0.24, 0.32), (2.16, 1.0), 0.096)]
    sd['seepage_bc'] = {
        'specified_heads': [{'head': 0.3, 'coords': [(0.0, 0.2), (0.2, 0.3)]}],
        # rainfall flux: 0 at t=0 (IC), stepped to 2.1e-4 for t>0 (series 'infil')
        'specified_fluxes': [{'flux': 'infil', 'coords': [(1.6, 1.0), (2.4, 1.0)]}],
        'exit_face': [(0.2, 0.3), (0.8, 0.6), (1.0, 0.7), (1.6, 1.0)],
    }
    dur = 208.0 * 1.001
    sd['tseep'] = {'times': [0.0, 0.0], 'series': {'infil': [0.0, 2.1e-4]},
                   'duration': dur, 'save_interval': None, 'stage_1': None,
                   'stage_2': None, 'save_times': [4.6, 31.0, 208.0]}
    save_slope_data_to_xlsx(sd, os.path.join(OUT, 'gw020.xlsx'))
    return 'gw020.xlsx'


# --- lock-value report (prints the docs test tags) -------------------------

def _print_locks():
    """Compute the ANALYTICAL lock values at the tag sample points and print the
    test-tag lines for the docs page.  The tags lock the closed-form values; the
    tolerance covers the demonstrated numerical (mesh + backward-Euler) error."""
    ss15 = _gw15_ss()
    cv15 = _GW15_K / ss15
    lines = []

    # GW15a double drainage (H=0.5), tags at t=500,1000; sample y=0.25,0.5,0.75
    for t in (500.0, 1000.0):
        Tv = cv15 * t / 0.25
        pts = []
        for y in (0.25, 0.5, 0.75):
            Z = 2.0 * (1.0 - y)
            h = _H_REF + _GW15_U0 * terzaghi_ue(Z, Tv)
            pts.append(f'0.125:{y}:{h:.3f}')
        lines.append(f'<!-- test: file=files/rocscience_gw/gw015a.xlsx, '
                     f'type=tseep_head, target_size=0.02, time={t:g}, '
                     f'points={";".join(pts)}, tolerance=0.6, benchmark=GW15a-t{t:g} -->')
    # GW15b single drainage (H=1.0), tags at t=2000,4000
    for t in (2000.0, 4000.0):
        Tv = cv15 * t / 1.0
        pts = []
        for y in (0.25, 0.5, 0.75):
            Z = 1.0 - y
            h = _H_REF + _GW15_U0 * terzaghi_ue(Z, Tv)
            pts.append(f'0.125:{y}:{h:.3f}')
        lines.append(f'<!-- test: file=files/rocscience_gw/gw015b.xlsx, '
                     f'type=tseep_head, target_size=0.02, time={t:g}, '
                     f'points={";".join(pts)}, tolerance=0.6, benchmark=GW15b-t{t:g} -->')

    # GW16a uniform (Terzaghi Tv=t), tags at t=0.2,0.5
    for t in (0.2, 0.5):
        pts = []
        for y in (0.25, 0.5, 0.75):
            h = _H_REF + _GW16_U0 * terzaghi_ue(1.0 - y, t)
            pts.append(f'0.25:{y}:{h:.3f}')
        lines.append(f'<!-- test: file=files/rocscience_gw/gw016a.xlsx, '
                     f'type=tseep_head, target_size=0.02, time={t:g}, '
                     f'max_head_change_frac={_GW16_FRAC:g}, points={";".join(pts)}, '
                     f'tolerance=4.0, benchmark=GW16a-t{t:g} -->')
    # GW16b A/B and GW16c B/A (top,bottom)
    for tag, top, bottom in (('b', _GW16_A, _GW16_B), ('c', _GW16_B, _GW16_A)):
        betas = _pyrah_betas(bottom[0], top[0])
        for t in (0.2, 0.5):
            pts = []
            for y in (0.25, 0.5, 0.75):
                ue = pyrah_ue(np.array([y]), t, bottom[0], top[0], bottom[1],
                              top[1], betas=betas, u0=_GW16_U0)[0]
                h = _H_REF + ue
                pts.append(f'0.25:{y}:{h:.3f}')
            lines.append(f'<!-- test: file=files/rocscience_gw/gw016{tag}.xlsx, '
                         f'type=tseep_head, target_size=0.02, time={t:g}, '
                         f'max_head_change_frac={_GW16_FRAC:g}, points={";".join(pts)}, '
                         f'tolerance=6.0, benchmark=GW16{tag}-t{t:g} -->')

    # GW21 Ferris at 600 hr; sample x=10,20,30,40,50 at mid-thickness y=2.5
    D = _gw21_D()
    for tag, ic in (('a', 0.0), ('b', 5.0)):
        pts = []
        for x in (10.0, 20.0, 30.0, 40.0, 50.0):
            h = _H_REF + ic + ferris_dh(x, _GW21_T, D, _GW21_DH)
            pts.append(f'{x:g}:2.5:{float(h):.3f}')
        lines.append(f'<!-- test: file=files/rocscience_gw/gw021{tag}.xlsx, '
                     f'type=tseep_head, target_size=0.8, time={_GW21_T:g}, '
                     f'points={";".join(pts)}, tolerance=0.05, benchmark=GW21{tag} -->')

    print('\n'.join(lines))


_TRANSIENT = (gw015a, gw015b, gw016a, gw016b, gw016c, gw021a, gw021b,
              gw017, gw018, gw019, gw020)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    import sys as _sys
    if '--locks' in _sys.argv:
        _print_locks()
    else:
        for fn in (gw001, gw002, gw003, gw004, gw005,
                   gw006a, gw006b, gw006c, gw006d, gw006e,
                   gw007, gw008, gw009a, gw009b, gw010, gw011, gw012, gw013,
                   *_TRANSIENT):
            print(fn())
