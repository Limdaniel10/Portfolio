#!/usr/bin/env python3
"""Import the author's own published Brunch articles as clean Markdown.

Only imports pages verified to belong to @lim-eat-less.
Never replaces an existing chapter containing text unless --force is passed.
Missing/unpublished sources are reported and never fabricated.
"""
from __future__ import annotations

import argparse
import json
import datetime as dt
import html
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "brunch_import.yml"
CONTENT = ROOT / "content" / "collections"
AUTHOR = "lim-eat-less"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.7",
}
ARTICLE_URL = re.compile(r"/@(?:lim-eat-less|@eQZr)/(\d+)(?:[/?#]|$)", re.I)
DATE_HEADING = re.compile(r"^(\s*)(20\d{2})\s*\\?\.\s*(\d{1,2})\s*\\?\.\s*(\d{1,2})(\s*:\s*.*)$")


def clean_text(text: str) -> str:
    text = html.unescape(text).replace("\u200b", "").replace("\ufeff", "").replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if re.fullmatch(r"(?:\*\s*){3,}|-{3,}|_{3,}|~{3,}", line):
            continue
        # Remove formatting (not the author's words): <s>, ~~text~~ and escaped punctuation.
        line = re.sub(r"</?(?:s|del|strike)>", "", line, flags=re.I)
        line = re.sub(r"~~(.+?)~~", r"\1", line)
        line = re.sub(r"(?<!\\)\\([*_\[\]#~])", r"\1", line)
        line = line.replace(r"\.", ".")
        match = DATE_HEADING.match(line)
        if match:
            pre, year, month, day, rest = match.groups()
            try:
                dt.date(int(year), int(month), int(day))
                rest = re.sub(r"\bdY\b", "Day", rest)
                line = f"{pre}{year}. {int(month):02d}. {int(day):02d}{rest}"
            except ValueError:
                pass
        lines.append(line)
    cleaned = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip() + "\n"


def fetch(session: requests.Session, url: str) -> BeautifulSoup:
    response = session.get(url, timeout=25, headers=HEADERS)
    response.raise_for_status()
    if "brunch.co.kr" not in urlparse(response.url).netloc:
        raise ValueError(f"Unexpected redirect: {response.url}")
    soup = BeautifulSoup(response.text, "html.parser")
    if soup.select_one("body") is None:
        raise ValueError(f"No HTML body returned for {url}")
    return soup


def book_links(soup: BeautifulSoup, limit: int) -> list[tuple[str, str]]:
    """Find the author's article links in their book's published chapter list."""
    found = []
    seen = set()
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        if not ARTICLE_URL.search(href):
            continue
        link = urljoin("https://brunch.co.kr", href)
        if link in seen:
            continue
        # Every chapter link is to one of this same author's article IDs.
        seen.add(link)
        label = a.get_text(" ", strip=True)
        found.append((link, label))
        if len(found) >= max(limit, 25):
            break
    return found


def get_source_title(soup: BeautifulSoup) -> str:
    for css in ("h1.cover_title", ".cover_title", "h1.tit_cover", "h1"):
        node = soup.select_one(css)
        if node:
            value = node.get_text(" ", strip=True)
            if value and len(value) > 1:
                return re.sub(r"^\d{1,2}화\s*", "", value).strip()
    tag = soup.select_one('meta[property="og:title"]')
    return tag.get("content", "").strip() if tag else ""


def get_published_date(soup: BeautifulSoup) -> str | None:
    for key, value in (("property", "article:published_time"), ("name", "date"), ("itemprop", "datePublished")):
        tag = soup.select_one(f'meta[{key}="{value}"]')
        if tag and tag.get("content"):
            candidate = tag["content"][:10]
            try:
                dt.date.fromisoformat(candidate)
                return candidate
            except ValueError:
                pass
    tag = soup.select_one("time[datetime]")
    if tag:
        try:
            return dt.date.fromisoformat(tag["datetime"][:10]).isoformat()
        except (KeyError, ValueError):
            pass
    return None


def extract_article(soup: BeautifulSoup, url: str) -> str:
    selectors = (
        "#wrapArticle .wrap_body",
        "div.wrap_body",
        ".item_view article",
        "article.wrap_view",
    )
    content = next((soup.select_one(sel) for sel in selectors if soup.select_one(sel)), None)
    if content is None:
        raise ValueError(f"Brunch article body unavailable: {url}")
    for node in content.select("script,style,button,iframe,nav,footer,hr,figure,img,video,svg"):
        node.decompose()
    paragraphs = []
    for node in content.select("p,h2,h3,h4,blockquote"):
        if node.find_parent(["p", "blockquote"]) is not None:
            continue
        line = node.get_text(" ", strip=True)
        if line and not re.fullmatch(r"Image(?:\s*:\s*.*)?", line, flags=re.I):
            paragraphs.append(line)
    if not paragraphs:
        raise ValueError(f"No article paragraphs found: {url}")
    body = clean_text("\n\n".join(paragraphs))
    if len(re.sub(r"\s", "", body)) < 120:
        raise ValueError(f"Article too short for safe import ({len(body)} chars): {url}")
    return body


def discover_book_urls(session: requests.Session, targets: dict) -> dict[str, str]:
    """Use verified links on the author's own profile, never guess slugs."""
    discovered = {}
    try:
        page = fetch(session, f"https://brunch.co.kr/@{AUTHOR}")
        candidate_urls = []
        for a in page.select('a[href*="/brunchbook/"]'):
            href = a.get("href", "")
            url = urljoin("https://brunch.co.kr", href)
            if url not in candidate_urls:
                candidate_urls.append(url)
        for url in candidate_urls[:45]:
            try:
                book = fetch(session, url)
                tag = book.select_one('meta[property="og:title"]')
                title = ((tag.get("content", "") if tag else "") + " " + " ".join(h.get_text(" ", strip=True) for h in book.select("h1,h2")[:5]))
                for book_id, record in targets.items():
                    if book_id in discovered or record.get("book_url"):
                        continue
                    if any(alias in title for alias in record.get("aliases", [])):
                        discovered[book_id] = url
                        print(f"DISCOVERED {book_id}: {url}")
            except (requests.RequestException, ValueError):
                continue
    except (requests.RequestException, ValueError) as exc:
        print(f"Profile discovery unavailable: {exc}")
    return discovered


def parse_existing(path: Path) -> tuple[dict, str]:
    if not path.exists():
        return {}, ""
    source = path.read_text(encoding="utf-8-sig")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", source, flags=re.S)
    if not match:
        raise ValueError(f"Existing Markdown lacks front matter: {path}")
    return (yaml.safe_load(match[1]) or {}), match[2]


def write_chapter(book_id: str, number: int, title: str, date: str | None,
                  url: str, text: str, force: bool) -> str:
    path = CONTENT / book_id / f"{number:03d}.md"
    old_meta, old_body = parse_existing(path)
    if old_body.strip() and not force:
        return "SKIP_EXISTING"
    # Protect unpublished entries, including their manual metadata, from being replaced.
    meta = {
        "title": title or old_meta.get("title") or f"제{number}화",
        "collection_id": book_id,
        "chapter": number,
        "date": date or old_meta.get("date"),
        "category": "collections",
        "special": False,
        "status": "text",
        "brunch_url": url,
        "notion_source": old_meta.get("notion_source"),
        "source_note": "Author original text imported from Brunch; images omitted",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000) + "---\n" + text
    path.write_text(doc, encoding="utf-8")
    return "IMPORTED"


def inspect_supplied_links(session: requests.Session, urls: list[str]) -> list[dict]:
    """Fetch source metadata for user-supplied articles before assigning chapters."""
    unique = list(dict.fromkeys(urls))
    rows = []
    for url in unique:
        row = {"url": url}
        try:
            soup = fetch(session, url)
            row["title"] = get_source_title(soup)
            row["published_date"] = get_published_date(soup)
            row["og_title"] = (soup.select_one('meta[property="og:title"]') or {}).get("content")
            row["author"] = (soup.select_one('meta[property="article:author"]') or {}).get("content")
            row["brunchbooks"] = [
                {"title": a.get_text(" ", strip=True)[:160], "href": urljoin("https://brunch.co.kr", a.get("href", ""))}
                for a in soup.select('a[href*="/brunchbook/"]')[:12]
            ]
            row["headings"] = [a.get_text(" ", strip=True) for a in soup.select("h1,h2,h3")[:12]]
            row["same_author_article_links"] = list({
                urljoin("https://brunch.co.kr", a.get("href", "")): a.get_text(" ", strip=True)[:100]
                for a in soup.select("a[href]")
                if ARTICLE_URL.search(urlparse(urljoin("https://brunch.co.kr", a.get("href", ""))).path)
            }.items())[:80]
            try:
                body = extract_article(soup, url)
                row["body_chars"] = len(body)
                row["opening"] = body[:350]
                row["backslashes"] = body.count(chr(92))
                row["date_lines"] = [line for line in body.splitlines()
                    if re.match(r"^20[0-9]{2}[.] [0-9]{2}[.] [0-9]{2}", line)][:6]
            except ValueError as exc:
                row["body_error"] = str(exc)
        except (requests.RequestException, ValueError) as exc:
            row["error"] = str(exc)
        rows.append(row)
        time.sleep(0.3)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Replace authored text; default preserves existing prose")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--book", action="append", help="Only these collection IDs")
    args = parser.parse_args()
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    books = manifest["collections"]
    if args.book:
        books = {key: val for key, val in books.items() if key in args.book}
    session = requests.Session()
    discovered = discover_book_urls(session, books)
    report = []
    discovery_report = {}
    for book_id, data in books.items():
        book_url = data.get("book_url") or discovered.get(book_id)
        known = data.get("chapters") or []
        published = []
        source_debug = None
        if book_url:
            try:
                book_page = fetch(session, book_url)
                published = book_links(book_page, data["count"])
                if book_id == "arctic":
                    source = str(book_page)
                    marker = "북극으로 가는 길"
                    position = source.find(marker)
                    source_debug = {
                        "marker_position": position,
                        "page_length": len(source),
                    }
            except (requests.RequestException, ValueError) as exc:
                print(f"BOOK_UNAVAILABLE {book_id}: {exc}")
        article_neighbors = []
        if book_id == "arctic":
            try:
                previous_article = fetch(session, "https://brunch.co.kr/@lim-eat-less/506")
                article_neighbors = [
                    {"url": urljoin("https://brunch.co.kr", a.get("href", "")), "text": a.get_text(" ", strip=True)[:160],
                     "title": a.get("title","")}
                    for a in previous_article.select("a[href]")
                    if ARTICLE_URL.search(a.get("href", ""))
                ]
                if len(known) >= 7 and not known[6].get("url"):
                    matches = [n for n in article_neighbors if "북극으로 가는 길" in (n["text"] + n["title"])]
                    if len(matches) == 1:
                        known[6]["url"] = matches[0]["url"]
                        print(f"FOUND_ARCTIC_EPISODE_7 {matches[0]['url']}")
            except (requests.RequestException, ValueError) as exc:
                print(f"ARTICLE_NEIGHBOR_UNAVAILABLE {exc}")
        discovery_report[book_id] = {"book_url": book_url, "published_links": [{"url": u, "label": label} for u, label in published], "debug": source_debug, "article_neighbors": article_neighbors}
        for no in range(1, data["count"] + 1):
            entry = next((c for c in known if c["chapter"] == no), {})
            title = entry.get("title", "")
            published_date = entry.get("date")
            article_url = entry.get("url")
            if not article_url and published:
                # Match chapter labels, when possible, before relying on sequential order.
                matched = next((u for u, label in published if title and title in label), None)
                article_url = matched or (published[no - 1][0] if no <= len(published) else None)
            if not article_url:
                report.append(f"NO_SOURCE {book_id}/{no:03d}")
                continue
            if not ARTICLE_URL.search(urlparse(article_url).path):
                report.append(f"BAD_URL {book_id}/{no:03d} {article_url}")
                continue
            path = CONTENT / book_id / f"{no:03d}.md"
            _, existing_body = parse_existing(path)
            if existing_body.strip() and not args.force:
                report.append(f"SKIP_EXISTING {book_id}/{no:03d}")
                continue
            try:
                article = fetch(session, article_url)
                body = extract_article(article, article_url)
                actual_title = get_source_title(article)
                actual_date = get_published_date(article) or published_date
                if title and actual_title and title not in actual_title and actual_title not in title:
                    raise ValueError(f"Title mismatch: expected {title}, got {actual_title}")
                if args.dry_run:
                    outcome = "DRY_RUN"
                else:
                    outcome = write_chapter(book_id, no, title or actual_title, actual_date,
                                            article_url, body, args.force)
                report.append(f"{outcome} {book_id}/{no:03d} {len(body)} chars")
                time.sleep(0.8)
            except (requests.RequestException, ValueError) as exc:
                report.append(f"UNAVAILABLE {book_id}/{no:03d}: {exc}")
    discovery_report["supplied_url_audit"] = inspect_supplied_links(session, manifest.get("supplied_urls", []))
    discovery_report["results"] = report
    (ROOT / "BRUNCH_DISCOVERY.json").write_text(json.dumps(discovery_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n".join(report))
    print(f"Total importable: {sum(x.startswith(('IMPORTED','DRY_RUN')) for x in report)}; "
          f"unavailable: {sum(x.startswith(('NO_SOURCE','BAD_URL','UNAVAILABLE')) for x in report)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
