# website

Static Bootstrap 4 site for the WiSE Lab, built with [Hugo](https://gohugo.io/)
(migrated from Jekyll).

## Making Updates

Modify content and push. Commits to `master` are built by GitHub Actions
(`.github/workflows/build-hugo.yml`) and rsynced to the live server.

### News

The news list is a simple markdown block: [`assets/news.md`](assets/news.md).

### Projects

Add a markdown file to [`content/projects/`](content/projects/) with front matter:

```yaml
---
title:  "[title]"
image: "/img/projects/[filename]"
priority: [int]
---
```

The body is a markdown-enabled description. Projects are listed in ascending
`priority` order — `priority` is simply the position in the list (1 = first), so
give each project a unique value. Images should be 3:2, ideally 510px × 340px, in
`static/img/projects/`.

### Team Members

Add an entry to [`data/team.yaml`](data/team.yaml) (move to
[`data/alumni.yaml`](data/alumni.yaml) as applicable):

```yaml
- firstname: "[firstname]"
  lastname: "[lastname]"
  priority: [int]
  title: "[title]"
  affiliation: "[department/school]"
  website: "[url]"        # optional
  image: "/img/team/[filename]"   # empty string -> anon.png
```

Images should be square, ideally 450px × 450px, in `static/img/team/`.
Members are sorted first by priority, then by last name.

### Publications

Add/update the BibTeX file [`_pubs/wise.bib`](_pubs/wise.bib) and push — that's it.
The deploy workflow regenerates the publications list and the
`static/bibliography/<key>.html` detail pages from it automatically
([`scripts/gen_bib.py`](scripts/gen_bib.py)).

_Optional — only to preview the publications page in a local `hugo server`:_

```bash
python3 -m venv .bibvenv && .bibvenv/bin/pip install -r scripts/requirements.txt
.bibvenv/bin/python scripts/gen_bib.py
```

Supported custom fields (same as the old jekyll-scholar setup):

- `link`: URL to an external reference. Displayed as `(Link)`.
- `pdf`: URL to a PDF. Displayed as `(PDF)`.
- `award`: Award mention, shown in red at the end of the entry.

**NOTE:** Tilde characters (`~`) in `pdf`/`link` must be escaped as `\%7E`.

## How the bibliography works

Hugo has no BibTeX/citeproc engine, so [`scripts/gen_bib.py`](scripts/gen_bib.py)
replaces jekyll-scholar: it parses `wise.bib`, renders each entry in APA style via
`citeproc-py` + the bundled [`scripts/apa.csl`](scripts/apa.csl), groups entries by
year (newest first), and emits the data + detail pages consumed by
[`layouts/partials/bibliography.html`](layouts/partials/bibliography.html). Output
matches the previous jekyll-scholar rendering.

## Directory layout

```
hugo.toml                 site config
content/                  pages (_index, about, publications) + projects/
data/                     team.yaml, alumni.yaml, publications.json (generated)
assets/                   css/main.scss (+ bootstrap), news.md  (Hugo Pipes)
static/                   img/, js/, favicons, bibliography/ (generated)
layouts/                  templates (baseof, partials, section/page layouts)
scripts/                  gen_bib.py, apa.csl, requirements.txt
_pubs/wise.bib            bibliography source
```

## Local Development

* Install the **extended** edition of Hugo (needed for the SCSS pipeline):
  <https://gohugo.io/installation/>
* Preview with `hugo server` at <http://localhost:1313>
* Build the production site into `public/` with `hugo --minify`

> The publications list is generated from `_pubs/wise.bib` by the deploy workflow at
> build time (see [Publications](#publications)) — nothing to run by hand.
> `data/publications.json` and `static/bibliography/` are build artifacts and are
> git-ignored; if you want the publications page to appear in a local `hugo server`
> preview, generate them once (see below).
