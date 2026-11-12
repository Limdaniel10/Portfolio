#!/usr/bin/env python3
"""One-time local conversion of archived Notion JSON text files into existing Markdown.
No API calls. Existing Markdown with real text is never overwritten without --overwrite.
"""
import argparse,json,re,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]

def parse_md(p):
 text=p.read_text(encoding='utf8');m=re.match(r'\A---\n(.*?)\n---\n(.*)\Z',text,re.S)
 return yaml.safe_load(m[1]),m[2]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('files',nargs='+',type=Path);ap.add_argument('--overwrite',action='store_true');args=ap.parse_args()
 index={}
 for p in (ROOT/'content/collections').rglob('*.md'):
  fm,body=parse_md(p)
  notion=(fm.get('notion_source') or '').split('/p/')[-1].split('?')[0]
  if notion:index[notion]=(p,fm,body)
 count=0;skipped=[]
 for file in args.files:
  data=json.loads(file.read_text(encoding='utf8-sig'))
  if not isinstance(data,list):raise ValueError(f'Expected JSON array: {file}')
  for entry in data:
   ident=entry.get('id') or entry.get('notion_id')
   if ident not in index:skipped.append((ident,'No matching existing chapter'));continue
   p,fm,old=index[ident]
   if old.strip() and not args.overwrite:skipped.append((ident,'Existing text protected'));continue
   body=entry.get('body') or entry.get('text') or ''
   if not isinstance(body,str) or not body.strip():skipped.append((ident,'Empty source text'));continue
   # Notion markdown is retained; only Notion-specific image blocks are stripped.
   body=re.sub(r'!\[[^\]]*\]\([^\n]+\)', '',body)
   body=re.sub(r'<\/?(?:columns|column)[^>]*>', '',body)
   body=re.sub(r'<p\s*/>', '\n\n',body)
   body=re.sub(r'\n{3,}','\n\n',body).strip()
   fm['status']='text';fm['source_note']='Original Notion manuscript (text-only import)'
   p.write_text('---\n'+yaml.safe_dump(fm,allow_unicode=True,sort_keys=False).strip()+'\n---\n\n'+body+'\n',encoding='utf8')
   count+=1
 print(f'Imported {count} original texts; skipped {len(skipped)}')
 for item in skipped[:20]:print('SKIP',*item)
if __name__=='__main__':main()
