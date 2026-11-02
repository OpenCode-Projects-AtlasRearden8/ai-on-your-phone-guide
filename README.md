# The AI-on-Your-Phone Guide

*A plain-English manual for using AI on the phone already in your pocket — choosing apps, on-device vs cloud models, voice input, privacy settings, battery and data tips, and accessibility extras.*

Written and maintained by **Asdale Dynamics, LLC** (Dylan Asdale), companion to the book *The Massive AI Manual* and the hub site dylanasdale.github.io.

## What this is

- **`docs/`** — the manual as Markdown chapters. Read them here, on any device, in any editor.
- **`site/`** — the same chapters as a small static HTML website with chapter navigation, mobile-friendly layout, and print styles (Print → Save as PDF gives a clean paper copy).
- **`build.py`** — builds `site/` from `docs/` in one command.
- **`tests/test_site.py`** — checks the build, verifies every internal link resolves, and confirms the site stays offline-only (no external assets, no keys, no accounts).

The site is **fully self-contained**: no CDN, no fonts to fetch, no JavaScript, no analytics. Zero accounts, zero API keys. It works from a folder on a phone, a USB stick, or GitHub Pages.

## How to build

    python3 build.py

Output: `site/index.html`, six chapter pages, and `style.css`.

Optionally install the Python `markdown` package first (`pip install markdown`); with it, richer Markdown rendering is used. Without it, a tiny built-in fallback converter still produces a complete, readable site.

## How to run the tests

    python3 -m unittest discover -s tests -v

## How to read the site

- Open `site/index.html` in any browser — it links to every chapter in the sidebar.
- Serve locally if you prefer: `python3 -m http.server -d site 8000`, then visit <http://localhost:8000>.

## The chapters

1. [Choosing AI Apps](docs/01-choosing-apps.md) — picking well-known apps from official stores, dodging copycats
2. [On-Device vs Cloud Models](docs/02-on-device-vs-cloud.md) — where your questions go and when it matters
3. [Voice Input](docs/03-voice-input.md) — talking to AI instead of typing
4. [Privacy Settings](docs/04-privacy-settings.md) — the four switches that matter and the postcard rule
5. [Battery and Data Tips](docs/05-battery-and-data.md) — what actually drains data and battery (spoiler: not typed chats)
6. [Accessibility Extras](docs/06-accessibility.md) — bigger text, screen readers, hands-free, low-energy routines

## Who it's for

Beginners who want AI explained *like a friend would*: plain English, step by step, never condescending — including nurses and shift workers, folks on older phones or limited data, and anyone who cares where their private things go. Education only; nothing here is medical, legal, or financial advice.

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Asdale Dynamics, LLC
