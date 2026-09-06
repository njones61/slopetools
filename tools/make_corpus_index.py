#!/usr/bin/env python3
"""Generate the corpus example index from the docs' own test tags.

Every `<!-- test: ... -->` tag in docs/**/*.md names a model file and sits on a
page that publishes the comparison behind it.  This tool turns that pairing into
two artifacts:

  * ``docs/verification/corpus_index.json`` — the machine index: one record per
    distinct model, carrying a FEATURE SIGNATURE read out of the model file
    itself (never from its name), the topics that signature implies, and every
    verification-page section that documents it, with a real readthedocs URL.

  * a TOPIC -> EXAMPLES table injected into the assistant skill
    (``docs/usage/claude/xslope.md``) between the ``corpus-index`` markers, so a
    question about tiebacks or geogrids can be answered by pointing at worked
    problems that have published comparisons.

Both outputs are deterministic — everything is sorted and nothing records a
timestamp — so ``run_tests.py --docs`` can regenerate the index in memory and
fail when the committed copies are stale.

Usage::

    python tools/make_corpus_index.py           # rewrite both artifacts
    python tools/make_corpus_index.py --check    # report staleness, write nothing

The feature signature is read from ``load_slope_data`` output only.  A model's
filename never decides a topic: a file called ``xslope_reinforce_fem.xlsx``
lands under reinforcement because its reinforce sheet has rows, and a sheet-pile
cutoff is found by the narrow no-flow notch its profile line actually draws.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / 'docs'
INDEX_PATH = DOCS / 'verification' / 'corpus_index.json'
SKILL_PATH = DOCS / 'usage' / 'claude' / 'xslope.md'
BUNDLED_SKILL = REPO_ROOT / 'xslope' / 'resources' / 'xslope_skill.md'
BASE_URL = 'https://xslope.readthedocs.io/en/latest/'

BEGIN_MARKER = '<!-- corpus-index:begin -->'
END_MARKER = '<!-- corpus-index:end -->'

SCHEMA_VERSION = 1

TAG_RE = re.compile(r'<!--\s*test:\s*(.*?)\s*-->')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
EXPLICIT_ANCHOR_RE = re.compile(r'\s*\{#([A-Za-z0-9_\-]+)\}\s*$')
XLSX_LINK_RE = re.compile(r'\]\(([^)\s]+\.xlsx)\)')
ANY_LINK_RE = re.compile(r'\]\(([^)\s]+)\)')
IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')


# --------------------------------------------------------------------------- #
# Markdown: headings, anchors, sections
# --------------------------------------------------------------------------- #

def slugify(value: str, separator: str = '-') -> str:
    """The slug python-markdown's toc extension would assign to a heading.

    Mirrors ``markdown.extensions.toc.slugify`` so the anchors this tool emits
    are the anchors the built site actually serves.  Reimplemented rather than
    imported so the index is identical on machines without mkdocs installed.
    """
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[%s\s]+' % separator, separator, value)


def unique_slug(slug: str, used: set) -> str:
    """python-markdown's duplicate-heading disambiguation (``foo``, ``foo_1``)."""
    while slug in used or not slug:
        m = IDCOUNT_RE.match(slug)
        slug = '%s_%d' % (m.group(1), int(m.group(2)) + 1) if m else '%s_1' % slug
    used.add(slug)
    return slug


def strip_inline_markup(text: str) -> str:
    """Heading text as rendered: markdown emphasis, code spans and links removed.

    The toc extension slugifies the rendered text, so ``**Both** cases`` and
    ``[VP32](rocscience.md#vp32)`` must lose their syntax before slugifying.

    Underscores are deliberately kept: python-markdown does not treat an
    intra-word ``_`` as emphasis, so the gamma_sat sample's heading really does
    serve ``#16-saturated-vs-moist-unit-weight-_sat`` on the built site.
    """
    text = EXPLICIT_ANCHOR_RE.sub('', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)      # links -> label
    text = re.sub(r'<[^>]+>', '', text)                        # inline html
    text = re.sub(r'[*`]+', '', text)                          # emphasis/code
    return text.strip()


def page_url_path(md_path: Path) -> str:
    """docs/verification/rs2.md -> 'verification/rs2/' (mkdocs pretty URL)."""
    rel = md_path.relative_to(DOCS).with_suffix('')
    parts = list(rel.parts)
    if parts[-1] == 'index':
        parts = parts[:-1]
    return '/'.join(parts) + ('/' if parts else '')


class Section:
    __slots__ = ('line', 'level', 'title', 'anchor', 'models', 'stems')

    #: The match dot a verification heading leads with (see verification_checks/dots.py);
    #: it is page status, not part of the title an index or the skill's table quotes.
    _DOTS = ('🟢', '🟡', '🔴', '🟣', '⊘')

    def __init__(self, line, level, title, anchor):
        self.line = line
        self.level = level
        title = title.strip()
        while title and title[0] in self._DOTS:
            title = title[1:].lstrip()
        self.title = title
        self.anchor = anchor
        self.models = set()     # model .xlsx paths linked in the body
        self.stems = set()      # basename stems of every asset the body links


def parse_page(md_path: Path):
    """Return (sections, tags) for one markdown page.

    A section records the anchor the site will serve and the set of model files
    the section body links — that link is what binds a model to the prose that
    documents it, which is far more reliable than matching a benchmark id
    against a heading (``RS2-4`` and ``RS2-24`` collide under any normalization
    that drops the hyphen).
    """
    text = md_path.read_text(encoding='utf-8')
    lines = text.splitlines()
    md_dir = md_path.parent

    sections = []
    used_slugs = set()
    in_fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        raw = m.group(2)
        explicit = EXPLICIT_ANCHOR_RE.search(raw)
        title = strip_inline_markup(raw)
        if explicit:
            anchor = explicit.group(1)
            used_slugs.add(anchor)
        else:
            anchor = unique_slug(slugify(title), used_slugs)
        sections.append(Section(i, len(m.group(1)), title, anchor))

    # Attribute each section's body links to it.
    for k, sec in enumerate(sections):
        end = sections[k + 1].line if k + 1 < len(sections) else len(lines)
        body = '\n'.join(lines[sec.line:end])
        for target in XLSX_LINK_RE.findall(body):
            target = target.split('#')[0]
            sec.models.add(os.path.normpath(os.path.join(md_dir, target)))
        for target in ANY_LINK_RE.findall(body):
            stem = Path(target.split('#')[0]).stem.lower()
            if stem:
                sec.stems.add(stem)

    tags = []
    for i, line in enumerate(lines):
        for m in TAG_RE.finditer(line):
            params = {}
            for pair in m.group(1).split(','):
                key, sep, value = pair.partition('=')
                if sep:
                    params[key.strip()] = value.strip()
            if 'file' not in params:
                continue        # a documentation example of the tag syntax
            params['_line'] = i
            params['_model'] = os.path.normpath(
                os.path.join(md_dir, params['file']))
            tags.append(params)
    return sections, tags


def resolve_section(sections, tag):
    """The section that documents this tag, as the page itself declares it.

    Preference order: the section whose body links the model file (the
    ``**Input files:**`` link); failing that, the section that links an asset of
    the same stem (a grouped section like VP87-VP94 documents its members
    through their ``images/vp087.png`` figures rather than one xlsx link each);
    failing that, the nearest preceding heading.  When several sections qualify,
    the one nearest the tag wins.
    """
    def _nearest(cands, how):
        if len(cands) == 1:
            return cands[0], how
        return min(cands, key=lambda s: (abs(s.line - tag['_line']), s.line)), how

    owners = [s for s in sections if tag['_model'] in s.models]
    if owners:
        return _nearest(owners, 'input-link')
    stem = Path(tag['_model']).stem.lower()
    kin = [s for s in sections if stem in s.stems]
    if kin:
        return _nearest(kin, 'asset-link')
    preceding = [s for s in sections if s.line < tag['_line']]
    if preceding:
        return preceding[-1], 'nearest-heading'
    return (sections[0], 'nearest-heading') if sections else (None, None)


# --------------------------------------------------------------------------- #
# Feature signature — read from the model, never from its name
# --------------------------------------------------------------------------- #

def _nonzero(x) -> bool:
    try:
        return x is not None and not math.isnan(float(x)) and float(x) != 0.0
    except (TypeError, ValueError):
        return False


def _finite(x) -> bool:
    try:
        return x is not None and math.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def find_cutoff_notches(slope_data):
    """Count sheet-pile / cutoff walls drawn as no-flow notches in a profile line.

    XSLOPE has no wall object: a partially penetrating cutoff is modelled by
    running the profile line down one face of the wall and back up the other, so
    the mesh carries a zero-width no-flow slit (docs/seep/samples.md).  The
    resulting vertex triple is far deeper than it is wide — 0.2 wide by 3.0 deep
    in the clay-blanket sample, 0.1 by 10 in the Pavlovsky sheet-pile — which no
    real ground surface does.  Require a 4:1 depth-to-width ratio.
    """
    count = 0
    for line in slope_data.get('profile_lines') or []:
        coords = line['coords'] if isinstance(line, dict) else line
        coords = [(float(x), float(y)) for x, y in coords]
        for i in range(1, len(coords) - 1):
            (xa, ya), (xb, yb), (xc, yc) = coords[i - 1], coords[i], coords[i + 1]
            width = abs(xc - xa)
            depth = min(ya, yc) - yb
            if depth > 0 and width >= 0 and depth >= 4.0 * max(width, 1e-12):
                count += 1
    return count


def feature_signature(slope_data):
    """The model's feature signature, entirely from loaded data."""
    mats = slope_data.get('materials') or []
    reinf = slope_data.get('reinforcement_lines') or []
    piles = slope_data.get('pile_lines') or []
    seep_bc = slope_data.get('seepage_bc') or {}

    sigma_keys = ('sigma_gamma', 'sigma_c', 'sigma_phi', 'sigma_cp',
                  'sigma_d', 'sigma_psi')
    sigmas = sorted({k[6:] for m in mats for k in sigma_keys if _nonzero(m.get(k))})

    # Reinforcement, subdivided by what the sheet's own columns say. A blank
    # Type is a generic tensile line; Dir/Appl still separate a geosynthetic-like
    # tangent line from an axial bar.
    r_types = sorted({(m.get('type') or 'generic') for m in reinf})
    r_dirs = sorted({(m.get('dir') or '') for m in reinf if m.get('dir')})
    r_appls = sorted({(m.get('appl') or '') for m in reinf if m.get('appl')})

    seep_defined = any(len(seep_bc.get(k) or []) > 0
                       for k in ('specified_heads', 'specified_fluxes', 'exit_face'))
    tseep = slope_data.get('tseep') or {}
    transient = bool(tseep.get('times')) if isinstance(tseep, dict) else bool(tseep)

    rapid = bool(slope_data.get('has_seepage_bc2')
                 or (slope_data.get('piezo_line2') or [])
                 or (slope_data.get('dloads2') or []))

    feat = {
        'n_materials': len(mats),
        'material_options': sorted({str(m.get('option') or '') for m in mats if m.get('option')}),
        'homogeneous': len(mats) == 1,
        'reinforcement': {
            'count': len(reinf),
            'types': r_types,
            'dirs': r_dirs,
            'appls': r_appls,
            'pullout': any(_nonzero(m.get('lp1')) or _nonzero(m.get('lp2')) for m in reinf),
            'end_anchorage': any(_nonzero(m.get('tend1')) or _nonzero(m.get('tend2')) for m in reinf),
            'residual_drop': any(_finite(m.get('t_res')) for m in reinf),
            'discrete_spacing': any(_nonzero(m.get('spacing')) and float(m['spacing']) != 1.0
                                    for m in reinf),
        },
        'piles': len(piles),
        'pile_fixities': sorted({str(p.get('head_fixity', p.get('fixity')))
                                 for p in piles
                                 if p.get('head_fixity', p.get('fixity'))}),
        'line_loads': len(slope_data.get('line_loads') or []),
        'dloads': len(slope_data.get('dloads') or []),
        'cutoff_walls': find_cutoff_notches(slope_data),
        'tension_crack': _nonzero(slope_data.get('tcrack_depth')),
        'tension_crack_water': _nonzero(slope_data.get('tcrack_water')),
        'seismic_k': float(slope_data.get('k_seismic') or 0.0),
        'rapid_drawdown': rapid,
        'seepage_problem': seep_defined,
        'transient_seepage': transient,
        'seepage_coupled': any(str(m.get('u') or '').lower() == 'seep' for m in mats),
        'piezo_line': bool(slope_data.get('piezo_line')),
        'ru': any(_nonzero(m.get('ru')) for m in mats),
        'unsaturated_models': sorted({str(m.get('unsat') or '').lower()
                                      for m in mats if m.get('unsat')}),
        'suction_strength': any(_nonzero(m.get('phi_b')) for m in mats),
        'tensile_cutoff': any(_finite(m.get('t_cut')) for m in mats),
        'hoek_brown': any(_nonzero(m.get('hb_gsi')) or _nonzero(m.get('hb_sci')) for m in mats),
        'sigmas': sigmas,
        'probabilistic': bool(sigmas),
        'non_circular': len(slope_data.get('non_circ') or []) > 0,
        'circular': len(slope_data.get('circles') or []) > 0,
        'k0': (float(slope_data['k0']) if _finite(slope_data.get('k0')) else None),
        'element_type': slope_data.get('element_type') or None,
        'ssr_zones': len(slope_data.get('ssr_zones') or []),
        'polygon_geometry': bool(slope_data.get('polygons')),
        'template_version': slope_data.get('template_version'),
        'unit_system': str(slope_data.get('unit_system') or ''),
    }
    return feat


# --------------------------------------------------------------------------- #
# Topics — implied by the signature
# --------------------------------------------------------------------------- #

def _r(feat):
    return feat['reinforcement']


TOPICS = [
    # (key, table label, predicate on the feature signature)
    ('reinforcement', 'Reinforcement & geosynthetics',
     lambda f: _r(f)['count'] > 0 and (
         'geosynthetic' in _r(f)['types']
         or ('generic' in _r(f)['types'] and 'tangent' in _r(f)['dirs']))),
    ('soil-nails', 'Soil nails',
     lambda f: 'nail' in _r(f)['types']),
    ('anchors-tiebacks', 'Anchors & tiebacks',
     lambda f: bool({'anchor', 'tieback'} & set(_r(f)['types']))),
    ('piles', 'Piles & drilled shafts',
     lambda f: f['piles'] > 0),
    ('cutoff-walls', 'Sheet-pile & cutoff walls',
     lambda f: f['cutoff_walls'] > 0),
    ('rapid-drawdown', 'Rapid drawdown',
     lambda f: f['rapid_drawdown']),
    ('transient-seepage', 'Transient seepage',
     lambda f: f['transient_seepage']),
    ('seepage-coupled', 'Seepage-coupled stability',
     lambda f: f['seepage_coupled']),
    ('probabilistic', 'Probabilistic & reliability',
     lambda f: f['probabilistic']),
    ('tension-cracks', 'Tension cracks',
     lambda f: f['tension_crack']),
    ('seismic', 'Seismic (pseudo-static)',
     lambda f: f['seismic_k'] != 0.0),
    ('non-circular', 'Non-circular surfaces',
     lambda f: f['non_circular']),
    ('zoned-dams', 'Layered & zoned dams',
     lambda f: f['n_materials'] >= 3 and (f['seepage_problem'] or f['piezo_line'])),
    ('homogeneous', 'Homogeneous benchmarks',
     lambda f: f['homogeneous']),
]

TOPIC_LABELS = {key: label for key, label, _ in TOPICS}


def topics_for(feat):
    return [key for key, _, pred in TOPICS if pred(feat)]


# --------------------------------------------------------------------------- #
# Example ranking
# --------------------------------------------------------------------------- #

CITATION_RE = re.compile(r'\(([^)]*\b(19|20)\d{2}[a-z]?\b[^)]*)\)')
PROPER_NOUN_RE = re.compile(r'\b[A-Z][a-z]{2,}\s+(Dam|Reservoir|Slope|Levee|Embankment)\b')


def example_score(title: str) -> int:
    """Rank named/published problems above bare ids.

    A parenthesised year is the corpus's own mark of an external source
    (``ACADS 1(a)``, ``Griffiths & Lane (1999)``, ``Huang & Jia 2008``); a named
    site (``Cannon Dam``) is the next best thing.
    """
    score = 0
    if CITATION_RE.search(title):
        score += 3
    if PROPER_NOUN_RE.search(title):
        score += 2
    return score


def pick_examples(entries, limit=6):
    """Choose up to `limit` examples for a topic, spread across source pages.

    Entries are (score, page, anchor, ...) records; the per-page cap is relaxed
    only when a topic cannot otherwise reach three examples, so a topic that
    genuinely lives on one page still gets a full row.
    """
    ranked = sorted(entries, key=lambda e: (-e['score'], e['page'], e['anchor']))
    for cap in (2, 3, len(ranked) or 1):
        chosen, per_page = [], {}
        for e in ranked:
            if per_page.get(e['page'], 0) >= cap:
                continue
            chosen.append(e)
            per_page[e['page']] = per_page.get(e['page'], 0) + 1
            if len(chosen) >= limit:
                break
        if len(chosen) >= min(3, len(ranked)):
            return chosen
    return chosen


def short_label(title: str) -> str:
    """A compact link label: the problem id plus a trimmed description."""
    title = re.sub(r'\s+', ' ', title).strip()
    for sep in (': ', ' — ', ' - '):
        head, found, tail = title.partition(sep)
        if found and len(head) <= 28:
            tail = tail.strip()
            if len(tail) > 42:
                tail = tail[:41].rstrip(' ,;(') + '…'
            return f'{head} — {tail}' if tail else head
    return title if len(title) <= 60 else title[:59].rstrip() + '…'


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def build_index(verbose=True):
    sys.path.insert(0, str(REPO_ROOT))
    from xslope.fileio import load_slope_data

    pages = sorted(DOCS.rglob('*.md'))
    # model path -> {'refs': [...]}
    models = {}
    unloadable = []
    n_tags = 0

    for md_path in pages:
        raw = md_path.read_text(encoding='utf-8')
        if '<!-- test:' not in raw:
            continue
        sections, tags = parse_page(md_path)
        url_path = page_url_path(md_path)
        for tag in tags:
            n_tags += 1
            sec, how = resolve_section(sections, tag)
            if sec is None:
                continue
            model = os.path.relpath(tag['_model'], REPO_ROOT)
            rec = models.setdefault(model, {'refs': {}})
            key = (url_path, sec.anchor)
            ref = rec['refs'].setdefault(key, {
                'page': url_path,
                'anchor': sec.anchor,
                'title': sec.title,
                'level': sec.level,
                'resolution': how,
                'url': f'{BASE_URL}{url_path}#{sec.anchor}',
                'source_md': str(md_path.relative_to(REPO_ROOT)),
                'checks': set(),
            })
            check = tag.get('benchmark') or tag.get('type', '')
            if check:
                ref['checks'].add(check)

    entries = []
    for model in sorted(models):
        abs_path = REPO_ROOT / model
        if not abs_path.exists():
            unloadable.append({'model': model, 'reason': 'file not found'})
            continue
        try:
            data = load_slope_data(str(abs_path))
        except Exception as exc:                                # noqa: BLE001
            unloadable.append({'model': model,
                               'reason': f'{type(exc).__name__}: {exc}'[:200]})
            if verbose:
                print(f'  unloadable: {model} — {type(exc).__name__}: {str(exc)[:90]}')
            continue
        feat = feature_signature(data)
        refs = []
        for key in sorted(models[model]['refs']):
            ref = dict(models[model]['refs'][key])
            ref['checks'] = sorted(ref['checks'])
            refs.append(ref)
        entries.append({
            'model': model,
            'topics': topics_for(feat),
            'references': refs,
            'features': feat,
        })

    topic_members = {key: [e['model'] for e in entries if key in e['topics']]
                     for key, _, _ in TOPICS}

    index = {
        'schema': SCHEMA_VERSION,
        'generated_by': 'tools/make_corpus_index.py',
        'base_url': BASE_URL,
        'stats': {
            'tags': n_tags,
            'models': len(entries),
            'unloadable': len(unloadable),
            'pages': sorted({r['page'] for e in entries for r in e['references']}),
            'topics': {key: len(topic_members[key]) for key, _, _ in TOPICS},
        },
        'topic_labels': {key: label for key, label, _ in TOPICS},
        'topics': {k: sorted(v) for k, v in topic_members.items()},
        'models': entries,
        'unloadable': sorted(unloadable, key=lambda u: u['model']),
    }
    return index


def render_table(index) -> str:
    """The TOPIC -> EXAMPLES markdown block injected into the skill."""
    by_model = {e['model']: e for e in index['models']}
    lines = [
        '### Worked examples by topic',
        '',
        'Cite these when a question matches a topic — they are verified pages carrying',
        'published comparisons against the source or vendor program, not illustrations.',
        '',
        '| Topic | Worked examples |',
        '|:------|:----------------|',
    ]
    for key, label, _ in TOPICS:
        members = index['topics'].get(key) or []
        if not members:
            continue        # no example in the corpus — say nothing rather than stretch
        cands = []
        for model in members:
            for ref in by_model[model]['references']:
                if ref['level'] <= 1:
                    # A page-title anchor is the whole corpus page, not a worked
                    # example; it only ever arises as a fallback for a tag that
                    # sits in a page's summary block with no section linking it.
                    continue
                cands.append({
                    'score': example_score(ref['title']),
                    'page': ref['page'],
                    'anchor': ref['anchor'],
                    'title': ref['title'],
                    'url': ref['url'],
                })
        # one row per section, deduplicated
        seen, uniq = set(), []
        for c in sorted(cands, key=lambda c: (c['page'], c['anchor'])):
            k = (c['page'], c['anchor'])
            if k in seen:
                continue
            seen.add(k)
            uniq.append(c)
        picks = pick_examples(uniq)
        cells = ' · '.join(f"[{short_label(p['title'])}]({p['url']})" for p in picks)
        lines.append(f'| {label} | {cells} |')
    lines.append('')
    return '\n'.join(lines)


def inject(skill_text: str, block: str) -> str:
    start = skill_text.find(BEGIN_MARKER)
    end = skill_text.find(END_MARKER)
    if start == -1 or end == -1:
        raise SystemExit(
            f'markers {BEGIN_MARKER} / {END_MARKER} not found in {SKILL_PATH}')
    return (skill_text[:start + len(BEGIN_MARKER)] + '\n' + block
            + skill_text[end:])


def serialize(index) -> str:
    return json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--check', action='store_true',
                    help='report whether the committed artifacts are stale; write nothing')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args(argv)
    verbose = not args.quiet

    index = build_index(verbose=verbose)
    index_text = serialize(index)
    block = render_table(index)

    skill_text = SKILL_PATH.read_text(encoding='utf-8')
    new_skill = inject(skill_text, block)

    stale = []
    if not INDEX_PATH.exists() or INDEX_PATH.read_text(encoding='utf-8') != index_text:
        stale.append(str(INDEX_PATH.relative_to(REPO_ROOT)))
    if new_skill != skill_text:
        stale.append(str(SKILL_PATH.relative_to(REPO_ROOT)))

    if args.check:
        if stale:
            print('stale: ' + ', '.join(stale))
            return 1
        if verbose:
            print('corpus index is current')
        return 0

    INDEX_PATH.write_text(index_text, encoding='utf-8')
    SKILL_PATH.write_text(new_skill, encoding='utf-8')
    BUNDLED_SKILL.write_text(new_skill, encoding='utf-8')
    if verbose:
        st = index['stats']
        print(f"corpus index: {st['models']} models from {st['tags']} tags "
              f"across {len(st['pages'])} pages"
              + (f", {st['unloadable']} unloadable" if st['unloadable'] else ''))
        for key, label, _ in TOPICS:
            n = st['topics'][key]
            print(f"   {label:34s} {n:4d}" + ('' if n else '   (no examples)'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
