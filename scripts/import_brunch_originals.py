#!/usr/bin/env python3
"""Import the portfolio owner's 13 original Brunch essays into their Markdown archive.

Conservative one-time importer: never overwrite an existing nonempty manuscript;
verify all articles before changing any files; keep all original frontmatter.
"""
from pathlib import Path
import re, html, sys
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/"writing_source/content/collections/el-salvador"
HEADERS={
 "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
 "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
 "Accept-Language":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
 "Referer":"https://brunch.co.kr/"
}

def extract_article(markup: str, chapter: int) -> str:
 soup=BeautifulSoup(markup,"html.parser")
 body=soup.select_one("div.wrap_body")
 if body is None: raise ValueError(f"chapter {chapter:02d}: body container missing")
 for tag in body.select("script, style, iframe, button"):
  tag.decompose()
 for br in body.find_all("br"):
  br.replace_with("\n")
 paragraphs=[]
 for block in body.find_all(["p","h2","h3"]):
  # Notion-like export paragraphs; preserve adjacent Korean inline spans exactly.
  s=html.unescape(block.get_text("",strip=False))
  s=s.replace("\xa0"," ").replace("\ufeff","").replace("\u200b","").replace("\r","").strip()
  s="\n".join(x.strip() for x in s.split("\n") if x.strip())
  if not s or s=="\\" or re.fullmatch(r"(?:---+|___+|\*[\s*]{2,})",s):continue
  if block.name in ("h2","h3"):s="## "+s
  elif block.find_parent("blockquote"):s="\n".join("> "+x for x in s.splitlines())
  # Dates beginning with a numeric year must not become Markdown numbered lists.
  s=re.sub(r"^(20\d{2}|\d{2})\.(?=\s+\d{1,2}\.\s*\d{1,2})",lambda m:m.group(1)+"\\.",s)
  paragraphs.append(s)
 result="\n\n".join(paragraphs).strip()+"\n"
 if len(result)<650 or len(paragraphs)<10:
  raise ValueError(f"chapter {chapter:02d}: suspiciously incomplete content: {len(result)} chars/{len(paragraphs)} blocks")
 return result

def main():
 gathered=[]
 for n in range(1,14):
  path=FOLDER/f"{n:03d}.md"
  original=path.read_text(encoding="utf8")
  match=re.fullmatch(r"(---\n[\s\S]*?\n---\n)([\s\S]*)",original)
  if match is None:raise ValueError(f"{path}: missing frontmatter")
  front,previous=match.groups()
  if previous.strip():
   print(f"SKIP {n:02d}: manuscript already has text; never overwrite")
   continue
  urlmatch=re.search(r"^brunch_url:\s*(https://brunch\.co\.kr/@lim-eat-less/(\d+))\s*$",front,re.M)
  if urlmatch is None:raise ValueError(f"{path}: Brunch original URL missing or untrusted")
  url,article_id=urlmatch.groups()
  response=requests.get(url,timeout=28,headers=HEADERS)
  response.raise_for_status()
  if response.url.rstrip("/").split("/")[-1]!=article_id:
   raise ValueError(f"{path}: unexpected article redirect: {response.url}")
  body=extract_article(response.text,n)
  front=front.replace("status: missing\n","status: text\n")
  front=front.replace("source_note: null\n","source_note: Author original text imported from Brunch\n")
  if "status: text\n" not in front:raise ValueError("Cannot set status")
  gathered.append((path,front+body))
  print(f"READ {n:02d}: {len(body)} characters, original {url}",flush=True)
 if len(gathered)!=13:
  raise ValueError(f"Expected all 13 original manuscripts; only {len(gathered)} available. No files replaced.")
 for path,content in gathered:
  path.write_text(content,encoding="utf8")
 print(f"COMPLETE: imported {len(gathered)} verified authored manuscripts as Markdown.",flush=True)

if __name__=="__main__":
 try:main()
 except Exception as exc:
  print(f"IMPORT FAILED: {exc}",file=sys.stderr)
  raise
