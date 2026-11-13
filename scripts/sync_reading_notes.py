#!/usr/bin/env python3
"""Publish public ReadingNotes from Google Sheets without changing Books/MonthlyPages."""
from __future__ import annotations
import argparse,csv,json,os,sys,tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
if __package__:
    from .sync_reading import ROOT,DataError,authenticate,load_live_sheet
else:
    from sync_reading import ROOT,DataError,authenticate,load_live_sheet

HEADERS=("NoteID","BookID","Title","Author","PublishedDate","Reflection","SelectedQuote","BrunchURL","QuoteSourceURL","Verification","ShowOnSite","MonthGroup")

def validate_notes(rows):
    if not rows:
        raise DataError("ReadingNotes: missing header")
    header=[str(x).strip() for x in rows[0]]
    if header[:len(HEADERS)]!=list(HEADERS):
        raise DataError("ReadingNotes: incorrect header order")
    seen=set()
    output=[]
    for rownum,row in enumerate(rows[1:],2):
        if not any(str(v).strip() for v in row):
            continue
        r={name:(str(row[i]).strip() if i<len(row) and row[i] is not None else "") for i,name in enumerate(HEADERS)}
        if not r["NoteID"] or r["NoteID"] in seen:
            raise DataError("ReadingNotes row %d: missing/duplicate NoteID"%rownum)
        seen.add(r["NoteID"])
        show=r["ShowOnSite"].upper()
        if show not in ("TRUE","FALSE","YES","NO","1","0",""):
            raise DataError("ReadingNotes row %d: invalid ShowOnSite"%rownum)
        if show not in ("TRUE","YES","1"):
            continue
        if not r["Title"] or not r["Author"] or not r["Reflection"]:
            raise DataError("ReadingNotes row %d: incomplete public reflection"%rownum)
        try:
            day=date.fromisoformat(r["PublishedDate"])
        except ValueError as exc:
            raise DataError("ReadingNotes row %d: invalid date"%rownum) from exc
        if not (2000<=day.year<=date.today().year+1):
            raise DataError("ReadingNotes row %d: date out of range"%rownum)
        url=r["BrunchURL"]
        parsed=urlparse(url)
        if parsed.scheme!="https" or parsed.hostname!="brunch.co.kr" or not parsed.path:
            raise DataError("ReadingNotes row %d: invalid Brunch URL"%rownum)
        output.append({
          "id":r["NoteID"],"book_id":r["BookID"],"title":r["Title"],"author":r["Author"],
          "date":r["PublishedDate"],"reflection":r["Reflection"],
          "quote":r["SelectedQuote"] if r["Verification"]=="Quote approved" else "",
          "brunch_url":url,"quote_source":r["QuoteSourceURL"],"verification":r["Verification"]
        })
    output.sort(key=lambda n:(n["date"],n["id"]),reverse=True)
    return output

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-csv",action="store_true")
    parser.add_argument("--csv",type=Path,default=ROOT/"reading/sheets/ReadingNotes.csv")
    parser.add_argument("--output",type=Path,default=ROOT/"reading/data/notes.json")
    args=parser.parse_args()
    if args.from_csv:
        with args.csv.open(encoding="utf-8-sig",newline="") as stream:
            rows=list(csv.reader(stream))
    else:
        sid=os.environ.get("GOOGLE_SHEETS_ID","")
        if not sid:
            raise DataError("Missing GOOGLE_SHEETS_ID")
        rows=load_live_sheet(sid,"ReadingNotes",authenticate())
    notes=validate_notes(rows)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    payload=json.dumps({"schema_version":1,"source":"ReadingNotes","notes":notes},ensure_ascii=False,indent=2)+"\n"
    with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=args.output.parent,prefix=".reading-notes-",delete=False) as stream:
        temp=Path(stream.name)
        stream.write(payload)
    os.replace(temp,args.output)
    print("Reading Notes: %d public reflections; unapproved quotes hidden."%len(notes))

if __name__=="__main__":
    try:main()
    except (DataError,FileNotFoundError,csv.Error) as exc:
        print("NOTES SYNC FAILED: "+str(exc),file=sys.stderr)
        sys.exit(1)
