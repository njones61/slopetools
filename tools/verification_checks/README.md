# Verification-page checks

Standing checks on the six verification pages under `docs/verification`
(`rs2`, `rocscience`, `geostudio`, `rocscience_groundwater`, `ssrm`, `seep`).
They run as one test in the default `run_tests.py` set, and they are cheap:
a page that has not changed since it was last certified costs one file read.

## What each check does

**Deltas** (`deltas.py`). Every percentage the page prints — `(+1.2%)`,
`−7%`, `**+2.1%**`, `<0.01%` — and every absolute factor-of-safety difference
("worth +0.013", "costs 0.18") is re-derived from two numbers the page itself
prints in the same sentence or the same table row:

    delta = (XSLOPE − source) / source × 100,  half-up, one decimal

Pairing is sign-aware and nearest-first, so a sign flip or a wrong last digit
cannot be certified by some other pair further down the paragraph. The check
also enforces the page convention that a signed delta is printed to one
decimal unless it is explicitly hedged ("to within −0.27%"), and reports
percentages spelled in words, which no arithmetic can reach.

Percentages that are not comparisons — a share of the mesh, a probability of
failure, a degree of consolidation — are excluded by named phrases, never by a
bare word, so a real comparison cannot hide behind an incidental noun.

**Tags** (`tags.py`). Three passes. Forward: every value a `<!-- test: -->`
tag locks must be printed in the section that carries the tag. Restatements:
every number a section attributes to XSLOPE must agree with a lock that
attribution reaches. Reverse: every value the page presents as locked — a factor
of safety in the Results column of a summary row whose Match cell carries a
colour dot — must have a tag behind it.
The tag is truth: when a tag and the text disagree, the text is what changes.

The forward pass is existential — it asks whether the lock is printed, not
whether every printing of it is right — so a section that states its locked
factor of safety twice could drift in one place with the other left standing.
The restatement pass is universal over the numbers the section claims as its
own results, which is a narrower set than "every number shaped like a factor of
safety":

* a cell in a results table's XSLOPE column, where the row's label names the
  locked method — the method a tag names in its key (`fs_bishop`), in
  `method=`, or in a `type=` that says SSRM, narrowed further by the element
  type it meshes on and by a tangency constraint on the search;
* a number a sentence introduces with "XSLOPE's" or "this model's", up to the
  next sentence boundary or the next mention of a source.

A number the page attributes to a source, and a number it attributes to nobody,
are left where they already are — to the delta check and to the untagged sweep.
A table with several XSLOPE columns (`XSLOPE composite` beside `XSLOPE
circles-only`) publishes a row's method under variants the row label does not
name, and a number a cell puts in parentheses (`1.415 *(search 1.411)*`) is a
second quantity stated there; neither is read. The locks in scope are the
section's own, a page-level bank tag whose input file the section links, any
page's tag on a file the section links, and the tags of a section this one
cross-references by anchor — the link being the page's own statement that the
two present the same problem. A restatement passes when it is the lock rounded
to a precision the page allows (`tag_round_dp`) or inside the tag's own
tolerance.

A tag value that is a semicolon **list** locks one value per element, and every
element is checked the same way — `expected=1.686;0.941;…` (a factor of safety
per march step) and `points=20:5:7.166;…` (a solved head per station, the
coordinates being inputs like `time=`). So a wrong digit in one cell of an
eleven-row table fails. Two restatements count as printing the lock, because
each is the same number read the way the comparison is made: the value rounded
to the page's own precision (`tag_round_dp`), and, for a `points` element, the
pressure head ψ = h − y at that station.

A page may publish only part of a probe set — a table of the stations that carry
the argument, or none of a set that guards a field's shape while the section
publishes something else. `tag_list_published` declares how many elements the
page prints, per lock and with the reason; the count is exact, so a mistyped
printed value fails just as an undeclared one does, and a declaration that
matches no tag is reported dead.

**Voice** (`voice.py`). These pages are documentation for a stranger who wants
to know whether XSLOPE reproduces a published problem and what the caveats are.
They are not addressed to the maintainer and they are not a record of how the
work went. Prose written mid-investigation reads differently — "the obvious
suspect was...", "their factors are withdrawn", "four candidate causes have been
measured" — and a reader who was not there gets nothing from it. The check
carries a curated list of phrasings that are campaign voice in essentially any
context, in four groups: first person, project process, investigation narrative,
and time measured from the project rather than from the problem. Each hit names
the page, the line, the phrase and the line's text.

It is deliberately narrow. It flags phrasings, not everything that could be
written better, and a phrase that has an ordinary descriptive reading is left
out rather than exempted case by case — "the firm base now sits at depth D" is
not campaign voice, so a bare "now sits" is not banned. Prose only: fenced
blocks, HTML comments (which is what a test tag is), inline code spans, link
targets and bare URLs are removed before matching, so a material named `us` or a
citation URL cannot fire. Where a page genuinely needs a banned phrase,
`voice_allow` names it — `(phrase, distinctive substring of the line)`, both
required, and an allowance that never fires is reported dead.

**Untagged numbers** (`untagged.py`). A section prints three kinds of number
that carry an argument: the factor of safety a tag locks, the value the source
published, and the comparison between them. Anything else shaped like a factor
of safety — a mesh-sweep row, a depth-cutoff row, a with/without variant, a
reading taken off a field at the critical strength — is a companion measurement
that nothing regenerates and nothing defends when a lock moves. The check reads
each section and reports every factor-of-safety-shaped number that is neither
within the tolerance of a tag the section carries (its own, a page-level bank
tag naming a file the section links, or another page's tag on that same file)
nor printed in a column whose header names the source. Inputs, dimensions,
percentages, figure and section numbers, code, math and link targets are taken
out of the running first.

It **reports and returns zero** while `untagged.ENFORCING` is False. Each flag
is a sentence someone has to read — a companion measurement to trim, a number
worth a tag of its own, or a quantity that only looks like a factor of safety
and belongs in `untagged_allow`. Enforcing it before that reading is done would
push the pages toward blanket allowances, which is the opposite of the point.

**Figures** (`figures.py`). Two modes, chosen per page.

* `panel` — the panel layout is read directly off the PNG (an ink-profile test
  for inter-panel gutters) and compared against the layout the caption declares.
  Used where the caption makes a layout claim: rs2's four-panel composites,
  and the "inputs and ... solution" / "mesh and solved heads" two-panel
  composites on `rocscience`, `geostudio` and `rocscience_groundwater`.
  A caption the classifier cannot read is a failure, not a pass, unless the
  figure is named in the page's `caption_exempt`.
* `structural` — used on `ssrm` and `seep`, whose figures are single-axes plots
  captioned with their file name: the caption makes no layout claim, so panel
  classification would be testing a claim the page does not make. Every
  referenced image must exist and carry non-empty alt text.

**Heading dots** (`dots.py`).  The match dot a summary table gives a problem —
🟢 🟡 🔴 🟣 or the ⊘ that means no data, scored as
`docs/verification/index.md#how-the-match-dots-are-scored` describes — also opens
that problem's section heading, so a reader skimming the page sees the status
without going back to the table:

    ### 🟢 RS2-1: Simple slope stability assessment {#rs2-1}

The table stays the single source: the check reads each row's anchor and dot and
requires the heading carrying that anchor to start with it, written in a heading
as the bare ⊘ rather than the table's styled span.  Only headings with an
explicit `{#anchor}` that a row names are checked; a heading no table names is
left alone.  A row linking another page names a section that page owns, and a row
whose anchor is an inline `<a id=...>` has no heading of its own to open with a
dot — the first is skipped, the second reported as a note.  A row whose anchor
the page defines nowhere is a broken link and fails.  `--fix` rewrites the
headings, touching only the leading dot.

Several rows may name one heading — a section covering three problems of the
manual, a catalog row piggybacking on the section another row built.  Where they
agree the heading takes their dot; where they disagree `heading_dot_multi` names
which of those rows speaks for the section.

## Running them

```bash
python -m tools.verification_checks.certify                  # all six pages
python -m tools.verification_checks.certify rs2 seep         # named pages
python -m tools.verification_checks.certify --force          # ignore the manifest
python -m tools.verification_checks.mutations                # the mutation suite
```

Each check can also be run on its own page for a detailed report:

```bash
python -m tools.verification_checks.deltas docs/verification/rs2.md
python -m tools.verification_checks.tags docs/verification/rs2.md
python -m tools.verification_checks.figures docs/verification/rs2.md
python -m tools.verification_checks.voice docs/verification/rs2.md
python -m tools.verification_checks.untagged docs/verification/rs2.md
python -m tools.verification_checks.dots docs/verification/rs2.md
python -m tools.verification_checks.dots --fix rs2      # rewrite the headings
```

## The recertify workflow

`certified.json` records the SHA-256 of each page's content as it stood when
the checks last passed **and a developer signed off**. A page whose hash still
matches is reported "unchanged, certified" and nothing else runs; a page whose
hash differs is re-checked in full, and even if every check passes it stays a
failure until the manifest is updated — certifying a page is a deliberate act,
because the developer is the one who read the flags while editing.

So: edit a page, fix whatever the checks raise, then run
`python -m tools.verification_checks.certify --recertify <page>` and commit the
updated `certified.json` in the same commit as the page change.

## Adding an exemption honestly

Each page's config lives in `pages/<page>.py`. An exemption is a claim about
the page, not a way to silence the checker, so:

* **Name both operands.** A `whitelist` entry is
  `(printed, distinctive substring, value-for, value-against)` and the checker
  still does the arithmetic — a wrong whitelist entry fails like anything else.
  It also re-checks that both operands are still printed where the claim can
  reach them, so editing one of them cannot silently orphan the comparison.
* **Say why the pairing is legitimate** in a comment above the entry: the two
  numbers sit in different sentences, or the delta is measured against a value
  printed in a table the sentence links to, or the page is deliberately
  comparing one vendor against another in its own voice.
* **Use `bounds` only where no pair exists.** "All six stages land within 1.6%"
  is a claim about a whole set; no single pair can check it, so it is
  adjudicated once, by hand, and named. The same goes for `abs_bounds` (an
  absolute FS difference whose partner value the page does not print) and
  `worded_ok` (a percentage spelled in words).
* **`not_a_comparison_extra` / `not_a_comparison_prefix` / `share_hdr_extra` /
  `share_rows` name quantities that are values, not differences** — a share of
  the domain, a probability of failure, a row of percent changes. Each must be
  a phrase or a named row, never a bare word.
* **`voice_allow` names a line where a banned phrase is legitimate** — usage
  prose addressed to the reader, a quoted source, a name that collides with a
  banned word. Say which of the four groups the phrase is in and why this line
  is not that. Adding one because the lint complained, without reading the
  sentence, is the failure the dead-allowance report exists to prevent.
* **`untagged_allow` names a number that only looks like a factor of safety** —
  a strength ratio, a stability number, a published quantity quoted in prose
  rather than tabulated. `(the number as printed, distinctive substring of its
  line)`. It is not a place to park a companion measurement: those are trimmed,
  or given a tag of their own.
* **`heading_dot_multi` names the dot a heading carries where the summary rows
  naming it disagree** — `(anchor, dot)`, and the dot must be one those rows
  actually give the anchor.  Say which of them the section's own locked
  comparisons come from.
* **`tag_exempt` names a coverage lock the page deliberately does not print** —
  a tag that exercises a code path rather than backing a published number. The
  page normally says so in prose; quote that reason in the comment.
* **`tag_list_published` names how much of a list lock the page prints** — the
  count, not a licence to skip the lock. Say which elements are published and
  why the rest are not (a regression probe set, a station the table does not
  tabulate, a quantity the section publishes in another form). Raising a count
  because the checker complained, without knowing which value moved, is exactly
  the failure the exact count exists to prevent.

An exemption that never fires is reported as a **dead exemption** and fails the
check. That is deliberate: it is what stops the lists silently accumulating
entries for text that no longer exists.

## Mutation suite

`mutations.py` plants one defect at a time — a wrong last digit, a flipped
sign, an operand moved out from under a certified claim, a caption that no
longer matches its figure, a section heading whose dot disagrees with its summary
row, a tagged value dropped from its section, one element
of an eleven-value row corrupted on the page or in the tag, a planted dead
exemption — and requires the checks to catch every one. It also plants edits
that must **not** be flagged (a value reprinted at a different, correct
precision), because a check that fails on those would push the pages toward
printing tag values verbatim instead of at the precision each comparison is read
at. Run it after any change to the check logic; a gate that certifies a wrong
number is worse than no gate.
