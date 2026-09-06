"""Heading dots: a problem's section heading opens with its summary-table dot.

Every corpus page's summary table carries a match dot per problem — 🟢 🟡 🔴 🟣
and the ⊘ that means no data, scored as
`docs/verification/index.md#how-the-match-dots-are-scored` describes.  The same
dot opens that problem's section heading, so a reader skimming the page, or its
sidebar table of contents, sees the status without going back to the table:

    ### 🟢 RS2-1: Simple slope stability assessment {#rs2-1}

The summary table stays the single source.  This check reads each table row's
anchor and its dot, then requires the heading that carries the anchor to start
with that dot; ⊘ is written in the heading as the bare character, since a
heading is also a table-of-contents entry and markup does not survive there.

What the check reads
--------------------
* **Rows.** Every row of every ``corpus-summary`` block whose first cell is a
  link and whose Match column carries a dot.  A row linking another page
  (``[7](geostudio.md#acads-weak-layer)``) names a section that page owns, so it
  is skipped here.
* **Headings.** Only headings carrying an explicit ``{#anchor}`` that a row
  names.  A heading no table names — a discussion, a shared cross-bearing — is
  left alone, dot or no dot: the table is what confers a status.
* **A row whose anchor is an inline ``<a id=...>``** rather than a heading is
  reported as a note, not a failure.  The anchor resolves, so the link is good;
  there is simply no heading of its own to open with a dot.  A row whose anchor
  the page does not define at all is a broken link and fails.

Several rows may name one heading — a section that covers three problems of the
manual, or a catalog row that piggybacks on the section another row built.
Where those rows agree, the heading takes their dot.  Where they disagree, the
page config's ``heading_dot_multi`` says which dot the heading carries, and the
declaration must name a dot one of the rows actually gives that anchor: the
table is still the source, the declaration only says which of its rows speaks
for the section.  A declaration that never fires is reported dead, like every
other exemption on these pages.

Usage
-----
    python -m tools.verification_checks.dots docs/verification/rs2.md
    python -m tools.verification_checks.dots --fix rs2 seep
"""
import os
import re
import sys

#: The match-quality dots, worst-to-best irrelevant here: the table decides.
MATCH_DOTS = ("🟢", "🟡", "🔴", "🟣")
#: "insufficient data or out of scope".  Written in a table as a span so the
#: page can style it, and in a heading as the bare character.
NODATA = "⊘"
DOTS = MATCH_DOTS + (NODATA,)

HEADING = re.compile(
    r"^(?P<hashes>#{2,6})\s+(?P<title>.*?)\s*"
    r"\{#(?P<anchor>[\w.:-]+)(?P<attrs>[^}]*)\}\s*$")
#: A dot already at the front of a heading title, in either spelling.
LEAD = re.compile(r'^(?:<span class="nodata">\s*⊘\s*</span>|[' +
                  "".join(DOTS) + r"])\s*")
ROW_LINK = re.compile(r"^\[(?P<label>[^\]]*)\]\((?P<target>[^)\s]+)\)$")
INLINE_ANCHOR = re.compile(r"""<a\s+(?:id|name)=["'](?P<anchor>[\w.:-]+)["']""")
SEPARATOR = set("|-: ")


def _dot(cell):
    """The dot a Match cell carries, normalized, or None."""
    if NODATA in cell:
        return NODATA
    for d in MATCH_DOTS:
        if d in cell:
            return d
    return None


def summary_rows(lines, marker="corpus-summary"):
    """(line number, label, link target, dot) for every dotted summary row."""
    rows, in_block, cols = [], False, None
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not in_block:
            if s.startswith("<div") and marker in s:
                in_block, cols = True, None
            continue
        if s.startswith("</div"):
            in_block = False
            continue
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cols is None:                      # the header row
            cols = {c.lower(): j for j, c in enumerate(cells)}
            continue
        if set(s) <= SEPARATOR:               # the |---|:-:| rule
            continue
        j = cols.get("match")
        if j is None or j >= len(cells):
            continue
        link = ROW_LINK.match(cells[0])
        dot = _dot(cells[j])
        if link and dot:
            rows.append((i, link.group("label"), link.group("target"), dot))
    return rows


def headings(lines):
    """anchor -> (line number, hashes, title, attrs) for anchored headings."""
    out = {}
    for i, line in enumerate(lines, 1):
        m = HEADING.match(line)
        if m:
            out[m.group("anchor")] = (i, m.group("hashes"), m.group("title"),
                                      m.group("attrs"))
    return out


def scan(path, cfg=None):
    """Read one page.  Returns (problems, fixes, notes).

    ``problems`` are strings; ``fixes`` are (line number, replacement line)
    pairs for the headings ``--fix`` would rewrite; ``notes`` are reported but
    do not fail.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    marker = getattr(cfg, "summary_marker", None) or "corpus-summary"
    declared = list(getattr(cfg, "heading_dot_multi", None) or [])
    heads = headings(lines)
    inline = {m.group("anchor") for m in INLINE_ANCHOR.finditer("\n".join(lines))}

    by_anchor = {}
    order = []
    for lineno, label, target, dot in summary_rows(lines, marker):
        if not target.startswith("#"):
            continue                       # a section another page owns
        anchor = target[1:]
        if anchor not in by_anchor:
            by_anchor[anchor] = []
            order.append(anchor)
        by_anchor[anchor].append((lineno, label, dot))

    problems, fixes, notes, fired = [], [], [], set()
    for anchor in order:
        rows = by_anchor[anchor]
        dots = {d for _, _, d in rows}
        if len(dots) > 1:
            named = ", ".join(f"{lbl} {d}" for _, lbl, d in rows)
            dec = next((e for e in declared if e[0] == anchor), None)
            if dec is None:
                problems.append(
                    f"#{anchor}: rows disagree ({named}) — add "
                    f"heading_dot_multi ({anchor!r}, dot) naming the dot the "
                    f"section carries")
                continue
            fired.add(dec)
            if dec[1] not in dots:
                problems.append(
                    f"#{anchor}: heading_dot_multi names {dec[1]}, which no "
                    f"row gives it ({named})")
                continue
            want = dec[1]
        else:
            want = dots.pop()
            dec = next((e for e in declared if e[0] == anchor), None)
            if dec is not None:             # the rows agree now
                fired.add(dec)
                if dec[1] != want:
                    problems.append(
                        f"#{anchor}: heading_dot_multi names {dec[1]} but "
                        f"every row now carries {want}")
                    continue

        if anchor not in heads:
            where = rows[0][0]
            if anchor in inline:
                notes.append(f"line {where}: #{anchor} is an inline anchor, "
                             f"not a heading — no heading dot to carry")
            else:
                problems.append(f"line {where}: row links #{anchor}, which the "
                                f"page defines nowhere")
            continue

        hline, hashes, title, attrs = heads[anchor]
        lead = LEAD.match(title)
        have = _dot(lead.group(0)) if lead else None
        if have == want:
            continue
        rest = title[lead.end():] if lead else title
        problems.append(
            f"line {hline}: heading #{anchor} starts with "
            f"{have or 'no dot'}, the table says {want}")
        fixes.append((hline, f"{hashes} {want} {rest} {{#{anchor}{attrs}}}"))

    for dec in declared:
        if dec not in fired:
            problems.append(f"dead heading_dot_multi entry {dec!r} — no "
                            f"summary row names that anchor")
    return problems, fixes, notes


def fix(path, cfg=None):
    """Rewrite the headings so each opens with its table's dot.  Returns how
    many were rewritten.  Only the leading dot changes: the title text and the
    ``{#anchor}`` are carried through untouched."""
    _, fixes, _ = scan(path, cfg)
    if not fixes:
        return 0
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for lineno, new in fixes:
        lines[lineno - 1] = new
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return len(fixes)


def run(path, cfg, report=print):
    """Check one page.  Returns the failure count."""
    problems, _, notes = scan(path, cfg)
    for note in notes:
        report(f"  dots      : note — {note}")
    if not problems:
        report("  dots      : clean")
        return 0
    for p in problems:
        report(f"  dots      : {os.path.basename(path)}:{p}")
    return len(problems)


def main(argv):
    from .pages import PAGES
    here = os.path.dirname(os.path.abspath(__file__))
    pagedir = os.path.join(os.path.dirname(os.path.dirname(here)),
                           "docs", "verification")
    do_fix = "--fix" in argv
    names = [a for a in argv[1:] if not a.startswith("-")] or sorted(PAGES)
    total = 0
    for n in names:
        p = n if n.endswith(".md") else os.path.join(pagedir, n + ".md")
        key = os.path.basename(p)[:-3]
        cfg = PAGES.get(key)
        print(f"{key}:")
        if do_fix:
            n_fixed = fix(p, cfg)
            print(f"  dots      : {n_fixed} heading(s) rewritten")
        total += run(p, cfg, report=print)
    print(f"\n{total} heading-dot problem(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
