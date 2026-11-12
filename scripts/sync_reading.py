#!/usr/bin/env python3
"""Validate Books + MonthlyPages, then atomically publish two static JSON files.

Live: GOOGLE_SERVICE_ACCOUNT_JSON=... GOOGLE_SHEETS_ID=... python scripts/sync_reading.py
Local: python scripts/sync_reading.py --from-csv
"""
from __future__ import annotations

import argparse
import calendar
import csv
import json
import os
import re
import sys
import tempfile
import time
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
HEADERS_BOOKS = ("BookID", "Title", "Author", "CompletedDate", "MonthOrder", "Status")
HEADERS_PAGES = ("Year", "Month", "PagesRead")
MONTH = re.compile(r"^(\d{4})-(\d{2})(?:-(\d{2}))?$")
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class DataError(ValueError):
    """Bad sheet data: do not overwrite the last successful public version."""


def parse_rows(lines, name):
    """Accept CSV (str rows) or Sheets values (list rows), preserve quoted commas."""
    if not lines:
        raise DataError(f"{name}: no rows returned; refusing to replace existing archive")
    header = [str(cell).strip().lstrip("\ufeff") for cell in lines[0]]
    expected = HEADERS_BOOKS if name == "Books" else HEADERS_PAGES
    if header[:len(expected)] != list(expected):
        raise DataError(f"{name}: expected headers {', '.join(expected)}, received {header}. Keep their order and spelling.")
    output = []
    for rownum, row in enumerate(lines[1:], start=2):
        if not any(str(v).strip() for v in row):
            continue
        record = {k: str(row[i]).strip() if i < len(row) and row[i] is not None else ""
                  for i, k in enumerate(expected)}
        output.append((rownum, record))
    if not output:
        raise DataError(f"{name}: no populated rows")
    return output


def month_from_completed_date(value, rownum):
    match = MONTH.fullmatch(value)
    if not match:
        raise DataError(f"Books row {rownum}: CompletedDate must be YYYY-MM or YYYY-MM-DD (got {value!r})")
    yr, mon = int(match.group(1)), int(match.group(2))
    day = int(match.group(3)) if match.group(3) else 1
    try:
        moment = date(yr, mon, day)
    except ValueError as exc:
        raise DataError(f"Books row {rownum}: invalid CompletedDate {value!r}") from exc
    if yr < 2000 or yr > date.today().year + 1:
        raise DataError(f"Books row {rownum}: implausible completion year {yr}")
    if match.group(3) and moment > date.today():
        raise DataError(f"Books row {rownum}: future completion date {value}")
    return yr, mon


def positive_int(raw, description, allow_zero=False):
    if not re.fullmatch(r"\d+", str(raw)):
        raise DataError(f"{description}: expected a whole nonnegative number, received {raw!r}")
    num = int(raw)
    if num < (0 if allow_zero else 1):
        raise DataError(f"{description}: value must be {'nonnegative' if allow_zero else 'positive'}")
    return num


def validate_books(lines):
    items, ids, slots, blank_order = [], set(), defaultdict(set), defaultdict(list)
    for rownum, r in parse_rows(lines, "Books"):
        ident, title, author, completed, order, status = (r[x] for x in HEADERS_BOOKS)
        if not ID_PATTERN.fullmatch(ident):
            raise DataError(f"Books row {rownum}: invalid/missing BookID {ident!r}; use e.g. BK-001413")
        if ident in ids:
            raise DataError(f"Books row {rownum}: duplicate BookID {ident!r}")
        ids.add(ident)
        if not title or not author:
            raise DataError(f"Books row {rownum}: Title and Author are both required")
        if status.lower() not in {"completed", "완독"}:
            raise DataError(f"Books row {rownum}: status must be Completed, not {status!r}; do not publish in-progress titles")
        year, month = month_from_completed_date(completed, rownum)
        index = positive_int(order, f"Books row {rownum} MonthOrder") if order else None
        key = year, month
        if index is not None:
            if index in slots[key]:
                raise DataError(f"Books row {rownum}: duplicate MonthOrder={index} in {year}-{month:02d}")
            slots[key].add(index)
        item = {"id": ident, "title": title, "author": author,
                "completed_date": completed, "year": year, "month": month,
                "month_order": index, "status": "Completed"}
        items.append(item)
        if index is None:
            blank_order[key].append(item)
    # For newly added books, MonthOrder can remain blank. They are appended to that month.
    for key, entries in blank_order.items():
        next_order = max(slots[key], default=0) + 1
        for entry in entries:
            entry["month_order"] = next_order
            next_order += 1
    items.sort(key=lambda b: (b["year"], b["month"], b["month_order"], b["id"]))
    return items


def validate_months(lines):
    result, seen = [], set()
    for rownum, r in parse_rows(lines, "MonthlyPages"):
        yr = positive_int(r["Year"], f"MonthlyPages row {rownum} Year")
        mon = positive_int(r["Month"], f"MonthlyPages row {rownum} Month")
        pages = positive_int(r["PagesRead"], f"MonthlyPages row {rownum} PagesRead", allow_zero=True)
        if yr < 2000 or yr > date.today().year + 1 or mon not in range(1, 13):
            raise DataError(f"MonthlyPages row {rownum}: invalid year/month {yr}/{mon}")
        if (yr, mon) in seen:
            raise DataError(f"MonthlyPages row {rownum}: duplicate Year/Month {yr}-{mon:02d}")
        seen.add((yr, mon))
        result.append({"year": yr, "month": mon, "pages_read": pages})
    return sorted(result, key=lambda m: (m["year"], m["month"]))


def read_csv_file(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def load_live_sheet(spreadsheet_id, name, auth_headers):
    import requests  # installed by requirements.txt for live sync only
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{quote(spreadsheet_id, safe='')}/values/{quote(name + '!A:Z', safe='')}"
    for attempt in range(4):
        try:
            response = requests.get(url, headers=auth_headers,
                                    params={"valueRenderOption": "FORMATTED_VALUE"}, timeout=30)
        except requests.RequestException as exc:
            if attempt == 3:
                raise DataError(f"Google Sheets {name} request failed after retries: {type(exc).__name__}") from exc
            time.sleep(2 ** attempt)
            continue
        if response.status_code in {429, 500, 502, 503, 504} and attempt < 3:
            time.sleep(2 ** attempt)
            continue
        if response.status_code != 200:
            raise DataError(f"Google Sheets {name} HTTP {response.status_code}. Check API enabled, service-account Viewer access, and GOOGLE_SHEETS_ID.")
        try:
            return response.json()["values"]
        except (ValueError, KeyError, TypeError) as exc:
            raise DataError(f"Google Sheets {name} returned invalid JSON or no values") from exc
    raise DataError(f"Google Sheets {name} unavailable")


def authenticate():
    try:
        import google.auth.transport.requests
        from google.oauth2 import service_account
    except ImportError as exc:
        raise DataError("Live mode requires pip install -r requirements.txt") from exc
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if not raw:
        raise DataError("Missing GitHub secret GOOGLE_SERVICE_ACCOUNT_JSON")
    try:
        creds = service_account.Credentials.from_service_account_info(
            json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
        creds.refresh(google.auth.transport.requests.Request())
    except Exception as exc:
        raise DataError(f"Google service-account authentication failed: {type(exc).__name__}; check the secret") from exc
    return {"Authorization": f"Bearer {creds.token}"}


def save_pair(out_dir, books, months, allow_deletions=False):
    out_dir.mkdir(parents=True, exist_ok=True)
    bookfile, pagefile = out_dir / "books.json", out_dir / "monthly-pages.json"
    if not allow_deletions:
        if bookfile.exists():
            old = json.loads(bookfile.read_text(encoding="utf-8"))
            previous = {r["id"] for r in old.get("books", [])}
            current = {r["id"] for r in books}
            removed = previous - current
            if removed:
                raise DataError(f"Refusing to remove {len(removed)} historical BookIDs: {', '.join(sorted(removed)[:5])}. Use --allow-deletions only for intentional corrections.")
        if pagefile.exists():
            old = json.loads(pagefile.read_text(encoding="utf-8"))
            previous_months = {(r["year"], r["month"]) for r in old.get("months", [])}
            current_months = {(r["year"], r["month"]) for r in months}
            if previous_months - current_months:
                raise DataError("Refusing to drop a previous Year/Month from MonthlyPages; restore the row or use --allow-deletions")
    payloads = [
        json.dumps({"schema_version": 1, "books": books}, ensure_ascii=False, indent=2) + "\n",
        json.dumps({"schema_version": 1, "months": months}, ensure_ascii=False, indent=2) + "\n",
    ]
    with tempfile.TemporaryDirectory(dir=out_dir, prefix=".reading-sync-") as tmp:
        for basename, text in zip(("books.json", "monthly-pages.json"), payloads):
            (Path(tmp) / basename).write_text(text, encoding="utf-8")
        # Both inputs are validated before either public output is updated.
        os.replace(Path(tmp) / "books.json", bookfile)
        os.replace(Path(tmp) / "monthly-pages.json", pagefile)
    return sum(m["pages_read"] for m in months)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-csv", action="store_true", help="Preview/rebuild JSON locally without Google credentials")
    parser.add_argument("--books-csv", type=Path, default=ROOT / "reading/sheets/Books.csv")
    parser.add_argument("--pages-csv", type=Path, default=ROOT / "reading/sheets/MonthlyPages.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reading/data")
    parser.add_argument("--spreadsheet-id", default=os.environ.get("GOOGLE_SHEETS_ID", ""))
    parser.add_argument("--allow-deletions", action="store_true", help="Dangerous: explicitly permit removing published records")
    args = parser.parse_args(argv)
    if args.from_csv:
        book_rows = read_csv_file(args.books_csv)
        month_rows = read_csv_file(args.pages_csv)
    else:
        if not args.spreadsheet_id:
            raise DataError("Missing GOOGLE_SHEETS_ID repository variable; use --from-csv for offline testing")
        headers = authenticate()
        book_rows = load_live_sheet(args.spreadsheet_id, "Books", headers)
        month_rows = load_live_sheet(args.spreadsheet_id, "MonthlyPages", headers)
    books = validate_books(book_rows)
    months = validate_months(month_rows)
    pages = save_pair(args.output_dir, books, months, args.allow_deletions)
    print(f"Validated: {len(books):,} completed books; {len(months)} monthly page records; {pages:,} pages. JSON ready.")


if __name__ == "__main__":
    try:
        main()
    except (DataError, FileNotFoundError, csv.Error) as error:
        print(f"SYNC FAILED (no deployment): {error}", file=sys.stderr)
        sys.exit(1)
