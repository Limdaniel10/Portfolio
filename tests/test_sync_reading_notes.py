"""Reading Notes automatically show only exact author/title Notion matches."""
import csv,unittest
from scripts.sync_reading_notes import validate_notes
from scripts.sync_reading import ROOT,DataError

class ReadingNotesTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/"reading/sheets/ReadingNotes.csv").open(encoding="utf-8",newline="") as f:
            self.rows=list(csv.reader(f))

    def test_182_recorded_reflections(self):
        self.assertEqual(len(self.rows)-1,182)
        notes=validate_notes(self.rows)
        self.assertEqual(len(notes),sum(1 for r in self.rows[1:] if r and r[10]=="TRUE"))
        self.assertGreaterEqual(len(notes),170)
        self.assertEqual(sum(bool(n["quote"]) for n in notes),
                         sum(r[9] in ("Quote approved","Notion exact match") and bool(r[6])
                             for r in self.rows[1:] if r and r[10]=="TRUE"))
        self.assertTrue(all(n["reflection"] and n["brunch_url"] for n in notes))

    def test_manual_approval_releases_quote(self):
        rows=[list(r) for r in self.rows]
        source=next(r for r in rows[1:] if len(r)>10 and r[6] and r[10]=="TRUE" and r[9]=="Reflection verified; quote pending")
        source[9]="Quote approved"
        notes=validate_notes(rows)
        self.assertEqual(next(n for n in notes if n["id"]==source[0])["quote"],source[6])

    def test_unreviewed_title_only_quote_stays_hidden(self):
        notes=validate_notes(self.rows)
        self.assertTrue(any(n["verification"]=="Reflection verified; quote pending" and not n["quote"] for n in notes))

    def test_hidden_reflections_stay_hidden(self):
        rows=[list(r) for r in self.rows]
        initial=len(validate_notes(rows))
        source=next(r for r in rows[1:] if r[10]=="TRUE")
        source[10]="FALSE"
        self.assertEqual(len(validate_notes(rows)),initial-1)

    def test_missing_author_rejected(self):
        rows=[list(r) for r in self.rows]
        source=next(r for r in rows[1:] if r[10]=="TRUE")
        source[3]=""
        with self.assertRaises(DataError):
            validate_notes(rows)

if __name__=="__main__":
    unittest.main()
