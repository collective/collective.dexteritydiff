import unittest2 as unittest
from ..testing import INTEGRATION_TESTING, TEST_CONTENT_TYPE_ID
from Products.CMFCore.utils import getToolByName
from ..compounddiff import DexterityCompoundDiff, EXCLUDED_FIELDS
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFDiffTool.interfaces import IDifference
from datetime import date
from plone.namedfile import NamedFile

class CompoundDiffTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING    
    
    def setUp(self):
        self.portal = self.layer['portal']    
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
    
    def test_should_diff(self):        
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
        for d in diffs:
            self.assertTrue(IDifference.providedBy(d))
            self.assertNotIn(d.field, EXCLUDED_FIELDS)
            if d.field in ['title', 'description', 'text']:
                self.assertFalse(d.same, 'Field %s should be different.' % d.field)
            else:
                self.assertTrue(d.same, 'Field %s should be equal.' % d.field)
        
    def test_should_provide_inline_diff_for_date_field(self):        
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj1', 
            date=date(2001, 1, 1), 
        )
        obj1 = self.portal['obj1']
        
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj2', 
            date=date(2001, 1, 2),
        )
        obj2 = self.portal['obj2']
               
        diffs = DexterityCompoundDiff(obj1, obj2, 'any')        
        for d in diffs:
            if d.field == 'date':                
                self.assertTrue(d.inline_diff())
        
    def test_should_provide_inline_diff_for_file_list_field(self):
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj1', 
            files=None, 
        )
        obj1 = self.portal['obj1']
        
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj2', 
            files=[NamedFile(data='data', filename=u'a.txt')],
        )
        obj2 = self.portal['obj2']
               
        diffs = DexterityCompoundDiff(obj1, obj2, 'any')        
        for d in diffs:
            if d.field == 'files':                
                inline_diff = d.inline_diff()
                self.assertTrue(inline_diff)         
                self.assertTrue(obj2.files[0].filename in inline_diff)
        
        
        
