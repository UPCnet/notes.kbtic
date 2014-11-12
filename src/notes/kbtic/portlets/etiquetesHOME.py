# -*- coding: utf-8 -*-

from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory('notes.kbtic')
from Products.CMFPlone import PloneMessageFactory as _


class IEtiquetesHOMEPortlet(IPortletDataProvider):
    """ Defines a new portlet
    """


class Assignment(base.Assignment):
    """ Assigner for portlet. """
    implements(IEtiquetesHOMEPortlet)
    title = _(u"Etiquetes HOME", default=u'Etiquetes HOME')


class Renderer(base.Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    render = ViewPageTemplateFile('etiquetesHOME.pt')

    def mostrarEtiquetesCategory1(self):
        """ Mostra etiquetes "Categories Servei"
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
        """ Mostra etiquetes "Categories Servei PPS"
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
        """ Mostra etiquetes "By Category (KBTIC-RIN)"
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
        """ Mostra etiquetes "By Category (ADS-SPO)"
        """
        from zope.component.hooks import getSite
        portal = getSite()
        results = []

        keys = [result for result in portal.uid_catalog.searchResults(portal_type='SimpleVocabularyTerm', sort_on='Title')
              if 'categoryADS' in result.getPath()]

        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()