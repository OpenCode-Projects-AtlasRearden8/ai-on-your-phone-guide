#!/usr/bin/env python3
"""Build the static HTML site for The AI-on-Your-Phone Guide.

Reads Markdown chapters from docs/ and writes plain, offline HTML files to
site/. No accounts, no API keys, no external resources: everything the
pages need (styles, text, images-if-any) is local. Run:

    python3 build.py

Requires the `markdown` package (pip install markdown). If it is missing,
a small built-in fallback converter is used instead so the build still
succeeds on a bare Python install.
"""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

COURSE = [
    "index.md",
    "01-choosing-apps.md",
    "02-on-device-vs-cloud.md",
    "03-voice-input.md",
    "04-privacy-settings.md",
    "05-battery-and-data.md",
    "06-accessibility.md",
]

TITLE = "The AI-on-Your-Phone Guide"
BYLINE = "A plain-English manual by Dylan Asdale - Asdale Dynamics, LLC"

CSS = """\
:root {
  --bg: #fdfcf9;
  --ink: #22252a;
  --muted: #5c6470;
  --accent: #1f6f50;
  --accent-soft: #e7f2ec;
  --border: #dde0e4;
  --card: #ffffff;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font: 17px/1.65 Georgia, "Times New Roman", serif;
}
.layout { display: flex; min-height: 100vh; max-width: 1100px; margin: 0 auto; }
nav.toc {
  width: 260px; flex: none; padding: 24px 18px;
  border-right: 1px solid var(--border);
}
nav.toc h2 {
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 13px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--muted); margin: 0 0 10px;
}
nav.toc ol { list-style: none; margin: 0; padding: 0; }
nav.toc li { margin: 0; }
nav.toc a {
  display: block; padding: 7px 10px; margin: 2px 0;
  color: var(--ink); text-decoration: none; border-radius: 8px;
  font-family: "Helvetica Neue", Arial, sans-serif; font-size: 15px;
}
nav.toc a:hover { background: var(--accent-soft); }
nav.toc a.active { background: var(--accent-soft); color: var(--accent); font-weight: 600; }
main { flex: 1; min-width: 0; padding: 36px 40px 72px; max-width: 46em; }
header.site-header {
  padding: 26px 40px 0; max-width: 1100px; margin: 0 auto;
}
header.site-header h1 {
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 18px; margin: 0;
}
header.site-header p { margin: 2px 0 0; color: var(--muted); font-size: 14px; }
main h1 { font-size: 1.9em; line-height: 1.2; margin: 0 0 .4em; }
main h2 { font-size: 1.35em; margin: 1.7em 0 .5em; color: var(--accent); }
main h3 { font-size: 1.1em; margin: 1.4em 0 .4em; }
main p, main li { color: #2c3038; }
main blockquote {
  margin: 1.4em 0; padding: 12px 18px;
  border-left: 4px solid var(--accent); background: var(--accent-soft);
  border-radius: 0 10px 10px 0;
}
main blockquote p { margin: .3em 0; }
main code {
  font: 90%/1.5 ui-monospace, Consolas, monospace;
  background: #eef0ee; border-radius: 5px; padding: 1px 6px;
}
main table { border-collapse: collapse; width: 100%; margin: 1.4em 0; font-size: .94em; }
main th, main td { border: 1px solid var(--border); padding: 8px 10px; text-align: left; vertical-align: top; }
main th { background: #f3f4f2; font-family: "Helvetica Neue", Arial, sans-serif; font-size: 13px; }
main ul, main ol { padding-left: 1.5em; }
main li { margin: .35em 0; }
main hr { border: 0; border-top: 1px solid var(--border); margin: 2em 0; }
main a { color: var(--accent); }
footer.pager { margin-top: 3em; display: flex; justify-content: space-between; gap: 16px; }
footer.pager a {
  font-family: "Helvetica Neue", Arial, sans-serif; font-size: 14px;
  color: var(--accent); text-decoration: none; padding: 10px 14px;
  border: 1px solid var(--border); border-radius: 10px; background: var(--card);
}
footer.pager a:hover { background: var(--accent-soft); }
footer.pager .placeholder { visibility: hidden; }
footer.colophon {
  margin-top: 2.5em; color: var(--muted); font-size: 13px;
  font-family: "Helvetica Neue", Arial, sans-serif;
}
.menu-toggle { display: none; }
@media (max-width: 800px) {
  .layout { display: block; }
  nav.toc { width: auto; border-right: 0; border-bottom: 1px solid var(--border); position: static; }
  main { padding: 24px 20px 56px; }
}

/* Print styles: paper-friendly, no navigation clutter. */
@media print {
  :root { --card: #fff; }
  body { background: #fff; font-size: 12pt; }
  nav.toc, .menu-toggle, footer.pager { display: none !important; }
  .layout { display: block; max-width: none; }
  main { max-width: none; padding: 0; }
  main h1 { page-break-before: always; }
  main h1:first-child { page-break-before: avoid; }
  main h2, main h3 { page-break-after: avoid; }
  main table { page-break-inside: avoid; }
  main a { color: #1c1c1c; text-decoration: none; }
  footer.colophon { border-top: 1px solid #999; padding-top: 8px; }
}
"""


def slug_from_name(markdown_name: str) -> str:
    return markdown_name.replace(".md", ".html")


class MiniMarkdown:
    """Very small Markdown subset used only when the `markdown` package is absent.

    Handles: headings, paragraphs, emphasis/strong/code, links, blockquotes,
    unordered/ordered lists, tables, and horizontal rules. Deliberately simple;
    the pip package always wins when available.
    """

    INLINE = [
        (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
        (re.compile(r"(?<!\w)\*([^*\n]+)\*(?!\w)"), r"<em>\1</em>"),
        (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
        (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"),
         lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1))),
    ]

    def convert(self, md_text: str) -> str:
        out: list[str] = []
        lines = md_text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped:
                i += 1
                continue
            if stripped == "---":
                out.append("<hr>")
                i += 1
                continue
            if stripped.startswith(">"):
                block = []
                while i < len(lines) and lines[i].strip().startswith(">"):
                    block.append(lines[i].strip().lstrip(">").strip())
                    i += 1
                out.append("<blockquote><p>%s</p></blockquote>" %
                           self._inline(" ".join(block)))
                continue
            if stripped.startswith("|") and i + 1 < len(lines) and \
                    set(lines[i + 1].strip()) <= set("|-: "):
                header = [c.strip() for c in stripped.strip("|").split("|")]
                i += 2
                body = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    body.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                    i += 1
                out.append(self._table(header, body))
                continue
            m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
            if m:
                level = max(1, len(m.group(1)))
                out.append("<h%d>%s</h%d>" % (level, self._inline(m.group(2)), level))
                i += 1
                continue
            if stripped[:2] in ("- ", "* "):
                items, i = self._list(lines, i, re.compile(r"^[-*]\s+"))
                out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % it for it in items))
                continue
            if re.match(r"^\d+\.\s", stripped):
                items, i = self._list(lines, i, re.compile(r"^\d+\.\s+"))
                out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % it for it in items))
                continue
            block = []
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith("#"):
                block.append(lines[i].strip())
                i += 1
            out.append("<p>%s</p>" % self._inline(" ".join(block)))
        return "\n".join(out)

    def _list(self, lines, i, pattern):
        items = []
        while i < len(lines) and pattern.match(lines[i].strip()):
            text = pattern.sub("", lines[i].strip())
            i += 1
            while i < len(lines) and lines[i].startswith("  ") and lines[i].strip():
                text += " " + lines[i].strip()
                i += 1
            items.append(self._inline(text))
        return items, i

    def _table(self, header, body):
        th = "".join("<th>%s</th>" % self._inline(c) for c in header)
        rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % self._inline(c) for c in row)
                       for row in body)
        return "<table><tr>%s</tr>%s</table>" % (th, rows)

    def _inline(self, text):
        for pat, rep in self.INLINE:
            text = pat.sub(rep, text)
        return text


def render_markdown(md_text: str) -> str:
    try:
        import markdown  # type: ignore

        return markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    except Exception:
        return MiniMarkdown().convert(md_text)


def extract_h1(md_text: str, fallback: str = "") -> str:
    m = re.search(r"^#\s+(.+?)\s*$", md_text, re.MULTILINE)
    return m.group(1) if m else fallback


def build_page(page_name: str, md_text: str, body: str) -> str:
    title = extract_h1(md_text, page_name)
    nav_items = []
    for name in COURSE:
        label = extract_h1((DOCS / name).read_text(encoding="utf-8"),
                           fallback=name.rsplit(".", 1)[0])
        active = ' class="active"' if name == page_name else ""
        nav_items.append(f'      <li><a href="{slug_from_name(name)}"{active}>{html.escape(label)}</a></li>')
    nav_html = "\n".join(nav_items)

    idx = COURSE.index(page_name)
    prev_html = next_html = '<span class="placeholder"></span>'
    if idx > 0:
        p = COURSE[idx - 1]
        prev_html = f'<a href="{slug_from_name(p)}">&larr; {html.escape(extract_h1((DOCS / p).read_text(encoding="utf-8"))[:44])}</a>'
    if idx < len(COURSE) - 1:
        n = COURSE[idx + 1]
        next_html = f'<a href="{slug_from_name(n)}">{html.escape(extract_h1((DOCS / n).read_text(encoding="utf-8"))[:44])} &rarr;</a>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="A plain-English manual for using AI on your phone: choosing apps, on-device vs cloud models, voice input, privacy, battery and data, and accessibility.">
<title>{html.escape(title if title == TITLE else f"{title} - {TITLE}")}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header">
  <h1>{html.escape(TITLE)}</h1>
  <p>{html.escape(BYLINE)}</p>
</header>
<div class="layout">
  <nav aria-label="Chapters" class="toc">
    <h2>Chapters</h2>
    <ol>
{nav_html}
    </ol>
  </nav>
  <main>
{body}
    <footer class="pager">
      {prev_html}
      {next_html}
    </footer>
    <footer class="colophon">
      <p>The AI-on-Your-Phone Guide - a plain-English manual from Asdale Dynamics, LLC.
      Runs entirely offline; nothing here requires an account or a key.</p>
    </footer>
  </main>
</div>
</body>
</html>
"""


def main() -> None:
    if not DOCS.is_dir():
        raise SystemExit(f"docs/ not found next to {Path(__file__).name}")

    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()

    pages = {}
    for name in COURSE:
        md_text = (DOCS / name).read_text(encoding="utf-8")
        pages[name] = render_markdown(md_text)

    for name, body in pages.items():
        body = re.sub(r'href="\.\./docs/([^"#]+)\.md', r'href="\1.html', body)
        body = re.sub(r'href="([^"#]+)\.md', r'href="\1.html', body)
        (SITE / slug_from_name(name)).write_text(
            build_page(name, (DOCS / name).read_text(encoding="utf-8"), body),
            encoding="utf-8")

    (SITE / "style.css").write_text(CSS, encoding="utf-8")

    print(f"Built {len(pages)} pages + style.css -> {SITE.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
