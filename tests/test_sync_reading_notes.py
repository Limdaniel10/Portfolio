"""Reading Notes preserve original reflections and hide quotes pending approval."""
import csv,unittest
from scripts.sync_reading_notes import validate_notes
from scripts.sync_reading import ROOT,DataError
class ReadingNotesTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/"reading/sheets/ReadingNotes.csv").open(encoding="utf-8",newline="") as f:
            self.rows=list(csv.reader(f))
    def test_reflections(self):
        notes=validate_notes(self.rows)
        self.assertEqual(len(notes),4)
        self.assertTrue(all(n["reflection"] and n["brunch_url"] for n in notes))
        self.assertTrue(all(n["quote"]=="" for n in notes))
    def test_quote_approval(self):
        rows=[list(x) for x in self.rows]
        rows[1][9]="Quote approved"
        notes=validate_notes(rows)
        self.assertEqual(next(n for n in notes if n["id"]==rows[1][0])["quote"],rows[1][6])
    def test_hidden(self):
        rows=[list(x) for x in self.rows]
        rows[2][10]="FALSE"
        self.assertEqual(len(validate_notes(rows)),3)
    def test_missing_author_rejected(self):
        rows=[list(x) for x in self.rows]
        rows[1][3]=""
        with self.assertRaises(DataError):
            validate_notes(rows)
if __name__=="__main__":
    unittest.main()
