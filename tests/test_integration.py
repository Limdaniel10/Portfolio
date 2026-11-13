#!/usr/bin/env python3
"""Run after build_site.py to catch broken Pages paths and data regression."""
from __future__ import annotations
import csv,json,re,sys
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
assert (SITE/'index.html').exists(),'Missing homepage'
expected=('about','career','traveling','writing','reading')
for section in expected:assert (SITE/section/'index.html').exists(),f'Missing /{section}/ index'
assert (SITE/'assets/resume.pdf').stat().st_size>10000,'Missing resume'
assert (SITE/'.nojekyll').exists()
assert (SITE/'data/visited-world.svg').stat().st_size>1000
travel=json.loads((SITE/'traveling/assets/data.js').read_text(encoding='utf8').strip().split('=',1)[1].rstrip(';'))
assert sum(bool(c['count_in_195']) for c in travel['countries'])==json.loads((SITE/'data/countries.json').read_text())['totalCountries']
assert len(travel['places'])>=282 and len(travel['domestic_places'])>=69
assert len(travel['airport_overnights'])>=45
books=json.loads((SITE/'reading/data/books.json').read_text())['books']
months=json.loads((SITE/'reading/data/monthly-pages.json').read_text())['months']
assert len(books)>=1400 and len(months)>=84
assert 'reading-notes-section' not in (SITE/'reading/index.html').read_text(encoding='utf8')
assert 'id="reading-highlights"' in (SITE/'reading/index.html').read_text(encoding='utf8')
highlight_data=json.loads((SITE/'reading/data/highlights.json').read_text(encoding='utf8'))['entries']
assert len(highlight_data)==337 and len({e['id'] for e in highlight_data})==337
assert {s:sum(e['source']==s for e in highlight_data) for s in ('I','II','III','IV')}=={'I':100,'II':100,'III':100,'IV':37}
assert sum(bool(e['book_id']) for e in highlight_data)==270
assert all(e['title'] and e['notion_url'].startswith('https://app.notion.com/') for e in highlight_data)
assert {e['book_id'] for e in highlight_data if e['book_id']} <= {b['id'] for b in books}

assert 'id="wr-archive"' in (SITE/'writing/readings/index.html').read_text(encoding='utf8')
assert len(json.loads((SITE/'writing/assets/reading-notes.json').read_text(encoding='utf8'))['notes'])==182

writing=json.loads((SITE/'writing/writing-index.json').read_text())
# Compare against the live Markdown source, not hardcoded chapter/essay totals.
# New chapters, essays, readings and fiction must deploy without editing tests.
content=ROOT/'writing_source/content'
source_chapters=list((content/'collections').rglob('*.md'))+list((content/'fiction').rglob('*.md'))
source_essays=list((content/'essays').rglob('*.md'))
source_readings=list((content/'readings').rglob('*.md'))
assert sum(len(c['chapters']) for c in writing['collections'])==len(source_chapters),'Writing: indexed chapter count does not match Markdown files'
assert len(writing['essays'])==len(source_essays),'Writing: indexed essays do not match Markdown files'
assert len(writing['readings'])==len(source_readings),'Writing: indexed readings do not match Markdown files'
failures=[];checked=0
for html in SITE.rglob('index.html'):
 soup=BeautifulSoup(html.read_text(encoding='utf8'),'html.parser')
 for tag in soup.select('a[href],link[href],script[src],img[src]'):
  raw=tag.get('href') or tag.get('src') or ''
  if not raw or raw.startswith(('#','mailto:','tel:','data:','https://','http://')):continue
  path=urlsplit(raw).path
  if not path:continue
  if path.startswith('/Portfolio/'):
   target=SITE/unquote(path[len('/Portfolio/'):])
  elif path.startswith('/'):
   failures.append(f'{html.relative_to(SITE)} : absolute non-Portfolio link {path}')
   continue
  else:target=html.parent/unquote(path)
  if target.is_dir():target/='index.html'
  checked+=1
  if not target.exists():failures.append(f'{html.relative_to(SITE)} : {raw} not found')
  if len(failures)>100:break
 if len(failures)>100:break
if failures:
 print('BROKEN LINKS (first 100):',*failures[:100],sep='\n  ')
 sys.exit(1)
print(f'PASS: home + five sections, {len(list(SITE.rglob("index.html")))} HTML pages, {checked} checked local links, {len(books)} books, {len(source_chapters)} Writing chapters, {len(travel["places"])} abroad places')
