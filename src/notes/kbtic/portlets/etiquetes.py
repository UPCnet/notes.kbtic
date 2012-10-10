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
    title = _(u"Portlet Etiquetes", default=u'Portlet etiquetes')


class Renderer(base.Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    render = ViewPageTemplateFile('etiquetes.pt')

    def mostrarEtiquetesCategory1(self):
        """ Busca etiquetes dintre del portal_vocabulary segons idioma
        """
        urltool = getToolByName(self.context, 'portal_url')
        path = urltool.getPortalPath()

        results = []
        path = path + '/portal_vocabularies/category1_keywords'
        keys = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm',
                                                             path={'query': path, 'depth': 1, },
                                                             sort_on='getObjPositionInParent')
        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results

    def mostrarEtiquetesCategory2(self):
        """ Busca etiquetes dintre del portal_vocabulary segons idioma
        """
        urltool = getToolByName(self.context, 'portal_url')
        path = urltool.getPortalPath()

        results = []
        path = path + '/portal_vocabularies/category2_keywords'
        keys = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm',
                                                             path={'query': path, 'depth': 1, },
                                                             sort_on='getObjPositionInParent')
        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results

    def mostrarEtiquetesCategory3(self):
        """ Busca etiquetes dintre del portal_vocabulary segons idioma
        """
        urltool = getToolByName(self.context, 'portal_url')
        path = urltool.getPortalPath()

        results = []
        path = path + '/portal_vocabularies/category3_keywords'
        keys = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm',
                                                             path={'query': path, 'depth': 1, },
                                                             sort_on='getObjPositionInParent')
        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results

    def mostrarEtiquetesCategory4(self):
        """ Busca etiquetes dintre del portal_vocabulary segons idioma
        """
        urltool = getToolByName(self.context, 'portal_url')
        path = urltool.getPortalPath()

        results = []
        path = path + '/portal_vocabularies/category4_keywords'
        keys = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm',
                                                             path={'query': path, 'depth': 1, },
                                                             sort_on='getObjPositionInParent')
        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results

    def mostrarEtiquetesCategoryCSPT(self):
        """ Busca etiquetes dintre del portal_vocabulary segons idioma
        """
        urltool = getToolByName(self.context, 'portal_url')
        path = urltool.getPortalPath()

        results = []
        path = path + '/portal_vocabularies/categoryCSPT_keywords'
        keys = self.context.portal_catalog.searchResults(portal_type='SimpleVocabularyTerm',
                                                             path={'query': path, 'depth': 1, },
                                                             sort_on='getObjPositionInParent')
        for value in keys:
            results.append({'id': value.id, 'title': value.Title})

        return results


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
