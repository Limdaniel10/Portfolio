#!/usr/bin/env python3
"""One-time, read-only check: can GitHub Actions access the author's Brunch posts?"""
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
HEADERS={
 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
 "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
 "Accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
 "Referer":"https://brunch.co.kr/",
}
def main():
 for n in range(1,14):
  source=ROOT/f"writing_source/content/collections/el-salvador/{n:03d}.md"
  data=source.read_text(encoding="utf8")
  match=re.search(r"^brunch_url:\s*(https://\S+)",data,re.M)
  if not match:
   print(f"{n:02d} MISSING_URL");continue
  url=match.group(1).strip()
  try:
   response=requests.get(url,timeout=18,headers=HEADERS)
   soup=BeautifulSoup(response.text,"html.parser")
   body=soup.select_one(".wrap_body")
   paragraphs=[p.get_text(" ",strip=True) for p in body.select("p")] if body else []
   content_len=sum(len(x) for x in paragraphs)
   print(f"{n:02d} status={response.status_code} body={'yes' if body else 'no'} paragraphs={len(paragraphs)} chars={content_len} final_path={response.url.split('/')[-1]} html_bytes={len(response.content)}")
  except Exception as exc:
   print(f"{n:02d} ERROR {type(exc).__name__}: {str(exc)[:120]}")
if __name__=="__main__":main()
