"""Public Reading Notes reflect the live reviewed source, not the book ledger."""
import csv,unittest
from scripts.sync_reading_notes import validate_notes
from scripts.sync_reading import ROOT,DataError

class ReadingNotesTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/"reading/sheets/ReadingNotes.csv").open(encoding="utf-8",newline="") as f:
            self.rows=list(csv.reader(f))

    def test_182_recorded_reflections(self):
        self.assertEqual(len(self.rows)-1,182)
        approved=validate_notes(self.rows)
        self.assertEqual(len(approved),sum(1 for r in self.rows[1:] if r and r[10]=="TRUE"))
        self.assertGreaterEqual(len(approved),170)
        self.assertTrue(all(n["reflection"] and n["brunch_url"] for n in approved))
        self.assertTrue(all(n["quote"]=="" for n in approved))

    def test_quote_must_be_approved(self):
        rows=[list(r) for r in self.rows]
        source=next(r for r in rows[1:] if len(r)>10 and r[6] and r[10]=="TRUE")
        source[9]="Quote approved"
        notes=validate_notes(rows)
        matching=next(n for n in notes if n["id"]==source[0])
        self.assertEqual(matching["quote"],source[6])

    def test_hidden_reflections_stay_hidden(self):
        rows=[list(r) for r in self.rows]
        original=len(validate_notes(rows))
        source=next(r for r in rows[1:] if r[10]=="TRUE")
        source[10]="FALSE"
        self.assertEqual(len(validate_notes(rows)),original-1)

    def test_missing_author_rejected(self):
        rows=[list(r) for r in self.rows]
        source=next(r for r in rows[1:] if r[10]=="TRUE")
        source[3]=""
        with self.assertRaises(DataError):
            validate_notes(rows)
if __name__=="__main__":
    unittest.main()
