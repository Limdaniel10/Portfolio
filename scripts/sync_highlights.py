#!/usr/bin/env python3
"""Publish a Sheets-owned highlights archive without changing Books/MonthlyPages.

Manage Title, Author, HighlightText, BookID, ReviewStatus and source columns
in Google Sheets > HighlightCandidates. A selected BookID associates an existing
completed book; suggested IDs never link until explicitly approved.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
if __package__:
    from .sync_reading import ROOT,DataError,authenticate,load_live_sheet
else:
    from sync_reading import ROOT,DataError,authenticate,load_live_sheet

HEADER=("HighlightID","Title","Author","QuoteCandidate","AdditionalPassages",
        "NotionURL","BookID","MatchStatus","ReviewStatus","Section",
        "EntryNumber","HighlightText","SuggestedBookID","SuggestedBookTitle")
REVIEW_STATUSES={
 "Needs review","Approved","Rejected","Duplicate","Suggested match",
 "Completion unverified","Different book","Unfinished","Excerpt only",
 "Completed but missing"
}

def merge_highlights(rows,payload,book_ids):
    if not rows or [str(v).strip().lstrip("\ufeff") for v in rows[0]][:len(HEADER)]!=list(HEADER):
        raise DataError("HighlightCandidates header mismatch; do not rearrange named columns")
    original=payload.get("entries",[])
    original_ids={e["id"] for e in original}
    if len(original_ids)!=len(original):
        raise DataError("Duplicate HighlightID in committed highlights archive")
    items=[]
    seen=set()
    for rownum,row in enumerate(rows[1:],2):
        if not any(str(v).strip() for v in row):
            continue
        r={name:(str(row[i]).strip() if i<len(row) and row[i] is not None else "")
           for i,name in enumerate(HEADER)}
        ident=r["HighlightID"]
        if not ident or ident in seen:
            raise DataError("HighlightCandidates row %d: duplicate/blank HighlightID"%rownum)
        seen.add(ident)
        if not r["Title"] or not r["Author"] or not r["HighlightText"]:
            raise DataError("HighlightCandidates row %d: title/author/HighlightText required"%rownum)
        if r["BookID"] and r["BookID"] not in book_ids:
            raise DataError("HighlightCandidates row %d: unknown BookID %s"%(rownum,r["BookID"]))
        if r["SuggestedBookID"] and r["SuggestedBookID"] not in book_ids:
            raise DataError("HighlightCandidates row %d: invalid suggested BookID"%rownum)
        review=r["ReviewStatus"] or "Needs review"
        if review not in REVIEW_STATUSES:
            raise DataError("HighlightCandidates row %d: unexpected ReviewStatus %s"%(rownum,review))
        if review in ("Unfinished","Excerpt only") and r["BookID"]:
            raise DataError("HighlightCandidates row %d: Unfinished/excerpt must not have a completed BookID"%rownum)
        try:
            ordinal=int(r["EntryNumber"]) if r["EntryNumber"] else rownum-1
            if ordinal<1:raise ValueError()
        except ValueError as exc:
            raise DataError("HighlightCandidates row %d: invalid EntryNumber"%rownum) from exc
        items.append({
            "id":ident,"source":r["Section"] or "New","ordinal":ordinal,
            "title":r["Title"],"author":r["Author"],"preview":r["QuoteCandidate"],
            "text":r["HighlightText"],"book_id":r["BookID"],
            "match_status":r["MatchStatus"],"review_status":review,
            "suggested_book_id":r["SuggestedBookID"],
            "suggested_title":r["SuggestedBookTitle"]
        })
    if not original_ids.issubset(seen):
        raise DataError("HighlightCandidates lost previously published entries: %s"%
                        ", ".join(sorted(original_ids-seen)[:8]))
    if len(items)<337:
        raise DataError("HighlightCandidates returned fewer than 337 original entries")
    result={**payload,"schema_version":2,
            "description":"Google Sheets-owned highlight archive; completion months from Books.",
            "entries":items}
    result.pop("sources",None)
    return result

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--offline",action="store_true",
                   help="Validate checked-in snapshot when Google Sheets is unavailable")
    args=p.parse_args(argv)
    path=ROOT/"reading/data/highlights.json"
    payload=json.loads(path.read_text(encoding="utf-8"))
    book_data=json.loads((ROOT/"reading/data/books.json").read_text(encoding="utf-8"))
    known={b["id"] for b in book_data["books"]}
    if args.offline:
        entries=payload.get("entries",[])
        if len(entries)<337 or any(not e.get("text") or e.get("book_id") and e["book_id"] not in known for e in entries):
            raise DataError("Offline highlights archive incomplete or invalid")
        print("Google Sheets Highlights checked-in snapshot: %d entries."%len(entries))
        return
    sid=os.environ.get("GOOGLE_SHEETS_ID")
    if not sid:raise DataError("Missing GOOGLE_SHEETS_ID for live highlights sync")
    rows=load_live_sheet(sid,"HighlightCandidates",authenticate())
    result=merge_highlights(rows,payload,known)
    serialized=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=path.parent,
                                     prefix=".highlights-",delete=False) as f:
        temp=Path(f.name)
        f.write(serialized)
    os.replace(temp,path)
    print("Google Sheets Highlights: %d passages; %d completed-book links; %d unfinished/excerpt-only."%(
        len(result["entries"]),
        sum(bool(e["book_id"]) for e in result["entries"]),
        sum(e["review_status"] in ("Unfinished","Excerpt only") for e in result["entries"])
    ))

if __name__=="__main__":
    try:main()
    except (DataError,ValueError,FileNotFoundError,KeyError) as exc:
        print("HIGHLIGHTS SYNC FAILED: "+str(exc),file=sys.stderr)
        sys.exit(1)
