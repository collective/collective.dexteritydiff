import unittest2 as unittest
from collective.dexteritydiff.testing import INTEGRATION_TESTING, TEST_CONTENT_TYPE_ID
from Products.CMFCore.utils import getToolByName
from ..booldiff import BoolDiff
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFDiffTool.interfaces import IDifference
from datetime import date

class DummyType(object):
    def __init__(self, bool_field):
        self.bool_field = bool_field

class BoolDiffTestCase(unittest.TestCase):
    
    def setUp(self):
        pass    
            
    def test_should_diff_boolean_fields(self):                
        self._test_diff_bool(False, False, True)
        self._test_diff_bool(False, True, False)
        self._test_diff_bool(True, False, False)
        self._test_diff_bool(True, True, True)
        
        self._test_diff_bool(False, None, False)
        
        self._test_diff_bool(True, None, False)
        self._test_diff_bool(None, False, False)
        self._test_diff_bool(None, True, False)
        self._test_diff_bool(None, None, True)
    
    def _test_diff_bool(self, b1, b2, same):
        diff = BoolDiff(DummyType(b1), DummyType(b2), 'bool_field')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertEqual(diff.same, same)
        
        inline_diff = diff.inline_diff()
        if same:
            self.assertFalse(inline_diff)
        else:
            self.assertTrue(('True' in inline_diff) or ('False' in inline_diff))
            #self.assertFalse('None' in inline_diff)
            
            
                           
                        