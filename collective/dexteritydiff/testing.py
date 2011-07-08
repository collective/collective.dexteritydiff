#coding=utf8
from plone.app.testing import (IntegrationTesting, PLONE_FIXTURE, 
    PloneSandboxLayer)
from .config import PACKAGE_NAME

class PackageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.dexteritydiff
        self.loadZCML(package=collective.dexteritydiff)                

FIXTURE = PackageLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='%s:Integration' % PACKAGE_NAME)
