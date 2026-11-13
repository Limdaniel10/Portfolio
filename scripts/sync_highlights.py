#!/usr/bin/env python3
"""Refresh Notion highlight-to-book links from Google Sheets without touching Notion passages.

Source: HighlightCandidates, with explicit BookID values maintained by the owner.
Reading/books.json supplies the valid IDs and the browser chooses earliest rereads.
This script never fabricates dates or fetches copyrighted excerpts.
"""
from __future__ import annotations
import argparse,json,os,sys,tempfile
from pathlib import Path
if __package__:
    from .sync_reading import ROOT,DataError,authenticate,load_live_sheet
else:
    from sync_reading import ROOT,DataError,authenticate,load_live_sheet

HEADER=("HighlightID","Title","Author","QuoteCandidate","AdditionalPassages","NotionURL",
        "BookID","MatchStatus","ReviewStatus","Section","EntryNumber")

def merge_highlights(rows,payload,book_ids):
    if not rows or [str(x).strip() for x in rows[0]][:len(HEADER)]!=list(HEADER):
        raise DataError("HighlightCandidates header mismatch")
    entries=payload.get("entries",[])
    if len(entries)<337:
        raise DataError("Notion highlight source missing original entries")
    source={entry["id"]:entry for entry in entries}
    if len(source)!=len(entries):
        raise DataError("Duplicate IDs in Notion highlight source")
    result={}
    for index,row in enumerate(rows[1:],2):
        if not any(str(v).strip() for v in row):
            continue
        r={k:(str(row[i]).strip() if i<len(row) and row[i] is not None else "") for i,k in enumerate(HEADER)}
        ident=r["HighlightID"]
        if not ident or ident in result or ident not in source:
            raise DataError("HighlightCandidates row %d: unknown/duplicate ID"%index)
        b=r["BookID"]
        if b and b not in book_ids:
            raise DataError("HighlightCandidates row %d: unknown BookID %s"%(index,b))
        if not r["Title"] or not r["Author"]:
            raise DataError("HighlightCandidates row %d: missing book title/author"%index)
        entry=dict(source[ident])
        entry.update({"book_id":b,"title":r["Title"],"author":r["Author"],
                      "preview":r["QuoteCandidate"],"notion_url":r["NotionURL"],
                      "match_status":r["MatchStatus"]})
        # Original Notion passages belong to the saved snapshot, never a spreadsheet excerpt.
        result[ident]=entry
    if set(result)!=set(source):
        missing=set(source)-set(result)
        raise DataError("Refusing to lose Notion highlights: "+", ".join(sorted(missing)[:5]))
    return {**payload,"entries":[result[e["id"]] for e in entries]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--offline",action="store_true",help="Check committed snapshot when Sheets is not configured")
    args=p.parse_args(argv)
    target=ROOT/"reading/data/highlights.json"
    snapshot=json.loads(target.read_text(encoding="utf-8"))
    books=json.loads((ROOT/"reading/data/books.json").read_text(encoding="utf-8"))
    valid={b["id"] for b in books["books"]}
    if args.offline:
        if not snapshot.get("entries") or any(e["book_id"] and e["book_id"] not in valid for e in snapshot["entries"]):
            raise DataError("Offline Notion archive missing or has invalid book links")
        print("Notion Highlights offline snapshot: %d entries."%len(snapshot["entries"]))
        return
    sid=os.environ.get("GOOGLE_SHEETS_ID","")
    if not sid:raise DataError("GOOGLE_SHEETS_ID is required for live HighlightCandidates sync")
    records=load_live_sheet(sid,"HighlightCandidates",authenticate())
    merged=merge_highlights(records,snapshot,valid)
    output=json.dumps(merged,ensure_ascii=False,indent=2)+"\n"
    with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=target.parent,prefix=".highlight-sync-",delete=False) as f:
        path=Path(f.name)
        f.write(output)
    os.replace(path,target)
    print("Notion Highlights: %d entries; %d BookIDs linked."%(
          len(merged["entries"]),sum(bool(x["book_id"]) for x in merged["entries"])))

if __name__=="__main__":
    try:main()
    except (DataError,ValueError,FileNotFoundError,KeyError) as exc:
        print("HIGHLIGHT SYNC FAILED: "+str(exc),file=sys.stderr)
        sys.exit(1)
