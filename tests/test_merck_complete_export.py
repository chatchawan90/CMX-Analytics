import csv
from decimal import Decimal
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from project.merck_complete_export import export_all_revenue


class CompleteExportTests(unittest.TestCase):
    def setUp(self):
        self.raw = pd.DataFrame({
            'docuno': ['IVZ1'] * 4,
            'ลำดับ': [1, 2, 3, 3],
            'รหัสสินค้า': ['abc', 'abc', 'unknown', 'unknown'],
            'รายละเอียดสินค้า': ['Original'] * 4,
            'แบรนด์': ['Merck', 'Merck', 'Sigma', 'Sigma'],
            'ยอดมูลค่าขายและลดหนี้ก่อนVAT': [
                Decimal('100.10'), Decimal('200.20'), Decimal('-25.05'), Decimal('-25.05')],
        })
        self.first = self.raw.copy()
        self.first['รหัสสินค้า'] = self.first['รหัสสินค้า'].str.upper()
        self.first['found'] = False
        self.lookup = pd.DataFrame({
            'รหัสสินค้า': ['ABC'],
            'รายละเอียดสินค้า': ['Catalog description'],
            'business_unit_desc': ['Chemistry'],
            'business_field_desc': ['Analytical'],
            'sbu_description': ['Solvents'],
        })

    def export(self, first=None, lookup=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'all.csv'
            result = export_all_revenue(
                self.raw, self.first if first is None else first,
                self.lookup if lookup is None else lookup, path)
            with path.open(encoding='utf-8-sig', newline='') as stream:
                rows = list(csv.DictReader(stream))
        return result, rows

    def test_preserves_unmatched_repeated_and_identical_source_rows_in_csv(self):
        result, rows = self.export()
        pd.testing.assert_frame_equal(result[self.raw.columns], self.raw)
        self.assertEqual(len(rows), 4)
        self.assertEqual([r['ลำดับ'] for r in rows], ['1', '2', '3', '3'])
        self.assertEqual(sum(Decimal(r['ยอดมูลค่าขายและลดหนี้ก่อนVAT']) for r in rows),
                         Decimal('250.20'))
        self.assertEqual([r['business_unit_desc'] for r in rows],
                         ['Chemistry', 'Chemistry', '', ''])
        self.assertEqual(result['found'].tolist(), [True, True, False, False])

    def test_keeps_first_match_and_uses_fallback_only_for_unmatched_rows(self):
        self.first['business_unit_desc'] = ['Biology', None, None, None]
        self.first.loc[0, 'found'] = True
        result, _ = self.export()
        self.assertEqual(result.loc[0, 'business_unit_desc'], 'Biology')
        self.assertEqual(result.loc[1, 'business_unit_desc'], 'Chemistry')

    def test_exports_when_no_products_match(self):
        result, rows = self.export(lookup=self.lookup.iloc[:0])
        self.assertEqual(len(rows), 4)
        self.assertFalse(result['found'].any())
        self.assertTrue(result['business_unit_desc'].isna().all())

    def test_rejects_duplicate_lookup_keys_instead_of_multiplying_revenue(self):
        with self.assertRaises(ValueError):
            self.export(lookup=pd.concat([self.lookup, self.lookup], ignore_index=True))

    def test_rejects_lost_or_reordered_first_pass_rows(self):
        for first in (self.first.iloc[:3], self.first.iloc[::-1]):
            with self.subTest(rows=len(first)), self.assertRaises(ValueError):
                self.export(first=first)


if __name__ == '__main__':
    unittest.main()
