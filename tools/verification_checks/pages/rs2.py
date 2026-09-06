"""Page config: docs/verification/rs2.md (RS2 finite-element corpus).

Figure mode: ``panel``.  Every figure on this page is produced by one figure
builder with a fixed set of layouts — a 2x2 composite (inputs, mesh, max shear
strain, displacement vectors), a side-by-side LEM pair, or an inputs-only single
axes — so the caption makes a checkable claim about how many panels the reader
will see, and the classifier reads that claim back off the PNG.
"""
from ..config import PageConfig

CONFIG = PageConfig(
    name="rs2",

    # Cross-scope comparisons: the two numbers live in different sentences, or
    # in a table the sentence refers to.  Each entry spells both out and is
    # re-derived.  Several are deliberate vendor-against-vendor statements the
    # page makes in its own voice rather than XSLOPE-against-source.
    #   (printed, distinctive substring of the line, value-for, value-against)
    whitelist=[
        ('+2.1', '[RS2-63](#rs2-63)', '1.409', '1.38'),
        ('+4.8', 'the other φ = 0 foundation problem', '1.477', '1.41'),
        ('+9.0', 'is not a search that stopped early', '0.169', '0.155'),
        ('+2.7', 'the three locks within ±2.7%', '0.339', '0.33'),
        ('−1.3', 'which XSLOPE sits', '1.323', '1.34'),
        ('+1.8', 'The same uncapped machinery is within 1.8%', '1.669', '1.64'),
        ('+3.2', 'baseline is within 3.2% at every frame', '1.713', '1.77'),
        ('+1.1', 'The two vendor numbers landing within', '1.9', '1.88'),
        ('+2.5', 'the three answers agree within', '1.25', '1.219'),
        ('+1.9', 'that rounding is worth', '0.997', '0.978'),
        ('+15.6', "above Slide2's own Spencer on an identical slope", '1.11', '0.960'),
        ('+3.0', 'one count in the last place', '0.34', '0.33'),
        ('+23.2', 'GEO FEM reads 23.2% above', '1.17', '0.95'),
        ('+11.3', 'above PLAXIS on #58 case 3', '0.59', '0.53'),
        ('+4.2', "the paper's 2.5 × 10⁻⁵", '2.605', '2.5'),
    ],

    # Absolute factor-of-safety differences whose partner value the page does
    # not print (a measurement stated on its own).
    abs_bounds=[
    ],

    # Percentages spelled in words.  Each is a QUALITATIVE characterisation, not
    # a comparison of two printed factors — adjudicated once and named here, so
    # that a new worded percentage fails until someone reads it.
    worded_ok=[
        "agreeing to a quarter of a percent",
        "costs about a percent, not several",
    ],

    # Statements of a BOUND or a SHARE rather than a comparison of two printed
    # factors: no pair exists to re-derive, so each is named here explicitly.
    bounds=[
        ('+4.2', 'lighter by section area'),
        ('+1.8', "the polygon's area is within"),
        ('+14', 'by 14% at 12.5 kPa'),
        ('+25', 'by 25% at 5 kPa'),
        ('+43', 'by 43% at 1 kPa'),
        ('+3', 'worth ~2–3% here'),
        ('+39.2', 'larger than the Mohr-Coulomb corridor'),
        ('+3.5', 'Every case lands within 3.5% of unity'),
        ('+1.6', 'stages land within 1.6%'),
        ('+1', 'and five of the six within 1%'),
        ('+0.8', 'land within 0.8%'),
        ('+2.2', 'that still lands within 2.2%'),
        ('+2.1', 'lands within 2.1% of'),
        ('+6', 'about 6% apart on cases 1 and 2'),
        ('+20', 'runs about 20% low'),
    ],

    # Flac3D is one of the four programs the RS2-62 tables carry as published
    # columns; the base authority vocabulary does not name it.
    auth_hdr_extra=["Flac3D"],

    locked_value_re=r"(?:SSRM|Spencer|Bishop|k꜀|FS)\s+\**(\d+\.\d{3})",

    figure_mode="panel",
    # Figures that are not model/mechanism plots: their captions describe a
    # diagnostic, so no panel form is claimed and none is required.
    caption_exempt={
        "images/rs2_67_fielddiff.png",
    },
)
