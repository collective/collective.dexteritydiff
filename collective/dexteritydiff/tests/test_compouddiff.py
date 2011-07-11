import unittest2 as unittest
from collective.dexteritydiff.testing import INTEGRATION_TESTING, TEST_CONTENT_TYPE_ID
from Products.CMFCore.utils import getToolByName
from collective.dexteritydiff.compounddiff import DexterityCompoundDiff
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFDiffTool.interfaces import IDifference


class CompoundDiffTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING    
    
    def setUp(self):
        self.portal = self.layer['portal']    
        
    
    def test_should_diff(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj1', 
            title=u'Object 1', 
            description=u'Desc 1', 
            text=u'Text 1'
        )
        obj1 = self.portal['obj1']
        
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj2', 
            title=u'Object 2',
            text=u'Text 2'
        )
        obj2 = self.portal['obj2']
        
        diffs = DexterityCompoundDiff(obj1, obj2, 'any')
        self.assertEqual(4, len(diffs))
        for d in diffs:
            self.assertTrue(IDifference.providedBy(d))
        
        
        
        
        
        
        
        
        
