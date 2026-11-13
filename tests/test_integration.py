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
# Four-language selector should be available on the home and all five sections.
assert (SITE/'js/i18n.js').exists() and (SITE/'css/i18n.css').exists(), 'Missing localization files'
for section in ('', *expected):
    page = SITE / section / 'index.html' if section else SITE / 'index.html'
    markup = page.read_text(encoding='utf8')
    assert 'i18n.js' in markup and 'i18n.css' in markup, f'Missing language control on {section or "home"}'
assert all(code in (SITE/'js/i18n.js').read_text(encoding='utf8') for code in ('en', 'ko', 'zh-Hans', 'es'))
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
assert len(highlight_data)>=405 and len({e['id'] for e in highlight_data})==len(highlight_data)
assert all(sum(e['source']==s for e in highlight_data)>=expected for s,expected in (('I',100),('II',100),('III',100),('IV',100),('V',5)))
assert all(sum(e['source']==s for e in highlight_data)<=100 for s in ('I','II','III','IV','V'))
assert sum(bool(e['book_id']) for e in highlight_data)>=355
assert next(e for e in highlight_data if e['id']=='HI-065')['text'].count('“나는 단수가 아니다.”')==1
assert any(e['id']=='HV-005' and e['book_id']=='BK-001413' for e in highlight_data)
# Multiple-read works must map to the earliest matching completed book.
known={'HII-034':'BK-000098','HI-067':'BK-000488','HIII-085':'BK-000301','HIII-089':'BK-000609'}
assert {e['id']:e['book_id'] for e in highlight_data if e['id'] in known}==known

assert all(e['title'] and e['text'] and e['review_status'] for e in highlight_data)
assert {e['book_id'] for e in highlight_data if e['book_id']} <= {b['id'] for b in books}
# The user confirmed Heo Yeon is the author of the two completed catalogue entries.
by_book={b['id']:b for b in books}
assert by_book['BK-000611']['author']=='허연'
assert by_book['BK-000636']['author']=='허연'
assert by_book['BK-000365']['author']=='무라카미 하루키'
by_highlight={e['id']:e for e in highlight_data}
assert by_highlight['HII-022']['book_id']=='BK-000611'
assert by_highlight['HII-022']['author']=='허연'
assert by_highlight['HII-022']['review_status']=='Approved'
# Hemingway's identically titled book was unfinished; it must not attach to Murakami.
assert by_highlight['HII-025']['author']=='어니스트 헤밍웨이'
assert not by_highlight['HII-025']['book_id']
assert by_highlight['HII-025']['review_status']=='Unfinished'

assert 'ORIGINAL NOTEBOOKS' not in (SITE/'reading/index.html').read_text(encoding='utf8')
reading_page=(SITE/'reading/index.html').read_text(encoding='utf8')
reading_js=(SITE/'reading/app.js').read_text(encoding='utf8')
assert 'Some books, lines that stayed with me.' in reading_page
assert 'id="highlightSearch"' in reading_page
assert 'id="highlightSource"' not in reading_page
assert 'highlight-source-links' not in reading_page
assert 'Open a year, then a month' not in reading_page
assert 'highlight-explainer' not in reading_page
assert 'Notion Highlight I' not in reading_page
assert 'Sorted by book completion' not in reading_page
assert 'group("highlight-year","ETC"' in reading_js
assert 'filter.addEventListener' not in reading_js

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
