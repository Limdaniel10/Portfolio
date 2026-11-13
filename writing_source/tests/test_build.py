import json,sys,tempfile,shutil
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
  initial=build(root=copy,base='/Portfolio/')
  initial_chapters=sum(len(b['chapters']) for b in initial['collections'])
  assert initial_chapters>=107, 'Original writing archive lost chapters'
  assert all(len(b['chapters'])>=baseline for b,baseline in zip(initial['collections'][:5],[40,20,17,17,13])), 'Archived collections lost chapters'
  assert (copy/'_site/writing/articles/solo-abroad/001/index.html').exists()
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
