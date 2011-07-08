import unittest2 as unittest
from collective.dexteritydiff.testing import INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
from collective.dexteritydiff.compounddiff import DexterityCompoundDiff

class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING    
    
    def setUp(self):
        self.portal = self.layer['portal']    
        self.diff_tool = getToolByName(self.portal, 'portal_diff')
    
    def test_grupo_site_admin_deve_ter_as_roles_corretas(self):
        self.assertIn(DexterityCompoundDiff.meta_type, self.diff_tool.listDiffTypes())
        self.assertTrue(self.diff_tool.getDiffType(DexterityCompoundDiff.meta_type))
        
        
        
        
