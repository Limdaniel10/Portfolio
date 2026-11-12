#!/usr/bin/env python3
"""Synchronize complete travel archive from nine Google Sheets tabs or bundled CSV.

This deliberately preserves the original map geometry for existing routes and builds
new point/flight features from newly added spreadsheet rows. All nine tabs form one
transaction: validation failures leave the previous traveling/assets/data.js intact.
"""
from __future__ import annotations
import argparse,csv,json,math,os,re,sys,tempfile
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
SHEETS=ROOT/'traveling/sheets'
OUTPUT=ROOT/'traveling/assets/data.js'
BASE=ROOT/'traveling/data/baseline.json'
TABLES={
 'Countries':('countries',['iso2','name','count_in_195','category']),
 'Places':('places',['id','name','type','latitude','longitude','country_iso2','first_visit_year','count_as_city_or_town']),
 'DomesticPlaces':('domestic_places',['id','name','type','latitude','longitude','country_iso2','region']),
 'Visits':('visits',['place_id','year','months','start_date','end_date','date_precision']),
 'Airports':('airports',['id','iata','name','municipality','country_iso2','latitude','longitude','source','type']),
 'Flights':('flights',['id','year','months','origin','destination','count_status','purpose']),
 'AirportNights':('airport_overnights',['id','date','year','place','airport_iata','latitude','longitude']),
 'Stays':('stays',['country_iso2','start_date','end_date']),
 'SurfaceRoutes':('surface_routes',['id','year','months','mode','from_name','to_name','from_lat','from_lon','to_lat','to_lon']),
}
FLOATS={'latitude','longitude','from_lat','from_lon','to_lat','to_lon'}
INTS={'year','first_visit_year'}
BOOLS={'count_in_195','count_as_city_or_town'}
NULLABLE={'end_date','first_visit_year','source','municipality','region','purpose','type','date_precision','start_date','from_name','to_name'}
MONTH_RE=re.compile(r'^20\d\d-(0[1-9]|1[012])$')
class TravelDataError(ValueError):pass

def convert(name,values):
 header=[str(v).strip().lstrip('\ufeff') for v in values[0]] if values else []
 expected=TABLES[name][1]
 if header[:len(expected)]!=expected:raise TravelDataError(f'{name}: expected headers {expected}, received {header}')
 records=[]
 for n,raw in enumerate(values[1:],2):
  if not any(str(x).strip() for x in raw):continue
  row={k:(str(raw[i]).strip() if i<len(raw) and raw[i] is not None else '') for i,k in enumerate(expected)}
  for k,v in list(row.items()):
   if k=='months':
    row[k]=[x.strip() for x in v.split(';') if x.strip()]
    if not all(MONTH_RE.fullmatch(x) for x in row[k]):raise TravelDataError(f'{name} row {n}: invalid months')
   elif k in BOOLS:
    if v.lower() not in ('true','false','yes','no','1','0'):raise TravelDataError(f'{name} row {n}: {k} must be TRUE/FALSE')
    row[k]=v.lower() in ('true','yes','1')
   elif k in FLOATS:
    try:row[k]=float(v)
    except ValueError as e:raise TravelDataError(f'{name} row {n}: {k} must be numeric') from e
    if not math.isfinite(row[k]) or (('lat' in k and not -90<=row[k]<=90) or ('lon' in k and not -180<=row[k]<=180)):
     raise TravelDataError(f'{name} row {n}: invalid coordinate {k}={row[k]}')
   elif k in INTS:
    if v=='':
     if k in NULLABLE:row[k]=None
     else:raise TravelDataError(f'{name} row {n}: {k} required')
    else:
     try:row[k]=int(v)
     except ValueError as e:raise TravelDataError(f'{name} row {n}: {k} must be integer') from e
   elif not v and k in NULLABLE:row[k]=None
  records.append(row)
 if not records:raise TravelDataError(f'{name}: no data rows; refusing to publish an empty archive')
 return records

def validate(tables,baseline,allow_deletions=False):
 for n,(key,_) in TABLES.items():
  current=tables[key];base=baseline['geometry']['features'] if key=='surface_routes' else baseline[key]
  ident='iso2' if key=='countries' else 'place_id' if key=='visits' else 'country_iso2' if key=='stays' else 'id'
  if key in ('visits','stays'):continue
  if key=='countries':
   # Source archive deliberately contains two entries for GB and MD with
   # different counting/category semantics. Do not deduplicate them.
   signatures=[(r['iso2'],r['count_in_195'],r['category']) for r in current]
   if len(signatures)!=len(set(signatures)):
    raise TravelDataError('Countries: duplicate (iso2, count_in_195, category) row')
   if not allow_deletions:
    previous={(r['iso2'],r['count_in_195'],r['category']) for r in base}
    if previous-set(signatures):raise TravelDataError('Countries: source country classifications were deleted')
   continue
  values=[r[ident] for r in current]
  if any(not v for v in values) or len(values)!=len(set(values)):
   raise TravelDataError(f'{n}: missing or duplicate {ident}')
  if not allow_deletions:
   old={r['properties']['id'] for r in base if r['properties'].get('kind')=='surface_route'} if key=='surface_routes' else {r[ident] for r in base}
   if old-set(values):raise TravelDataError(f'{n}: {len(old-set(values))} existing records removed. Refusing accidental data loss; use --allow-deletions for intentional removals.')
 country={r['iso2'] for r in tables['countries']};pids={r['id'] for r in tables['places']};ap={r['iata'] for r in tables['airports']}
 for p in tables['places']+tables['domestic_places']:
  if p['country_iso2'] not in country:raise TravelDataError(f"Unknown country code {p['country_iso2']}: add it to Countries first")
 for v in tables['visits']:
  if v['place_id'] not in pids:raise TravelDataError(f"Visit place_id not in Places: {v['place_id']}")
 for f in tables['flights']:
  if f['origin'] not in ap or f['destination'] not in ap:raise TravelDataError(f"Flight {f['id']} unknown airport: {f['origin']}/{f['destination']}")
 for s in tables['stays']:
  if s['country_iso2'] not in country:raise TravelDataError(f"Stay: unknown country {s['country_iso2']}")
 for a in tables['airport_overnights']:
  if a['airport_iata'] not in ap:raise TravelDataError(f"Airport night: unknown airport {a['airport_iata']}")

def flight_coords(a,b):
 # Short schematic route; cross-antimeridian legs are split at 180°.
 lon1,lat1=a['longitude'],a['latitude'];lon2,lat2=b['longitude'],b['latitude']
 delta=lon2-lon1
 if abs(delta)<=180:return {'type':'LineString','coordinates':[[lon1,lat1],[lon2,lat2]]}
 if delta>180:lon2-=360
 else:lon2+=360
 edge=180 if lon2>180 else -180
 t=(edge-lon1)/(lon2-lon1)
 mid=lat1+t*(lat2-lat1)
 return {'type':'MultiLineString','coordinates':[[[lon1,lat1],[edge,mid]],[[-edge,mid],[b['longitude'],lat2]]]}

def build_data(tables,baseline):
 data={k:baseline[k] for k in ('schema_version','transport_modes','country_basis')}
 # Author-confirmed count: 193 UN members plus Vatican City; Taiwan is excluded.
 data['country_basis']=194
 data['transport_modes']=sorted(set(data['transport_modes'])|{r['mode'] for r in tables['surface_routes']})
 for _,(key,_) in TABLES.items():
  if key!='surface_routes':data[key]=tables[key]
 orig={(f['properties']['kind'],f['properties'].get('id')):f for f in baseline['geometry']['features']}
 visits=defaultdict(list)
 for v in data['visits']:visits[v['place_id']].append(v)
 feats=[]
 def point(x,kind,props):return {'type':'Feature','geometry':{'type':'Point','coordinates':[x['longitude'],x['latitude']]},'properties':{'kind':kind,**props}}
 for p in data['places']:
  vv=visits[p['id']]
  feats.append(point(p,'place',{'id':p['id'],'name':p['name'],'country_iso2':p['country_iso2'],'years':sorted({v['year'] for v in vv}),'months_resolved':sorted({v['months'][0] for v in vv if len(v['months'])==1})}))
 for p in data['domestic_places']:
  feats.append(point(p,'domestic_place',{'id':p['id'],'name':p['name'],'country_iso2':p['country_iso2']}))
 for r in tables['surface_routes']:
  f=orig.get(('surface_route',r['id']))
  coords=[[r['from_lon'],r['from_lat']],[r['to_lon'],r['to_lat']]]
  if f is not None:
   old=f['geometry']['coordinates']
   if old and math.dist(old[0],coords[0])<.001 and math.dist(old[-1],coords[-1])<.001:
    geom=f['geometry'] # Original curved route remains unchanged
   else:geom={'type':'LineString','coordinates':coords}
  else:geom={'type':'LineString','coordinates':coords}
  feats.append({'type':'Feature','geometry':geom,'properties':{'kind':'surface_route','id':r['id'],'year':r['year'],'months':r['months'],'month_resolved':len(r['months'])==1,'mode':r['mode'],'from_name':r['from_name'] or '', 'to_name':r['to_name'] or ''}})
 airports={a['iata']:a for a in data['airports']}
 for f in data['flights']:
  if f['count_status']!='recorded_flown' or f['origin']==f['destination']:continue
  old=orig.get(('flight',f['id']))
  geom=old['geometry'] if old and old['properties'].get('from')==f['origin'] and old['properties'].get('to')==f['destination'] else flight_coords(airports[f['origin']],airports[f['destination']])
  feats.append({'type':'Feature','geometry':geom,'properties':{'kind':'flight','id':f['id'],'year':f['year'],'months':f['months'],'month_resolved':len(f['months'])==1,'mode':'Plane','from':f['origin'],'to':f['destination']}})
 for n in data['airport_overnights']:
  feats.append({'type':'Feature','geometry':{'type':'Point','coordinates':[n['longitude'],n['latitude']]},'properties':{'kind':'airport_overnight','id':n['id'],'date':n['date'],'year':n['year'],'airport':n['airport_iata']}})
 data['geometry']={'type':'FeatureCollection','features':feats}
 return data

def main(argv=None):
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--from-csv',action='store_true')
 parser.add_argument('--spreadsheet-id',default=os.environ.get('GOOGLE_TRAVEL_SHEETS_ID',''))
 parser.add_argument('--allow-deletions',action='store_true')
 args=parser.parse_args(argv)
 baseline=json.loads(BASE.read_text(encoding='utf8'))
 if not args.from_csv:
  if not args.spreadsheet_id:raise TravelDataError('GOOGLE_TRAVEL_SHEETS_ID is not set')
  from sync_reading import authenticate,load_live_sheet
  headers=authenticate()
 data={}
 for name,(key,_) in TABLES.items():
  if args.from_csv:
   with (SHEETS/(name+'.csv')).open(encoding='utf-8-sig',newline='') as f: rows=list(csv.reader(f))
  else:rows=load_live_sheet(args.spreadsheet_id,name,headers)
  data[key]=convert(name,rows)
 validate(data,baseline,args.allow_deletions)
 payload=build_data(data,baseline)
 text='window.TRAVEL='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n'
 OUTPUT.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile('w',encoding='utf8',dir=OUTPUT.parent,delete=False,prefix='.travel-',suffix='.js') as f:
  f.write(text); temp=f.name
 os.replace(temp,OUTPUT)
 print(f"Validated Travel archive: {len(payload['countries'])} countries/territories, {len(payload['places'])} abroad places, {len(payload['flights'])} flight records, {len(payload['geometry']['features'])} geometry features")
if __name__=='__main__':
 try:main()
 except (TravelDataError,FileNotFoundError,csv.Error,ValueError) as e:
  print(f'TRAVEL SYNC FAILED: {e}',file=sys.stderr);sys.exit(1)
