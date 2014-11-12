# -*- coding: utf-8 -*-

from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory('notes.kbtic')
from Products.CMFPlone import PloneMessageFactory as _


class IEtiquetesPortlet(IPortletDataProvider):
    """ Defines a new portlet
    """


class Assignment(base.Assignment):
    """ Assigner for portlet. """
    implements(IEtiquetesPortlet)
    title = _(u"Etiquetes KBTIC", default=u'Etiquetes KBTIC')


class Renderer(base.Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    render = ViewPageTemplateFile('etiquetes.pt')

    def mostrarEtiquetesCategory1(self):
        """ Categories Servei
        """
        from zope.component.hooks import getSite
        portal = getSite()
        results = []
        keys = [result for result in portal.uid_catalog.searchResults(portal_type='SimpleVocabularyTerm', sort_on='Title')
              if 'category1' in result.getPath()]

        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results

    def mostrarEtiquetesCategory2(self):
        """ Categories Servei PPS
        """
        from zope.component.hooks import getSite
        portal = getSite()
        results = []

        keys = [result for result in portal.uid_catalog.searchResults(portal_type='SimpleVocabularyTerm', sort_on='Title')
              if 'category2' in result.getPath()]

        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results

    def mostrarEtiquetesCategory3(self):
        """ By Category (KBTIC-RIN)
        """
        from zope.component.hooks import getSite
        portal = getSite()
        results = []
        keys = [result for result in portal.uid_catalog.searchResults(portal_type='SimpleVocabularyTerm', sort_on='Title')
              if 'category3' in result.getPath()]

        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results

    def mostrarEtiquetesCategoryADS(self):
        """ By Category (ADS-SPO)
        """
        from zope.component.hooks import getSite
        portal = getSite()
        results = []

        keys = [result for result in portal.uid_catalog.searchResults(portal_type='SimpleVocabularyTerm', sort_on='Title')
              if 'categoryADS' in result.getPath()]

        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results


    def mostrarEtiquetes(self):
        """ Etiquetes del sistema
        """
        indexName='Subject'
        catalog = getToolByName(self, 'portal_catalog')
        keywords = list(catalog.uniqueValuesFor(indexName))
        keywords.sort(key=lambda x:x.lower())
        return keywords    


    def getKeywordIndexes(self):
        """Gets a list of indexes from the catalog. Uses config.py to choose the
        meta type and filters out a subset of known indexes that should not be
        managed.
        """
        IGNORE_INDEXES = [
            'object_provides',
            'allowedRolesAndUsers',
            'getRawRelatedItems',
            'getEventType',
        ]        
        catalog = getToolByName(self, 'portal_catalog')
        idxs = catalog.index_objects()
        idxs = [i.id for i in idxs if i.meta_type == 'KeywordIndex' and
                i.id not in IGNORE_INDEXES]
        idxs.sort()
        return idxs


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
