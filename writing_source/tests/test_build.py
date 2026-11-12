import json,sys,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build import build

def run():
 with tempfile.TemporaryDirectory() as td:
  copy=Path(td)/'repo';shutil.copytree(ROOT/'content',copy/'content');shutil.copytree(ROOT/'assets',copy/'assets');shutil.copytree(ROOT/'scripts',copy/'scripts')
  initial=build(root=copy,base='/Portfolio/')
  assert sum(len(b['chapters']) for b in initial['collections'])==107
  assert [len(b['chapters']) for b in initial['collections'][:5]]==[40,20,17,17,13]
  assert (copy/'_site/writing/articles/solo-abroad/001/index.html').exists()
  test=copy/'content/collections/solo-abroad/041.md'
  test.write_text('''---
title: 자동 생성 테스트
collection_id: solo-abroad
chapter: 41
date: 2026-11-12
category: collections
brunch_url: https://brunch.co.kr/@lim-eat-less/999
---

## 새 글

GitHub Markdown에서 자동으로 생성된 본문입니다.
''',encoding='utf8')
  new=build(root=copy,base='/Portfolio/')
  b=next(x for x in new['collections'] if x['id']=='solo-abroad')
  assert len(b['chapters'])==41
  page=copy/'_site/writing/articles/solo-abroad/041/index.html'
  assert page.exists();html=page.read_text();assert 'GitHub Markdown에서 자동으로 생성된 본문입니다.' in html
  assert '<h2>새 글</h2>' in html
  assert '/Portfolio/writing/articles/solo-abroad/040/' in html
  assert '/Portfolio/writing/' in html
  assert 'brunch.co.kr/@lim-eat-less/999' in html
  idx=json.loads((copy/'_site/writing/writing-index.json').read_text())
  assert any(c['chapter']==41 for c in idx['collections'][0]['chapters'])
  test.unlink();deleted=build(root=copy,base='/Portfolio/')
  assert len(deleted['collections'][0]['chapters'])==40
  assert not page.exists()
  print('PASS: 107 baseline chapters; add chapter 41 -> JSON, collection, HTML, navigation, Markdown conversion, Brunch link; delete -> removed')
if __name__=='__main__':run()
