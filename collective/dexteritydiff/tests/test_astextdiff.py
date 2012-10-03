from collective.dexteritydiff.astextdiff import AsTextDiff
from datetime import date
from Products.CMFDiffTool.interfaces import IDifference

import unittest2 as unittest


class DummyType(object):
    def __init__(self, date):
        self.date = date


class AsTextDiffTestCase(unittest.TestCase):

    def test_should_diff_anything_as_text(self):
        self._test_diff_date(date(2011, 1, 1), date(2012, 2, 2), False)
        self._test_diff_date(date(2011, 1, 1), date(2011, 1, 1), True)
        self._test_diff_date(date(2011, 1, 1), None, False)
        self._test_diff_date(None, None, True)

    def _test_diff_date(self, d1, d2, same):
        diff = AsTextDiff(DummyType(d1), DummyType(d2), 'date')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertEqual(diff.same, same)

        inline_diff = diff.inline_diff()
        if same:
            self.assertFalse(inline_diff)
        else:
            self.assertTrue(inline_diff)
            if d1 is not None:
                self.assertTrue(str(d1) in inline_diff)
            if d2 is not None:
                self.assertTrue(str(d2) in inline_diff)

            #self.assertFalse('None' in inline_diff)
