#coding=utf8
from plone.app.testing import (IntegrationTesting, PLONE_FIXTURE, 
    PloneSandboxLayer)
from .config import PACKAGE_NAME
from Products.CMFCore.utils import getToolByName
from plone.dexterity.fti import DexterityFTI
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm, getVocabularyRegistry
from zope.component import provideUtility, getGlobalSiteManager, getSiteManager
from zope.schema.interfaces import IVocabularyFactory

TEST_CONTENT_TYPE_ID = 'TestContentType'

VOCABULARY_TUPLES = [
    (u'first_value', u'First Title'),
    (u'second_value', None),
]

VOCABULARY = SimpleVocabulary([SimpleTerm(value=v, title=t) for (v, t) in VOCABULARY_TUPLES])

def vocabulary_factory(context):
    return VOCABULARY

class PackageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.dexteritydiff
        import plone.app.dexterity
        self.loadZCML(package=collective.dexteritydiff)        
        self.loadZCML(package=plone.app.dexterity)

    def setUpPloneSite(self, portal):
        types_tool = getToolByName(portal, 'portal_types')
        
        sm = getSiteManager(portal)
        sm.registerUtility(
            component=vocabulary_factory, 
            provided=IVocabularyFactory, 
            name=u'collective.dexteritydiff.testing.VOCABULARY'
        )
        
        fti = DexterityFTI(
            TEST_CONTENT_TYPE_ID,
            factory=TEST_CONTENT_TYPE_ID,
            global_allow=True,
            behaviors=(
                'plone.app.versioningbehavior.behaviors.IVersionable',
                'plone.app.dexterity.behaviors.metadata.IBasic',
                'plone.app.dexterity.behaviors.metadata.IRelatedItems',
            ),
            model_source = '''
            <model xmlns="http://namespaces.plone.org/supermodel/schema">
                <schema>
                    <field name="text" type="zope.schema.Text">
                        <title>Text</title>
                        <required>False</required>
                    </field>
                    <field name="file" type="plone.namedfile.field.NamedFile">
                        <title>File</title>
                        <required>False</required>
                    </field>            
                    <field name="date" type="zope.schema.Date">
                        <title>Date</title>
                        <required>False</required>                        
                    </field>                      
                    <field name="files" type="zope.schema.List">
                        <title>Date</title>
                        <required>False</required>
                        <value_type type="plone.namedfile.field.NamedFile">
                            <title>Val</title>
                        </value_type>
                    </field>   
                    <field name="choice" type="zope.schema.Choice">
                        <title>Choice</title>
                        <required>False</required>
                        <vocabulary>collective.dexteritydiff.testing.VOCABULARY</vocabulary>
                    </field>                                                                       
                </schema>
            </model>
            '''
        )
        types_tool._setObject(TEST_CONTENT_TYPE_ID, fti)
        
        self['test_content_type_fti'] = fti
        

FIXTURE = PackageLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='%s:Integration' % PACKAGE_NAME)
