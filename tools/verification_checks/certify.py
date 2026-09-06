#!/usr/bin/env python3
"""Change-gated runner for the verification-page checkers.

``certified.json`` records, for each page, the SHA-256 of the page's content as
it stood when the checks last passed and the developer signed off.  On a run:

* hash matches  -> the page is reported "unchanged, certified" and nothing else
                   runs.  This is what keeps the check cheap in the default
                   suite: one file read per page.
* hash differs  -> every check runs.  If they all pass the page is still a
                   FAILURE until the manifest is updated, because certifying a
                   page is a deliberate act: the developer must have read the
                   flags the checks raised while the page was being edited.
                   ``--recertify`` runs the checks and, on success, writes the
                   new hash.

Usage
-----
    python -m tools.verification_checks.certify              # check all pages
    python -m tools.verification_checks.certify rs2 seep     # check some
    python -m tools.verification_checks.certify --recertify rs2
    python -m tools.verification_checks.certify --force      # ignore hashes
"""
import hashlib
import json
import os
import sys

from . import deltas, dots, figures, tags, untagged, voice
from .pages import ORDER, PAGES

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PAGE_DIR = os.path.join(REPO, "docs", "verification")
MANIFEST = os.path.join(HERE, "certified.json")

RECERTIFY_HINT = (
    "run `python -m tools.verification_checks.certify --recertify {page}` and "
    "commit the updated tools/verification_checks/certified.json alongside the "
    "page change")


def page_path(name):
    return os.path.join(PAGE_DIR, name + ".md")


def page_hash(name):
    with open(page_path(name), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_manifest():
    if not os.path.exists(MANIFEST):
        return {}
    with open(MANIFEST) as fh:
        return json.load(fh).get("pages", {})


def save_manifest(pages):
    with open(MANIFEST, "w") as fh:
        json.dump({
            "_comment": "Content hash of each verification page as last "
                        "certified by tools/verification_checks. A page whose "
                        "hash differs is re-checked in full; see README.md.",
            "pages": {k: pages[k] for k in sorted(pages)},
        }, fh, indent=1)
        fh.write("\n")


def check_page(name, report=print):
    """Run every check on one page.  Returns the failure count."""
    cfg = PAGES[name]
    path = page_path(name)
    fails = 0
    n, _ = deltas.run(path, cfg, report=report)
    fails += n
    fails += tags.run(path, cfg, report=report)
    fails += figures.run(path, cfg, report=report)
    fails += voice.run(path, cfg, report=report)
    fails += dots.run(path, cfg, report=report)
    # Reports its findings and returns 0 while `untagged.ENFORCING` is False —
    # every flag is a sentence that has to be read before it can be trimmed,
    # tagged or allowed.  See untagged.py.
    fails += untagged.run(path, cfg, report=report)
    return fails


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    recertify = "--recertify" in argv
    force = "--force" in argv
    quiet = "--quiet" in argv
    names = [a for a in argv if not a.startswith("-")] or list(ORDER)
    for n in names:
        if n not in PAGES:
            print(f"unknown page {n!r}; known: {', '.join(ORDER)}")
            return 2

    manifest = load_manifest()
    report = (lambda *a: None) if quiet else print
    failed, stale, updated = [], [], False
    for name in names:
        h = page_hash(name)
        if not force and not recertify and manifest.get(name) == h:
            print(f"{name}.md: unchanged, certified")
            continue
        if not quiet:
            print(f"--- {name}.md: content changed since certification, "
                  f"running all checks")
        n = check_page(name, report=report)
        if n:
            print(f"{name}.md: FAILED ({n} problem(s))")
            failed.append(name)
            continue
        if recertify:
            manifest[name] = h
            updated = True
            print(f"{name}.md: checks pass — certified at {h[:12]}")
        else:
            print(f"{name}.md: checks pass but the manifest is stale — "
                  + RECERTIFY_HINT.format(page=name))
            stale.append(name)
    if updated:
        save_manifest(manifest)
    if failed or stale:
        return len(failed) + len(stale)
    return 0


if __name__ == "__main__":
    sys.exit(main())
