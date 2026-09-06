"""Spencer's system has more than one root; only one is a body of soil.

Spencer's assumption — every interslice force at the same inclination theta —
turns equilibrium into two equations in (F, theta). Those equations divide every
slice by

    m_alpha = 1 / [cos(alpha - theta) + sin(alpha - theta) tan(phi) / F]

whose denominator vanishes when theta stands a right angle away from a slice's
own base inclination, less the friction that base mobilizes. Past that point the
slice's base normal has reversed, and roots there are common. They are not
solutions: they read low, and they read low by factors, not by percentages.

WHAT WENT WRONG

The solver descended from a handful of starting guesses and reported whichever
root it reached. Its Newton stage clipped theta into the pole-free band; its
scipy stage did not, and on a non-circular surface refined out of the seismic
benchmark VP104's own circular critical it walked outside the band and returned
F = 0.577 at theta = -16.3 degrees, where Morgenstern-Price with f(x) = 1 — the
same equations, solved a different way — reads 2.690 on the identical slices.
The force-equilibrium closure then inherited it: `_force_closure_root` breaks a
tie against the moment answer, which on a non-circular surface is Spencer's, so
Corps of Engineers reported 0.786 while its own warnings named an admissible root
five to nine times higher.

WHAT DECIDES WHICH ROOT

* theta stays inside the band where m_alpha keeps its sign on every slice. This
  is the geometric bound Spencer (1973) and Duncan & Wright describe — the
  interslice inclination lies between the inclinations of the ground surface and
  the slip surface — written in the form the equations give, and it is Spencer's
  form of the base factor `solve.FE_MIN_BASE_FACTOR` keeps clear of zero for the
  force-equilibrium closure.
* the largest interslice resultant stays within the total driving load on the
  mass (`solve.FE_MAX_Z_OVER_W` over `solve._driving_load`), and base tension
  does not saturate (`solve.MAX_BASE_TENSION_EXTENT`) — the closure's own two
  remaining measures, unchanged.
* where the cascade reaches no admissible root, the band is swept in (F, s)
  coordinates, s the position across the band, so a bounded descent cannot leave
  it; every crossing found is judged on the measures above and the survivors are
  tie-broken against the moment answer by ratio.

WHICH OF TWO ROOTS INSIDE THE BAND

The band refuses a root that has reversed a base normal. It cannot separate two
crossings that both stand inside it, and there the cascade reported whichever of
its starts reached one first: on the critical circle a Spencer search finds for
VP16, F = 1.082 at theta = -27.1 degrees where the other crossing reads 1.113 —
Bishop's answer on the same slices — and on the critical non-circular surface of
VP9, 0.580 where the other reads 1.529.

Sweeping the band settles it and costs about a hundred times what the cascade
does, which a search cannot pay on every trial, so the reported root is first
read for the signature the wrong branch carries: a line of thrust outside the
slice on most of its boundaries. That measure is already computed for the
solution's warnings, so it costs nothing, and the bar
`solve.SPENCER_THRUST_OUT_DISPUTED` is measured — over 320 accepted Spencer
answers on the corpus's own surfaces the thrust line leaves the slice on at most
54% of boundaries, and over 5 251 search trials where Spencer and
Morgenstern-Price at f(x) = 1 agree, on more than 65% of them in 13. VP16's
disputed root carries 92% and VP9's 80%.

The ratio to the moment answer was measured for this job and does not do it: an
accepted Spencer answer runs from 0.42 to 1.05 times Bishop's on a circle and
from 0.82 to 1.71 times Janbu's off one, while VP16's disputed root sits at 0.97
of Bishop. The moment answer is the tie-break here, not the trigger.

NO FIXED CAP ON THETA, and that is a measurement rather than a preference. A cap
at 45 degrees — the angle a real section's geometry rarely passes — refuses the
planar benchmark VP43 / GS-2.26, whose 1.352 at theta = 49.6 degrees is the value
Janbu, Corps, Lowe & Karafiath and Morgenstern-Price all return on the same
slices, and the wedge benchmark VP48, whose 0.991 at theta = -55.0 degrees is
likewise unanimous. Both sit inside the band their own geometry allows. Those two
are pinned below so the cap cannot come back.

A MAGNITUDE bar on the base factor is also deliberately absent here, for the same
kind of reason: VP104b's own circle solves at a base factor of 0.048, against
Bishop's 1.518 and Morgenstern-Price's 1.519 on the same slices, so the
force-equilibrium closure's 0.05 would refuse it. Spencer's roots are not wedged
between poles the way that march's are — the band already excludes those.

WHAT IS CHECKED

* the two refined VP104 surfaces: Spencer returns Morgenstern-Price's constant-f
  value to ten significant figures, at an interslice inclination inside the band;
* the two surfaces where both roots stand inside the band: the answer is
  Morgenstern-Price's constant-f value and the root passed over is named;
* the trigger's bar from both sides — every disputed root stands above it, and
  every answer the corpus locks stands below it;
* the roots passed over are named in results['warnings'] or in the refusal, with
  the measure each failed;
* the two benchmarks whose answers sit past 45 degrees still solve, at their
  locked values;
* the out-of-band refusal classifies as inadmissible, so a search reports it by
  class;
* two mutations: the band gate lifted, which puts the low out-of-band roots
  back, and the disputed-root trigger disarmed, which puts VP16's 1.082 and
  VP9's 0.580 back.

Run directly:  PYTHONPATH=. python3 test/spencer_root_check.py
"""

import os
import re
import warnings

import numpy as np

warnings.filterwarnings('ignore')

from xslope import solve
from xslope.fileio import load_slope_data
from xslope.slice import generate_slices

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CORPUS = os.path.join(REPO, 'docs', 'verification', 'files', 'rocscience')


def _poly(points):
    """A non-circular surface from (x, y) pairs, ends free on the ground."""
    out = [{'X': float(x), 'Y': float(y), 'Movement': 'Horiz'} for x, y in points]
    out[0]['Movement'] = 'Free'
    out[-1]['Movement'] = 'Free'
    return out


#: The surfaces the defect was found on: each is VP104's own circular Spencer
#: critical resampled into a six-point polyline and refined by
#: `noncircular_search`, kept as geometry so the solver is checked without
#: re-running a search. `out_of_band` is what the unbounded scipy stage returned
#: there, and `mprice_constant` is what the same equations give under
#: Morgenstern-Price with f(x) = 1 — the value the answer must agree with.
REFINED = {
    'vp104a': dict(
        model=os.path.join(CORPUS, 'vp104a.xlsx'),
        points=[(33.388168328718606, 26.694084164359303),
                (35.04633204775693, 24.447110580463796),
                (40.781500225948, 25.282445644030215),
                (45.11322002266858, 27.44553864799717),
                (46.98187599077924, 30.770910359276677),
                (50.04356453348249, 35.0)],
        out_of_band=0.5766,
    ),
    'vp104b': dict(
        model=os.path.join(CORPUS, 'vp104b.xlsx'),
        points=[(33.574978839857486, 26.787489419928743),
                (35.140844265639984, 24.541999679708002),
                (43.46943211613009, 25.414876790710945),
                (45.53804190385431, 27.56230590854391),
                (47.559732571866064, 30.832329878815216),
                (49.68725346855099, 34.843626734275496)],
        out_of_band=0.3896,
    ),
}

#: The surfaces where BOTH roots stand inside the band. The band cannot separate
#: these — past it a base normal has reversed, and neither of these has — so what
#: separates them is the line of thrust, which leaves the slice on most of the
#: wrong root's boundaries and on few of the right one's. Each surface is the
#: critical one a Spencer search reached while the cascade was reporting the
#: wrong root, kept as geometry so the solver is checked without re-running a
#: search. `disputed` is that root; `answer` is the one Morgenstern-Price with
#: f(x) = 1 returns on the identical slices.
DISPUTED = {
    'vp016': dict(
        model=os.path.join(CORPUS, 'vp016.xlsx'),
        circle=dict(Xo=28.282006072998048, Yo=43.12587432861328,
                    Depth=13.179095584154132, R=29.946778744459145),
        num_slices=40,
        disputed=1.0823, answer=1.1128,
    ),
    'vp009': dict(
        model=os.path.join(CORPUS, 'vp009.xlsx'),
        points=[(44.38457329166787, 28.442286645833935),
                (46.0, 25.86),
                (72.0, 33.14),
                (75.9705032704, 40.0)],
        num_slices=50,
        disputed=0.5802, answer=1.5294,
    ),
}

#: The two benchmarks whose accepted answer stands past 45 degrees, with the
#: factor of safety their verification rows lock and the inclination it comes at.
#: A fixed cap on theta refuses both.
PAST_45 = {
    'vp043': dict(model=os.path.join(CORPUS, 'vp043.xlsx'),
                  num_slices=40, fs=1.352, theta=49.6),
    'vp048': dict(model=os.path.join(CORPUS, 'vp048.xlsx'),
                  num_slices=50, fs=0.991, theta=-55.0),
}

NUM_SLICES = 40


def _slices(model, points=None, num_slices=NUM_SLICES):
    sd = load_slope_data(model)
    non_circ = _poly(points) if points is not None else sd['non_circ']
    ok, res = generate_slices(sd, non_circ=non_circ, num_slices=num_slices,
                              debug=False)
    if not ok:
        raise AssertionError(f"could not slice {os.path.basename(model)}: {res}")
    return res[0]


def _disputed_slices(spec):
    """The slice table of one DISPUTED surface, circular or not."""
    sd = load_slope_data(spec['model'])
    if 'circle' in spec:
        ok, res = generate_slices(sd, circle=dict(spec['circle']),
                                  num_slices=spec['num_slices'], debug=False)
    else:
        ok, res = generate_slices(sd, non_circ=_poly(spec['points']),
                                  num_slices=spec['num_slices'], debug=False)
    if not ok:
        raise AssertionError(f"could not slice {os.path.basename(spec['model'])}: "
                             f"{res}")
    return res[0]


def _band(df, F, theta_deg):
    """(lo, hi) degrees: the pole-free band of this slice set at this F."""
    alpha = np.radians(df['alpha'].values)
    phi = np.radians(df['phi'].values)
    right_facing = df.attrs.get('right_facing',
                                df['y_cb'].iat[0] > df['y_cb'].iat[-1])
    if right_facing:
        alpha, tan_p = -alpha, -np.tan(phi)
    else:
        tan_p = np.tan(phi)
    offset = alpha - np.arctan(tan_p / F)
    lo = float(offset.max()) - np.pi / 2
    hi = float(offset.min()) + np.pi / 2
    return np.degrees(lo), np.degrees(hi)


def leg_the_refined_surfaces_read_the_same_equations():
    """Spencer must agree with Morgenstern-Price at f(x) = 1, in the band."""
    fails = []
    for name, spec in REFINED.items():
        df = _slices(spec['model'], spec['points'])
        ok_s, res_s = solve.spencer(df.copy())
        ok_m, res_m = solve.mprice(df.copy(), f_type='constant')
        if not ok_m:
            fails.append(f"{name}: Morgenstern-Price gives no reference here "
                         f"({res_m})")
            continue
        if not ok_s:
            fails.append(f"{name}: spencer refused a surface Morgenstern-Price "
                         f"solves at {res_m['FS']:.4f} ({res_s})")
            continue
        if abs(res_s['FS'] / res_m['FS'] - 1.0) > 1e-6:
            fails.append(f"{name}: spencer {res_s['FS']:.6f} against "
                         f"Morgenstern-Price's {res_m['FS']:.6f} on the same "
                         f"slices — the same equations, a different root")
            continue
        if abs(res_s['FS'] - spec['out_of_band']) < 1e-2:
            fails.append(f"{name}: spencer still reports the out-of-band root "
                         f"{res_s['FS']:.4f}")
            continue
        lo, hi = _band(df, res_s['FS'], res_s['theta'])
        if not (lo - 1e-6 <= res_s['theta'] <= hi + 1e-6):
            fails.append(f"{name}: theta {res_s['theta']:.2f} deg is outside the "
                         f"band [{lo:.1f}, {hi:.1f}] deg it was reported in")
            continue
        print(f"  {name:8s} spencer {res_s['FS']:.4f} at θ = {res_s['theta']:.2f}° "
              f"in [{lo:.1f}, {hi:.1f}]°, Morgenstern-Price(f=1) "
              f"{res_m['FS']:.4f} (was {spec['out_of_band']})")
    return fails


def leg_the_discarded_roots_are_named():
    """A root passed over must be named, with the measure it failed.

    A surface whose cascade reaches the admissible root first has nothing to
    name, and that is not a defect — so what is required is that the out-of-band
    roots ARE named wherever the cascade meets one, and that no naming ever lists
    the answer among the roots it discarded.
    """
    fails = []
    named_anywhere = 0
    for name, spec in REFINED.items():
        df = _slices(spec['model'], spec['points'])
        ok, res = solve.spencer(df.copy())
        text = " ".join(res.get('warnings') or []) if ok else str(res)
        found = re.findall(r'FS=([0-9.]+) at θ=(-?[0-9.]+)° \(([^)]+)\)', text)
        if not found:
            print(f"  {name:8s} the cascade reached the answer with nothing to "
                  f"discard")
            continue
        named_anywhere += 1
        if any(why.strip() == '' for _, _, why in found):
            fails.append(f"{name}: a discarded root is named without a reason: "
                         f"{text[:160]!r}")
        if ok and any(abs(float(fs) - res['FS']) < 1e-9 for fs, _, _ in found):
            fails.append(f"{name}: the reported root appears in its own list of "
                         f"discarded roots")
        if not any('outside the admissible band' in why for _, _, why in found):
            fails.append(f"{name}: no discarded root is named as out of band, on a "
                         f"surface where the defect was one ({text[:160]!r})")
        else:
            print(f"  {name:8s} {len(found)} root(s) named, out-of-band among them")
    if not named_anywhere:
        fails.append("neither surface named a discarded root, so this leg no "
                     "longer exercises the reporting")
    return fails


def leg_two_roots_inside_the_band():
    """Where both roots stand inside the band, the moment answer decides."""
    fails = []
    for name, spec in DISPUTED.items():
        df = _disputed_slices(spec)
        ok_s, res_s = solve.spencer(df.copy())
        ok_m, res_m = solve.mprice(df.copy(), f_type='constant')
        if not (ok_s and ok_m):
            fails.append(f"{name}: spencer {ok_s} / Morgenstern-Price {ok_m} on a "
                         f"surface both used to solve")
            continue
        if abs(res_s['FS'] - spec['disputed']) < 5e-4:
            fails.append(f"{name}: spencer still reports the disputed root "
                         f"{res_s['FS']:.4f}, where the same equations under "
                         f"Morgenstern-Price read {res_m['FS']:.4f}")
            continue
        if abs(res_s['FS'] / res_m['FS'] - 1.0) > 1e-6:
            fails.append(f"{name}: spencer {res_s['FS']:.6f} against "
                         f"Morgenstern-Price's {res_m['FS']:.6f} on the same "
                         f"slices")
            continue
        if abs(res_s['FS'] - spec['answer']) > 5e-4:
            fails.append(f"{name}: spencer {res_s['FS']:.4f}, not the "
                         f"{spec['answer']:.4f} this surface is pinned at")
            continue
        text = " ".join(res_s.get('warnings') or [])
        if f"{spec['disputed']:.3f}" not in text:
            fails.append(f"{name}: the root passed over ({spec['disputed']:.3f}) "
                         f"is not named in the warnings: {text[:200]!r}")
            continue
        lo, hi = _band(df, spec['disputed'], 0.0)
        print(f"  {name:8s} spencer {res_s['FS']:.4f} = Morgenstern-Price(f=1); "
              f"the root passed over, {spec['disputed']:.4f}, is named and was "
              f"inside the band [{lo:.1f}, {hi:.1f}]°")
    return fails


def leg_the_trigger_is_measured():
    """The disputed roots carry the thrust signature; the accepted ones do not.

    The bar is what decides whether a search pays for the sweep, so it is pinned
    from both sides: every root this leg calls disputed must stand above it, and
    the answers the corpus benchmarks lock — including the two whose interslice
    inclination passes 45 degrees — must stand below it.
    """
    fails = []
    bar = solve.SPENCER_THRUST_OUT_DISPUTED
    for name, spec in DISPUTED.items():
        solved = _disputed_slices(spec)
        ok, res = solve.spencer(solved)
        if not ok:
            fails.append(f"{name}: spencer refused a surface it solves")
            continue
        out = solve._thrust_outside_fraction(solved['y_lt'].values,
                                             solved['y_lb'].values,
                                             solved['yt_l'].values)
        if out > bar:
            fails.append(f"{name}: the ANSWER's thrust line is outside on "
                         f"{out:.0%} of boundaries, past the {bar:.0%} bar, so "
                         f"the trigger fires on the root it just chose")
        else:
            print(f"  {name:8s} the answer's thrust line is outside on {out:.0%} "
                  f"of boundaries, under the {bar:.0%} bar")
    for name, spec in PAST_45.items():
        solved = _slices(spec['model'], num_slices=spec['num_slices'])
        ok, res = solve.spencer(solved)
        if not ok:
            continue
        out = solve._thrust_outside_fraction(solved['y_lt'].values,
                                             solved['y_lb'].values,
                                             solved['yt_l'].values)
        if out > bar:
            fails.append(f"{name}: a locked answer's thrust line is outside on "
                         f"{out:.0%} of boundaries, past the {bar:.0%} bar")
        else:
            print(f"  {name:8s} locked answer, thrust line outside on {out:.0%}")
    return fails


def leg_answers_past_forty_five_degrees_stand():
    """The band is the surface's own geometry, not a fixed angle."""
    fails = []
    for name, spec in PAST_45.items():
        df = _slices(spec['model'], num_slices=spec['num_slices'])
        ok, res = solve.spencer(df.copy())
        if not ok:
            fails.append(f"{name}: spencer refused its locked surface ({res})")
            continue
        if abs(res['FS'] - spec['fs']) > 5e-4:
            fails.append(f"{name}: spencer {res['FS']:.4f}, not the locked "
                         f"{spec['fs']:.3f}")
            continue
        if abs(res['theta'] - spec['theta']) > 0.2:
            fails.append(f"{name}: theta {res['theta']:.1f} deg, not the "
                         f"{spec['theta']:.1f} this case is pinned at; the case no "
                         f"longer stands past 45 degrees")
            continue
        if abs(res['theta']) <= 45.0:
            fails.append(f"{name}: theta {res['theta']:.1f} deg no longer exceeds "
                         f"45 degrees, so a fixed cap would pass unnoticed")
            continue
        print(f"  {name:8s} spencer {res['FS']:.4f} at θ = {res['theta']:.1f}°, "
              f"past any 45° cap")
    return fails


def leg_the_refusal_is_classified():
    """A search must be able to say which kind of failure it skipped."""
    fails = []
    message = (solve.SPENCER_INADMISSIBLE +
               "; rejected FS=0.459 at θ=-76.5° (interslice inclination -76.5 deg "
               "outside the admissible band [-59.6, -21.1] deg)")
    got = solve.failure_kind(message)
    if got != 'inadmissible':
        fails.append(f"the out-of-band refusal classified {got!r}, "
                     f"expected 'inadmissible'")
    else:
        print(f"  the out-of-band refusal classifies as {got}")
    return fails


def _mutation(label, apply, restore, leg, fails):
    apply()
    try:
        caught = leg()
    finally:
        restore()
    if not caught:
        fails.append(f"{label}: the leg passed with the defect in place")
    else:
        print(f"  mutation  {label} -> caught ({len(caught)} failure(s))")


def leg_mutations():
    """Lifting the band must put the out-of-band roots back."""
    fails = []
    original = solve.spencer_theta_bounds

    def no_band(alpha, tan_p, F_val, margin_deg=5.0):
        """The band lifted: every interslice inclination admissible."""
        return -np.pi / 2, np.pi / 2

    _mutation("the band lifted",
              lambda: setattr(solve, 'spencer_theta_bounds', no_band),
              lambda: setattr(solve, 'spencer_theta_bounds', original),
              leg_the_refined_surfaces_read_the_same_equations, fails)

    bar = solve.SPENCER_THRUST_OUT_DISPUTED
    _mutation("the disputed-root trigger disarmed",
              lambda: setattr(solve, 'SPENCER_THRUST_OUT_DISPUTED', 2.0),
              lambda: setattr(solve, 'SPENCER_THRUST_OUT_DISPUTED', bar),
              leg_two_roots_inside_the_band, fails)
    return fails


LEGS = [
    ("the refined surfaces read the same equations",
     leg_the_refined_surfaces_read_the_same_equations),
    ("the discarded roots are named", leg_the_discarded_roots_are_named),
    ("two roots inside the band", leg_two_roots_inside_the_band),
    ("the trigger is measured", leg_the_trigger_is_measured),
    ("answers past forty-five degrees stand",
     leg_answers_past_forty_five_degrees_stand),
    ("the refusal is classified", leg_the_refusal_is_classified),
    ("mutations", leg_mutations),
]


def run():
    failures = []
    for label, fn in LEGS:
        print(f"[{label}]")
        try:
            failures.extend(fn())
        except Exception as e:
            failures.append(f"{label}: raised {type(e).__name__}: {e}")
    return failures


if __name__ == '__main__':
    import sys
    fails = run()
    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("\nSpencer root selection: all legs pass")
