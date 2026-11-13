"""Unit tests for add-only travel sheet conversion and map geometry behavior."""
import csv,copy,json,unittest
from pathlib import Path
from scripts.sync_travel import ROOT,SHEETS,BASE,TABLES,convert,validate,build_data,TravelDataError

class TravelSyncTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.baseline=json.loads(BASE.read_text(encoding='utf8'))
  cls.tables={}
  for name,(key,_) in TABLES.items():
   with (SHEETS/(name+'.csv')).open(encoding='utf-8-sig',newline='') as f:
    cls.tables[key]=convert(name,list(csv.reader(f)))
 def test_complete_archive_survives_round_trip(self):
  validate(self.tables,self.baseline)
  data=build_data(self.tables,self.baseline)
  self.assertEqual(sum(c['count_in_195'] for c in data['countries']),91)
  taiwan=[c for c in data['countries'] if c['iso2']=='TW']
  self.assertEqual(len(taiwan),1)
  self.assertTrue(taiwan[0]['count_in_195'])
  self.assertEqual(taiwan[0]['category'],'country')
  territories=[c for c in data['countries'] if not c['count_in_195'] and c['category']=='region_or_territory' and c['iso2'] not in ('GB','MD')]
  self.assertEqual(len(territories),6)
  self.assertGreaterEqual(len(data['geometry']['features']),len(self.baseline['geometry']['features']))
  self.assertEqual(data['country_basis'],196)
  self.assertIn('Bus',data['transport_modes'])
  verified={('place-0043',2024,'2024-02'),('place-0071',2025,'2025-10'),('place-0066',2025,'2025-12'),('place-0178',2026,'2026-05'),('place-0032',2026,'2026-06')}
  actual={(v['place_id'],v['year'],m) for v in data['visits'] for m in v['months']}
  self.assertTrue(verified.issubset(actual))
  self.assertFalse(any(p['country_iso2']=='HN' for p in data['places']))
  self.assertEqual(sum(f['count_status']=='recorded_flown' for f in data['flights']),278)
  rs=[f for f in data['geometry']['features'] if f['properties']['kind']=='surface_route']
  self.assertEqual(len(rs),len([f for f in self.baseline['geometry']['features'] if f['properties']['kind']=='surface_route'])+2)
  self.assertTrue(any(f['properties']['from_name']=='Moscow' and f['properties']['to_name']=='Irkutsk' for f in rs))
  legs={f['properties']['id']:f['properties'] for f in rs}
  self.assertEqual([(legs[f'route-086-leg-0{i}']['from_name'],legs[f'route-086-leg-0{i}']['to_name']) for i in (1,2,3)], [('St Petersburg','Moscow'),('Moscow','Irkutsk'),('Irkutsk','Vladivostok')])
  self.assertEqual(legs['route-086-leg-03']['months'],['2026-06'])
  self.assertEqual(legs['route-087-leg-01']['mode'],'Bus')
  self.assertEqual(legs['route-087-leg-02']['mode'],'Bus')
  self.assertEqual(legs['route-093-leg-01']['mode'],'Train')
  self.assertEqual(legs['route-093-leg-01']['from_name'],'Zurich Airport')
  self.assertEqual(legs['route-093-leg-01']['to_name'],'Geneva')
  self.assertEqual(legs['route-093-leg-01']['months'],['2022-07'])
  self.assertEqual(sum(f['count_status']=='recorded_flown' for f in data['flights']),278)
  self.assertEqual(len(data['places']),282)
  self.assertEqual(len(data['domestic_places']),69)
  # Rebooking is a separate actual flown leg. Preserve the cancelled ticket.
  self.assertTrue(any(f['origin']=='NAP' and f['destination']=='GVA' and f['count_status']=='cancelled' for f in data['flights']))
  self.assertTrue(any(f['origin']=='NAP' and f['destination']=='ZRH' and f['count_status']=='recorded_flown' for f in data['flights']))
  self.assertTrue(any(a['iata']=='ZRH' for a in data['airports']))
  expected_jp=[('place-0006',2011,'2011-07'),('place-0006',2011,'2011-08')]
  actual={(v['place_id'],v['year'],m) for v in data['visits'] for m in v['months']}
  self.assertTrue(all(v in actual for v in expected_jp))
  self.assertIn(('place-0021',2026,'2026-05'),actual)
  # Original Peru/Bolivia visits and cross-border route remain unchanged.
  route_names={(f['properties']['from_name'],f['properties']['to_name']) for f in data['geometry']['features'] if f['properties'].get('kind')=='surface_route'}
  self.assertIn(('Cusco','Puno'),route_names)
  self.assertIn(('Puno','Copacabana'),route_names)
 def test_add_place_visit_flight_and_route(self):
  tables=copy.deepcopy(self.tables)
  tables['places'].append(dict(id='place-new-test',name='New Test Place',type='city',latitude=34.0,longitude=-112.0,country_iso2='US',first_visit_year=2026,count_as_city_or_town=True))
  tables['visits'].append(dict(place_id='place-new-test',year=2026,months=['2026-11'],start_date='2026-11-11',end_date='2026-11-12',date_precision='exact'))
  tables['flights'].append(dict(id='flight-new-test',year=2026,months=['2026-11'],origin='IAH',destination='ATL',count_status='recorded_flown',purpose='transport'))
  tables['surface_routes'].append(dict(id='route-new-test',year=2026,months=['2026-11'],mode='Car',from_name='A',to_name='B',from_lat=34.0,from_lon=-112.0,to_lat=34.2,to_lon=-112.2))
  validate(tables,self.baseline)
  data=build_data(tables,self.baseline)
  feats={f['properties'].get('id'):f for f in data['geometry']['features']}
  self.assertEqual(feats['place-new-test']['geometry']['coordinates'],[-112,34])
  self.assertEqual(feats['flight-new-test']['properties']['mode'],'Plane')
  self.assertEqual(feats['route-new-test']['properties']['mode'],'Car')
  self.assertEqual(len(data['geometry']['features']),len(build_data(self.tables,self.baseline)['geometry']['features'])+3)
 def test_accidental_delete_rejected(self):
  tables=copy.deepcopy(self.tables);tables['places'].pop()
  with self.assertRaises(TravelDataError):validate(tables,self.baseline)
 def test_duplicate_country_special_case_preserved(self):
  dup=[r['iso2'] for r in self.tables['countries']]
  self.assertEqual(dup.count('GB'),2)
  self.assertEqual(dup.count('MD'),2)
if __name__=='__main__': unittest.main()
