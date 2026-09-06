"""Per-page configuration for the verification-page checkers.

A page config carries everything that is a property of ONE verification page:
its exemption lists (each naming both operands of a comparison the arithmetic
cannot reach), the extra vocabulary its tables use, and the figure conventions
its images follow.  The check modules themselves are page-agnostic.

An exemption is a claim about the page, not a way to silence the checker: every
entry names the two values being compared, and the whitelist entries are still
re-derived arithmetically, so a wrong exemption fails like anything else.  An
exemption that never fires is itself reported as a failure (a "dead exemption"),
which is what keeps the lists honest as pages are edited.
"""
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class PageConfig:
    """Everything the three checkers need to know about one page."""

    #: page identity — the file name under docs/verification without .md
    name: str

    # ---------------------------------------------------------------- deltas
    #: Cross-scope percentage comparisons: the two numbers live in different
    #: sentences, or in a table the sentence refers to.  Each entry is
    #: ``(printed, distinctive substring of the line, value-for, value-against)``
    #: and is re-derived; both operands must still be printed somewhere the
    #: claim can reach, or the entry is reported as orphaned.
    whitelist: List[Tuple[str, str, str, str]] = field(default_factory=list)

    #: Lines where a phrase the VOICE check bans is legitimate: usage prose
    #: addressed to the reader, a quoted source, a material or option whose name
    #: collides with a banned word.  Entries are (phrase, distinctive substring
    #: of the line); both must match, and an allowance that never fires is
    #: reported dead, exactly like the other exemption lists.
    voice_allow: List[Tuple[str, str]] = field(default_factory=list)


    #: Statements of a BOUND or a SHARE rather than a comparison of two printed
    #: factors ("all six land within 1.6%"): no single pair exists to re-derive,
    #: so each is named by ``(printed, distinctive substring)``.
    bounds: List[Tuple[str, str]] = field(default_factory=list)

    #: Absolute factor-of-safety differences whose partner value the page does
    #: not print ("the cutoff is worth −0.025").  ``(printed, substring)``.
    abs_bounds: List[Tuple[str, str]] = field(default_factory=list)

    #: Percentages spelled in words.  No arithmetic can be attached to them, so
    #: each is adjudicated once and named here by a distinctive substring; a new
    #: worded percentage fails until someone reads it.
    worded_ok: List[str] = field(default_factory=list)

    #: Extra regex alternatives appended to the "this percentage is not a
    #: comparison" pattern (domain shares, mesh fractions, ...).  Each must be a
    #: phrase, never a bare word.
    not_a_comparison_extra: List[str] = field(default_factory=list)

    #: Extra regex alternatives, anchored to the text IMMEDIATELY BEFORE a
    #: percentage, that mark it as not a comparison — a probability of failure,
    #: a degree of consolidation.  Some quantities are qualified by what precedes
    #: them rather than by what follows.  Each must be a phrase, never a bare
    #: word, and each is matched with `$` against the 40 characters before the
    #: token.
    not_a_comparison_prefix: List[str] = field(default_factory=list)

    #: Table rows whose percentages are values rather than comparisons — a
    #: row of percent CHANGES in a sensitivity sweep, a beta-to-probability
    #: row.  Each entry is a distinctive substring of the row (normally its
    #: label cell), so the exemption names the row it excuses.
    share_rows: List[str] = field(default_factory=list)

    #: Extra regex alternatives appended to the share-column header pattern: a
    #: table column whose header declares it holds shares (a degree of
    #: consolidation, a percentage of a total), not comparisons.
    share_hdr_extra: List[str] = field(default_factory=list)

    #: Extra regex alternatives appended to the authority-column header pattern
    #: (vendor and reference names this page's tables use as the source column).
    auth_hdr_extra: List[str] = field(default_factory=list)

    # ------------------------------------------------------------------ tags
    #: Tag keys whose values must appear verbatim in the section carrying the
    #: tag.  Prefixes end with '*'.  A key whose value is a semicolon list
    #: (``points``, ``expected``) locks one value per element and every element
    #: is checked; see ``tag_list_published``.
    tag_value_keys: List[str] = field(
        default_factory=lambda: ['expected_fs*', 'fs_*', 'expected_beta',
                                 'expected_kc', 'expected_flowrate*',
                                 'expected_head*', 'points', 'expected',
                                 'expected_elements', 'expected_nodes'])

    #: Decimal places a section may restate a tag value to.  ``None`` demands
    #: the tag value verbatim (the rs2 convention: the page prints the lock).
    #: Set to 2 on a page whose prose quotes locks at the source figure's own
    #: precision, so ``expected_fs=1.822`` is satisfied by a printed ``1.82``,
    #: and a page whose tables print solved fields to fewer places than the
    #: probes lock them to.  Only rounding DOWN in precision is accepted, and
    #: only to this many places, so a genuinely different value still fails.
    tag_round_dp: int = None

    #: How much of a LIST lock the page publishes, where it does not publish
    #: all of it.  ``points=20:5:7.166;...`` locks a solved head per station and
    #: ``expected=1.686;0.941;...`` one factor of safety per march step; a page
    #: may tabulate the whole set, a selection of it, or none of it (a probe set
    #: that guards a field's shape while the section publishes something else).
    #: Each entry is ``(distinctive substring of the tag line, how many of its
    #: elements the page prints)`` and the count is EXACT in both directions: a
    #: mistyped printed value drops the count and fails, and a newly published
    #: one raises it and fails until the declaration is updated.  A substring
    #: may match several tag lines that share a count (a family of probe sets);
    #: one that matches none is reported as a dead declaration.
    tag_list_published: List[Tuple[str, int]] = field(default_factory=list)

    #: Tag values the page deliberately does not print — coverage locks that
    #: exercise a code path rather than back a published number.  Each entry is
    #: ``(value, distinctive substring of the tag line)``; an entry that never
    #: fires is reported, like a dead delta exemption.
    tag_exempt: List[Tuple[str, str]] = field(default_factory=list)

    # -------------------------------------------------------------- untagged
    #: Factor-of-safety-shaped numbers a section prints that no tag locks and
    #: no source column carries, and that are legitimate anyway: a strength
    #: ratio, a stability number, a published quantity quoted only in prose.
    #: Each entry is ``(the number as printed, distinctive substring of its
    #: line)``, so the allowance names the line it excuses, and one that never
    #: fires is reported dead like every other exemption.  It is NOT the place
    #: to park a companion measurement — those are trimmed, or given a tag.
    untagged_allow: List[Tuple[str, str]] = field(default_factory=list)

    #: Regex naming the values a summary row presents as locked, for the
    #: reverse sweep (every locked value must have a tag behind it).  ``None``
    #: disables the reverse sweep on pages that carry no dotted summary table.
    locked_value_re: str = None

    #: Substring identifying the summary block the reverse sweep reads.
    summary_marker: str = 'corpus-summary'

    # ----------------------------------------------------------- heading dots
    #: Where several summary rows name one section anchor and their dots
    #: DISAGREE — a section covering three problems of the manual, a catalog row
    #: piggybacking on the section another row built — this says which dot the
    #: heading carries.  ``(anchor, dot)``, and the dot must be one a row
    #: actually gives that anchor, so the table stays the source and the entry
    #: only says which row speaks for the section.  An entry that never fires,
    #: or whose rows have since come into agreement on another dot, is reported.
    heading_dot_multi: List[Tuple[str, str]] = field(default_factory=list)

    # --------------------------------------------------------------- figures
    #: 'panel'      — classify each PNG's panel layout and compare it against
    #:                the panel form the caption declares.
    #: 'structural' — the page's figures have no single meaningful panel form,
    #:                so check that every referenced image exists and that no
    #:                caption is empty.
    figure_mode: str = 'panel'

    #: Images whose captions describe a diagnostic and so claim no panel form.
    caption_exempt: set = field(default_factory=set)

    #: Caption phrases that force a panel form, checked before the generic
    #: classifier.  ``[(substring, form)]`` with form in {'one','two','four'}.
    caption_rules: List[Tuple[str, str]] = field(default_factory=list)
