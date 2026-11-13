#!/usr/bin/env python3
"""Validate the seven-language localized Portfolio without changing source prose.

Run from repository root: python tests/test_i18n.py
"""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LANGS = ("en", "ko", "zh-Hans", "es", "zh-Hant", "fr", "de")

def catalog(filename: str, page: str) -> dict[str, list[str | None]]:
    path = ROOT / "js" / filename
    code = """
global.window = {};
require(process.argv[1]);
process.stdout.write(JSON.stringify(window.PortfolioDetailedTranslations));
"""
    result = subprocess.run(
        ["node", "-e", code, str(path)],
        check=True, capture_output=True, text=True, cwd=ROOT,
    )
    data = json.loads(result.stdout)
    assert page in data, f"{filename}: no catalog for {page}"
    return data[page]

for page in ("about", "career"):
    html_path = ROOT / page / "index.html"
    soup = BeautifulSoup(html_path.read_text(encoding="utf8"), "html.parser")
    html_scripts = [x.get("src", "") for x in soup.find_all("script") if x.get("src")]
    detail_script = f"../js/i18n-{page}.js"
    assert detail_script in html_scripts, f"{page}: detail translation bundle missing"
    assert "../js/i18n.js" in html_scripts, f"{page}: shared switcher missing"
    assert html_scripts.index(detail_script) < html_scripts.index("../js/i18n.js"), (
        f"{page}: detail bundle must precede shared switcher"
    )
    catalog_data = catalog(f"i18n-{page}.js", page)
    assert len(catalog_data) >= (35 if page == "about" else 60)
    for selector, translations in catalog_data.items():
        targets = soup.select(selector)
        assert len(targets) == 1, (
            f"{page}: selector must point to exactly one element: {selector!r} "
            f"(found {len(targets)})"
        )
        assert isinstance(translations, list) and len(translations) == len(LANGS), (
            f"{page}: {selector}: must have {len(LANGS)} language entries"
        )
        assert translations[0] is None, (
            f"{page}: source English should come from canonical HTML: {selector}"
        )
        original = targets[0]
        original_hrefs = [x.get("href") for x in original.find_all("a")]
        for lang, val in zip(LANGS[1:], translations[1:]):
            assert isinstance(val, str) and val.strip(), (
                f"{page}: blank translation for {lang}: {selector}"
            )
            frag = BeautifulSoup(val, "html.parser")
            assert [x.get("href") for x in frag.find_all("a")] == original_hrefs, (
                f"{page}: links changed in {lang}: {selector}"
            )
            if original.find("span") and selector.endswith(("summary", ".textlink", "h1")):
                assert frag.find("span"), (
                    f"{page}: visual label lost its span in {lang}: {selector}"
                )
    print(f"PASS {page}: {len(catalog_data)} independently translatable elements × "
          f"{len(LANGS)} languages; source links preserved")

shared = (ROOT / "js" / "i18n.js").read_text(encoding="utf8")
for code in LANGS:
    assert f'"{code}"' in shared, f"Missing language {code}"
assert "window.PortfolioDetailedTranslations" in shared, "No detailed locale integration"
print(f"PASS: all {len(LANGS)} language codes in shared switcher")
