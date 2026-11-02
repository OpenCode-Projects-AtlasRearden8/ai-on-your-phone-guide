# STATUS.md — The AI-on-Your-Phone Guide

*Updated: 2026-11-02*

## What was built

A complete, self-contained beginner manual for using AI on phones, written and maintained by Asdale Dynamics, LLC (Dylan Asdale), companion to *The Massive AI Manual*.

- **`docs/`** — Markdown source of the manual:
  - `index.md` — overview, who it's for, how to use it
  - `01-choosing-apps.md` — picking apps, official stores, copycat red flags
  - `02-on-device-vs-cloud.md` — where questions go, local vs cloud trade-offs, 10-second chooser
  - `03-voice-input.md` — dictation, voice conversation mode, workplace safety rules, troubleshooting
  - `04-privacy-settings.md` — the four switches that matter, postcard rule, never-share list
  - `05-battery-and-data.md` — honest data/battery numbers, three settings that matter
  - `06-accessibility.md` — text size, screen readers, camera-to-AI, ADHD-friendly/low-energy routines
- **`site/`** — generated static HTML mirroring the docs: shared stylesheet, chapter sidebar navigation, prev/next pagers, print styles (`@media print` hides navigation; Print → Save as PDF makes a clean paper copy), fully mobile-responsive.
- **`build.py`** — one-command site builder (`python3 build.py`). Uses the `markdown` package when available; ships a built-in mini converter fallback so the build succeeds on bare Python.
- **`tests/test_site.py`** — unittest suite (13 tests; see below).
- **`README.md`** — how to build, run, and read; credits Asdale Dynamics, LLC.
- **`LICENSE`** — MIT, exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it

- Build the site: `python3 build.py`
- Read it: open `site/index.html` in any browser, or serve with `python3 -m http.server -d site 8000` → <http://localhost:8000>
- Run tests: `python3 -m unittest discover -s tests -v`

## Verification results

- `python3 build.py` — passes; builds 7 pages + `style.css` from scratch.
- `python3 -m unittest discover -s tests -v` — **13/13 OK**, covering:
  - fresh build succeeds; all 7 HTML pages + CSS produced
  - every page has sidebar nav, exactly one active link, prev/next pager, colophon
  - print + mobile styles present
  - **every relative link in `docs/` and `site/` resolves to a real file** (tested links)
  - site is offline-only: zero JavaScript, zero external URLs/assets, local CSS only
  - no secrets or API-key patterns anywhere in the repo
  - LICENSE/README required lines present; all six required chapter topics exist
- Fallback mini-Markdown converter verified on all seven chapters (build runs without `pip install markdown`).
- Git initialized; single plain commit as the existing identity (`772c1af`).

## Constraints honored

- Zero API keys, zero accounts, no remote resources, no publishing — static files only.
- Plain-English tone throughout; education-only (no medical/legal/financial advice).
- MIT `LICENSE` with the exact copyright line; README credits Asdale Dynamics, LLC.

## Known gaps

- Voice-input and accessibility UI details describe iOS/Android behavior generically; exact menu names drift between OS versions and were not verified against live devices.
- Data/battery numbers in Chapter 5 are honest approximations, not measured benchmarks.
- Site search isn't included (browser Ctrl+F is the search story); no table of contents per page, just chapter navigation.
- No CI configuration; tests are run manually via `python3 -m unittest discover -s tests -v`.
- GitHub Pages hosting is *documented* (commit `site/` and enable Pages) but was not set up or published — intentionally, since this repo must not be published.
