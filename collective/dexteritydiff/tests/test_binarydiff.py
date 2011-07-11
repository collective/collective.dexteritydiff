import unittest2 as unittest
from collective.dexteritydiff.testing import INTEGRATION_TESTING, TEST_CONTENT_TYPE_ID
from Products.CMFCore.utils import getToolByName
from collective.dexteritydiff.binarydiff import DexterityBinaryDiff
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFDiffTool.interfaces import IDifference
from plone.namedfile.file import NamedFile


class BinaryDiffTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING    
    
    def setUp(self):
        self.portal = self.layer['portal']    
        
    
    def test_should_detect_different_filename(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj1',
            file=NamedFile(data='contents', filename=u'blah.txt')
        )
        obj1 = self.portal['obj1']
        
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj2',
            file=NamedFile(data='contents', filename=u'bleh.txt') 
        )
        obj2 = self.portal['obj2']
                
        diff = DexterityBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertFalse(diff.same)
    
    def test_should_detect_different_data(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj1',
            file=NamedFile(data='contents', filename=u'f.txt')
        )
        obj1 = self.portal['obj1']
        
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj2',
            file=NamedFile(data='different contents', filename=u'f.txt') 
        )
        obj2 = self.portal['obj2']
                
        diff = DexterityBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertFalse(diff.same)
        
    def test_should_detect_same_data_and_filename(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj1',
            file=NamedFile(data='contents', filename=u'f.txt')
        )
        obj1 = self.portal['obj1']
        
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj2',
            file=NamedFile(data='contents', filename=u'f.txt') 
        )
        obj2 = self.portal['obj2']
                
        diff = DexterityBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertTrue(diff.same)        
