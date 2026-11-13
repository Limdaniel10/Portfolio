"""Test retention and BookID integrity for the separate Notion highlight archive."""
import copy,json,unittest
from scripts.sync_highlights import merge_highlights,HEADER
from scripts.sync_reading import ROOT,DataError

class HighlightSyncTests(unittest.TestCase):
    def setUp(self):
        self.payload=json.loads((ROOT/"reading/data/highlights.json").read_text(encoding="utf-8"))
        self.books=json.loads((ROOT/"reading/data/books.json").read_text(encoding="utf-8"))
        self.ids={b["id"] for b in self.books["books"]}
        self.rows=[list(HEADER)]
        for e in self.payload["entries"]:
            self.rows.append([e["id"],e["title"],e["author"],e.get("preview",""),"",e["notion_url"],
                              e.get("book_id",""),e.get("match_status",""),"Needs review",
                              e["source"],str(e["ordinal"])])
    def test_preserve_complete_notion_passages(self):
        result=merge_highlights(self.rows,self.payload,self.ids)
        self.assertEqual(len(result["entries"]),337)
        self.assertEqual([e["text"] for e in result["entries"]],
                         [e["text"] for e in self.payload["entries"]])
    def test_owner_can_link_title_variant(self):
        rows=copy.deepcopy(self.rows)
        row=next(r for r in rows if r[0]=="HII-028")
        row[6]="BK-000656"
        result=merge_highlights(rows,self.payload,self.ids)
        selected=next(x for x in result["entries"] if x["id"]=="HII-028")
        self.assertEqual(selected["book_id"],"BK-000656")
    def test_unknown_bookid_or_missing_highlight_is_rejected(self):
        rows=copy.deepcopy(self.rows)
        rows[1][6]="BK-unknown"
        with self.assertRaises(DataError):merge_highlights(rows,self.payload,self.ids)
        with self.assertRaises(DataError):merge_highlights(self.rows[:-1],self.payload,self.ids)

if __name__=="__main__":
    unittest.main()
