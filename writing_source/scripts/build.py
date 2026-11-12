#!/usr/bin/env python3
"""Build self-contained, static GitHub Pages writing archive from Markdown only."""
from pathlib import Path
import argparse,html,json,re,shutil,sys
from collections import defaultdict
import yaml
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
MD=MarkdownIt('commonmark',{'html':False,'linkify':True}).enable('table')

def esc(v): return html.escape(str(v or ''),quote=True)
def url(base,relative):return base+relative.lstrip('/')
def chapter_href(c): return c['url'] if c.get('has_body') or not c.get('brunch_url') else c['brunch_url']
def chapter_attrs(c): return '' if c.get('has_body') or not c.get('brunch_url') else ' target="_blank" rel="noopener noreferrer"'
BOOK_DESCRIPTIONS={'solo-abroad':'A solo journey across the Americas, written in Korean.','milan-night':'A night in Milan and the long journey it set in motion.','ometepe':'A spring-break journey through the Caribbean and Nicaragua.','caribbean':'Island-hopping stories from the southern Caribbean.','el-salvador':'A student escapes class for a journey to El Salvador.'}
def frontmatter(path):
 s=path.read_text(encoding='utf-8-sig');m=re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$',s,re.S)
 if not m:raise ValueError(f'Missing YAML frontmatter: {path}')
 data=yaml.safe_load(m[1]) or {};return data,m[2]
def make_page(title,body,base,style,nav='Writing'):
 header=(ROOT/'assets/header-fragment.html').read_text()
 footer=(ROOT/'assets/footer-fragment.html').read_text()
 # links are relative to /Portfolio/, not the current chapter directory
 h=BeautifulSoup(header,'html.parser');f=BeautifulSoup(footer,'html.parser')
 for a in list(h.select('a[href]'))+list(f.select('a[href]')):
  href=a.get('href','')
  if href=='#top':a['href']='#top'
  elif href.startswith('#'):a['href']=base+'writing/'+('' if href=='#writing' else href[1:]+'/')
  elif href.startswith('../'):a['href']=base+href[3:]
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f8f5ef"><title>{esc(title)} — Chaehyun Lim</title><link rel="stylesheet" href="{base}writing/assets/style.css"><link rel="icon" type="image/svg+xml" href="{base}assets/favicon.svg"><meta property="og:type" content="article"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="Korean original essays and travel narratives by Chaehyun Lim."><meta property="og:image" content="https://limdaniel10.github.io/Portfolio/assets/social-card.png"><meta name="twitter:card" content="summary_large_image"></head><body id="top">{h}<main>{body}</main>{f}</body></html>'''

def build(root=ROOT,base='/Portfolio/',out=None):
 global ROOT;ROOT=Path(root).resolve()
 if not base.startswith('/') or not base.endswith('/'):raise ValueError('base must start/end with /')
 out=Path(out).resolve() if out else ROOT/'_site'
 if out.exists():shutil.rmtree(out)
 site=out/'writing';site.mkdir(parents=True)
 shutil.copytree(ROOT/'assets',site/'assets',ignore=shutil.ignore_patterns('*fragment.html'))
 configs=yaml.safe_load((ROOT/'content/collections.yml').read_text(encoding='utf8'))
 books={b['id']:dict(b,chapters=[]) for b in configs}; essays=[]; readings=[]; all_entries=[]; seen=set()
 for path in sorted((ROOT/'content').rglob('*.md')):
  meta,body=frontmatter(path);cat=meta.get('category');book=meta.get('collection_id')
  if cat not in ('collections','fiction','essays','readings'):raise ValueError(f'Invalid category: {path}')
  if book and book not in books:raise ValueError(f'Unknown collection_id {book}: {path}')
  if cat in ('collections','fiction') and not book:raise ValueError(f'collection_id required: {path}')
  chapter=meta.get('chapter');chapter=int(chapter) if chapter is not None else None
  if book and chapter is None:raise ValueError(f'chapter required: {path}')
  if book:
   key=(book,chapter)
   if key in seen:raise ValueError(f'Duplicate chapter {key}')
   seen.add(key)
  slug=path.stem;slug=re.sub('[^a-z0-9-]','-',slug.lower()).strip('-') or 'article'
  relative=f'articles/{book}/{slug}/' if book else f'articles/{cat}/{slug}/'
  item=dict(title=str(meta.get('title') or 'Untitled'),collection_id=book,chapter=chapter,date=str(meta.get('date') or ''),category=cat,special=bool(meta.get('special')),status=meta.get('status') or ('text' if body.strip() else 'external'),brunch_url=meta.get('brunch_url') or '',source_note=meta.get('source_note') or '',url=url(base,'writing/'+relative),path=relative,has_body=bool(body.strip()),body=body)
  if book:books[book]['chapters'].append(item)
  elif cat=='essays':essays.append(item)
  else:readings.append(item)
  all_entries.append(item)
 for b in books.values():b['chapters'].sort(key=lambda c:(c['chapter'],c['special']))
 # HTML index and chapter navigation generated from filesystem, not manual JSON
 index={'collections':[{**{k:v for k,v in b.items() if k!='chapters'},'chapters':[{k:v for k,v in c.items() if k!='body'} for c in b['chapters']]} for b in books.values()], 'essays':[{k:v for k,v in c.items() if k!='body'} for c in essays], 'readings':[{k:v for k,v in c.items() if k!='body'} for c in readings]}
 (site/'writing-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf8')
 for item in all_entries:
  if item['status']=='missing':continue
  p=site/item['path'];p.mkdir(parents=True,exist_ok=True)
  book=books.get(item['collection_id']);siblings=book['chapters'] if book else sorted([e for e in all_entries if e['category']==item['category'] and not e['collection_id']],key=lambda e:(e['date'],e['title']))
  ix=siblings.index(item);prev=siblings[ix-1] if ix else None;nxt=siblings[ix+1] if ix+1<len(siblings) else None
  crumbs=f'<a href="{base}writing/">Writing</a><span>/</span><a href="{base}writing/{"fiction" if book and book["category"]=="fiction" else "collections" if book else item["category"]}/">{esc(book["title"] if book else item["category"].title())}</a>'
  content=MD.render(item['body']) if item['has_body'] else '<p class="empty-note">This chapter is available on Brunch in Korean.</p>' if item['brunch_url'] else '<p class="empty-note">This chapter is not yet available here.</p>'
  links=''.join(f'<a href="{esc(item[k])}" target="_blank" rel="noopener noreferrer">{label} ↗</a>' for k,label in [('brunch_url','Read on Brunch')] if item[k])
  navigation=f'<nav class="reader-nav" aria-label="Chapter navigation">'+(f'<a href="{chapter_href(prev)}">← Previous</a>' if prev else '<span></span>')+f'<a href="{base}writing/{"book/"+book["id"]+"/" if book else item["category"]+"/"}">Table of contents</a>'+(f'<a href="{chapter_href(nxt)}">Next →</a>' if nxt else '<span></span>')+'</nav>'
  article=f'<section class="shell detail-view" style="display:block"><div class="detail-breadcrumb">{crumbs}</div><article class="reader-layout"><div class="reader-overline"><span>{esc(book["title"] if book else item["category"].title())}</span><span>{"SPECIAL" if item["special"] else "TEXT ARCHIVE"}</span></div><div class="reader-heading"><span class="reader-ordinal">{item["chapter"] or ""}</span><h1>{esc(item["title"])}</h1><p>{esc(item["date"])}</p></div><div class="essay-reading-body">{content}</div><div class="reader-source-links">{links}</div>{navigation}</article></section>'
  (p/'index.html').write_text(make_page(item['title'],article,base,''),encoding='utf8')
 for b in books.values():
  p=site/'book'/b['id'];p.mkdir(parents=True,exist_ok=True)
  chapters_html=''.join(f'<a class="chapter-row" href="{esc(chapter_href(c))}"{chapter_attrs(c)}><span class="chapter-number">{"SPECIAL" if c["special"] else str(c["chapter"]).zfill(2)}</span><span class="chapter-title">{esc(c["title"])}</span><span class="chapter-arrow">↗</span></a>' for c in b['chapters'] if c['status']!='missing') or '<p class="empty-note">No chapters yet. Add a Markdown file to this collection.</p>'
  view=f'<section class="shell detail-view" style="display:block"><div class="detail-breadcrumb"><a href="{base}writing/">Writing</a><span>/</span><a href="{base}writing/collections/">Collections</a><span>/</span>{esc(b["title"])}</div><div class="book-detail"><div><div class="book-cover book-{b["order"]}"><span class="book-kicker">{esc(b["status"])}</span><strong class="book-name">{esc(b["title"])}</strong></div></div><div><div class="eyebrow">{esc(b["status"])}</div><h2>{esc(b["title"])}</h2><p>{esc(BOOK_DESCRIPTIONS.get(b["id"],"Original Korean-language essays, first shared on Brunch."))}</p><p>{sum(c["status"]!="missing" for c in b["chapters"])} published chapters · Read here or follow the original Brunch publication.</p><div class="toc"><div class="toc-head"><h3>Table of contents</h3><span>{sum(c["status"]!="missing" for c in b["chapters"])} entries</span></div><div class="chapter-list">{chapters_html}</div></div></div></div></section>'
  (p/'index.html').write_text(make_page(b['title'],view,base,''),encoding='utf8')
 # landing page original visual blocks preserved
 home=BeautifulSoup((ROOT/'assets/home-fragment.html').read_text(),'html.parser')
 for a in home.select('a[href]'):
  h=a['href'];a['href']=url(base,'writing/'+h[1:]+'/') if h.startswith('#') else h
 for section,btype in [('collections','collections'),('fiction','fiction'),('essays','essays'),('readings','readings')]:
  card=home.select_one('a.portal-card.'+section)
  if card:
   count=sum(len(b['chapters']) for b in books.values() if b['category']==btype) if btype in ('collections','fiction') else len(essays if btype=='essays' else readings)
   small=card.select_one('.card-bottom small')
   if small:small.string=("Planned Korean SF trilogy" if section=="fiction" else "Notes in progress" if section=="readings" else f"{count} entries" if section!="collections" else f'{sum(b["status"]=="completed" for b in books.values())} complete · {sum(b["status"]=="in-progress" for b in books.values())} in progress')
 (site/'index.html').write_text(make_page('Writing',str(home),base,''),encoding='utf8')
 for cat in ['collections','fiction','essays','readings']:
  p=site/cat;p.mkdir(exist_ok=True)
  if cat in ['collections','fiction']:
   arr=[b for b in books.values() if b['category']==cat];arr.sort(key=lambda x:x['order'])
   groups=[('Completed manuscripts',[b for b in arr if b['status']=='completed']),('Works in progress',[b for b in arr if b['status']=='in-progress']),('Planned fiction',[b for b in arr if b['status']=='planned'])]
   body=''.join(f'<section class="content-section"><div class="section-header"><h3>{label}</h3></div><div class="book-grid">'+''.join(f'<a class="book-entry" href="{base}writing/book/{b["id"]}/"><div class="book-cover book-{b["order"]}"><span class="book-kicker">{esc(b["status"])}</span><strong class="book-name">{esc(b["title"])}</strong></div><div class="book-caption"><strong>{esc(b["title"])}</strong><span>{len(b["chapters"])} chapters ↗</span></div></a>' for b in group)+'</div></section>' for label,group in groups if group)
  else:
   arr=essays if cat=='essays' else readings
   body='<div class="chapter-list">'+''.join(f'<a class="chapter-row" href="{a["url"]}"><span class="chapter-title">{esc(a["title"])}</span><span class="chapter-arrow">↗</span></a>' for a in arr)+'</div>' if arr else '<p class="empty-note">New writing will appear here as the archive grows.</p>'
  page=f'<section class="shell detail-view" style="display:block"><div class="detail-breadcrumb"><a href="{base}writing/">Writing</a><span>/</span>{cat.title()}</div><div class="detail-top"><div><span class="eyebrow">The writing archive</span><h2>{cat.title()}</h2><p>{"Manuscripts, chapters and ongoing work" if cat=="collections" else "A growing archive"}</p></div></div>{body}</section>'
  (p/'index.html').write_text(make_page(cat.title(),page,base,''),encoding='utf8')
 return index

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--base',default='/Portfolio/');ap.add_argument('--out',default=None);a=ap.parse_args();idx=build(base=a.base,out=a.out);print('Built',sum(len(b['chapters']) for b in idx['collections']),'chapters,',len(idx['essays']),'essays')
