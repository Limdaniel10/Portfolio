#!/usr/bin/env python3
"""One-time, bounded public Brunch magazine index for the owner's reading archive.
Only articles visibly marked as part of '100일 하루 한 줄' are retained.
Images are not downloaded. No private cookies or credentials are used.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import html,json,re,requests,sys,time

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"reading/data/brunch-index.json"
MAGAZINE="100일 하루 한 줄"
HEADERS={
 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
 "Accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
 "Referer":"https://brunch.co.kr/"
}

def clean(value):
    return " ".join(html.unescape(value or "").replace("\xa0"," ").split()).strip()

def first_tag(soup,selectors):
    for query in selectors:
        x=soup.select_one(query)
        if x:
            txt=clean(x.get_text(" ",strip=True))
            if txt:
                return txt
    return ""

def page(n):
    url="https://brunch.co.kr/@lim-eat-less/"+str(n)
    try:
        r=requests.get(url,headers=HEADERS,timeout=18,allow_redirects=True)
        if r.status_code!=200:
            return {"id":n,"error":"HTTP "+str(r.status_code)}
        soup=BeautifulSoup(r.text,"html.parser")
        visible=clean(soup.get_text(" ",strip=True))
        present=MAGAZINE in visible or MAGAZINE in r.text
        if not present:
            return {"id":n,"skip":"not magazine"}
        title=first_tag(soup,["h1.cover_title",".cover_title",".tit_cover","h1"])
        if not title:
            og=soup.select_one('meta[property="og:title"]')
            title=clean(og.get("content","")) if og else ""
        author=first_tag(soup,[".cover_sub_title",".cover_subtitle",".sub_title",".cover_sub"])
        date_raw=first_tag(soup,[".cover_date",".date",".wrap_cover .date","time"])
        if not date_raw:
            meta=soup.select_one('meta[property="article:published_time"]')
            date_raw=meta.get("content","") if meta else ""
        iso=""
        for fmt in ("%Y-%m-%d","%Y-%m-%dT%H:%M:%S","%b %d. %Y","%b %d, %Y","%Y. %m. %d.","%Y. %m. %d"):
            try:
                iso=datetime.strptime(date_raw.strip().split("+")[0],fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                pass
        if not iso:
            match=re.search(r"\b(2025)[.\-/]\s*(\d{1,2})[.\-/]\s*(\d{1,2})",r.text)
            if match:
                iso=match.group(1)+"-"+match.group(2).zfill(2)+"-"+match.group(3).zfill(2)
        body=soup.select_one("div.wrap_body") or soup.select_one("article")
        reflection=""
        if body:
            for tag in body.select("script,style,iframe,button"):
                tag.decompose()
            paragraphs=[clean(el.get_text(" ",strip=True)) for el in body.select("p,h2,h3,blockquote")]
            paragraphs=[p for p in paragraphs if p and len(p)>1]
            reflection="\n\n".join(paragraphs)
        # Do not collect unrelated navigation or comments if article body is absent.
        return {"id":n,"title":title,"author":author,"date":iso,"reflection":reflection[:12000],
                "url":url,"has_body":bool(reflection),"date_raw":date_raw[:80]}
    except requests.RequestException as exc:
        return {"id":n,"error":type(exc).__name__}

def main():
    IDs=range(225,511)  # Covers the 2025 public-book-reflection magazine period.
    found=[];misses={};samples={}
    with ThreadPoolExecutor(max_workers=4) as executor:
        jobs={executor.submit(page,n):n for n in IDs}
        for future in as_completed(jobs):
            r=future.result()
            n=r["id"]
            if n in (260,307,404,406,469):
                samples[str(n)]={k:v for k,v in r.items() if k not in ("reflection",)}
                samples[str(n)]["reflection_chars"]=len(r.get("reflection",""))
            if "url" in r:
                found.append(r)
            else:
                key=r.get("error",r.get("skip","other"))
                misses[key]=misses.get(key,0)+1
    found.sort(key=lambda x:x["id"])
    print("Magazine scan: %d candidates among %d public article IDs; statuses=%s"%(len(found),len(IDs),json.dumps(misses,ensure_ascii=False)),flush=True)
    print("Known-post diagnostics: "+json.dumps(samples,ensure_ascii=False),flush=True)
    if len(found)<20:
        raise SystemExit("Too few magazine matches; refuse to publish a misleading index.")
    TARGET.parent.mkdir(parents=True,exist_ok=True)
    TARGET.write_text(json.dumps({"schema_version":1,"magazine":MAGAZINE,"scan_range":[225,510],
                                  "candidate_count":len(found),"articles":found},
                                  ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Saved "+str(TARGET.relative_to(ROOT)),flush=True)

if __name__=="__main__":
    main()
