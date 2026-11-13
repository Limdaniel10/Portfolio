"""182 original Brunch book entries: exact Notion quotes and source-only placeholders."""
import csv,unittest
from scripts.sync_reading_notes import validate_notes
from scripts.sync_reading import ROOT,DataError

class ReadingNotesTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/"reading/sheets/ReadingNotes.csv").open(encoding="utf-8",newline="") as f:
            self.rows=list(csv.reader(f))

    def test_full_182_archive(self):
        self.assertEqual(len(self.rows)-1,182)
        notes=validate_notes(self.rows)
        self.assertEqual(len(notes),182)
        self.assertEqual(sum(bool(n["reflection"]) for n in notes),175)
        self.assertEqual(sum(bool(n["quote"]) for n in notes),
                         sum(r[9] in ("Quote approved","Notion exact match") and bool(r[6])
                             for r in self.rows[1:] if r and r[10]=="TRUE"))
        self.assertTrue(all(n["title"] and n["author"] and n["brunch_url"] for n in notes))
        self.assertTrue(all(n["verification"]=="Needs review" for n in notes if not n["reflection"]))

    def test_manual_approval_releases_quote(self):
        rows=[list(r) for r in self.rows]
        source=next(r for r in rows[1:] if r[6] and r[10]=="TRUE" and r[9]=="Reflection verified; quote pending")
        source[9]="Quote approved"
        notes=validate_notes(rows)
        self.assertEqual(next(n for n in notes if n["id"]==source[0])["quote"],source[6])

    def test_unreviewed_quote_hidden(self):
        notes=validate_notes(self.rows)
        self.assertTrue(any(n["verification"]=="Reflection verified; quote pending" and not n["quote"] for n in notes))

    def test_source_only_reflection_requires_review(self):
        rows=[list(r) for r in self.rows]
        source=next(r for r in rows[1:] if not r[5])
        source[9]="Quote approved"
        with self.assertRaises(DataError):
            validate_notes(rows)

    def test_hidden_item_not_published(self):
        rows=[list(r) for r in self.rows]
        source=next(r for r in rows[1:] if r[10]=="TRUE")
        source[10]="FALSE"
        self.assertEqual(len(validate_notes(rows)),181)

    def test_missing_author_rejected(self):
        rows=[list(r) for r in self.rows]
        source=next(r for r in rows[1:] if r[10]=="TRUE")
        source[3]=""
        with self.assertRaises(DataError):
            validate_notes(rows)
if __name__=="__main__":
    unittest.main()
