# Copyright 2025 Norman L. Jones
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from math import sin, cos, tan, radians, atan, atan2, degrees

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar, root_scalar, newton
from shapely.geometry import LineString, Point
from tabulate import tabulate

from .advanced import rapid_drawdown
from .hoekbrown import hb_tangent
from .preflight import method_surface_reason


#: The ways a method returns no answer on a surface, as the FIRST words of the
#: message it fails with. They are different facts about the model and are
#: reported as different facts: an assumption about the interslice forces gives a
#: system that on some surfaces has NO ADMISSIBLE ROOT — no iteration count and
#: no starting guess reaches an answer the method would accept — while a system
#: that does have one can still be missed by the iteration, and a root that is
#: found can still be refused on the state it implies.
#:
#: "ADMISSIBLE" carries weight here and the claim is scoped to it deliberately.
#: Spencer's equations are singular where a slice's m_alpha changes sign, and
#: outside that pole-free band roots commonly do exist — at interslice
#: inclinations that reverse a base normal. Those are not solutions anyone would
#: report (the solver refuses them on base tension when its scipy stage happens
#: to land on one), and saying a surface "admits no solution" full stop would be
#: false about them. See :func:`spencer`'s existence tests.
SPENCER_NO_ADMISSIBLE_SOLUTION = (
    "Spencer's parallel interslice force assumption admits no admissible "
    "solution on this surface")
SPENCER_NO_CONVERGENCE = ("Spencer's method did not converge within the maximum "
                          "number of iterations.")
SPENCER_INADMISSIBLE = ("Spencer's method: no admissible interslice inclination "
                        "and factor of safety on this surface")

#: Spencer's interslice inclination is bounded by the surface's own geometry
#: rather than by a fixed angle. Spencer (1973) and Duncan & Wright place the
#: interslice-force inclination between the inclination of the ground surface and
#: that of the slip surface, and the equations give that bound exactly: theta must
#: stay within a right angle of every slice base, less the friction the base
#: mobilizes, or that slice's m_alpha changes sign and its base normal reverses.
#: That is the pole-free band `safe_theta_bounds` computes, and it is Spencer's
#: form of the base factor `FE_MIN_BASE_FACTOR` keeps clear of zero for the
#: force-equilibrium closure.
#:
#: A FIXED cap was measured and does not hold: 45 degrees, the angle a real
#: section's geometry rarely passes, refuses the planar-surface benchmark whose
#: answer every other method confirms (VP43 / GS-2.26, 1.352 at theta = 49.6
#: degrees) and the wedge benchmark VP48 (0.991 at -56.1 degrees). Both sit
#: comfortably inside the band their own geometry allows, so the band is the
#: bound and no fixed angle is applied on top of it.

#: Morgenstern-Price's two, which are the same two facts under its own
#: assumption: no crossing of F_f and F_m anywhere in the lambda range it
#: searches is that method's no-admissible-root condition, and its admissibility
#: guard is the refusal of a solution it did find.
MPRICE_NO_CROSSING = "Morgenstern-Price: no F_f/F_m crossing found in "
MPRICE_INADMISSIBLE = "Morgenstern-Price: inadmissible solution "

#: The force-equilibrium family's three, under its own assumption. The closure is
#: scanned over a fixed window rather than iterated from a guess, so "the
#: iteration ran out" is no longer one of its outcomes: either the window holds no
#: root at all, or it holds roots and none of them describes a body of soil (both
#: no-admissible-root facts), or the root it reports is refused afterwards on the
#: base tension it implies.
#: The simplified methods' one. OMS, Bishop and Janbu each return a single
#: factor of safety from a converged iteration, so "no root" is not one of their
#: outcomes; what they can do is converge on a state that is not a body of soil,
#: and until now nothing tested for it. See `_base_normal_admissibility`.
SIMPLIFIED_INADMISSIBLE = ": inadmissible solution "

FORCE_EQ_NO_ROOT = "force_equilibrium: the force closure has no root in FS = "
FORCE_EQ_NO_ADMISSIBLE_ROOT = ("force_equilibrium: no admissible force-closure "
                               "root on this surface")
FORCE_EQ_INADMISSIBLE = "force_equilibrium: inadmissible solution "

#: message prefix -> class. ONLY messages whose meaning has been read off the
#: code that emits them appear here. Anything else is unmapped, and a caller that
#: tallies failures must say so rather than guess: the fallback that used to be
#: "not_converged" turned Morgenstern-Price's no-crossing condition — a
#: no-admissible-root fact — into a fabricated report of iterations running out.
_FAILURE_KINDS = (
    (SPENCER_NO_ADMISSIBLE_SOLUTION, "no_admissible_solution"),
    (SPENCER_INADMISSIBLE, "inadmissible"),
    (SPENCER_NO_CONVERGENCE, "not_converged"),
    (MPRICE_NO_CROSSING, "no_admissible_solution"),
    (MPRICE_INADMISSIBLE, "inadmissible"),
    (FORCE_EQ_NO_ROOT, "no_admissible_solution"),
    (FORCE_EQ_NO_ADMISSIBLE_ROOT, "no_admissible_solution"),
    (FORCE_EQ_INADMISSIBLE, "inadmissible"),
    ("the Ordinary Method of Slices" + SIMPLIFIED_INADMISSIBLE, "inadmissible"),
    ("Bishop's Simplified Method" + SIMPLIFIED_INADMISSIBLE, "inadmissible"),
    ("Janbu's Simplified Method" + SIMPLIFIED_INADMISSIBLE, "inadmissible"),
)

#: How far above the residual the solver ACCEPTS the reachable floor must stand
#: before the general-case existence test will say a surface admits no admissible
#: solution: a thousandfold. Anchored to the tolerance rather than to a fraction
#: of the driving weight because the measured floors form a continuum (2e-4 to
#: 8e-3 of the driving weight across the corpus, with no gap in them) while the
#: distance from acceptance is what the claim is actually about.
NO_SOLUTION_MARGIN = 1e3

#: A backstop under the above, for a model whose weights are small enough that
#: the tolerance-relative bar would sit in float noise.
NO_SOLUTION_FLOOR = 1e-6

#: How far the extent of base tension may go before a solution is refused: more
#: than half the slices. A base in tension mobilizes no Mohr-Coulomb strength, so
#: past that point the solution contradicts the strength model it was solved with
#: on most of the surface. Shared by force_equilibrium (corps, lowe) and mprice.
#: Valid criticals across the corpus run 0-15%.
MAX_BASE_TENSION_EXTENT = 0.5

#: The factor-of-safety window the force-equilibrium closure is scanned over, and
#: how finely. `Z_{n+1}(F) = 0` is not single-valued: the per-slice determinant
#: `cos(alpha-theta) + tan(phi)/F * sin(alpha-theta)` vanishes at its own factor of
#: safety on every slice where `alpha - theta` is obtuse, and each of those poles
#: separates one root of the closure from the next. A slip surface can therefore
#: carry a dozen roots between 0.05 and 10, only one of which describes a body of
#: soil. The scan brackets them all; `_force_closure_root` selects among them.
FE_FS_MIN = 0.05
FE_FS_MAX = 10.0
FE_FS_SCAN = 200

#: How close to zero the force-equilibrium base factor may come at a root. The
#: factor `cos(alpha-theta) + tan(phi)/F * sin(alpha-theta)` is this march's
#: counterpart of Bishop's `m_alpha`: it divides every per-slice solve, so a root
#: where it vanishes on any slice sits on the pole rather than describing a state
#: of the mass. Between each consecutive pair of poles the residual sweeps the
#: whole real line and so always has a root; those are the spurious branch, and
#: they are the ones that read a low factor of safety against side forces of
#: several times the weight of the sliding mass. Measured over every Corps and
#: Lowe solution the shipped corpus produces on its own surfaces, the answers that
#: agree with the moment methods keep this factor above 0.2 on every slice, while
#: the between-poles roots sit at 0.003 to 0.022.
#:
#: The same bar gates Bishop's and Janbu's m_alpha, which is the same quantity
#: under the horizontal-interslice assumption: `N' = num / m_alpha`, so a slice
#: whose m_alpha has reached zero has a base normal that runs to infinity and then
#: reverses, and a factor of safety computed from it is not a state of the mass.
#: Measured over every Bishop and Janbu solution the corpus produces on its own
#: surfaces (570 solves), the nearest any accepted answer comes to it is 0.2439 —
#: five times the bar — while the root the guard refuses on
#: `xslope_noncircular`'s deep surface reaches -0.2507 on four of forty-one
#: slices.
FE_MIN_BASE_FACTOR = 0.05

#: Largest interslice resultant a force-equilibrium root may carry, as a multiple
#: of the total driving load on the sliding mass (`_driving_load`: its weight plus
#: the distributed, line, seismic and tension-crack-water loads applied to it). The
#: interslice forces are internal to that mass and are equilibrated by it, so a
#: boundary transmitting more than everything driving the mass is describing a
#: numerical branch of the recurrence rather than a state of stress. Roots on the
#: physical branch across the corpus run well under half that load. The denominator
#: is the whole driving load rather than the weight alone so that a bearing-capacity
#: section carried by a surcharge at a nominal unit weight is judged on the load it
#: actually carries.
FE_MAX_Z_OVER_W = 1.0

#: How far BELOW the moment-equilibrium factor of safety on the same slices a
#: force-equilibrium root may stand before it is refused, as a ratio. The measure
#: is one-sided on purpose. Corps of Engineers and Lowe & Karafiath read ABOVE the
#: moment methods by construction, and on a submerged phi = 0 section they read
#: far above — 5.7 times on `xslope_submerged`'s own circle, which
#: `docs/lem/force_eq.md` documents as the method's behavior rather than a
#: defect. Reading far below is the other thing: it is what the spurious branch of
#: the closure does, and the tie-break can only choose among roots that survive,
#: so on a surface whose ONLY surviving root is that branch nothing caught it.
#:
#: Measured over the 588 Corps and Lowe answers the corpus produces on its own
#: surfaces: 540 stand at or above the moment answer, and of the 48 that stand
#: below, the furthest is 1.21 times below. The next three are 8.1, 97.5 and 109
#: times below — `gw012` and `vp046b`, which are this same defect, unrecognized —
#: so the bar sits in a factor of seven of clear air.
FE_MAX_BELOW_MOMENT = 2.0

#: When Spencer's cascade reports a root, the fraction of interior boundaries
#: whose line of thrust may fall outside the slice before the root is treated as
#: DISPUTED and the whole band is swept for the crossings it was chosen against.
#:
#: This is a trigger, not a refusal: a disputed root is still reported if the
#: sweep and the tie-break return it. It has to be cheap, because a search
#: solves thousands of surfaces and the sweep costs about a hundred times what
#: the cascade does, and it has to be measured, because a bar set by taste would
#: either miss the defect or spend the sweep on every trial.
#:
#: The line of thrust is where the interslice resultant acts. Duncan & Wright
#: require it to lie within the slice, and `_admissibility_warnings` already
#: reports it, so the measure costs nothing to read. Measured over 320 accepted
#: Spencer answers on the corpus's own surfaces the thrust line leaves the slice
#: on at most 54% of boundaries, and over 5 251 search trials on nine models
#: where Spencer and Morgenstern-Price with f(x) = 1 — the same equations solved
#: a different way — return the same factor of safety, on more than 65% of them
#: in 13 trials, 0.25%. On the 665 trials where those two disagree by more than
#: 1% it stands past 65% in 578, and both roots this round was asked to correct
#: are among them: the critical circle of the Rocscience benchmark VP16 at 92%
#: and the critical non-circular surface of VP9 at 80%.
#:
#: The ratio to the moment answer was measured for this job first, and does not
#: do it. Over those same trials an accepted Spencer answer runs from 0.42 to
#: 1.05 times Bishop's on a circle and from 0.82 to 1.71 times Janbu's off one —
#: the tension-cracked benchmark VP30 solves at two thirds of Bishop from every
#: starting guess — while VP16's disputed root sits at 0.97 of Bishop, inside
#: that range with room to spare. The moment answer stays what it always was
#: here, the tie-break; it is not the trigger.
SPENCER_THRUST_OUT_DISPUTED = 0.65

#: The band sweep's starting grid — factors of safety across the window, and
#: positions across the band at each — with the residual-evaluation budget one
#: descent may spend. Module level so a check can vary the resolution and prove
#: the crossings the sweep returns do not move with it.
SPENCER_SWEEP_GRID = (18, 7)
SPENCER_SWEEP_MAX_NFEV = 200


def _thrust_outside_fraction(y_lt, y_lb, yt_l):
    """The fraction of interior boundaries whose line of thrust leaves the slice.

    The same measure `_admissibility_warnings` reports, as a number: the thrust
    line's height above the base as a fraction of the boundary's own height,
    counted outside when it is not in [-0.05, 1.05] or is not finite. Boundaries
    of no height are skipped. Returns 0.0 when there are none to measure.
    """
    y_lt = np.asarray(y_lt, dtype=float)
    y_lb = np.asarray(y_lb, dtype=float)
    yt_l = np.asarray(yt_l, dtype=float)
    h_bnd = y_lt[1:] - y_lb[1:]
    tall = h_bnd > 1e-9
    if not np.any(tall):
        return 0.0
    ratio = (yt_l[1:][tall] - y_lb[1:][tall]) / h_bnd[tall]
    inside = np.isfinite(ratio) & (ratio >= -0.05) & (ratio <= 1.05)
    return 1.0 - float(np.mean(inside))


def failure_kind(message):
    """Which kind of failure this message reports, or None if it is unmapped.

    ``"no_admissible_solution"``  the system has no root the method would accept,
                                  whatever the solver does.
    ``"inadmissible"``            a solution was found and refused on the state it
                                  implies.
    ``"not_converged"``           the iteration did not reach a root that may well
                                  exist.
    ``None``                      a message this module has not measured. Not a
                                  class: callers report it as unclassified rather
                                  than folding it into one of the three.
    """
    text = str(message)
    for prefix, kind in _FAILURE_KINDS:
        if text.startswith(prefix):
            return kind
    return None




def _c_eff(slice_df):
    """Effective (apparent) cohesion per slice: base cohesion ``c`` plus the
    matric-suction apparent cohesion ``c_suction`` when present.

    ``c_suction`` is written by ``generate_slices`` only for the opt-in Fredlund
    extended Mohr-Coulomb suction option, and is 0.0 on every slice otherwise.
    Because IEEE-754 addition of 0.0 is exact, ``c + c_suction`` is bit-identical
    to ``c`` when the option is off, so every solver stays invariant by default.
    The column is absent from pre-suction DataFrames, in which case the base
    cohesion array is returned unchanged.
    """
    c = slice_df['c'].values
    if 'c_suction' in slice_df.columns:
        return c + slice_df['c_suction'].values
    return c


#: Per-slice columns that carry an applied load into the equilibrium equations,
#: alongside the slice weight. Each is a force resultant on one slice in the same
#: units as ``w``: the distributed surface load, the line-load resultant, the
#: horizontal seismic force and the tension-crack water force. Reinforcement,
#: pile and passive-support terms are deliberately absent — they resist the
#: motion rather than drive it, and a resisting force scaled into the denominator
#: would let a stronger section carry larger spurious interslice forces.
_DRIVING_LOAD_COLUMNS = ('dload', 'lload', 'kw', 't')


def _driving_load(slice_df):
    """Total driving load on the sliding mass: its own weight plus every applied load.

    The force-equilibrium root finder judges an interslice resultant against the
    load the mass carries, and on most models that load is the soil itself. It is
    not always: a bearing-capacity section built at a nominal unit weight is driven
    entirely by a surcharge, and dividing a real side force by a weight of 10^-4
    makes every root look like millions of times the mass. The measure is therefore
    the sum of the magnitudes of every driving term the march itself sums —
    ``|w|`` plus the distributed load, the line load, the seismic force and the
    tension-crack water force — so a weightless model is not a special case.

    Returns 0.0 for an empty slice set; callers substitute their own floor.
    """
    n = len(slice_df)
    if not n:
        return 0.0
    total = float(np.abs(np.asarray(slice_df['w'].values, dtype=float)).sum())
    for col in _DRIVING_LOAD_COLUMNS:
        if col in slice_df.columns:
            total += float(np.abs(np.asarray(slice_df[col].values, dtype=float)).sum())
    return total


def solve_selected(method_name, slice_df, rapid=False):
    """
    Executes a specified limit equilibrium solution method and displays results.

    Parameters
    ----------
    method_name : str
        Name of the solution method function to call. Must be one of:
        'oms', 'bishop', 'janbu', 'spencer', 'corps', 'lowe',
        'mprice'
    slice_df : pandas.DataFrame
        Slice dataframe containing all required columns for the specified method
        (see individual method documentation for column requirements)
    rapid : bool, optional
        If True, performs rapid drawdown analysis using the specified method.
        Default is False.

    Returns
    -------
    dict or str
        If successful: dictionary containing method results (includes 'FS' and method-specific parameters)
        If failed: error message string

    Notes
    -----
    This function automatically prints the factor of safety and method-specific
    parameters to the console. For methods with additional parameters:
    - Spencer: displays theta (interslice force angle)
    - Janbu: displays fo (correction factor)
    - Corps of Engineers: displays theta
    """

    func = globals()[method_name]

    if rapid:
        success, result = rapid_drawdown(slice_df, method_name)
    else:
        success, result = func(slice_df)
    if not success:
        print(f'Error: {result}')
        return result

    if func == oms:
        print(f'OMS: FS={result["FS"]:.3f}')
    elif func == bishop:
        print(f'Bishop: FS={result["FS"]:.3f}')
    elif func == spencer:
        print(f'Spencer: FS={result["FS"]:.3f}, theta={result["theta"]:.2f}')
        for w in result.get('warnings', []):
            print(f'  Spencer admissibility warning: {w}')
    elif func == janbu:
        print(f'Janbu Corrected FS={result["FS"]:.3f}, fo={result["fo"]:.2f}')
    elif func == corps:
        print(f'Corps Engineers: FS={result["FS"]:.3f}, theta={result["theta"]:.2f}')
        for w in result.get('warnings', []):
            print(f'  Corps admissibility warning: {w}')
    elif func == lowe:
        print(f'Lowe & Karafiath: FS={result["FS"]:.3f}')
        for w in result.get('warnings', []):
            print(f'  Lowe & Karafiath admissibility warning: {w}')
    elif func == mprice:
        print(f'Morgenstern-Price ({result["f_type"]}): FS={result["FS"]:.3f}, '
              f'lambda={result["lambda"]:.3f}')
        for w in result.get('warnings', []):
            print(f'  Morgenstern-Price admissibility warning: {w}')

    return result

def solve_all(slice_df, rapid=False):
    """
    Executes all available limit equilibrium solution methods sequentially.

    Runs six different limit equilibrium methods on the provided slice dataframe
    and displays the factor of safety for each method. This is useful for comparing
    results across multiple solution approaches.

    Parameters
    ----------
    slice_df : pandas.DataFrame
        Slice dataframe containing all required columns for all methods.
        Must include: 'alpha', 'phi', 'c', 'w', 'u', 'dl', 'dload', 'd_x', 'd_y',
        'beta', 'kw', 't', 'y_t', 'p', 'x_c', 'y_cg', and additional columns
        required for specific methods (e.g., 'r', 'xo', 'yo' for circular methods).

    Returns
    -------
    None
        Results are printed to console for each method.

    Notes
    -----
    Methods executed in order:
    1. Ordinary Method of Slices (OMS)
    2. Bishop's Simplified Method
    3. Janbu's Simplified Method
    4. Corps of Engineers Method
    5. Lowe & Karafiath Method
    6. Spencer's Method
    7. Morgenstern-Price Method

    A method that CANNOT apply to this surface is skipped with its reason stated,
    rather than reported as a bare error: OMS and Bishop take moments about a circle
    center, so on a non-circular surface the question is ill-posed rather than merely
    hard. Refusing the whole run would be actively wrong -- on a straight-plane
    benchmark it would suppress the two published answers because OMS cannot run.
    A method that applies but fails numerically still reports its own error.
    """
    family = "circular" if _has_circle_center(slice_df) else "noncircular"
    for name in ('oms', 'bishop', 'janbu', 'corps', 'lowe', 'spencer', 'mprice'):
        reason = method_surface_reason(name, family)
        if reason:
            print(f'Skipped {name}: {reason}')
            continue
        solve_selected(name, slice_df, rapid=rapid)


def _has_circle_center(slice_df):
    """True when the slice table carries a usable circle center.

    Uses ``pd.isna`` rather than ``is None``: a circle center that has been through a
    float round-trip arrives as NaN, not None, and an identity test against None lets
    it straight past -- OMS then returns ``(True, {'FS': nan})``, a success tuple
    carrying NaN that every caller downstream accepts as a solution.
    """
    if 'r' not in slice_df.columns or len(slice_df) == 0:
        return False
    r = slice_df['r'].iloc[0]
    return r is not None and not pd.isna(r)


def _moment_arms(slice_df, Xo, Yo, alpha, right_facing):
    """Per-slice moment arms about the center of rotation (Xo, Yo), for the two
    moment methods (OMS, Bishop).

        xr   horizontal arm of the slice weight        ( = R·sinα  on a circle )
        a_S  moment arm of the base shear              ( = R       on a circle )
        a_N  perpendicular offset of the base normal   ( = 0       on a circle )

    On a true circular arc the base normal points straight at the center, so it
    exerts no moment, and every base is at radius R — which is what lets the
    textbook OMS/Bishop equations factor R out and drop the normal entirely.
    Neither holds on a COMPOSITE surface (a circle truncated at bedrock, see
    slice.CompositeSurface): the run along the floor is not at radius R and its
    normal misses the center. These are the general arms — SLOPE/W's per-slice R
    and its normal offset f — and they collapse identically to (R·sinα, R, 0) when
    the surface is a circle, so no circular result moves.

    The x-arms are taken in the orientation-normalized frame that alpha lives in
    (mirrored on right-facing slopes), the same correction as a_dx / pile_x_arm.
    """
    xr = slice_df['x_c'].values - Xo
    if right_facing:
        xr = -xr
    yr = slice_df['y_cb'].values - Yo
    sa, ca = np.sin(alpha), np.cos(alpha)
    a_S = xr * sa - yr * ca
    a_N = xr * ca + yr * sa
    return xr, a_S, a_N


def oms(slice_df, debug=False):
    """
    Computes FS by direct application of Equation 9 (Ordinary Method of Slices).

    Inputs
    ------
    slice_df : pandas.DataFrame
        Must contain exactly these columns (length = n slices):
          'alpha'   (deg)   = base inclination αᵢ
          'phi'     (deg)   = friction angle φᵢ
          'c'             = cohesion cᵢ
          'w'             = slice weight Wᵢ
          'u'             = pore pressure force/unit‐length on base, uᵢ
          'dl'            = base length Δℓᵢ
          'dload'         = resultant distributed load Dᵢ
          'd_x','d_y'     = centroid (x,y) at which Dᵢ acts
          'beta'   (deg)   = distributed-load inclination βᵢ
          'kw'            = seismic horizontal kWᵢ
          't'             = tension‐crack horizontal Tᵢ  (zero except one slice)
          'y_t'           = y‐loc of Tᵢ's line of action (zero except that one slice)
          'p'             = reinforcement uplift pᵢ (zero if none)
          'x_c','y_cg'    = slice‐centroid (x,y) for seismic moment arm
          'h_pile'        = pile/pier force on base (zero if none)
          'theta_p' (RAD)  = pile force inclination from horizontal — stored and
                            consumed in RADIANS, unlike every other angle here
          'r'             = radius of circular failure surface
          'xo','yo'       = x,y coordinates of circle center

    Returns
    -------
    (bool, dict_or_str)
      • If success: (True, {'method':'oms', 'FS': <computed value>})
      • If denominator → 0 or other fatal error: (False, "<error message>")


    """
    if not _has_circle_center(slice_df):
        return False, method_surface_reason('oms', 'noncircular')

    # 1) Unpack circle‐center and radius as single values
    Xo = slice_df['xo'].iloc[0]    # Xoᵢ (x-coordinate of circle center)
    Yo = slice_df['yo'].iloc[0]    # Yoᵢ (y-coordinate of circle center)
    R  = slice_df['r'].iloc[0]     # Rᵢ (radius of circular failure surface)

    # 2) Pull arrays directly from slice_df
    alpha_deg = slice_df['alpha'].values    # αᵢ in degrees
    phi_deg   = slice_df['phi'].values      # φᵢ in degrees
    c     = _c_eff(slice_df)            # cᵢ (+ apparent cohesion from matric suction, if any)
    W     = slice_df['w'].values        # Wᵢ
    u     = slice_df['u'].values        # uᵢ (pore‐force per unit length)
    dl     = slice_df['dl'].values       # Δℓᵢ
    D     = slice_df['dload'].values        # Dᵢ
    d_x    = slice_df['d_x'].values      # d_{x,i}
    d_y    = slice_df['d_y'].values      # d_{y,i}
    beta_deg  = slice_df['beta'].values     # βᵢ in degrees
    kw    = slice_df['kw'].values       # kWᵢ
    T     = slice_df['t'].values        # Tᵢ (zero except one slice)
    y_t    = slice_df['y_t'].values      # y_{t,i} (zero except one slice)
    P     = slice_df['p'].values        # pᵢ
    x_c    = slice_df['x_c'].values      # x_{c,i}
    y_cg = slice_df['y_cg'].values       # y_{cg,i} coordinate of slice centroid

    # Pile forces (backward compatible — zeros if no pile data)
    n = len(slice_df)
    H_pile  = slice_df['h_pile'].values  if 'h_pile'  in slice_df.columns else np.zeros(n)
    theta_p = slice_df['theta_p'].values if 'theta_p' in slice_df.columns else np.zeros(n)
    y_pile  = slice_df['y_pile'].values  if 'y_pile'  in slice_df.columns else np.zeros(n)
    x_pile  = slice_df['x_pile'].values  if 'x_pile'  in slice_df.columns else np.zeros(n)

    # v12 support/load terms (all zero when the columns are absent -> pre-v12
    # behavior). Axial reinforcement mirrors the pile-force pattern (a known
    # force at a point with a real direction); line loads mirror the
    # distributed-load pattern (an equivalent resultant at an inclination in the
    # dload convention); passive terms are factored by FS where supported.
    def _c12(name):
        return slice_df[name].values.astype(float) if name in slice_df.columns else np.zeros(n)
    P_pt  = _c12('p_pt')
    pa_cx = _c12('pa_cx'); pa_cy = _c12('pa_cy')
    pa_mx = _c12('pa_mx'); pa_my = _c12('pa_my')
    pp_cx = _c12('pp_cx'); pp_cy = _c12('pp_cy')
    pp_mx = _c12('pp_mx'); pp_my = _c12('pp_my')
    H_pas = _c12('h_pile_pas')
    LL    = _c12('lload')
    ll_b  = np.radians(_c12('ll_beta'))
    ll_x  = _c12('ll_x'); ll_y = _c12('ll_y')
    has_passive = bool(np.any(P_pt) or np.any(pp_cx) or np.any(pp_cy) or np.any(H_pas))
    # Axial components are stored normalized to cos(psi) > 0; on a right-facing
    # slope the tension on the sliding mass is the NEGATION of that direction,
    # so its vertical component flips sign. Only the vertical-equilibrium copies
    # flip: the horizontal component is consumed as a resisting magnitude, and
    # the moment terms flip their own x-part where used.
    _rf = slice_df['y_lb'].iat[0] > slice_df['y_rb'].iat[-1]
    pa_cy_v = -pa_cy if _rf else pa_cy
    pp_cy_v = -pp_cy if _rf else pp_cy

    # 3) Convert angles to radians
    alpha = np.radians(alpha_deg)   # αᵢ [rad]
    phi   = np.radians(phi_deg)     # φᵢ [rad]
    beta  = np.radians(beta_deg)    # βᵢ [rad]

    # 4) Precompute sines/cosines
    sin_alpha = np.sin(alpha)          # sin(αᵢ)
    cos_alpha = np.cos(alpha)          # cos(αᵢ)
    sin_ab    = np.sin(alpha - beta)   # sin(αᵢ−βᵢ)
    cos_ab    = np.cos(alpha - beta)   # cos(αᵢ−βᵢ)
    tan_phi   = np.tan(phi)            # tan(φᵢ)

    # ————————————————————————————————————————————————————————
    # 5) Build the NUMERATOR (Eqn 8) = Σᵢ [  cᵢ·Δℓᵢ
    #       + (Wᵢ·cosαᵢ + Dᵢ·cos(αᵢ−βᵢ) − kWᵢ·sinαᵢ − Tᵢ·sinαᵢ − uᵢ·Δℓᵢ )·tanφᵢ ]
    #


    # N′ᵢ = Wᵢ·cosαᵢ + Dᵢ·cos(αᵢ−βᵢ) − kWᵢ·sinαᵢ − Tᵢ·sinαᵢ − uᵢ·Δℓᵢ + Hᵢ·sin(αᵢ−θₚᵢ)
    N_eff = (
        W * cos_alpha
      + D * cos_ab
      - kw * sin_alpha
      - T * sin_alpha
      - (u * dl)
      + (H_pile - H_pas) * np.sin(alpha - theta_p)
      + (sin_alpha * pa_cx - cos_alpha * pa_cy_v)   # axial reinforcement, normal comp
      + LL * np.cos(alpha - ll_b)                 # line load (dload pattern)
    )

    #   Σ  Dᵢ·sinβᵢ·(Yo - d_{y,i}) 
    a_dy = Yo - d_y
    sum_Dy = np.sum(D * np.sin(beta) * a_dy)

    # ————————————————————————————————————————————————————————
    # 6) Build each piece of the DENOMINATOR exactly as Eqn 8, as MOMENTS about the
    # center of rotation. (The classic form divides the moment terms by R instead;
    # the two are the same equation, but only the moment form survives a composite
    # surface, where the base is not everywhere at radius R.)

    #  (B) = Σ  Dᵢ·cosβᵢ·(Xo - d_{x,i})
    # The vertical D-component (D·cosβ) acts at horizontal arm (d_x - Xo). That arm
    # flips sign when the slope faces right, and cosβ (unlike sinβ) is NOT corrected
    # by the β sign-flip applied in generate_slices, so flip it here. The horizontal
    # D-component term (a_dy / sum_Dy) is already sign-correct via that β-flip and is
    # left untouched; likewise the seismic arm a_k (the local ``a_s`` below) and
    # the tension-crack arm a_t.
    # An explicit facing from generate_slices (flat-arc / override case) wins;
    # otherwise fall back to the historical geometric test, byte-identical.
    right_facing = slice_df.attrs.get(
        'right_facing', slice_df['y_lb'].iat[0] > slice_df['y_rb'].iat[-1])

    # Moment arms about (Xo, Yo). a_S == R and a_N == 0 on a true circle.
    xr, a_S, a_N = _moment_arms(slice_df, Xo, Yo, alpha, right_facing)

    #  (A) = Σ [ Wᵢ · sinαᵢ ] · R  =  Σ [ Wᵢ · xrᵢ ]
    sum_W = np.sum(W * xr)

    a_dx = d_x - Xo
    if right_facing:
        a_dx = -a_dx
    sum_Dx = np.sum(D * np.cos(beta) * a_dx)

    #  (C) = Σ [ kWᵢ * a_k ] with a_k = (Yo - y_{cg,i}), the seismic arm the
    #  derivation and the report's symbol table both call a_k.
    a_s = Yo - y_cg
    sum_kw = np.sum(kw * a_s)

    #  (D) = Σ [ Tᵢ * (Yo - y_{t,i}) ]
    a_t = Yo - y_t
    sum_T = np.sum(T * a_t)

    # Pile resisting moment about circle center:
    # M_pile = Σ [ H·cos(θₚ)·(Yo - y_pile) + H·sin(θₚ)·(x_pile - Xo) ]
    # The vertical-component arm (x_pile - Xo) is in real coordinates while alpha runs in
    # the orientation-normalized frame, so it must flip on right-facing slopes (same
    # correction as the distributed-load a_dx arm). Only matters for battered piles
    # (theta_p != 0); for theta_p = 0 this term is zero.
    pile_x_arm = -(x_pile - Xo) if right_facing else (x_pile - Xo)
    h_act = H_pile - H_pas
    sum_pile_moment = np.sum(
        h_act * np.cos(theta_p) * (Yo - y_pile)
      + h_act * np.sin(theta_p) * pile_x_arm
    )
    sum_pile_moment_pas = np.sum(
        H_pas * np.cos(theta_p) * (Yo - y_pile)
      + H_pas * np.sin(theta_p) * pile_x_arm
    )

    # Axial reinforcement moment about the circle center (pile pattern: the
    # x-arm flips on right-facing slopes). M = cx*(Yo - y_r) + cy*(x_r - Xo),
    # linearized through the slice sums (mx = sum cy*x_r, my = sum cx*y_r).
    # (facing-invariant: on right-facing slopes the stored axial components and
    # the resisting-rotation sense both negate, so the raw expression stands)
    ra_x_part = (pa_mx - Xo * pa_cy)
    rp_x_part = (pp_mx - Xo * pp_cy)
    sum_reinf_moment_a = np.sum(pa_cx * Yo - pa_my + ra_x_part)
    sum_reinf_moment_p = np.sum(pp_cx * Yo - pp_my + rp_x_part)

    # Line-load moment terms mirror the distributed-load terms exactly.
    # LL·cos(ll_b) = −L·sin δ: the line load is stored in the dload convention,
    # its magnitude L at an angle δ from horizontal folded into a resultant at
    # ll_beta, with the sign of the vertical component absorbed into that angle
    # (generate_slices, "Line loads"). LL·sin(ll_b) = +L·cos δ, mirrored on a
    # right-facing slope as the top-edge beta is. So these two sums ARE the
    # published −[L cos δ·a_fy + L sin δ·a_fx] on the driving side.
    ll_x_arm = -(ll_x - Xo) if right_facing else (ll_x - Xo)
    sum_LLx = np.sum(LL * np.cos(ll_b) * ll_x_arm)
    sum_LLy = np.sum(LL * np.sin(ll_b) * (Yo - ll_y))

    # Put them together. Every term is now a moment about (Xo, Yo): the support/load
    # terms already were (that is why the classic form divides them by R), and the
    # slice terms pick up their arms here. Active P, sum_Dy, and the pile/axial
    # moments are known resisting forces, not factored by FS; line loads are known
    # applied loads. The base normal joins the driving side through a_N — zero for
    # every slice of a circle, non-zero along a composite surface's floor run.
    denominator = (sum_W + sum_Dx + sum_kw + sum_T + sum_LLx
                   - np.sum(P * a_S) - (sum_Dy + sum_LLy)
                   - sum_pile_moment - sum_reinf_moment_a
                   - np.sum((N_eff + u * dl) * a_N))

    # Passive support (ultimate capacities mobilized with the soil) joins the
    # RESISTING side: numerator gains the capacity moments. OMS is non-iterative,
    # so passive components cannot enter N_eff; their resisting moment is the
    # entire contribution (consistent with OMS's moment-only basis).
    numerator = (np.sum((c * dl + N_eff * tan_phi) * a_S) + np.sum(P_pt * a_S)
                 + sum_reinf_moment_p + sum_pile_moment_pas)

    # 7) Finally compute FS = (numerator)/(denominator)
    if denominator <= 0:
        return False, "Net driving moment is non-positive (resisting forces exceed driving forces)."
    FS = numerator / denominator

    # 8) Store effective normal forces in the DataFrame
    slice_df['n_eff'] = N_eff

    # The Fellenius normal does not divide by m_alpha, so only the extent of base
    # tension is tested here; see _base_normal_admissibility.
    reason, warns = _base_normal_admissibility(
        "the Ordinary Method of Slices", N_eff)
    if reason:
        return False, reason

    if debug==True:
        print(f'numerator = {numerator:.4f}')
        print(f'denominator = {denominator:.4f}')
        print(f'Sum_W = {sum_W:.4f}')
        print(f'Sum_Dx = {sum_Dx:.4f}')
        print(f'Sum_Dy = {sum_Dy:.4f}')
        print(f'Sum_kw = {sum_kw:.4f}')
        print(f'Sum_T = {sum_T:.4f}')
        if np.any(H_pile > 0):
            print(f'sum_pile_moment = {sum_pile_moment:.4f}')
        print('N_eff =', np.array2string(N_eff, precision=4, separator=', '))

    # 9) Return success and the FS
    return True, {'method': 'oms', 'FS': FS, 'warnings': warns}

def bishop(slice_df, debug=False, tol=1e-6, max_iter=100, fs_seed=None):
    """
    Computes FS using the complete Bishop's Simplified Method (Equation 10) and computes N_eff (Equation 8).
    Requires circular slip surface and full input data structure consistent with OMS.

    Parameters:
        slice_df : pandas.DataFrame with required columns (see OMS spec)
        debug : bool, if True prints diagnostic info
        tol : float, convergence tolerance
        max_iter : int, maximum iteration steps

    Returns:
        (bool, dict | str): (True, {'method': 'bishop', 'FS': value}) or (False, error message)
    """

    if not _has_circle_center(slice_df):
        return False, method_surface_reason('bishop', 'noncircular')

    # 1) Unpack circle‐center and radius as single values
    Xo = slice_df['xo'].iloc[0]    # Xoᵢ (x-coordinate of circle center)
    Yo = slice_df['yo'].iloc[0]    # Yoᵢ (y-coordinate of circle center)
    R  = slice_df['r'].iloc[0]     # Rᵢ (radius of circular failure surface)

    # Load input arrays
    alpha = np.radians(slice_df['alpha'].values)
    phi   = np.radians(slice_df['phi'].values)
    c     = _c_eff(slice_df)
    W     = slice_df['w'].values
    u     = slice_df['u'].values
    dl    = slice_df['dl'].values
    D     = slice_df['dload'].values
    d_x   = slice_df['d_x'].values
    d_y   = slice_df['d_y'].values
    beta  = np.radians(slice_df['beta'].values)
    kw    = slice_df['kw'].values
    T     = slice_df['t'].values
    y_t   = slice_df['y_t'].values
    P     = slice_df['p'].values
    x_c   = slice_df['x_c'].values
    y_cg  = slice_df['y_cg'].values

    # Pile forces (backward compatible — zeros if no pile data)
    n = len(slice_df)
    H_pile  = slice_df['h_pile'].values  if 'h_pile'  in slice_df.columns else np.zeros(n)
    theta_p = slice_df['theta_p'].values if 'theta_p' in slice_df.columns else np.zeros(n)
    y_pile  = slice_df['y_pile'].values  if 'y_pile'  in slice_df.columns else np.zeros(n)
    x_pile  = slice_df['x_pile'].values  if 'x_pile'  in slice_df.columns else np.zeros(n)

    # v12 support/load terms (all zero when the columns are absent)
    def _c12(name):
        return slice_df[name].values.astype(float) if name in slice_df.columns else np.zeros(n)
    P_pt  = _c12('p_pt')
    pa_cx = _c12('pa_cx'); pa_cy = _c12('pa_cy')
    pa_mx = _c12('pa_mx'); pa_my = _c12('pa_my')
    pp_cx = _c12('pp_cx'); pp_cy = _c12('pp_cy')
    pp_mx = _c12('pp_mx'); pp_my = _c12('pp_my')
    H_pas = _c12('h_pile_pas')
    LL    = _c12('lload')
    ll_b  = np.radians(_c12('ll_beta'))
    ll_x  = _c12('ll_x'); ll_y = _c12('ll_y')
    # Vertical-equilibrium copies of the axial components: flip on right-facing
    # slopes (see oms(); the moment terms below flip their own x-part instead).
    _rf = slice_df['y_lb'].iat[0] > slice_df['y_rb'].iat[-1]
    pa_cy_v = -pa_cy if _rf else pa_cy
    pp_cy_v = -pp_cy if _rf else pp_cy

    # Trigonometric terms
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    tan_phi   = np.tan(phi)
    sin_beta  = np.sin(beta)
    cos_beta  = np.cos(beta)

    # Moment arms. The vertical-D-component arm (a_dx) flips sign on right-facing
    # slopes and is not corrected by the β sign-flip in generate_slices (cosβ is
    # even in β), so flip it here. a_dy (horizontal-D-component) is already correct
    # via that β-flip; the seismic arm a_k (the local ``a_s`` below) and the
    # tension-crack arm a_t track the sliding-direction convention. See oms().
    # Explicit facing (flat-arc / override) wins; else historical test, byte-identical.
    right_facing = slice_df.attrs.get(
        'right_facing', slice_df['y_lb'].iat[0] > slice_df['y_rb'].iat[-1])
    a_dx = d_x - Xo
    if right_facing:
        a_dx = -a_dx
    a_dy = Yo - d_y
    a_s  = Yo - y_cg
    a_t  = Yo - y_t

    # Slice moment arms about (Xo, Yo): a_S == R and a_N == 0 on a true circle, so
    # this reproduces the classic R-normalized Bishop equation exactly. A composite
    # surface (circle truncated at bedrock) needs the general arms. See _moment_arms.
    xr, a_S, a_N = _moment_arms(slice_df, Xo, Yo, alpha, right_facing)

    # Pile resisting moment about circle center (same term as OMS) — flip the
    # vertical-component arm (x_pile - Xo) on right-facing slopes, as for a_dx above.
    pile_x_arm = -(x_pile - Xo) if right_facing else (x_pile - Xo)
    h_act = H_pile - H_pas
    sum_pile_moment = np.sum(
        h_act * np.cos(theta_p) * (Yo - y_pile)
      + h_act * np.sin(theta_p) * pile_x_arm
    )
    sum_pile_moment_pas = np.sum(
        H_pas * np.cos(theta_p) * (Yo - y_pile)
      + H_pas * np.sin(theta_p) * pile_x_arm
    )

    # Axial reinforcement and line-load moment terms (see oms())
    # (facing-invariant: on right-facing slopes the stored axial components and
    # the resisting-rotation sense both negate, so the raw expression stands)
    ra_x_part = (pa_mx - Xo * pa_cy)
    rp_x_part = (pp_mx - Xo * pp_cy)
    sum_reinf_moment_a = np.sum(pa_cx * Yo - pa_my + ra_x_part)
    sum_reinf_moment_p = np.sum(pp_cx * Yo - pp_my + rp_x_part)
    ll_x_arm = -(ll_x - Xo) if right_facing else (ll_x - Xo)
    sum_LLx = np.sum(LL * np.cos(ll_b) * ll_x_arm)
    sum_LLy = np.sum(LL * np.sin(ll_b) * (Yo - ll_y))

    # Driving moment about (Xo, Yo) — active pile/axial moments are known resisting
    # forces, not factored by FS; line loads are known applied loads. Everything here
    # is FS-independent; the base-normal moment is not, and is added in the loop.
    sum_W = np.sum(W * xr)
    sum_Dx = np.sum(D * cos_beta * a_dx)
    sum_Dy = np.sum(D * sin_beta * a_dy)
    sum_kw = np.sum(kw * a_s)
    sum_T = np.sum(T * a_t)
    denom_fixed = (sum_W + sum_Dx + sum_kw + sum_T + sum_LLx
                   - np.sum(P * a_S) - (sum_Dy + sum_LLy)
                   - sum_pile_moment - sum_reinf_moment_a)

    # Passive capacity moments join the resisting side (the numerator of F)
    res_passive = np.sum(P_pt * a_S) + sum_reinf_moment_p + sum_pile_moment_pas

    # Vertical component of pile force (upward, reduces net downward force on slice)
    H_sin_tp = H_pile * np.sin(theta_p)

    # Iterative solution — from the caller's seed when one is given (Monte
    # Carlo passes the most-likely-values FS), else the historical start.
    F = 1.0 if fs_seed is None else float(fs_seed)
    for _ in range(max_iter):
        # Compute N_eff — H·sin(θp) enters vertical equilibrium
        # Vertical equilibrium: known loads at full value; passive support
        # mobilizes with the soil, so its vertical components carry 1/F.
        vert_known = (W + D * cos_beta + LL * np.cos(ll_b)
                      - P * sin_alpha - pa_cy_v - (H_pile - H_pas) * np.sin(theta_p))
        vert_pas = (P_pt * sin_alpha + pp_cy_v + H_pas * np.sin(theta_p))
        num_N = (
            vert_known - vert_pas / F
            - u * dl * cos_alpha
            - (c * dl * sin_alpha) / F
        )
        denom_N = cos_alpha + (sin_alpha * tan_phi) / F
        N_eff = num_N / denom_N

        # The base normal exerts a moment only where it misses the center of
        # rotation (a_N = 0 on every slice of a true arc, non-zero along a composite
        # surface's floor run). It depends on N_eff, so it lives inside the loop.
        denominator = denom_fixed - np.sum((N_eff + u * dl) * a_N)
        if denominator <= 0:
            return False, "Net driving moment is non-positive (resisting forces exceed driving forces)."

        # Resisting moment: the mobilized base shear (c·dl + N'·tanφ) on its own arm
        numerator = np.sum((c * dl + N_eff * tan_phi) * a_S) + res_passive
        F_new = numerator / denominator

        if abs(F_new - F) < tol:
            slice_df['n_eff'] = N_eff
            reason, warns = _base_normal_admissibility(
                "Bishop's Simplified Method", N_eff, m_alpha=denom_N)
            if reason:
                return False, reason
            if debug:
                print(f"FS = {F_new:.6f}")
                print(f"Numerator = {numerator:.6f}")
                print(f"Denominator = {denominator:.6f}")
                if np.any(H_pile > 0):
                    print(f"sum_pile_moment = {sum_pile_moment:.6f}")
                print("N_eff =", np.array2string(N_eff, precision=4, separator=', '))
            return True, {'method': 'bishop', 'FS': F_new,
                          'warnings': warns}

        F = F_new

    return False, "Bishop method did not converge within the maximum number of iterations."

def janbu(slice_df, debug=False, tol=1e-6, max_iter=100):
    """
    Computes FS using Janbu's Simplified Method with the f0 correction factor.

    Janbu's Simplified Method satisfies overall HORIZONTAL FORCE equilibrium of
    the sliding mass with the inter-slice shear forces neglected. The effective
    base normal force is obtained from VERTICAL equilibrium of each slice — the
    same m_alpha = cosα + sinα·tanφ/F relation used by Bishop's method — which
    makes the factor of safety iterative in F. The base (uncorrected) factor of
    safety is then multiplied by Janbu's empirical correction factor
    f0(d/L, soil type), which compensates for neglecting the inter-slice shear.

    This is the standard Janbu Simplified formulation (matching e.g. GeoStudio
    SLOPE/W's F_f at lambda=0). It is NOT the Ordinary/Fellenius normal force —
    using N = W·cosα − u·dl with a ΣW·sinα denominator (an earlier xslope error)
    collapses the base FS onto the Ordinary Method of Slices.

    Implements the full slice force budget: distributed loads (dload at the load
    inclination beta), seismic force (kw, horizontal), tension-crack water force
    (t, horizontal), line reinforcement (p), and pile forces (h_pile/theta_p).

    Parameters:
        slice_df : pandas.DataFrame with required columns (see OMS spec)
        debug : bool, if True prints diagnostic info
        tol : float, convergence tolerance on F
        max_iter : int, maximum fixed-point iterations

    Returns:
        (bool, dict | str): (True, {'method': 'janbu', 'FS': corrected_value,
                            'fo': correction_factor, 'FS_base': uncorrected_value})
                           or (False, error message)
    """

    # Load input arrays
    alpha = np.radians(slice_df['alpha'].values)
    phi = np.radians(slice_df['phi'].values)
    c = _c_eff(slice_df)
    W = slice_df['w'].values
    u = slice_df['u'].values
    dl = slice_df['dl'].values
    D = slice_df['dload'].values
    beta = np.radians(slice_df['beta'].values)
    kw = slice_df['kw'].values
    T = slice_df['t'].values
    P = slice_df['p'].values

    # Pile forces (backward compatible — zeros if no pile data)
    n = len(slice_df)
    H_pile  = slice_df['h_pile'].values  if 'h_pile'  in slice_df.columns else np.zeros(n)
    theta_p = slice_df['theta_p'].values if 'theta_p' in slice_df.columns else np.zeros(n)

    # Trigonometric terms
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    tan_phi = np.tan(phi)
    cos_beta = np.cos(beta)
    sin_beta = np.sin(beta)

    # Pile force components: vertical H·sin(θp) into vertical equilibrium,
    # horizontal H·cos(θp) into the horizontal force balance.
    H_sin_tp = H_pile * np.sin(theta_p)
    H_cos_tp = H_pile * np.cos(theta_p)

    # v12 support/load terms (all zero when the columns are absent)
    def _c12(name):
        return slice_df[name].values.astype(float) if name in slice_df.columns else np.zeros(n)
    P_pt  = _c12('p_pt')
    pa_cx = _c12('pa_cx'); pa_cy = _c12('pa_cy')
    pp_cx = _c12('pp_cx'); pp_cy = _c12('pp_cy')
    H_pas = _c12('h_pile_pas')
    LL    = _c12('lload')
    ll_b  = np.radians(_c12('ll_beta'))
    # Vertical-equilibrium copies of the axial components: flip on right-facing
    # slopes (see oms()).
    _rf = slice_df['y_lb'].iat[0] > slice_df['y_rb'].iat[-1]
    pa_cy_v = -pa_cy if _rf else pa_cy
    pp_cy_v = -pp_cy if _rf else pp_cy
    H_sin_act = (H_pile - H_pas) * np.sin(theta_p)
    H_cos_act = (H_pile - H_pas) * np.cos(theta_p)
    H_sin_pas = H_pas * np.sin(theta_p)
    H_cos_pas = H_pas * np.cos(theta_p)

    # External horizontal driving forces (independent of F): seismic (driving),
    # tension-crack water (driving), distributed and line loads (signed by their
    # own inclination), reinforcement and pile horizontal components (resisting).
    #
    # A surface load carries the force (D·sinβ, −D·cosβ): its horizontal component
    # is a SIGNED quantity in the sliding-direction frame, not a magnitude in the
    # driving direction the way seismic kw and the tension-crack force T are. A
    # load normal to a slope face has β > 0 and therefore pushes INTO the slope,
    # opposing sliding — reservoir thrust on an upstream face is the everyday
    # case — so it enters the driving sum NEGATED. This is the same convention
    # every other method uses (the −sum_Dy term in oms/bishop, the −D·sinβ term
    # in _equilibrium_march), and line loads follow the distributed-load pattern.
    #
    # Reinforcement is applied parallel to the slice base (the flexible assumption,
    # psi = alpha), so its HORIZONTAL component is P*cos(alpha) -- matching the
    # P*sin(alpha) vertical component already used in num_N below, and matching
    # spencer's `R * cos_psi` with psi = alpha. Summing the bare magnitude here
    # over-credited the reinforcement and raised FS non-conservatively.
    horiz_ext = (np.sum(kw) + np.sum(T) - np.sum(D * sin_beta) - np.sum(LL * np.sin(ll_b))
                 - np.sum(P * cos_alpha) - np.sum(pa_cx) - np.sum(H_cos_act))

    # Iterate F: the base normal depends on F through m_alpha, exactly as Bishop.
    F = 1.0
    N_eff = None
    converged = False
    for _ in range(max_iter):
        m_alpha = cos_alpha + sin_alpha * tan_phi / F
        # Effective base normal from VERTICAL slice equilibrium (Bishop's N').
        num_N = (W + D * cos_beta + LL * np.cos(ll_b) - P * sin_alpha - pa_cy_v - H_sin_act
                 - (P_pt * sin_alpha + pp_cy_v + H_sin_pas) / F
                 - u * dl * cos_alpha - (c * dl * sin_alpha) / F)
        N_eff = num_N / m_alpha
        N_total = N_eff + u * dl
        # Horizontal force equilibrium: resisting shear (projected horizontally)
        # over driving (base-normal horizontal component + external horizontal).
        resisting = np.sum((c * dl + N_eff * tan_phi) * cos_alpha)
        # Passive support mobilizes with the soil: its horizontal components
        # reduce the driving side factored by 1/F.
        driving = (np.sum(N_total * sin_alpha) + horiz_ext
                   - (np.sum(P_pt * cos_alpha) + np.sum(pp_cx) + np.sum(H_cos_pas)) / F)
        if driving <= 0:
            return False, "Net horizontal driving force is non-positive (resisting forces exceed driving forces)."
        F_new = resisting / driving
        if abs(F_new - F) < tol:
            F = F_new
            converged = True
            break
        # Damped update: the passive-support 1/F terms on the driving side can
        # make the plain fixed-point map non-contractive (oscillating between
        # two values); the half-step converges to the same fixed point.
        F = 0.5 * (F + F_new)

    if not converged:
        return False, "Janbu method did not converge within the maximum number of iterations."

    # The converged m_alpha and base normals, tested before the correction factor
    # is applied: f0 scales the answer and cannot rescue a reversed base normal.
    janbu_reason, janbu_warns = _base_normal_admissibility(
        "Janbu's Simplified Method", N_eff,
        m_alpha=cos_alpha + sin_alpha * tan_phi / F)
    if janbu_reason:
        return False, janbu_reason

    FS_base = F

    # === Compute Janbu correction factor ===

    # Get failure surface endpoints
    x_l = slice_df['x_l'].iloc[0]   # leftmost x
    y_lt = slice_df['y_lb'].iloc[0]   # left surface endpoint (base corner; the slice
    x_r = slice_df['x_r'].iloc[-1]  # rightmost x        top sits at crest elevation
    y_rt = slice_df['y_rb'].iloc[-1]  # right surface endpoint  against a vertical face)

    # Length of failure surface (straight line approximation)
    L = np.hypot(x_r - x_l, y_rt - y_lt)

    # Calculate perpendicular distance from each slice center to failure surface line
    x0 = slice_df['x_c'].values
    y0 = slice_df['y_cb'].values

    # Distance from point to line formula: |ax + by + c| / sqrt(a² + b²)
    # Line equation: (y_rt - y_lt)x - (x_r - x_l)y + (x_r * y_lt - y_rt * x_l) = 0
    numerator_dist = np.abs((y_rt - y_lt) * x0 - (x_r - x_l) * y0 + x_r * y_lt - y_rt * x_l)
    dists = numerator_dist / L
    d = np.max(dists)  # maximum perpendicular distance

    dL_ratio = d / L

    # Determine b1 factor by overall soil type (Janbu's three correction-factor
    # curves). The classification is global by design — Janbu's chart is read
    # once for the whole surface — using a small tolerance rather than exact
    # float equality so that, e.g., a φ stored as 1e-12 still reads as φ=0.
    phi_sum = slice_df['phi'].sum()
    c_sum = slice_df['c'].sum()

    if phi_sum < 1e-9:    # c-only soil (undrained, φ = 0)
        b1 = 0.67
    elif c_sum < 1e-9:    # φ-only soil (no cohesion)
        b1 = 0.31
    else:                 # c-φ soil
        b1 = 0.50

    # Correction factor. The polynomial 1 + b1·(d/L − 1.4·(d/L)²) is a fit to
    # Janbu's correction-factor charts and is only valid up to the chart domain;
    # it peaks at d/L = 1/2.8 ≈ 0.357 and turns over (eventually < 1) beyond
    # that, which is unphysical. d/L is geometrically unbounded, so clamp it to
    # the peak: f0 saturates at its maximum rather than decreasing for very deep
    # surfaces. Typical slip surfaces have d/L well below 0.357 (the repo
    # benchmarks are ~0.13–0.20), so this only guards pathological geometries.
    DL_PEAK = 1.0 / 2.8
    dL_eff = min(dL_ratio, DL_PEAK)
    if debug and dL_ratio > DL_PEAK:
        print(f"Janbu f0: d/L = {dL_ratio:.3f} exceeds chart peak {DL_PEAK:.3f}; clamped.")
    fo = 1 + b1 * (dL_eff - 1.4 * dL_eff ** 2)

    # Final corrected factor of safety
    FS = FS_base * fo

    # Store effective normal forces in DataFrame
    slice_df['n_eff'] = N_eff

    if debug:
        print(f"FS_base (uncorrected) = {FS_base:.6f}")
        print(f"d/L ratio = {dL_ratio:.4f}")
        print(f"b1 factor = {b1:.2f}")
        print(f"fo correction = {fo:.4f}")
        print(f"FS_corrected = {FS:.6f}")
        if np.any(H_pile > 0):
            print(f"sum_pile_horizontal = {np.sum(H_cos_tp):.6f}")
        print("N_eff =", np.array2string(N_eff, precision=4, separator=', '))

    return True, {
        'method': 'janbu',
        'FS': FS,
        'fo': fo,
        'FS_base': FS_base,
        'warnings': janbu_warns,
    }


def _equilibrium_march(alpha, phi, c, w, u, dl, D, beta, kw, T, P, H_pile, theta_p, theta, FS,
                       P_pt=None, pa_cx=None, pa_cy=None, pp_cx=None, pp_cy=None,
                       H_pas=None, LL=None, ll_b=None):
    """Shared fixed-FS force-equilibrium march (left -> right over slices).

    The per-slice engine extracted from `force_equilibrium` so it can be reused:
    the force-equilibrium methods (Corps of Engineers, Lowe-Karafiath — via
    `force_equilibrium`) and, in future, Morgenstern-Price all march on it. It does
    NOT root-find FS — it evaluates ONE trial `FS` and returns the resulting base
    normals and interslice forces. Callers form their own residuals from the
    output: force closure is `Z[n]`; M-P additionally accumulates a moment residual
    from the returned `N`.

    Parameters (per-slice numpy arrays of length n; angles already in RADIANS):
        alpha, phi, c, w, u, dl  base inclination, friction, cohesion, weight,
                                 pore pressure/length, base length
        D, beta                  distributed surface load magnitude and inclination
        kw                       horizontal seismic force
        T                        tension-crack water force (nonzero only on the
                                 cracked slice)
        P                        reinforcement force (parallel to base)
        H_pile, theta_p          pile force magnitude and inclination (theta_p in
                                 RADIANS, like everything else here)
        theta                    interslice-force inclination at each BOUNDARY,
                                 length n+1 (radians)
        FS                       trial factor of safety
    Returns:
        (N, Z): N = base normal force per slice (length n, effective normal);
                Z = interslice resultant at each boundary (length n+1, Z[0] = 0).

    SIGN / RIGHT-FACING CONVENTION  ── do not forget ─────────────────────────────
    This march uses every per-slice quantity (alpha, beta, kw, T, P, ...) EXACTLY
    as passed; it performs NO internal sign flips for slope facing. Right-facing
    slopes are handled by the CALLER negating the whole `theta_list` before the
    call (see `corps` / `lowe`). Negating theta flips the sign
    of Z, which is why the tension guard back in `force_equilibrium` keys its
    Z<0 / Z>0 test on the `right_facing` flag.

    This DIFFERS from `spencer()`, which instead flips alpha, beta, psi, R, c, kw,
    V, tan_p and the pile horizontal component INTERNALLY (its `if right_facing:`
    block). Morgenstern-Price is built on THIS march, so its moment accumulator
    must follow the caller-negates-theta convention used here, NOT Spencer's
    internal-flip convention. The `f(x)=1 == Spencer` validation must therefore be
    run on a right-facing geometry specifically, to confirm the two reconcile.
    ──────────────────────────────────────────────────────────────────────────────
    """
    n = len(alpha)

    # Fully VECTORIZED march. Per slice the 2x2 gives, in closed form,
    #   Z[i+1] = (a11·b1 − a21·b0)/det   with   b0 = b0base − Z[i]·ct[i],
    #                                            b1 = b1base − Z[i]·st[i],
    # which is AFFINE in Z[i]:  Z[i+1] = p[i] + q[i]·Z[i]  (a LINEAR recurrence). A
    # linear recurrence has a closed form via cumulative products, so the whole march
    # is np.cumprod/np.cumsum — no Python loop (~2x faster than the per-slice loop,
    # and it speeds up Corps/L-K too). The multiplier q stays ~1 for physical slip
    # surfaces (cumprod magnitude ~1 even at 120 slices), so it is numerically stable;
    # we fall back to the scalar recurrence if cumprod ever goes non-finite.
    ca = np.cos(alpha); sa = np.sin(alpha)
    cb = np.cos(beta);  sb = np.sin(beta)
    ct = np.cos(theta); st = np.sin(theta)            # interslice angle, length n+1
    cp = np.cos(theta_p); sp = np.sin(theta_p)
    c_m = c / FS
    tan_phi_m = np.tan(phi) / FS

    # v12 support/load terms (zeros when not supplied). Axial reinforcement
    # mirrors the pile terms; passive support carries 1/FS (mobilizes with the
    # soil, like c_m); line loads mirror the distributed-load terms.
    z = np.zeros(n)
    P_pt  = z if P_pt  is None else P_pt
    pa_cx = z if pa_cx is None else pa_cx
    pa_cy = z if pa_cy is None else pa_cy
    pp_cx = z if pp_cx is None else pp_cx
    pp_cy = z if pp_cy is None else pp_cy
    H_pas = z if H_pas is None else H_pas
    LL    = z if LL    is None else LL
    ll_b  = z if ll_b  is None else ll_b
    h_act_cp = (H_pile - H_pas) * cp
    h_act_sp = (H_pile - H_pas) * sp
    a11 = tan_phi_m * ca - sa                          # A first column (N coefficients)
    a21 = tan_phi_m * sa + ca
    a12 = -ct[1:]; a22 = -st[1:]                       # A second column at boundary i+1
    det = a11 * a22 - a12 * a21
    b0base = (-c_m*dl*ca - P*ca - pa_cx + u*dl*sa - D*sb - LL*np.sin(ll_b) + kw + T
              - h_act_cp - (P_pt*ca + pp_cx + H_pas*cp) / FS)
    b1base = (-c_m*dl*sa - P*sa - pa_cy - u*dl*ca + w + D*cb + LL*np.cos(ll_b)
              - h_act_sp - (P_pt*sa + pp_cy + H_pas*sp) / FS)
    cti = ct[:-1]; sti = st[:-1]                       # interslice angle at boundary i

    # Z[i+1] = p[i] + q[i]·Z[i]
    p = (a11 * b1base - a21 * b0base) / det
    q = (a21 * cti - a11 * sti) / det
    Z = np.empty(n + 1)
    Z[0] = 0.0
    Pc = np.empty(n + 1)
    Pc[0] = 1.0
    np.cumprod(q, out=Pc[1:])                          # Pc[i] = prod_{j<i} q[j]
    if np.all(np.isfinite(Pc)) and np.all(Pc[1:] != 0.0):
        Z[1:] = Pc[1:] * np.cumsum(p / Pc[1:])
    else:                                              # pathological geometry → scalar scan
        for i in range(n):
            Z[i + 1] = p[i] + q[i] * Z[i]

    b0 = b0base - Z[:-1] * cti
    b1 = b1base - Z[:-1] * sti
    N = (b0 * a22 - a12 * b1) / det
    return N, Z


def _moment_about_origin(N, FS, *, x_c, y_cg, y_cb, alpha, c, phi, dl, u, w,
                         D, beta, d_x, d_y, kw, V, y_t, P, H_pile, theta_p,
                         x_pile, y_pile, P_pt=None, pa_mx=None, pa_my=None,
                         pp_mx=None, pp_my=None, H_pas=None, LL=None, ll_b=None,
                         ll_x=None, ll_y=None):
    """Moment of the WHOLE sliding mass about the origin (0,0), CCW positive.

    This is the Morgenstern-Price moment residual (plan §4a). Its root in `FS` at a
    fixed interslice-force distribution is `F_m`. The moment of a force with global
    components `(F_x, F_y)` acting at `(x, y)` is `M = x·F_y − y·F_x`.

    The interslice forces are INTERNAL: on the whole mass they cancel exactly (equal
    and opposite on each shared boundary), regardless of `λ` or the thrust line, so
    they do not appear here — that is what lets us sum about the origin without
    knowing the line of thrust.

    All angle arrays are in RADIANS. `N` is the EFFECTIVE base normal from the
    march; the total base reaction for its moment arm is `N + u·dl` (effective +
    pore uplift, plan §4a rows 2/2b), and the mobilized base shear is
    `S = (c·dl + N·tanφ)/FS`.

    Per-slice terms (summed), each straight from the §4a table:
        weight W        →  −W·x_c
        normal N′+U     →  (N + u·dl)·(x_c·cosα + y_cb·sinα)
        base shear S    →  S·(x_c·sinα − y_cb·cosα)
        surface load D  →  −D·(d_x·cosβ + d_y·sinβ)
        seismic kW      →  kW·y_cg
        tension water V →  V·y_t
        reinforcement R →  R·(x_c·sinα − y_cb·cosα)
        pile H          →  H·(x_pile·sinθ_p − y_pile·cosθ_p)

    SIGN/RIGHT-FACING: convention-agnostic — it uses whatever arrays it is given.
    Facing is handled by the caller (see `_mp_march`); this keeps the math one place.
    """
    sa, ca = np.sin(alpha), np.cos(alpha)
    sb, cb = np.sin(beta), np.cos(beta)
    S = (c * dl + N * np.tan(phi)) / FS          # mobilized base shear (N is effective)
    M = (
        -w * x_c                                  # weight (0,−W) at (x_c, y_cg)
        + (N + u * dl) * (x_c * ca + y_cb * sa)   # total normal N′+U at (x_c, y_cb)
        + S * (x_c * sa - y_cb * ca)              # base shear at (x_c, y_cb)
        - D * (d_x * cb + d_y * sb)               # surface load at (d_x, d_y)
        + kw * y_cg                               # seismic (horizontal) at y_cg
        + V * y_t                                 # tension-crack water (horiz) at y_t
        + P * (x_c * sa - y_cb * ca)              # reinforcement (∥ base) at (x_c, y_cb)
        + H_pile * (x_pile * np.sin(theta_p) - y_pile * np.cos(theta_p))  # pile
    )
    Msum = float(np.sum(M))
    # v12 terms (zeros when not supplied): axial reinforcement (components at the
    # crossing point, moment about origin = mx - my), passive support factored by
    # FS, and line loads (distributed-load pattern at their own point).
    z = np.zeros_like(x_c)
    P_pt  = z if P_pt  is None else P_pt
    pa_mx = z if pa_mx is None else pa_mx
    pa_my = z if pa_my is None else pa_my
    pp_mx = z if pp_mx is None else pp_mx
    pp_my = z if pp_my is None else pp_my
    H_pas = z if H_pas is None else H_pas
    LL    = z if LL    is None else LL
    ll_b  = z if ll_b  is None else ll_b
    ll_x  = z if ll_x  is None else ll_x
    ll_y  = z if ll_y  is None else ll_y
    Msum += float(np.sum(
        (pa_mx - pa_my)                                     # axial active
        + (pp_mx - pp_my) / FS                              # axial passive
        + P_pt * (x_c * sa - y_cb * ca) / FS                # tangent passive
        - H_pas * (x_pile * np.sin(theta_p) - y_pile * np.cos(theta_p)) * (1.0 - 1.0 / FS)
        - LL * (ll_x * np.cos(ll_b) + ll_y * np.sin(ll_b))  # line load
    ))
    return Msum


def _mp_extract(slice_df, right_facing):
    """Pull every array the M-P march needs out of the DataFrame ONCE, apply the
    right-facing flips, and return a plain dict of numpy arrays.

    Hoisting this out of the per-iteration residual avoids re-reading ~25 pandas
    columns on every Newton step — `DataFrame.__getitem__` otherwise dominates the
    M-P solve (it is read ~13× per solve, once per residual evaluation).

    RIGHT-FACING flips mirror spencer()'s internal set (alpha, beta, phi=tan_p, c, P,
    kw, V) plus the pile `theta_p -> π-θp` (flips cos θp, not sin θp) so that f(x)=1
    reduces to Spencer — validated by the f(x)=1 == Spencer gate (S3b).
    """
    n = len(slice_df)
    g = lambda col: slice_df[col].values.astype(float)
    A = dict(
        alpha=np.radians(slice_df['alpha'].values), phi=np.radians(slice_df['phi'].values),
        c=_c_eff(slice_df).astype(float), w=g('w'), u=g('u'), dl=g('dl'), D=g('dload'),
        beta=np.radians(slice_df['beta'].values), kw=g('kw'), V=g('t'), P=g('p'),
        H_pile=g('h_pile') if 'h_pile' in slice_df.columns else np.zeros(n),
        theta_p=g('theta_p') if 'theta_p' in slice_df.columns else np.zeros(n),
        x_c=g('x_c'), y_cg=g('y_cg'), y_cb=g('y_cb'),
        d_x=g('d_x'), d_y=g('d_y'), y_t=g('y_t'),
        x_pile=g('x_pile') if 'x_pile' in slice_df.columns else np.zeros(n),
        y_pile=g('y_pile') if 'y_pile' in slice_df.columns else np.zeros(n),
        # v12 support/load terms
        P_pt=g('p_pt') if 'p_pt' in slice_df.columns else np.zeros(n),
        pa_cx=g('pa_cx') if 'pa_cx' in slice_df.columns else np.zeros(n),
        pa_cy=g('pa_cy') if 'pa_cy' in slice_df.columns else np.zeros(n),
        pa_mx=g('pa_mx') if 'pa_mx' in slice_df.columns else np.zeros(n),
        pa_my=g('pa_my') if 'pa_my' in slice_df.columns else np.zeros(n),
        pp_cx=g('pp_cx') if 'pp_cx' in slice_df.columns else np.zeros(n),
        pp_cy=g('pp_cy') if 'pp_cy' in slice_df.columns else np.zeros(n),
        pp_mx=g('pp_mx') if 'pp_mx' in slice_df.columns else np.zeros(n),
        pp_my=g('pp_my') if 'pp_my' in slice_df.columns else np.zeros(n),
        H_pas=g('h_pile_pas') if 'h_pile_pas' in slice_df.columns else np.zeros(n),
        LL=g('lload') if 'lload' in slice_df.columns else np.zeros(n),
        ll_b=np.radians(g('ll_beta')) if 'll_beta' in slice_df.columns else np.zeros(n),
        ll_x=g('ll_x') if 'll_x' in slice_df.columns else np.zeros(n),
        ll_y=g('ll_y') if 'll_y' in slice_df.columns else np.zeros(n),
    )
    if right_facing:
        for k in ('alpha', 'beta', 'phi', 'c', 'P', 'kw', 'V'):
            A[k] = -A[k]
        A['theta_p'] = np.pi - A['theta_p']
        # Axial reinforcement enters in real components at real positions and
        # the stored direction (cos(psi) > 0) is the NEGATION of the real
        # tension on a right-facing slope: negate the whole vector (all sums),
        # as in spencer().
        for k in ('pa_cx', 'pa_cy', 'pa_mx', 'pa_my',
                  'pp_cx', 'pp_cy', 'pp_mx', 'pp_my'):
            A[k] = -A[k]
        # Line loads mirror beta's flip
        A['ll_b'] = -A['ll_b']
        # tangent-passive mirrors P
        A['P_pt'] = -A['P_pt']
    return A


def _mp_residuals(A, f_vals, lam, FS):
    """`(N, Z, force_res, moment_res)` from PRE-EXTRACTED arrays `A` (`_mp_extract`),
    at interslice scale λ and trial FS. No DataFrame access — this is what the
    Approach-A/B inner loops call every iteration.

    `θ_j = arctan(λ·f_vals_j)` (M-P's `tan θ = λ·f`); `force_res = Z[n]` → 0 at force
    equilibrium; `moment_res` → 0 at moment equilibrium. With `f_vals ≡ 1` this is
    Spencer (constant θ) — the make-or-break regression.
    """
    theta = np.arctan(lam * f_vals)
    N, Z = _equilibrium_march(A['alpha'], A['phi'], A['c'], A['w'], A['u'], A['dl'],
                              A['D'], A['beta'], A['kw'], A['V'], A['P'],
                              A['H_pile'], A['theta_p'], theta, FS,
                              P_pt=A['P_pt'], pa_cx=A['pa_cx'], pa_cy=A['pa_cy'],
                              pp_cx=A['pp_cx'], pp_cy=A['pp_cy'], H_pas=A['H_pas'],
                              LL=A['LL'], ll_b=A['ll_b'])
    force_res = Z[-1]
    moment_res = _moment_about_origin(
        N, FS, x_c=A['x_c'], y_cg=A['y_cg'], y_cb=A['y_cb'], alpha=A['alpha'],
        c=A['c'], phi=A['phi'], dl=A['dl'], u=A['u'], w=A['w'], D=A['D'], beta=A['beta'],
        d_x=A['d_x'], d_y=A['d_y'], kw=A['kw'], V=A['V'], y_t=A['y_t'], P=A['P'],
        H_pile=A['H_pile'], theta_p=A['theta_p'], x_pile=A['x_pile'], y_pile=A['y_pile'],
        P_pt=A['P_pt'], pa_mx=A['pa_mx'], pa_my=A['pa_my'], pp_mx=A['pp_mx'],
        pp_my=A['pp_my'], H_pas=A['H_pas'], LL=A['LL'], ll_b=A['ll_b'],
        ll_x=A['ll_x'], ll_y=A['ll_y'])
    return N, Z, force_res, moment_res


def _mp_march(slice_df, lam, f_vals, FS, right_facing=False):
    """Morgenstern-Price march for a single `(λ, FS)`: extract arrays then evaluate.

    Thin wrapper over `_mp_extract` + `_mp_residuals`, kept for direct/standalone
    callers (tests, gates). The solver itself extracts ONCE and calls
    `_mp_residuals` in the loop. Returns `(N, Z, force_res, moment_res)`.
    """
    n = len(slice_df)
    f_vals = np.asarray(f_vals, dtype=float)
    if len(f_vals) != n + 1:
        raise ValueError(f"f_vals length ({len(f_vals)}) must be n+1 ({n+1})")
    return _mp_residuals(_mp_extract(slice_df, right_facing), f_vals, lam, FS)


def interslice_tension_note(Z):
    """The interslice-tension state of an accepted solution, as one note or None.

    ONE RULE, for spencer, mprice, corps and lowe alike.

    MEASURE — the fraction of INTERIOR slice boundaries (j = 1 … n-1; the two end
    boundaries carry no force by definition) whose interslice resultant is
    tensile, with ``Z`` in the physical convention (tension < 0). The measure is
    only defined on a MIXED field: where every interior boundary carries the same
    sign the fraction saturates at 0 or 1, the sign convention itself is what is
    being read, and no verdict is offered.

    THRESHOLD — any tension at all. Soil carries no tension, so a tensile
    interslice resultant is already a departure from the Mohr-Coulomb model the
    method was solved with. No larger number has a source. Duncan & Wright treat
    interslice tension as a check the engineer makes on a reported solution;
    SLOPE/W reports its interslice forces and flags the negative ones; Slide2 and
    RS2 impose no such test at all.

    CONSEQUENCE — report. The factor of safety is never decided by this measure,
    and no solution is ever refused for it, because across the shipped corpus the
    measure carries no information about whether a factor of safety is right:

      * the tension-crack sample (docs/lem/files/xslope_tension_KEY.xlsx) run with
        its crack removed — the crest tension a crack exists to remove — reports
        10% and its factor of safety is 8% HIGH (4.960 against 4.588 with the
        crack modeled);
      * GS-2.26's toe plane reports 69-71% on all four methods and every one of
        them returns 1.35199772881, which is SLOPE/W's own answer on the same
        plane;
      * the tutorial embankment's phi = 0 circles report 26-36% across a smooth
        family, and every solution in it — reported and refused alike — returns
        Bishop's exact phi = 0 moment factor of safety to four decimals, since at
        phi = 0 moment equilibrium fixes the answer whatever the interslice
        forces do;
      * VP47, VP48 and VP60 report 100% and all four methods agree with each
        other and with the vendor.

    So the case that most needs the engineer's attention sits lowest on the
    measure and the highest readings are all correct: any refusal threshold is
    anti-correlated with correctness. What IS refused is base tension by extent
    (MAX_BASE_TENSION_EXTENT) and a non-positive factor of safety — quantities
    that contradict the strength model rather than describe the internal forces.
    """
    Z = np.asarray(Z, dtype=float)
    Z_int = Z[1:-1]
    if Z_int.size == 0:
        return None
    tensile = Z_int < 0
    if not tensile.any() or not (Z_int > 0).any():
        return None
    z_min = float(np.min(Z_int))
    z_max = float(np.max(Z_int))
    return (f"interslice tension on {float(tensile.mean()):.0%} of interior "
            f"boundaries (min Z = {z_min:.1f} vs max compression {z_max:.1f})")


def _admissibility_warnings(c, N_eff, Z, y_lt=None, y_lb=None, yt_l=None):
    """Report-only admissibility screen shared by spencer/mprice/corps/lowe.

    Returns a list of Duncan & Wright admissibility notes for an ALREADY-ACCEPTED
    solution — it never affects FS, convergence, or acceptance. Spencer's base
    tension gate normalizes by cohesive capacity, so a c=0 slice can carry
    unbounded base tension without tripping it (VP30: -71 kN/m on the
    cohesionless crack-face sliver scores 0.0 and passes), and the extent gate
    force_equilibrium and mprice apply misses the same slice. The first note
    below reports what those cannot see:
      - base tension only on COHESIONLESS slices (the guard's blind spot);
      - interslice tension by :func:`interslice_tension_note`, the one measure
        all four methods report from;
      - thrust line outside the slice on >10% of interior boundaries, with
        NaN/inf ratios counting as outside — skipped when no thrust line is
        supplied (corps/lowe expose no line of thrust).

    Z must arrive in the physical convention (tension < 0); callers whose march
    stores the opposite sign negate it before passing it in.
    """
    warns = []
    c = np.asarray(c, dtype=float)
    N_eff = np.asarray(N_eff, dtype=float)
    Z = np.asarray(Z, dtype=float)
    n_scale = float(np.max(np.abs(N_eff))) if len(N_eff) else 0.0
    cohesionless = np.abs(c) <= 1e-9
    bad_n = np.flatnonzero(cohesionless & (N_eff < -0.01 * n_scale))
    if bad_n.size:
        worst = int(bad_n[np.argmin(N_eff[bad_n])])
        warns.append(f"base tension on {bad_n.size} cohesionless slice(s), "
                     f"worst N' = {float(N_eff[worst]):.1f} at slice {worst + 1}")
    note = interslice_tension_note(Z)
    if note:
        warns.append(note)
    if yt_l is not None and y_lt is not None and y_lb is not None:
        frac_out = _thrust_outside_fraction(y_lt, y_lb, yt_l)
        if frac_out > 0.10:
            warns.append(f"line of thrust outside the slice on {frac_out:.0%} "
                         f"of boundaries")
    return warns


def _base_normal_admissibility(method_name, N_eff, m_alpha=None):
    """Whether a simplified method's converged answer is a state of the mass.

    The Ordinary, Bishop and Janbu methods each converge on a single factor of
    safety and, until this test, reported it whatever the base normals underneath
    it had done. Two things can have gone wrong, and they are the two the
    force-equilibrium closure already tests for:

    * Bishop and Janbu divide every slice's base normal by
      ``m_alpha = cos(alpha) + sin(alpha) tan(phi) / F``, which vanishes at
      ``tan(alpha) = -F / tan(phi)``. Past that inclination m_alpha is negative,
      the base normal has reversed, and the "solution" is the far side of a
      singularity rather than a slower slide. On `xslope_noncircular`'s deep
      surface four of forty-one slices sit past it, m_alpha reaches -0.2507, the
      least base normal is -963.6, and Janbu reports 0.8152 where Spencer reads
      4.3825 on the identical slices. The bar is `FE_MIN_BASE_FACTOR`, the same
      one the force-equilibrium closure keeps its own base factor clear of; the
      corpus's own answers stay five times above it. The Ordinary method's normal
      does not divide by m_alpha and is not tested on it.
    * A base in tension mobilizes no Mohr-Coulomb strength, so past
      `MAX_BASE_TENSION_EXTENT` of the slices the answer contradicts the strength
      model it was solved with over most of the surface. Below that extent it is
      reported and not refused, exactly as `force_equilibrium` and `mprice` treat
      it. No accepted corpus answer carries any.

    Returns ``(reason, warnings)``: `reason` is a refusal message when the answer
    is not admissible and None when it is, and `warnings` are the report-only
    notes to carry on the results dict.
    """
    N_eff = np.asarray(N_eff, dtype=float)
    n = N_eff.size
    if not n:
        return None, []
    if m_alpha is not None:
        m_alpha = np.asarray(m_alpha, dtype=float)
        min_m = float(m_alpha.min())
        if min_m < FE_MIN_BASE_FACTOR:
            past = int(np.count_nonzero(m_alpha < FE_MIN_BASE_FACTOR))
            return (f"{method_name}{SIMPLIFIED_INADMISSIBLE}"
                    f"(m_alpha down to {min_m:.4f} on {past} of {n} slices, so the "
                    f"base normal has passed through its own singularity; least "
                    f"N' = {float(N_eff.min()):.1f})"), []
    tension = N_eff < 0
    frac = float(tension.mean())
    if frac > MAX_BASE_TENSION_EXTENT:
        return (f"{method_name}{SIMPLIFIED_INADMISSIBLE}"
                f"({100 * frac:.0f}% of base normals in tension)"), []
    if frac > 0:
        worst = int(np.argmin(N_eff))
        return None, [f"base tension on {int(tension.sum())} of {n} slices "
                      f"(worst N' = {float(N_eff[worst]):.1f} at slice {worst + 1})"]
    return None, []


def spencer_theta_bounds(alpha, tan_p, F_val, margin_deg=5.0):
    """The pole-free band of interslice inclinations for one slice set and F.

    Spencer's equations divide every slice by
    ``m_alpha = 1 / [cos(alpha - theta) + sin(alpha - theta) tan(phi) / F]``.
    Writing the denominator as ``sqrt(1 + k^2) cos(alpha - theta - arctan(k))``
    with ``k = tan(phi)/F``, it keeps its sign exactly while
    ``|alpha_i - theta - arctan(k_i)| < pi/2`` on every slice, which gives the
    band returned here. Outside it a slice's base normal has reversed, so a root
    found there is a discontinuity of the equations rather than a state of the
    mass.

    This is the geometric bound Spencer (1973) and Duncan & Wright describe — the
    interslice inclination lies between the inclinations of the ground surface and
    the slip surface — in the form the equations give, and it is Spencer's
    counterpart of the base factor `FE_MIN_BASE_FACTOR` keeps clear of zero for
    the force-equilibrium closure. `alpha` and `tan_p` arrive in the solver's
    own frame (both negated on a right-facing slope).

    `margin_deg` narrows the band at both ends, which is what keeps an iteration
    off the poles; the acceptance test uses the band itself, at margin 0. Module
    level rather than a closure so a check can replace it.
    """
    margin = np.radians(margin_deg)
    offset = np.asarray(alpha, dtype=float) - np.arctan(
        np.asarray(tan_p, dtype=float) / F_val)
    lo = float(np.max(offset)) - np.pi / 2 + margin
    hi = float(np.min(offset)) + np.pi / 2 - margin
    if lo >= hi:
        lo, hi = -np.pi / 2, np.pi / 2      # fallback if no valid range
    return max(lo, -np.pi / 2), min(hi, np.pi / 2)


def force_equilibrium(slice_df, theta_list, tol=1e-6, max_iter=50, debug=False, right_facing=False):
    """
    Limit‐equilibrium by force equilibrium in X & Y with variable interslice angles.

    Parameters:
        slice_df (pd.DataFrame): must contain columns
            'alpha' (slice base inclination, degrees),
            'phi'   (slice friction angle, degrees),
            'c'     (cohesion),
            'dl'    (slice base length),
            'w'     (slice weight),
            'u'     (pore force per unit length),
            'dload' (distributed load),
            'beta'  (distributed load inclination, degrees),
            'kw'    (seismic force),
            't'     (tension crack water force),
            'p'     (reinforcement force),
            'h_pile' (pile force, optional), 'theta_p' (pile inclination, RADIANS, optional)
        theta_list (array-like): slice‐boundary force inclinations (degrees),
                                 length must be n+1 if there are n slices
        tol, max_iter: accepted for backward compatibility; the root is now
                       bracketed rather than iterated from a seed, so neither is
                       used (see `_force_closure_root`)
        debug (bool): print residuals during iteration

    Returns:
        (bool, dict or str):
           - If solved: (True, {'FS': <value>, 'warnings': [...]})
           - If failed: (False, "error message")

    The closure `Z[n](FS) = 0` has several roots on many surfaces; which one is
    reported is decided by `_force_closure_root`, and any others are named in
    `warnings`.
    """
    import numpy as np

    n = len(slice_df)
    if len(theta_list) != n+1:
        return False, f"theta_list length ({len(theta_list)}) must be n+1 ({n+1})"

    residual, N, Z, det, poles = _force_closure(slice_df, theta_list, right_facing)

    if debug:
        r0 = residual(1.5)
        print(f"FS_guess=1.500000 → residual={r0:.4g}")

    FS_opt, root_notes = _force_closure_root(residual, Z, N, det, poles, slice_df)
    if FS_opt is None:
        return False, root_notes

    # A non-positive factor of safety is unphysical. The scan only admits roots
    # above FE_FS_MIN, so this is a belt-and-braces check on the returned root.
    if not np.isfinite(FS_opt) or FS_opt <= 0:
        return False, f"force_equilibrium: non-physical factor of safety ({FS_opt})"

    # Re-evaluate at the root so N and Z hold the values at FS_opt.
    residual(FS_opt)

    # Admissibility guard. A free search can drive the force-equilibrium solver onto
    # grossly non-physical surfaces and report a spurious low FS. What is refused is
    # base tension by EXTENT — a few negative base normals occur in valid solutions
    # and are not rejected, but past half the slices the solution contradicts the
    # Mohr-Coulomb strength it was solved with over most of the surface. Interslice
    # tension is reported below and never refused; see interslice_tension_note.
    frac_N_neg = float(np.mean(N < 0)) if n else 0.0
    if frac_N_neg > MAX_BASE_TENSION_EXTENT:
        return False, (FORCE_EQ_INADMISSIBLE +
                       f"({100*frac_N_neg:.0f}% of base normals in tension)")

    slice_df['n_eff'] = N  # store effective normal forces in slice_df
    slice_df['z'] = Z[:-1]  # store interslice forces in slice_df, adjust length to n slices

    # Report-only admissibility screen (corps/lowe inherit it), carrying the same
    # interslice-tension measure spencer and mprice report. The parallel-force
    # march exposes no line of thrust, so only the base-tension and interslice-
    # tension signatures apply; the third is skipped. On right-facing slopes the
    # caller negates theta_list, flipping Z's sign, so tension there is Z>0 — pass
    # the physical-convention Z (tension < 0) the helper expects.
    Z_phys = -Z if right_facing else Z
    warns = _admissibility_warnings(_c_eff(slice_df), N, Z_phys)
    warns.extend(root_notes)

    if debug:
        r_opt = residual(FS_opt)
        print(f" Converged FS = {FS_opt:.6f}, residual = {r_opt:.4g}")

    return True, {'FS': FS_opt, 'warnings': warns}


def _force_closure(slice_df, theta_list, right_facing=False):
    """Build the force-closure residual `Z[n](FS)` for one slice set.

    Extracted from `force_equilibrium` so the root finder, the diagnostics and the
    checks all evaluate the same closure. Returns `(residual, N, Z, det, poles)`: calling
    `residual(FS)` marches the slices at that trial factor of safety, fills the
    persistent `N` (effective base normals), `Z` (interslice resultants at each
    boundary, `Z[0] = 0`) and `det` (the per-slice base factor) arrays in place, and
    returns the right-end interslice force, whose root in `FS` is the
    force-equilibrium solution. `poles` are the factors of safety at which the base
    factor vanishes, in closed form.
    """
    n = len(slice_df)

    # extract and convert to radians
    alpha   = np.radians(slice_df['alpha'].values)
    phi     = np.radians(slice_df['phi'].values)
    c       = _c_eff(slice_df)
    w       = slice_df['w'].values
    u       = slice_df['u'].values
    dl      = slice_df['dl'].values
    D       = slice_df['dload'].values
    beta    = np.radians(slice_df['beta'].values)
    kw      = slice_df['kw'].values
    T       = slice_df['t'].values
    P       = slice_df['p'].values
    theta   = np.radians(np.asarray(theta_list))

    # Pile forces (backward compatible — zeros if no pile data)
    H_pile  = slice_df['h_pile'].values  if 'h_pile'  in slice_df.columns else np.zeros(n)
    theta_p = slice_df['theta_p'].values if 'theta_p' in slice_df.columns else np.zeros(n)

    # v12 support/load terms (all zero when the columns are absent)
    def _c12(name):
        return slice_df[name].values.astype(float) if name in slice_df.columns else np.zeros(n)
    P_pt  = _c12('p_pt')
    pa_cx = _c12('pa_cx'); pa_cy = _c12('pa_cy')
    pp_cx = _c12('pp_cx'); pp_cy = _c12('pp_cy')
    H_pas = _c12('h_pile_pas')
    LL    = _c12('lload')
    ll_b  = np.radians(_c12('ll_beta'))
    # The march mixes the orientation-normalized frame (alpha, theta) with the
    # stored axial components (normalized to cos(psi) > 0). The horizontal
    # component enters as a resisting magnitude (facing-agnostic), but the real
    # tension on a right-facing slope is the negation of the stored direction,
    # so its VERTICAL component flips (same correction as janbu()).
    if right_facing:
        pa_cy = -pa_cy
        pp_cy = -pp_cy

    N = np.zeros(n)  # normal forces on slice bases (filled by each march)
    Z = np.zeros(n+1)  # interslice forces, Z[0] = 0 by definition (no force entering leftmost slice)
    # The march's base factor, the force-equilibrium counterpart of Bishop's
    # m_alpha: the 2x2 determinant per slice reduces to
    #   det_i = cos(alpha_i - theta_{i+1}) + tan(phi_i)/FS * sin(alpha_i - theta_{i+1}),
    # so it is a closed-form function of the trial factor of safety. Where it
    # passes through zero the recurrence has a pole, and the closure a spurious
    # sign change; `_force_closure_root` reads it to reject those.
    d_ang = alpha - theta[1:]
    cos_d, sin_d = np.cos(d_ang), np.sin(d_ang)
    tan_phi = np.tan(phi)
    det = np.zeros(n)
    # Where each slice's base factor vanishes, in closed form: det_i = 0 at
    # FS = -tan(phi_i) * tan(alpha_i - theta_{i+1}). The scan is cut at these so
    # that every bracket it forms holds at most one pole, and a root wedged
    # between two close poles cannot fall through the grid.
    with np.errstate(divide='ignore', invalid='ignore'):
        poles = -tan_phi * np.tan(d_ang)
    poles = np.sort(poles[np.isfinite(poles) & (poles > 0.0)])

    def residual(FS):
        """Right-side interslice force Z[n] for a given FS (force-closure residual).

        Delegates the per-slice march to the shared `_equilibrium_march`, then
        copies its output into the persistent N/Z arrays (via slice assignment) so
        the admissibility check and the slice_df writes after the root-find see the
        values at the converged FS. Pure extraction — arithmetic is unchanged.
        """
        N_march, Z_march = _equilibrium_march(
            alpha, phi, c, w, u, dl, D, beta, kw, T, P, H_pile, theta_p, theta, FS,
            P_pt=P_pt, pa_cx=pa_cx, pa_cy=pa_cy, pp_cx=pp_cx, pp_cy=pp_cy,
            H_pas=H_pas, LL=LL, ll_b=ll_b)
        N[:] = N_march
        Z[:] = Z_march
        det[:] = cos_d + tan_phi / FS * sin_d
        return Z[n]

    return residual, N, Z, det, poles


def _force_closure_root(residual, Z, N, det, poles, slice_df):
    """Bracket every root of the force-closure residual and return the physical one.

    `residual(F)` is `Z[n]`, the interslice force left over at the right end of the
    march. Its root in `F` is the force-equilibrium factor of safety — but the march
    is a linear recurrence whose per-slice determinant
    ``cos(alpha - theta) + tan(phi)/F * sin(alpha - theta)`` vanishes at
    ``F = -tan(phi) * tan(alpha - theta)``, so on any surface with obtuse
    ``alpha - theta`` the residual has poles, and a root of its own between each
    consecutive pair. A single-guess secant lands on whichever of them it happens to
    reach, which on some surfaces is a branch where the interslice forces run to
    hundreds of times the weight of the sliding mass.

    The window ``[FE_FS_MIN, FE_FS_MAX]`` is scanned, every sign change is bracketed
    with `brentq`, and each bracketed value is tested against three measures:

    * the base factor stays clear of zero (`FE_MIN_BASE_FACTOR`) — a root sitting on
      a pole is a discontinuity in the closure rather than a state of the mass, and
      the march that produced it is ill-conditioned;
    * the largest interslice resultant stays within `FE_MAX_Z_OVER_W` times the
      total driving load on the sliding mass (`_driving_load`) — bounded interslice
      forces, no boundary carrying more than everything driving the mass;
    * base tension does not saturate (`MAX_BASE_TENSION_EXTENT`, the same extent
      test the caller applies to the returned solution).

    The moment-equilibrium answer on the same slices — Bishop's method on a
    circular surface, Spencer's otherwise — is then solved once and used twice: a
    root standing more than `FE_MAX_BELOW_MOMENT` below it is refused, since that
    is what the spurious branch does even where it looks clean on the three
    measures above, and among the roots that remain the one nearest it is returned,
    nearness measured as a ratio since a factor of safety is one. The screen is
    one-sided: these methods read above the moment answer by construction. Where
    the reference does not solve, the smallest surviving root is returned. The
    roots that were passed over are named in `results['warnings']` with the measure
    each failed. When no root passes, the failure says so; no other method's factor
    of safety is ever substituted.

    Returns `(FS, warnings)` on success and `(None, message)` when no root passes.
    """
    from scipy.optimize import brentq

    # The load the interslice forces are judged against: the mass's own weight
    # plus every load applied to it. On a bearing-capacity section built at a
    # nominal unit weight the weight alone is numerically zero, and no root could
    # pass a test divided by it. See `_driving_load`.
    load_sum = _driving_load(slice_df)
    scale = load_sum if load_sum > 0 else 1.0

    # A uniform sweep of the window, cut either side of every pole so that no
    # bracket spans one and no root between two close poles is stepped over.
    edge = 1e-7 * (FE_FS_MAX - FE_FS_MIN)
    inside = poles[(poles > FE_FS_MIN + edge) & (poles < FE_FS_MAX - edge)]
    grid = np.unique(np.concatenate([
        np.linspace(FE_FS_MIN, FE_FS_MAX, FE_FS_SCAN),
        inside - edge, inside + edge]))
    at_pole = np.isin(grid, inside - edge)      # bracket [g, g+1] holds a pole
    vals = np.empty(grid.size)
    for i, F in enumerate(grid):
        try:
            vals[i] = residual(float(F))
        except Exception:
            vals[i] = np.nan

    brackets = []
    for i in range(grid.size - 1):
        a, b = vals[i], vals[i + 1]
        if not (np.isfinite(a) and np.isfinite(b)):
            continue
        if a == 0.0:
            brackets.append(float(grid[i]))
        elif a * b < 0.0 and not at_pole[i]:
            try:
                brackets.append(float(brentq(residual, grid[i], grid[i + 1],
                                             xtol=1e-9, maxiter=100)))
            except Exception:
                pass
    if np.isfinite(vals[-1]) and vals[-1] == 0.0:
        brackets.append(float(grid[-1]))

    admissible, rejected = [], []
    for r in brackets:
        try:
            res_r = residual(r)
        except Exception:
            continue
        min_det = float(np.abs(det).min()) if len(det) else 1.0
        max_Z = float(np.abs(Z).max())
        frac_neg = float(np.mean(N < 0)) if len(N) else 0.0
        if not np.isfinite(res_r):
            rejected.append((r, "the march does not close here"))
        elif min_det < FE_MIN_BASE_FACTOR:
            rejected.append((r, f"base factor {min_det:.3f}"))
        elif max_Z > FE_MAX_Z_OVER_W * load_sum:
            rejected.append((r, f"interslice force {max_Z / scale:.0f}x the "
                                f"load on the mass"))
        elif frac_neg > MAX_BASE_TENSION_EXTENT:
            rejected.append((r, f"{100 * frac_neg:.0f}% of bases in tension"))
        else:
            admissible.append(r)

    # The moment-equilibrium answer on the same slices — Bishop's method on a
    # circular surface, Spencer's otherwise. It does two jobs: it screens out a
    # root that stands far below it, and it breaks the tie among the roots that
    # survive. Solved once, and only when there is something left to judge.
    ref = None
    if admissible:
        ref_method = bishop if _has_circle_center(slice_df) else spencer
        try:
            ok_r, res_r = ref_method(slice_df.copy())
            if ok_r and np.isfinite(res_r['FS']) and res_r['FS'] > 0:
                ref = float(res_r['FS'])
        except Exception:
            ref = None

    # A root that reads far BELOW the moment answer is the spurious branch, even
    # where it looks clean on the three measures above: on the eight-layer slope's
    # grid-seeded Corps critical the surviving root is 0.121 against Bishop's
    # 9.115, on a march whose base factor never falls under 0.94 and whose side
    # forces stay at 0.72 of the load. Reading far ABOVE is not the same thing and
    # is not screened; see FE_MAX_BELOW_MOMENT.
    if ref is not None and admissible:
        kept = []
        for r in admissible:
            if r * FE_MAX_BELOW_MOMENT < ref:
                rejected.append((r, f"{ref / r:.0f}x below the moment factor of "
                                    f"safety ({ref:.3f}) on these slices"))
            else:
                kept.append(r)
        admissible = kept

    named = ", ".join(f"FS={r:.3f} ({why})" for r, why in sorted(rejected))
    if not admissible:
        if rejected:
            return None, (FORCE_EQ_NO_ADMISSIBLE_ROOT + f"; rejected {named}")
        return None, (FORCE_EQ_NO_ROOT +
                      f"{FE_FS_MIN:g} to {FE_FS_MAX:g}")

    FS_opt = admissible[0]
    if len(admissible) > 1:
        if ref is not None:
            # Distance measured as a RATIO, not a difference: a factor of safety is
            # strength over demand, so a root at a fifth of the moment answer is
            # further from it than one at twice, and an arithmetic distance calls
            # those two a tie.
            FS_opt = min(admissible, key=lambda r: (abs(np.log(r / ref)), r))
        else:
            FS_opt = min(admissible)

    warns = []
    passed_over = [f"FS={r:.3f} (admissible)" for r in sorted(admissible) if r != FS_opt]
    passed_over += [f"FS={r:.3f} ({why})" for r, why in sorted(rejected)]
    if passed_over:
        warns.append("force closure has other roots on these slices: "
                     + "; ".join(passed_over))
    return FS_opt, warns


def corps(slice_df, variant=2, debug=False):
    """
    Corps of Engineers (Modified Swedish) force-equilibrium solver.

    The interslice forces are assumed parallel at an inclination set by one of the
    two standard Corps conventions (USACE EM 1110-2-1902). Both are offered by
    commercial codes (e.g. SLOPE/W "Corps of Engineers #1/#2"):

      variant=1: a single constant θ = inclination of the line from the bottom to
                 the top of the failure surface (the crest-to-toe chord).
      variant=2 (default): θ at each slice boundary parallel to the GROUND SURFACE
                 (slice top).

    Variant 2 is the default because it is robust under an unconstrained
    search (variant 1 uses one fixed θ everywhere and can return a spuriously
    low FS on surfaces with steep segments, which a self-search exploits).
    Note that variant 2 is NOT the conservative choice: the ground-parallel
    convention systematically gives the HIGHEST (least conservative) factor of
    safety among XSLOPE's methods — typically a few percent to ~15% above
    Spencer — and the USACE manual itself notes the "average embankment slope"
    assumption can be unconservative. Report a rigorous method (Spencer) for
    design; use Corps for comparison.

    Both Corps conventions and Lowe & Karafiath set the inter-slice inclination
    from the signed ground/base slope and negate it on right-facing slopes, so
    the force-equilibrium factor of safety is mirror-symmetric.

    Parameters:
        slice_df (pd.DataFrame): Must include ['x_l','y_lt','x_r','y_rt'] plus all
                           columns required by force_equilibrium.
        variant (int): 1 = crest-to-toe chord, 2 = per-slice ground-parallel.

    Returns:
        Tuple(bool, dict or str): Whatever force_equilibrium returns.
    """
    n = len(slice_df)

    if variant == 1:
        # endpoints of the slip surface -> one constant θ
        x0, y0 = slice_df['x_l'].iat[0], slice_df['y_lb'].iat[0]
        x1, y1 = slice_df['x_r'].iat[-1], slice_df['y_rb'].iat[-1]
        dx = x1 - x0
        dy = y1 - y0
        if abs(dx) < 1e-12:
            theta_deg = 90.0
        else:
            theta_deg = np.degrees(np.arctan2(dy, dx))  # signed crest-to-toe chord
        theta_list = np.full(n+1, theta_deg)
        theta_out = theta_deg
    else:
        # per-boundary θ parallel to the ground surface (slice top)
        x_l = slice_df['x_l'].values
        y_lt = slice_df['y_lt'].values
        x_r = slice_df['x_r'].values
        y_rt = slice_df['y_rt'].values
        slope_top = (y_rt - y_lt) / (x_r - x_l)   # signed ground-surface slope per slice
        theta_list = np.zeros(n+1)
        for j in range(n+1):
            if j == 0:
                s = slope_top[0]
            elif j == n:
                s = slope_top[-1]
            else:
                s = 0.5*(slope_top[j-1] + slope_top[j])
            theta_list[j] = np.degrees(np.arctan(s))
        theta_out = float(np.mean(theta_list))

    # The force-equilibrium engine marches slices left→right with a hard-coded
    # sliding sense (Z[0]=0 at the left). On a right-facing slope the signed
    # ground/chord slope carries the wrong sign for that march, so the
    # inter-slice inclinations are negated — the same convention lowe
    # uses. This is a no-op for left-facing slopes (the common case and every
    # shipped benchmark). Without it, force-equilibrium FS is asymmetric under
    # mirroring and can violate the expected method ordering on right-facing
    # geometries.
    # Explicit facing (flat-arc / override) wins; else historical test, byte-identical.
    right_facing = slice_df.attrs.get(
        'right_facing', slice_df['y_lb'].iat[0] > slice_df['y_rb'].iat[-1])
    if right_facing:
        theta_list = -theta_list
        theta_out = -theta_out

    slice_df['theta'] = theta_list[:-1]  # store theta in slice_df. Adjust length to n slices.

    # delegate to your force_equilibrium solver
    success, results = force_equilibrium(slice_df, theta_list, debug=debug, right_facing=right_facing)
    if not success:
        return success, results
    else:
        results['method'] = 'corps'  # append method
        results['theta'] = theta_out           # append theta (mean for variant 2)
        return success, results

def lowe(slice_df, debug=False):
    """
    Lowe-Karafiath limit equilibrium: variable interslice inclinations equal to
    the average of the top‐and bottom‐surface slopes of the two adjacent slices
    at each boundary.
    """
    n = len(slice_df)

    # grab boundary coords
    x_l = slice_df['x_l'].values
    y_lt = slice_df['y_lt'].values
    y_lb = slice_df['y_lb'].values
    x_r = slice_df['x_r'].values
    y_rt = slice_df['y_rt'].values
    y_rb = slice_df['y_rb'].values

    # determine facing (explicit flat-arc / override wins; else historical test)
    right_facing = slice_df.attrs.get('right_facing', (y_lb[0] > y_rb[-1]))

    # precompute each slice's top & bottom slopes
    widths   = (x_r - x_l)
    slope_top    = (y_rt - y_lt) / widths
    slope_bottom = (y_rb - y_lb) / widths

    # build θ_list for j=0..n
    if debug:
        print("boundary slopes (top/bottom) avg, θ_list:")  # header for debug list

    theta_list = np.zeros(n+1)
    for j in range(n+1):
        if j == 0:
            st = slope_top[0]
            sb = slope_bottom[0]
        elif j == n:
            st = slope_top[-1]
            sb = slope_bottom[-1]
        else:
            st = 0.5*(slope_top[j-1] + slope_top[j])
            sb = 0.5*(slope_bottom[j-1] + slope_bottom[j])

        avg_slope = 0.5*(st + sb)
        theta = np.degrees(np.arctan(avg_slope))

        # sign convention
        if right_facing:
            theta_list[j] =  -theta
        else:
            theta_list[j] = theta

        if debug:
            print(f"  j={j:2d}: st={st:.3f}, sb={sb:.3f}, θ={theta:.3f}°")

    slice_df['theta'] = theta_list[:-1]  # store theta in slice_df. Adjust length to n slices.

    # call your force_equilibrium solver
    success, results = force_equilibrium(slice_df, theta_list, debug=debug, right_facing=right_facing)
    if not success:
        return success, results
    else:
        results['method'] = 'lowe'  # append method
        return success, results

def spencer(slice_df, tol=1e-4, max_iter = 100, debug_level=0, residual_hook=None,
            existence_test=True, fs_seed=None, theta_seed=None):
    """
    Spencer's Method using Steve G. Wright's formulation from the UTEXAS v2  user manual.


    Parameters:
        slice_df (pd.DataFrame): must contain columns
            'alpha' (slice base inclination, degrees),
            'phi'   (slice friction angle, degrees),
            'c'     (cohesion),
            'dl'    (slice base length),
            'w'     (slice weight),
            'u'     (pore force per unit length),
            'dload' (distributed load),
            'beta'  (distributed load inclination, degrees),
            'kw'    (seismic force),
            't'     (tension crack water force),
            'p'     (reinforcement force),
            'y_lt'  (left-top y, used with 'y_lb' by the report-only
                     admissibility screen for the thrust-line check),
            'h_pile' (pile force, optional), 'theta_p' (pile inclination, RADIANS, optional)

        residual_hook (callable, optional): handed ``compute_residuals`` — the
            function whose two zeros ARE the solution — as soon as this surface's
            force and moment terms are assembled, and before anything is solved.
            Nothing in the solve reads it back; it exists so a check can compare a
            closed form against the equations the solver actually solves, on the
            solver's own numbers rather than a second transcription of them (see
            test/spencer_disclosure_check.py).
        existence_test (bool, default True): whether the exact phi = 0 test may
            refuse a surface before the retry cascade runs. Setting it False
            spends the full cascade on every surface, which is how a check proves
            the refusal is inert — the cascade must reach no solution the solver
            would accept on any surface the test refuses. Nothing in the package
            passes False; it exists for that proof.

    Returns:
        float: FS where FS_force = FS_moment
        float: beta (degrees)
        bool: converged flag
        The results dict also carries 'warnings': a list of admissibility
        notes (base tension on cohesionless slices, interslice tension,
        thrust line outside the slices) — empty when the solution is clean.
        Warnings never affect FS or convergence.
    """

    alpha = np.radians(slice_df['alpha'].values)  # slice base inclination, degrees
    phi   = np.radians(slice_df['phi'].values)  # slice friction angle, degrees  
    c     = _c_eff(slice_df)  # cohesion (+ apparent cohesion from matric suction, if any)
    dx    = slice_df['dx'].values  # slice width
    dl    = slice_df['dl'].values  # slice base length
    W     = slice_df['w'].values  # slice weight
    u     = slice_df['u'].values  # pore presssure
    x_c   = slice_df['x_c'].values  # center of base x-coordinate
    y_cb  = slice_df['y_cb'].values  # center of base y-coordinate
    y_lb   = slice_df['y_lb'].values  # left side base y-coordinate
    y_rb   = slice_df['y_rb'].values  # right side base y-coordinate
    P     = slice_df['dload'].values  # distributed load resultant 
    beta  = np.radians(slice_df['beta'].values)  # distributed load inclination, degrees
    kw    = slice_df['kw'].values  # seismic force
    V     = slice_df['t'].values  # tension crack water force
    y_v   = slice_df['y_t'].values  # tension crack water force y-coordinate
    R     = slice_df['p'].values  # reinforcement force

    # Pile forces (backward compatible — zeros if no pile data)
    n_slices = len(slice_df)
    H_pile    = slice_df['h_pile'].values  if 'h_pile'  in slice_df.columns else np.zeros(n_slices)
    theta_pile = slice_df['theta_p'].values if 'theta_p' in slice_df.columns else np.zeros(n_slices)
    x_pile    = slice_df['x_pile'].values  if 'x_pile'  in slice_df.columns else np.zeros(n_slices)
    y_pile    = slice_df['y_pile'].values  if 'y_pile'  in slice_df.columns else np.zeros(n_slices)

    # v12 support/load terms (all zero when the columns are absent)
    def _c12(name):
        return slice_df[name].values.astype(float) if name in slice_df.columns else np.zeros(n_slices)
    pa_cx = _c12('pa_cx'); pa_cy = _c12('pa_cy')
    pa_mx = _c12('pa_mx'); pa_my = _c12('pa_my')
    pp_cx = _c12('pp_cx'); pp_cy = _c12('pp_cy')
    pp_mx = _c12('pp_mx'); pp_my = _c12('pp_my')
    P_pt  = _c12('p_pt')
    H_pas = _c12('h_pile_pas')
    LL    = _c12('lload')
    ll_b  = np.radians(_c12('ll_beta'))
    ll_x  = _c12('ll_x'); ll_y = _c12('ll_y')

    # psi/x_r/y_r below carry the TANGENT-direction reinforcement only — the 'p'
    # column (Dir = tangent, Appl = active) and its passive twin 'p_pt'. A tangent
    # line is treated as flexible: its force turns to lie along the failure surface
    # at the slice base, so psi is the base angle alpha and the force acts at the
    # center of the base. Reinforcement declared Dir = axial never reaches this
    # branch: slice.py resolves it at the line's OWN inclination into the pa_*
    # (active) and pp_* (passive) component and first-moment sums read above
    # (slice.py, "Reinforcement lines"), which each method adds separately.
    psi = alpha  # psi is the angle of the tangent reinforcement force from the horizontal
    y_r = y_cb  # y_r is the y-coordinate of the point of action of the reinforcement
    x_r = x_c  # x_r is the x-coordinate of the point of action of the reinforcement

    # use variable names to match the derivation.
    x_p = slice_df['d_x'].values  # distributed load x-coordinate
    y_p = slice_df['d_y'].values  # distributed load y-coordinate
    y_k = slice_df['y_cg'].values  # seismic force y-coordinate
    x_b = x_c  # center of base x-coordinate
    y_b = y_cb  # center of base y-coordinate


    tan_p = np.tan(phi)  # tan(phi)

    # Explicit facing (flat-arc / override) wins; else historical y_cb test. On a
    # flat arc y_cb[0] and y_cb[-1] are near-equal, so this comparison is
    # otherwise noise-driven — see generate_slices / _resolve_right_facing.
    right_facing = slice_df.attrs.get('right_facing', (y_cb[0] > y_cb[-1]))
    # If right facing, swap angles and strengths. For most methods, you can use the normal angle conventions
    # and get the right answer. But for Spencer, due to the way that the moment equation is written,
    # you need to swap the angles and strengths if the slope is right facing.
    if right_facing:
        alpha = -alpha
        beta = -beta
        psi = -psi
        R = -R
        c = -c
        kw = -kw
        V = -V   # tension-crack water thrust: flips with the sliding direction, like kw
        tan_p = -tan_p

    # pre-compute the trigonometric functions
    cos_a = np.cos(alpha)  # cos(alpha)
    sin_a = np.sin(alpha)  # sin(alpha)
    #tan_p = np.tan(phi)  # tan(phi)    # moved above
    cos_b = np.cos(beta)  # cos(beta)
    sin_b = np.sin(beta)  # sin(beta)
    sin_psi = np.sin(psi)  # sin(psi)
    cos_psi = np.cos(psi)  # cos(psi)

    # Pile force components. On right-facing slopes only the HORIZONTAL component
    # flips with the facing (it reverses with the sliding direction); the vertical
    # (upward) component is facing-independent — up is up. Flipping the whole H_pile
    # (as the other reflected quantities above) would wrongly negate the vertical
    # component and break battered (theta_p != 0) piles.
    H_cos_tp = H_pile * np.cos(theta_pile)  # horizontal component
    H_sin_tp = H_pile * np.sin(theta_pile)  # vertical component (upward)
    if right_facing:
        H_cos_tp = -H_cos_tp
        # Axial reinforcement enters in REAL components at real positions, and
        # the stored direction (cos(psi) > 0) is the NEGATION of the real
        # tension on a right-facing slope: negate the whole vector (all four
        # sums; verified against the left-facing mirror oracle). Line loads
        # mirror beta.
        pa_cx = -pa_cx; pa_cy = -pa_cy
        pa_mx = -pa_mx; pa_my = -pa_my
        pp_cx = -pp_cx; pp_cy = -pp_cy
        pp_mx = -pp_mx; pp_my = -pp_my
        P_pt = -P_pt          # tangent passive mirrors R
        ll_b = -ll_b

    # Passive pile portion: mobilized (divided by F), so it is removed from the
    # constant pile components and carried in the F-dependent passive arrays.
    frac_pas = np.divide(H_pas, H_pile, out=np.zeros_like(H_pas), where=H_pile != 0)
    H_cos_pas = H_cos_tp * frac_pas
    H_sin_pas = H_sin_tp * frac_pas
    H_cos_tp = H_cos_tp - H_cos_pas
    H_sin_tp = H_sin_tp - H_sin_pas

    Fh = (- kw - V + P * sin_b + R * cos_psi + H_cos_tp      # Equation (1) + pile horizontal
          + pa_cx + LL * np.sin(ll_b))                         # + axial reinf + line load
    Fv = (- W - P * cos_b + R * sin_psi + H_sin_tp             # Equation (2) + pile vertical (upward)
          + pa_cy - LL * np.cos(ll_b))                         # + axial reinf + line load

    # Passive (ultimate) support components: enter every equation divided by F.
    # Tangent-passive acts parallel to the base at the base center (like R);
    # axial-passive at its crossing point; passive piles per their components.
    Fh_pas = P_pt * cos_psi + pp_cx + H_cos_pas
    Fv_pas = P_pt * sin_psi + pp_cy + H_sin_pas
    Mo_pas = (- (pp_my - y_b * pp_cx) + (pp_mx - x_b * pp_cy)
              - H_cos_pas * (y_pile - y_b) + H_sin_pas * (x_pile - x_b))
    Mo = - P * sin_b * (y_p - y_b) - P * cos_b * (x_p - x_b) \
        + kw * (y_k - y_b) + V * (y_v - y_b) - R * cos_psi * (y_r - y_b) + R * sin_psi * (x_r - x_b) \
        - H_cos_tp * (y_pile - y_b) + H_sin_tp * (x_pile - x_b) \
        - (pa_my - y_b * pa_cx) + (pa_mx - x_b * pa_cy) \
        - LL * np.sin(ll_b) * (ll_y - y_b) - LL * np.cos(ll_b) * (ll_x - x_b)  # Eq (3) + pile/axial/line-load moments
    
    # ========== BEGIN SOLUTION ==========

    def compute_Q_and_yQ(F, theta_rad):
        """Compute Q and y_Q for given F and theta values. Passive support
        mobilizes with the soil: its components carry 1/F."""
        Fv_e = Fv + Fv_pas / F
        Fh_e = Fh + Fh_pas / F
        # Equation (24): m_alpha
        ma = 1 / (np.cos(alpha - theta_rad) + np.sin(alpha - theta_rad) * tan_p / F)

        # Equation (23): Q
        Q = (- Fv_e * sin_a - Fh_e * cos_a - (c / F) * dl + (Fv_e * cos_a - Fh_e * sin_a + u * dl) * tan_p / F) * ma

        # Equation (26): y_Q with numerical safeguard
        # Add small epsilon to prevent divide-by-zero when Q * cos(theta) is very small
        Q_cos_theta = Q * np.cos(theta_rad)
        eps = 1e-10
        safe_denom = np.where(np.abs(Q_cos_theta) < eps, eps * np.sign(Q_cos_theta + eps), Q_cos_theta)
        y_q = y_b + (Mo + Mo_pas / F) / safe_denom

        return Q, y_q
    
    def compute_residuals(F, theta_rad):
        """Compute residuals R1 and R2 for given F and theta values."""
        Q, y_q = compute_Q_and_yQ(F, theta_rad)

        # Equation (27): R1 = sum(Q)
        R1 = np.sum(Q)

        # Equation (28): R2 = sum(Q * (x_b * sin(theta) - y_Q * cos(theta)))
        R2 = np.sum(Q * (x_b * np.sin(theta_rad) - y_q * np.cos(theta_rad)))

        return R1, R2, Q, y_q

    if residual_hook is not None:
        residual_hook(compute_residuals)

    def compute_derivatives(F, theta_rad, Q, y_q):

        """Compute all derivatives needed for Newton's method."""
        # Precompute trigonometric terms
        cos_alpha_theta = np.cos(alpha - theta_rad)
        sin_alpha_theta = np.sin(alpha - theta_rad)
        cos_theta = np.cos(theta_rad)
        sin_theta = np.sin(theta_rad)
        
        # Constants for Q expression (Equations 45-49), generalized: passive
        # support makes C1, C2 (and Mo) functions of F —
        #   C1(F) = C1_0 + C1_p/F,  C2(F) = C2_0 + C2_p/F,  Mo(F) = Mo + Mo_pas/F
        # so N(F) = C1 + C2/F and dN/dF = -(C1_p + C2_0 + 2*C2_p/F)/F^2, written
        # below as -(C1_p + C2 + C2_p/F)/F^2 using C2_0 = C2 - C2_p/F. With no
        # passive elements (C1_p = C2_p = 0) every expression reduces to the
        # original closed forms exactly.
        Fv_e = Fv + Fv_pas / F
        Fh_e = Fh + Fh_pas / F
        C1 = -Fv_e * sin_a - Fh_e * cos_a
        C2 = -c * dl + (Fv_e * cos_a - Fh_e * sin_a + u * dl) * tan_p
        C1_p = -Fv_pas * sin_a - Fh_pas * cos_a
        C2_p = (Fv_pas * cos_a - Fh_pas * sin_a) * tan_p
        C3 = cos_alpha_theta
        C4 = sin_alpha_theta * tan_p
        
        # Denominator for Q
        denom_Q = C3 + C4 / F
        
        # First-order partial derivatives of Q (Equations 50-51, generalized)
        dN_dF = -(C1_p + C2 + C2_p / F) / F**2
        dQ_dF = (1 / denom_Q**2) * (dN_dF * denom_Q + (C1 + C2 / F) * C4 / F**2)
        
        dC3_dtheta = sin_alpha_theta  # Equation (55)
        dC4_dtheta = -cos_alpha_theta * tan_p  # Equation (56)
        dQ_dtheta = (-1 / denom_Q**2) * (C1 + C2 / F) * (dC3_dtheta + dC4_dtheta / F)

        # Partial derivatives of y_Q (Equations 59-60)
        # Add numerical safeguard to prevent divide-by-zero when Q * cos_theta is very small
        Q_cos_theta = Q * cos_theta
        eps = 1e-10  # Small epsilon to prevent exact zero division

        # Use np.where to handle element-wise operations safely
        # Where |Q * cos_theta| < eps, set derivatives to a large value to signal ill-conditioning
        safe_denom = np.where(np.abs(Q_cos_theta) < eps, eps * np.sign(Q_cos_theta + eps), Q_cos_theta)

        Mo_e = Mo + Mo_pas / F
        dyQ_dF = ((-Mo_pas / F**2) / safe_denom
                  + (-1 / safe_denom**2) * Mo_e * dQ_dF * cos_theta)
        dyQ_dtheta = (-1 / safe_denom**2) * Mo_e * (dQ_dtheta * cos_theta - Q * sin_theta)
        
        # First-order partial derivatives of R1 (Equations 35-36)
        dR1_dF = np.sum(dQ_dF)
        dR1_dtheta = np.sum(dQ_dtheta)

        # First-order partial derivatives of R2 (Equations 40-41)
        dR2_dF = np.sum(dQ_dF * (x_b * sin_theta - y_q * cos_theta)) - np.sum(Q * dyQ_dF * cos_theta)
        dR2_dtheta = np.sum(dQ_dtheta * (x_b * sin_theta - y_q * cos_theta)) + np.sum(Q * (x_b * cos_theta + y_q * sin_theta - dyQ_dtheta * cos_theta))

        return dR1_dF, dR1_dtheta, dR2_dF, dR2_dtheta

    
    def safe_theta_bounds(F_val, margin_deg=5):
        return spencer_theta_bounds(alpha, tan_p, F_val, margin_deg)

    def newton_solve(F0, theta0_rad, max_iter, tol, debug_level):
        """Run Newton iteration with backtracking line search. Returns (converged, F, theta_rad, iteration)."""
        theta_lo, theta_hi = safe_theta_bounds(F0)
        if theta0_rad < theta_lo or theta0_rad > theta_hi:
            theta0_rad = (theta_lo + theta_hi) / 2

        F = F0
        theta_rad = theta0_rad
        stagnation_count = 0

        for iteration in range(max_iter):
            R1, R2, Q, y_q = compute_residuals(F, theta_rad)
            residual_norm = R1**2 + R2**2

            if debug_level >= 1:
                if iteration == 0:
                    print(f"Iteration {1} - Initial: F = {F:.3f}, theta = {np.degrees(theta_rad):.3f}°, R1 = {R1:.6e}, R2 = {R2:.6e}")
                else:
                    print(f"Iteration {iteration + 1} - Updated: F = {F:.3f}, theta = {np.degrees(theta_rad):.3f}°, R1 = {R1:.6e}, R2 = {R2:.6e}")

            if abs(R1) < tol and abs(R2) < tol:
                if debug_level >= 1:
                    print(f"Converged in {iteration + 1} iterations, R1 = {R1:.6e}, R2 = {R2:.6e}")
                return True, F, theta_rad, iteration

            dR1_dF, dR1_dtheta, dR2_dF, dR2_dtheta = compute_derivatives(F, theta_rad, Q, y_q)

            J = np.array([[dR1_dF, dR1_dtheta],
                          [dR2_dF, dR2_dtheta]])

            try:
                cond_num = np.linalg.cond(J)
                if cond_num > 1e12:
                    return False, F, theta_rad, iteration
            except:
                return False, F, theta_rad, iteration

            try:
                delta_solution = np.linalg.solve(J, np.array([-R1, -R2]))
                delta_F = delta_solution[0]
                delta_theta = delta_solution[1]
            except np.linalg.LinAlgError:
                return False, F, theta_rad, iteration

            if debug_level >= 1:
                print(f"          Newton: delta_F = {delta_F:.3f}, delta_theta = {np.degrees(delta_theta):.3f}°, {delta_theta: .3f} (rad)")

            # Backtracking line search: find step size that reduces residual norm
            step = 1.0
            for _ in range(20):
                F_trial = F + step * delta_F
                theta_trial = theta_rad + step * delta_theta

                if F_trial <= 0:
                    step *= 0.5
                    continue

                theta_lo, theta_hi = safe_theta_bounds(F_trial)
                theta_trial = np.clip(theta_trial, theta_lo, theta_hi)

                R1_trial, R2_trial, _, _ = compute_residuals(F_trial, theta_trial)
                trial_norm = R1_trial**2 + R2_trial**2

                if trial_norm < residual_norm:
                    break
                step *= 0.5

            if debug_level >= 1 and step < 1.0:
                print(f"          Line search: step = {step:.4f}")

            # Detect stagnation (line search found no improvement)
            if step < 1e-6:
                stagnation_count += 1
                if stagnation_count >= 5:
                    if debug_level >= 1:
                        print(f"          Stagnation detected, exiting Newton solver early")
                    return False, F, theta_rad, iteration
            else:
                stagnation_count = 0

            F = F + step * delta_F
            theta_rad = theta_rad + step * delta_theta

            if F <= 0:
                F = 0.1

            theta_lo, theta_hi = safe_theta_bounds(F)
            theta_rad = np.clip(theta_rad, theta_lo, theta_hi)

        return False, F, theta_rad, max_iter - 1

    # ------------------------------------------------------------------
    # Which (F, theta) pairs are a state of the mass
    # ------------------------------------------------------------------
    # Spencer's system has more than one root on many surfaces, and the ones
    # outside the pole-free band are not equilibrium states: past a pole a
    # slice's m_alpha has changed sign, so its base normal has reversed and the
    # slice solution that produced the root is meaningless. The band is the same
    # quantity `_force_closure_root` calls the base factor, written for this
    # method's interslice assumption, and the two share their remaining measures.

    def theta_band(F_val, margin_deg=0.0):
        """The interslice inclinations admissible at this factor of safety.

        The pole-free band `max(alpha) - pi/2 < theta - arctan(tan(phi)/F) <
        min(alpha) + pi/2`: theta within a right angle of every slice base, less
        the friction that base mobilizes. Outside it a slice's m_alpha has changed
        sign and its base normal has reversed, so the root is a discontinuity of
        the equations rather than a state of the mass. This is the geometric bound
        Spencer (1973) and Duncan & Wright describe — the interslice inclination
        lies between the inclinations of the ground surface and the slip surface —
        written in the form the equations themselves give.
        """
        return safe_theta_bounds(F_val, margin_deg)

    def _state_at(F_val, theta_val):
        """Base normals, interslice resultants and base factors at one root."""
        _, _, Q_val, _ = compute_residuals(F_val, theta_val)
        Fv_f = Fv + Fv_pas / F_val
        Fh_f = Fh + Fh_pas / F_val
        N_val = (-Fv_f * cos_a + Fh_f * sin_a
                 + Q_val * np.sin(alpha - theta_val) - u * dl)
        Z_val = np.concatenate(([0.0], -np.cumsum(Q_val)))
        base = (np.cos(alpha - theta_val)
                + np.sin(alpha - theta_val) * tan_p / F_val)
        return N_val, Z_val, base

    def _thrust_out_at(F_val, theta_val):
        """How much of this root's line of thrust falls outside the slices.

        The same recurrence the reported solution's thrust line comes from
        (equation 69), evaluated at a candidate root rather than at the accepted
        one, so the fraction can be read before the root is reported. It is what
        `SPENCER_THRUST_OUT_DISPUTED` is measured against.
        """
        _, _, Q_val, _ = compute_residuals(F_val, theta_val)
        Mo_f = Mo + Mo_pas / F_val
        Z_val = np.concatenate(([0.0], -np.cumsum(Q_val)))
        n_s = len(Q_val)
        yt_left = np.zeros(n_s)
        yt_left[0] = y_lb[0]
        s_th, c_th = np.sin(theta_val), np.cos(theta_val)
        with np.errstate(divide='ignore', invalid='ignore'):
            for i in range(n_s - 1):
                yt_left[i + 1] = y_b[i] - (
                    (Mo_f[i] - Z_val[i] * s_th * dx[i] / 2
                     - Z_val[i + 1] * s_th * dx[i] / 2
                     - Z_val[i] * c_th * (yt_left[i] - y_b[i]))
                    / (Z_val[i + 1] * c_th))
        return _thrust_outside_fraction(slice_df['y_lt'].values, y_lb, yt_left)

    #: The load the interslice resultants are judged against, as in
    #: `_force_closure_root`: the mass's own weight plus every load applied to it.
    load_scale = _driving_load(slice_df)
    if not load_scale > 0:
        load_scale = 1.0

    #: Every root the cascade reached and would not report, with its reason.
    rejected_roots = []

    def why_inadmissible(F_val, theta_val):
        """The measure this root fails, or None when it describes the mass.

        The three measures are `_force_closure_root`'s, in Spencer's variables.
        The base factor is the band: m_alpha's denominator keeps its sign on every
        slice exactly inside it, and a root outside it has reversed a base normal.
        A MAGNITUDE bar on that factor, the force-equilibrium closure's
        `FE_MIN_BASE_FACTOR`, is deliberately not applied here — it was measured
        and refuses answers the corpus confirms (VP104b's own circle solves at a
        base factor of 0.048, against Bishop's 1.518 and Morgenstern-Price's
        1.519 on the same slices), because Spencer's roots are not wedged between
        poles the way the march's are: the band already excludes those. The
        remaining two are the closure's unchanged — interslice resultants bounded
        by the driving load, and base tension short of the extent past which the
        solution contradicts the strength it was solved with over most of the
        surface.
        """
        if not (np.isfinite(F_val) and np.isfinite(theta_val)) or F_val <= 0:
            return "the equations do not close here"
        lo, hi = theta_band(F_val)
        if not (lo - 1e-9 <= theta_val <= hi + 1e-9):
            return (f"interslice inclination {np.degrees(theta_val):.1f} deg "
                    f"outside the admissible band "
                    f"[{np.degrees(lo):.1f}, {np.degrees(hi):.1f}] deg")
        N_val, Z_val, _base = _state_at(F_val, theta_val)
        if not np.all(np.isfinite(N_val)):
            return "the equations do not close here"
        max_Z = float(np.abs(Z_val).max())
        if max_Z > FE_MAX_Z_OVER_W * load_scale:
            return (f"interslice force {max_Z / max(load_scale, 1e-30):.0f}x the "
                    f"load on the mass")
        frac_neg = float(np.mean(N_val < 0)) if len(N_val) else 0.0
        if frac_neg > MAX_BASE_TENSION_EXTENT:
            return f"{100 * frac_neg:.0f}% of bases in tension"
        return None

    def accept_or_save(F_val, theta_val, label=""):
        """Report this root, or record why it is not one and keep looking."""
        why = why_inadmissible(F_val, theta_val)
        if why is None:
            return True
        if not any(abs(F_val - f) < 1e-9 and abs(theta_val - t) < 1e-12
                   for f, t, _ in rejected_roots):
            rejected_roots.append((float(F_val), float(theta_val), why))
        if debug_level >= 1:
            print(f"  {label}F={F_val:.3f}, θ={np.degrees(theta_val):.1f}° → "
                  f"{why} — continuing search")
        return False

    def name_rejected():
        """The discarded roots, in one phrase, with the measure each failed."""
        return ", ".join(
            f"FS={f:.3f} at θ={np.degrees(t):.1f}° ({why})"
            for f, t, why in sorted(rejected_roots))

    #: Admissible roots the tie-break stood down in favour of the reported one.
    passed_over = []

    def _same_root(a, b):
        """Whether two (F, theta) pairs are the same crossing.

        The tolerance is relative on F and a thousandth of a degree on theta:
        the sweep descends on the same crossing from many starts and stops on
        the residual, so the values it returns for one crossing agree to about
        eight digits rather than exactly, and an exact test would report one
        root many times over.
        """
        return (abs(a[0] - b[0]) <= 1e-6 * max(1.0, abs(a[0]), abs(b[0]))
                and abs(a[1] - b[1]) <= 1.7e-5)

    #: The moment-equilibrium answer on these slices, solved at most once.
    _moment_ref = []

    def moment_answer():
        """Bishop's factor of safety on a circle, Janbu's on any other surface.

        The tie-break's reference, and the same one `_force_closure_root` uses.
        It is solved once and cached: a search calls this method thousands of
        times, and both references cost well under a millisecond, but neither is
        free enough to solve twice on the same slices.
        """
        if not _moment_ref:
            ref = None
            ref_method = bishop if _has_circle_center(slice_df) else janbu
            try:
                ok_r, res_r = ref_method(slice_df.copy())
                if ok_r and np.isfinite(res_r['FS']) and res_r['FS'] > 0:
                    ref = float(res_r['FS'])
            except Exception:
                ref = None
            _moment_ref.append(ref)
        return _moment_ref[0]

    def pick_by_moment_answer(found):
        """Among admissible roots, the one nearest the moment-equilibrium answer.

        The same tie-break `_force_closure_root` applies, and for the same
        reason: a factor of safety is strength over demand, so nearness is a
        ratio. Bishop's method is the moment-only answer on a circular surface;
        on a non-circular one Janbu's is the closest thing to it, and where
        neither solves the smallest admissible root is taken.
        """
        if len(found) == 1:
            return found[0]
        ref = moment_answer()
        if ref is None:
            return min(found, key=lambda ft: ft[0])
        return min(found, key=lambda ft: (abs(np.log(ft[0] / ref)), ft[0]))

    def sweep_the_band():
        """Every (F, theta) crossing the band holds, from starts spread across it.

        The band's width and position both move with F, so the sweep is run in
        (F, s) with s the position across the band, 0 at its lower edge and 1 at
        its upper. A bounded least-squares descent in those coordinates cannot
        leave the band, which an unbounded root finder started inside it
        regularly does. About 3 500 residual evaluations, against the cascade's
        thirty, so it runs only where the cascade has failed or where the
        agreement test below finds the cascade's root disputed.
        """
        from scipy.optimize import least_squares

        w_scale = float(np.sum(np.abs(Fv))) or 1.0
        l_scale = float(max(np.ptp(x_b), np.ptp(y_b), 1e-12))

        def _theta_of(F_val, s_val):
            t_lo, t_hi = theta_band(float(F_val), margin_deg=0.5)
            return t_lo + float(s_val) * (t_hi - t_lo)

        def _band_residual(x):
            th = _theta_of(x[0], x[1])
            R1_v, R2_v, _, _ = compute_residuals(float(x[0]), th)
            if not (np.isfinite(R1_v) and np.isfinite(R2_v)):
                return np.array([1e12, 1e12])
            return np.array([R1_v / w_scale, R2_v / (w_scale * l_scale)])

        n_F, n_s = SPENCER_SWEEP_GRID
        crossings = []
        for F_try in np.geomspace(FE_FS_MIN, FE_FS_MAX, n_F):
            for s_try in np.linspace(0.1, 0.9, n_s):
                try:
                    sol = least_squares(_band_residual, [float(F_try), float(s_try)],
                                        bounds=([FE_FS_MIN, 0.0], [FE_FS_MAX, 1.0]),
                                        xtol=1e-12, ftol=1e-12,
                                        max_nfev=SPENCER_SWEEP_MAX_NFEV)
                except Exception:
                    continue
                F_c = float(sol.x[0])
                th_c = _theta_of(F_c, sol.x[1])
                R1_c, R2_c, _, _ = compute_residuals(F_c, th_c)
                if not (abs(R1_c) < tol and abs(R2_c) < tol):
                    continue
                if any(_same_root((F_c, th_c), cr) for cr in crossings):
                    continue
                crossings.append((F_c, th_c))
        return crossings

    # ---------------------------------------------------------------------
    # Does an ADMISSIBLE solution exist at all?
    # ---------------------------------------------------------------------
    # Spencer's assumption — every interslice force at the SAME inclination
    # theta — turns equilibrium into two equations in (F, theta). On some
    # surfaces that system has no root the method would accept, and then no
    # starting guess and no iteration count reaches one: the retry cascade below
    # simply spends time proving it the slow way, and what comes back reads as
    # "did not converge", which says the solver failed when the truth is about
    # the method. These two tests separate the cases.
    #
    # BOTH verdicts are scoped to the ADMISSIBLE range of theta — the pole-free
    # band max(alpha) - pi/2 < theta < min(alpha) + pi/2, where m_alpha keeps its
    # sign on every slice, which is the range the solver's own safe_theta_bounds
    # searches. Outside it roots commonly DO exist, at inclinations that reverse
    # the base normal on some slices; where the scipy stage happens to land on
    # one, accept_or_save refuses it as anomalous base tension. So neither test
    # may claim that a surface admits no solution at all — only that it admits
    # none the method would accept. The phi = 0 test measures which of the two it
    # is and says so.
    #
    # The FIRST is exact and runs BEFORE the cascade, on the surfaces where the
    # question is provably scalar (see _decoupled_terms). The SECOND is a coarse
    # sweep, evidence rather than proof, and runs only AFTER the cascade has
    # failed — it must never preempt a retry that might have found the root.

    def _decoupled_terms():
        """The scalar existence problem this surface reduces to, or None.

        At phi = 0, with no force or moment terms other than weight (Fh = 0 and
        Mo = 0 on every slice, no passive support), on a CIRCULAR surface,
        Spencer's system decouples. Writing n_i = -Fv_i sin(a_i) - c_i dl_i / F
        (the driving weight component less the mobilized cohesion), equation (23)
        gives Q_i = n_i sec(a_i - theta), so

            R1 = sum_i n_i sec(a_i - theta)                                (force)
            R2 = (Xo sin(theta) - Yo cos(theta)) R1 + R sum_i n_i         (moment)

        — the moment sum factors that way because on a circle
        x_b = Xo + R sin(a) and y_b = Yo - R cos(a), which is the identity this
        checks on the surface's own numbers rather than assuming. So R2 = 0 with
        R1 = 0 forces sum_i n_i = 0, i.e. F is the MOMENT factor of safety
        sum(c dl) / sum(W sin a) — Bishop's phi = 0 answer exactly — and theta is
        left to satisfy the scalar h(theta) = sum_i n_i sec(a_i - theta) = 0.

        Returns ``(n, F_m, R)`` or None when any precondition fails, in which case
        the caller falls back to the coarse sweep.

        BOTH FACINGS QUALIFY. A right-facing slope reaches this with alpha
        negated, and on a mirrored model x_b is mirrored with it, so
        x_b - R sin(alpha) returns the mirrored centre exactly (measured: ptp 0.0
        on a mirrored embankment, against 7e-15 on the original) and the same
        surface gets the same verdict either way round. What the identity check
        actually excludes is a surface that is not a circle in the frame it is
        evaluated in — a composite surface truncated along the base, whose run
        there is not at radius R.
        """
        if np.any(np.abs(tan_p) > 1e-12):
            return None                      # phi = 0 only
        if np.any(np.abs(Fh) > 1e-9) or np.any(np.abs(Mo) > 1e-9):
            return None                      # no loads reaching force/moment terms
        if np.any(np.abs(Fh_pas) > 1e-12) or np.any(np.abs(Fv_pas) > 1e-12) \
                or np.any(np.abs(Mo_pas) > 1e-12):
            return None                      # no passive support
        if not _has_circle_center(slice_df):
            return None
        Rr = float(slice_df['r'].iloc[0])
        if not np.isfinite(Rr) or Rr <= 0:
            return None
        # x_b = Xo + R sin(a), y_b = Yo - R cos(a) — constant to rounding on a
        # true circle in either facing, and NOT constant on a composite surface,
        # whose run along the base is not at radius R.
        Xo_i = x_b - Rr * sin_a
        Yo_i = y_b + Rr * cos_a
        if (np.ptp(Xo_i) > 1e-6 * Rr) or (np.ptp(Yo_i) > 1e-6 * Rr):
            return None
        drive = float(np.sum(-Fv * sin_a - Fh * cos_a))   # sum W sin(alpha)
        coh = float(np.sum(c * dl))                       # sum c dl
        if drive == 0.0 or not np.isfinite(coh):
            return None
        F_m = coh / drive                    # both flip together when right-facing
        if not np.isfinite(F_m) or F_m <= 0:
            return None
        n = -Fv * sin_a - Fh * cos_a - (c / F_m) * dl
        return n, F_m, Rr

    def _roots_outside_band(n, lo, hi):
        """Whether h has a zero at an INADMISSIBLE inclination, outside the band.

        h is continuous between consecutive poles (theta = a_i -+ pi/2 + k pi),
        and runs to +/-infinity at each, so a sign change with no pole between
        the two samples is a root by the intermediate value theorem. h(theta+pi)
        = -h(theta), so one period covers every distinct root.

        This is what keeps the verdict honest. Roots out here are real roots of
        Spencer's equations — they are simply not solutions: past a pole a
        slice's m_alpha has changed sign, so its base normal has reversed, and
        the solver refuses such a root as anomalous base tension when its scipy
        stage lands on one. Reporting that the surface admits NO root would be
        false; reporting that it admits no ADMISSIBLE root is the fact.
        """
        start = float(np.min(alpha)) - np.pi / 2
        th = np.linspace(start, start + np.pi, 20001)
        with np.errstate(divide='ignore', invalid='ignore'):
            h = (1.0 / np.cos(alpha[None, :] - th[:, None])) @ n
        poles = np.concatenate([alpha - np.pi / 2, alpha + np.pi / 2])
        poles = np.concatenate([poles - np.pi, poles, poles + np.pi])
        ok = np.isfinite(h)
        for i in range(len(th) - 1):
            if not (ok[i] and ok[i + 1]) or h[i] * h[i + 1] >= 0:
                continue
            if np.any((poles > th[i]) & (poles < th[i + 1])):
                continue                     # a pole, not a crossing
            mid = 0.5 * (th[i] + th[i + 1])
            if not (lo < mid < hi):
                return True
        return False

    def _phi0_admits_no_admissible_solution():
        """True when the scalar test PROVES no ADMISSIBLE (F, theta) solves this.

        h(theta) = sum_i n_i sec(a_i - theta) is swept across the pole-free band
        max(a) - pi/2 < theta < min(a) + pi/2, where every sec is positive and
        finite; outside it a slice's m_alpha changes sign, which is the
        singularity the solver's own theta bounds exclude. h runs to +/-infinity
        at both ends of the band (the extreme-alpha slice dominates), so a sign
        change inside means an admissible root exists by the intermediate value
        theorem, and no sign change means there is none.

        The claim stops there, at the band. Outside it roots are common (see
        _roots_outside_band), and the message says which case this surface is,
        because "no root in the band" and "no root anywhere" are different facts
        and only one of them is usually true.

        The verdict is only returned when h's extremum stands clear of the
        acceptance tolerance by a wide margin. F is not quite pinned: the solver
        accepts |R2| < tol, which admits |sum n_i| < tol / R and so lets 1/F move
        by tol / (R sum(c dl)), shifting h by at most tol * max(sec) / R. The
        margin below is 1e4 times that bound, so no surface that could have been
        accepted is ever refused. Anything short of it returns False and the
        ordinary cascade runs.
        """
        terms = _decoupled_terms()
        if terms is None:
            return False
        n, F_m, Rr = terms
        # F_m is the moment factor of safety of this surface, and at phi = 0 it is
        # Bishop's answer term for term (m_alpha = cos a, so sum c dx / m_alpha is
        # sum c dl). Recorded for the same reason the Bishop restart below records
        # its own: a search ranking the surfaces it could not solve reads it here.
        slice_df.attrs['moment_fs'] = float(F_m)
        lo = float(np.max(alpha)) - np.pi / 2
        hi = float(np.min(alpha)) + np.pi / 2
        if not (hi > lo):
            return False
        edge = 1e-6 * (hi - lo)
        th = np.linspace(lo + edge, hi - edge, 2001)
        sec = 1.0 / np.cos(alpha[None, :] - th[:, None])
        h = sec @ n
        if not np.all(np.isfinite(h)):
            return False
        if h.min() < 0.0 < h.max():
            return False                     # an admissible root exists: solvable
        k = int(np.argmax(h)) if h.max() < 0 else int(np.argmin(h))
        extremum = float(h[k])
        shift = tol * float(np.max(np.abs(sec[k]))) / Rr
        if abs(extremum) <= 1e4 * max(shift, 1e-30):
            return False                     # too close to call: let the solver try
        elsewhere = (
            "and the roots that do exist lie outside that band, at inclinations "
            "that reverse the base normal on some slices"
            if _roots_outside_band(n, lo, hi) else
            "and no root exists at any inclination")
        _no_solution_detail[:] = [
            f"at phi = 0 the force and moment equations decouple, and the force "
            f"balance has no root at any ADMISSIBLE interslice inclination "
            f"({np.degrees(lo):.1f} to {np.degrees(hi):.1f} deg, where every "
            f"slice keeps the sign of its base normal): its extreme value there "
            f"is {extremum:+.4g} at theta = {np.degrees(th[k]):.2f} deg, against "
            f"a moment factor of safety of {F_m:.4f}, {elsewhere}"]
        return True

    def _residual_floor_bounded_away():
        """True when nothing anywhere in (F, theta) comes near solving this surface.

        The general case has no closed form, so the evidence is measured: the
        residual pair is normalized by the quantities that make it up (the total
        slice weight, and that times the surface's own length scale, so the
        measure reads the same on a 20 ft and a 500 m slope), swept over a wide
        (F, theta) grid, and then descended from ten separated starting basins by
        least squares, each free to walk to a root the grid stepped over. What
        comes back is the smallest residual anywhere in reach. A surface with a
        root leaves residuals that collapse toward zero around it; a floor that
        stays a thousandfold above the residual the solver would have ACCEPTED
        has none within reach of anything.

        This is evidence, not proof — which is why it runs only after every retry
        has been spent, and never in front of one.
        """
        w_scale = float(np.sum(np.abs(Fv)))
        l_scale = float(max(np.ptp(x_b), np.ptp(y_b), 1e-12))
        if not np.isfinite(w_scale) or w_scale <= 0:
            return False

        def _norm(x):
            R1_v, R2_v, _, _ = compute_residuals(x[0], x[1])
            if not (np.isfinite(R1_v) and np.isfinite(R2_v)):
                return np.array([1e30, 1e30])
            return np.array([R1_v / w_scale, R2_v / (w_scale * l_scale)])

        grid = []
        for F_try in np.geomspace(0.05, 20.0, 25):
            t_lo, t_hi = safe_theta_bounds(F_try, margin_deg=1)
            if not (t_hi > t_lo):
                continue
            for th in np.linspace(t_lo, t_hi, 41):
                grid.append((float(np.hypot(*_norm((F_try, th)))), F_try, float(th)))
        if not grid:
            return False
        grid.sort()
        floor = grid[0][0]
        # Descend from starts SPREAD across the range, not merely from the best
        # few grid points: the residual surface has many local minima, the best
        # grid point does not reliably sit in the deepest basin, and a verdict
        # taken from one descent moves when the grid spacing moves. Ten separated
        # basins is what makes the answer the same at 25 x 41 and at 45 x 61.
        from scipy.optimize import least_squares
        starts = []
        for _, F_try, th in grid:
            if all(abs(np.log(F_try) - np.log(f)) > 0.3 or abs(th - t) > np.radians(10)
                   for f, t in starts):
                starts.append((F_try, th))
            if len(starts) >= 10:
                break
        for F_try, th in starts:
            try:
                sol = least_squares(_norm, [F_try, th], xtol=1e-12, ftol=1e-12,
                                    max_nfev=400)
            except Exception:
                continue
            if sol.x[0] > 0:
                floor = min(floor, float(np.hypot(*_norm(sol.x))))
        if not np.isfinite(floor):
            return False
        # The bar is set by what the solver ACCEPTS, not by a round number: a
        # solution is taken at |R1| < tol, which in these normalized terms is
        # tol / w_scale, and the verdict is only given when the reachable floor
        # stands a thousandfold above that. (Measured floors on the corpus run
        # 2e-4 to 8e-3 — four to five orders above acceptance — with no natural
        # gap in them, which is exactly why the bar is anchored to the tolerance
        # rather than cut through that continuum at a chosen fraction.)
        bar = max(NO_SOLUTION_FLOOR, NO_SOLUTION_MARGIN * (tol / w_scale))
        if floor <= bar:
            return False
        _no_solution_detail[:] = [
            f"the force and moment residuals are bounded away from zero over the "
            f"whole admissible range of F and theta (the smallest normalized "
            f"residual reachable is {floor:.3g}, {floor / bar:.0f} times the "
            f"{bar:.2g} a solution would have to reach)"]
        return True

    #: Filled by whichever test returns the verdict, read into the message.
    _no_solution_detail = []

    if existence_test and _phi0_admits_no_admissible_solution():
        # Exact, and therefore taken before a single iteration is spent: no retry
        # reaches an admissible root that is not there, so the cascade below has
        # nothing to add but time. What it WOULD have added on some of these
        # surfaces is the anomalous-base-tension refusal — its scipy stage is
        # unbounded in theta and sometimes lands on one of the out-of-band roots
        # this verdict already accounts for. Both are the same fact about the
        # surface (no admissible solution) and both are counted as that; the
        # refusal keeps its own message below wherever the cascade does run.
        return False, f"{SPENCER_NO_ADMISSIBLE_SOLUTION}: {_no_solution_detail[0]}."

    # Strategy 1: Newton from the caller's seed when one is given (a Monte
    # Carlo campaign passes the most-likely-values solution, which sits within
    # a few percent of every realization's root), else the default start.
    F0 = 1.5 if fs_seed is None else float(fs_seed)
    if theta_seed is None:
        theta0_rad = np.radians(-8.0) if right_facing else np.radians(8)
    else:
        theta0_rad = np.radians(float(theta_seed))

    converged, F, theta_rad, iteration = newton_solve(F0, theta0_rad, max_iter, tol, debug_level)
    if converged and not accept_or_save(F, theta_rad, "Newton default: "):
        converged = False

    # Strategy 2: Newton with Bishop's FS and multiple theta starts
    if not converged:
        try:
            success_bishop, result_bishop = bishop(slice_df)
            if success_bishop:
                F0_bishop = result_bishop['FS']
                # Recorded on the table, not just used as a starting guess: this
                # is the MOMENT factor of safety of this surface, and a search
                # that has to rank the surfaces its method could not solve reads
                # it here rather than solving Bishop a second time.
                slice_df.attrs['moment_fs'] = float(F0_bishop)
                if debug_level >= 1:
                    print(f"Retrying with Bishop FS = {F0_bishop:.3f} as initial guess")
                theta_tries = [theta0_rad, -theta0_rad, 0.0, np.radians(15), np.radians(-15)]
                for theta_try in theta_tries:
                    conv_b, F_b, theta_b, _ = newton_solve(F0_bishop, theta_try, max_iter, tol, debug_level)
                    if conv_b:
                        if accept_or_save(F_b, theta_b, "Newton Bishop: "):
                            converged, F, theta_rad = True, F_b, theta_b
                            break
        except Exception:
            pass  # Bishop may fail for non-circular surfaces

    # Strategy 3: scipy.optimize.root with multiple starts (ordered by |theta|)
    if not converged:
        from scipy.optimize import root as scipy_root

        def residual_vec(x):
            if x[0] <= 0.01:
                return np.array([1e10, 1e10])
            R1_v, R2_v, _, _ = compute_residuals(x[0], x[1])
            if not (np.isfinite(R1_v) and np.isfinite(R2_v)):
                return np.array([1e10, 1e10])
            return np.array([R1_v, R2_v])

        def jac_mat(x):
            if x[0] <= 0.01:
                return np.eye(2) * 1e10
            R1_v, R2_v, Q_v, yq_v = compute_residuals(x[0], x[1])
            if not (np.isfinite(R1_v) and np.isfinite(R2_v)):
                return np.eye(2) * 1e10
            d = compute_derivatives(x[0], x[1], Q_v, yq_v)
            return np.array([[d[0], d[1]], [d[2], d[3]]])

        F_starts = [1.0, 1.5, 2.0, 0.5, 3.0]
        try:
            sb, rb = bishop(slice_df)
            if sb:
                F_starts.insert(0, rb['FS'])
                slice_df.attrs['moment_fs'] = float(rb['FS'])
        except Exception:
            pass

        # Order by |theta| to prefer physically reasonable solutions first
        theta_starts = np.radians(np.array([0, 5, -5, 10, -10, 15, -15, 20, -20, 25, -25], dtype=float))

        for F_try in F_starts:
            # scipy_root is unbounded, so a start outside the admissible band
            # walks to a root outside it. Each start is brought into the band at
            # its own trial factor of safety, and the result is tested there too.
            t_lo, t_hi = theta_band(F_try, margin_deg=1.0)
            for theta_try in np.clip(theta_starts, t_lo, t_hi):
                try:
                    sol = scipy_root(residual_vec, [F_try, float(theta_try)],
                                     jac=jac_mat, method='hybr')
                    if sol.success and sol.x[0] > 0.01:
                        R1_c, R2_c, _, _ = compute_residuals(sol.x[0], sol.x[1])
                        if abs(R1_c) < tol and abs(R2_c) < tol:
                            if accept_or_save(sol.x[0], sol.x[1], "scipy: "):
                                converged = True
                                F = sol.x[0]
                                theta_rad = sol.x[1]
                                if debug_level >= 1:
                                    print(f"Converged via scipy root: F={F:.3f}, theta={np.degrees(theta_rad):.3f}°")
                                break
                except Exception:
                    continue
            if converged:
                break

    # Strategy 4: sweep the admissible band. The three strategies above descend
    # from a handful of starting guesses, and on a surface whose system carries
    # more than one root they reach whichever basin they were dropped into — on
    # the refined non-circular surfaces of the seismic benchmarks that was a root
    # raked 76 degrees below horizontal, reading a third of what the same
    # equations give under Morgenstern-Price. The band is therefore swept: every
    # crossing reachable from a start inside it is collected, the three measures
    # are applied to each, and the survivors are tie-broken against the moment
    # answer exactly as the force-equilibrium closure's roots are.
    from_sweep = False
    if not converged:
        crossings = sweep_the_band()
        admissible = [(f, t) for f, t in crossings if why_inadmissible(f, t) is None]
        for f, t in crossings:
            accept_or_save(f, t, "band sweep: ")
        if admissible:
            F, theta_rad = pick_by_moment_answer(admissible)
            passed_over.extend((f, t) for f, t in admissible
                               if not _same_root((f, t), (F, theta_rad)))
            converged = True
            from_sweep = True
            if debug_level >= 1:
                print(f"Band sweep: {len(crossings)} crossing(s), "
                      f"{len(admissible)} admissible → F={F:.4f}, "
                      f"θ={np.degrees(theta_rad):.2f}°")

    # The band refuses roots that reverse a base normal; it does not decide
    # between two crossings that both stand inside it, and the cascade above
    # reports whichever of its starts reached one first. On the critical circle
    # a Spencer search finds for VP16 both crossings are in band, and the
    # default start reaches F = 1.082 at theta = -27.1 deg where the other
    # reads 1.113 — Bishop's answer on the same slices, and Morgenstern-Price's
    # with f(x) = 1, the same equations solved a different way.
    #
    # Sweeping the band settles it and costs about a hundred times what the
    # cascade does, which a search cannot pay on every trial. So the reported
    # root is read for the signature the wrong branch carries — a line of
    # thrust outside the slice on most of its boundaries, which the solution
    # computes anyway — and only a root that carries it is disputed. Where it
    # is, every crossing the band holds is collected and judged, and the
    # survivors are tie-broken against the moment answer, exactly as the
    # force-equilibrium closure's roots are. See SPENCER_THRUST_OUT_DISPUTED for
    # the measurement the bar rests on and for the measure it was chosen over.
    if converged and not from_sweep and \
            _thrust_out_at(F, theta_rad) > SPENCER_THRUST_OUT_DISPUTED:
        reported = (F, theta_rad)
        others = [root for root in sweep_the_band()
                  if not _same_root(root, reported)]
        for root in others:
            accept_or_save(root[0], root[1], "band sweep: ")
        admissible = [reported] + [root for root in others
                                   if why_inadmissible(root[0], root[1]) is None]
        F, theta_rad = pick_by_moment_answer(admissible)
        passed_over.extend(root for root in admissible
                           if not _same_root(root, (F, theta_rad)))
        if debug_level >= 1:
            print(f"Disputed root: {len(others) + 1} crossing(s) in band, "
                  f"{len(admissible)} admissible → F={F:.4f}, "
                  f"θ={np.degrees(theta_rad):.2f}°")

    if not converged:
        if rejected_roots:
            # Roots WERE found and none of them describes a state of the mass.
            # That is a more specific fact than "no admissible solution" — it
            # names each root and the measure it failed — so it keeps its own
            # message, ahead of the residual sweep below.
            return False, f"{SPENCER_INADMISSIBLE}; rejected {name_rejected()}"
        if _residual_floor_bounded_away():
            return False, f"{SPENCER_NO_ADMISSIBLE_SOLUTION}: {_no_solution_detail[0]}."
        return False, SPENCER_NO_CONVERGENCE

    # Final computation of Q and y_q
    R1, R2, Q, y_q = compute_residuals(F, theta_rad)

    if debug_level >= 2:
        ma = 1 / (np.cos(alpha - theta_rad) + np.sin(alpha - theta_rad) * tan_p / F)
        # The force sums as the FINAL Q evaluation used them: equations (1) and
        # (2) plus the passive components at their mobilized 1/F share, which is
        # what compute_Q_and_yQ divides by the converged F. Writing the constant
        # part instead would leave equation (23) irreproducible from these
        # columns on any model that carries passive support; with none, the
        # passive arrays are zero and F_h/F_v are equations (1) and (2) exactly.
        Fh_e = Fh + Fh_pas / F
        Fv_e = Fv + Fv_pas / F
        slice_df['ma'] = ma
        slice_df['Q'] = Q
        slice_df['y_q'] = y_q
        slice_df['F_h'] = Fh_e
        slice_df['F_v'] = Fv_e
        slice_df['Mo'] = Mo
        # Print F and theta to 12 decimal places
        print(f"F = {F:.12f}, theta = {np.degrees(theta_rad):.12f}°")
        # Report the residuals
        print(f"R1 = {R1:.6e}, R2 = {R2:.6e}")
        # Debug print values per slice
        for i in range(len(Q)):
            print(f"Slice {i+1}: ma = {ma[i]:.3f}, Q = {Q[i]:.1f}, y_q = {y_q[i]:.2f}, F_h = {Fh_e[i]:.1f}, F_v = {Fv_e[i]:.1f}, Mo = {Mo[i]:.2f}")

    
    # Convert theta to degrees for output
    theta_opt = np.degrees(theta_rad)
    
    # ========== END SOLUTION ==========

    # Store theta in df
    slice_df['theta'] = theta_opt

    # --- Compute N_eff using Equation (18), with passive components at 1/F ---
    Fv_fin = Fv + Fv_pas / F
    Fh_fin = Fh + Fh_pas / F
    Mo_fin = Mo + Mo_pas / F
    N_eff = - Fv_fin * cos_a + Fh_fin * sin_a + Q * np.sin(alpha - theta_rad) - u * dl
    slice_df['n_eff'] = N_eff

    # --- Compute interslice forces Z using Equation (67) ---
    n = len(Q)
    Z = np.zeros(n+1)
    for i in range(n):
        Z[i+1] = Z[i] - Q[i] 
    slice_df['z'] = Z[:-1]        # Z_i acting on slice i's left face
 

    # --- Compute line of thrust using Equation (69) ---
    yt_l = np.zeros(n)  # the y-coordinate of the line of thrust on the left side of the slice.
    yt_r = np.zeros(n)  # the y-coordinate of the line of thrust on the right side of the slice.
    yt_l[0] = y_lb[0]  
    sin_theta = np.sin(theta_rad)
    cos_theta = np.cos(theta_rad)
    for i in range(n):
        if i == n - 1:
            yt_r[i] = y_rb[i]
        else:
            yt_r[i] = y_b[i] - ((Mo_fin[i] - Z[i] * sin_theta * dx[i] / 2 - Z[i+1] * sin_theta * dx[i] / 2 - Z[i] * cos_theta * (yt_l[i] - y_b[i])) / (Z[i+1] * cos_theta))
            yt_l[i+1] = yt_r[i]
    slice_df['yt_l'] = yt_l
    slice_df['yt_r'] = yt_r

    # --- Admissibility screen (report-only; acceptance above is unchanged) ---
    # max_tension_ratio normalizes base tension by cohesive capacity, so a c=0
    # slice can carry unlimited base tension without tripping it (VP30: -71 kN/m
    # on the cohesionless crack-face sliver scores 0.0 and passes). The shared
    # helper reports the Duncan & Wright signatures that guard cannot see; here
    # spencer keeps its own thrust line (yt_l), so all three fire. Z is already
    # in the physical convention (tension < 0) for both facings.
    warns = _admissibility_warnings(
        c, N_eff, Z,
        y_lt=slice_df['y_lt'].values,
        y_lb=slice_df['y_lb'].values,
        yt_l=yt_l)
    # Every root the cascade reached and passed over, with the measure it
    # failed, so the answer carries the alternatives it was chosen against.
    if passed_over:
        warns.append("Spencer's system has other admissible roots on these "
                     "slices: " + ", ".join(
                         f"FS={f:.3f} at θ={np.degrees(t):.1f}°"
                         for f, t in sorted(passed_over)))
    if rejected_roots:
        warns.append("Spencer's system has other roots on these slices: "
                     + name_rejected())
    if warns and debug_level >= 1:
        print("Spencer admissibility warnings: " + "; ".join(warns))

    # --- Return results ---
    results = {}
    results['method'] = 'spencer'
    results['FS'] = F
    results['theta'] = theta_opt
    results['warnings'] = warns

    return True, results


def _mp_f_vals(slice_df, f_type):
    """Interslice-force shape function f evaluated at each slice BOUNDARY.

    The boundaries are x_b = [x_l[0], x_r[0], ..., x_r[n-1]] (length n+1), and the
    normalized position is s_j = (x_b[j] - x_L) / (x_R - x_L) in [0, 1]. Only the
    SHAPE of f matters (tan θ = λ·f, so scaling f just rescales λ), so each is
    normalized to a unit peak by convention.

    v1 library:
        'constant'  -> f = 1            (recovers Spencer; the regression case)
        'half_sine' -> f = sin(π s)     (textbook / GeoStudio default; f=0 at ends)
    """
    x_l = slice_df['x_l'].values.astype(float)
    x_r = slice_df['x_r'].values.astype(float)
    x_b = np.concatenate([[x_l[0]], x_r])           # boundary x-coords, length n+1
    span = x_b[-1] - x_b[0]
    s = (x_b - x_b[0]) / span if span != 0 else np.zeros_like(x_b)
    if f_type == 'constant':
        return np.ones_like(s)
    elif f_type == 'half_sine':
        return np.sin(np.pi * s)
    else:
        raise ValueError(f"unknown f_type {f_type!r} (use 'constant' or 'half_sine')")


def _mp_line_of_thrust(slice_df, Z, theta_rad, right_facing, FS=1.0):
    """Line of thrust for Morgenstern-Price (post-process diagnostic; plan §4 opt b).

    Generalizes Spencer's per-slice moment recurrence (its eqs 68-69) to a
    per-BOUNDARY interslice angle. Taking moments on each slice about its base
    center fixes where the right interslice force acts, given the left: the weight
    and base reaction act at the base center (thin-slice x_c = x_b → zero arm), so
    only the external-load moment `Mo` and the interslice `Z`/θ terms remain. With a
    constant θ this reduces EXACTLY to Spencer's recurrence (the f(x)=1 == Spencer
    check). Stores 'yt_l'/'yt_r' in slice_df.

    `theta_rad` = per-boundary interslice angle (length n+1, radians); `Z` = the
    interslice resultant at each boundary (length n+1) from the march. The same
    right-facing reflection the march/Spencer use is applied to the load terms.
    """
    n = len(slice_df)
    alpha = np.radians(slice_df['alpha'].values)
    beta  = np.radians(slice_df['beta'].values)
    P   = slice_df['dload'].values            # distributed load resultant
    kw  = slice_df['kw'].values
    V   = slice_df['t'].values                # tension-crack water
    R   = slice_df['p'].values                # reinforcement
    dx  = slice_df['dx'].values
    x_b = slice_df['x_c'].values; y_b = slice_df['y_cb'].values
    y_lb = slice_df['y_lb'].values; y_rb = slice_df['y_rb'].values
    x_p = slice_df['d_x'].values; y_p = slice_df['d_y'].values   # surface-load point
    y_k = slice_df['y_cg'].values; y_v = slice_df['y_t'].values
    H_pile     = slice_df['h_pile'].values  if 'h_pile'  in slice_df.columns else np.zeros(n)
    theta_pile = slice_df['theta_p'].values if 'theta_p' in slice_df.columns else np.zeros(n)
    x_pile = slice_df['x_pile'].values if 'x_pile' in slice_df.columns else np.zeros(n)
    y_pile = slice_df['y_pile'].values if 'y_pile' in slice_df.columns else np.zeros(n)
    psi = alpha; y_r = y_b; x_r = x_b           # TANGENT reinforcement ∥ base, acts at base center
                                                # (axial arrives pre-resolved in pa_*/pp_* below)

    # v12 support/load terms (zeros when the columns are absent)
    def _c12(name):
        return slice_df[name].values.astype(float) if name in slice_df.columns else np.zeros(n)
    P_pt  = _c12('p_pt')
    pa_cx = _c12('pa_cx'); pa_cy = _c12('pa_cy')
    pa_mx = _c12('pa_mx'); pa_my = _c12('pa_my')
    pp_cx = _c12('pp_cx'); pp_cy = _c12('pp_cy')
    pp_mx = _c12('pp_mx'); pp_my = _c12('pp_my')
    H_pas = _c12('h_pile_pas')
    LL    = _c12('lload')
    ll_b  = np.radians(_c12('ll_beta'))
    ll_x  = _c12('ll_x'); ll_y = _c12('ll_y')

    if right_facing:                            # same reflection as spencer()/_mp_march
        beta = -beta; psi = -psi; R = -R; kw = -kw; V = -V
        # axial: negate the whole force vector, as in spencer()
        pa_cx = -pa_cx; pa_cy = -pa_cy; pa_mx = -pa_mx; pa_my = -pa_my
        pp_cx = -pp_cx; pp_cy = -pp_cy; pp_mx = -pp_mx; pp_my = -pp_my
        P_pt = -P_pt                            # tangent passive mirrors R
        ll_b = -ll_b                            # line loads mirror beta
    sin_b, cos_b = np.sin(beta), np.cos(beta)
    sin_psi, cos_psi = np.sin(psi), np.cos(psi)
    frac_pas = np.divide(H_pas, H_pile, out=np.zeros_like(H_pas), where=H_pile != 0)
    H_cos_tp = H_pile * np.cos(theta_pile)
    H_sin_tp = H_pile * np.sin(theta_pile)
    if right_facing:
        H_cos_tp = -H_cos_tp                    # horizontal pile component flips, vertical not
    H_cos_pas = H_cos_tp * frac_pas
    H_sin_pas = H_sin_tp * frac_pas
    H_cos_tp = H_cos_tp - H_cos_pas
    H_sin_tp = H_sin_tp - H_sin_pas

    # Mo: moment of the external loads about the base center (Spencer eq 3 + pile
    # + v12 axial reinforcement, passive support factored by FS, and line loads).
    Mo = (- P * sin_b * (y_p - y_b) - P * cos_b * (x_p - x_b)
          + kw * (y_k - y_b) + V * (y_v - y_b)
          - R * cos_psi * (y_r - y_b) + R * sin_psi * (x_r - x_b)
          - H_cos_tp * (y_pile - y_b) + H_sin_tp * (x_pile - x_b)
          - (pa_my - y_b * pa_cx) + (pa_mx - x_b * pa_cy)
          + (- (pp_my - y_b * pp_cx) + (pp_mx - x_b * pp_cy)
             - P_pt * cos_psi * (y_r - y_b) + P_pt * sin_psi * (x_r - x_b)
             - H_cos_pas * (y_pile - y_b) + H_sin_pas * (x_pile - x_b)) / FS
          - LL * np.sin(ll_b) * (ll_y - y_b) - LL * np.cos(ll_b) * (ll_x - x_b))

    st, ct = np.sin(theta_rad), np.cos(theta_rad)   # per boundary (length n+1)
    yt_l = np.zeros(n)
    yt_r = np.zeros(n)
    yt_l[0] = y_lb[0]
    for i in range(n):
        if i == n - 1:
            yt_r[i] = y_rb[i]
        else:
            denom = Z[i + 1] * ct[i + 1]
            if denom == 0:
                yt_r[i] = y_b[i]
            else:
                yt_r[i] = y_b[i] - ((Mo[i]
                                     - Z[i] * st[i] * dx[i] / 2
                                     - Z[i + 1] * st[i + 1] * dx[i] / 2
                                     - Z[i] * ct[i] * (yt_l[i] - y_b[i])) / denom)
            yt_l[i + 1] = yt_r[i]
    slice_df['yt_l'] = yt_l
    slice_df['yt_r'] = yt_r


def mprice(slice_df, f_type='half_sine', tol=1e-6,
                      max_iter=50, solver='auto',
                      debug_level=0):
    """Morgenstern-Price complete-equilibrium method (Approach A: F_f / F_m crossing).

    M-P satisfies BOTH force and moment equilibrium with a VARIABLE interslice-force
    inclination: ``tan(θ_j) = λ · f(x_j)``, where ``f`` is a prescribed shape
    function (see `_mp_f_vals`) and ``λ`` a scalar. Spencer is the special case
    ``f ≡ 1`` (then ``θ = arctan λ`` is constant).

    Approach A (Fredlund-Krahn / GLE style): for each ``λ`` find
        ``F_f(λ)`` = the FS root of the force residual  (Z[n] = 0), and
        ``F_m(λ)`` = the FS root of the moment residual (moment about origin = 0),
    then find ``λ*`` where ``F_f = F_m``. The crossing FS is the M-P factor of
    safety; ``λ*`` fixes the interslice-force distribution. Both residuals come from
    `_mp_march`.

    Parameters:
        f_type: 'constant' (== Spencer regression) or 'half_sine' (design default).
    Returns:
        (True, {'method','FS','lambda','f_type','theta'(deg, per boundary, n+1)})
        or (False, message).

    Right-facing slopes are handled: `_mp_extract` mirrors the per-slice arrays, and
    ``f ≡ 1`` reproduces `spencer()` to machine precision on both facings.
    """
    from scipy.optimize import brentq

    n = len(slice_df)
    if n < 2:
        return False, "Morgenstern-Price needs at least 2 slices."

    # Facing detection mirrors spencer(); _mp_march applies the right-facing flip set.
    # Explicit facing (flat-arc / override) wins; else the historical y_cb test.
    _ycb = slice_df['y_cb'].values
    right_facing = bool(slice_df.attrs.get('right_facing', _ycb[0] > _ycb[-1]))

    try:
        f_vals = _mp_f_vals(slice_df, f_type)
    except ValueError as e:
        return False, str(e)

    # Extract all per-slice arrays ONCE (with right-facing flips); the inner Newton
    # loops call _mp_residuals(A, ...) — no per-iteration DataFrame access.
    A = _mp_extract(slice_df, right_facing)

    # Seed FS from Bishop where possible (as Spencer does), else the fixed seed.
    seed = 1.5
    try:
        ok_b, res_b = bishop(slice_df)
        if ok_b:
            seed = res_b['FS']
    except Exception:
        pass

    def F_f(lam, s):
        """Force-equilibrium FS at this λ: the FS root of `force_res` (= Z[n]). The
        force residual is monotonic in FS, so this root is unique and well-behaved —
        no branch-jumping (unlike the moment-only FS, which is multivalued)."""
        return newton(lambda FS: _mp_residuals(A, f_vals, lam, FS)[2],
                      s, tol=tol, maxiter=max_iter)

    def h(lam):
        """Moment residual evaluated AT the force-equilibrium FS for this λ:
        ``h(λ) = moment_res(F_f(λ), λ)``. This is the key to a robust Approach A.
        `F_f(λ)` is smooth and single-valued, so `h` is a SMOOTH scalar function of λ
        alone whose root is the M-P solution (where force AND moment both close) — it
        sidesteps the multivalued moment-only FS curve `F_m(λ)` (and its asymptote)
        entirely. (This curve search is the slow-but-robust reference path; the
        Approach-B Newton, S5, is the fast path.)"""
        return _mp_residuals(A, f_vals, lam, F_f(lam, seed))[3]

    lo, hi = -1.5, 1.5      # λ search interval (sign change of F_f − F_m)

    def approach_A():
        """Robust reference (slow): scan h(λ) on a grid, brentq each sign change,
        and take the crossing nearest λ=0 (the physical one). ~61 h-evals."""
        grid = np.linspace(lo, hi, 61)
        hv = []
        for lam in grid:
            try:
                hv.append(h(lam))
            except Exception:
                hv.append(np.nan)
        hv = np.array(hv)
        crossings = []
        for i in range(len(grid) - 1):
            a, b = hv[i], hv[i + 1]
            if np.isfinite(a) and np.isfinite(b) and a * b <= 0 and not (a == 0 and b == 0):
                try:
                    crossings.append(brentq(h, grid[i], grid[i + 1], xtol=1e-9, maxiter=100))
                except Exception:
                    pass
        return min(crossings, key=abs) if crossings else None

    def approach_B():
        """Fast path (Approach B): 2-D Newton (scipy `hybr`) on the SCALED
        `(force_res, moment_res)` residuals over `(FS, λ)`, seeded at `(Bishop-FS,
        0)`. Both residuals come from ONE `_mp_march` per evaluation, so this is ~3×
        faster than the h(λ) secant (which nests a full `F_f` root-find inside every
        step). Scaling the two residuals to O(1) (they differ by ~1e3×) is what makes
        `hybr` well-conditioned; seeding near the physical solution keeps it off the
        multivalued moment-only branch. Returns λ* or None (→ fall back to A)."""
        from scipy.optimize import root
        f0 = _mp_residuals(A, f_vals, 0.0, seed)
        sf = abs(f0[2]) or 1.0       # force-residual scale at the seed
        sm = abs(f0[3]) or 1.0       # moment-residual scale at the seed

        def R(x):
            F, lam = x
            if not (np.isfinite(F) and np.isfinite(lam)) or F <= 0.05:
                return [1e3, 1e3]
            try:
                _, _, fr, mr = _mp_residuals(A, f_vals, lam, F)
            except Exception:
                return [1e3, 1e3]
            return [fr / sf, mr / sm]

        try:
            sol = root(R, [seed, 0.0], method='hybr')
        except Exception:
            return None
        F_b, lam_b = sol.x
        if not (sol.success and F_b > 0.05 and (lo - 0.5) <= lam_b <= (hi + 0.5)):
            return None
        rb = R(sol.x)                # confirm it's a true root, not a merit-fn stall
        if abs(rb[0]) < 1e-4 and abs(rb[1]) < 1e-4:
            return float(lam_b), float(F_b)   # λ* and its FS (skips a redundant re-solve)
        return None

    # RESIDUAL-SURFACE MAP (why a high-side M-P excursion is not a branch jump).
    # Mapped on the right-facing seepage sample (docs/seep xslope_rface_SEEP_KEY, 40
    # slices), whose h(λ) = moment residual evaluated at F_f(λ) falls MONOTONICALLY
    # from +2.5e7 at λ=-1.5 to -1.9e7 at λ=+1.1 and crosses zero exactly once, at
    # λ* = -0.2188 (FS 2.0797). Seeding approach_B's hybr at (FS0, 0) returns that
    # same root for every FS0 in [1.07, 5.07] and under ulp-scale jitter of the
    # Bishop seed. A 78x31 (FS0, λ0) seed grid does find other roots that pass the
    # acceptance test, but every one sits at FS <= 1.6 with |λ0| >= 1.1 — off the
    # λ0 = 0 seed line this solver actually uses, and well BELOW the physical FS.
    # There is no secondary root above it. So an M-P answer that comes back HIGH on
    # a model of this class is not the root-finder: look at the water first. The one
    # such excursion on record (3.183 against a locked 2.080, once in ~2000 rows)
    # was exactly the DRY answer for that model, to four digits. Its cause was
    # mesh.find_element_containing_point's spatial-grid cache, then keyed on
    # id(nodes): a recycled address served one model the grid of another, every
    # base point missed, and the seepage field read as u = 0 throughout. Fixed
    # there (identity test over all three arrays, strong-referenced), and slice.py
    # now refuses a surface whose seep base points ALL fall outside the mesh.
    # Note a Spencer/M-P cross-check could not have caught it: run dry, Spencer
    # gives 3.177 and M-P 3.183, agreeing to 0.2%, because losing the pore-pressure
    # field moves every method together.
    FS = None
    if solver == 'A':
        lam_star = approach_A()
    else:                       # 'auto' (default) / 'B': fast 2-D Newton, fall back to A
        b = approach_B()
        if b is not None:
            lam_star, FS = b           # B gives FS directly — no redundant F_f re-solve
        elif solver == 'auto':
            lam_star = approach_A()
        else:
            lam_star = None
    if lam_star is None:
        return False, (MPRICE_NO_CROSSING + f"λ ∈ [{lo}, {hi}].")

    # Recover N, Z, θ at λ* (FS already known from Approach B; else solve it via A's F_f).
    if FS is None:
        FS = F_f(lam_star, seed)
    N, Z, force_res, moment_res = _mp_residuals(A, f_vals, lam_star, FS)
    theta_deg = np.degrees(np.arctan(lam_star * f_vals))   # per boundary, length n+1

    # Admissibility guard, the same one force_equilibrium applies: base tension by
    # EXTENT, and nothing else. Interslice tension is reported below and never
    # refused — the measure is the same one every other method reports from, and
    # on this surface M-P's λ-optimisation reads exactly what Spencer's constant θ
    # reads (see interslice_tension_note).
    frac_N_neg = float(np.mean(N < 0))
    if frac_N_neg > MAX_BASE_TENSION_EXTENT:
        return False, (MPRICE_INADMISSIBLE +
                       f"({100*frac_N_neg:.0f}% of base normals in tension)")

    slice_df['n_eff'] = N
    slice_df['z'] = Z[:-1]
    slice_df['theta'] = theta_deg[1:]   # right-boundary interslice angle per slice
    _mp_line_of_thrust(slice_df, Z, np.arctan(lam_star * f_vals), right_facing, FS=FS)

    # Report-only admissibility screen (never affects FS/λ or acceptance). M-P
    # keeps the un-negated θ convention for both facings, so its Z is already
    # physical (tension < 0); the thrust line just stored gives the third
    # signature. On VP30 this reports interslice tension and a thrust line outside
    # the slices, the two signatures that describe how the λ-optimisation is
    # holding the mass together on that surface.
    warns = _admissibility_warnings(
        slice_df['c'].values, N, Z,
        y_lt=slice_df['y_lt'].values,
        y_lb=slice_df['y_lb'].values,
        yt_l=slice_df['yt_l'].values)

    if debug_level >= 1:
        print(f"Morgenstern-Price ({f_type}): FS = {FS:.5f}, λ = {lam_star:.5f}, "
              f"force_res = {force_res:.2e}, moment_res = {moment_res:.2e}")
        for w in warns:
            print(f"  M-P admissibility warning: {w}")

    return True, {
        'method': 'mprice',
        'FS': FS,
        'lambda': lam_star,
        'f_type': f_type,
        'theta': theta_deg,
        'warnings': warns,
    }


# =====================================================================
# Nonlinear strength coupling — options 'pow' (v12) and 'hb' (v14)
#
# Both envelopes are curved, so the shear strength depends on the base normal
# stress, which itself depends on FS. Each is handled the same way: linearize
# the envelope at the current sigma'_n into an instantaneous Mohr-Coulomb
# tangent (c_i, phi_i), solve, recompute sigma'_n, repeat until FS is
# stationary (_with_nonlinear_strength).
# =====================================================================

def _hb_update_strength(slice_df, sigma_n):
    """Re-linearize the generalized Hoek-Brown envelope at the current base
    normal stress into an instantaneous tangent (c_i, phi_i) for every
    hb-flagged slice (Balmer transformation; see xslope.hoekbrown)."""
    m = slice_df['hb_flag'].values.astype(bool)
    if not m.any():
        return
    s = np.maximum(np.asarray(sigma_n, dtype=float)[m], 0.0)
    c_i, phi_i = hb_tangent(s,
                            slice_df['hb_sci'].values[m],
                            slice_df['hb_gsi'].values[m],
                            slice_df['hb_mi'].values[m],
                            slice_df['hb_d'].values[m])
    c_vals = slice_df['c'].values.copy()
    phi_vals = slice_df['phi'].values.copy()
    c_vals[m] = c_i
    phi_vals[m] = phi_i
    slice_df['c'] = c_vals
    slice_df['phi'] = phi_vals


def _pow_update_strength(slice_df, sigma_n):
    """Re-linearize the power-curve envelope tau = a*(sigma'_n + d)^b + c_p at
    the current base normal stress into an instantaneous-tangent (c_i, phi_i)
    for every pow-flagged slice: phi_i = arctan(a*b*(sigma+d)^(b-1)) and c_i =
    tau(sigma) - sigma*tan(phi_i). sigma is clamped at zero (no tensile normal
    stress) and (sigma + d) is floored at a small fraction of the mean stress so
    b < 1 curves cannot produce an unbounded tangent slope at the origin."""
    m = slice_df['pow_flag'].values.astype(bool)
    if not m.any():
        return
    a = slice_df['pow_a'].values[m]
    b = slice_df['pow_b'].values[m]
    cp = slice_df['pow_c'].values[m]
    d = slice_df['pow_d'].values[m]
    s = np.maximum(np.asarray(sigma_n, dtype=float)[m], 0.0)
    ref = max(1.0, float(np.mean(s)) if len(s) else 1.0)
    s_eff = np.maximum(s + d, 1e-4 * ref)
    slope = a * b * np.power(s_eff, b - 1.0)
    tau = a * np.power(s_eff, b) + cp
    c_vals = slice_df['c'].values.copy()
    phi_vals = slice_df['phi'].values.copy()
    c_vals[m] = tau - s * slope
    phi_vals[m] = np.degrees(np.arctan(slope))
    slice_df['c'] = c_vals
    slice_df['phi'] = phi_vals


def _has_nonlinear(slice_df):
    """True if any slice sits on a curved envelope ('pow' or 'hb')."""
    for flag in ('pow_flag', 'hb_flag'):
        if flag in slice_df.columns and slice_df[flag].any():
            return True
    return False


def _with_nonlinear_strength(method):
    """Outer fixed-point wrapper giving every solution method curved-envelope
    support ('pow' and 'hb'): solve with the current tangent strengths, update
    sigma'_n from the method's n_eff, re-tangent, repeat until FS is stationary.
    slice_df arrives seeded with tangent strengths at a no-FS normal-stress
    estimate (slice.py), so the first inner solve is already close. Damped (50%)
    sigma updates prevent oscillation on strongly curved envelopes."""
    import functools

    @functools.wraps(method)
    def wrapped(slice_df, *args, **kwargs):
        if not _has_nonlinear(slice_df):
            return method(slice_df, *args, **kwargs)
        dl = slice_df['dl'].values.astype(float)
        sigma = None
        fs_prev = None
        for _ in range(40):
            ok, res = method(slice_df, *args, **kwargs)
            if not ok:
                return ok, res
            n_eff = slice_df['n_eff'].values.astype(float)
            sigma_new = np.where(dl > 0, n_eff / np.where(dl > 0, dl, 1.0), 0.0)
            sigma = sigma_new if sigma is None else 0.5 * sigma + 0.5 * sigma_new
            if 'pow_flag' in slice_df.columns:
                _pow_update_strength(slice_df, sigma)
            if 'hb_flag' in slice_df.columns:
                _hb_update_strength(slice_df, sigma)
            if fs_prev is not None and abs(res['FS'] - fs_prev) < 1e-4:
                return ok, res
            fs_prev = res['FS']
        return False, ("Nonlinear strength iteration did not converge in 40 outer "
                       "iterations (envelope tangent vs normal stress).")
    return wrapped


# Rebind the public solution methods with the nonlinear-strength outer loop.
# Import-time rebinding covers both `solve.oms(...)` attribute lookups and
# `from xslope.solve import oms` (imports resolve after module execution).
oms = _with_nonlinear_strength(oms)
bishop = _with_nonlinear_strength(bishop)
janbu = _with_nonlinear_strength(janbu)
spencer = _with_nonlinear_strength(spencer)
corps = _with_nonlinear_strength(corps)
lowe = _with_nonlinear_strength(lowe)
mprice = _with_nonlinear_strength(mprice)
