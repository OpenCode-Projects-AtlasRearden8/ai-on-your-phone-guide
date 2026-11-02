"""Tests for The AI-on-Your-Phone Guide.

Run with:  python3 -m unittest discover -s tests -v

What is covered:
- the build runs clean from scratch and produces every page + style.css
- the generated HTML includes chapter navigation, prev/next pagers, print styles
- every relative link inside docs/ and site/ resolves to an existing file
- the site is offline-only: no external resources, no JavaScript, no third-party code
- no secrets or API keys anywhere in the repo
- required project files exist and carry the correct license/copyright lines
"""

from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

CHAPTERS = [
    "index.html",
    "01-choosing-apps.html",
    "02-on-device-vs-cloud.html",
    "03-voice-input.html",
    "04-privacy-settings.html",
    "05-battery-and-data.html",
    "06-accessibility.html",
]

MD_CHAPTERS = [p.replace(".html", ".md") for p in CHAPTERS]

SECRET_PATTERNS = [
    re.compile(r"sk-(ant-)?[A-Za-z0-9]{20}"),                          # OpenAI/Anthropic-style keys
    re.compile(r"(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"]?[A-Za-z0-9]",
               re.IGNORECASE),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),                           # GitHub PATs
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),                               # AWS access keys
]

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
HTML_LINK = re.compile(r'href="([^"#]+)"')
EXTERNAL_URL = re.compile(r'^https?://')


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


class BuildTests(unittest.TestCase):
    """The build runs clean from scratch and produces a complete site."""

    def test_build_fresh_site(self):
        result = run([sys.executable, "build.py"])
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in CHAPTERS:
            self.assertTrue((SITE / name).is_file(), f"missing site/{name}")
        self.assertTrue((SITE / "style.css").is_file(), "missing site/style.css")

    def test_pages_have_nav_pagers_colophon(self):
        for name in CHAPTERS:
            page = (SITE / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertIn('class="toc"', page)
                self.assertIn("Chapters", page)
                self.assertIn('class="pager"', page)
                self.assertIn("colophon", page)
                self.assertIn("Asdale Dynamics, LLC", page)
                # exactly one chapter marked active in the sidebar
                self.assertEqual(page.count(' class="active"'), 1)

    def test_print_and_mobile_styles(self):
        css = (SITE / "style.css").read_text(encoding="utf-8")
        self.assertIn("@media print", css)
        self.assertIn("page-break", css)
        self.assertIn("display: none", css)  # nav/pagers hidden on paper
        self.assertIn("@media (max-width", css)  # phone-friendly layout

    def test_pages_link_to_each_other(self):
        pages = {name: (SITE / name).read_text(encoding="utf-8") for name in CHAPTERS}
        for name in CHAPTERS[:-1]:
            self.assertIn(CHAPTERS[CHAPTERS.index(name) + 1],
                          HTML_LINK.findall(pages[name]), f"{name} lacks next link")
        for name in CHAPTERS[1:]:
            self.assertIn(CHAPTERS[CHAPTERS.index(name) - 1],
                          HTML_LINK.findall(pages[name]), f"{name} lacks prev link")


class LinkTests(unittest.TestCase):
    """Every tested link inside the repo resolves to a real file."""

    def resolve(self, link: str, source_dir: Path) -> Path:
        self.assertFalse(link.startswith("/"), f"absolute link {link!r} in {source_dir}")
        return (source_dir / link).resolve()

    def test_markdown_relative_links_resolve(self):
        for name in MD_CHAPTERS:
            text = (DOCS / name).read_text(encoding="utf-8")
            matches = MARKDOWN_LINK.findall(text)
            self.assertTrue(matches, f"{name} should link to the next chapter at least")
            for link in matches:
                self.assertFalse(EXTERNAL_URL.match(link),
                                 f"{name} contains external URL: {link}")
                target = self.resolve(link, DOCS)
                self.assertTrue(target.exists(), f"broken link {link!r} in {name}")

    def test_html_relative_links_resolve(self):
        for name in CHAPTERS:
            page = (SITE / name).read_text(encoding="utf-8")
            for link in HTML_LINK.findall(page):
                target = self.resolve(link, SITE)
                self.assertTrue(target.exists(), f"broken link {link!r} in site/{name}")

    def test_no_external_assets_or_scripts_in_site(self):
        for name in CHAPTERS:
            page = (SITE / name).read_text(encoding="utf-8")
            with self.subTest(page=name):
                self.assertNotIn("<script", page.lower(), "site must ship zero JavaScript")
                self.assertIsNone(EXTERNAL_URL.search(page),
                                  f"site/{name} references an external URL")
                self.assertNotIn('src="', page)  # no remote/local fetches either
                self.assertIn('rel="stylesheet" href="style.css">', page)

    def test_css_is_local_only(self):
        css = (SITE / "style.css").read_text(encoding="utf-8")
        self.assertIsNone(EXTERNAL_URL.search(css), "CSS must not import remote resources")


class HygieneTests(unittest.TestCase):
    """No secrets, no personal data, and the required stamped files exist."""

    def test_no_secrets_in_repo(self):
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(
                    part in {"__pycache__", ".git"} for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    offenders.append(f"{path.relative_to(ROOT)} matches {pattern.pattern!r}")
        self.assertEqual(offenders, [], "potential secrets found:\n" + "\n".join(offenders))

    def test_license_is_mit_with_exact_copyright(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", license_text)
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", license_text)

    def test_readme_credits_company_and_explains_usage(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)
        self.assertIn("python3 build.py", readme)
        self.assertIn("unittest discover", readme)

    def test_docs_cover_all_six_required_topics(self):
        self.assertTrue((DOCS / "01-choosing-apps.md").is_file())
        self.assertTrue((DOCS / "02-on-device-vs-cloud.md").is_file())
        self.assertTrue((DOCS / "03-voice-input.md").is_file())
        self.assertTrue((DOCS / "04-privacy-settings.md").is_file())
        self.assertTrue((DOCS / "05-battery-and-data.md").is_file())
        self.assertTrue((DOCS / "06-accessibility.md").is_file())

    def test_docs_have_self_tests_documented(self):
        # chapter content sanity: every chapter has a checkpoint and an H1 title
        for name in MD_CHAPTERS[1:]:
            text = (DOCS / name).read_text(encoding="utf-8")
            with self.subTest(chapter=name):
                self.assertTrue(text.startswith("# Chapter"), f"{name} missing H1")
                self.assertIn("## Checkpoint", text, f"{name} missing checkpoint")


if __name__ == "__main__":
    unittest.main()
