import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from ..choicediff import ChoiceDiff
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFDiffTool.interfaces import IDifference
from datetime import date
from ..testing import INTEGRATION_TESTING, TEST_CONTENT_TYPE_ID, VOCABULARY_TUPLES, VOCABULARY
from ..utils import title_or_value

class ChoiceDiffTestCase(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj1',
        )
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj2',
        )        
        
        self.obj1 = self.portal['obj1']
        self.obj2 = self.portal['obj2']  
        
                    
    def test_should_diff_choice_field(self):       
        self._test_diff_choice(VOCABULARY_TUPLES[0][0], VOCABULARY_TUPLES[0][0], True)        
        self._test_diff_choice(VOCABULARY_TUPLES[0][0], VOCABULARY_TUPLES[1][0], False)
        self._test_diff_choice(VOCABULARY_TUPLES[1][0], VOCABULARY_TUPLES[0][0], False)
        self._test_diff_choice(VOCABULARY_TUPLES[1][0], VOCABULARY_TUPLES[1][0], True)
        
        self._test_diff_choice(VOCABULARY_TUPLES[0][0], None, False)
        self._test_diff_choice(VOCABULARY_TUPLES[1][0], None, False)
        self._test_diff_choice(None, VOCABULARY_TUPLES[0][0], False)
        self._test_diff_choice(None, VOCABULARY_TUPLES[1][0], False)
        self._test_diff_choice(None, None, True)
    
    def _test_diff_choice(self, value1, value2, same):
        self.obj1.choice = value1
        self.obj2.choice = value2                
        diff = ChoiceDiff(self.obj1, self.obj2, 'choice')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertEqual(diff.same, same)
        
        inline_diff = diff.inline_diff()
        if same:
            self.assertFalse(inline_diff)
        else:
            if value1 is not None:
                self.assertTrue(title_or_value(VOCABULARY, value1) in inline_diff)
            if value2 is not None:
                self.assertTrue(title_or_value(VOCABULARY, value2) in inline_diff)
    
            
            
                           
                        