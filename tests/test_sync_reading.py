"""Run with: python -m unittest discover -s tests -v"""
import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.sync_reading import (DataError, parse_rows, validate_books,
                                  validate_months, save_pair, ROOT)


class ReadingSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / 'reading/sheets/Books.csv').open(encoding='utf-8-sig', newline='') as f:
            cls.books_csv = list(csv.reader(f))
        with (ROOT / 'reading/sheets/MonthlyPages.csv').open(encoding='utf-8-sig', newline='') as f:
            cls.pages_csv = list(csv.reader(f))

    def test_complete_archive_retained(self):
        books = validate_books(self.books_csv)
        pages = validate_months(self.pages_csv)
        self.assertEqual(len(books), 1412)
        self.assertEqual(len(pages), 84)
        self.assertEqual(sum(m['pages_read'] for m in pages), 471691)
        y2026 = [b for b in books if b['year'] == 2026]
        self.assertEqual(len(y2026), 93)
        self.assertEqual(len([b for b in y2026 if b['month'] == 1]), 15)
        self.assertEqual(len([b for b in y2026 if b['month'] == 3]), 6)
        self.assertEqual(len([b for b in y2026 if b['month'] == 4]), 26)
        self.assertEqual(len([b for b in y2026 if b['month'] == 11]), 3)
        self.assertTrue(all(b['status'] == 'Completed' for b in books))
        self.assertEqual(len({b['id'] for b in books}), 1412)

    def test_duplicate_book_id_rejected(self):
        rows = [list(r) for r in self.books_csv[:3]]
        rows[2][0] = rows[1][0]
        with self.assertRaisesRegex(DataError, 'duplicate BookID'):
            validate_books(rows)

    def test_invalid_month_date_rejected(self):
        rows = [list(r) for r in self.books_csv[:2]]
        rows[1][3] = '2026-13'
        with self.assertRaisesRegex(DataError, 'invalid CompletedDate'):
            validate_books(rows)

    def test_noncompleted_book_rejected(self):
        rows = [list(r) for r in self.books_csv[:2]]
        rows[1][5] = 'Reading'
        with self.assertRaisesRegex(DataError, 'status must be Completed'):
            validate_books(rows)

    def test_duplicated_pages_month_rejected(self):
        rows = self.pages_csv[:3] + [self.pages_csv[1]]
        with self.assertRaisesRegex(DataError, 'duplicate Year/Month'):
            validate_months(rows)

    def test_negative_pages_rejected(self):
        rows = [list(r) for r in self.pages_csv[:2]]
        rows[1][2] = '-4'
        with self.assertRaisesRegex(DataError, 'nonnegative number'):
            validate_months(rows)

    def test_no_partial_publication_on_bad_data(self):
        with tempfile.TemporaryDirectory() as temporary:
            d = Path(temporary)
            books = validate_books(self.books_csv)
            pages = validate_months(self.pages_csv)
            save_pair(d, books, pages)
            before = (d/'books.json').read_bytes()
            # A change dropping one book must not overwrite the published archive.
            with self.assertRaisesRegex(DataError, 'Refusing to remove'):
                save_pair(d, books[:-1], pages)
            self.assertEqual((d/'books.json').read_bytes(), before)
            self.assertEqual(len(json.loads(before)['books']), 1412)

    def test_unnumbered_new_book_appends_to_month(self):
        rows = [list(r) for r in self.books_csv]
        rows.append(['BK-001413', 'A Newly Completed Book', 'One Author', '2026-11', '', 'Completed'])
        out = validate_books(rows)
        sample = next(b for b in out if b['id'] == 'BK-001413')
        self.assertEqual((sample['year'], sample['month'], sample['month_order']), (2026, 11, 4))


if __name__ == '__main__':
    unittest.main()
