from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class NotesKbtic(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import notes.kbtic
        xmlconfig.file('configure.zcml',
                       notes.kbtic,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'notes.kbtic:default')

NOTES_KBTIC_FIXTURE = NotesKbtic()
NOTES_KBTIC_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(NOTES_KBTIC_FIXTURE, ),
                       name="NotesKbtic:Integration")