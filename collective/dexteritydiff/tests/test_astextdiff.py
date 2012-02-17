import unittest2 as unittest
from collective.dexteritydiff.testing import INTEGRATION_TESTING, TEST_CONTENT_TYPE_ID
from Products.CMFCore.utils import getToolByName
from ..astextdiff import AsTextDiff
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFDiffTool.interfaces import IDifference
from datetime import date

class DummyType(object):
    def __init__(self, date):
        self.date = date

class AsTextDiffTestCase(unittest.TestCase):
    
    def setUp(self):
        pass    
            
    def test_should_diff_anything_as_text(self):                
        self._test_diff_date(date(2011, 1, 1), date(2012, 2, 2), False)
        self._test_diff_date(date(2011, 1, 1), date(2011, 1, 1), True)
        self._test_diff_date(date(2011, 1, 1), None, False)
        self._test_diff_date(None, None, True)
    
    def _test_diff_date(self, d1, d2, same):
        diff = AsTextDiff(DummyType(d1), DummyType(d2), 'date')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertEqual(diff.same, same)
        self.assertNotEqual(bool(diff.inline_diff()), same)               