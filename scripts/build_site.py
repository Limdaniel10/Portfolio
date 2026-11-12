#!/usr/bin/env python3
"""Assemble the entire GitHub Pages site, including Writing Markdown and real travel-map SVG.

For the Portfolio repository: python scripts/build_site.py --base /Portfolio/
For local test: python scripts/build_site.py --base /
"""
from __future__ import annotations
import argparse,json,re,shutil,subprocess,sys
from pathlib import Path
import pycountry

ROOT=Path(__file__).resolve().parents[1]

def parse_js_object(path,name):
 s=path.read_text(encoding='utf8').strip()
 prefix=f'window.{name}='
 if not s.startswith(prefix):raise ValueError(f'{path}: invalid {name} source')
 return json.loads(s[len(prefix):].rstrip(';'))

def make_map(data,world):
 highlighted=set(); secondary=set()
 for c in data['countries']:
  country=pycountry.countries.get(alpha_2=c['iso2'])
  code=country.alpha_3 if country else None
  if not code:continue
  (highlighted if c['count_in_195'] else secondary).add(code)
 def project(pt):
  x=(float(pt[0])+180)/360*1000
  y=(82-float(pt[1]))/160*500
  return (max(-30,min(1030,x)),max(-30,min(530,y)))
 def ringpath(ring):
  if len(ring)<3:return ''
  # Choose enough points for a crisp small SVG, while keeping the homepage light.
  step=max(1,len(ring)//220)
  points=ring[::step]
  if points[-1]!=ring[-1]:points.append(ring[-1])
  # Do not draw a line across the map where a ring crosses the antimeridian.
  segments=[];cur=[];last=None
  for pt in points:
   x,y=project(pt)
   if last is not None and abs(x-last[0])>450:
    if len(cur)>2:segments.append(cur)
    cur=[]
   cur.append((x,y));last=(x,y)
  if len(cur)>2:segments.append(cur)
  return ' '.join('M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in segment)+' Z' for segment in segments)
 svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" role="img" aria-label="Countries visited highlighted in aqua">',
      '<style>path{stroke:#50717e;stroke-width:.58;vector-effect:non-scaling-stroke;stroke-linecap:round;stroke-linejoin:round}</style>',
      '<g fill="none" stroke="#354d5c" stroke-width=".55" opacity=".3">',
      ''.join(f'<path d="M0 {i}H1000"/>' for i in (125,250,375)),
      '</g>']
 from html import escape
 mapped_ids={feature.get('id') for feature in world['features']}
 for feature in world['features']:
  fid=feature.get('id');geom=feature.get('geometry') or {};coords=geom.get('coordinates') or []
  # The very large Antarctic polygon obscures the visual at this small scale.
  if fid=='ATA':continue
  polys=[coords] if geom.get('type')=='Polygon' else coords if geom.get('type')=='MultiPolygon' else []
  d=' '.join(ringpath(r) for poly in polys for r in poly if len(r)>=3)
  if not d:continue
  color= '#91d3d9' if fid in highlighted else '#547c89' if fid in secondary else '#293f4c'
  name=escape(str(feature.get('properties',{}).get('name',fid)))
  svg.append(f'<path fill="{color}" d="{d}"><title>{name}</title></path>')
 # Microstates/small islands absent from the low-resolution map receive markers
 # at coordinates from the user's own recorded visited places (not guessed dots).
 for c in data['countries']:
  if not c['count_in_195']:continue
  country=pycountry.countries.get(alpha_2=c['iso2'])
  if country and country.alpha_3 in mapped_ids:continue
  candidates=[p for p in data['places'] if p.get('country_iso2')==c['iso2']]
  if not candidates:continue
  x,y=project([candidates[0]['longitude'],candidates[0]['latitude']])
  name=escape(str(c.get('name','small country')))
  svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.1" fill="#91d3d9" stroke="#f3fafb" stroke-width=".85"><title>{name}</title></circle>')
 svg.append('</svg>')
 return '\n'.join(svg)+'\n' 

def build(base,output):
 if not base.startswith('/') or not base.endswith('/'):
  raise ValueError('base should look like /Portfolio/ or /')
 if output.resolve() in (ROOT.resolve(),Path('/').resolve()):
  raise ValueError('Refusing unsafe output directory')
 output=output.resolve(); temp=(ROOT/'.build_writing').resolve()
 # Build Writing separately: its generator deletes the given output folder.
 subprocess.run([sys.executable,str(ROOT/'writing_source/scripts/build.py'),'--base',base,'--out',str(temp)],check=True)
 if output.exists():shutil.rmtree(output)
 output.mkdir(parents=True)
 for f in ('index.html','.nojekyll'):
  shutil.copy2(ROOT/f,output/f)
 for folder in ('css','js','assets','about','career'):
  shutil.copytree(ROOT/folder,output/folder)
 for folder in ('traveling','reading'):
  dst=output/folder;dst.mkdir()
  src=ROOT/folder
  include={'traveling':['index.html','style.css','app.js','assets'],
           'reading':['index.html','styles.css','app.js','data']}[folder]
  for item in include:
   p=src/item;q=dst/item
   if p.is_dir():shutil.copytree(p,q)
   else:shutil.copy2(p,q)
 shutil.copytree(temp/'writing',output/'writing')
 shutil.rmtree(temp)
 travel=parse_js_object(ROOT/'traveling/assets/data.js','TRAVEL')
 world=parse_js_object(ROOT/'traveling/assets/world.js','WORLD')
 d=output/'data';d.mkdir()
 n=sum(bool(c['count_in_195']) for c in travel['countries'])
 (d/'countries.json').write_text(json.dumps({'totalCountries':n,'continents':6,'source':'traveling/assets/data.js'},indent=2)+'\n',encoding='utf8')
 (d/'visited-world.svg').write_text(make_map(travel,world),encoding='utf8')
 print(f'Full site built: {output}, country highlights={n}, writing pages={len(list((output/"writing").rglob("index.html")))}')

def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--base',default='/Portfolio/')
 p.add_argument('--out',type=Path,default=ROOT/'_site')
 a=p.parse_args(argv)
 build(a.base,a.out)
if __name__=='__main__':main()
