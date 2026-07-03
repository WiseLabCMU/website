#!/usr/bin/env python3
"""Generate the publications data + BibTeX detail pages from _pubs/wise.bib.

This replaces the old jekyll-scholar pipeline. Hugo has no BibTeX/citeproc
engine, so this script does the BibTeX -> HTML step at build time:

  _pubs/wise.bib  ->  data/publications.json         (consumed by the
                      static/bibliography/<key>.html   publications template)

Rendering uses the real APA CSL style (scripts/apa.csl) via citeproc-py, so
citations stay in the same style Jekyll produced. Parsing uses bibtexparser
(robust) and we hand-build CSL-JSON, because citeproc-py's own BibTeX reader
crashes on a few real-world author strings in this file.

Run it after editing wise.bib:  python scripts/gen_bib.py
(CI runs it automatically before `hugo`.)
"""
import json
import os
import re

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode, splitname
from bibtexparser.latexenc import latex_to_unicode

from citeproc import (CitationStylesStyle, CitationStylesBibliography,
                      Citation, CitationItem, formatter)
from citeproc.source.json import CiteProcJSON

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIB = os.path.join(ROOT, "_pubs", "wise.bib")
CSL = os.path.join(ROOT, "scripts", "apa.csl")
DATA_OUT = os.path.join(ROOT, "data", "publications.json")
DETAIL_DIR = os.path.join(ROOT, "static", "bibliography")

# bibtex entry type -> CSL type
TYPE_MAP = {
    "article": "article-journal",
    "inproceedings": "paper-conference",
    "conference": "paper-conference",
    "incollection": "chapter",
    "inbook": "chapter",
    "book": "book",
    "techreport": "report",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "misc": "article",
    "unpublished": "manuscript",
}


def strip_braces(s):
    return s.replace("{", "").replace("}", "").strip()


def polish(s, has_container=False):
    """Fix APA punctuation that citeproc-py 0.9.3 renders differently from the
    citeproc-ruby engine Jekyll used (all deterministic, style-level fixes)."""
    # citeproc-py doesn't merge a period after terminal '?'/'!' or a duplicate '.'
    s = s.replace("?.", "?").replace("!.", "!")
    s = re.sub(r"(?<!\.)\.\.(?!\.)", ".", s)  # "A.." -> "A." but keep "..."
    # APA uses an Oxford comma before the final ampersand; citeproc-py drops the
    # ", " delimiter ("E.&amp; R" -> "E., &amp; R")
    s = re.sub(r"(?<=[^\s,])&amp; ", ", &amp; ", s)
    # ensure a space before a trailing DOI/URL
    s = re.sub(r"(?<=\S)(https?://)", r" \1", s)
    # BibTeX "--" -> en-dash in titles/venues (citeproc-ruby did this everywhere)
    s = s.replace("--", "–")
    # APA title-case capitalizes after a hyphen ("Energy-efficiency" ->
    # "Energy-Efficiency"); citeproc-py doesn't. Only the title-cased venue is
    # italicized, and only when the work has a container (otherwise <i> wraps the
    # sentence-cased title of a standalone work, which must not be touched).
    if has_container:
        s = re.sub(r"<i>(.*?)</i>",
                   lambda m: "<i>" + re.sub(r"-([a-z])",
                                            lambda h: "-" + h.group(1).upper(),
                                            m.group(1)) + "</i>",
                   s)
    # typographic apostrophes, as citeproc-ruby's locale produced
    s = s.replace("'", "’")
    return s


def to_names(field):
    """Parse a BibTeX author/editor field into CSL-JSON name dicts."""
    out = []
    # BibTeX separates names with a whitespace-delimited "and"
    for chunk in re.split(r"\s+and\s+", field.strip()):
        chunk = chunk.strip().rstrip(",").strip()
        if not chunk:
            continue
        # Protect multi-word brace surnames (e.g. "{Simunic Rosing}") as a single
        # token, but leave accent groups (e.g. "{\'e}") for LaTeX decoding.
        def protect(m):
            inner = m.group(1)
            return inner.replace(" ", "\x00") if " " in inner else m.group(0)
        decoded = latex_to_unicode(re.sub(r"\{([^{}]*)\}", protect, chunk))
        try:
            parts = splitname(decoded, strict_mode=False)
        except Exception:
            out.append({"literal": strip_braces(decoded.replace("\x00", " "))})
            continue

        def join(tokens):
            return strip_braces(" ".join(tokens).replace("\x00", " "))

        family = join(parts.get("last", []))
        given = join(parts.get("first", []))
        von = join(parts.get("von", []))
        jr = join(parts.get("jr", []))
        if not family and not given:
            continue
        name = {}
        if family:
            name["family"] = family
        if given:
            name["given"] = given
        if von:
            name["non-dropping-particle"] = von
        if jr:
            name["suffix"] = jr
        if not name:
            name = {"literal": strip_braces(chunk)}
        out.append(name)
    return out


def raw_entry_blocks(text):
    """Yield (key, raw_text) for each @entry, brace-balanced, in file order."""
    i, n = 0, len(text)
    while i < n:
        at = text.find("@", i)
        if at == -1:
            break
        brace = text.find("{", at)
        if brace == -1:
            break
        # key is between the first '{' and the first ','
        comma = text.find(",", brace)
        key = text[brace + 1:comma].strip()
        # walk braces to find the matching close
        depth = 0
        j = brace
        while j < n:
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        raw = text[at:j + 1]
        yield key, raw
        i = j + 1


def main():
    with open(BIB, encoding="utf-8") as f:
        raw = f.read()

    # Strip non-entry junk lines (Jekyll front matter, stray markdown/text)
    cleaned = "\n".join(
        ln for ln in raw.splitlines()
        if ln.strip() != "---"
        and not ln.strip().startswith("## ")
        and not ln.strip().startswith("BibTeX |")
    )

    # Raw blocks preserve original key case + source text for detail pages
    raw_by_key = {}
    order = []
    for key, block in raw_entry_blocks(cleaned):
        raw_by_key[key] = block
        order.append(key)

    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    parser.customization = convert_to_unicode
    db = bibtexparser.loads(cleaned, parser=parser)
    entries = {e["ID"]: e for e in db.entries}

    # A second parse without convert_to_unicode keeps the braces intact in
    # author/editor fields, which we need to protect multi-word surnames.
    raw_parser = BibTexParser(common_strings=True)
    raw_parser.ignore_nonstandard_types = False
    raw_db = bibtexparser.loads(cleaned, parser=raw_parser)
    raw_entries = {e["ID"]: e for e in raw_db.entries}

    # Build CSL-JSON for every entry (keyed by original key)
    csl_items = []
    meta = {}  # key -> {pdf, link, award}
    for key in order:
        e = entries.get(key)
        if e is None:
            continue
        etype = e.get("ENTRYTYPE", "misc").lower()
        raw_e = raw_entries.get(key, e)
        item = {"id": key, "type": TYPE_MAP.get(etype, "article-journal")}
        if "author" in raw_e:
            item["author"] = to_names(raw_e["author"])
        if "editor" in raw_e:
            item["editor"] = to_names(raw_e["editor"])
        if "title" in e:
            item["title"] = strip_braces(e["title"])
        year = e.get("year", "").strip()
        m = re.search(r"\d{4}", year)
        if m:
            item["issued"] = {"date-parts": [[int(m.group())]]}
        container = e.get("booktitle") or e.get("journal")
        if container:
            item["container-title"] = strip_braces(container)
        if "publisher" in e:
            item["publisher"] = strip_braces(e["publisher"])
        if "volume" in e:
            item["volume"] = strip_braces(e["volume"])
        if "number" in e:
            item["issue"] = strip_braces(e["number"])
        if "pages" in e:
            # BibTeX "--" ranges -> single hyphen so citeproc en-dashes them
            item["page"] = strip_braces(e["pages"]).replace("--", "-")
        if "doi" in e:
            item["DOI"] = strip_braces(e["doi"])
        if "url" in e:
            item["URL"] = strip_braces(e["url"])
        csl_items.append(item)

        meta[key] = {
            "pdf": strip_braces(e["pdf"]).replace("\\%", "%") if "pdf" in e else "",
            "link": strip_braces(e["link"]).replace("\\%", "%") if "link" in e else "",
            "award": strip_braces(e["award"]) if "award" in e else "",
            "year": m.group() if m else "",
        }

    # Render every citation through the APA CSL
    bib_source = CiteProcJSON(csl_items)
    style = CitationStylesStyle(CSL, validate=False)
    bibliography = CitationStylesBibliography(style, bib_source, formatter.html)
    keys_in_order = [it["id"] for it in csl_items]
    has_container = {it["id"]: "container-title" in it for it in csl_items}
    for key in keys_in_order:
        bibliography.register(Citation([CitationItem(key)]))
    rendered = {}
    for key, item in zip(keys_in_order, bibliography.bibliography()):
        rendered[key] = polish(str(item), has_container[key])

    # Group by year (descending), preserving bib order within a year
    groups = {}
    for key in keys_in_order:
        yr = meta[key]["year"] or "n.d."
        groups.setdefault(yr, []).append(key)

    def year_sort_key(y):
        return int(y) if y.isdigit() else -1

    out_groups = []
    for yr in sorted(groups, key=year_sort_key, reverse=True):
        out_entries = []
        for key in groups[yr]:
            out_entries.append({
                "key": key,
                "citation": rendered[key],
                "pdf": meta[key]["pdf"],
                "link": meta[key]["link"],
                "award": meta[key]["award"],
            })
        out_groups.append({"year": yr, "entries": out_entries})

    os.makedirs(os.path.dirname(DATA_OUT), exist_ok=True)
    with open(DATA_OUT, "w", encoding="utf-8") as f:
        json.dump({"groups": out_groups}, f, indent=2, ensure_ascii=False)

    # Detail pages: raw source BibTeX inside a <pre>. jekyll-scholar mapped
    # ':' in keys to '_' for the filename; keep that so existing links work.
    os.makedirs(DETAIL_DIR, exist_ok=True)
    # Clear stale pages so removing/renaming a bib entry doesn't orphan its page.
    for old in os.listdir(DETAIL_DIR):
        if old.endswith(".html"):
            os.remove(os.path.join(DETAIL_DIR, old))
    for key in keys_in_order:
        fname = key.replace(":", "_") + ".html"
        block = raw_by_key.get(key, "").strip()
        html = "<html>\n<body>\n<pre>\n{}\n</pre>\n</body>\n</html>".format(block)
        with open(os.path.join(DETAIL_DIR, fname), "w", encoding="utf-8") as f:
            f.write(html)

    total = sum(len(g["entries"]) for g in out_groups)
    print("publications:", total, "entries,", len(out_groups), "years")
    print("detail pages:", len(keys_in_order))


if __name__ == "__main__":
    main()
