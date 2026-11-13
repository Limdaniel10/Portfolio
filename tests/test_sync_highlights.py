"""Google Sheets is the canonical source of all highlights and classification."""
import copy,json,unittest
from scripts.sync_highlights import merge_highlights,HEADER
from scripts.sync_reading import ROOT,DataError

class HighlightSyncTests(unittest.TestCase):
    def setUp(self):
        self.snapshot=json.loads((ROOT/"reading/data/highlights.json").read_text(encoding="utf-8"))
        self.books=json.loads((ROOT/"reading/data/books.json").read_text(encoding="utf-8"))
        self.ids={b["id"] for b in self.books["books"]}
        self.rows=[list(HEADER)]
        for e in self.snapshot["entries"]:
            self.rows.append([e["id"],e["title"],e["author"],e["preview"],"","",
                              e["book_id"],e["match_status"],e["review_status"],
                              e["source"],str(e["ordinal"]),e["text"],
                              e["suggested_book_id"],e["suggested_title"]])
    def test_sheet_text_is_canonical(self):
        rows=copy.deepcopy(self.rows)
        rows[1][11]="Newly corrected passage from Google Sheets"
        updated=merge_highlights(rows,self.snapshot,self.ids)
        self.assertEqual(updated["entries"][0]["text"],rows[1][11])
        self.assertEqual(len(updated["entries"]),337)
    def test_linking_is_explicit_not_proposed(self):
        result=merge_highlights(self.rows,self.snapshot,self.ids)
        suggested=next(e for e in result["entries"] if e.get("suggested_book_id"))
        self.assertFalse(suggested["book_id"])
        self.assertEqual(suggested["review_status"],"Suggested match")
        rows=copy.deepcopy(self.rows)
        target=next(r for r in rows if r[0]==suggested["id"])
        target[6]=target[12]
        target[8]="Approved"
        updated=merge_highlights(rows,self.snapshot,self.ids)
        self.assertEqual(next(e for e in updated["entries"] if e["id"]==suggested["id"])["book_id"],target[6])
    def test_unfinished_separated(self):
        rows=copy.deepcopy(self.rows)
        missing=next(r for r in rows[1:] if not r[6])
        missing[8]="Unfinished"
        result=merge_highlights(rows,self.snapshot,self.ids)
        entry=next(e for e in result["entries"] if e["id"]==missing[0])
        self.assertEqual(entry["review_status"],"Unfinished")
    def test_new_sheet_row_is_allowed(self):
        rows=copy.deepcopy(self.rows)
        rows.append(["NEW-001","New book","Example writer","First passage","","",
                     "","","Needs review","New","1","First passage","",""])
        result=merge_highlights(rows,self.snapshot,self.ids)
        self.assertEqual(len(result["entries"]),338)
    def test_missing_bookids_and_deleted_records_rejected(self):
        rows=copy.deepcopy(self.rows)
        rows[1][6]="BK-no-such-book"
        with self.assertRaises(DataError):merge_highlights(rows,self.snapshot,self.ids)
        with self.assertRaises(DataError):merge_highlights(self.rows[:-1],self.snapshot,self.ids)
    def test_unfinished_cannot_count_as_completed(self):
        rows=copy.deepcopy(self.rows)
        rows[1][8]="Unfinished"
        with self.assertRaises(DataError):merge_highlights(rows,self.snapshot,self.ids)

if __name__=="__main__":
    unittest.main()
