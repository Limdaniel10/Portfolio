import json,sys,tempfile,shutil,re
from bs4 import BeautifulSoup
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import build

def run():
 with tempfile.TemporaryDirectory() as td:
  copy=Path(td)/'repo'
  shutil.copytree(ROOT/'content',copy/'content')
  shutil.copytree(ROOT/'assets',copy/'assets')
  shutil.copytree(ROOT/'scripts',copy/'scripts')
  # Every published manuscript should be clean prose, with no exported linebreak
  # backslashes or Markdown horizontal rules that show up as stray visual marks.
  checked=0
  for source in (copy/'content').rglob('*.md'):
   raw=source.read_text(encoding='utf8')
   lines=raw.splitlines()
   end_meta=next((i for i,line in enumerate(lines[1:],start=1) if line.strip()=='---'),None)
   assert lines and lines[0].strip()=='---' and end_meta is not None, f'{source}: missing frontmatter'
   for n,line in enumerate(lines[end_meta+1:],start=end_meta+2):
    stripped=line.strip()
    assert stripped!=chr(92), f'{source}:{n} has stray backslash'
    assert not (len(stripped)>=3 and len(set(stripped))==1 and stripped[0] in '-_*'), f'{source}:{n} has unwanted horizontal rule'
   checked+=1
  assert checked>=110, f'Expected all archived manuscripts; found {checked}'
  print(f'PASS: {checked} Writing manuscripts contain no isolated backslashes or horizontal rules')
  mountain=(copy/'content/collections/ometepe/014.md').read_text(encoding='utf8')
  assert '2023. 03. 25 · Day 8' in mountain or '2023\. 03. 25 · Day 8' in mountain
  initial=build(root=copy,base='/Portfolio/')
  initial_chapters=sum(len(b['chapters']) for b in initial['collections'])
  assert initial_chapters>=107, 'Original writing archive lost chapters'
  assert all(len(b['chapters'])>=baseline for b,baseline in zip(initial['collections'][:5],[40,20,17,17,13])), 'Archived collections lost chapters'
  assert (copy/'_site/writing/articles/solo-abroad/001/index.html').exists()
  # A date starting with "2023. 03." is prose, NOT two ordered lists.
  for slug in ('011','014','017-special'):
   content=(copy/f'_site/writing/articles/ometepe/{slug}/index.html').read_text(encoding='utf8')
   assert '<ol start="2023">' not in content, f'{slug}: year was parsed as list'
   assert '2023. 03.' in content, f'{slug}: date text missing'
  assert '<p>2023. 03. 24 · Day 7</p>' in (copy/'_site/writing/articles/ometepe/011/index.html').read_text(encoding='utf8')
  assert '<p>2023. 11. 01: 팔도 도시락</p>' in (copy/'_site/writing/articles/milan-night/005/index.html').read_text(encoding='utf8'), 'Milan chapter 5 date must render as regular prose'
  # Audit every published HTML chapter, not just its Markdown source.
  verified_dates=0
  inspected_pages=0
  for manuscript in (copy/'content').rglob('*.md'):
   raw=manuscript.read_text(encoding='utf8')
   front_end=re.search(r'\A---\s*\n[\s\S]*?\n---\s*\n',raw)
   assert front_end, f'{manuscript}: bad frontmatter'
   body=raw[front_end.end():]
   if not body.strip() or 'status: missing' in raw[:front_end.end()]:continue
   folder=manuscript.parent.name if manuscript.parent.name!='essays' else 'essays'
   if folder not in ('essays','readings'):
    slug='articles/'+folder+'/'+manuscript.stem
   else:slug='articles/'+folder+'/'+manuscript.stem
   page=copy/'_site/writing'/slug/'index.html'
   assert page.exists(), f'Missing rendered page: {manuscript}'
   soup=BeautifulSoup(page.read_text(encoding='utf8'),'html.parser')
   article=soup.select_one('.essay-reading-body')
   assert article is not None, f'Missing rendered prose: {manuscript}'
   assert not article.select('hr'), f'Unexpected horizontal line in {manuscript}'
   assert all(p.get_text(strip=True)!=chr(92) for p in article.select('p')),f'Stray backslash in {manuscript}'
   for line in body.splitlines():
    date=re.match(r'^\s*((?:20\d{2}|\d{2}))\\?\.\s+(\d{1,2})\.\s*(\d{1,2})',line)
    if not date:continue
    expect=f'{date.group(1)}. {date.group(2)}. {date.group(3)}'
    paragraphs=[re.sub(r'\s+',' ',p.get_text(' ',strip=True)) for p in article.select('p')]
    assert any(expect in text for text in paragraphs),f'Date rendered as list or missing: {manuscript}: {line!r}'
    verified_dates+=1
   inspected_pages+=1
  assert inspected_pages>=95, f'Expected published manuscripts, got {inspected_pages}'
  assert verified_dates>=50, f'Date coverage unexpectedly low: {verified_dates}'
  print(f'PASS: {inspected_pages} published Writing pages inspected in HTML; {verified_dates} dates render as paragraphs; no unwanted horizontal rules')
  book_before=next(b for b in initial['collections'] if b['id']=='solo-abroad')
  target_folder=copy/'content/collections/solo-abroad'
  ids=[int(p.stem) for p in target_folder.glob('*.md') if p.stem.isdigit()]
  next_chapter=max(ids,default=0)+1
  chapter_slug=f'{next_chapter:03d}'
  test=target_folder/f'{chapter_slug}.md'
  assert not test.exists()
  test.write_text(f'''---
title: 자동 생성 테스트
collection_id: solo-abroad
chapter: {next_chapter}
date: 2026-11-12
category: collections
status: text
brunch_url: https://brunch.co.kr/@lim-eat-less/999
---

## 새 글

GitHub Markdown에서 자동으로 생성된 본문입니다.
''',encoding='utf8')
  new=build(root=copy,base='/Portfolio/')
  b=next(x for x in new['collections'] if x['id']=='solo-abroad')
  assert len(b['chapters'])==len(book_before['chapters'])+1
  page=copy/f'_site/writing/articles/solo-abroad/{chapter_slug}/index.html'
  assert page.exists()
  html=page.read_text(encoding='utf8')
  assert 'GitHub Markdown에서 자동으로 생성된 본문입니다.' in html
  assert '<h2>새 글</h2>' in html
  assert '/Portfolio/writing/' in html
  assert 'brunch.co.kr/@lim-eat-less/999' in html
  idx=json.loads((copy/'_site/writing/writing-index.json').read_text(encoding='utf8'))
  assert any(c['chapter']==next_chapter for c in next(b for b in idx['collections'] if b['id']=='solo-abroad')['chapters'])
  test.unlink()
  deleted=build(root=copy,base='/Portfolio/')
  assert len(next(b for b in deleted['collections'] if b['id']=='solo-abroad')['chapters'])==len(book_before['chapters'])
  assert not page.exists()
  print(f'PASS: {initial_chapters} baseline chapters; add chapter {next_chapter} -> regenerated index, HTML, navigation, Brunch link; remove -> restored')
if __name__=='__main__':
 run()
