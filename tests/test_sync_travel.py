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
  self.assertEqual(sum(c['count_in_195'] for c in data['countries']),90)
  self.assertGreaterEqual(len(data['geometry']['features']),len(self.baseline['geometry']['features']))
  self.assertEqual(data['country_basis'],194)
  self.assertIn('Bus',data['transport_modes'])
  rs=[f for f in data['geometry']['features'] if f['properties']['kind']=='surface_route']
  self.assertEqual(len(rs),len([f for f in self.baseline['geometry']['features'] if f['properties']['kind']=='surface_route'])+1)
  self.assertTrue(any(f['properties']['from_name']=='Moscow' and f['properties']['to_name']=='Irkutsk' for f in rs))
  self.assertEqual(len(data['places']),282)
  self.assertEqual(len(data['domestic_places']),69)
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
