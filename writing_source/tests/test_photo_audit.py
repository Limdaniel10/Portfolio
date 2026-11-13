#!/usr/bin/env python3
"""Guard the Brunch-photo-verified Writing / Readings dataset during deployment.

The Writing archive is curated from original Brunch photo slides and must not
be replaced by the older Google Sheets ReadingNotes export.
"""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "writing_source/assets/reading-notes.json"
notes = json.loads(DATA.read_text(encoding="utf-8"))["notes"]

assert len(notes) >= 182, f"Writing photo archive unexpectedly shrank: {len(notes)}"
assert len({x["id"] for x in notes}) == len(notes), "Duplicate Writing note IDs"
assert len({x["brunch_url"] for x in notes}) == len(notes), "Duplicate Brunch URLs"
assert all(x["title"] and x["author"] and x["brunch_url"] for x in notes)
assert all(date.fromisoformat(x["date"]) for x in notes)
verified_quotes = [x for x in notes if x.get("photo_quote_verified")]
verified_dates = [x for x in notes if x.get("photo_date_verified")]
assert len(verified_quotes) >= 182, "Photo-verified Writing quotes were lost"
assert len(verified_dates) >= 180, "Photo-verified Writing dates were lost"
assert all(x["quote"] and x.get("quote_source") == x["brunch_url"] for x in verified_quotes)
assert all(x.get("date_source", "").startswith("Brunch image:") for x in verified_dates)
assert {x["id"] for x in notes if x.get("content_status") == "intentionally_no_reflection"} >= {
    "BR-000473", "BR-000472", "BR-000436"
}
# Separate full-photo transcription from the earlier excerpt/photo-presence audit.
full_korean = [x for x in notes if x.get("photo_korean_full_verified")]
full_bilingual = [x for x in notes if x.get("photo_full_transcription_verified")]
translated = [x for x in notes if str(x.get("quote_en", "")).strip()]
assert len(full_korean) == len(notes), "A Korean photo quotation lacks full transcription"
assert len(translated) >= len(notes) - 1, "More than one English photo is missing"
assert len(full_bilingual) >= len(notes) - 3, "Photo transcription/source concordance regressed"
assert all(x.get("quote") and not x.get("photo_quote_excerpt") for x in full_korean)
assert all(x.get("quote_en") and x.get("photo_korean_full_verified") for x in full_bilingual)
known_exceptions = {x["brunch_url"].rsplit("/", 1)[-1] for x in notes
                    if not x.get("photo_full_transcription_verified")}
assert known_exceptions <= {"309", "391", "481"}, (
    f"Unexpected unresolved photo sources: {sorted(known_exceptions)}"
)
print(f"PASS: {len(full_korean)} complete Korean quotes, "
      f"{len(translated)} English quotes, {len(full_bilingual)} bilingual matches")

print(
    f"PASS: {len(notes)} Writing entries; {len(verified_quotes)} photo quotes, "
    f"{len(verified_dates)} photo dates; no duplicate IDs or URLs."
)
