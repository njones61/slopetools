"""Page config: docs/verification/rocscience_groundwater.md (RS2 groundwater).

Figure mode: ``panel``.  The corpus figures are a fixed two-panel composite —
mesh on the left, solved heads on the right — and the caption says exactly that,
so the caption makes a layout claim the classifier can read back off the PNG.
The transient/profile figures at the end of the page (isochrones, head along a
query line, an erfc profile) are plotted by different scripts at whatever panel
count the comparison needs and their captions make no layout claim, so each is
named in ``caption_exempt`` rather than left in a silent "other" bucket.
"""
from ..config import PageConfig

CONFIG = PageConfig(
    name="rocscience_groundwater",

    bounds=[
        # the match-dot legend, not a comparison
        ('+3', 'within 3% of the vendor and/or reference figure'),
        ('+6', '| 🟡 | 3–6% |'),
        ('+6', 'more than 6% |'),
        # van Genuchten vs SEEP2D on the linear-front problems, as a set
        ('+0.15', 'agree on discharge to better than'),
    ],

    whitelist=[
        # the 3.5–4.7% van Genuchten band, quoted ahead of the two case pairs
        # it summarises (gw009a 2.307 against SEEP2D's 2.421)
        ('+4.7', 'the total discharge reads 3.5–4.7% below SEEP2D', '2.307', '2.421'),
    ],

    # Percentages expressed as a share of a reference quantity
    not_a_comparison_extra=[
        r"of \$u_0\$",
        r"of u₀",
        r"of the driving head",
        r"of the profile's head range",
        r"of the 0\.25 m divide mound",
        r"of the 0\.56 m head range",
        r"of the 45 m dam",
    ],

    auth_hdr_extra=[r"Slide2?\b", r"Ref \[1\]", r"SEEP2D", r"Eqs? 4\.", r"Vedernikov", r"Clement",
                    r"Kozeny", r"Terzaghi", r"Pyrah", r"Ferris"],

    tag_value_keys=['expected_fs*', 'fs_*', 'expected_flowrate*',
                    'expected_head*', 'expected_beta', 'expected_kc',
                    'points', 'expected'],
    # this page's tables print solved heads to the precision each comparison is
    # read at — two decimals where the probe locks three — so a correctly
    # rounded restatement satisfies the tag.  The discharge locks are all in
    # exponential notation and are matched by their mantissa and exponent, so
    # they are unaffected by this.
    tag_round_dp=2,
    # Regression locks on XSLOPE's own discharge, which the page deliberately
    # does not publish as a comparison: GW2 says "flowrate is locked as a
    # regression value" (the manual publishes head points, not Q), and GW11
    # says the tag "locks XSLOPE's own flowrate rather than a published one"
    # because the manual does not print k_s for that case.
    tag_exempt=[
        ('4.534e-06', 'benchmark=GW2-q'),
        ('7.820e-07', 'benchmark=GW11-q'),
    ],

    # How much of each head-probe set the section publishes, where it does not
    # publish all of it.  The sets not named here are printed in full and are
    # machine-checked element by element: GW2 and GW3 as total head, GW6's
    # four cases and GW19's near-steady top-boundary frame as pressure head
    # (h − y at the probe), GW17's two later frames in prose.
    tag_list_published=[
        # "a head regression at three interior stations guards the mound
        # shape"; the section publishes the crest position and elevation.
        ('benchmark=GW1-h', 0),
        # the section publishes the phreatic elevations at x = 14 / 18 / 20,
        # y₁, x₁ and Q; the four probes guard the solved field.
        ('benchmark=GW4-h', 0),
        # chart target: the lock is XSLOPE's own field, published as a band
        # comparison (46 of Fig 5-4's 49 grid points).
        ('benchmark=GW5-h', 0),
        # "the three-station regression that guards the solved field".
        ('benchmark=GW7-h', 0),
        # four of the five query-line stations are columns of the published
        # Fig 22.7 profile; the y = 0.8 probe falls between its 0.85 and 0.70.
        ('benchmark=GW7-q22', 4),
        # the section publishes 0.253 (water table at the symmetry edge) and
        # 0.347 (total head at the top of that edge); the other three stations
        # of the five-station lock guard the solved field.
        ('benchmark=GW8-h', 2),
        # the published quantity is the release point; the five heads are a
        # regression guard, like the flowrate lock beside them.
        ('benchmark=GW11-h', 0),
        # the consolidation sections publish the agreement with the closed-form
        # (GW15) and recomputed (GW16) series as a percentage of u₀, plus the
        # isochrone figures; the locked heads themselves are not printed.
        ('benchmark=GW15', 0),
        ('benchmark=GW16', 0),
        # the 15 h frame is compared as a front position (1.1–1.8 m inside the
        # upstream face), not as station heads.
        ('benchmark=GW17-t15', 0),
        # two of the four probe stations, x = 30 and x = 40, are columns of the
        # digitized Fig 20.5 profile table; 35 and 45 are not stations of it.
        ('benchmark=GW18-t', 2),
        # the section publishes the near-steady top-boundary profile (locked in
        # full by GW19-top-t11340) and the rms of the early frames; the three
        # interior probes per frame are a regression guard.  At 73 min the
        # counter also sees one of them: the (1, 5) probe is 0.033 m of
        # pressure head, which rounds onto a +0.03 residual the near-steady
        # table prints.
        ('benchmark=GW19-t73', 1),
        ('benchmark=GW19-t416', 0),
        ('benchmark=GW19-t792', 0),
        ('benchmark=GW19-t11340', 0),
        # the section publishes the agreement with Ferris' erfc solution
        # (0.015 ft across the domain) and the profile figure.
        ('benchmark=GW21', 0),
    ],
    # the summary rows quote discharges, heads and offsets in physical units
    # rather than a fixed-precision factor of safety, so there is no
    # locked-value pattern to sweep against the tags
    locked_value_re=None,

    figure_mode="panel",
    caption_rules=[
        ("mesh and solved heads", "two"),
    ],
    # Series and profile figures: the caption names what is plotted against
    # what, and claims no panel layout.
    caption_exempt={
        "images/gw015.png",
        "images/gw016.png",
        "images/gw017.png",
        "images/gw018.png",
        "images/gw019.png",
        "images/gw020.png",
        "images/gw021.png",
    },
)
