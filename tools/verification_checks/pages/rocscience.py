"""Page config: docs/verification/rocscience.md (Rocscience Slide2 corpus).

Figure mode: ``panel``.  The corpus figures are a fixed two-panel composite —
model inputs on the left, the representative solution on the right — and every
caption says so ("inputs and ... solution", "inputs and the shallow mechanism"),
which is a layout claim the classifier reads back off the PNG.  The one
transient rapid-drawdown curve at VP102 is a single time-series axes whose
caption makes no layout claim, so it is named in ``caption_exempt``.
"""
from ..config import PageConfig

CONFIG = PageConfig(
    # Strength-envelope coefficients written the way a factor of safety is:
    # Baker's power-curve tau = A * sigma'^b on VP44/VP45 and the London-clay
    # offset inside (sigma' + 0.152) on VP61 are inputs, not measurements.
    untagged_allow=[
        ('1.107', 'power curve'),
        ('0.86', 'power curve'),
        ('1.107', 'Power-curve case'),
        ('0.86', 'Power-curve case'),
        ('0.152', 'power curve'),
    ],
    name="rocscience",

    bounds=[
        # ---- agreement bounds over a set of surfaces, cases or stations ----
        ('+0.3', 'Janbu/Spencer within 0.3% of Slide'),
        ('+0.3', 'Spencer within 0.3% on both'),
        ('−2.8', 'runs from −2.8% to +0.2%'),
        ('+0.2', 'runs from −2.8% to +0.2%'),
        ('−0.5', "benchmark diagnostic (−0.5% at Slide2's K"),
        ('−3.0', 'with the plain static-head `u=piezo`'),
        ('+0.7', 'and it lands within 0.7% of Slide on both circles'),
        ('+0.6', 'within 0.6% of Bishop'),
        ('+3', 'brackets the factor of safety within 1–3%'),
        ('+1', "Morgenstern–Price lands within 1% of W&H's 2.36"),
        ('+0.6', "reproduces Slide's Bishop values within 0.6%"),
        ('+1.6', "Ng & Shi's own published Bishop values within 1.6%"),
        ('+2', 'halving or doubling a moves FS by'),
        ('+19', 'FS with FE pore pressures is 14–19% lower'),
        ('+13', 'guts the artesian pressures and reads'),
        ('+40', 'u at the toe 40% above hydrostatic'),
        ('+65', 'and 65% at 5 ft depth'),
        ('+0.5', 'Every method within 0.5%'),
        ('+0.6', 'The FE case lands within 0.6% of Slide'),
        ('+6', 'the critical circle is a shallow toe surface'),
        ('+2', 'on the exact vertices both methods land within'),
        ('+0.7', 'the whole family tracks Slide within 0.7%'),
        ('+1', 'and D&W within 1%'),
        ('+0.5', 'XSLOPE lands within 0.5% of Slide (1.527 vs 1.534)'),
        ('+3', 'worth about 3% of the factor of safety'),
        ('+3', 'every station sits within 3% of the Slide2 Spencer column'),
        ('+0.6', 'Every optimized value sits within 0.6% of Slide2'),
        ('+0.1', 'The two published columns agree to about 0.1%'),
        ('+0.8', 'Every other case agrees with Slide within 0.8%'),
        ('+2.4', 'and with the originating paper within 2.4%'),
        ('+0.5', "within 0.5% of Slide's limit-filtered search"),
        ('+0.7', "Slide's constrained block search lands within 0.7%"),

        # ---- probabilities of failure and reliability spreads ----
        ('+18', "reproduces Duncan's own 18% almost exactly"),
        ('+18', "sits below Duncan's 18%"),
        ('+18', '18% (Duncan 2000 TSPM)'),
        ('+33', '30–33% (D&W 2014'),
    ],

    whitelist=[
        # VP20: the theory value XSLOPE reproduces exactly is the table's 2.500,
        # and these two sentences measure the OTHER programs against it
        ('+1.4', 'reads ~1.4% high', '2.534', '2.500'),
        ('+3.6', 'sits ~3.6% below theory', '2.41', '2.500'),
        # theory bracket: Slide2 against the exact 1.0 the sentence states
        ('−5.9', 'against theory', '0.941', '1.0'),
        # Bishop/Spencer pair cells: the delta pair is printed as one cell, so
        # the FIRST member's two operands are named (the second reconciles from
        # the last number before it)
        ('−1.8', '| Piezometric line |', '1.070', '1.090'),
        ('−0.6', '| tangent 15 ft |', '1.389', '1.398'),
        ('−0.6', '| I: c<sub>u</sub> = 200 + 15·z |', '1.305', '1.313'),
        ('−0.5', '| II: c<sub>u</sub> = 300 |', '1.328', '1.335'),
        ('−0.4', '| II | 5 |', '0.905', '0.909'),
        ('−0.3', '| III | 10 |', '1.042', '1.045'),
        # Cai & Ugai D1/D = 3: the two published values against each other
        ('+4.4', 'Slide sits 4.4% above the paper', '1.43', '1.37'),
    ],

    worded_ok=[
        # a qualitative characterisation of the sensitivity endpoints, not a
        # comparison of two printed factors
        "within about a percent at every endpoint",
    ],

    # Percentages expressed as a share of a quantity, or as a parameter range
    not_a_comparison_extra=[
        r"of their means",
        r"of the fill strength",
        r"of the gabion fill",
        r"of the displacement",
        r"filled",
    ],
    # Quantities identified by what PRECEDES them: a coefficient of variation
    # is a value, not a difference.
    not_a_comparison_prefix=[
        r"COV(?: of)? ",
    ],
    # Reliability tables: the beta / probability-of-failure columns hold
    # probabilities, not comparisons
    share_hdr_extra=[r"\bPF\b", r"σ_F", r"RI_ln"],
    # Rows whose cells are percent CHANGES or probabilities rather than
    # comparisons; the sensitivity rows say so in their own Note cell
    share_rows=[
        '| ΔFS over the A range',
        '| ΔFS over the b range',
        '| β_ln → PF |',
    ],

    auth_hdr_extra=[r"Slide\b", r"Slide2", r"SLOPE/W", r"UTEXAS4", r"WINSTABL",
                    r"XSTABL", r"Cai & Ugai", r"Sheahan", r"El-Ramly",
                    r"Borges & Cardoso", r"C&X", r"W&H", r"Chowdhury",
                    r"Pockoski", r"theory"],

    tag_value_keys=['expected_fs*', 'fs_*', 'expected_beta', 'expected_kc',
                    'expected_flowrate*', 'expected_head*', 'points',
                    'expected'],
    tag_round_dp=2,
    locked_value_re=None,

    figure_mode="panel",
    caption_rules=[
        ("inputs and", "two"),
        ("FS vs A and b", "two"),
    ],
    # the one time-series figure on the page: a factor-of-safety curve against
    # Slide2's own table, claiming no panel layout
    caption_exempt={
        "images/vp102t_curve.png",
    },
)
